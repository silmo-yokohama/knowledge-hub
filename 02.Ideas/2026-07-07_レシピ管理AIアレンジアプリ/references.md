# 参考資料: レシピ管理AIアレンジアプリ

> 作成日: 2026-07-07

## 類似サービス・競合

- [CookGo（クックゴー）：レシピ簡単取り込み - App Store](https://apps.apple.com/jp/app/cookgo-%E3%82%AF%E3%83%83%E3%82%AF%E3%82%B4%E3%83%BC-%E3%83%AC%E3%82%B7%E3%83%94%E7%B0%A1%E5%8D%98%E5%8F%96%E3%82%8A%E8%BE%BC%E3%81%BF/id6744090840): TikTok/Instagram/Facebook/Pinterest/任意のURLからレシピを自動インポート。共有→PDF出力機能があるが（実物ファイルで確認済み）、お気に入り・検索は弱く、材料変更時に手順の文章が同期されない点が本アイデアの出発点となった不満
- [CookGo - MWM](https://mwm.ai/apps/cookgo-easy-recipe-import/6744090840): インポート元の一覧。写真からのレシピ生成にも対応
- [10万ダウンロード突破！SNSのレシピが消えない料理サポートアプリ『CookGo』とは（AppBank）](https://www.appbank.net/2026/05/21/iphone-application/3002521.php): CookGoの機能紹介記事
- [レシピはクックパッド - App Store](https://apps.apple.com/jp/app/%E3%82%AF%E3%83%83%E3%82%AF%E3%83%91%E3%83%83%E3%83%89-no-1%E6%96%99%E7%90%86%E3%83%AC%E3%82%B7%E3%83%94%E6%A4%9C%E7%B4%A2%E3%82%A2%E3%83%97%E3%83%AA/id340368403): 国内最大級（約330万件）のレシピ投稿数。「無駄なく食べきれる分量だけ」機能で人数に応じた分量自動計算に対応するが、AIによる好み反映・栄養評価・過去レシピ学習は無い
- [レシピ管理アプリ比較5選（Kuramo Blog）](https://kuramo.app/blog/articles/recipe-app-comparison): クラシルは管理栄養士監修の公式レシピを動画で確認できる点が強み。Cookpadは投稿数、クラシルは動画での手順確認に強みがあるが、いずれも「個人の好みを学習してアレンジする」機能は持たない

## 参考記事・ドキュメント

- [日本食品標準成分表2020年版（八訂）：文部科学省](https://www.mext.go.jp/a_menu/syokuhinseibun/mext_01110.html): 栄養計算の公式データソース
- [八訂におけるエネルギー計算方法（土筆/建帛社 特別寄稿）](https://www.kenpakusha.co.jp/np/news/459/): エネルギー(kcal) = たんぱく質(アミノ酸組成)×4.0 + 脂質(脂肪酸TG当量)×9.0 + 利用可能炭水化物(単糖当量)×3.75 + 食物繊維×2.0 + 糖アルコール×2.4 + 有機酸×3.0 + アルコール×7.0 という八訂公式の計算式を確認
- [食品成分データベース - 文部科学省](https://fooddb.mext.go.jp/): 食品ごとの成分値を検索・CSV取得できる公式データベース（公式APIは無し）
- [日本食品標準成分表2020年版(八訂)のJSONデータ（GitHub, katoharu432, CC BY 4.0）](https://github.com/katoharu432/standards-tables-of-food-composition-in-japan): 食品成分表をJSON化した二次データ。Claude Codeが栄養計算時に参照可能
- [日本人の食事摂取基準（2025年版）策定検討会報告書（厚生労働省）](https://www.mhlw.go.jp/content/10904750/001396865.pdf): 食塩相当量の目標量（成人男性7.5g未満/日、女性6.5g未満/日）を確認。塩分注意の閾値判定に使用
- [Claude Videoの仕組みと制限（note/Fuma）](https://note.com/fuma_ai_lab/n/n598365996689): Claudeによる動画読み取りはyt-dlp+Whisper経由であり、ログイン必須のプラットフォーム（Instagram等）には対応しないことを確認
- [Claude Codeで弊社サイトをリニューアルしました（H2O space）](https://h2o-space.com/news/1713314450): Claude Codeによる制作実例（技術検証の参考として）
- [Supabase Free Tier Limits 2026（ITPath Solutions）](https://www.itpathsolutions.com/supabase-free-tier-limits): 無料枠は7日間操作が無いとプロジェクトが一時停止するが、操作で即座にタイマーがリセットされ約30秒で復帰、データは失われないことを確認

## 使えそうな技術・ライブラリ

- [Claude Code](https://code.claude.com/): レシピのオーサリング（好み参照・栄養計算・スキーマ準拠のYAML生成）とリポジトリへのcommitを担う中核ツール。スマホブラウザの claude.ai/code からも利用可能
- [Astro](https://astro.build/): `01.Research/viewer` で使用中の静的サイトジェネレータ。レシピビューア（一覧・検索・タグ絞り込み）に同じパターンを流用
- [GitHub Pages](https://pages.github.com/): ビューアのホスティング。既存の `.github/workflows/deploy.yml` を流用可能
- [Supabase](https://supabase.com/): お気に入り・週間予定表・買い物リストのチェック状態等、アプリから直接読み書きする「日常操作」データの保存先。無料枠（500MB DB）で個人利用には十分
- [日本食品標準成分表2020年版（八訂）](https://www.mext.go.jp/a_menu/syokuhinseibun/mext_01110.html): 栄養計算の固定データソース・計算方式
