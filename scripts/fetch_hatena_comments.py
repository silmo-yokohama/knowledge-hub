#!/usr/bin/env python3
"""
はてなブックマーク ブコメ取得スクリプト

指定された記事URLのはてなブックマークコメント（ブコメ）を取得し、
JSON形式で標準出力に出力する。

使い方:
    python3 fetch_hatena_comments.py <記事URL>

例:
    python3 fetch_hatena_comments.py "https://example.com/article"

注意:
    User-Agentヘッダがないと空レスポンスが返るため必須。
"""

import sys
import json
import urllib.request
import urllib.parse

# ブコメ取得APIのベースURL
HATENA_ENTRY_API = "https://b.hatena.ne.jp/entry/jsonlite/?url={encoded_url}"

# User-Agentヘッダ（必須 - ないと空レスポンスが返る）
USER_AGENT = "knowledge-hub/0.1"


def fetch_comments(article_url: str) -> dict:
    """
    指定された記事URLのはてなブックマークコメントを取得する。

    Args:
        article_url: コメントを取得する対象の記事URL

    Returns:
        ブコメ情報を含む辞書

    Raises:
        urllib.error.URLError: HTTPリクエスト失敗時
    """
    encoded_url = urllib.parse.quote(article_url, safe="")
    api_url = HATENA_ENTRY_API.format(encoded_url=encoded_url)

    req = urllib.request.Request(api_url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=15) as response:
        body = response.read().decode("utf-8")
        # 空レスポンスの場合はブコメ0件として扱う
        if not body.strip():
            return None
        return json.loads(body)


def filter_comments(data: dict) -> list[dict]:
    """
    コメント付きブックマークのみをフィルタリングして返す。

    Args:
        data: はてなブックマークAPIのレスポンス

    Returns:
        コメント付きブックマークの辞書リスト
    """
    if not data or "bookmarks" not in data:
        return []

    comments = []
    for bookmark in data["bookmarks"]:
        # コメントが空でないものだけフィルタ
        if bookmark.get("comment", "").strip():
            comments.append(
                {
                    "user": bookmark.get("user", ""),
                    "comment": bookmark["comment"],
                    "timestamp": bookmark.get("timestamp", ""),
                    "tags": bookmark.get("tags", []),
                }
            )

    return comments


def main():
    """メイン処理: 記事URLのブコメを取得してJSONとして出力する。"""
    if len(sys.argv) < 2:
        print(
            json.dumps(
                {"error": "記事URLを引数に指定してください。", "usage": "python3 fetch_hatena_comments.py <URL>"},
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        sys.exit(1)

    article_url = sys.argv[1]

    try:
        raw_data = fetch_comments(article_url)
    except Exception as e:
        print(
            json.dumps({"error": f"ブコメ取得に失敗しました: {str(e)}", "url": article_url}, ensure_ascii=False),
            file=sys.stderr,
        )
        sys.exit(1)

    comments = filter_comments(raw_data)

    # 結果をJSON出力
    result = {
        "url": article_url,
        "title": raw_data.get("title", "") if raw_data else "",
        # countフィールドは文字列で返る場合があるためintに変換
        "total_bookmarks": int(raw_data.get("count", 0)) if raw_data else 0,
        "comments_count": len(comments),
        "comments": comments,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
