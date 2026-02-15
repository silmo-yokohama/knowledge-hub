import type { Source } from '../../types/headline.ts'

export interface Filters {
  sources: Set<Source>
  searchText: string
  showCheckedOnly: boolean
}

interface Props {
  filters: Filters
  onChange: (filters: Filters) => void
  /** 利用可能なカテゴリ一覧 */
  categories: string[]
  /** 選択中のカテゴリ（空 = 全選択） */
  selectedCategories: Set<string>
  onCategoryChange: (categories: Set<string>) => void
}

/**
 * フィルターバー
 * ソース / カテゴリ / テキスト検索 / チェック状態で絞り込み
 */
export function FilterBar({
  filters,
  onChange,
  categories,
  selectedCategories,
  onCategoryChange,
}: Props) {
  /** ソーストグル */
  const toggleSource = (source: Source) => {
    const next = new Set(filters.sources)
    if (next.has(source)) next.delete(source)
    else next.add(source)
    onChange({ ...filters, sources: next })
  }

  /** カテゴリトグル */
  const toggleCategory = (category: string) => {
    const next = new Set(selectedCategories)
    if (next.has(category)) next.delete(category)
    else next.add(category)
    onCategoryChange(next)
  }

  return (
    <div className="space-y-3 mb-6">
      {/* 上段: ソース + チェック */}
      <div className="flex items-center gap-4 flex-wrap">
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

      {/* 中段: カテゴリ */}
      {categories.length > 0 && (
        <div className="flex items-center gap-1.5 flex-wrap">
          <span className="text-[11px] font-mono text-[var(--color-ink-tertiary)] mr-1">
            CATEGORY
          </span>
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => toggleCategory(cat)}
              className={`text-[11px] px-2 py-1 rounded-md font-medium
                         transition-all duration-200 cursor-pointer border
                         ${
                           selectedCategories.has(cat)
                             ? 'bg-[var(--color-accent)] text-white border-[var(--color-accent)]'
                             : 'border-[var(--color-border)] text-[var(--color-ink-tertiary)] hover:text-[var(--color-ink-secondary)] hover:border-[var(--color-ink-tertiary)]'
                         }`}
            >
              {cat}
            </button>
          ))}
          {/* 選択中の場合、全解除ボタンを表示 */}
          {selectedCategories.size > 0 && (
            <button
              onClick={() => onCategoryChange(new Set())}
              className="text-[10px] px-1.5 py-0.5 text-[var(--color-ink-tertiary)]
                         hover:text-[var(--color-ink-secondary)] cursor-pointer"
            >
              リセット
            </button>
          )}
        </div>
      )}

      {/* 下段: テキスト検索 */}
      <div className="flex items-center gap-3">
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
      </div>
    </div>
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
