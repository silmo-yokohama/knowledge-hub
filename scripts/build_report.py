#!/usr/bin/env python3
"""
マッチング評価結果をもとにレポートJSONを生成
"""
import json
import hashlib
from datetime import datetime

def gen_id(url):
    return hashlib.sha256(url.encode()).hexdigest()[:8]

# マッチング評価結果: (rank, category, summary, titleJa)
# 手動評価済みの記事リスト

articles = []

def add(rank, category, source, title, url, score, scoreLabel, summary, titleJa=None, subreddit=None):
    articles.append({
        "id": gen_id(url),
        "title": title,
        "titleJa": titleJa,
        "url": url,
        "category": category,
        "source": source,
        "score": score,
        "scoreLabel": scoreLabel,
        "subreddit": subreddit,
        "rank": rank,
        "summary": summary,
        "checked": False,
    })

# ===== S ランク: AI/LLM, フロントエンド, UI/UX =====

# --- はてなブックマーク ---
add("S", "AI/LLM", "hatena", "Claude16台で10万行のCコンパイラを作った論文を読んで、「いや答えあるじゃん」と思った話",
    "https://zenn.dev/shio_shoppaize/articles/shogun-spec-first", 291, "291 users",
    "AnthropicがClaude16台並列で10万行Cコンパイラを作った論文の解説と、仕様駆動開発への考察")

add("S", "AI/LLM", "hatena", "Google SRE が Gemini CLI を使用して実際の障害を解決している方法 | Google Cloud 公式ブログ",
    "https://cloud.google.com/blog/ja/topics/developers-practitioners/how-google-sres-use-gemini-cli-to-solve-real-world-outages/", 284, "284 users",
    "Google SREチームがGemini CLIを障害対応に活用した実例とトイル排除の取り組み")

add("S", "フロントエンド", "hatena", "Next.jsをVercelからCloudflareへ移行し、90%のコスト削減を実現した話 - Hello Tech",
    "https://tech.hello.ai/entry/vercel-cloudflare-migration", 133, "133 users",
    "Next.jsアプリをVercelからCloudflareに移行し月額コスト90%削減した背景と実装詳細")

add("S", "AI/LLM", "hatena", "Gemini × NotebookLM 連携で「自分専用エージェント」を量産する：蓄積した履歴を血肉化する究極の活用術",
    "https://zenn.dev/minipoisson/articles/2806b4a0865acb", 126, "126 users",
    "Gemini履歴をNotebookLMに集約し、4人の専門家エージェントとして毎日活用する手法")

add("S", "AI/LLM", "hatena", "DeNAがPerl6000行を1カ月でGo言語へ、特性異なるAIエージェント駆使",
    "https://xtech.nikkei.com/atcl/nxt/column/18/00001/11469/", 50, "50 users",
    "DeNAがAIエージェントを使いPerl6000行のAPIをGo言語に1カ月で移行した事例")

add("S", "AI/UX", "hatena", "AIエージェントのUXを進化させる「A2UI」でアプリを構築 - Taste of Tech Topics",
    "https://acro-engineer.hatenablog.com/entry/2026/02/10/120000", 44, "44 users",
    "AIエージェント向けUI設計「A2UI」の概念と実装方法の解説")

add("S", "AI/LLM", "hatena", "頭のいい人が「思考を整理したい」ときにChatGPTでやっている\u201c意外な使い方\u201d",
    "https://diamond.jp/articles/-/383511", 40, "40 users",
    "AIを思考整理ツールとして使う具体的な方法論、600社2万人に研修した専門家による解説")

add("S", "AI/LLM", "hatena", "AIは仕事を減らさず増やすことがテック企業を対象にした調査で明らかに",
    "https://gigazine.net/news/20260210-ai-changed-work-habits/", 39, "39 users",
    "ハーバード・ビジネス・レビューの調査でAIは仕事量を増やしていることが判明")

add("S", "AI/LLM", "hatena", "日本発のAI VTuber「しずく」開発元、米VC大手a16zから資金調達",
    "https://www.itmedia.co.jp/news/articles/2602/10/news075.html", 35, "35 users",
    "キャラクターAIスタートアップShizuku AIがa16zから日本関連初の投資を獲得")

add("S", "AI/LLM", "hatena", "VRAM96GB(Unified memory 128GB)でどのLLMが使えるか - きしだのHatena",
    "https://nowokay.hatenablog.com/entry/2026/02/10/162234", 31, "31 users",
    "VRAM96GB環境で使えるLLMの比較。gpt-oss-120b、GLM-4.6V、Qwen3-Coderの使い分け")

add("S", "AI/LLM", "hatena", "「コーディングは死ぬ」「AIはソフトウェアをディスラプトする」　生成AI革命の本当の価値",
    "https://atmarkit.itmedia.co.jp/ait/articles/2602/10/news022.html", 24, "24 users",
    "a16zマーティン・カサド氏が東京で講演、生成AIはインターネットと同レベルの変革と解説")

