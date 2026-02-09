---
name: daily-trends
description: 日次のトレンド記事を収集し、PROFILE.mdの興味領域に基づいて評価・分類したレポートを生成する。「トレンド」「今日のニュース」「キャッチアップ」で起動。
---

# /daily-trends - 日次トレンドレポート生成スキル

## 概要

はてなブックマークの人気エントリー、Yahoo ニュース RSS、Redditのホット投稿からトレンド記事を収集し、
PROFILE.mdの興味領域に基づいてマッチング評価・分類したレポートを生成する。

## ワークフロー

以下のステップを順番に実行してください。途中でエラーが発生した場合でも、取得できたデータで可能な限りレポートを生成してください。

### Step 1: プロフィール読み込み

Read ツールで `/home/a/00.knowledge-hub/PROFILE.md` を読み込み、ユーザーの興味領域を把握する。

特に以下のセクションに注目:
- 「さらに深掘りしたい分野」→ Sランク評価の対象
- 「まだ詳しくない分野」→ Aランク評価の対象
- 「仕事分野」「趣味分野」→ B/Cランク評価の対象

### Step 2: 日付と出力先の確認

1. 今日の日付を確認する（YYYY-MM-DD形式）
2. 出力先ディレクトリ `01.Trends/Headlines/YYYY-MM/` が存在しない場合は作成する
3. 同日のレポート `YYYY-MM-DD.json` が既に存在する場合は、**ユーザーに上書きの確認を取る**
4. `01.Trends/DeepDives/` 配下の全ファイルをGlobツールで取得し、各ファイルの先頭から「元記事」URLを抽出して、**過去に詳細分析済みの記事URLリスト**を作成する
   - パターン: `/home/a/00.knowledge-hub/01.Trends/DeepDives/**/*.md`
   - 各ファイルの `> 元記事:` 行からURLを取得する
   - このリストに含まれるURLの記事は、後のマッチング評価でスキップする

### Step 3: はてなブックマーク人気エントリーの取得

Bashツールで以下のコマンドを実行し、はてなブックマークの人気エントリーを取得する:

```bash
python3 /home/a/00.knowledge-hub/scripts/fetch_hatena_rss.py it knowledge economics
```

- 出力はJSON形式
- `articles` 配列の各要素に `title`, `url`, `bookmarks`, `tags`, `category`, `description` が含まれる
- エラーが発生した場合は `errors` フィールドを確認し、取得できたカテゴリのデータで続行する

### Step 4: Yahoo ニュース RSS の取得

Bashツールで以下のコマンドを実行し、Yahoo ニュースの最新記事を取得する:

```bash
python3 /home/a/00.knowledge-hub/scripts/fetch_yahoo_rss.py it sports
```

- 出力はJSON形式
- **トークン節約のため `it sports` の2フィードのみ取得する**（全フィード取得は約700件になり非効率）
- `articles` 配列の各要素に `title`, `url`, `date`, `source`, `feed`, `feed_label`, `description` が含まれる
- はてブ記事と URL が重複する記事は除外する
- エラーが発生した場合は `errors` フィールドを確認し、取得できたフィードのデータで続行する

### Step 5: Reddit ホット投稿の取得

Bashツールで以下のコマンドを実行し、Redditのホット投稿を取得する:

```bash
python3 /home/a/00.knowledge-hub/scripts/fetch_reddit_hot.py
```

- 出力はJSON形式
- デフォルトで6つのsubreddit（programming, webdev, nextjs, vuejs, LocalLLaMA, ClaudeAI）から各10件取得
- `articles` 配列の各要素に `title`, `url`, `permalink`, `score`, `num_comments`, `subreddit` が含まれる
- ピン留め投稿（stickied）は自動的に除外される
- **英語のタイトルは後のレポート生成時に日本語訳を併記する**
- エラーが発生した場合は `errors` フィールドを確認し、取得できたsubredditのデータで続行する

### Step 6: 重複除去と統合

はてブ、Yahoo ニュース、Reddit の全記事を統合し、URLベースで重複を除去する。

- 同一URLの記事は1つに統合し、情報が豊富な方（ブクマ数やソース情報がある方）を優先する
- Yahooニュースの記事はブクマ数がないため、ソース名（`source` フィールド）をブクマ数の代わりに表示する
- Redditの記事はスコアとコメント数を表示する

### Step 7: マッチング評価（タイトルベースで高速判定）

収集した全記事に対して、 `references/matching-criteria.md` の基準に従いランク付けを行う。

