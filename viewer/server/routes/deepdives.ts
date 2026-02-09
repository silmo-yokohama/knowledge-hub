import { Router } from 'express'
import fs from 'fs/promises'
import path from 'path'

const router = Router()

/** DeepDivesデータのルートディレクトリ */
const DEEPDIVES_DIR = path.resolve(import.meta.dirname, '../../../01.Trends/DeepDives')

/**
 * GET /api/deepdives
 * DeepDivesファイルの一覧を返す
 */
router.get('/', async (_req, res) => {
  try {
    const months = await fs.readdir(DEEPDIVES_DIR).catch(() => [])
    const files: Array<{ filename: string; date: string; title: string; path: string }> = []

    for (const month of months) {
      const monthDir = path.join(DEEPDIVES_DIR, month)
      const stat = await fs.stat(monthDir)
      if (!stat.isDirectory()) continue

      const entries = await fs.readdir(monthDir)
      for (const filename of entries) {
        if (!filename.endsWith('.md')) continue

        // ファイル名パターン: YYYY-MM-DD_タイトル.md
        const match = filename.match(/^(\d{4}-\d{2}-\d{2})_(.+)\.md$/)
        if (!match) continue

        files.push({
          filename,
          date: match[1],
          title: match[2],
          path: `${month}/${filename}`,
        })
      }
    }

    // 新しい順にソート
    files.sort((a, b) => b.date.localeCompare(a.date) || a.title.localeCompare(b.title))
    res.json({ files })
  } catch (error) {
    console.error('DeepDives一覧取得エラー:', error)
    res.status(500).json({ error: 'DeepDives一覧の取得に失敗しました' })
  }
})

/**
 * GET /api/deepdives/:month/:filename
 * 指定ファイルのMarkdown本文を返す
 */
router.get('/:month/:filename', async (req, res) => {
  try {
    const { month, filename } = req.params
    const filePath = path.join(DEEPDIVES_DIR, month, filename)

    const content = await fs.readFile(filePath, 'utf-8')
    res.json({ filename, content })
  } catch (error) {
    console.error('DeepDive取得エラー:', error)
    res.status(404).json({ error: '指定のDeepDiveファイルが見つかりません' })
  }
})

export { router as deepdivesRouter }
