# 参考資料: BatFlip（バットフリップ） - NPB野球 海外の反応メディア

> 作成日: 2026-02-11

## 類似サービス・競合

### 野球アンテナサイト（国内）

- [プロ野球まとめアンテナ](https://puroyakyuu.atna.jp/): 5chまとめブログを集約する従来型アンテナサイト。広告過多
- [プロ野球・なんJまとめアンテナ](https://nanj.an-matome.com/): なんJ系野球まとめサイトの集約。広告量が多い
- [野球アンテナだ！](https://yakyuyakyu.antenam.info/): 野球まとめブログの集約サイト
- [野球まとめアンテナ](https://yakyuu.atodeyo.com/): 野球まとめのまとめサイト

→ **差別化ポイント**: 既存サイトは全て5ch/なんJまとめの集約。海外の反応コンテンツは扱っていない。また広告量が過剰でUXが悪い

### 海外の反応サイト（野球関連）

- [メジャーリーグベースボール 海外の反応](https://mlb-kaigai-hannou.com/): MLB選手（大谷翔平等）の海外の反応。MLB特化でNPBは対象外
- [ボールパーク速報 海外の反応](https://www.ballparksokuhou.com/): MLB・NPB・WBCの海外の反応。Reddit含む複数ソースから翻訳
- [ヤクテナ](https://www.yakutena.com/): 海外の反応サイトを集約するアンテナ。野球カテゴリあり

→ **差別化ポイント**: 既存の海外の反応サイトはMLB中心。「海外ファンがNPBをどう見ているか」に特化したサイトはほぼない。また、AI自動生成による更新頻度の高さとコスト効率で差別化できる

### コンテンツソース

- [r/NPB](https://www.reddit.com/r/NPB/) (購読者: 47,351人): NPB全般の英語コミュニティ。メインのコンテンツソース
- [r/baseball](https://www.reddit.com/r/baseball/) (購読者: 3,076,026人): MLB中心だが日本人選手の話題も豊富
- [r/InternationalBaseball](https://www.reddit.com/r/InternationalBaseball/) (購読者: 7,967人): WBC等の国際大会の話題

## 参考記事・ドキュメント

### 技術構成

- [microCMS + Next.js 15でJamstackブログを作ってみよう](https://blog.microcms.io/microcms-next15-jamstack-blog/): Next.js + microCMSの基本構成ガイド（公式）
- [Next.jsとmicroCMSで技術ブログを作ろう](https://zenn.dev/hathle/books/next-microcms-blog-book/viewer/05_microcms): セットアップからデプロイまでの詳細ハンズオン
- [microCMS リッチエディタの操作方法](https://document.microcms.io/manual/rich-editor-usage): リッチエディタでのHTML・外部サービス埋め込みの仕様

### API・データソース

- [X API Rate Limits](https://docs.x.com/x-api/fundamentals/rate-limits): Free tier で月500投稿可能
- [X Developer Portal](https://developer.x.com/): APIキー取得・App登録
- [Supabase Pricing](https://supabase.com/pricing): 無料枠 - 500MB DB、50K MAU、認証機能込み
- [Turso Pricing](https://turso.tech/pricing): 無料枠 - 5GB storage、500M rows read/月（参考比較用）

## 使えそうな技術・ライブラリ

### フロントエンド

- [Next.js](https://nextjs.org/): React フレームワーク。SSG/ISR でパフォーマンスとSEOを両立
- [Chart.js](https://www.chartjs.org/): 軽量なグラフ描画ライブラリ。順位変動グラフに使用
- [Recharts](https://recharts.org/): React 向けグラフライブラリ。Chart.jsの代替候補

### バックエンド・インフラ

- [microCMS](https://microcms.io/): 日本製ヘッドレスCMS。API経由での記事投稿に対応
- [Vercel](https://vercel.com/): Next.js のホスティング。無料枠で運用可能
- [Supabase](https://supabase.com/): PostgreSQL + 認証 + リアルタイム。将来のコメント機能用

### AI・翻訳

- [Claude API (Haiku)](https://docs.anthropic.com/): 低コスト・高品質な翻訳・要約・キュレーション
- [OpenAI API (GPT-4o-mini)](https://platform.openai.com/): Claude Haikuの代替候補

### 既存の資産（knowledge-hub プロジェクト）

- `scripts/fetch_reddit_comments.py`: Redditコメント取得スクリプト（ネストフラット化対応済み）
- `scripts/fetch_reddit_hot.py`: Redditホット投稿取得スクリプト（複数subreddit対応済み）
- `scripts/fetch_yahoo_comments.py`: Yahooニュースコメント取得スクリプト（ページネーション対応済み）
- `scripts/fetch_yahoo_rss.py`: Yahoo ニュースRSS取得スクリプト