**トークン節約**: 評価は**タイトルのみ**で判定する。`description` フィールドはタイトルだけでは判断が難しい場合にのみ参照する。

**前処理**:
- Step 2 で作成した「過去に詳細分析済みの記事URLリスト」に含まれる記事を除外する

**評価の方法**:
- 記事のタイトル、概要、タグを総合的に分析する
- PROFILE.mdの興味領域との関連度をAIの文脈理解力で判断する
- キーワードの完全一致だけでなく、意味的な関連性も考慮する

**評価ランク**:
| ランク | 点数 | 対象 |
|--------|------|------|
| S | 5 | 「深掘りしたい分野」直結（AI/LLM, Next.js/Nuxt, Claude Code, UI/UX等） |
| A | 4 | 「まだ詳しくない分野」や「仕事分野」関連（DevOps, Go/Python, DDD等） |
| B | 3 | 仕事分野の周辺や趣味分野（個人開発, 横浜DeNA, ゲーム等） |
| C | 2 | 一般ニュース領域（政治, 経済, スポーツ全般） |
| D | 1 | 上記に該当しない → レポートに含めない |

### Step 8: レポート生成

`references/report-schema.md` のJSONスキーマに従い、レポートデータを生成する。

**レポートの構成（JSON）**:
- `date`: レポート日付（`YYYY-MM-DD`）
- `generatedAt`: 生成日時（ISO 8601）
- `dataSources`: データソース一覧
- `summary`: 記事総数・ランク別件数 `{ total, S, A, B, C }`
- `articles`: 記事配列（各記事は以下のフィールドを持つ）
  - `id`: URLのSHA-256ハッシュ先頭8文字
  - `title`: 記事タイトル
  - `titleJa`: Reddit英語記事の日本語訳（日本語記事は `null`）
  - `url`: 記事URL
  - `category`: カテゴリー（例: AI/LLM, フロントエンド, 野球 等）
  - `source`: 取得元（`"hatena"` / `"yahoo"` / `"reddit"`）
  - `score`: 数値スコア（はてブ数 / Redditポイント / Yahooは `0`）
  - `scoreLabel`: 表示用スコア（`"210 users"` / `"ITmedia NEWS"` / `"735pt 100comments"`）
  - `subreddit`: Redditの場合のみ（例: `"r/ClaudeAI"`）、それ以外は `null`
  - `rank`: ランク（`"S"` / `"A"` / `"B"` / `"C"`）
  - `summary`: 概要（30〜50文字程度の1行要約）
  - `checked`: `false`（初期値、ビューアでチェック）
- `trendAnalysis`: その日のトレンド分析（3〜5件）。カテゴリに関係なく、複数の記事に共通するテーマや話題を横断的に分析する
  - `topic`: トレンドのテーマ（短いタイトル、20文字程度。例: 「AI安全性の議論が加速」「新フレームワークのリリースラッシュ」）
  - `description`: なぜその話題が注目されているかの説明（100〜150文字程度。どんな記事が共通のテーマに触れているか、なぜ同時に話題になっているかを分析）
  - `relatedArticleIds`: 関連する記事の `id` 一覧

**IDの生成方法**:
記事URLをSHA-256ハッシュにかけ、先頭8文字を使用する。Pythonの場合:

```python
import hashlib
article_id = hashlib.sha256(url.encode()).hexdigest()[:8]
```

### Step 9: ファイル保存

Write ツールでレポートをJSON形式で以下のパスに保存する:

```
/home/a/00.knowledge-hub/01.Trends/Headlines/YYYY-MM/YYYY-MM-DD.json
```

- `JSON.stringify` 相当の整形済みJSON（インデント2スペース）で出力する
- `ensure_ascii=False` 相当で日本語はそのまま出力する

### Step 10: 完了報告

レポート生成が完了したら、以下を報告する:
- 生成したレポートのパス
- 収集した記事の総数とランク別の内訳
- エラーがあった場合はその内容
- 「ビューア（`cd viewer && npm run dev`）で記事をチェックし、`/detail-catch-up` を実行すると詳細分析レポートを生成できます」と案内する

## 注意事項

- レポートは全て日本語で記述する
- 既存ファイルの上書きは禁止（ユーザー確認必須）
- 一部のソースの取得に失敗しても、取得できたデータだけでレポートを生成する
- Redditの投稿タイトルは英語のため、レポートでは日本語訳を併記する（例: `**[原題](URL)** - 日本語タイトル`）
- 1日1回の実行を想定しているが、複数回実行しても問題ないようにする