add("S", "AI/LLM", "hatena", "なぜAIによるエンジニア代替はうまくいかないのか？　\u201c効率化\u201dのはずが、現場で起きている逆転現象",
    "https://atmarkit.itmedia.co.jp/ait/articles/2602/10/news011.html", 24, "24 users",
    "AIがコード作成を効率化する一方、レビューや修正作業が増えベテランが疲弊している現状分析")

add("S", "AI/LLM", "hatena", "codex 5.3, opus 4.6, gemini 3.0 proの画像認識能力を比べた",
    "https://zenn.dev/simossyi/articles/f5ef8378959878", 17, "17 users",
    "3大AIモデルの画像認識能力を比較、Gemini 3.0 Proの描写が最も正確との結論")

add("S", "AI/LLM", "hatena", "ウェブ検索機能をオンにした状態で最も優れたAIですら約30％のケースで事実誤認の「ハルシネーション」を起こすと研究で判明",
    "https://gigazine.net/news/20260210-ai-hallucination-halluhard/", 15, "15 users",
    "EPFL等の研究チームが新ベンチマーク「HalluHard」でAIのハルシネーション率を測定")

add("S", "AI/LLM", "hatena", "AIで年間200冊のロマンス小説を執筆する作家がAI執筆について語る",
    "https://gigazine.net/news/20260210-chatbot-book/", 14, "14 users",
    "AIで年200冊を執筆する作家の実態。プロ作家の約1/3がAI利用を隠して執筆")

add("S", "AI/LLM", "hatena", "「Claude Code」の代替ツールを試す--ローカルで動作し、オープンソースかつ無料",
    "https://japan.zdnet.com/article/35243616/", 9, "9 users",
    "Claude Code代替としてGooseとQwen3-coderの組み合わせを検証した記事")

# --- Yahoo ニュース ---
add("S", "AI/LLM", "yahoo", "「ChatGPT」の広告機能、米国でテスト開始 ～無料と「Go」プランで掲出(窓の杜)",
    "https://news.yahoo.co.jp/articles/53aad468b802f92a64acebd903e06ec2b80063d5?source=rss", 0, "窓の杜",
    "OpenAIがChatGPTに広告を導入するテストを米国で開始。無料プランと最安プランが対象")

add("S", "AI/LLM", "yahoo", "日本政府、AIの社会実装を妨げている規制の情報を募集　制度見直しの参考に(ITmedia NEWS)",
    "https://news.yahoo.co.jp/articles/22381892da9295959bb556410e2b1bae13a67778?source=rss", 0, "ITmedia NEWS",
    "内閣府がAI社会実装の障害となる規制・制度の情報を募集開始")

add("S", "AI/LLM", "yahoo", "人材紹介業務、AIが丸ごと代行　カウンセリングや面接も(ITmedia NEWS)",
    "https://news.yahoo.co.jp/articles/332614855041657e8974ded7116d7dcded5f0329?source=rss", 0, "ITmedia NEWS",
    "PeopleXがAIエージェントで求職者のカウンセリングから面接まで代行するサービス開始")

add("S", "AI/LLM", "yahoo", "LINEヤフー、人事にAI本格活用　月1600時間以上の工数削減へ(ITmedia NEWS)",
    "https://news.yahoo.co.jp/articles/565b75cab51b9597e46989255111eb06685bf9a7?source=rss", 0, "ITmedia NEWS",
    "LINEヤフーが人事総務領域で生成AI活用を本格化。10件のAIツールで月1600時間削減")

add("S", "AI/LLM", "yahoo", "NTTグループは「AIがSI事業にもたらす影響」をどう見ている？(ITmedia エンタープライズ)",
    "https://news.yahoo.co.jp/articles/b168fe91da58f420dc078074e714921931edbd28?source=rss", 0, "ITmedia エンタープライズ",
    "NTTグループがAIのSI事業への影響について決算会見で言及した内容を分析")

# --- Reddit ---
add("S", "AI/LLM", "reddit", "Do not Let the Coder in Qwen3-Coder-Next Fool You! It's the Smartest, General Purpose Model of its Size",
    "https://old.reddit.com/r/LocalLLaMA/comments/1r0abpl/do_not_let_the_coder_in_qwen3codernext_fool_you/", 446, "446pt 148comments",
    "Qwen3-Coder-Nextはコーディング特化ではなく、同サイズ最高の汎用モデルとの評価",
    titleJa="Qwen3-Coder-Nextの「Coder」に騙されるな！同サイズ最高の汎用モデルだ", subreddit="r/LocalLLaMA")

