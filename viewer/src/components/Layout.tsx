import type { ReactNode } from 'react'
import { NavLink } from 'react-router-dom'
import { ThemeToggle } from './ThemeToggle.tsx'

interface Props {
  children: ReactNode
}

/**
 * アプリ全体のレイアウト
 * ヘッダー（ナビゲーション + テーマ切り替え）+ メインコンテンツ
 * ワイドスクリーン対応: max-width制限なし、全幅活用
 */
export function Layout({ children }: Props) {
  return (
    <div className="min-h-screen flex flex-col">
      {/* ヘッダー */}
      <header
        className="sticky top-0 z-50 border-b border-[var(--color-border)]
                    bg-[var(--color-surface)]/95 backdrop-blur-sm"
      >
        <div className="px-8 h-14 flex items-center justify-between">
          {/* ロゴ & タイトル */}
          <NavLink to="/" className="flex items-center gap-3 no-underline">
            <span
              className="font-display text-xl font-semibold tracking-tight
                         text-[var(--color-ink)]"
            >
              Knowledge Hub
            </span>
            <span
              className="text-[10px] font-mono font-medium tracking-widest uppercase
                         text-[var(--color-ink-tertiary)] border border-[var(--color-border)]
                         px-1.5 py-0.5 rounded"
            >
              Trends
            </span>
          </NavLink>

          {/* ナビゲーション */}
          <nav className="flex items-center gap-1">
            <NavItem to="/" label="Headlines" />
            <NavItem to="/deepdives" label="Deep Dives" />
            <NavItem to="/favorites" label="Favorites" />
            <div className="w-px h-5 bg-[var(--color-border)] mx-2" />
            <ThemeToggle />
          </nav>
        </div>
      </header>

      {/* メインコンテンツ: 全幅使用 */}
      <main className="flex-1">
        {children}
      </main>
    </div>
  )
}

/** ナビゲーションリンク */
function NavItem({ to, label }: { to: string; label: string }) {
  return (
    <NavLink
      to={to}
      end={to === '/'}
      className={({ isActive }) =>
        `px-3 py-1.5 rounded-md text-sm font-medium transition-colors duration-200 no-underline
         ${
           isActive
             ? 'bg-[var(--color-accent-soft)] text-[var(--color-accent)]'
             : 'text-[var(--color-ink-secondary)] hover:text-[var(--color-ink)] hover:bg-[var(--color-surface-hover)]'
         }`
      }
    >
      {label}
    </NavLink>
  )
}
