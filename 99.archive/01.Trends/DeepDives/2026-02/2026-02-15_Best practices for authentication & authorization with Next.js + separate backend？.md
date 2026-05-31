# Best practices for authentication & authorization with Next.js + separate backend?

> 元記事: [Best practices for authentication & authorization with Next.js + separate backend?](https://old.reddit.com/r/nextjs/comments/1r4ov76/best_practices_for_authentication_authorization/)
> 分析日: 2026-02-15
> ソース: Reddit (r/nextjs)
> スコア: 4pt 10comments

---

## 記事の要約

- Next.jsをフロントエンド、別のバックエンド（REST API）として構成する場合の認証・認可のベストプラクティスについてのディスカッション
- 主な質問: バックエンド分離時の認証方法、セッション管理の責務分担、Next.jsでのルート保護方法、ロールベースの認可の実装方法
- コミュニティの推奨: HttpOnly JWTを使い、Next.js APIをBFF（Backend For Frontend）として中継する構成
- next-authはバックエンド分離構成では使えないため、カスタム実装またはbetter-authを検討すべき
- Next.jsのサーバーコンポーネントでJWTを読み取り、必要な情報をpropsでクライアントコンポーネントに渡すのが推奨パターン

---

## 詳細の深掘り

### HttpOnly JWT + BFFパターン

最も支持された回答は、HttpOnly JWTを使い、Next.js APIルートをBFF（Backend For Frontend）として活用するパターン。フローは以下の通り:

1. **クライアント → Next.js API → 外部バックエンド**: クライアントから直接外部バックエンドにリクエストするのではなく、Next.jsのAPIルートを経由する
2. **JWTの読み取り**: サーバーコンポーネントでのみJWTを読み取り、ロール等の情報をpropsとしてクライアントコンポーネントに渡す
3. **クライアントコンポーネントからのアクセス**: サーバー→クライアントのpropsパターンが使えない場合は、Next.js APIエンドポイントを公開してクライアントからfetchする（next-authやbetter-authの`useSession`フックと同じ仕組み）

### Cookieの設定問題

投稿者が直面した具体的な問題として「クライアント側でCookieを設定しても、サーバーコンポーネントからアクセスできない」という課題があった。解決策は「サーバー側でfetchし、レスポンスからCookieを取得して、ブラウザに設定する」というフロー。credentials（認証情報）の含め方も重要なポイント。

### Next.jsと分離バックエンドの適合性への疑問

興味深い意見として「これはNext.jsが最適解でないケースの一つ」という指摘があった。バックエンドがすべて（セッション管理、ロール等）を処理すべきで、フロントエンドは純粋にUX/デザインの責務だけを担うなら、Next.jsのデフォルトサーバーレンダリングはむしろ複雑さを増す。SEOが必要な部分だけNext.js、それ以外はVite+Reactという分離構成も提案されている。

---

## キーポイント

- バックエンド分離構成でのNext.js認証は「HttpOnly JWT + Next.js APIルート（BFF）」が推奨パターン
- JWTはサーバーコンポーネントでのみ読み取り、クライアントコンポーネントにはpropsで必要情報を渡す
- next-authは分離バックエンド構成では使用不可。better-authの検討を
- Next.jsがすべてのケースで最適解ではない — SEO不要な管理画面等はVite+Reactも選択肢

---

## あなたへの関連性

### 実務への応用

Next.jsとバックエンドの分離構成はフリーランス案件で頻出するパターン:

- **BFFパターンの実装経験**: Next.js APIルートをBFFとして使う構成は、クライアントの既存バックエンドと組み合わせる案件で実践できる
- **認証設計の提案力**: HttpOnly JWT + サーバーコンポーネントでの読み取りパターンを理解しておくと、認証設計の提案時に説得力が増す
- **フレームワーク選定の判断**: 「Next.jsが最適でないケース」を把握しておくことで、プロジェクトに応じた適切なフレームワーク提案ができる

### 学習ヒント

- **認証基盤の実装**: 「まだ詳しくない分野」のバックエンド開発と直結するテーマ。JWT、セッション管理、ロールベースアクセス制御の仕組みを深く理解する良い機会
- **BFFパターン**: Clean Architectureの「インターフェースアダプター層」と関連する設計パターン。DDDの学習と合わせて理解を深められる
- **better-auth**: next-authの代替として注目されているライブラリ。分離バックエンドに対応しており、調査する価値がある

---

## 議論の分析

コメント元: Reddit r/nextjs（10件）

### 主な論点

- バックエンド分離時の認証フロー設計
- Next.js APIルートのBFF活用
- Next.jsの適用範囲の限界

### 肯定的な意見

HttpOnly JWT + BFFパターンの有効性について具体的なコード例を含む回答が支持されている。NestJS + Next.jsの認証に関するYouTubeコースの紹介もあり、学習リソースも共有された。

### 否定的な意見

「Next.jsが最適解でないケースの一つ」という根本的な問いかけがあった。バックエンドが認証を完全に管理するなら、Next.jsのサーバーレンダリングはフロントエンドの認証処理を複雑にするだけという主張。「Proプランでは課金最大化のための設計」というVercelの価格戦略への不信感も背景にある。

### 注目コメント

> HttpOnly JWT。クライアント → Next.js API → 外部バックエンド。JWTはサーバーコンポーネントからのみ読み取り、関連情報（ロール等）はpropsでクライアントコンポーネントに渡す。クライアントコンポーネントからJWTを読む必要がある場合はNext.js APIエンドポイントを公開してfetchする（これはnext-authやbetter-authのuseSessionフックがやっていることと同じ）
> — @Latter_Associate8866 3ポイント

> これはNext.jsが最適解でないケースの一つ。バックエンドがセッション管理やロール等すべてを処理すべきで、フロントの責務は純粋にUX/デザインだけ。Next.jsのデフォルトサーバーレンダリングはむしろ複雑さを増す
> — @Beagles_Are_God 2ポイント
