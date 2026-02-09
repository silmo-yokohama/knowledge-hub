import { useState, useEffect, useCallback } from 'react'
import type { HeadlineReport, HeadlineDateEntry } from '../types/headline.ts'

/**
 * Headlines の日付一覧を取得するフック
 */
export function useHeadlineDates() {
  const [dates, setDates] = useState<HeadlineDateEntry[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch('/api/headlines')
      .then((res) => res.json())
      .then((data) => setDates(data.dates))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  return { dates, loading, error }
}

/**
 * 指定日のHeadlinesデータを取得・操作するフック
 */
export function useHeadlineReport(date: string | null) {
  const [report, setReport] = useState<HeadlineReport | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!date) return
    setLoading(true)
    setError(null)

    fetch(`/api/headlines/${date}`)
      .then((res) => {
        if (!res.ok) throw new Error('データが見つかりません')
        return res.json()
      })
      .then((data) => setReport(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [date])

  /**
   * 記事のチェック状態を切り替える（楽観的更新）
   */
  const toggleCheck = useCallback(
    async (articleId: string) => {
      if (!report || !date) return

      // 楽観的更新: UIを先に更新
      const prevArticles = report.articles
      const updated = report.articles.map((a) =>
        a.id === articleId ? { ...a, checked: !a.checked } : a,
      )
      setReport({ ...report, articles: updated })

      try {
        const article = updated.find((a) => a.id === articleId)
        const res = await fetch(`/api/headlines/${date}/articles/${articleId}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ checked: article?.checked }),
        })
        if (!res.ok) throw new Error('更新失敗')
      } catch {
        // ロールバック
        setReport({ ...report, articles: prevArticles })
      }
    },
    [report, date],
  )

  return { report, loading, error, toggleCheck }
}
