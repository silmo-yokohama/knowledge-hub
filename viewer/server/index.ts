import express from 'express'
import cors from 'cors'
import { headlinesRouter } from './routes/headlines.js'
import { deepdivesRouter } from './routes/deepdives.js'
import { favoritesRouter } from './routes/favorites.js'

const app = express()
const PORT = 3001

app.use(cors())
app.use(express.json())

// APIルート
app.use('/api/headlines', headlinesRouter)
app.use('/api/deepdives', deepdivesRouter)
app.use('/api/favorites', favoritesRouter)

app.listen(PORT, () => {
  console.log(`API server running on http://localhost:${PORT}`)
})
