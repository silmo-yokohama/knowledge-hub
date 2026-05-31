# Claude Code 拡張機能の整理（Skills / Agents / Plugins / Agent Teams）

> 元記事: [Claude Code 拡張機能の整理（Skills / Agents / Plugins / Agent Teams）](https://zenn.dev/singularity/articles/2026-02-07-claude-code-extensibility-memo)
> 分析日: 2026-02-10
> ソース: はてブ
> ブックマーク数: 221 users

---

## 記事の要約
- Claude Codeの拡張機能を体系的に整理した記事。Plugin（配布パッケージ）にはSkills、Agents、Hooks、MCPサーバーの4つを含められる
- Slash CommandsよりSkillsを使うべき。YAML frontmatterでツール制限やモデル指定が可能であり、Plugin化も見据えた設計に適している
- Sub-agentの内部処理はメインコンテキストを消費しないが、戻り値は消費する（コンテキスト節約の重要知見）
- Skill=タスク定義（何をするか）、Agent=実行者の定義（どう振る舞うか）という明確な役割分離がある
- Skill作成の運用ルールとして、フォアグラウンドで構築・確認後にSub-agent化し、maxTurns設定を必須とすることが推奨されている

---

## 詳細の深掘り

### Plugin構成の4要素とSkillsの優位性

Claude Codeの配布可能なPluginは以下の4要素で構成される。

| 要素 | 役割 |
|------|------|
| Skills | ワークフロー定義（何をするか） |
| Agents | 実行者定義（どう振る舞うか） |
| Hooks | イベント駆動の自動処理 |
| MCPサーバー | 外部サービス連携 |

記事はSlash CommandsよりSkillsを明確に推奨している。理由は以下の通り。

1. Slash Commandsで可能な全機能をカバーしている
2. `disable-model-invocation` で自動発動の制御が可能
3. Plugin に含められるため、将来の配布・共有を見据えた設計ができる

YAML frontmatterの主要フィールドは以下の通り。

| フィールド | 説明 |
|-----------|------|
| `description` | Claudeが自動判断に使用する説明文 |
| `allowed-tools` | 許可するツールの指定 |
| `model` | sonnet / opus / haiku から選択 |
| `context` | `fork` でSub-agent実行 |
| `maxTurns` | 最大ターン数（暴走防止のため必須） |
| `disable-model-invocation` | 自動発動を無効化する設定 |

### Sub-agentのコンテキスト消費メカニズム

記事で最も実践的な知見は、Sub-agentとメインコンテキストの消費関係である。

- **Sub-agentの内部処理**（ファイル読み込み、ツール呼び出し等）: メインのコンテキストを**消費しない**
- **Sub-agentの戻り値**: メインのコンテキストを**消費する**

つまり、Sub-agent内でどれだけ大量のファイルを読み書きしても、メイン側のコンテキストウィンドウには影響しない。しかし、Sub-agentがメインに返す結果テキストはコンテキストを消費する。

最適な運用パターンは「結果をファイルに書き出して、返答は最小限にする」こと。これにより、Sub-agentの処理結果を失わずにメインのコンテキストを節約できる。

```
Skill: /review-pr（ワークフロー定義）
  └── Agent: code-reviewer（実行者）を context: fork で呼び出す
       └── 結果はファイルに書き出し、返答は「完了。結果は /path/to/result.md に出力」のみ
```

### SkillとAgentの設計思想と運用ルール

SkillとAgentの関係は「タスク定義」と「実行者定義」の分離として理解するのが正確である。

- **Skill**: 「何をするか」を定義するワークフロー。`/review-pr` のようなタスク
- **Agent**: 「どう振る舞うか」を定義する実行者。`code-reviewer` のような人格・専門性

複数のSkillから同じAgentを使い回せるのが設計上の大きな利点である。例えば、`/review-pr` と `/review-code` という2つのSkillが、どちらも `code-reviewer` Agentを呼び出すという構成が可能になる。

Skill作成の推奨プロセスは以下の5ステップである。

1. **フォアグラウンドで構築**: まず通常のSkillとして作成する
2. **動作確認・デバッグ**: 期待通りに動くことを確認する
3. **Sub-agent化**: `context: fork` を追加して独立実行に切り替え
4. **出力の最適化**: 結果はファイルに書き出し、返答は最小限にする
5. **maxTurns設定**: 必須。10ターン程度が目安で、暴走防止に不可欠

特に `maxTurns` の設定漏れはSub-agentが延々とループする原因になるため、必ず設定すべきと強調されている。

---

## キーポイント
- **Slash CommandsよりSkills**: Plugin化を見据えるなら、最初からSkillsで作るべき。YAML frontmatterによるツール制限・モデル指定が強力
- **コンテキスト消費の非対称性**: Sub-agentの内部処理はメインを消費しないが、戻り値は消費する。「ファイルに書き出して返答は最小限」が黄金パターン
- **maxTurnsは必須設定**: 設定しないとSub-agentが暴走するリスクがあり、10ターン程度を目安とする

---

## あなたへの関連性

### 実務への応用
Claude Code Skillsに強い関心を持っているなら、この記事は必読レベルの整理資料である。特に、既に `/daily-trends` や `/new-idea` などのSkillsを運用しているナレッジハブプロジェクトにおいて、以下の点を改善に活かせる。

1. **Sub-agent化によるコンテキスト節約**: 現在のSkillsでトークン消費が多い処理をSub-agent化し、結果をファイル出力にすることで効率化できる
2. **maxTurns設定の追加**: 既存Skillsに `maxTurns` が未設定であれば追加を検討する
3. **Agent定義の分離**: 複数Skillsで共通する振る舞い（例: レポート生成）をAgent定義として切り出すことで再利用性を高められる

### 学習ヒント
Claude Codeの拡張機能は急速に進化しており、Skills/Agents/Hooks/MCPの4層構造を理解しておくことで、今後リリースされる新機能への対応力が上がる。特にHooksのイベント駆動モデル（`PreToolUse`/`PostToolUse`など）は、将来的にCI/CDパイプラインとの統合や、品質チェックの自動化に応用できる可能性がある。

---

## 関連リンク
- [Claude Code 公式ドキュメント - Skills](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Claude Code 公式ドキュメント - Agents](https://docs.anthropic.com/en/docs/claude-code/agents)
- [元記事: Claude Code 拡張機能の整理](https://zenn.dev/singularity/articles/2026-02-07-claude-code-extensibility-memo)
