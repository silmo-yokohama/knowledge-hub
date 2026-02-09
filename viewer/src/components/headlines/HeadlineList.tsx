import { useState, useMemo } from 'react'
import type { HeadlineReport, Rank, Source } from '../../types/headline.ts'
import { HeadlineCard } from './HeadlineCard.tsx'
import { FilterBar, type Filters } from './FilterBar.tsx'
import { PickupSection } from './PickupSection.tsx'

interface Props {
  report: HeadlineReport
  /** チェック状態トグル */
  onToggleCheck: (articleId: string) => void
}

/**
 * 記事一覧コンポーネント
 * サマリー、フィルター、ピックアップ、カードリストを統合
 */
export function HeadlineList({ report, onToggleCheck }: Props) {
  const [filters, setFilters] = useState<Filters>({
    ranks: new Set<Rank>(),
    sources: new Set<Source>(),
    searchText: '',
    showCheckedOnly: false,
  })
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)

  /** 利用可能なカテゴリ一覧（重複排除・ソート） */
  const categories = useMemo(() => {
    const cats = new Set(report.articles.map((a) => a.category))
    return Array.from(cats).sort()
  }, [report.articles])

  /** フィルタ適用済みの記事 */
  const filteredArticles = useMemo(() => {
    return report.articles.filter((article) => {
      // ランクフィルタ（空 = 全選択）
      if (filters.ranks.size > 0 && !filters.ranks.has(article.rank)) return false
      // ソースフィルタ（空 = 全選択）
      if (filters.sources.size > 0 && !filters.sources.has(article.source)) return false
      // カテゴリフィルタ
      if (selectedCategory && article.category !== selectedCategory) return false
      // チェック済みフィルタ
      if (filters.showCheckedOnly && !article.checked) return false
      // テキスト検索
      if (filters.searchText) {
        const query = filters.searchText.toLowerCase()
        const searchable = `${article.title} ${article.titleJa ?? ''} ${article.summary} ${article.category}`.toLowerCase()
        if (!searchable.includes(query)) return false
      }
      return true
    })
  }, [report.articles, filters, selectedCategory])

  const checkedCount = report.articles.filter((a) => a.checked).length

  return (
    <div>
      {/* サマリーバー */}
      <div className="flex items-baseline gap-5 mb-8">
        <h1 className="font-display text-3xl font-bold text-[var(--color-ink)]">
          {formatDateHeading(report.date)}
        </h1>
        <div className="flex items-center gap-4 text-sm font-mono text-[var(--color-ink-tertiary)]">
          <span>{report.summary.total}件</span>
          <span className="text-[var(--color-rank-s)]">S:{report.summary.S}</span>
          <span className="text-[var(--color-rank-a)]">A:{report.summary.A}</span>
          <span className="text-[var(--color-rank-b)]">B:{report.summary.B}</span>
          <span className="text-[var(--color-rank-c)]">C:{report.summary.C}</span>
          {checkedCount > 0 && (
            <span className="text-green-600 dark:text-green-400">
              ✓ {checkedCount}件選択中
            </span>
          )}
        </div>
      </div>

      {/* トレンド分析 */}
      {report.trendAnalysis.length > 0 && (
        <PickupSection
          trends={report.trendAnalysis}
          articles={report.articles}
          onToggleCheck={onToggleCheck}
        />
      )}

      {/* フィルターバー */}
      <FilterBar
        filters={filters}
        onChange={setFilters}
        categories={categories}
        selectedCategory={selectedCategory}
        onCategoryChange={setSelectedCategory}
      />

      {/* フィルタ結果の件数 */}
      {filteredArticles.length !== report.articles.length && (
        <p className="text-xs text-[var(--color-ink-tertiary)] mb-4 font-mono">
          {filteredArticles.length} / {report.articles.length} 件を表示
        </p>
      )}

      {/* 記事カードリスト: ワイド画面で2カラムグリッド */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-3">
        {filteredArticles.map((article, index) => (
          <HeadlineCard
            key={article.id}
            article={article}
            onToggleCheck={() => onToggleCheck(article.id)}
            delay={index * 20}
          />
        ))}
      </div>

      {filteredArticles.length === 0 && (
        <div className="text-center py-16">
          <p className="text-[var(--color-ink-tertiary)] text-sm">
            該当する記事が見つかりません
          </p>
        </div>
      )}
    </div>
  )
}

/** 日付ヘッディング */
function formatDateHeading(dateStr: string): string {
  const date = new Date(dateStr + 'T00:00:00')
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const weekdays = ['日', '月', '火', '水', '木', '金', '土']
  const weekday = weekdays[date.getDay()]
  return `${year}年${month}月${day}日（${weekday}）`
}
