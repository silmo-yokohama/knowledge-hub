import type { Article } from '../../types/headline.ts'

interface Props {
  article: Article
  /** チェックボックスのトグル */
  onToggleCheck: () => void
  /** 表示アニメーションの遅延（ミリ秒） */
  delay?: number
}

/**
 * 記事カードコンポーネント
 * 左ボーダーのランク色、チェックボックス、お気に入り、メタ情報を表示
 */
export function HeadlineCard({
  article,
  onToggleCheck,
  delay = 0,
}: Props) {
  const rankColor = getRankColor(article.rank)

  return (
    <article
      className={`group relative rounded-lg border transition-all duration-300
                  hover:shadow-md
                  ${
                    article.checked
                      ? 'bg-[var(--color-checked-bg)] border-[var(--color-checked-border)]'
                      : 'bg-[var(--color-surface-raised)] border-[var(--color-border-subtle)] hover:border-[var(--color-border)]'
                  }`}
      style={{
        borderLeftWidth: '3px',
        borderLeftColor: rankColor,
        animationDelay: `${delay}ms`,
      }}
    >
      <div className="p-4 flex gap-3">
        {/* チェックボックス */}
        <button
          onClick={onToggleCheck}
          className="mt-0.5 shrink-0 w-5 h-5 rounded border-2 flex items-center justify-center
                     transition-all duration-200 cursor-pointer"
          style={{
            borderColor: article.checked ? '#22C55E' : 'var(--color-border)',
            backgroundColor: article.checked ? '#22C55E' : 'transparent',
          }}
          aria-label={article.checked ? 'チェック解除' : 'チェック'}
        >
          {article.checked && (
            <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
            </svg>
          )}
        </button>

        {/* メインコンテンツ */}
        <div className="flex-1 min-w-0">
          {/* タイトル */}
          <h3 className="text-sm font-medium leading-relaxed">
            <a
              href={article.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-[var(--color-ink)] no-underline hover:text-[var(--color-accent)]
                         transition-colors duration-200"
            >
              {article.titleJa ?? article.title}
            </a>
          </h3>

          {/* Reddit の場合は原題も表示 */}
          {article.titleJa && (
            <p className="text-xs text-[var(--color-ink-tertiary)] mt-0.5 truncate italic">
              {article.title}
            </p>
          )}

          {/* 概要 */}
          <p className="text-xs text-[var(--color-ink-secondary)] mt-1.5 leading-relaxed">
            {article.summary}
          </p>

          {/* メタ情報 */}
          <div className="flex items-center gap-2 mt-2 flex-wrap">
            {/* ランクバッジ */}
            <span
              className="text-[10px] font-mono font-bold px-1.5 py-0.5 rounded"
              style={{
                color: 'white',
                backgroundColor: rankColor,
              }}
            >
              {article.rank}
            </span>

            {/* カテゴリ */}
            <span className="text-[11px] font-medium text-[var(--color-ink-secondary)]
                           px-1.5 py-0.5 rounded bg-[var(--color-surface-hover)]">
              {article.category}
            </span>

            {/* ソースバッジ */}
            <span
              className="text-[10px] font-mono px-1.5 py-0.5 rounded"
              style={{
                color: getSourceColor(article.source),
                backgroundColor: `color-mix(in srgb, ${getSourceColor(article.source)} 10%, transparent)`,
              }}
            >
              {getSourceLabel(article.source)}
            </span>

            {/* スコア */}
            <span className="text-[11px] font-mono text-[var(--color-ink-tertiary)]">
              {article.scoreLabel}
            </span>

            {/* subreddit */}
            {article.subreddit && (
              <span className="text-[11px] font-mono text-[var(--color-source-reddit)]">
                {article.subreddit}
              </span>
            )}
          </div>
        </div>
      </div>
    </article>
  )
}

function getRankColor(rank: string): string {
  const map: Record<string, string> = {
    S: 'var(--color-rank-s)',
    A: 'var(--color-rank-a)',
    B: 'var(--color-rank-b)',
    C: 'var(--color-rank-c)',
  }
  return map[rank] ?? 'var(--color-rank-c)'
}

function getSourceColor(source: string): string {
  const map: Record<string, string> = {
    hatena: 'var(--color-source-hatena)',
    yahoo: 'var(--color-source-yahoo)',
    reddit: 'var(--color-source-reddit)',
  }
  return map[source] ?? 'var(--color-ink-tertiary)'
}

function getSourceLabel(source: string): string {
  const map: Record<string, string> = {
    hatena: 'はてブ',
    yahoo: 'Yahoo',
    reddit: 'Reddit',
  }
  return map[source] ?? source
}