add("S", "AI/LLM", "reddit", "Hugging Face Is Teasing Something Anthropic Related",
    "https://i.redd.it/wvu2vi2jwnig1.png", 359, "359pt 82comments",
    "Hugging FaceがAnthropic関連の何かを予告。オープンソース展開への期待が高まる",
    titleJa="Hugging FaceがAnthropic関連の何かを予告", subreddit="r/LocalLLaMA")

add("S", "AI/LLM", "reddit", "asked a vibe coder what they're building",
    "https://v.redd.it/kguop9ic6mig1", 290, "290pt 30comments",
    "バイブコーダー（AIでコードを書く人）が何を作っているかをインタビューした動画",
    titleJa="バイブコーダーに何を作っているか聞いてみた", subreddit="r/ClaudeAI")

add("S", "AI/LLM", "reddit", "Qwen-Image-2.0 is out - 7B unified gen+edit model with native 2K and actual text rendering",
    "https://qwen.ai/blog?id=qwen-image-2.0", 290, "290pt 61comments",
    "Qwen-Image-2.0リリース。7Bパラメータで画像生成・編集を統合、2K解像度対応",
    titleJa="Qwen-Image-2.0リリース — 7Bの統合画像生成・編集モデル", subreddit="r/LocalLLaMA")

add("S", "AI/LLM", "reddit", "I just delivered on a $30,000 contract thanks to Claude Code",
    "https://old.reddit.com/r/ClaudeAI/comments/1r0n1qz/i_just_delivered_on_a_30000_contract_thanks_to/", 216, "216pt 71comments",
    "Claude Codeを活用して3万ドルの契約を完遂した開発者の体験談",
    titleJa="Claude Codeのおかげで3万ドルの案件を納品できた", subreddit="r/ClaudeAI")

add("S", "AI/LLM", "reddit", "Head of AI safety research resigns after constitution update",
    "https://x.com/i/status/2020881722003583421", 159, "159pt 53comments",
    "AnthropicのAI安全性研究責任者がConstitution更新後に辞任。安全性方針に懸念か",
    titleJa="AI安全性研究責任者がConstitution更新後に辞任", subreddit="r/ClaudeAI")

add("S", "AI/LLM", "reddit", "You can use your Claude Pro subscription as an API endpoint — no extra API costs",
    "https://old.reddit.com/r/ClaudeAI/comments/1r0ugjm/you_can_use_your_claude_pro_subscription_as_an/", 130, "130pt 63comments",
    "Claude ProサブスクリプションをAPIエンドポイントとして使える方法の紹介",
    titleJa="Claude ProサブスクをAPIとして利用可能 — 追加API費用なし", subreddit="r/ClaudeAI")

add("S", "AI/LLM", "reddit", "A fully local home automation voice assistant using Qwen3 ASR, LLM and TTS on an RTX 5060 Ti",
    "https://v.redd.it/feropirhmkig1", 127, "127pt 21comments",
    "RTX 5060 Ti 16GB VRAMでQwen3のASR・LLM・TTSを動かす完全ローカル音声アシスタント",
    titleJa="Qwen3でRTX 5060 Ti上に完全ローカル音声アシスタントを構築", subreddit="r/LocalLLaMA")

add("S", "AI/LLM", "reddit", "Femtobot: A 10MB Rust Agent for Low-Resource Machines",
    "https://v.redd.it/nbv8vsnwwkig1", 105, "105pt 27comments",
    "10MBのRust製AIエージェント「Femtobot」。低リソースマシンでも動作可能",
    titleJa="Femtobot: 低リソースマシン向け10MBのRust製AIエージェント", subreddit="r/LocalLLaMA")

add("S", "AI/LLM", "reddit", "Step-3.5-Flash IS A BEAST",
    "https://old.reddit.com/r/LocalLLaMA/comments/1r0khh8/step35flash_is_a_beast/", 104, "104pt 43comments",
    "Step-3.5-Flashモデルの性能が非常に高いとの評価。コミュニティで注目を集める",
    titleJa="Step-3.5-Flashが驚異的な性能", subreddit="r/LocalLLaMA")

add("S", "AI/LLM", "reddit", "MechaEpstein-8000",
    "https://huggingface.co/ortegaalfredo/MechaEpstein-8000-GGUF", 622, "622pt 135comments",
    "Hugging Faceで公開された8Bパラメータの制限なしLLMモデル。議論を呼ぶ",
    titleJa="MechaEpstein-8000 — 制限なしの8BパラメータLLM", subreddit="r/LocalLLaMA")

add("S", "AI/LLM", "reddit", "Did anthropic just replace sonnet 4.5 with opus 4.5",
    "https://i.redd.it/7mz1eayopnig1.jpeg", 30, "30pt 13comments",
    "AnthropicがSonnet 4.5をOpus 4.5に差し替えたのではという議論",
    titleJa="AnthropicはSonnet 4.5をOpus 4.5に差し替えた？", subreddit="r/ClaudeAI")

