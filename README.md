# knowledge-hub

日々のインプット（ニュース・学習）を一元管理し、アイデアやアウトプットにつなげるナレッジハブ。
Claude Code スキルとしてターミナル上で動作し、ビューアアプリで可視化・操作できます。

## 全体像

```text
インプット              処理・蓄積               アウトプット
─────────         ─────────────          ──────────
はてなブックマーク ─┐
Yahoo ニュース ────┼→ /daily-trends ──→ Headlines（JSON）
Reddit ────────────┘        │
                            ↓
               ビューアで記事をチェック
                            │
                            ↓
                   /detail-catch-up ──→ DeepDives（Markdown）

YouTube / Web記事 ──→ /learning-log ──→ 学習レポート（Markdown）

ひらめき・思いつき ──→ /new-idea ─────→ 企画書 + GitHub Issue
```

## スキル一覧

| スキル | 起動ワード | 機能 |
|--------|------------|------|
| `/daily-trends` | 「トレンド」「今日のニュース」「キャッチアップ」 | トレンド記事収集・評価レポート生成 |
| `/detail-catch-up` | 「詳細分析」「深掘り」 | チェックした記事の詳細分析レポート生成 |
| `/new-idea` | 「アイデア」「壁打ち」「企画」 | アイデア壁打ち・企画書作成 |
| `/learning-log` | 「学習」「学習ログ」「勉強」 | 学習内容の要約・蓄積 |

---

## 日次トレンドキャッチアップの流れ

日々のニュースを追いかける基本ワークフローです。

### 1. トレンドレポートの生成（`/daily-trends`）

Claude Code のターミナルで実行します。

```bash
/daily-trends
```

**やっていること**:

1. はてなブックマーク・Yahoo ニュース・Reddit から記事を自動収集
1. PROFILE.md の興味領域に基づいて S〜D ランクで自動評価
1. JSON レポートを `01.Trends/Headlines/YYYY-MM/YYYY-MM-DD.json` に保存

**評価ランクの基準**:

| ランク | 対象 | 例 |
|--------|------|-----|
| S（5点） | 深掘りしたい分野 | AI/LLM、Next.js/Nuxt、Claude Code |
| A（4点） | まだ詳しくない分野 | DevOps、Go/Python、DDD |
| B（3点） | 仕事・趣味周辺 | 個人開発、横浜DeNA、ゲーム |
| C（2点） | 一般ニュース | 政治、経済、スポーツ全般 |
| D（1点） | 非該当 | レポートには含まれない |

### 2. ビューアで記事をチェック

生成されたレポートをブラウザで閲覧し、深掘りしたい記事にチェックを入れます。

```bash
cd viewer && npm run dev
```

ブラウザで http://localhost:5173 を開くと、記事一覧が表示されます。
詳しくは後述の「ビューアアプリ」セクションを参照してください。

### 3. 詳細分析の実行（`/detail-catch-up`）

ビューアでチェックした記事を詳細に分析します。

```bash
/detail-catch-up
```

**やっていること**:

1. 最新の Headlines レポートからチェック済み記事を抽出
1. 各記事の本文を取得し、要約・深掘り分析を実施
1. はてブ・Yahoo・Reddit のコメントを収集し、議論の傾向を分析
1. Markdown レポートを `01.Trends/DeepDives/` に保存

**レポートの内容**:
- 記事の要約（箇条書き + キーポイント）
- PROFILE.md に基づく深掘り（実務への応用・学習ヒント）
- コメント議論分析（賛成/反対/補足の傾向）
- 関連リンク一覧

---

## アイデア壁打ち（`/new-idea`）

思いついたアイデアを対話形式でブラッシュアップし、企画書にまとめます。

```bash
/new-idea
```

**ワークフロー**:

