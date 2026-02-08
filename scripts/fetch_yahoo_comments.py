#!/usr/bin/env python3
"""
Yahoo ニュース コメント取得スクリプト

指定されたYahoo ニュース記事URLのコメントを公開APIから取得し、
JSON形式で標準出力に出力する。

使い方:
    python3 fetch_yahoo_comments.py <Yahoo ニュース記事URL>

例:
    python3 fetch_yahoo_comments.py "https://news.yahoo.co.jp/articles/xxxxx"

注意:
    - User-Agentヘッダを必ず付与すること
    - ページネーション対応: 全コメントを自動取得する
    - ページ間には1秒のスリープを入れてレート制限に対応
"""

import sys
import json
import time
import re
import urllib.request
import urllib.parse

# User-Agentヘッダ（必須）
USER_AGENT = "knowledge-hub/0.1"

# 1ページあたりの取得件数（APIの上限を考慮して50件に設定）
RESULTS_PER_PAGE = 50

# コメントリストAPIのベースURL
COMMENT_LIST_API = (
    "https://news.yahoo.co.jp/api/public/comment-list"
    "/properties/{property_id}/articles/{article_id}"
)

# コメントダイジェストAPIのベースURL（フォールバック用）
COMMENT_DIGEST_API = (
    "https://news.yahoo.co.jp/api/public/comment-digest"
    "/properties/{property_id}/articles/{article_id}"
)

# デフォルトのプロパティID
DEFAULT_PROPERTY_ID = "news_user"


def extract_article_id(url: str) -> str:
    """
    Yahoo ニュース記事URLから記事ID（Shannon ID）を抽出する。

    Args:
        url: Yahoo ニュース記事のURL

    Returns:
        記事ID文字列

    Raises:
        ValueError: URLから記事IDを抽出できない場合
    """
    # パターン1: /articles/{id} 形式
    match = re.search(r"/articles/([a-f0-9]{40})", url)
    if match:
        return match.group(1)

    # パターン2: /articles/{id}/comments 形式（末尾にcommentsがある場合）
    match = re.search(r"/articles/([a-f0-9]{40})/comments", url)
    if match:
        return match.group(1)

    raise ValueError(
        f"URLからYahoo ニュースの記事IDを抽出できませんでした: {url}"
    )


def fetch_comment_page(
    article_id: str, start: int, results: int = RESULTS_PER_PAGE
) -> dict:
    """
    コメントリストAPIから1ページ分のコメントを取得する。

    Args:
        article_id: Yahoo ニュース記事ID（Shannon ID）
        start: 開始位置（1始まり）
        results: 1ページあたりの取得件数

    Returns:
        APIレスポンスの辞書

    Raises:
        urllib.error.HTTPError: APIリクエスト失敗時
    """
    api_url = COMMENT_LIST_API.format(
        property_id=DEFAULT_PROPERTY_ID,
        article_id=article_id,
    )
    params = urllib.parse.urlencode({"start": start, "results": results})
    full_url = f"{api_url}?{params}"

    req = urllib.request.Request(
        full_url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_all_comments(article_id: str) -> dict:
    """
    ページネーションを処理して全コメントを取得する。

    Args:
        article_id: Yahoo ニュース記事ID（Shannon ID）

    Returns:
        全コメント情報を含む辞書
    """
    all_comments = []
    start = 1
    total_results = None

    while True:
        page_data = fetch_comment_page(article_id, start)

        # 初回で総件数を取得
        if total_results is None:
            total_results = page_data.get("totalResults", 0)

        comments = page_data.get("comments", [])
        if not comments:
            break

        all_comments.extend(comments)

        # 全件取得済みなら終了
        if start + len(comments) > total_results:
            break

        # 次のページへ
        start += len(comments)

        # レート制限対応: ページ間に1秒のスリープ
        time.sleep(1)

    return {
        "total_results": total_results or 0,
        "comments": all_comments,
        "article": page_data.get("article") if page_data else None,
    }


def format_comment(raw_comment: dict) -> dict:
    """
    APIレスポンスのコメントデータを統一フォーマットに変換する。

    Args:
        raw_comment: APIから取得した生のコメントデータ

    Returns:
        整形されたコメント辞書
    """
    return {
        "user": raw_comment.get("name", ""),
        "comment": raw_comment.get("text", ""),
        "post_date": raw_comment.get("postDate", ""),
        "comment_id": raw_comment.get("commentId", ""),
        "empathy_count": raw_comment.get("empathyCount", 0),
        "insight_count": raw_comment.get("insightCount", 0),
        "negative_count": raw_comment.get("negativeCount", 0),
        "reply_count": (
            raw_comment.get("reply", {}).get("totalResults", 0)
            if raw_comment.get("reply")
            else 0
        ),
        "permalink": raw_comment.get("permalink", ""),
    }


def main():
    """メイン処理: Yahoo ニュース記事URLのコメントを取得してJSONとして出力する。"""
    if len(sys.argv) < 2:
        print(
            json.dumps(
                {
                    "error": "Yahoo ニュース記事URLを引数に指定してください。",
                    "usage": "python3 fetch_yahoo_comments.py <URL>",
                },
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        sys.exit(1)

    article_url = sys.argv[1]

    # 記事IDの抽出
    try:
        article_id = extract_article_id(article_url)
    except ValueError as e:
        print(
            json.dumps(
                {"error": str(e), "url": article_url},
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        sys.exit(1)

    # コメント取得
    try:
        raw_data = fetch_all_comments(article_id)
    except Exception as e:
        print(
            json.dumps(
                {
                    "error": f"コメント取得に失敗しました: {str(e)}",
                    "url": article_url,
                },
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        sys.exit(1)

    # コメントの整形
    comments = [format_comment(c) for c in raw_data["comments"]]

    # 結果をJSON出力
    result = {
        "url": article_url,
        "article_id": article_id,
        "total_comments": raw_data["total_results"],
        "fetched_comments": len(comments),
        "comments": comments,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