add("S", "AI/LLM", "reddit", "Opus 4.6 Reasoning Distill 3k prompts",
    "https://old.reddit.com/r/LocalLLaMA/comments/1r0v0y1/opus_46_reasoning_distill_3k_prompts/", 26, "26pt 18comments",
    "Opus 4.6の推論能力を蒸留した3000プロンプトのデータセット公開",
    titleJa="Opus 4.6の推論蒸留用3000プロンプト", subreddit="r/LocalLLaMA")

add("S", "AI/LLM", "reddit", "I measured the personality of 6 open-source LLMs (7B-9B) by probing their hidden states.",
    "https://old.reddit.com/r/LocalLLaMA/comments/1r11zsa/i_measured_the_personality_of_6_opensource_llms/", 22, "22pt 6comments",
    "6つのOSS LLMの隠れ状態を探索し「性格」を測定した研究",
    titleJa="6つのOSS LLM（7B-9B）の「性格」を隠れ状態から測定", subreddit="r/LocalLLaMA")

add("S", "AI/LLM", "reddit", "We hid backdoors in binaries — Opus 4.6 found 49% of them",
    "https://quesma.com/blog/introducing-binaryaudit/", 14, "14pt 3comments",
    "バイナリにバックドアを仕込みOpus 4.6でテスト。49%を検出できたとの結果",
    titleJa="バイナリにバックドアを隠してテスト — Opus 4.6が49%検出", subreddit="r/ClaudeAI")

add("S", "フロントエンド", "reddit", "Exploring React Internals: How React Fixed Recursive Render Problems",
    "https://i.redd.it/ln6ek51iknig1.gif", 6, "6pt 4comments",
    "Reactの内部構造解説。再帰レンダリング問題をどう解決したか",
    titleJa="Reactの内部解説: 再帰レンダリング問題の解決方法", subreddit="r/webdev")

add("S", "フロントエンド", "reddit", "Is starting learning Nextjs in 2026 worth it?",
    "https://old.reddit.com/r/nextjs/comments/1r0voi6/is_starting_learning_nextjs_in_2026_worth_it/", 5, "5pt 17comments",
    "2026年にNext.jsを学び始めるべきかの議論。コミュニティの見解",
    titleJa="2026年にNext.jsを学び始める価値はあるか？", subreddit="r/nextjs")

add("S", "フロントエンド", "reddit", "Is this the most flexible open-source Toast API in Vue?",
    "https://v.redd.it/hxjx7tp4u2ig1", 60, "60pt 42comments",
    "Vue向けオープンソースToast APIの紹介。柔軟性の高さが評価される",
    titleJa="Vue最強のオープンソースToast API？", subreddit="r/vuejs")

add("S", "フロントエンド", "reddit", "tailwind v4 vs stylex",
    "https://old.reddit.com/r/nextjs/comments/1r0znqx/tailwind_v4_vs_stylex/", 0, "0pt 6comments",
    "Tailwind CSS v4とStyleXの比較議論。Next.jsプロジェクトでの選択指針",
    titleJa="Tailwind v4 vs StyleX", subreddit="r/nextjs")

add("S", "フロントエンド", "reddit", "Would you leave Vercel for a European alternative?",
    "https://old.reddit.com/r/nextjs/comments/1r0d1l6/would_you_leave_vercel_for_a_european_alternative/", 6, "6pt 15comments",
    "Vercelからヨーロッパ代替サービスへの移行を検討する議論",
    titleJa="Vercelからヨーロッパの代替サービスに移行する？", subreddit="r/nextjs")

add("S", "フロントエンド", "reddit", "How to implement a Service Worker update notification in Vue 3 SPA?",
    "https://old.reddit.com/r/vuejs/comments/1qzerx4/how_to_implement_a_service_worker_update/", 10, "10pt 3comments",
    "Vue 3 SPAでService Worker更新通知を実装する方法の議論",
    titleJa="Vue 3 SPAでService Worker更新通知を実装するには？", subreddit="r/vuejs")

# ===== A ランク: DevOps, Cloud, Go, Python, セキュリティ, 設計 =====

add("A", "設計", "hatena", "ログ設計ガイドラインを公開しました | フューチャー技術ブログ",
    "https://future-architect.github.io/articles/20260210a/", 19, "19 users",
    "フューチャー社内有志によるログ設計ガイドラインの公開。システム運用の品質向上に貢献")

add("A", "セキュリティ", "hatena", "Windowsのイベントログ分析トレーニング用コンテンツの公開 - JPCERT/CC Eyes",
    "https://blogs.jpcert.or.jp/ja/2026/02/windows-1.html", 40, "40 users",
    "JPCERT/CCが標的型攻撃調査のためのWindowsイベントログ分析トレーニング資料を公開")

