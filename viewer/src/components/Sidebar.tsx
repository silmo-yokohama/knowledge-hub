import { NavLink } from 'react-router-dom'
import type { HeadlineDateEntry } from '../types/headline.ts'

interface Props {
  dates: HeadlineDateEntry[]
  loading: boolean
}

/**
 * 日付選択サイドバー
 * 利用可能な日付をリスト表示し、カテゴリ別件数を表示
 */
export function Sidebar({ dates, loading }: Props) {
  if (loading) {
    return (
      <aside className="w-72 shrink-0 border-r border-[var(--color-border)] p-5">
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div
              key={i}
              className="h-20 rounded-lg bg-[var(--color-surface-hover)] animate-pulse"
            />
          ))}
        </div>
      </aside>
    )
  }

  return (
    <aside
      className="w-72 shrink-0 border-r border-[var(--color-border)]
                  bg-[var(--color-surface-sidebar)] overflow-y-auto"
    >
      <div className="p-5">
        <h2 className="text-[11px] font-mono font-medium tracking-widest uppercase
                        text-[var(--color-ink-tertiary)] mb-4">
          Archives
        </h2>
        <div className="space-y-1.5">
          {dates.map((entry) => (
            <NavLink
              key={entry.date}
              to={`/headlines/${entry.date}`}
              className={({ isActive }) =>
                `block rounded-lg p-3 transition-all duration-200 no-underline group
                 ${
                   isActive
                     ? 'bg-[var(--color-surface-raised)] shadow-sm border border-[var(--color-border)]'
                     : 'hover:bg-[var(--color-surface-hover)] border border-transparent'
                 }`
              }
            >
              {/* 日付と件数 */}
              <div className="flex items-baseline justify-between">
                <span className="font-display text-base font-semibold text-[var(--color-ink)]">
                  {formatDate(entry.date)}
                </span>
                <span className="text-[11px] font-mono text-[var(--color-ink-tertiary)]">
                  {entry.summary.total}件
                </span>
              </div>
              {/* カテゴリ別件数（上位3つ） */}
              {entry.summary.byCategory && (
                <div className="flex gap-1.5 mt-2 flex-wrap">
                  {getTopCategories(entry.summary.byCategory, 3).map(([cat, count]) => (
                    <CategoryPill key={cat} category={cat} count={count} />
                  ))}
                </div>
              )}
            </NavLink>
          ))}
        </div>
      </div>
    </aside>
  )
}

/** カテゴリ別件数ピル */
function CategoryPill({ category, count }: { category: string; count: number }) {
  return (
    <span
      className="text-[10px] font-mono font-medium px-1.5 py-0.5 rounded
                 text-[var(--color-ink-secondary)] bg-[var(--color-surface-hover)]"
    >
      {category}:{count}
    </span>
  )
}

/** カテゴリ別件数の上位N件を返す */
function getTopCategories(byCategory: Record<string, number>, n: number): [string, number][] {
  return Object.entries(byCategory)
    .sort(([, a], [, b]) => b - a)
    .slice(0, n)
}

/** 日付フォーマット: "2026-02-09" → "2月9日 (日)" */
function formatDate(dateStr: string): string {
  const date = new Date(dateStr + 'T00:00:00')
  const weekdays = ['日', '月', '火', '水', '木', '金', '土']
  const month = date.getMonth() + 1
  const day = date.getDate()
  const weekday = weekdays[date.getDay()]
  return `${month}月${day}日 (${weekday})`
}
