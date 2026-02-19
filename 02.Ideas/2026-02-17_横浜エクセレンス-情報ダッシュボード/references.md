# 参考資料: 横浜エクセレンス 情報ダッシュボード

> 作成日: 2026-02-17

## 類似サービス・競合

### B.LEAGUEスタッツサイト

- [B.LEAGUE公式 成績詳細](https://www.bleague.jp/stats/): 公式スタッツページ。B1/B2の選手別・チーム別成績を2017-18シーズンから閲覧可能。ただしアドバンスドスタッツなし、特定チームへのフォーカス機能なし
- [Bリーグスタッツ](https://bleague-stats.com/): 個人開発のBリーグ専門スタッツサイト。選手・チーム・試合の詳細スタッツをリアルタイムで確認可能。特定チーム特化のダッシュボード機能はない
- [B.League Analytics](https://bleagueanalytics.net/): アドバンスドスタッツ（PER、NetRtg、USG%等）に特化した分析サイト。ブログ記事形式。**B1中心でB2のカバレッジが薄い**
- [Basketballnavi.DB](https://stats.basketballnavi.com/): B1/B2/B3全カテゴリを網羅していたデータベース。BOXスコア、+/-等も掲載。**2021-22シーズンで運営終了**
- [tmotarena.com](https://www.tmotarena.com/database/database.html): 個人運営のBリーグデータサイト。4ファクター分析コラムあり。UIが古い
- [SPAIA](https://spaia.jp/basketball/bleague/b1/stats): スポーツ×AI×データ解析のプラットフォーム。B1/B2の個人・チーム別スタッツ。特定チーム特化機能なし

### 横浜エクセレンス関連

- [横浜エクセレンス公式](https://yokohama-ex.jp/): チーム公式サイト。ニュース、試合日程、選手紹介、チケット情報。詳細スタッツなし
- [B.LEAGUE公式 横浜エクセレンスページ](https://www.bleague.jp/club_detail/?TeamID=714): B.LEAGUE公式内のチームページ。基本情報のみ
- **ファンサイト**: 横浜エクセレンス専門のファンサイトやファン運営データベースは**存在しない**（調査時点）

### 海外スタッツサイト（Bリーグ対応）

- [RealGM - Japanese BLeague](https://basketball.realgm.com/international/league/105/Japanese-BLeague/stats): 英語サイト。個人・チームスタッツ提供
- [Proballers](https://www.proballers.com/basketball/league/281/japan-b1-league): 英語。順位表・スケジュール。B1のみ
- [Flashscore](https://www.flashscore.com/basketball/japan/b-league/): リアルタイムスコア。基本スタッツのみ

## 参考記事・ドキュメント

- [BリーグとNBAのバスケスタッツサイトまとめ (note)](https://note.com/b__s__k__t/n/nf627655e3cc5): 国内外のバスケスタッツサイトの網羅的なまとめ記事

## 使えそうな技術・ライブラリ

### フロントエンド

- [Next.js](https://nextjs.org/): Reactベースのフルスタックフレームワーク。SSG/ISRでパフォーマンス確保
- [Recharts](https://recharts.org/): React向け軽量チャートライブラリ。スタッツ可視化に利用
- [Tailwind CSS](https://tailwindcss.com/): ユーティリティファーストCSSフレームワーク

### スクレイピング・データ取得

- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/): Pythonの定番HTMLパーサー
- [Playwright (Python)](https://playwright.dev/python/): CSRページ対応のHeadlessブラウザ。B.LEAGUE公式がCSRの場合に必要
- [feedparser](https://feedparser.readthedocs.io/): PythonのRSSパーサー。Google News RSS解析用

### インフラ・DB

- [Vercel](https://vercel.com/): Next.jsホスティング。無料枠で運用可能
- [Supabase](https://supabase.com/): PostgreSQLベースのBaaS。無料枠あり。MVP後のDB移行先候補
- [GitHub Actions](https://docs.github.com/ja/actions): CI/CD＋定期バッチ実行。無料枠で十分

### 参考OSSプロジェクト

- [nextjs-sportly](https://github.com/ZacharySal/nextjs-sportly): Next.js + ESPN APIのスポーツ情報サイト。アーキテクチャ参考
- [BallersDash](https://github.com/nogibjj/BallersDash): Streamlitベースのスクレイピング＋NBAスタッツダッシュボード。データパイプライン参考
- [bleaguer（Rパッケージ）](https://bleaguebydata.hatenablog.jp/entry/2019/01/14/083000): B.LEAGUE公式サイトからのデータ取得方法の参考

## 他リーグの参考事例

- [nf3（旧ヌルデータ置き場）](https://nf3.sakura.ne.jp/): NPBの伝説的個人データサイト。カウント別打率、投手別成績等の膨大なニッチデータ。「データベースとして使いたい」の完成形の一つ
- [Football LAB](https://www.football-lab.jp/): Jリーグのデータ分析サイト。CBP等の独自指標。データビジュアライゼーションの参考
- [データで楽しむプロ野球](https://baseballdata.jp/): NPBの独自指標を含むデータ分析サイト
