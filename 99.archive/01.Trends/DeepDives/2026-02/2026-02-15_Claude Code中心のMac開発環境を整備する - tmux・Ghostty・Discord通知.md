# Claude Code中心のMac開発環境を整備する - tmux・Ghostty・Discord通知

> 元記事: [Claude Code中心のMac開発環境を整備する - tmux・Ghostty・Discord通知](https://nyosegawa.github.io/posts/claude-code-mac-dev-environment/)
> 分析日: 2026-02-15
> ソース: はてブ
> ブックマーク数: 266 users

---

## 記事の要約

- Claude Codeを中心に据えたMac開発環境として、tmux・Ghostty・Discord通知の3つのコンポーネントを整備した実践記事
- 「1プロジェクト = 1ウィンドウ = 4ペイン固定」のtmux管理スクリプト（dev-tmux）を自作し、Claude Code専用のレイアウトを構築
- Ghostty（ターミナルエミュレータ）+ Starship（プロンプト）の組み合わせで、情報量を最小限に絞った視認性の高いターミナル環境を実現
- Claude Code Hooksを活用し、返信完了時や権限確認時にDiscordへ自動通知する仕組みを構築
- すべての設定ファイルがdotfilesリポジトリで公開されている

---

## 詳細の深掘り

### dev-tmux: 4ペイン固定レイアウト

著者が自作したtmux管理スクリプトで、以下の固定レイアウトを提供する:

- **ペイン1（左上・最大）**: Claude Code — メインの作業スペース
- **ペイン2（左下）**: git操作・自由ターミナル — 手動操作用
- **ペイン3・4（右側）**: サーバー・フロントエンドプロセス — 開発サーバーやビルドプロセスの監視用

Option+Rでサーバーの起動/再起動が可能で、Claude Codeが依存パッケージを更新した後もワンキーで再起動できる。「Claude Codeに任せつつ、必要な情報は常に見える」という設計思想がある。

### Ghostty + Starship によるターミナル環境

Ghosttyの設定で `macos-option-as-alt = true` が重要なポイント。これによりOptionキーがAlt/Metaとして機能し、tmuxのキーバインドと干渉しない。Starshipはディレクトリ、Gitブランチ、時刻の3つに情報を絞り、Claude Codeの出力を邪魔しない最小限のプロンプトを実現している。

### Claude Code Hooks → Discord通知

Claude Code Hooksを利用して、以下のイベント時にDiscordへ自動通知を送信する:

- **返信完了時**: Claude Codeの応答が完了したことを通知
- **権限確認時**: ファイル変更やコマンド実行の承認が必要な場合に通知

Pythonスクリプトが会話ログから直近のやり取りを抽出し、色分けされたメッセージで状態を伝える。これにより、Claude Codeにタスクを任せている間に別の作業をしていても、進捗を見逃さない仕組みになっている。

---

## キーポイント

- Claude Codeを「常に開いておくメイン画面」と位置づけ、開発環境全体をそれに最適化するアプローチ
- tmuxの固定レイアウトにより、プロジェクトごとに一貫した作業スペースが確保される
- Hooksによる通知は、AIに作業を委任する時代の「監督」のあり方を示している
- dotfilesとして公開されており、すぐに自分の環境に取り入れられる

---

## あなたへの関連性

### 実務への応用

現在もClaude Codeを日常的に使っている立場として、この環境構成はすぐに参考にできる:

- **tmuxの4ペインレイアウト**: 複数プロジェクトを同時に進めるフリーランス業務で、プロジェクトごとにワークスペースを分離できる。Next.js/Nuxtの開発サーバーを右ペインで常時監視する構成は実用的
- **Discord通知**: Claude Codeに長時間タスク（大規模リファクタリング等）を任せている間の監視手段として有用。Slackや他のチャットツールへの応用も考えられる
- **Option+Rでサーバー再起動**: Claude Codeがpackage.jsonを変更した後の再起動を自動化するのは、開発フローの小さなストレスを解消できる

### 学習ヒント

- **Claude Code Hooks**: Hooksの実装方法の参考事例として、通知以外の用途（ログ記録、自動テスト実行等）への応用を検討できる
- **tmux**: 普段あまりtmuxを使っていない場合、このようなClaude Code特化の使い方から入ると学習のモチベーションになる
- **dotfiles管理**: 設定ファイルをGitで管理する習慣は、開発環境の再現性を高めるDevOps的な考え方の入り口になる

---

## 関連リンク

- [nyosegawa/dotfiles（設定ファイル一式）](https://github.com/nyosegawa/dotfiles)
