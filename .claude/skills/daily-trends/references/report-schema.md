# レポートスキーマ: daily-trends

以下のJSON形式で `01.Trends/Headlines/YYYY-MM/YYYY-MM-DD.json` に出力する。

---

## JSONスキーマ

```json
{
  "date": "2026-02-09",
  "generatedAt": "2026-02-09T10:30:00",
  "dataSources": ["はてなブックマーク", "Yahoo ニュース", "Reddit"],
  "summary": {
    "total": 56,
    "S": 16,
    "A": 14,
    "B": 13,
    "C": 13
  },
  "articles": [
    {
      "id": "a1b2c3d4",
      "title": "Claude Code の新機能がリリースされ、スキル機能が大幅に強化された",
      "titleJa": null,
      "url": "https://example.com/article",
      "category": "AI/LLM",
      "source": "hatena",
      "score": 120,
      "scoreLabel": "120 users",
      "subreddit": null,
      "rank": "S",
      "summary": "Claude Code の新機能がリリースされ、スキル機能が大幅に強化された",
      "checked": false
    }
  ],
  "trendAnalysis": [
    {
      "topic": "AI安全性と倫理の議論が加速",
      "description": "Opus 4.6の利益最大化実験やAIコード品質への影響など、AI開発の安全性・倫理面に関する記事が複数のソースで同時に話題に。技術的な進歩だけでなく、社会的責任への関心の高まりが見られる。",
      "relatedArticleIds": ["a1b2c3d4", "e5f6g7h8"]
    }
  ]
}
```

## フィールド説明

### トップレベル

| フィールド | 型 | 説明 |
|-----------|-----|------|
| `date` | string | レポート日付（`YYYY-MM-DD`） |
| `generatedAt` | string | 生成日時（ISO 8601） |
| `dataSources` | string[] | データソース名一覧 |
| `summary` | object | 記事総数・ランク別件数 |
| `articles` | Article[] | 記事配列 |
| `trendAnalysis` | TrendInsight[] | その日のトレンド分析（3〜5件） |

### Article

| フィールド | 型 | 説明 |
|-----------|-----|------|
| `id` | string | URLのSHA-256ハッシュ先頭8文字 |
| `title` | string | 記事タイトル |
| `titleJa` | string \| null | Reddit英語記事の日本語訳（日本語記事は `null`） |
| `url` | string | 記事URL |
| `category` | string | カテゴリー（例: AI/LLM, フロントエンド, 野球） |
| `source` | string | 取得元: `"hatena"` / `"yahoo"` / `"reddit"` |
| `score` | number | 数値スコア（はてブ数 / Redditポイント / Yahooは `0`） |
| `scoreLabel` | string | 表示用スコア（`"210 users"` / `"ITmedia NEWS"` / `"735pt 100comments"`） |
| `subreddit` | string \| null | Redditのsubreddit名（例: `"r/ClaudeAI"`）、Reddit以外は `null` |
| `rank` | string | ランク: `"S"` / `"A"` / `"B"` / `"C"` |
| `summary` | string | 概要（30〜50文字程度の1行要約） |
| `checked` | boolean | チェック状態（初期値 `false`、ビューアで更新） |

### TrendInsight

| フィールド | 型 | 説明 |
|-----------|-----|------|
| `topic` | string | トレンドのテーマ（短いタイトル、20文字程度） |
| `description` | string | トレンドの説明（なぜ注目されているか、100〜150文字程度） |
| `relatedArticleIds` | string[] | 関連する記事の `id` 一覧 |

## 補足ルール

- 各ランク内では記事を関連度の高い順にソートする（はてブ記事はブックマーク数も考慮）
- Dランク（対象外）の記事はレポートに含めない
- 過去にDeepDivesで詳細分析済みの記事はレポートに含めない
- `checked` フィールドの初期値は `false`。ビューアのチェックボックスで更新される
- 概要は記事の内容を1行（30〜50文字程度）で要約する
- IDの生成: `hashlib.sha256(url.encode()).hexdigest()[:8]`
- `trendAnalysis` は3〜5件程度。カテゴリに関係なく、複数の記事に共通するテーマや話題を横断的に分析する
- 各トレンドには関連する記事のIDを紐付け、ビューアで対応する記事にジャンプできるようにする