add("A", "セキュリティ", "hatena", "そのバックアップでは会社を守れない　「3-2-1ルール」を過去にする\u201c新常識\u201d",
    "https://techtarget.itmedia.co.jp/tt/news/2602/09/news03.html", 23, "23 users",
    "従来の「3-2-1バックアップルール」の限界と、新しいバックアップ戦略の提案")

add("A", "AWS", "hatena", "AWS ElastiCache for Redis を Valkey へ移行した話 - freee Developers Hub",
    "https://developers.freee.co.jp/entry/aws-elasticache-for-valkey-migration", 22, "22 users",
    "freeeが約50クラスターのElastiCache for RedisをValkeyエンジンへ移行した事例")

add("A", "開発ツール", "hatena", "zellijからtmuxに戻した - ちなみに",
    "https://blog.nishimu.land/entry/2026/02/10/001806", 15, "15 users",
    "Rust製ターミナルマルチプレクサzellijを11ヶ月使った後tmuxに戻した理由と比較")

add("A", "フロントエンド", "yahoo", "React/Nest.js/Auth0/Docker/Terraformを使ったWebアプリ開発の実践ガイドが発売(窓の杜)",
    "https://news.yahoo.co.jp/articles/4b6bd870985c363e326284da634bb479cb908c37?source=rss", 0, "窓の杜",
    "React+Nest.js+Auth0+AWS/Azureデプロイまでカバーする実践ガイド書籍が発売")

add("A", "DevOps", "reddit", "Localstack will require an account to use starting in March 2026",
    "https://blog.localstack.cloud/the-road-ahead-for-localstack/#why-were-making-a-change", 68, "68pt 27comments",
    "AWS開発のローカルエミュレータLocalstackが3月からアカウント必須に",
    titleJa="Localstackが2026年3月からアカウント必須に", subreddit="r/programming")

add("A", "設計", "reddit", "What Functional Programmers Get Wrong About Systems",
    "https://www.iankduncan.com/engineering/2026-02-09-what-functional-programmers-get-wrong-about-systems/", 72, "72pt 27comments",
    "関数型プログラマーがシステム設計で犯しがちな間違いについての考察",
    titleJa="関数型プログラマーがシステムについて間違えていること", subreddit="r/programming")

add("A", "設計", "reddit", "Spec-driven development doesn't work if you're too confused to write the spec",
    "https://publish.obsidian.md/deontologician/Posts/Spec-driven+development+doesn't+work+if+you're+too+confused+to+write+the+spec", 57, "57pt 12comments",
    "仕様が書けないほど混乱している場合、仕様駆動開発は機能しないという主張",
    titleJa="仕様を書けないほど混乱しているなら、仕様駆動開発は機能しない", subreddit="r/programming")

add("A", "Python", "reddit", "Making Pyrefly's Diagnostics 18x Faster",
    "https://pyrefly.org/blog/2026/02/06/performance-improvements/", 7, "7pt 0comments",
    "Python型チェッカーPyreflyの診断速度を18倍高速化した取り組み",
    titleJa="Pyreflyの診断を18倍高速化した方法", subreddit="r/programming")

add("A", "Python", "reddit", "Python's Dynamic Typing Problem",
    "https://www.whileforloop.com/en/blog/2026/02/10/python-dynamic-typing-problem/", 2, "2pt 18comments",
    "Pythonの動的型付けが引き起こす問題点についての分析",
    titleJa="Pythonの動的型付けの問題", subreddit="r/programming")

# ===== B ランク: 個人開発, キャリア, ゲーム, Vue.js周辺 =====

add("B", "Web開発", "reddit", "I just implemented social auth in my app. Rate my oauth.",
    "https://i.redd.it/bc93qdgi4hig1.png", 549, "549pt 106comments",
    "自作アプリにソーシャルログインを実装した結果の共有とフィードバック",
    titleJa="自分のアプリにソーシャル認証を実装した。評価してくれ", subreddit="r/webdev")

add("B", "ゲーム", "reddit", "Fluorite, Toyota's Upcoming Brand New Game Engine in Flutter",
    "https://fosdem.org/2026/schedule/event/7ZJJWW-fluorite-game-engine-flutter/", 382, "382pt 83comments",
    "トヨタがFlutterベースの新ゲームエンジン「Fluorite」を開発中",
    titleJa="Fluorite — トヨタがFlutterで新ゲームエンジンを開発中", subreddit="r/programming")

add("B", "プログラミング", "reddit", "Atari 2600 Raiders of the Lost Ark source code completely disassembled and reverse engineered",
    "https://github.com/joshuanwalker/Raiders2600/", 586, "586pt 69comments",
    "Atari 2600版『レイダース/失われたアーク』のソースコードを完全逆アセンブル",
    titleJa="Atari 2600版レイダースのソースコードを完全リバースエンジニアリング", subreddit="r/programming")

