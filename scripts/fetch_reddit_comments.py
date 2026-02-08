#!/usr/bin/env python3
"""
Reddit コメント取得スクリプト

指定されたReddit投稿URLのコメントをJSON APIから取得し、
JSON形式で標準出力に出力する。

使い方:
    python3 fetch_reddit_comments.py <Reddit投稿URL>

例:
    python3 fetch_reddit_comments.py "https://www.reddit.com/r/programming/comments/xxxxx/title/"
    python3 fetch_reddit_comments.py "https://old.reddit.com/r/programming/comments/xxxxx/title/"

注意:
    - WebFetchはreddit.comをブロックするためこのスクリプトを使用する
    - User-Agentヘッダを必ず付与する
    - ネストされた返信コメントもフラット化して取得する
    - スコア順（best）でソートして取得する
"""

import sys
import json
import re
import urllib.request

# User-Agentヘッダ（必須）
USER_AGENT = "knowledge-hub/0.1"

# 1リクエストあたりの最大取得数
# limit=200でトップレベル+ネスト含め十分なコメント数を取得できる
COMMENT_LIMIT = 200


def extract_post_info(url: str) -> tuple[str, str]:
    """
    Reddit投稿URLからサブレッドと投稿IDを抽出する。

    Args:
        url: Reddit投稿のURL

    Returns:
        (subreddit, post_id) のタプル

    Raises:
        ValueError: URLからReddit投稿情報を抽出できない場合
    """
    # パターン: /r/{subreddit}/comments/{post_id}/...
    match = re.search(
        r"/r/([^/]+)/comments/([a-z0-9]+)", url, re.IGNORECASE
    )
    if match:
        return match.group(1), match.group(2)

    raise ValueError(
        f"URLからReddit投稿のサブレッドと投稿IDを抽出できませんでした: {url}"
    )


def fetch_post_and_comments(subreddit: str, post_id: str) -> list:
    """
    Reddit JSON APIから投稿情報とコメントを取得する。

    Args:
        subreddit: サブレッド名
        post_id: 投稿ID

    Returns:
        APIレスポンス（配列: [投稿データ, コメントデータ]）

    Raises:
        urllib.error.HTTPError: APIリクエスト失敗時
    """
    # old.reddit.comを使い、.json拡張子でJSON形式を取得
    api_url = (
        f"https://old.reddit.com/r/{subreddit}/comments/{post_id}"
        f".json?limit={COMMENT_LIMIT}&sort=best"
    )

    req = urllib.request.Request(
        api_url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def flatten_comments(children: list, depth: int = 0) -> list[dict]:
    """
    ネストされたRedditコメントツリーをフラットなリストに変換する。

    Args:
        children: コメントの子要素リスト
        depth: 現在のネスト深度

    Returns:
        フラット化されたコメント辞書のリスト
    """
    result = []
    for child in children:
        # kind='t1' がコメント、'more' は追加コメントの参照
        if child["kind"] != "t1":
            continue

        data = child["data"]
        comment = {
            "user": data.get("author", "[deleted]"),
            "comment": data.get("body", ""),
            "score": data.get("score", 0),
            "depth": depth,
            "comment_id": data.get("id", ""),
            "permalink": (
                f"https://www.reddit.com{data['permalink']}"
                if data.get("permalink")
                else ""
            ),
            "created_utc": data.get("created_utc", 0),
        }
        result.append(comment)

        # ネストされた返信を再帰的に処理
        replies = data.get("replies", "")
        if isinstance(replies, dict):
            reply_children = replies.get("data", {}).get("children", [])
            result.extend(flatten_comments(reply_children, depth + 1))

    return result


def format_post(post_data: dict) -> dict:
    """
    投稿データを整形する。

    Args:
        post_data: Reddit APIからの投稿データ

    Returns:
        整形された投稿情報辞書
    """
    return {
        "title": post_data.get("title", ""),
        "author": post_data.get("author", "[deleted]"),
        "subreddit": post_data.get("subreddit", ""),
        "score": post_data.get("score", 0),
        "upvote_ratio": post_data.get("upvote_ratio", 0),
        "num_comments": post_data.get("num_comments", 0),
        "url": post_data.get("url", ""),
        "is_self": post_data.get("is_self", False),
        "selftext": post_data.get("selftext", ""),
        "permalink": (
            f"https://www.reddit.com{post_data['permalink']}"
            if post_data.get("permalink")
            else ""
        ),
        "created_utc": post_data.get("created_utc", 0),
    }


def main():
    """メイン処理: Reddit投稿URLのコメントを取得してJSONとして出力する。"""
    if len(sys.argv) < 2:
        print(
            json.dumps(
                {
                    "error": "Reddit投稿URLを引数に指定してください。",
                    "usage": "python3 fetch_reddit_comments.py <URL>",
                },
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        sys.exit(1)

    post_url = sys.argv[1]

    # 投稿情報の抽出
    try:
        subreddit, post_id = extract_post_info(post_url)
    except ValueError as e:
        print(
            json.dumps(
                {"error": str(e), "url": post_url},
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        sys.exit(1)

    # APIからデータ取得
    try:
        raw_data = fetch_post_and_comments(subreddit, post_id)
    except Exception as e:
        print(
            json.dumps(
                {
                    "error": f"Reddit APIからのデータ取得に失敗しました: {str(e)}",
                    "url": post_url,
                },
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        sys.exit(1)

    # 投稿情報の整形
    post_info = format_post(raw_data[0]["data"]["children"][0]["data"])

    # コメントのフラット化
    comment_children = raw_data[1]["data"]["children"]
    comments = flatten_comments(comment_children)

    # 結果をJSON出力
    result = {
        "url": post_url,
        "subreddit": f"r/{subreddit}",
        "post": post_info,
        "total_comments": post_info["num_comments"],
        "fetched_comments": len(comments),
        "comments": comments,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
