# はてなブックマーク RSSカテゴリ一覧

## 取得対象カテゴリ

| カテゴリID | 名称 | RSS URL |
|-----------|------|---------|
| `it` | テクノロジー | `https://b.hatena.ne.jp/hotentry/it.rss` |
| `knowledge` | 学び | `https://b.hatena.ne.jp/hotentry/knowledge.rss` |
| `economics` | 政治経済 | `https://b.hatena.ne.jp/hotentry/economics.rss` |

## 追加カテゴリ（必要に応じて）

| カテゴリID | 名称 | RSS URL |
|-----------|------|---------|
| `entertainment` | エンタメ | `https://b.hatena.ne.jp/hotentry/entertainment.rss` |
| `game` | アニメとゲーム | `https://b.hatena.ne.jp/hotentry/game.rss` |

## スクリプト実行コマンド

```bash
# デフォルト（it, knowledge, economics）
python3 /home/a/00.knowledge-hub/scripts/fetch_hatena_rss.py

# 全カテゴリ指定
python3 /home/a/00.knowledge-hub/scripts/fetch_hatena_rss.py it knowledge economics entertainment game
```

## 注意事項

- カテゴリ間で1秒のスリープが入る（レート制限対策）
- 出力はJSON形式（標準出力）
