# knowledge-hub

日々のインプット（ニュース・学習）を一元管理し、アイデアやアウトプットにつなげるナレッジハブ。
Claude Codeスキルとしてターミナル上で動作します。

## スキル一覧

| スキル名 | 機能 | フェーズ |
|----------|------|----------|
| `/daily-trends` | トレンド記事収集・評価レポート生成 | v0 |
| `/detail-catch-up` | チェックした記事の詳細分析レポート生成 | v0 |
| `/new-idea` | アイデア壁打ち・企画書作成 | v1（予定） |
| 学習ログスキル | 学習内容の要約・蓄積 | v2（予定） |
| `/write-blog` | ブログ執筆サポート | v3（予定） |

## ディレクトリ構成

```
knowledge-hub/
├── 01.Trends/
│   ├── Headlines/          # /daily-trends レポート出力先
│   └── DeepDives/          # /detail-catch-up レポート出力先
├── 02.Ideas/               # v1用
├── 03.Learnings/           # v2用
├── 04.BlogDrafts/          # v3用
├── scripts/                # ユーティリティスクリプト
├── PROFILE.md              # 興味領域の定義
├── CLAUDE.md               # プロジェクト固有ルール
├── requirements.md         # 要件定義書
└── README.md
```

## セットアップ

### 前提条件

- Claude Code CLI がインストール済み
- Python 3.x がインストール済み
- GitHub CLI (`gh`) がインストール済み

### 手順

1. リポジトリをクローン

```bash
git clone https://github.com/silmo-yokohama/knowledge-hub.git
cd knowledge-hub
```

2. 環境変数の設定（v1以降、Reddit API利用時）

```bash
cp .env.example .env
# .env ファイルを編集してReddit API認証情報を設定
```

3. スキルの利用

Claude Codeのターミナルで以下のコマンドを実行:

```
/daily-trends      # 日次トレンドレポートを生成
/detail-catch-up   # チェックした記事を詳細分析
```

## データソース

| ソース | 取得方法 | 認証 | フェーズ |
|--------|----------|------|----------|
| はてなブックマーク | RSS + jsonlite API | 不要 | v0 |
| Yahoo News等 | WebSearch | 不要 | v0 |
| Reddit | OAuth API | 必要 | v1（予定） |

## ライセンス

プライベートリポジトリ。個人利用のみ。
