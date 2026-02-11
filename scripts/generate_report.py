#!/usr/bin/env python3
"""
日次トレンドレポート生成スクリプト
はてブ・Yahoo・Redditのデータを統合し、マッチング評価を行ってJSON出力する
"""
import json
import hashlib
import sys
from datetime import datetime

def gen_id(url):
    """URLからSHA-256ハッシュ先頭8文字のIDを生成"""
    return hashlib.sha256(url.encode()).hexdigest()[:8]

# 除外URL（過去にDeepDivesで分析済み）
EXCLUDED_URLS = {
    "https://azukiazusa.dev/blog/trying-claude-code-agent-teams/",
    "https://zenn.dev/sakasegawa/articles/e6a8aa168a7d19",
    "https://zenn.dev/storehero/articles/f21d49387577bb",
    "https://old.reddit.com/r/nextjs/comments/1qy7z3t/nextjs_new_to_testing_what_testing_tools_to_use/",
    "https://news.yahoo.co.jp/articles/f59b3c8a985797a209738ce0a464c503a1ce5f66?source=rss",
    "https://techtarget.itmedia.co.jp/tt/news/2602/06/news09.html",
    "https://posfie.com/@taimport/p/EF2JWnz",
    "https://2025.stateofjs.com/en-US/",
    "https://www.reddit.com/gallery/1qzbe6m",
    "https://www.publickey1.jp/blog/26/state_of_javascript_2025react1webpackvite.html",
    "https://eslint.org/blog/2026/02/eslint-v10.0.0-released/",
    "https://zenn.dev/idapan/articles/af819fa822c090",
    "https://news.yahoo.co.jp/articles/bcfac7e787ebef25b51f3f4aee637c0314910731",
    "https://numagasablog.com/entry/2026/02/08/221502",
    "https://sizu.me/ushironoko/posts/1t256hfucxc6",
    "https://news.yahoo.co.jp/articles/77a0948327faec419d377f5ca726f4d11da569ea",
    "https://zenn.dev/smartvain/articles/ai-attacked-my-code-security-mostly-placebo",
    "https://blog.lai.so/agent-teams/",
    "https://zenn.dev/singularity/articles/2026-02-07-claude-code-extensibility-memo",
    "https://newsletter.eng-leadership.com/p/96-engineers-dont-fully-trust-ai",
    "https://www.blundergoat.com/articles/ai-makes-the-easy-part-easier-and-the-hard-part-harder",
    "https://old.reddit.com/r/ClaudeAI/comments/1qzzav6/cool_we_dont_need_experts_anymore_thanks_to/",
    "https://i.redd.it/zxfqxyraahig1.png",
    "https://www.reddit.com/gallery/1r0ie1y",
    "https://old.reddit.com/r/ClaudeAI/comments/1r0dxob/ive_used_ai_to_write_100_of_my_code_for_1_year_as/",
    "https://old.reddit.com/r/webdev/comments/1qzo2na/whats_a_widely_accepted_best_practice_youve/",
    "https://old.reddit.com/r/webdev/comments/1qzysqt/anyone_else_miss_the_simplicity",
}

def load_data():
    """3つのデータソースを読み込み"""
    hatena_path = sys.argv[1]
    yahoo_path = sys.argv[2]
    reddit_path = sys.argv[3]

    with open(hatena_path) as f:
        hatena = json.load(f)
    with open(yahoo_path) as f:
        yahoo = json.load(f)
    with open(reddit_path) as f:
        reddit = json.load(f)

    return hatena, yahoo, reddit

def main():
    hatena, yahoo, reddit = load_data()

    # URL重複チェック用セット
    seen_urls = set()
    all_articles = []

    # はてなブックマーク処理
    for art in hatena["articles"]:
        url = art["url"]
        if url in EXCLUDED_URLS or url in seen_urls:
            continue
        seen_urls.add(url)
        all_articles.append({
            "url": url,
            "title": art["title"],
            "source": "hatena",
            "score": art["bookmarks"],
            "scoreLabel": f'{art["bookmarks"]} users',
            "subreddit": None,
            "tags": art.get("tags", []),
            "description": art.get("description", ""),
            "hatena_category": art.get("category", ""),
        })

    # Yahoo ニュース処理（はてブと重複するURLを除外）
    for art in yahoo["articles"]:
        url = art["url"]
        if url in EXCLUDED_URLS or url in seen_urls:
            continue
        seen_urls.add(url)
        all_articles.append({
            "url": url,
            "title": art["title"],
            "source": "yahoo",
            "score": 0,
            "scoreLabel": art.get("source", "Yahoo ニュース"),
            "subreddit": None,
            "tags": [],
            "description": art.get("description", ""),
            "yahoo_feed": art.get("feed", ""),
        })

    # Reddit処理
    for art in reddit["articles"]:
        url = art["url"]
        if url in EXCLUDED_URLS or url in seen_urls:
            continue
        seen_urls.add(url)
        all_articles.append({
            "url": url,
            "title": art["title"],
            "source": "reddit",
            "score": art["score"],
            "scoreLabel": f'{art["score"]}pt {art["num_comments"]}comments',
            "subreddit": art["subreddit"],
            "tags": [],
            "description": "",
            "permalink": art.get("permalink", ""),
        })

    # 全記事のURLとタイトルをリスト出力（評価用）
    for i, art in enumerate(all_articles):
        print(f"{i}|{art['source']}|{art['score']}|{gen_id(art['url'])}|{art['title'][:80]}|{art['url'][:80]}")

    print(f"\n--- Total: {len(all_articles)} articles ---")

if __name__ == "__main__":
    main()