add("B", "個人開発", "reddit", "Jmail was developed in five hours",
    "https://old.reddit.com/r/webdev/comments/1r0lhwu/jmail_was_developed_in_five_hours/", 274, "274pt 79comments",
    "メールクライアント「Jmail」を5時間で開発したという投稿",
    titleJa="Jmailは5時間で開発された", subreddit="r/webdev")

add("B", "キャリア", "reddit", "Constant Breakdowns as a Junior Dev",
    "https://old.reddit.com/r/webdev/comments/1r0nh0c/constant_breakdowns_as_a_junior_dev/", 154, "154pt 62comments",
    "ジュニア開発者としての精神的苦労と挫折についての赤裸々な告白",
    titleJa="ジュニア開発者としての度重なる挫折", subreddit="r/webdev")

add("B", "組織/キャリア", "hatena", "オープニング研修で「職場において、機嫌を態度で表現する権利はありません」と言ったら良い人だけ残った話",
    "https://togetter.com/li/2662066", 208, "208 users",
    "「機嫌を態度で表現する権利はない」と研修で伝えたところ良い人材だけが残った話")

add("B", "キャリア", "reddit", "Large tech companies don't need heroes",
    "https://www.seangoedecke.com/heroism/", 29, "29pt 5comments",
    "大手テック企業にヒーローは不要という組織論",
    titleJa="大手テック企業にヒーローは不要", subreddit="r/programming")

add("B", "Web開発", "reddit", "spent 30 min planning and avoided a week of refactoring",
    "https://old.reddit.com/r/webdev/comments/1r0qlov/spent_30_min_planning_and_avoided_a_week_of/", 30, "30pt 21comments",
    "30分の計画で1週間のリファクタリングを回避した経験談",
    titleJa="30分の計画で1週間のリファクタリングを回避", subreddit="r/webdev")

add("B", "個人開発", "reddit", "I built Soundle. Like Wordle but you guess sounds instead of words",
    "https://old.reddit.com/r/vuejs/comments/1r0p3i0/i_built_soundle_like_wordle_but_you_guess_sounds/", 15, "15pt 6comments",
    "Vueで作られた音当てゲーム「Soundle」の紹介",
    titleJa="Soundleを作った。Wordleの音版", subreddit="r/vuejs")

add("B", "Web開発", "reddit", "PWAs in real projects, worth it?",
    "https://old.reddit.com/r/webdev/comments/1r0z6g9/pwas_in_real_projects_worth_it/", 4, "4pt 37comments",
    "実プロジェクトでPWAを採用する価値についての議論",
    titleJa="実プロジェクトでPWAは価値がある？", subreddit="r/webdev")

add("B", "フロントエンド", "reddit", "Vue3 Date/time picker component",
    "https://old.reddit.com/r/vuejs/comments/1qzdt2z/vue3_datetime_picker_component/", 4, "4pt 19comments",
    "Vue3用の日付/時刻ピッカーコンポーネントの推薦と議論",
    titleJa="Vue3の日付/時刻ピッカーコンポーネント", subreddit="r/vuejs")

add("B", "フロントエンド", "reddit", "Early showcase: Framework-agnostic interactive video library with quizzes & smart rewind",
    "https://github.com/parevo/interactive-video", 8, "8pt 0comments",
    "React・Vue・バニラJS対応のインタラクティブ動画ライブラリのプレビュー公開",
    titleJa="React/Vue対応のインタラクティブ動画ライブラリ初公開", subreddit="r/vuejs")

add("B", "フロントエンド", "reddit", "Shadcn code is different depending on how it's installed",
    "/r/shadcn/comments/1r0ut5u/shadcn_code_is_different_depending_on_how_its/", 3, "3pt 3comments",
    "shadcnのインストール方法によって生成されるコードが異なる問題の報告",
    titleJa="shadcnはインストール方法によって生成コードが異なる", subreddit="r/nextjs")

add("B", "フロントエンド", "reddit", "NextJS Authentication with Supabase Auth (Google, GitHub, Facebook and Protected Routes)",
    "https://youtu.be/I7slTmDKuj8", 3, "3pt 1comments",
    "Next.jsでSupabase Authを使った認証実装チュートリアル",
    titleJa="Next.js + Supabase Auth認証チュートリアル", subreddit="r/nextjs")

# ===== C ランク: 政治, 経済, スポーツ =====

add("C", "政治", "hatena", "衆院選 1200万人以上が中道に投票、7議席（小選挙区）",
    "https://anond.hatelabo.jp/20260209214223", 532, "532 users",
    "衆院選の死票を分析。中道に1200万票集まるも小選挙区では7議席に留まった")