1. アイデアの概要をヒアリング（What / Why / Who / 差別化）
1. 率直なフィードバックを交えた深掘り（2〜3ラウンド）
1. 5軸で実現可能性を評価（技術・コスト・差別化・需要・工数）
1. 3つのファイルを生成:
   - `overview.md` - 企画書（5W1H、MVP定義、技術スタック）
   - `discussion.md` - 壁打ち記録（対話要約、主要論点）
   - `references.md` - 参考資料（類似サービス、技術情報）
1. GitHub Issue を自動作成（MVPチェックリスト付き）

**出力先**: `02.Ideas/YYYY-MM-DD_{タイトル}/`

---

## 学習ログ（`/learning-log`）

YouTube 動画や Web 記事の学習内容を、対話を通じて整理・蓄積します。

```bash
/learning-log
```

**ワークフロー**:

1. 学習ソースを入力（YouTube URL / Web URL / 書籍・その他）
1. NotebookLM MCP でソースを自動分析（要約・構造化・応用分析）
1. 対話で理解を深める（2〜3ラウンド）
   - 理解の確認 → 実務への応用 → 振り返り
1. 初学者向けの学習レポートを生成（Mermaid 図付き）

**出力先**: `03.Learnings/YYYY-MM-DD_{タイトル}/REPORT.md`

**補足**: NotebookLM MCP が未設定の場合は、WebFetch での記事取得 → 対話のみのフローにフォールバックします。

---

## ビューアアプリ

トレンドレポートをブラウザで閲覧・操作するための Web アプリです。

### 技術スタック

- **フロントエンド**: React + TypeScript + Vite + Tailwind CSS
- **バックエンド**: Express（API サーバー）

### 起動方法

```bash
cd viewer && npm run dev
```

- **フロントエンド（Vite）**: http://localhost:5173
- **API サーバー（Express）**: http://localhost:3001

### 画面構成

#### Headlines（トップページ）

日付別のトレンドレポートを閲覧する画面です。

- **サイドバー**: 日付の切り替え（最新日付に自動遷移）
- **フィルタバー**: ランク / ソース / カテゴリ / テキスト検索で絞り込み
- **記事カード**: タイトル、URL、スコア、カテゴリ、概要を表示
  - チェックボックスで深掘り対象を選択（JSON ファイルに即時反映）
  - お気に入りボタンで記事を保存
- **ピックアップ**: その日の注目記事 TOP3
- **トレンド分析**: 複数記事に共通するテーマの横断分析

#### DeepDives

詳細分析レポートを閲覧する画面です。

- 月別にレポートを一覧表示
- Markdown レンダリング（シンタックスハイライト対応）

#### Favorites

お気に入り登録した記事をまとめて閲覧する画面です。

- お気に入りの一覧表示・解除が可能
- データは `01.Trends/favorites.json` に永続化

### ダークモード

画面右上のトグルボタンでライト / ダークモードを切り替えられます。

---

## ディレクトリ構成

```
knowledge-hub/
├── .claude/skills/           # Claude Code スキル定義
│   ├── daily-trends/         #   トレンドレポート生成
│   ├── detail-catch-up/      #   記事詳細分析
│   ├── new-idea/             #   アイデア壁打ち
│   └── learning-log/         #   学習ログ
├── 01.Trends/
│   ├── Headlines/            # /daily-trends の出力先（JSON）
│   ├── DeepDives/            # /detail-catch-up の出力先（Markdown）
│   └── favorites.json        # お気に入り記事
├── 02.Ideas/                 # /new-idea の出力先
├── 03.Learnings/             # /learning-log の出力先
├── 04.BlogDrafts/            # ブログ下書き（将来用）
├── scripts/                  # データ取得用 Python スクリプト
├── viewer/                   # ビューアアプリ（Vite + React + Express）
├── PROFILE.md                # 興味領域の定義（評価基準）
├── CLAUDE.md                 # プロジェクト固有ルール
└── README.md
```

### ファイル命名規則

