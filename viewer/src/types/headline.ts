/** 記事の取得元 */
export type Source = 'hatena' | 'yahoo' | 'reddit'

/** 個別記事 */
export interface Article {
  /** 一意なID（URLベースで生成） */
  id: string
  /** 記事タイトル（原文） */
  title: string
  /** 日本語タイトル（Reddit英語記事の場合のみ） */
  titleJa: string | null
  /** 記事URL */
  url: string
  /** カテゴリ（AI/LLM, フロントエンド, 野球 等） */
  category: string
  /** データソース */
  source: Source
  /** スコア値（はてブ: ブクマ数、Reddit: ポイント数、Yahoo: 0） */
  score: number
  /** 表示用スコアラベル（"210 users" / "ITmedia NEWS" / "735pt 100comments"） */
  scoreLabel: string
  /** subreddit名（Reddit記事のみ） */
  subreddit: string | null
  /** 概要文（30〜50文字） */
  summary: string
  /** チェック状態（detail-catch-up の対象選定に使用） */
  checked: boolean
}

/** トレンド分析（その日のホットトピック） */
export interface TrendInsight {
  /** トレンドのテーマ（短いタイトル） */
  topic: string
  /** トレンドの説明（なぜ注目されているか、どんな記事があるか） */
  description: string
  /** 関連する記事のID一覧 */
  relatedArticleIds: string[]
}

/** カテゴリ別件数サマリー */
export interface Summary {
  total: number
  byCategory: Record<string, number>
}

/** ヘッドラインレポート全体 */
export interface HeadlineReport {
  /** レポート日付（YYYY-MM-DD） */
  date: string
  /** 生成日時（ISO 8601） */
  generatedAt: string
  /** 使用データソース */
  dataSources: string[]
  /** 件数サマリー */
  summary: Summary
  /** 記事一覧（カテゴリ別→スコア順でソート済み） */
  articles: Article[]
  /** トレンド分析（その日のホットトピック） */
  trendAnalysis: TrendInsight[]
}

/** Headlines一覧APIのレスポンス */
export interface HeadlineDateEntry {
  date: string
  path: string
  summary: Summary
}

/** お気に入りDeepDive記事 */
export interface FavoriteArticle {
  /** DeepDiveファイルのpath（例: "2026-02/2026-02-09_ESLint v10.0.0 released.md"） */
  articleId: string
  /** 記事日付 */
  date: string
  /** 記事タイトル */
  title: string
  /** 登録日時 */
  addedAt: string
}

/** DeepDiveファイルエントリ */
export interface DeepDiveEntry {
  filename: string
  date: string
  title: string
  path: string
}
