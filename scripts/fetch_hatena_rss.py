#!/usr/bin/env python3
"""
はてなブックマーク人気エントリーRSSフィード取得スクリプト

指定されたカテゴリのはてなブックマーク人気エントリーをRSSから取得し、
JSON形式で標準出力に出力する。

使い方:
    python3 fetch_hatena_rss.py [カテゴリ...]

例:
    python3 fetch_hatena_rss.py it knowledge economics

カテゴリ一覧:
    it           - テクノロジー
    knowledge    - 学び
    economics    - 政治経済
    entertainment - エンタメ
    game         - アニメとゲーム
"""

import sys
import json
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

# RSSフィードのベースURL
HATENA_RSS_BASE = "https://b.hatena.ne.jp/hotentry/{category}.rss"

# User-Agentヘッダ（はてなAPI利用時に必須）
USER_AGENT = "knowledge-hub/0.1"

# 有効なカテゴリ一覧
VALID_CATEGORIES = ["it", "knowledge", "economics", "entertainment", "game"]

# デフォルトカテゴリ（引数なし実行時）
DEFAULT_CATEGORIES = ["it", "knowledge", "economics"]

# RSSの名前空間定義
NAMESPACES = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rss": "http://purl.org/rss/1.0/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "hatena": "http://www.hatena.ne.jp/info/xmlns#",
    "taxo": "http://purl.org/rss/1.0/modules/taxonomy/",
}


def fetch_rss(category: str) -> str:
    """
    指定カテゴリのはてなブックマークRSSフィードを取得する。

    Args:
        category: はてなブックマークのカテゴリ名

    Returns:
        RSSフィードのXML文字列

    Raises:
        urllib.error.URLError: HTTPリクエスト失敗時
    """
    url = HATENA_RSS_BASE.format(category=category)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=15) as response:
        return response.read().decode("utf-8")


def parse_rss(xml_text: str, category: str) -> list[dict]:
    """
    RSSフィードのXMLをパースして記事情報のリストを返す。

    Args:
        xml_text: RSSフィードのXML文字列
        category: 記事が属するカテゴリ名

    Returns:
        記事情報の辞書リスト
    """
    root = ET.fromstring(xml_text)
    articles = []

    # RSS 1.0形式のitemを取得
    for item in root.findall("rss:item", NAMESPACES):
        title = item.find("rss:title", NAMESPACES)
        link = item.find("rss:link", NAMESPACES)
        description = item.find("rss:description", NAMESPACES)
        date = item.find("dc:date", NAMESPACES)
        bookmarks = item.find("hatena:bookmarkcount", NAMESPACES)

        # タグ（subject）を収集
        tags = []
        for subject in item.findall("dc:subject", NAMESPACES):
            if subject.text:
                tags.append(subject.text)

        article = {
            "title": title.text if title is not None and title.text else "",
            "url": link.text if link is not None and link.text else "",
            "bookmarks": int(bookmarks.text) if bookmarks is not None and bookmarks.text else 0,
            "date": date.text if date is not None and date.text else "",
            "tags": tags,
            "category": category,
            "description": description.text if description is not None and description.text else "",
        }
        articles.append(article)

    return articles


def main():
    """メイン処理: カテゴリごとにRSSを取得してJSONとして出力する。"""
    # コマンドライン引数からカテゴリを取得（なければデフォルト）
    categories = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_CATEGORIES

    # 無効なカテゴリのチェック
    for cat in categories:
        if cat not in VALID_CATEGORIES:
            print(
                json.dumps(
                    {"error": f"無効なカテゴリ: {cat}", "valid_categories": VALID_CATEGORIES},
                    ensure_ascii=False,
                ),
                file=sys.stderr,
            )
            sys.exit(1)

    all_articles = []
    errors = []

    for i, category in enumerate(categories):
        # カテゴリ間でレート制限対策のスリープ
        if i > 0:
            time.sleep(1)

        try:
            xml_text = fetch_rss(category)
            articles = parse_rss(xml_text, category)
            all_articles.extend(articles)
        except Exception as e:
            errors.append({"category": category, "error": str(e)})

    # 結果をJSON出力
    result = {
        "fetched_at": datetime.now().isoformat(),
        "categories": categories,
        "total": len(all_articles),
        "articles": all_articles,
    }

    # エラーがあった場合は含める
    if errors:
        result["errors"] = errors

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
