# knowledge-hub プロジェクトルール

## プロジェクト概要

日々のインプット（ニュース・学習）を一元管理し、アイデアやアウトプットにつなげるナレッジハブ。
Claude Codeスキルとして動作し、ターミナル上で完結する。

## ディレクトリ構成と用途

| ディレクトリ | 用途 |
|-------------|------|
| `01.Trends/Headlines/` | `/daily-trends` で生成されるトレンドレポートの保存先 |
| `01.Trends/DeepDives/` | `/detail-catch-up` で生成される詳細分析レポートの保存先 |
| `02.Ideas/` | `/new-idea` で生成されるアイデア企画書の保存先（v1以降） |
| `03.Learnings/` | 学習ログスキルで生成されるナレッジの保存先（v2以降） |
| `04.BlogDrafts/` | `/write-blog` で生成されるブログ下書きの保存先（v3以降） |
| `scripts/` | データ取得用のユーティリティスクリプト |

## ファイル命名規則

- **Headlines レポート**: `01.Trends/Headlines/YYYY-MM/YYYY-MM-DD.md`
- **DeepDives レポート**: `01.Trends/DeepDives/YYYY-MM/YYYY-MM-DD_{kebab-case-title}.md`
- **アイデア**: `02.Ideas/YYYY-MM-DD_{title}/`
- **学習ログ**: `03.Learnings/YYYY-MM-DD_{title}/REPORT.md`
- **ブログ下書き**: `04.BlogDrafts/YYYY-MM-DD_{title}/draft.md`

## レポート生成ルール

- 既存ファイルの上書きは禁止。同名ファイルが存在する場合はユーザーに確認すること
- レポートは全て日本語で記述すること
- Markdown形式で記述し、VSCodeのプレビューで正しく表示されること

## 外部API利用ルール

- はてなブックマークRSS: カテゴリ間で1秒以上のスリープを入れること
- はてなブックマークブコメAPI: User-Agentヘッダを必ず付与すること（ないと空レスポンスになる）
- 全てのHTTPリクエスト: User-Agentヘッダ `knowledge-hub/0.1` を付与すること
- レート制限を考慮し、連続リクエストには適切な間隔を設けること

## スキル関連

- スキル配置先: `~/.claude/skills/`
- プロフィール情報: `/home/a/00.knowledge-hub/PROFILE.md`
- スクリプト配置先: `/home/a/00.knowledge-hub/scripts/`

## 重要な参照パス

- プロジェクトルート: `/home/a/00.knowledge-hub/`
- PROFILE.md: `/home/a/00.knowledge-hub/PROFILE.md`
- requirements.md: `/home/a/00.knowledge-hub/requirements.md`
