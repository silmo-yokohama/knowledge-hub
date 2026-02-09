import type { Rank, Source } from '../../types/headline.ts'

export interface Filters {
  ranks: Set<Rank>
  sources: Set<Source>
  searchText: string
  showCheckedOnly: boolean
}

interface Props {
  filters: Filters
  onChange: (filters: Filters) => void
  /** 利用可能なカテゴリ一覧 */
  categories: string[]
  selectedCategory: string | null
  onCategoryChange: (category: string | null) => void
}

/**
 * フィルターバー
 * ランク / ソース / カテゴリ / テキスト検索 / チェック状態で絞り込み
 */
export function FilterBar({
  filters,
  onChange,
  categories,
  selectedCategory,
  onCategoryChange,
}: Props) {
  /** ランクトグル */
  const toggleRank = (rank: Rank) => {
    const next = new Set(filters.ranks)
    if (next.has(rank)) next.delete(rank)
    else next.add(rank)
    onChange({ ...filters, ranks: next })
  }

  /** ソーストグル */
  const toggleSource = (source: Source) => {
    const next = new Set(filters.sources)
    if (next.has(source)) next.delete(source)
    else next.add(source)
    onChange({ ...filters, sources: next })
  }

  return (
    <div className="space-y-3 mb-6">
      {/* 上段: ランク + ソース + チェック */}
      <div className="flex items-center gap-4 flex-wrap">
        {/* ランクフィルタ */}
        <div className="flex items-center gap-1.5">
          <span className="text-[11px] font-mono text-[var(--color-ink-tertiary)] mr-1">
            RANK
          </span>
          {(['S', 'A', 'B', 'C'] as Rank[]).map((rank) => (
            <RankToggle
              key={rank}
              rank={rank}
              active={filters.ranks.has(rank)}
              onClick={() => toggleRank(rank)}
            />
          ))}
        </div>

        {/* 区切り線 */}
        <div className="w-px h-5 bg-[var(--color-border)]" />

        {/* ソースフィルタ */}
        <div className="flex items-center gap-1.5">
          <span className="text-[11px] font-mono text-[var(--color-ink-tertiary)] mr-1">
            SOURCE
          </span>
          <SourceToggle
            label="はてブ"
            active={filters.sources.has('hatena')}
            onClick={() => toggleSource('hatena')}
            color="var(--color-source-hatena)"
          />
          <SourceToggle
            label="Yahoo"
            active={filters.sources.has('yahoo')}
            onClick={() => toggleSource('yahoo')}
            color="var(--color-source-yahoo)"
          />
          <SourceToggle
            label="Reddit"
            active={filters.sources.has('reddit')}
            onClick={() => toggleSource('reddit')}
            color="var(--color-source-reddit)"
          />
        </div>

        {/* 区切り線 */}
        <div className="w-px h-5 bg-[var(--color-border)]" />

        {/* チェック済みフィルタ */}
        <button
          onClick={() =>
            onChange({ ...filters, showCheckedOnly: !filters.showCheckedOnly })
          }
          className={`text-xs px-2.5 py-1 rounded-md transition-colors duration-200 cursor-pointer border
                      ${
                        filters.showCheckedOnly
                          ? 'bg-[var(--color-checked-bg)] border-[var(--color-checked-border)] text-green-700 dark:text-green-400'
                          : 'border-[var(--color-border)] text-[var(--color-ink-tertiary)] hover:text-[var(--color-ink-secondary)]'
                      }`}
        >
          ✓ チェック済み
        </button>
      </div>

      {/* 下段: テキスト検索 + カテゴリ */}
      <div className="flex items-center gap-3">
        {/* テキスト検索 */}
        <div className="relative flex-1 max-w-sm">
          <svg
            className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--color-ink-tertiary)]"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={1.5}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"
            />
          </svg>
          <input
            type="text"
            placeholder="記事を検索..."
            value={filters.searchText}
            onChange={(e) =>
              onChange({ ...filters, searchText: e.target.value })
            }
            className="w-full pl-9 pr-3 py-1.5 text-sm rounded-lg border border-[var(--color-border)]
                       bg-[var(--color-surface-raised)] text-[var(--color-ink)]
                       placeholder:text-[var(--color-ink-tertiary)]
                       focus:outline-none focus:border-[var(--color-accent)]
                       transition-colors duration-200"
          />
        </div>

        {/* カテゴリ選択 */}
        {categories.length > 0 && (
          <select
            value={selectedCategory ?? ''}
            onChange={(e) =>
              onCategoryChange(e.target.value || null)
            }
            className="text-sm px-3 py-1.5 rounded-lg border border-[var(--color-border)]
                       bg-[var(--color-surface-raised)] text-[var(--color-ink)]
                       focus:outline-none focus:border-[var(--color-accent)]
                       transition-colors duration-200 cursor-pointer"
          >
            <option value="">全カテゴリ</option>
            {categories.map((cat) => (
              <option key={cat} value={cat}>
                {cat}
              </option>
            ))}
          </select>
        )}
      </div>
    </div>
  )
}

/** ランクトグルボタン */
function RankToggle({
  rank,
  active,
  onClick,
}: {
  rank: Rank
  active: boolean
  onClick: () => void
}) {
  const colorMap: Record<Rank, string> = {
    S: 'var(--color-rank-s)',
    A: 'var(--color-rank-a)',
    B: 'var(--color-rank-b)',
    C: 'var(--color-rank-c)',
  }

  return (
    <button
      onClick={onClick}
      className="w-7 h-7 rounded-md text-xs font-mono font-bold
                 transition-all duration-200 cursor-pointer border"
      style={{
        color: active ? 'white' : colorMap[rank],
        backgroundColor: active ? colorMap[rank] : 'transparent',
        borderColor: active ? colorMap[rank] : `color-mix(in srgb, ${colorMap[rank]} 30%, transparent)`,
      }}
    >
      {rank}
    </button>
  )
}

/** ソーストグルボタン */
function SourceToggle({
  label,
  active,
  onClick,
  color,
}: {
  label: string
  active: boolean
  onClick: () => void
  color: string
}) {
  return (
    <button
      onClick={onClick}
      className="text-[11px] px-2 py-1 rounded-md font-medium
                 transition-all duration-200 cursor-pointer border"
      style={{
        color: active ? 'white' : color,
        backgroundColor: active ? color : 'transparent',
        borderColor: active ? color : `color-mix(in srgb, ${color} 30%, transparent)`,
      }}
    >
      {label}
    </button>
  )
}