add("C", "政治", "hatena", "「リベラルの若者」が自民党に投票する構造｜女子大生起業家",
    "https://note.com/seanky/n/n105e4166a784", 459, "459 users",
    "若者はリベラルな価値観を持ちつつも自民党を選ぶ構造を分析した記事")

add("C", "政治", "hatena", "中道が大敗した理由を心理学的に解説する",
    "https://anond.hatelabo.jp/20260209191143", 456, "456 users",
    "心理学の用語を使って中道改革連合が大敗した理由を解説")

add("C", "政治", "hatena", "【衆院選2026】自民圧勝の夜、東浩紀・ゲンロンカフェ『あの夜2』で「リベラルの自殺」を目撃した",
    "https://note.com/bright_wasp5197/n/na8014b3cc1db", 418, "418 users",
    "衆院選開票特番で東浩紀が語った「リベラルの自殺」の意味")

add("C", "政治", "hatena", "「チームみらいは誰の声を聞いているのか——オードリー・タンとの分岐点」という記事の誤情報について",
    "https://note.com/nishiohirokazu/n/n58b6f250d298", 422, "422 users",
    "チームみらいとTalk to the Cityに関する記事の技術的誤りを専門家が指摘")

add("C", "政治", "hatena", "総選挙の結果について ｜ 日本共産党",
    "https://www.jcp.or.jp/web_policy/17280.html", 298, "298 users",
    "日本共産党が衆院選の結果（改選8→4議席）を総括した声明")

add("C", "政治", "hatena", "2026年総選挙、左派は国民を\u201cバカにしない\u201dから負けた",
    "https://note.com/moyamoyamic/n/n7345923c40c3", 289, "289 users",
    "リベラルが毎回国民の判断力を過大評価して負けるパターンを分析")

add("C", "政治", "hatena", "日本 NATOのウクライナ支援の枠組みに参加の方針固める",
    "https://news.web.nhk.newsweb/na/na-k10015047881000", 181, "181 users",
    "日本がNATOのウクライナ支援枠組みに参加する方針を固めた速報")

add("C", "経済", "yahoo", "オルカン、純資産総額が10兆円突破(Impress Watch)",
    "https://news.yahoo.co.jp/articles/87feef6f6d0c93bd4b71c43ba0b8d445073da1c3?source=rss", 0, "Impress Watch",
    "eMAXIS Slim全世界株式（オルカン）の純資産総額が10兆円を突破")

add("C", "経済", "yahoo", "楽天G、減損損失約305億円  楽天シンフォニーの事業立ち上げ遅れなど影響(ケータイ Watch)",
    "https://news.yahoo.co.jp/articles/761dcc2f9702b5654fa05a56e7ac40fff1948f22?source=rss", 0, "ケータイ Watch",
    "楽天グループが楽天シンフォニーの事業遅れで約305億円の減損損失を計上")

add("C", "スポーツ", "yahoo", "【ソフトバンク】30歳の誕生日を迎えた周東佑京　WBCに臨む覚悟(スポーツ報知)",
    "https://news.yahoo.co.jp/articles/de46226fc8f7b81e1817b440f69b1ba6b7c527e5?source=rss", 0, "スポーツ報知",
    "ソフトバンク周東佑京がWBCに向けた意気込みを語る")

add("C", "スポーツ", "yahoo", "フィギュアで衝撃「禁止技じゃないの？」かつては減点対象、解禁された大技(THE ANSWER)",
    "https://news.yahoo.co.jp/articles/ae313eb1afac1c50be253b5f338085412e5cf5a1?source=rss", 0, "THE ANSWER",
    "ミラノ五輪でマリニンがバックフリップを披露。かつての禁止技が解禁された経緯")

add("C", "スポーツ", "yahoo", "【五輪】スノーボード　１６歳清水さら「全く緊張していない」冬季五輪日本女子最年少メダルへ(スポーツ報知)",
    "https://news.yahoo.co.jp/articles/3bebb6ebbd05961714fdccdad5a6038c0ac7c7bb?source=rss", 0, "スポーツ報知",
    "16歳の清水さらがミラノ五輪スノーボードHP予選に臨む。日本女子最年少メダルを目指す")

add("C", "テック規制", "yahoo", "EU、TikTokの無限スクロールは「違法」の見解　\u201c中毒デザイン\u201dにメス(Impress Watch)",
    "https://news.yahoo.co.jp/articles/128286814bf369d289948df0fe224ef4b15ec15c?source=rss", 0, "Impress Watch",
    "欧州委員会がTikTokの中毒性あるデザインがDSA違反との判断を下す")

# ===== トレンド分析 =====
# 記事を出力した後にトレンド分析を生成

# --- JSON出力 ---
# ランク順ソート: S → A → B → C、同ランク内はスコア降順
rank_order = {"S": 0, "A": 1, "B": 2, "C": 3}
articles.sort(key=lambda a: (rank_order[a["rank"]], -a["score"]))

