#!/usr/bin/env python3
"""
Reddit ホット投稿取得スクリプト

指定されたsubredditのホット投稿をJSON APIから取得し、
JSON形式で標準出力に出力する。

使い方:
    python3 fetch_reddit_hot.py [subreddit...]

例:
    # デフォルトのsubredditから取得
    python3 fetch_reddit_hot.py

    # 特定のsubredditから取得
    python3 fetch_reddit_hot.py programming webdev nextjs

デフォルトsubreddit:
    programming, webdev, nextjs, vuejs, LocalLLaMA, ClaudeAI
"""

import sys
import json
import time
import urllib.request
from datetime import datetime

# User-Agentヘッダ（必須）
USER_AGENT = "knowledge-hub/0.1"

# 1サブレッドあたりの取得件数
POSTS_PER_SUBREDDIT = 10

# デフォルトのsubredditリスト（PROFILE.mdの興味領域に対応）
DEFAULT_SUBREDDITS = [
    "programming",   # プログラミング全般
    "webdev",        # Web開発
    "nextjs",        # Next.js
    "vuejs",         # Vue.js / Nuxt
    "LocalLLaMA",    # AI/LLM
    "ClaudeAI",      # Claude AI
]


def fetch_hot_posts(subreddit: str, limit: int = POSTS_PER_SUBREDDIT) -> list:
    """
    指定subredditのホット投稿をJSON APIから取得する。

    Args:
        subreddit: subreddit名（r/なし）
        limit: 取得する投稿数

    Returns:
        APIレスポンスの子要素リスト

    Raises:
        urllib.error.HTTPError: APIリクエスト失敗時
    """
    api_url = (
        f"https://old.reddit.com/r/{subreddit}/hot.json"
        f"?limit={limit}&t=day"
    )

    req = urllib.request.Request(
        api_url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))
        return data.get("data", {}).get("children", [])


def format_post(child: dict, subreddit: str) -> dict:
    """
    APIレスポンスの投稿データを統一フォーマットに変換する。

    Args:
        child: APIからの投稿データ（kind + data）
        subreddit: subreddit名

    Returns:
        整形された投稿辞書
    """
    data = child.get("data", {})

    # ピン留め投稿はスキップ対象としてフラグを立てる
    is_stickied = data.get("stickied", False)

    return {
        "title": data.get("title", ""),
        "url": data.get("url", ""),
        "permalink": f"https://www.reddit.com{data['permalink']}" if data.get("permalink") else "",
        "score": data.get("score", 0),
        "num_comments": data.get("num_comments", 0),
        "subreddit": f"r/{subreddit}",
        "author": data.get("author", "[deleted]"),
        "is_self": data.get("is_self", False),
        "stickied": is_stickied,
        "created_utc": data.get("created_utc", 0),
    }


def main():
    """メイン処理: subredditごとにホット投稿を取得してJSONとして出力する。"""
    # コマンドライン引数からsubredditを取得（なければデフォルト）
    subreddits = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_SUBREDDITS

    all_posts = []
    errors = []

    for i, subreddit in enumerate(subreddits):
        # subreddit間でレート制限対策のスリープ
        if i > 0:
            time.sleep(1)

        try:
            children = fetch_hot_posts(subreddit)
            for child in children:
                if child.get("kind") != "t3":
                    continue
                post = format_post(child, subreddit)
                # ピン留め投稿はスキップ
                if post["stickied"]:
                    continue
                all_posts.append(post)
        except Exception as e:
            errors.append({"subreddit": f"r/{subreddit}", "error": str(e)})

    # 結果をJSON出力
    result = {
        "fetched_at": datetime.now().isoformat(),
        "subreddits": [f"r/{s}" for s in subreddits],
        "total": len(all_posts),
        "articles": all_posts,
    }

    if errors:
        result["errors"] = errors

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
