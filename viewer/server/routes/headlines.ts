import { Router } from 'express'
import fs from 'fs/promises'
import path from 'path'

const router = Router()

/** Trendsデータのルートディレクトリ */
const HEADLINES_DIR = path.resolve(import.meta.dirname, '../../../01.Trends/Headlines')

/**
 * GET /api/headlines
 * 利用可能な日付の一覧を返す（件数サマリー付き）
 */
router.get('/', async (_req, res) => {
  try {
    const months = await fs.readdir(HEADLINES_DIR).catch(() => [])
    const dates: Array<{ date: string; path: string; summary: Record<string, number> }> = []

    for (const month of months) {
      const monthDir = path.join(HEADLINES_DIR, month)
      const stat = await fs.stat(monthDir)
      if (!stat.isDirectory()) continue

      const files = await fs.readdir(monthDir)
      for (const file of files) {
        if (!file.endsWith('.json')) continue
        const filePath = path.join(monthDir, file)
        const content = JSON.parse(await fs.readFile(filePath, 'utf-8'))
        dates.push({
          date: content.date,
          path: `${month}/${file}`,
          summary: content.summary,
        })
      }
    }

    // 新しい順にソート
    dates.sort((a, b) => b.date.localeCompare(a.date))
    res.json({ dates })
  } catch (error) {
    console.error('Headlines一覧取得エラー:', error)
    res.status(500).json({ error: 'Headlines一覧の取得に失敗しました' })
  }
})

/**
 * GET /api/headlines/:date
 * 指定日のHeadlinesデータを返す
 */
router.get('/:date', async (req, res) => {
  try {
    const { date } = req.params
    // YYYY-MM-DD → YYYY-MM/YYYY-MM-DD.json
    const month = date.substring(0, 7)
    const filePath = path.join(HEADLINES_DIR, month, `${date}.json`)

    const content = await fs.readFile(filePath, 'utf-8')
    res.json(JSON.parse(content))
  } catch (error) {
    console.error('Headlinesデータ取得エラー:', error)
    res.status(404).json({ error: '指定日のデータが見つかりません' })
  }
})

/**
 * PATCH /api/headlines/:date/articles/:id
 * 記事のchecked状態を更新し、JSONファイルに書き戻す
 */
router.patch('/:date/articles/:id', async (req, res) => {
  try {
    const { date, id } = req.params
    const { checked } = req.body

    if (typeof checked !== 'boolean') {
      res.status(400).json({ error: 'checked は boolean である必要があります' })
      return
    }

    const month = date.substring(0, 7)
    const filePath = path.join(HEADLINES_DIR, month, `${date}.json`)
    const content = JSON.parse(await fs.readFile(filePath, 'utf-8'))

    // 該当記事を検索して更新
    const article = content.articles.find((a: { id: string }) => a.id === id)
    if (!article) {
      res.status(404).json({ error: '記事が見つかりません' })
      return
    }

    article.checked = checked
    // 整形してファイルに書き戻し
    await fs.writeFile(filePath, JSON.stringify(content, null, 2), 'utf-8')

    res.json({ success: true, articleId: id, checked })
  } catch (error) {
    console.error('チェック状態更新エラー:', error)
    res.status(500).json({ error: 'チェック状態の更新に失敗しました' })
  }
})

export { router as headlinesRouter }