# サマリー集計
summary = {"total": len(articles), "S": 0, "A": 0, "B": 0, "C": 0}
for a in articles:
    summary[a["rank"]] += 1

# トレンド分析
trend_analysis = [
    {
        "topic": "AIと仕事の関係性を問い直す議論",
        "description": "AIがエンジニアの仕事を奪うのではなく、逆に仕事量を増やしているという調査結果や、AIによるエンジニア代替がうまくいかない理由など、AI導入の現実と理想のギャップに焦点を当てた記事が複数登場。開発現場の変容が注目を集めている。",
        "relatedArticleIds": [gen_id(u) for u in [
            "https://gigazine.net/news/20260210-ai-changed-work-habits/",
            "https://atmarkit.itmedia.co.jp/ait/articles/2602/10/news011.html",
            "https://atmarkit.itmedia.co.jp/ait/articles/2602/10/news022.html",
            "https://old.reddit.com/r/ClaudeAI/comments/1r0n1qz/i_just_delivered_on_a_30000_contract_thanks_to/",
        ]]
    },
    {
        "topic": "Opus 4.6の能力が話題の中心に",
        "description": "Opus 4.6のバイナリ監査能力、推論蒸留データセット、Sonnet 4.5との差し替え疑惑など、Anthropicの最新モデルに関する話題がReddit上で多角的に議論されている。AI安全性研究責任者の辞任も波紋を広げている。",
        "relatedArticleIds": [gen_id(u) for u in [
            "https://quesma.com/blog/introducing-binaryaudit/",
            "https://old.reddit.com/r/LocalLLaMA/comments/1r0v0y1/opus_46_reasoning_distill_3k_prompts/",
            "https://i.redd.it/7mz1eayopnig1.jpeg",
            "https://x.com/i/status/2020881722003583421",
            "https://zenn.dev/simossyi/articles/f5ef8378959878",
        ]]
    },
    {
        "topic": "ローカルLLM・OSSモデルの競争激化",
        "description": "Qwen3-Coder-Nextの汎用性能、Qwen-Image-2.0の画像生成、Step-3.5-Flash、Hugging FaceのAnthropic関連予告など、オープンソースLLMの進化が加速。ローカル実行可能なAIエージェントの開発も活発化している。",
        "relatedArticleIds": [gen_id(u) for u in [
            "https://old.reddit.com/r/LocalLLaMA/comments/1r0abpl/do_not_let_the_coder_in_qwen3codernext_fool_you/",
            "https://qwen.ai/blog?id=qwen-image-2.0",
            "https://old.reddit.com/r/LocalLLaMA/comments/1r0khh8/step35flash_is_a_beast/",
            "https://i.redd.it/wvu2vi2jwnig1.png",
            "https://v.redd.it/feropirhmkig1",
            "https://v.redd.it/nbv8vsnwwkig1",
            "https://nowokay.hatenablog.com/entry/2026/02/10/162234",
        ]]
    },
    {
        "topic": "2026年衆院選の結果分析が活発",
        "description": "自民圧勝・中道大敗の衆院選結果を受け、はてブで死票分析、心理学的考察、リベラル敗北の構造分析など多角的な議論が展開。1200万票が7議席になった小選挙区制の問題も浮き彫りに。",
        "relatedArticleIds": [gen_id(u) for u in [
            "https://anond.hatelabo.jp/20260209214223",
            "https://note.com/seanky/n/n105e4166a784",
            "https://anond.hatelabo.jp/20260209191143",
            "https://note.com/bright_wasp5197/n/na8014b3cc1db",
        ]]
    },
    {
        "topic": "Next.js/Vercelエコシステムの変化",
        "description": "VercelからCloudflareへの移行で90%コスト削減した事例や、Vercelの欧州代替サービスの議論、Tailwind v4 vs StyleXの比較など、Next.jsホスティング・スタイリング周りのエコシステムが変化の兆しを見せている。",
        "relatedArticleIds": [gen_id(u) for u in [
            "https://tech.hello.ai/entry/vercel-cloudflare-migration",
            "https://old.reddit.com/r/nextjs/comments/1r0d1l6/would_you_leave_vercel_for_a_european_alternative/",
            "https://old.reddit.com/r/nextjs/comments/1r0znqx/tailwind_v4_vs_stylex/",
            "https://old.reddit.com/r/nextjs/comments/1r0voi6/is_starting_learning_nextjs_in_2026_worth_it/",
        ]]
    },
]

report = {
    "date": "2026-02-11",
    "generatedAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    "dataSources": ["はてなブックマーク", "Yahoo ニュース", "Reddit"],
    "summary": summary,
    "articles": articles,
    "trendAnalysis": trend_analysis,
}

# JSON出力
print(json.dumps(report, ensure_ascii=False, indent=2))

