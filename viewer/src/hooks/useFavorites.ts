import { useState, useEffect, useCallback } from 'react'
import type { FavoriteArticle, DeepDiveEntry } from '../types/headline.ts'

/**
 * DeepDive記事のお気に入り機能フック
 */
export function useFavorites() {
  const [favorites, setFavorites] = useState<FavoriteArticle[]>([])
  const [loading, setLoading] = useState(true)

  /** お気に入り一覧を取得 */
  const fetchFavorites = useCallback(async () => {
    try {
      const res = await fetch('/api/favorites')
      const data = await res.json()
      setFavorites(data.favorites)
    } catch (err) {
      console.error('お気に入り取得エラー:', err)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchFavorites()
  }, [fetchFavorites])

  /** 指定DeepDiveがお気に入りかどうか（pathで判定） */
  const isFavorite = useCallback(
    (path: string) => favorites.some((f) => f.articleId === path),
    [favorites],
  )

  /** お気に入り登録/解除をトグル */
  const toggleFavorite = useCallback(
    async (entry: DeepDiveEntry) => {
      const exists = isFavorite(entry.path)

      if (exists) {
        // 楽観的に削除
        setFavorites((prev) => prev.filter((f) => f.articleId !== entry.path))
        try {
          await fetch(`/api/favorites/${encodeURIComponent(entry.path)}`, { method: 'DELETE' })
        } catch {
          fetchFavorites() // ロールバック
        }
      } else {
        // 楽観的に追加
        const newFav: FavoriteArticle = {
          articleId: entry.path,
          date: entry.date,
          title: entry.title,
          addedAt: new Date().toISOString(),
        }
        setFavorites((prev) => [...prev, newFav])
        try {
          await fetch('/api/favorites', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newFav),
          })
        } catch {
          fetchFavorites() // ロールバック
        }
      }
    },
    [isFavorite, fetchFavorites],
  )

  return { favorites, loading, isFavorite, toggleFavorite }
}
