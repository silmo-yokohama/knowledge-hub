import { Router } from 'express'
import fs from 'fs/promises'
import path from 'path'

const router = Router()

/** お気に入りデータの保存先 */
const FAVORITES_FILE = path.resolve(import.meta.dirname, '../../../01.Trends/favorites.json')

/** お気に入りDeepDive記事 */
interface FavoriteArticle {
  /** DeepDiveファイルのpath（例: "2026-02/2026-02-09_ESLint v10.0.0 released.md"） */
  articleId: string
  /** 記事日付 */
  date: string
  /** 記事タイトル */
  title: string
  /** 登録日時 */
  addedAt: string
}

/**
 * お気に入りデータを読み込む
 */
async function readFavorites(): Promise<FavoriteArticle[]> {
  try {
    const content = await fs.readFile(FAVORITES_FILE, 'utf-8')
    return JSON.parse(content)
  } catch {
    return []
  }
}

/**
 * お気に入りデータを書き込む
 */
async function writeFavorites(favorites: FavoriteArticle[]): Promise<void> {
  await fs.writeFile(FAVORITES_FILE, JSON.stringify(favorites, null, 2), 'utf-8')
}

/**
 * GET /api/favorites
 * お気に入り一覧を返す
 */
router.get('/', async (_req, res) => {
  try {
    const favorites = await readFavorites()
    res.json({ favorites })
  } catch (error) {
    console.error('お気に入り取得エラー:', error)
    res.status(500).json({ error: 'お気に入りの取得に失敗しました' })
  }
})

/**
 * POST /api/favorites
 * お気に入りを登録する
 */
router.post('/', async (req, res) => {
  try {
    const { articleId, date, title } = req.body

    if (!articleId || !title) {
      res.status(400).json({ error: 'articleId と title は必須です' })
      return
    }

    const favorites = await readFavorites()

    // 既に登録済みならスキップ
    if (favorites.some((f) => f.articleId === articleId)) {
      res.json({ success: true, message: '既に登録済みです' })
      return
    }

    favorites.push({
      articleId,
      date,
      title,
      addedAt: new Date().toISOString(),
    })

    await writeFavorites(favorites)
    res.json({ success: true })
  } catch (error) {
    console.error('お気に入り登録エラー:', error)
    res.status(500).json({ error: 'お気に入りの登録に失敗しました' })
  }
})

/**
 * DELETE /api/favorites/:articleId
 * お気に入りを解除する
 * articleId はURLエンコードされたファイルパス
 */
router.delete('/:articleId', async (req, res) => {
  try {
    const articleId = decodeURIComponent(req.params.articleId)
    const favorites = await readFavorites()
    const filtered = favorites.filter((f) => f.articleId !== articleId)

    if (filtered.length === favorites.length) {
      res.status(404).json({ error: 'お気に入りが見つかりません' })
      return
    }

    await writeFavorites(filtered)
    res.json({ success: true })
  } catch (error) {
    console.error('お気に入り削除エラー:', error)
    res.status(500).json({ error: 'お気に入りの削除に失敗しました' })
  }
})

export { router as favoritesRouter }
