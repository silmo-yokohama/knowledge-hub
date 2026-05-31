// @ts-check
import { defineConfig } from 'astro/config';
import { visit } from 'unist-util-visit';

/**
 * Markdown 内の ```mermaid フェンスを <pre class="mermaid"> に変換する remark プラグイン。
 * Shiki によるハイライト前に html ノードへ差し替えることで、
 * クライアント側の mermaid.js がそのまま図としてレンダリングできるようにする。
 */
function remarkMermaid() {
  return (/** @type {any} */ tree) => {
    visit(tree, 'code', (/** @type {any} */ node, /** @type {number} */ index, /** @type {any} */ parent) => {
      if (node.lang !== 'mermaid' || !parent) return;
      const escaped = String(node.value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
      parent.children[index] = {
        type: 'html',
        value: `<pre class="mermaid">${escaped}</pre>`,
      };
    });
  };
}

// GitHub Pages（プロジェクトページ）向け設定。
// 公開URL: https://silmo-yokohama.github.io/knowledge-hub/
export default defineConfig({
  site: 'https://silmo-yokohama.github.io',
  base: '/knowledge-hub',
  // dev / preview 共通のサーバ設定。
  // Windows で 4321 が予約済み（EACCES）だったため 8787 に固定し、IPv4 で待ち受ける。
  server: {
    host: '127.0.0.1',
    port: 8787,
  },
  markdown: {
    remarkPlugins: [remarkMermaid],
  },
});
