# State of JS 2025の調査結果が公開

> 元記事: [StateOfJS 2025 Results are out](https://2025.stateofjs.com/en-US/)
> 分析日: 2026-02-08
> ソース: Reddit
> Reddit: r/vuejs | 18ポイント | 0コメント

---

## 記事の要約

- State of JS 2025の調査結果が公開。JavaScriptエコシステムの安定化と、ワークフローの激変が最大のテーマ
- Svelte 5（Runesベースのシグナルリアクティビティ）が開発者体験（DX）ランキングで首位を獲得
- AIによるコード生成比率が前年の20%から29%に増加。「React vs Vue」から「Human vs Agent」へ
- Viteのダウンロード数がwebpackを逆転。VitestとPlaywrightの利用率が前年比14ポイント増加
- HonoとBunが満足度90%超のS-tierに新たにランクイン

---

## 詳細の深掘り

### エコシステムの安定化とワークフローの変革

State of JS 2025の最大のメッセージは、「10年間の急速な変化を経て、JavaScriptエコシステムは安定期に入った」ということだ。フレームワーク競争は停滞気味だが、その代わりにワークフロー（ビルドツール、テストツール、AI統合）の領域で劇的な変化が起きている。

フレームワークの主戦場はメタフレームワークに移行しており、AstroがNext.jsの王座に挑戦する構図になっている。ビルドツールの世界では、Viteがwebpackのダウンロード数を今年ついに逆転した。

### Svelte 5のDXトップ獲得

Svelte 5が新しい「Runes」と呼ばれるシグナルベースのリアクティビティシステムを導入し、開発者体験（DX）ランキングで首位を獲得した。コミュニティがReactの `useEffect` と依存配列（dependency array）に疲弊し、よりきめ細かい（fine-grained）リアクティビティを求める流れが反映された結果と分析されている。

### AIコード生成の急伸

最も注目すべきトレンドの一つがAI統合だ。開発者がAIの出力として生成するコードの比率が、前年の20%から29%に増加した。まだ過半数には達していないが、バランスは急速に「Human vs Agent」の方向に傾いている。記事は「初めて、最大のストーリーが『React vs Vue』ではなく『Human vs Agent』になった」と表現しており、JavaScript開発の根本的なパラダイムシフトが進行中であることを示唆している。

### テストツールとランタイムの躍進

テスト領域ではVitestとPlaywrightの利用率がそれぞれ前年比14ポイント増加と、急速な普及が進んでいる。Jestからの移行が加速している状況が数字で裏付けられた。

ランタイム/サーバーフレームワーク領域では、HonoとBunが満足度90%超のS-tierに新規ランクイン。軽量・高速なアプローチが開発者に支持されている。

---

## キーポイント

- JavaScriptエコシステムは「フレームワーク競争」から「ワークフロー革新」のフェーズに移行
- AIコード生成比率の20%→29%増加は、開発の在り方の根本的変化を予兆
- Vite/Vitest/Playwrightの三点セットが2026年のモダンJS開発の標準構成に

---

## あなたへの関連性

### 実務への応用

フロントエンドエンジニアとして、State of JS 2025の結果は直接的にスタック選定に影響する。特に以下のポイント：

- **Vitest + Playwright** が業界標準に向かっている（前年比14pt増）ことを踏まえ、新規案件でのテスト構成はこの組み合わせを基本にするのが合理的
- **Viteがwebpackを逆転** した事実は、既存プロジェクトのビルドツール移行の判断材料に
- **Svelte 5のDXトップ** は、Next.js/Nuxt以外のフレームワークの動向として押さえておくべき
- **AIコード生成29%** は、Claude CodeやCodex CLIを活用した開発スタイルが業界全体で定着しつつある証拠

### 学習ヒント

Svelte 5のRunes（シグナルベースのリアクティビティ）は、Vue 3のComposition APIやReactのuseEffectとは異なるアプローチとして、フロントエンドの設計思想を広げる良い学習対象。また、Honoは軽量HTTPフレームワークとして、バックエンド開発（Go, Python）を学ぶ過程でNode.js/Bun上の軽量サーバーとして比較検討できる。

---

## 関連リンク

- [State of JavaScript 2025 公式結果](https://2025.stateofjs.com/en-US/)
- [State of JS 2025 is Out: The "Vibe Shift" is Real（Medium解説記事）](https://hmnshudhmn24.medium.com/state-of-js-2025-is-out-the-vibe-shift-is-real-94841a161997)
- [State of JavaScript 2025: Libraries](https://2025.stateofjs.com/en-US/libraries/)
