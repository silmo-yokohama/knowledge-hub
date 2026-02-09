import { NavLink } from 'react-router-dom'
import type { DeepDiveEntry } from '../../types/headline.ts'

interface Props {
  files: DeepDiveEntry[]
  loading: boolean
  /** お気に入り判定 */
  isFavorite: (path: string) => boolean
  /** お気に入りトグル */
  onToggleFavorite: (entry: DeepDiveEntry) => void
}

/**
 * DeepDive記事の一覧
 * 日付ごとにグルーピングして表示。各記事にお気に入りボタンを配置
 */
export function DeepDiveList({ files, loading, isFavorite, onToggleFavorite }: Props) {
  if (loading) {
    return (
      <div className="space-y-3">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-12 rounded-lg bg-[var(--color-surface-hover)] animate-pulse" />
        ))}
      </div>
    )
  }

  if (files.length === 0) {
    return (
      <p className="text-sm text-[var(--color-ink-tertiary)] py-8 text-center">
        Deep Dive レポートがまだありません
      </p>
    )
  }

  // 日付ごとにグルーピング
  const grouped = files.reduce<Record<string, DeepDiveEntry[]>>((acc, file) => {
    if (!acc[file.date]) acc[file.date] = []
    acc[file.date].push(file)
    return acc
  }, {})

  return (
    <div className="space-y-6">
      {Object.entries(grouped).map(([date, entries]) => (
        <div key={date}>
          {/* 日付ヘッダー */}
          <h3 className="text-[11px] font-mono font-medium tracking-widest uppercase
                          text-[var(--color-ink-tertiary)] mb-2 sticky top-0
                          bg-[var(--color-surface-sidebar)] py-1">
            {formatDate(date)}
          </h3>
          {/* 記事リスト */}
          <div className="space-y-0.5">
            {entries.map((entry) => {
              const fav = isFavorite(entry.path)
              return (
                <div key={entry.path} className="group flex items-center gap-1">
                  <NavLink
                    to={`/deepdives/${entry.path}`}
                    className={({ isActive }) =>
                      `flex-1 block px-3 py-2.5 rounded-lg text-sm no-underline transition-all duration-200
                       ${
                         isActive
                           ? 'bg-[var(--color-accent-soft)] text-[var(--color-accent)] font-medium'
                           : 'text-[var(--color-ink-secondary)] hover:bg-[var(--color-surface-hover)] hover:text-[var(--color-ink)]'
                       }`
                    }
                  >
                    <span className="line-clamp-2 leading-snug">{entry.title}</span>
                  </NavLink>
                  {/* お気に入りボタン */}
                  <button
                    onClick={(e) => {
                      e.preventDefault()
                      onToggleFavorite(entry)
                    }}
                    className={`shrink-0 p-1 rounded transition-all duration-200 cursor-pointer
                               ${fav ? 'text-amber-400' : 'text-[var(--color-ink-tertiary)] opacity-0 group-hover:opacity-60 hover:!opacity-100'}`}
                    aria-label={fav ? 'お気に入り解除' : 'お気に入り登録'}
                  >
                    <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill={fav ? 'currentColor' : 'none'} stroke="currentColor" strokeWidth={1.5}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z" />
                    </svg>
                  </button>
                </div>
              )
            })}
          </div>
        </div>
      ))}
    </div>
  )
}

function formatDate(dateStr: string): string {
  const date = new Date(dateStr + 'T00:00:00')
  const month = date.getMonth() + 1
  const day = date.getDate()
  const weekdays = ['日', '月', '火', '水', '木', '金', '土']
  return `${month}/${day} (${weekdays[date.getDay()]})`
}
