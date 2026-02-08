# 議論分析の方法論

## コメント取得方法

取得元に応じて適切なスクリプトを使用する。

---

### はてなブックマーク（はてブ）

#### API仕様

はてなブックマークのブコメ取得には `fetch_hatena_comments.py` スクリプトを使用する。

```bash
python3 /home/a/00.knowledge-hub/scripts/fetch_hatena_comments.py "{記事URL}"
```

**重要**: このスクリプトは内部でUser-Agentヘッダを設定済み。直接APIを叩く場合は必ずUser-Agentを付与すること（ないと空レスポンスが返る）。

#### 出力形式

```json
{
  "url": "記事URL",
  "title": "記事タイトル",
  "total_bookmarks": 100,
  "comments_count": 30,
  "comments": [
    {
      "user": "ユーザー名",
      "comment": "コメント本文",
      "timestamp": "2026/02/08 12:00",
      "tags": ["タグ1", "タグ2"]
    }
  ]
}
```

#### 分析スキップ条件

- コメント付きブックマーク（`comments_count`）が **10件未満** の場合

---

### Yahoo ニュース

#### API仕様

Yahoo ニュースのコメント取得には `fetch_yahoo_comments.py` スクリプトを使用する。

```bash
python3 /home/a/00.knowledge-hub/scripts/fetch_yahoo_comments.py "{記事URL}"
```

- 記事URLは `/comments` 付きでも `/comments` なしでも動作する
- 公開APIを使用してコメントを全件取得する（ページネーション自動処理）
- ページ間には1秒のスリープが自動的に入り、レート制限に対応済み

#### 出力形式

```json
{
  "url": "記事URL",
  "article_id": "記事ID（Shannon ID）",
  "total_comments": 141,
  "fetched_comments": 141,
  "comments": [
    {
      "user": "ユーザー名",
      "comment": "コメント本文",
      "post_date": "6日前",
      "comment_id": "UUID",
      "empathy_count": 399,
      "insight_count": 5,
      "negative_count": 15,
      "reply_count": 5,
      "permalink": "https://news.yahoo.co.jp/profile/news/comments/..."
    }
  ]
}
```

#### Yahoo ニュース固有のフィールド

| フィールド | 説明 |
|-----------|------|
| `empathy_count` | 「共感した」の数。コメントへの支持を示す |
| `insight_count` | 「なるほど」の数。有益な情報だと評価された数 |
| `negative_count` | 「うーん」の数。否定的な反応の数 |
| `reply_count` | 返信コメントの数 |
| `post_date` | 投稿日時（「6日前」等の相対表記） |

#### 分析スキップ条件

- コメント総数（`total_comments`）が **10件未満** の場合

#### Yahoo ニュースコメントの分析で特に注目すべき点

- **共感数（empathy_count）が高いコメント**: 多くの読者が共感したコメントは世論の傾向を反映している
- **なるほど数（insight_count）が高いコメント**: 有益な補足情報や新しい視点を含む可能性が高い
- **共感数に対してうーん数（negative_count）が高いコメント**: 賛否が分かれている論点を示す
- **返信数（reply_count）が多いコメント**: 議論が活発に行われている論点

---

### Reddit

#### API仕様

Redditのコメント取得には `fetch_reddit_comments.py` スクリプトを使用する。

```bash
python3 /home/a/00.knowledge-hub/scripts/fetch_reddit_comments.py "{Reddit投稿URL}"
```

- `old.reddit.com` のJSON APIを使用してコメントを取得する
- `www.reddit.com` と `old.reddit.com` の両方のURLに対応
- ネストされた返信コメントもフラット化して取得する
- スコア順（best）でソートして上位約200件を取得
- WebFetchはreddit.comをブロックするため、必ずこのスクリプトを使用すること

#### 出力形式

```json
{
  "url": "Reddit投稿URL",
  "subreddit": "r/programming",
  "post": {
    "title": "投稿タイトル",
    "author": "投稿者名",
    "subreddit": "programming",
    "score": 7091,
    "upvote_ratio": 0.95,
    "num_comments": 1125,
    "url": "リンク先URL（外部記事の場合）",
    "is_self": false,
    "selftext": "自己投稿の本文（is_self=trueの場合）",
    "permalink": "https://www.reddit.com/r/..."
  },
  "total_comments": 1125,
  "fetched_comments": 199,
  "comments": [
    {
      "user": "ユーザー名",
      "comment": "コメント本文",
      "score": 5781,
      "depth": 0,
      "comment_id": "コメントID",
      "permalink": "https://www.reddit.com/r/.../comment_id/",
      "created_utc": 1707350400.0
    }
  ]
}
```

#### Reddit固有のフィールド

| フィールド | 説明 |
|-----------|------|
| `score` | 投票スコア（upvote - downvote）。コミュニティの評価を示す |
| `depth` | コメントのネスト深度。0=トップレベル、1=返信、2=返信の返信... |
| `upvote_ratio` | 投稿の賛成率（0.0〜1.0）。議論の紛糾度を示す |
| `is_self` | 自己投稿かどうか。trueの場合は `selftext` が本文 |
| `selftext` | 自己投稿の本文（Markdown形式） |

#### 分析スキップ条件

- コメント総数（`total_comments`）が **10件未満** の場合

#### Redditコメントの分析で特に注目すべき点

- **スコア（score）が高いコメント**: コミュニティが高く評価したコメントで、主流の意見を反映する
- **depth=0のコメント**: トップレベルの意見。全体的な論調を把握するのに適している
- **depth=1以上で高スコアのコメント**: トップレベルコメントへの反論や補足として注目度が高い
- **upvote_ratio**: 投稿自体の賛否比率。0.5に近いほど賛否が分かれている
- **英語コメント**: Redditのコメントは英語が主体。分析レポートでは日本語に翻訳して記載すること

---

## 共通の分析ルール

### 分析の観点

1. **論点抽出**: コメント全体を俯瞰し、主要な議論テーマを3〜5個抽出する
2. **賛否分析**: 記事の主張に対する賛成・反対・中立の傾向を把握する
3. **補足情報**: コメントから得られる追加情報（事実の補足、別視点、参考リンク等）を収集する
4. **誤り指摘**: 記事の事実誤認や誤解を指摘するコメントがあれば記載する

### 分析のルール

- **中立的な立場**: 分析者は中立的な立場を保ち、どちらかに肩入れしない
- **個人攻撃の除外**: 特定の人物への誹謗中傷、差別的発言は分析対象から除外する
- **コメントの引用**: 特に示唆に富むコメントを1〜3件選び、原文のまま引用する
- **定量的な把握**: 可能であれば「賛成が多数」「意見が二分」など傾向を示す
- **AI要約タグ**（はてブのみ）: `AI要約` タグがついたコメントは自動生成の可能性があるため、分析対象から除外する
- **反応数の活用**（Yahoo ニュースのみ）: 共感数・なるほど数・うーん数を参考に、コメントの影響力や注目度を判断する
- **スコアの活用**（Redditのみ）: スコア（投票数）を参考に、コミュニティの評価を判断する
- **英語コメントの翻訳**（Redditのみ）: 引用するコメントは日本語に翻訳して記載する
