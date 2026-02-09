import { NavLink } from 'react-router-dom'
import type { HeadlineDateEntry } from '../types/headline.ts'

interface Props {
  dates: HeadlineDateEntry[]
  loading: boolean
}

/**
 * 日付選択サイドバー
 * 利用可能な日付をリスト表示し、ランク別件数バッジを表示
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
              {/* 日付 */}
              <div className="font-display text-base font-semibold text-[var(--color-ink)]">
                {formatDate(entry.date)}
              </div>
              {/* ランク別件数 */}
              <div className="flex gap-2 mt-2">
                <RankPill rank="S" count={entry.summary.S} />
                <RankPill rank="A" count={entry.summary.A} />
                <RankPill rank="B" count={entry.summary.B} />
                <RankPill rank="C" count={entry.summary.C} />
              </div>
            </NavLink>
          ))}
        </div>
      </div>
    </aside>
  )
}

/** ランク別件数ピル */
function RankPill({ rank, count }: { rank: string; count: number }) {
  const colorMap: Record<string, string> = {
    S: 'var(--color-rank-s)',
    A: 'var(--color-rank-a)',
    B: 'var(--color-rank-b)',
    C: 'var(--color-rank-c)',
  }
  return (
    <span
      className="text-[10px] font-mono font-medium px-1.5 py-0.5 rounded"
      style={{
        color: colorMap[rank],
        backgroundColor: `color-mix(in srgb, ${colorMap[rank]} 12%, transparent)`,
      }}
    >
      {rank}:{count}
    </span>
  )
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
