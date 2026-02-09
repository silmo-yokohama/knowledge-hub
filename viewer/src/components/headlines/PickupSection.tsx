import type { TrendInsight, Article } from '../../types/headline.ts'

interface Props {
  trends: TrendInsight[]
  articles: Article[]
  /** 記事のチェック状態をトグル */
  onToggleCheck: (articleId: string) => void
}

/**
 * トレンド分析セクション
 * その日のホットトピックをテーマごとにカード形式で表示
 */
export function PickupSection({ trends, articles, onToggleCheck }: Props) {
  /** IDから記事を検索 */
  const findArticle = (articleId: string) =>
    articles.find((a) => a.id === articleId)

  return (
    <section className="mb-10">
      <h2 className="font-display text-xl font-semibold text-[var(--color-ink)] mb-4 flex items-center gap-2">
        <span className="text-[var(--color-accent)]">◆</span>
        Today&apos;s Trends
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-5 gap-4">
        {trends.map((trend, index) => (
          <article
            key={index}
            className="rounded-lg border border-[var(--color-border-subtle)]
                       bg-[var(--color-surface-raised)] p-5
                       transition-all duration-300 hover:shadow-md hover:border-[var(--color-border)]"
          >
            {/* テーマ */}
            <h3 className="font-display text-base font-semibold text-[var(--color-ink)] leading-snug">
              {trend.topic}
            </h3>
            {/* 説明 */}
            <p className="text-xs text-[var(--color-ink-secondary)] mt-2.5 leading-relaxed">
              {trend.description}
            </p>
            {/* 関連記事 */}
            {trend.relatedArticleIds.length > 0 && (
              <div className="mt-3.5 pt-2.5 border-t border-[var(--color-border-subtle)]">
                <span className="text-[10px] font-mono text-[var(--color-ink-tertiary)] uppercase tracking-wider">
                  関連記事
                </span>
                <ul className="mt-1.5 space-y-1">
                  {trend.relatedArticleIds.map((id) => {
                    const article = findArticle(id)
                    if (!article) return null
                    return (
                      <li key={id} className="flex items-center gap-1">
                        {/* チェックボタン */}
                        <button
                          onClick={() => onToggleCheck(article.id)}
                          className="shrink-0 w-3.5 h-3.5 rounded border flex items-center justify-center
                                     transition-all duration-200 cursor-pointer"
                          style={{
                            borderColor: article.checked ? '#22C55E' : 'var(--color-border)',
                            backgroundColor: article.checked ? '#22C55E' : 'transparent',
                          }}
                          aria-label={article.checked ? 'チェック解除' : 'チェック'}
                        >
                          {article.checked && (
                            <svg className="w-2.5 h-2.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                              <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                            </svg>
                          )}
                        </button>
                        <a
                          href={article.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-[11px] text-[var(--color-ink-secondary)] no-underline
                                     hover:text-[var(--color-accent)] transition-colors
                                     line-clamp-1 block flex-1 min-w-0"
                        >
                          <span
                            className="inline-block text-[9px] font-mono font-bold px-1 py-0.5 rounded text-white mr-1 align-middle"
                            style={{ backgroundColor: getRankColor(article.rank) }}
                          >
                            {article.rank}
                          </span>
                          {article.titleJa ?? article.title}
                        </a>
                      </li>
                    )
                  })}
                </ul>
              </div>
            )}
          </article>
        ))}
      </div>
    </section>
  )
}

/** ランクに応じた色を返す */
function getRankColor(rank: string): string {
  const map: Record<string, string> = {
    S: 'var(--color-rank-s)',
    A: 'var(--color-rank-a)',
    B: 'var(--color-rank-b)',
    C: 'var(--color-rank-c)',
  }
  return map[rank] ?? 'var(--color-rank-c)'
}
