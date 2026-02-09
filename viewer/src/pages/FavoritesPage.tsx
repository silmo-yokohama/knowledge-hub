import { Link } from 'react-router-dom'
import { useFavorites } from '../hooks/useFavorites.ts'
import type { FavoriteArticle, DeepDiveEntry } from '../types/headline.ts'

/**
 * お気に入り一覧ページ
 * お気に入り登録した DeepDive 記事を一覧表示
 */
export function FavoritesPage() {
  const { favorites, loading, toggleFavorite } = useFavorites()

  /** お気に入り解除（FavoriteArticle → DeepDiveEntry に変換して渡す） */
  const handleRemove = (fav: FavoriteArticle) => {
    const entry: DeepDiveEntry = {
      path: fav.articleId,
      date: fav.date,
      title: fav.title,
      filename: fav.articleId.split('/').pop() ?? '',
    }
    toggleFavorite(entry)
  }

  if (loading) {
    return (
      <div className="px-10 py-8">
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-20 bg-[var(--color-surface-hover)] rounded-lg animate-pulse" />
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="px-10 py-8">
      <h1 className="font-display text-3xl font-bold text-[var(--color-ink)] mb-8 flex items-center gap-3">
        <svg className="w-6 h-6 text-amber-400" viewBox="0 0 24 24" fill="currentColor">
          <path d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z" />
        </svg>
        Favorites
        <span className="text-sm font-mono font-normal text-[var(--color-ink-tertiary)]">
          {favorites.length}件
        </span>
      </h1>

      {favorites.length === 0 ? (
        <div className="text-center py-16">
          <p className="text-[var(--color-ink-tertiary)] text-sm">
            お気に入りに登録された記事はありません
          </p>
          <p className="text-[var(--color-ink-tertiary)] text-xs mt-2">
            Deep Dives ページで記事の ★ をクリックして登録できます
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-3">
          {favorites.map((fav) => (
            <FavoriteCard
              key={fav.articleId}
              favorite={fav}
              onRemove={() => handleRemove(fav)}
            />
          ))}
        </div>
      )}
    </div>
  )
}

/** お気に入りDeepDive記事カード */
function FavoriteCard({
  favorite,
  onRemove,
}: {
  favorite: FavoriteArticle
  onRemove: () => void
}) {
  return (
    <article
      className="group rounded-lg border border-[var(--color-border-subtle)]
                 bg-[var(--color-surface-raised)] p-5
                 transition-all duration-200 hover:shadow-md hover:border-[var(--color-border)]"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <Link
            to={`/deepdives/${favorite.articleId}`}
            className="text-base font-medium text-[var(--color-ink)] no-underline
                       hover:text-[var(--color-accent)] transition-colors"
          >
            {favorite.title}
          </Link>
          <div className="flex items-center gap-2 mt-2">
            <span className="text-[10px] font-mono text-[var(--color-ink-tertiary)]">
              {favorite.date}
            </span>
            <span className="text-[10px] font-mono text-[var(--color-ink-tertiary)]">
              {new Date(favorite.addedAt).toLocaleDateString('ja-JP')} に登録
            </span>
          </div>
        </div>
        <button
          onClick={onRemove}
          className="text-amber-400 hover:text-amber-500 transition-colors cursor-pointer shrink-0"
          aria-label="お気に入り解除"
        >
          <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
            <path d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z" />
          </svg>
        </button>
      </div>
    </article>
  )
}
