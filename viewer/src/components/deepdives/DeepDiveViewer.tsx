import Markdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeHighlight from 'rehype-highlight'

interface Props {
  content: string | null
  loading: boolean
  error: string | null
}

/**
 * DeepDive レポートの Markdown リッチ表示
 * react-markdown + remark-gfm + rehype-highlight で
 * テーブル、コードブロック、引用等を美しく表示
 */
export function DeepDiveViewer({ content, loading, error }: Props) {
  if (loading) {
    return (
      <div className="animate-pulse space-y-4 p-8">
        <div className="h-8 bg-[var(--color-surface-hover)] rounded w-3/4" />
        <div className="h-4 bg-[var(--color-surface-hover)] rounded w-full" />
        <div className="h-4 bg-[var(--color-surface-hover)] rounded w-5/6" />
        <div className="h-4 bg-[var(--color-surface-hover)] rounded w-4/6" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-sm text-[var(--color-ink-tertiary)]">{error}</p>
      </div>
    )
  }

  if (!content) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <p className="font-display text-lg text-[var(--color-ink-tertiary)]">
            左のリストから記事を選択してください
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="px-12 py-10 max-w-none">
      <Markdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeHighlight]}
        components={{
          /* 見出し */
          h1: ({ children }) => (
            <h1 className="font-display text-3xl font-bold text-[var(--color-ink)] mt-0 mb-5 pb-4
                           border-b border-[var(--color-border)]">
              {children}
            </h1>
          ),
          h2: ({ children }) => (
            <h2 className="font-display text-2xl font-semibold text-[var(--color-ink)] mt-10 mb-4">
              {children}
            </h2>
          ),
          h3: ({ children }) => (
            <h3 className="font-display text-xl font-semibold text-[var(--color-ink)] mt-8 mb-3">
              {children}
            </h3>
          ),
          /* 段落 */
          p: ({ children }) => (
            <p className="text-base text-[var(--color-ink-secondary)] leading-[1.9] mb-5">
              {children}
            </p>
          ),
          /* リスト */
          ul: ({ children }) => (
            <ul className="text-base text-[var(--color-ink-secondary)] leading-[1.9] mb-5 pl-5
                           list-disc marker:text-[var(--color-accent)]">
              {children}
            </ul>
          ),
          ol: ({ children }) => (
            <ol className="text-base text-[var(--color-ink-secondary)] leading-[1.9] mb-5 pl-5
                           list-decimal marker:text-[var(--color-accent)]">
              {children}
            </ol>
          ),
          li: ({ children }) => (
            <li className="mb-1">{children}</li>
          ),
          /* 引用 */
          blockquote: ({ children }) => (
            <blockquote className="border-l-3 border-[var(--color-accent)] pl-4 py-1 my-4
                                   bg-[var(--color-accent-soft)] rounded-r-lg">
              {children}
            </blockquote>
          ),
          /* コード（インライン） */
          code: ({ className, children, ...props }) => {
            const isBlock = className?.includes('language-')
            if (isBlock) {
              return (
                <code className={`${className} text-sm`} {...props}>
                  {children}
                </code>
              )
            }
            return (
              <code className="text-sm font-mono bg-[var(--color-surface-hover)] text-[var(--color-accent)]
                             px-1.5 py-0.5 rounded" {...props}>
                {children}
              </code>
            )
          },
          /* テーブル */
          table: ({ children }) => (
            <div className="overflow-x-auto my-4">
              <table className="w-full text-sm border-collapse">{children}</table>
            </div>
          ),
          th: ({ children }) => (
            <th className="text-left text-xs font-semibold text-[var(--color-ink-secondary)]
                           uppercase tracking-wider py-2 px-3 border-b-2 border-[var(--color-border)]">
              {children}
            </th>
          ),
          td: ({ children }) => (
            <td className="py-2 px-3 text-sm text-[var(--color-ink-secondary)]
                           border-b border-[var(--color-border-subtle)]">
              {children}
            </td>
          ),
          /* リンク */
          a: ({ href, children }) => (
            <a
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              className="text-[var(--color-accent)] no-underline hover:underline
                         underline-offset-2 decoration-[var(--color-accent)]/40"
            >
              {children}
            </a>
          ),
          /* 水平線 */
          hr: () => <hr className="my-8 border-t border-[var(--color-border)]" />,
          /* 強調 */
          strong: ({ children }) => (
            <strong className="font-semibold text-[var(--color-ink)]">{children}</strong>
          ),
        }}
      >
        {content}
      </Markdown>
    </div>
  )
}
