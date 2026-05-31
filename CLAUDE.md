# knowledge-hub プロジェクトルール

## プロジェクト概要

Web調査（リサーチ）の結果を蓄積し、アイデア・学習・ブログのアウトプットにつなげるリサーチ蓄積ハブ。
Claude Code スキルとしてターミナル上で動作し、蓄積したリサーチは Astro 製サイトでブラウザ閲覧・公開できる。

中心となるのは `/research-log`：公式起点 × コミュニティ補完 × 反証検証で深掘り調査し、結果を `01.Research/` に
frontmatter 付き Markdown として蓄積する（グローバル `/research` の強化版）。

## ディレクトリ構成と用途

| ディレクトリ | 用途 |
|-------------|------|
| `01.Research/` | `/research-log` で生成されるリサーチレポート（frontmatter付き Markdown）の保存先 |
| `01.Research/viewer/` | リサーチ閲覧サイト（Astro 静的サイト）。`01.Research/*.md` を読み込んで表示 |
| `02.Ideas/` | `/new-idea` で生成されるアイデア企画書の保存先 |
| `03.Learnings/` | `/learning-log` で生成される学習ログの保存先 |
| `04.BlogDrafts/` | ブログ下書きの保存先 |
| `99.archive/` | 旧トレンド収集機能（`01.Trends/` 等）のアーカイブ。現役では使わない |

## ファイル命名規則

- **リサーチレポート**: `01.Research/YYYY-MM-DD_{slug}.md`（`{slug}` は半角英数字＋ハイフン。直下にフラット配置）
- **アイデア**: `02.Ideas/YYYY-MM-DD_{title}/`（overview.md / discussion.md / references.md）
- **学習ログ**: `03.Learnings/YYYY-MM-DD_{title}/REPORT.md`
- **ブログ下書き**: `04.BlogDrafts/YYYY-MM-DD_{title}/draft.md`

## レポート生成ルール

- 既存ファイルの上書きは禁止。同名ファイルが存在する場合はユーザーに確認すること
- レポートは全て日本語で記述すること
- Markdown 形式で記述し、VSCode のプレビューで正しく表示されること
- リサーチの frontmatter スキーマは `.claude/skills/research-log/references/report-template.md` に従い、
  ビューアの `01.Research/viewer/src/content.config.ts` と一致させること（title / description / date / tags / category / sources / confidence）

## リサーチ取得手段の優先順位

`/research-log` のサブエージェントが情報を取得する際の順序（詳細は `.claude/skills/research-log/references/source-priority.md`）:

1. `WebSearch` で候補ソースを発見
2. 対象専用 CLI/MCP（GitHub なら `gh` / `mcp__github__*` 等）が使えれば最優先
3. なければ `WebFetch`
4. fallback で `curl`（空ページ / API直叩き / RSS 等）
5. 最終手段でヘッドレスブラウザ、それでも無理なら諦めて別ソース

引用ポリシー: ソース URL は必ず付与。非日本語の引用は「原文＋日本語訳」をセットで。単一ソースの主張は注記する。

## スキル関連

- スキル配置先: `.claude/skills/`（プロジェクトローカル）
  - `research-log` … 深掘り調査＋リポジトリ蓄積（中心スキル）
  - `new-idea` … アイデア壁打ち・企画書作成
  - `learning-log` … 学習ログ生成
- これらのスキルは PROFILE.md に依存しない（必要な文脈は対話の中で把握する）

## ビューア（Astro 静的サイト）

`01.Research/*.md` を読み込んで一覧・詳細を表示する閲覧サイト。配置は `01.Research/viewer/`。

**起動方法**:

```bash
cd 01.Research/viewer
npm run dev   # → http://127.0.0.1:8787/knowledge-hub/
```

- 開発ポートは `8787`・host `127.0.0.1` 固定（`astro.config.mjs`。Windows での 4321 ポート予約 EACCES 回避のため）
- 本文の base パスは `/knowledge-hub`（GitHub Pages プロジェクトページ配信前提。ルート直下では表示されない）
- Node は 24 系（`.nvmrc` = 24、`engines.node >= 24`）
- 機能: タグ/カテゴリ絞り込み（クライアントサイド）、ダークモード（既定ダーク・localStorage 永続）、Mermaid のクライアント描画（テーマ連動）
- コンテンツ収集は `01.Research` 直下の `*.md` のみ（再帰しない。`viewer/` 自身の node_modules 等を巻き込まないため）

## デプロイ（GitHub Pages）

- `.github/workflows/deploy.yml` が `main` への push で Astro をビルドし GitHub Pages へデプロイ
- 公開URL: `https://silmo-yokohama.github.io/knowledge-hub/`
- リサーチページの個別URL: `https://silmo-yokohama.github.io/knowledge-hub/research/YYYY-MM-DD_{slug}/`
- 初回のみリポジトリ Settings → Pages → Source を「GitHub Actions」にする必要がある

## 重要な参照パス

- プロジェクトルート: `c:\Users\silmo\life\knowledge-hub\`（このリポジトリ）
- リサーチ蓄積先: `01.Research/`
- ビューア: `01.Research/viewer/`
- 要件定義書: `99.docs/requirements.md`
