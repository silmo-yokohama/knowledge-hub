import { useState, useMemo } from 'react'
import type { HeadlineReport, Source } from '../../types/headline.ts'
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
 * サマリー、フィルター、ピックアップ、カテゴリ別カードリストを統合
 */
export function HeadlineList({ report, onToggleCheck }: Props) {
  const [filters, setFilters] = useState<Filters>({
    sources: new Set<Source>(),
    searchText: '',
    showCheckedOnly: false,
  })
  const [selectedCategories, setSelectedCategories] = useState<Set<string>>(new Set())

  /** 利用可能なカテゴリ一覧（重複排除・ソート） */
  const categories = useMemo(() => {
    const cats = new Set(report.articles.map((a) => a.category))
    return Array.from(cats).sort()
  }, [report.articles])

  /** フィルタ適用済みの記事 */
  const filteredArticles = useMemo(() => {
    return report.articles.filter((article) => {
      // ソースフィルタ（空 = 全選択）
      if (filters.sources.size > 0 && !filters.sources.has(article.source)) return false
      // カテゴリフィルタ（空 = 全選択）
      if (selectedCategories.size > 0 && !selectedCategories.has(article.category)) return false
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
  }, [report.articles, filters, selectedCategories])

  /** カテゴリ別にグループ化（カテゴリの表示順はレポートの byCategory の順序） */
  const groupedByCategory = useMemo(() => {
    const groups: { category: string; articles: typeof filteredArticles }[] = []
    const categoryOrder = Object.keys(report.summary.byCategory ?? {})

    // レポートのカテゴリ順に並べる
    for (const cat of categoryOrder) {
      const catArticles = filteredArticles.filter((a) => a.category === cat)
      if (catArticles.length > 0) {
        groups.push({ category: cat, articles: catArticles })
      }
    }

    // byCategory にないカテゴリがあれば末尾に追加
    const knownCats = new Set(categoryOrder)
    const remaining = filteredArticles.filter((a) => !knownCats.has(a.category))
    if (remaining.length > 0) {
      const extraCats = new Set(remaining.map((a) => a.category))
      for (const cat of extraCats) {
        groups.push({
          category: cat,
          articles: remaining.filter((a) => a.category === cat),
        })
      }
    }

    return groups
  }, [filteredArticles, report.summary.byCategory])

  const checkedCount = report.articles.filter((a) => a.checked).length

  /** カテゴリ別件数の上位を表示用に整形 */
  const categoryCountsDisplay = useMemo(() => {
    const entries = Object.entries(report.summary.byCategory ?? {})
      .sort(([, a], [, b]) => b - a)
    return entries
  }, [report.summary.byCategory])

  return (
    <div>
      {/* サマリーバー */}
      <div className="flex items-baseline gap-5 mb-8">
        <h1 className="font-display text-3xl font-bold text-[var(--color-ink)]">
          {formatDateHeading(report.date)}
        </h1>
        <div className="flex items-center gap-3 text-sm font-mono text-[var(--color-ink-tertiary)] flex-wrap">
          <span>{report.summary.total}件</span>
          {categoryCountsDisplay.map(([cat, count]) => (
            <span key={cat} className="text-[var(--color-ink-secondary)]">
              {cat}:{count}
            </span>
          ))}
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
        selectedCategories={selectedCategories}
        onCategoryChange={setSelectedCategories}
      />

      {/* フィルタ結果の件数 */}
      {filteredArticles.length !== report.articles.length && (
        <p className="text-xs text-[var(--color-ink-tertiary)] mb-4 font-mono">
          {filteredArticles.length} / {report.articles.length} 件を表示
        </p>
      )}

      {/* カテゴリ別記事リスト */}
      <div className="space-y-8">
        {groupedByCategory.map((group) => (
          <section key={group.category}>
            {/* カテゴリヘッダー */}
            <div className="flex items-center gap-3 mb-3">
              <h2 className="font-display text-lg font-semibold text-[var(--color-ink)]">
                {group.category}
              </h2>
              <span className="text-xs font-mono text-[var(--color-ink-tertiary)]">
                {group.articles.length}件
              </span>
            </div>
            {/* カードグリッド */}
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-3">
              {group.articles.map((article, index) => (
                <HeadlineCard
                  key={article.id}
                  article={article}
                  onToggleCheck={() => onToggleCheck(article.id)}
                  delay={index * 20}
                />
              ))}
            </div>
          </section>
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
