# knowledge-hub

Web調査（リサーチ）の結果を蓄積し、アイデア・学習・ブログのアウトプットにつなげる**リサーチ蓄積ハブ**。
Claude Code スキルとしてターミナル上で動作し、蓄積したリサーチは Astro 製サイトでブラウザ閲覧・公開できます。

公開サイト: **https://silmo-yokohama.github.io/knowledge-hub/**

## 全体像

```text
インプット            処理（Claudeスキル）          蓄積              閲覧・公開
─────────         ──────────────────       ────────       ──────────
調べたいテーマ ──→ /research-log ──────────→ 01.Research/     ──→ Astro サイト
                  （深掘り調査＋反証検証）     （Markdown）        （GitHub Pages）
                                                  │
                                                  └─→ ブログ・学習の素材として再利用

ひらめき      ──→ /new-idea  ──────────────→ 02.Ideas/（企画書 + GitHub Issue）
学習          ──→ /learning-log ───────────→ 03.Learnings/（学習レポート）
```

## 中心スキル: `/research-log`

グローバル `/research` の強化版。**調査結果をチャットに出して終わりにせず、リポジトリに蓄積**します。

```bash
/research-log   # 「調査して残して」「リサーチを蓄積」「ブログネタ用に調べて」でも起動
```

**やっていること**:

1. 調査トピックを 2〜4 軸に分解
1. **公式情報**をサブエージェント並列で調査（3〜5体）→ 充足度を判定
1. **コミュニティ情報**で補完（Qiita / Zenn / はてブ / note / X / Reddit 等）
1. **反証検証（adversarial verify）**：主要な主張を別エージェントに反証させ、覆った主張を除外/注記
1. クロスチェック後、`01.Research/YYYY-MM-DD_{slug}.md` に frontmatter 付き Markdown で保存
1. チャットにも引用付きサマリを提示し、`main` に push → GitHub Pages に反映 → **公開URLを提示**

各レポートは「結論 / 調査結果（根拠URL・引用）/ 注意点・矛盾 / 参照ソース」を含み、Mermaid 図も埋め込めます。

## その他のスキル

| スキル | 起動ワード | 機能 |
|--------|------------|------|
| `/research-log` | リサーチログ / 調査して残して | 深掘り調査＋リポジトリ蓄積（中心） |
| `/new-idea` | アイデア / 壁打ち / 企画 | アイデア壁打ち → 企画書3点 + GitHub Issue |
| `/learning-log` | 学習 / 学習ログ / 勉強 | 学習内容の要約・蓄積（NotebookLM 連携可） |

スキル配置先は `.claude/skills/`。いずれも PROFILE.md に依存せず、必要な文脈は対話で把握します。

## 閲覧サイト（Astro）

`01.Research/*.md` を読み込み、一覧・詳細を静的生成する閲覧サイト。配置は `01.Research/viewer/`。

### 技術スタック

- **Astro 5**（静的生成 / コンテンツコレクション）
- 素の CSS（カスタムプロパティでテーマ管理）
- Mermaid（クライアント描画・テーマ連動）
- Node **24** 系（`.nvmrc` 同梱）

### 起動方法

```bash
cd 01.Research/viewer
npm install        # 初回のみ
npm run dev        # → http://127.0.0.1:8787/knowledge-hub/
```

> ポートは `8787`・host `127.0.0.1` に固定（Windows での 4321 ポート予約による `EACCES` を回避するため）。
> base パスが `/knowledge-hub` のため、URL は必ず `/knowledge-hub/` まで付けて開きます。

### 画面

- **一覧**: 統計タイル（件数 / カテゴリ / タグ / 最終更新）＋ タグ・カテゴリ絞り込み ＋ カードグリッド
- **詳細**: 読みやすい本文 ＋ 右に sticky メタレール（タグ / 公式・コミュニティ別ソース）
- **ダークモード**: 既定ダーク。右のトグルで切替（localStorage 永続、Mermaid も連動）

デザインはミニマル・低彩度のダーク基調（Linear / Vercel 系をより硬質なスイス・グリッドに寄せた方向）。

## デプロイ（GitHub Pages）

`main` への push で `.github/workflows/deploy.yml` が Astro をビルドし GitHub Pages へ自動デプロイします。

- 公開URL: `https://silmo-yokohama.github.io/knowledge-hub/`
- リサーチ個別: `https://silmo-yokohama.github.io/knowledge-hub/research/YYYY-MM-DD_{slug}/`
- 初回のみ Settings → Pages → Source を「GitHub Actions」に設定

## ディレクトリ構成

```
knowledge-hub/
├── .claude/skills/           # Claude Code スキル定義
│   ├── research-log/         #   リサーチ深掘り＋蓄積（中心）
│   ├── new-idea/             #   アイデア壁打ち
│   └── learning-log/         #   学習ログ
├── 01.Research/              # /research-log の出力（Markdown）
│   ├── YYYY-MM-DD_{slug}.md
│   └── viewer/               #   閲覧サイト（Astro）
├── 02.Ideas/                 # /new-idea の出力
├── 03.Learnings/             # /learning-log の出力
├── 04.BlogDrafts/            # ブログ下書き
├── 99.archive/               # 旧トレンド収集機能のアーカイブ
├── 99.docs/                  # 要件定義書など
├── CLAUDE.md                 # プロジェクト固有ルール
└── README.md
```

### ファイル命名規則

| 種別 | パス | 形式 |
|------|------|------|
| リサーチレポート | `01.Research/YYYY-MM-DD_{slug}.md` | Markdown（frontmatter付き） |
| アイデア企画書 | `02.Ideas/YYYY-MM-DD_{title}/` | ディレクトリ（3ファイル） |
| 学習レポート | `03.Learnings/YYYY-MM-DD_{title}/REPORT.md` | Markdown |

リサーチの frontmatter は `title / description / date / tags / category / sources / confidence`。
スキーマは `.claude/skills/research-log/references/report-template.md` と
`01.Research/viewer/src/content.config.ts` を一致させて運用します。

## セットアップ

### 前提条件

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code)
- Node.js **24**（`01.Research/viewer/.nvmrc` 参照。`nvm use` で切替）

### 手順

```bash
git clone https://github.com/silmo-yokohama/knowledge-hub.git
cd knowledge-hub

# 閲覧サイトの依存をインストール
cd 01.Research/viewer && npm install

# Claude Code を起動してリサーチを蓄積
claude
```

```bash
/research-log     # リサーチを深掘りして蓄積
/new-idea          # アイデア壁打ち
/learning-log      # 学習ログを記録
```

## 旧トレンド収集機能について

本プロジェクトは当初、はてブ / Yahoo / Reddit から日次でトレンドを収集する仕組み（`/daily-trends`・
`/detail-catch-up`）を持っていましたが、リサーチ蓄積ハブへ刷新する際に撤去しました。
過去データは `99.archive/01.Trends/` に退避しています（git 履歴にも残存）。

## ライセンス

MIT License
