import { useState, useEffect } from 'react'
import type { DeepDiveEntry } from '../types/headline.ts'

/**
 * DeepDivesの一覧を取得するフック
 */
export function useDeepDiveList() {
  const [files, setFiles] = useState<DeepDiveEntry[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch('/api/deepdives')
      .then((res) => res.json())
      .then((data) => setFiles(data.files))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  return { files, loading, error }
}

/**
 * 指定ファイルのDeepDive本文を取得するフック
 */
export function useDeepDiveContent(path: string | null) {
  const [content, setContent] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!path) {
      setContent(null)
      return
    }
    setLoading(true)
    setError(null)

    fetch(`/api/deepdives/${path}`)
      .then((res) => {
        if (!res.ok) throw new Error('ファイルが見つかりません')
        return res.json()
      })
      .then((data) => setContent(data.content))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [path])

  return { content, loading, error }
}
