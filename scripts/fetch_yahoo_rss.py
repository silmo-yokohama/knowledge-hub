#!/usr/bin/env python3
"""
Yahoo ニュース RSS フィード取得スクリプト

指定されたフィードからYahoo ニュースの最新記事をRSSから取得し、
JSON形式で標準出力に出力する。

フィード定義は yahoo_rss_feeds.json から読み込む。
フィードの追加・削除は JSON ファイルを編集するだけで反映される。

使い方:
    python3 fetch_yahoo_rss.py [フィードキー...]

例:
    # 全フィードを取得（デフォルト）
    python3 fetch_yahoo_rss.py

    # 特定のフィードのみ取得
    python3 fetch_yahoo_rss.py it sports fullcount

    # 利用可能なフィード一覧を表示
    python3 fetch_yahoo_rss.py --list
"""

import sys
import json
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

# User-Agentヘッダ（外部API利用ルールに準拠）
USER_AGENT = "knowledge-hub/0.1"

# フィード定義ファイルのパス（スクリプトと同じディレクトリ）
FEEDS_CONFIG_PATH = Path(__file__).parent / "yahoo_rss_feeds.json"


def load_feeds() -> dict[str, dict]:
    """
    JSONファイルからフィード定義を読み込み、フラットな辞書として返す。

    categories と media の区分を維持しつつ、
    フィードキーでアクセスできるフラットな辞書に変換する。

    Returns:
        {フィードキー: {"url": ..., "label": ..., "group": ...}} の辞書
    """
    with open(FEEDS_CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    feeds = {}
    for group_name, group_feeds in config.items():
        # _comment キーはスキップ
        if group_name.startswith("_"):
            continue
        for key, feed_data in group_feeds.items():
            if key.startswith("_"):
                continue
            feeds[key] = {
                "url": feed_data["url"],
                "label": feed_data["label"],
                "group": group_name,
            }
    return feeds


def print_feed_list(feeds: dict[str, dict]):
    """
    利用可能なフィード一覧を見やすく表示する。

    Args:
        feeds: フィード定義の辞書
    """
    # グループごとに分類して表示
    groups: dict[str, list[tuple[str, str]]] = {}
    for key, data in feeds.items():
        group = data["group"]
        if group not in groups:
            groups[group] = []
        groups[group].append((key, data["label"]))

    print("利用可能なフィード一覧:")
    print()
    for group_name, items in groups.items():
        print(f"  [{group_name}]")
        for key, label in sorted(items):
            print(f"    {key:<15} - {label}")
        print()


def fetch_rss(url: str) -> str:
    """
    指定URLのRSSフィードを取得する。

    Args:
        url: RSSフィードのURL

    Returns:
        RSSフィードのXML文字列

    Raises:
        urllib.error.URLError: HTTPリクエスト失敗時
    """
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=15) as response:
        return response.read().decode("utf-8")


def parse_rss(xml_text: str, feed_key: str, feeds: dict[str, dict]) -> list[dict]:
    """
    RSS 2.0形式のXMLをパースして記事情報のリストを返す。

    Args:
        xml_text: RSSフィードのXML文字列
        feed_key: フィードを識別するキー名
        feeds: フィード定義の辞書

    Returns:
        記事情報の辞書リスト
    """
    root = ET.fromstring(xml_text)
    articles = []

    # RSS 2.0 形式: channel > item
    channel = root.find("channel")
    if channel is None:
        return articles

    for item in channel.findall("item"):
        title_el = item.find("title")
        link_el = item.find("link")
        description_el = item.find("description")
        pub_date_el = item.find("pubDate")

        # タイトルからメディア名を抽出（括弧内の文字列）
        title_text = title_el.text if title_el is not None and title_el.text else ""
        source = ""
        if "(" in title_text and title_text.endswith(")"):
            source = title_text[title_text.rfind("(") + 1 : -1]

        article = {
            "title": title_text,
            "url": link_el.text if link_el is not None and link_el.text else "",
            "date": pub_date_el.text if pub_date_el is not None and pub_date_el.text else "",
            "source": source,
            "feed": feed_key,
            "feed_label": feeds[feed_key]["label"],
            "description": description_el.text if description_el is not None and description_el.text else "",
        }
        articles.append(article)

    return articles


def deduplicate_articles(articles: list[dict]) -> list[dict]:
    """
    URLベースで重複記事を除去する。

    Args:
        articles: 記事情報の辞書リスト

    Returns:
        重複を除いた記事情報の辞書リスト
    """
    seen_urls = set()
    unique_articles = []
    for article in articles:
        url = article["url"]
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_articles.append(article)
    return unique_articles


def main():
    """メイン処理: フィードごとにRSSを取得してJSONとして出力する。"""
    # フィード定義を読み込み
    feeds = load_feeds()

    # --list オプション: フィード一覧を表示して終了
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        print_feed_list(feeds)
        sys.exit(0)

    # コマンドライン引数からフィードキーを取得（なければ全フィード）
    feed_keys = sys.argv[1:] if len(sys.argv) > 1 else list(feeds.keys())

    # 無効なフィードキーのチェック
    valid_keys = list(feeds.keys())
    for key in feed_keys:
        if key not in valid_keys:
            print(
                json.dumps(
                    {"error": f"無効なフィードキー: {key}", "valid_keys": valid_keys},
                    ensure_ascii=False,
                ),
                file=sys.stderr,
            )
            sys.exit(1)

    all_articles = []
    errors = []

    for i, key in enumerate(feed_keys):
        # フィード間でレート制限対策のスリープ（1秒以上）
        if i > 0:
            time.sleep(1)

        try:
            xml_text = fetch_rss(feeds[key]["url"])
            articles = parse_rss(xml_text, key, feeds)
            all_articles.extend(articles)
        except Exception as e:
            errors.append({"feed": key, "error": str(e)})

    # 複数フィード間での重複を除去
    unique_articles = deduplicate_articles(all_articles)

    # 結果をJSON出力
    result = {
        "fetched_at": datetime.now().isoformat(),
        "feeds": feed_keys,
        "total_before_dedup": len(all_articles),
        "total": len(unique_articles),
        "articles": unique_articles,
    }

    # エラーがあった場合は含める
    if errors:
        result["errors"] = errors

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
