import { useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Sidebar } from '../components/Sidebar.tsx'
import { HeadlineList } from '../components/headlines/HeadlineList.tsx'
import { useHeadlineDates, useHeadlineReport } from '../hooks/useHeadlines.ts'

/**
 * Headlines ページ
 * サイドバー（日付選択）+ メインエリア（記事一覧・フィルタ）
 */
export function HeadlinesPage() {
  const { date } = useParams<{ date?: string }>()
  const navigate = useNavigate()

  const { dates, loading: datesLoading } = useHeadlineDates()
  const { report, loading: reportLoading, error, toggleCheck } = useHeadlineReport(date ?? null)

  // 日付未指定の場合、最新の日付にリダイレクト
  useEffect(() => {
    if (!date && dates.length > 0) {
      navigate(`/headlines/${dates[0].date}`, { replace: true })
    }
  }, [date, dates, navigate])

  return (
    <div className="flex h-[calc(100vh-3.5rem)]">
      {/* サイドバー */}
      <Sidebar dates={dates} loading={datesLoading} />

      {/* メインコンテンツ */}
      <div className="flex-1 overflow-y-auto px-10 py-8">
        {reportLoading && (
          <div className="space-y-3">
            <div className="h-8 w-64 bg-[var(--color-surface-hover)] rounded animate-pulse" />
            <div className="h-4 w-48 bg-[var(--color-surface-hover)] rounded animate-pulse" />
            {[1, 2, 3, 4, 5].map((i) => (
              <div
                key={i}
                className="h-24 bg-[var(--color-surface-hover)] rounded-lg animate-pulse"
              />
            ))}
          </div>
        )}

        {error && (
          <div className="flex items-center justify-center h-64">
            <p className="text-sm text-[var(--color-ink-tertiary)]">{error}</p>
          </div>
        )}

        {report && (
          <HeadlineList
            report={report}
            onToggleCheck={toggleCheck}
          />
        )}

        {!date && !datesLoading && dates.length === 0 && (
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <p className="font-display text-lg text-[var(--color-ink-tertiary)]">
                トレンドレポートがまだありません
              </p>
              <p className="text-sm text-[var(--color-ink-tertiary)] mt-2">
                <code className="font-mono text-[var(--color-accent)]">/daily-trends</code> を実行してレポートを生成してください
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
