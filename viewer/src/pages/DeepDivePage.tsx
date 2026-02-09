import { useParams } from 'react-router-dom'
import { DeepDiveList } from '../components/deepdives/DeepDiveList.tsx'
import { DeepDiveViewer } from '../components/deepdives/DeepDiveViewer.tsx'
import { useDeepDiveList, useDeepDiveContent } from '../hooks/useDeepDives.ts'
import { useFavorites } from '../hooks/useFavorites.ts'

/**
 * Deep Dives ページ
 * 左: 記事一覧（日付ごとグルーピング）+ お気に入りボタン
 * 右: 選択した記事の Markdown リッチ表示
 */
export function DeepDivePage() {
  const { month, filename } = useParams<{ month?: string; filename?: string }>()
  const { files, loading: listLoading } = useDeepDiveList()
  const { isFavorite, toggleFavorite } = useFavorites()

  // month と filename から API パスを構築
  const selectedPath = month && filename ? `${month}/${filename}` : null
  const { content, loading: contentLoading, error } = useDeepDiveContent(selectedPath)

  return (
    <div className="flex h-[calc(100vh-3.5rem)]">
      {/* 左: 記事一覧 */}
      <aside
        className="w-80 shrink-0 border-r border-[var(--color-border)]
                    bg-[var(--color-surface-sidebar)] overflow-y-auto p-5"
      >
        <h2 className="text-[11px] font-mono font-medium tracking-widest uppercase
                        text-[var(--color-ink-tertiary)] mb-4">
          Deep Dives
        </h2>
        <DeepDiveList
          files={files}
          loading={listLoading}
          isFavorite={isFavorite}
          onToggleFavorite={toggleFavorite}
        />
      </aside>

      {/* 右: Markdown 表示 */}
      <div className="flex-1 overflow-y-auto">
        <DeepDiveViewer
          content={content}
          loading={contentLoading}
          error={error}
        />
      </div>
    </div>
  )
}
