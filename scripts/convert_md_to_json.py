#!/usr/bin/env python3
"""
Headlines Markdownレポートを JSON 形式に変換するスクリプト

使い方:
  python3 scripts/convert_md_to_json.py 01.Trends/Headlines/2026-02/2026-02-09.md
"""
import sys
import re
import json
import hashlib
from pathlib import Path


def generate_id(url: str) -> str:
    """URLからSHA-256ハッシュの先頭8文字をIDとして生成"""
    return hashlib.sha256(url.encode()).hexdigest()[:8]


def parse_headline_md(content: str) -> dict:
    """MarkdownのHeadlinesレポートをパースしてdict形式に変換"""
    lines = content.split('\n')

    # ヘッダー情報の抽出
    date_match = re.search(r'(\d{4})年(\d{2})月(\d{2})日', lines[0])
    date = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}" if date_match else ""

    generated_at = ""
    for line in lines:
        m = re.search(r'生成日時:\s*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})', line)
        if m:
            generated_at = m.group(1).replace(' ', 'T') + ':00'
            break

    # 件数サマリー
    summary = {"total": 0, "S": 0, "A": 0, "B": 0, "C": 0}
    for line in lines:
        m = re.search(r'記事総数:\s*(\d+)件.*S:\s*(\d+)件.*A:\s*(\d+)件.*B:\s*(\d+)件.*C:\s*(\d+)件', line)
        if m:
            summary = {
                "total": int(m.group(1)),
                "S": int(m.group(2)),
                "A": int(m.group(3)),
                "B": int(m.group(4)),
                "C": int(m.group(5)),
            }
            break

    # 記事のパース
    articles = []
    current_rank = ""
    i = 0
    while i < len(lines):
        line = lines[i]

        # ランクセクションの検出
        if line.startswith('## S '):
            current_rank = 'S'
        elif line.startswith('## A '):
            current_rank = 'A'
        elif line.startswith('## B '):
            current_rank = 'B'
        elif line.startswith('## C '):
            current_rank = 'C'
        elif line.startswith('## 本日のピックアップ'):
            current_rank = ''  # ピックアップセクションでは記事パースを停止

        # 記事行の検出: - [ ] または - [x]
        if current_rank and re.match(r'^- \[[ x]\] \*\*\[', line):
            checked = '[x]' in line[:6]

            # タイトルとURL
            title_match = re.search(r'\*\*\[([^\]]+)\]\(([^)]+)\)\*\*', line)
            if not title_match:
                i += 1
                continue

            title = title_match.group(1)
            url = title_match.group(2)

            # Reddit英語記事の日本語訳
            title_ja = None
            ja_match = re.search(r'\*\*\s*-\s*(.+)$', line)
            if ja_match:
                title_ja = ja_match.group(1).strip()

            # メタデータ行
            i += 1
            meta_line = lines[i].strip() if i < len(lines) else ""
            # "  - AI/LLM | はてブ | 210 users | ⭐ S" のパターン
            meta_line = meta_line.lstrip('- ').strip()

            # カテゴリ
            parts = [p.strip() for p in meta_line.split('|')]
            category = parts[0] if parts else ""

            # ソースとスコアの判定
            source = "hatena"
            score = 0
            score_label = ""
            subreddit = None

            if len(parts) >= 2:
                source_str = parts[1].strip()
                if 'はてブ' in source_str:
                    source = "hatena"
                elif 'Yahoo' in source_str:
                    source = "yahoo"
                elif 'Reddit' in source_str:
                    source = "reddit"

            # はてブ: "210 users"
            for p in parts:
                p = p.strip()
                m = re.match(r'(\d+)\s*users', p)
                if m:
                    score = int(m.group(1))
                    score_label = f"{score} users"
                    break

            # Reddit: "r/ClaudeAI", "735pt 100comments"
            for p in parts:
                p = p.strip()
                if p.startswith('r/'):
                    subreddit = p
                m = re.match(r'(\d+)pt\s+(\d+)comments', p)
                if m:
                    score = int(m.group(1))
                    score_label = f"{m.group(1)}pt {m.group(2)}comments"

            # Yahoo: ソースメディア名
            if source == "yahoo" and not score_label:
                for p in parts[1:]:
                    p = p.strip()
                    if p and not p.startswith('⭐') and 'Yahoo' not in p:
                        score_label = p
                        break

            # 概要行
            i += 1
            summary_line = lines[i].strip() if i < len(lines) else ""
            summary_text = summary_line.lstrip('- ').strip()

            article = {
                "id": generate_id(url),
                "title": title,
                "titleJa": title_ja,
                "url": url,
                "category": category,
                "source": source,
                "score": score,
                "scoreLabel": score_label,
                "subreddit": subreddit,
                "rank": current_rank,
                "summary": summary_text,
                "checked": checked,
            }
            articles.append(article)

        i += 1

    # ピックアップTOP3のパース
    pickups = []
    in_pickup = False
    for i, line in enumerate(lines):
        if '本日のピックアップ' in line:
            in_pickup = True
            continue
        if in_pickup:
            m = re.match(r'###\s+(\d+)\.\s+\[([^\]]+)\]\(([^)]+)\)', line)
            if m:
                pos = int(m.group(1))
                pickup_url = m.group(3)
                # 次の行から理由を取得
                reason = ""
                for j in range(i + 1, min(i + 5, len(lines))):
                    rm = re.match(r'\*\*選出理由\*\*:\s*(.+)', lines[j])
                    if rm:
                        reason = rm.group(1)
                        break
                # URLからarticleIdを検索
                article_id = generate_id(pickup_url)
                pickups.append({
                    "position": pos,
                    "articleId": article_id,
                    "reason": reason,
                })

    return {
        "date": date,
        "generatedAt": generated_at,
        "dataSources": ["はてなブックマーク", "Yahoo ニュース", "Reddit"],
        "summary": summary,
        "articles": articles,
        "pickupTop3": pickups,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 convert_md_to_json.py <path-to-md-file>")
        sys.exit(1)

    md_path = Path(sys.argv[1])
    if not md_path.exists():
        print(f"ファイルが見つかりません: {md_path}")
        sys.exit(1)

    content = md_path.read_text(encoding='utf-8')
    report = parse_headline_md(content)

    # 出力先: 同ディレクトリに .json で出力
    json_path = md_path.with_suffix('.json')
    json_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )

    print(f"変換完了: {json_path}")
    print(f"  記事数: {len(report['articles'])}")
    print(f"  チェック済み: {sum(1 for a in report['articles'] if a['checked'])}")
    print(f"  ピックアップ: {len(report['pickupTop3'])}")


if __name__ == '__main__':
    main()