| 種別 | パス | 形式 |
|------|------|------|
| Headlines レポート | `01.Trends/Headlines/YYYY-MM/YYYY-MM-DD.json` | JSON |
| DeepDives レポート | `01.Trends/DeepDives/YYYY-MM/YYYY-MM-DD_記事タイトル.md` | Markdown |
| お気に入り | `01.Trends/favorites.json` | JSON |
| アイデア企画書 | `02.Ideas/YYYY-MM-DD_{タイトル}/` | ディレクトリ（3ファイル） |
| 学習レポート | `03.Learnings/YYYY-MM-DD_{タイトル}/REPORT.md` | Markdown |

---

## セットアップ

### 前提条件

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) がインストール済み
- Python 3.x がインストール済み
- Node.js（ビューアアプリの実行に必要）

### 手順

1. リポジトリをクローン

```bash
git clone https://github.com/silmo-yokohama/knowledge-hub-public.git knowledge-hub
cd knowledge-hub
```

1. PROFILE.md を作成

```bash
cp PROFILE.example.md PROFILE.md
```

`PROFILE.md` を開いて、自分の興味領域に合わせて編集してください。
このファイルがトレンド記事の評価基準になります。

1. ビューアの依存関係をインストール

```bash
cd viewer && npm install
```

1. Claude Code を起動してスキルを実行

```bash
claude
```

```bash
/daily-trends      # 日次トレンドレポートを生成
/detail-catch-up   # チェックした記事を詳細分析
/new-idea           # アイデア壁打ちを開始
/learning-log       # 学習ログを記録
```

### PROFILE.md のカスタマイズ

`PROFILE.md` の内容がトレンド記事の評価ランクに影響します:

- **さらに深掘りしたい分野** → S ランク（最高評価）
- **まだ詳しくない分野** → A ランク
- **仕事分野・趣味分野** → B ランク
- **その他（ニュース等）** → C ランク

---

## データソース

| ソース | 取得方法 | 取得内容 |
|--------|----------|----------|
| はてなブックマーク | RSS（IT / 学び / 経済・政治） | 人気エントリー + ブックマーク数 |
| Yahoo ニュース | RSS（IT / スポーツ） | ニュース記事 |
| Reddit | JSON API（6 subreddit） | ホット投稿（各10件） |

### コメント取得（詳細分析時）

| ソース | 取得方法 |
|--------|----------|
| はてなブックマーク | jsonlite API |
| Yahoo ニュース | 公開コメントリスト API（ページネーション対応） |
| Reddit | old.reddit.com JSON API |

---

## スクリプト一覧

`scripts/` ディレクトリに配置された Python スクリプトです。
スキルから自動的に呼び出されるため、通常は直接実行する必要はありません。

| スクリプト | 用途 |
|-----------|------|
| `fetch_hatena_rss.py` | はてブ人気エントリー RSS 取得 |
| `fetch_yahoo_rss.py` | Yahoo ニュース RSS 取得 |
| `fetch_reddit_hot.py` | Reddit ホット投稿取得（6 subreddit） |
| `fetch_hatena_comments.py` | はてブコメント取得 |
| `fetch_yahoo_comments.py` | Yahoo ニュースコメント取得 |
| `fetch_reddit_comments.py` | Reddit コメント取得 |
| `convert_md_to_json.py` | Markdown → JSON 変換（旧形式の移行用） |

---

## リポジトリ構成

このプロジェクトは2つのリポジトリで運用されています:

- **[knowledge-hub](https://github.com/silmo-yokohama/knowledge-hub)**（Private）: スキル成果物を含む本体
- **[knowledge-hub-public](https://github.com/silmo-yokohama/knowledge-hub-public)**（Public）: ツール部分のみの公開ミラー

プライベートリポジトリへの push 時、GitHub Actions がスキル成果物（`01.Trends/`、`02.Ideas/` 等）と個人プロフィール（`PROFILE.md`）を除外した上で公開リポジトリに自動同期します。

## ライセンス

MIT License
