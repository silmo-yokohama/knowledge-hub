# 参考資料: 横浜エクセレンス ファンサイト

> 作成日: 2026-02-08

## 類似サービス・競合

- [B.League Analytics](https://bleagueanalytics.net/): Bリーグ全体のスタッツ分析サイト。チーム別ランキングやディフェンス分析が充実。ただしリーグ全体対象で、特定チーム特化ではない
- [Bリーグスタッツ](https://bleague-stats.com/): リアルタイムの詳細スタッツを提供。選手・チーム・試合別のデータが閲覧可能
- [Basketballnavi.DB](https://stats.basketballnavi.com/): Bリーグのクラブ一覧・試合日程・戦績を提供するデータベースサイト
- [SPAIA](https://spaia.jp/basketball/bleague/b1/stats/team): スポーツAIによるBリーグスタッツ分析。チーム別・個人別の成績を提供
- [B.LEAGUE公式 スタッツページ](https://www.bleague.jp/stats/): 公式の成績詳細ページ。網羅的だが、UI/UXに難があり情報が散らばっている

**差別化ポイント**: 上記はいずれもBリーグ全体を対象としている。横浜エクセレンスに特化したファンサイトは現時点で存在しない。スタッツ＋観戦記の組み合わせも独自性がある。

## データソース

- [B.LEAGUE公式 順位表（B2）](https://www.bleague.jp/standings/?tab=2): リーグ順位
- [B.LEAGUE公式 チーム詳細](https://www.bleague.jp/club_detail/?TeamID=714&tab=1): 横浜エクセレンスのチーム情報
- [B.LEAGUE公式 選手一覧](https://www.bleague.jp/club_detail/?TeamID=714&tab=2): 横浜エクセレンスのロースター
- [Yahoo Sports Bリーグ B2](https://sports.yahoo.co.jp/basket/bleague/b2): 試合リアルタイム情報
- [Yahoo Sports Bリーグニュース](https://sports.yahoo.co.jp/list/news/bleague?genre=bleague&category=253): ニュース（将来対応）

## 参考記事・ドキュメント

- [B.LEAGUEとNBAのバスケスタッツサイトまとめ（note）](https://note.com/b__s__k__t/n/nf627655e3cc5): 既存のスタッツサイトの比較とまとめ
- [バスケットボールキング Bリーグスタッツレポート](https://basketballking.jp/news/japan/20251023/572746.html): B.LEAGUE公式スタッツレポートの紹介記事

## 使えそうな技術・ライブラリ

- [Next.js](https://nextjs.org/): フロントエンドフレームワーク。SSG/ISRによるパフォーマンス最適化
- [Tailwind CSS](https://tailwindcss.com/): ユーティリティファーストCSSフレームワーク
- [Recharts](https://recharts.org/): React向けチャートライブラリ。スタッツの可視化に使用
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/): Pythonスクレイピングライブラリ。データ取得バッチに使用
- [Vercel](https://vercel.com/): ホスティング。Next.jsとの相性最良、無料枠あり
- [Supabase](https://supabase.com/): PostgreSQLベースのBaaS。無料枠で十分な規模

## 横浜エクセレンス公式情報

- [横浜エクセレンス 公式サイト](https://yokohama-ex.jp/): チーム公式。カラーコードの参考元
- [横浜エクセレンス X（旧Twitter）](https://x.com/yokohamaex_): 公式SNS
- [横浜エクセレンス B.LEAGUE公式ページ](https://www.bleague.jp/club_detail/?TeamID=714): Bリーグ内のチームページ
