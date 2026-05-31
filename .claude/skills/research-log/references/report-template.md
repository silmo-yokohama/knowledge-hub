# リサーチレポート テンプレート

`/research-log` が `01.Research/YYYY-MM-DD_{slug}.md` に保存する Markdown の形式。
**frontmatter のスキーマは将来 Astro のコンテンツコレクションが読む契約**。キー名・型を厳守すること。

## ファイル名規則

- パス: `01.Research/YYYY-MM-DD_{slug}.md`
- `YYYY-MM-DD`: 調査実行日
- `{slug}`: トピックを表す **半角英数字＋ハイフン**（例: `nextjs-server-actions`, `astro-content-collections`）
  - 日本語トピックでも slug は英数字に変換する（URL / ファイル名の安定のため）
  - タイトル（日本語）は frontmatter の `title` に入れる

## frontmatter スキーマ

```yaml
---
title: "Next.js Server Actions の調査"        # 日本語可。一覧・詳細の見出し
description: "Server Actions の仕様・ユースケース・落とし穴を公式起点で調査"  # 一覧カードの要約（1〜2文）
date: 2026-05-31                              # 調査実行日 (YYYY-MM-DD)
tags: [nextjs, react, server-actions]         # 絞り込み用キーワード（英数字小文字推奨、表記ゆれを避ける）
category: "フロントエンド"                     # 大分類（1つ）。例: フロントエンド / AI / インフラ / 設計
sources:                                       # 参照ソース（本文の根拠と一致させる）
  - title: "Server Actions and Mutations"
    url: "https://nextjs.org/docs/..."
    type: official                             # official | community
  - title: "Zenn記事タイトル (著者, 2026-04)"
    url: "https://zenn.dev/..."
    type: community
confidence: medium                             # high | medium | low（公式充足度 + 反証検証の結果ベース）
---
```

### スキーマのルール

- `title` / `description` / `date` / `tags` / `category` / `sources` は **必須**。`confidence` は推奨
- `tags`: 小文字英数字＋ハイフンで統一（`Next.js` ではなく `nextjs`）。表記ゆれは絞り込みを壊すので注意
- `category`: 1 つだけ。既存リサーチの category を Glob で確認し、近いものがあれば揃える（乱立を防ぐ）
- `sources[].type`: 公式一次情報は `official`、それ以外は `community`
- `confidence`: 公式が十分で反証検証も通った → `high` / 部分的 → `medium` / 二次情報メイン → `low`

## 本文構造

```markdown
## 📌 結論 (TL;DR)

<3-5 行で調査全体の要点>

## 🔍 調査結果

### <調査軸1のタイトル>

- <要点を箇条書き>
- <要点>

**根拠**:
- [公式 docs - ページタイトル](URL)
- [Zenn - 記事タイトル (著者, YYYY-MM-DD)](URL)

**引用**:
> <日本語の引用文>
> — [ソースタイトル](URL)

> <英語の原文>
> <日本語訳>
> — [ソースタイトル](URL)

### <調査軸2のタイトル>

...

<!-- 概念の関係・フロー・状態遷移などは Mermaid を埋め込む（サイト側がクライアント描画する） -->
\`\`\`mermaid
flowchart TD
  A[リクエスト] --> B{Server Action}
  B -->|成功| C[再検証]
  B -->|失敗| D[エラー返却]
\`\`\`

## ⚠️ 注意点・矛盾・反証結果

- <矛盾している主張があれば両論併記>
- <反証検証で refuted / uncertain になった主張>
- <古い情報・裏取り不能・発信者の信頼性に関する注記>

## 📚 参照ソース一覧

- 公式:
  - [Title](URL)
- コミュニティ:
  - [Title (著者, 日付)](URL)
```

## 品質基準

- 本文は日本語。英語引用は「原文＋日本語訳」をセット
- **Mermaid 図はテーマに図解要素があれば 1 つ以上**入れる（プロセス→flowchart、状態遷移→stateDiagram、関係→graph、全体像→mindmap）
- frontmatter の `sources` と本文の「参照ソース一覧」は内容を一致させる
- 反証検証の結果を必ず本文に反映する（覆った主張を残さない）
