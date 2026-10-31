> プラグイン版 0.1.1 preview: [インストール・更新 (English)](docs/plugin-guide.md) · [한국어 안내](docs/plugin-guide.ko.md)。[MIT ライセンス](LICENSE)。公式ディレクトリには未掲載です。

# Evidence-First：日本語クイックスタート

[한국어](README.md) · [English](README.en.md) · 日本語 · [中文](README.zh.md)

共有する原典記録（L1）と意味モデル（L2）を利用し、個人・部門・AIの解釈を独立して保持するスキルです。検証はリスクに比例させ、出典を追跡し、判断と実行権限を区別します。AIは外部の利用者であり、オントロジーの必須要素ではありません。

1. [インストール手順（英語）](docs/evidence-first-installation.en.md)に従い、skills/evidence-first フォルダー全体をコピーします。
2. 「Evidence-First を使い、日本語で回答してください」とAIに依頼します。標準の [SKILL.md](skills/evidence-first/SKILL.md) は英語ですが、回答言語を英語に限定しません。
3. 保存方法（なし・Wiki・SQLite・グラフDB・組合せ）と機能（基本検索・関係探索・RAG）を別々に選びます。必要になった時点で追加・移行できます。
4. 既存の権限内で必要な改善を提案・実行・検証し、十分に機能する方法は維持します。

```sh
python "PATH_TO_SKILL/scripts/workspace.py" --root "PROJECT" --lang ja init --mode wiki
python "PATH_TO_SKILL/scripts/workspace.py" --root "PROJECT" enable rag
python "PATH_TO_SKILL/scripts/rag.py" --root "PROJECT" build
python "PATH_TO_SKILL/scripts/rag.py" --root "PROJECT" --lang ja retrieve --question "冷却原因は確認されましたか？" --search-query "cooling cause"
```

PATH_TO_SKILL と PROJECT は実際のパスに置き換えます。最後の検索例は英語の資料に対する検索語の例です。RAGは登録された記録を検索するため、実際の利用では許可された資料を登録してください。

Wikiの見出し・RAG生成規則には日本語カタログがあります。CLIのオプション・JSONキー・技術的エラーは英語を維持します。AIはそれらを日本語で説明できます。[言語対応の範囲](skills/evidence-first/references/languages.md)と[架空の英語サンプル](skills/evidence-first/examples/README.en.md)を参照してください。

原文・ID・information_type・verification_status・権限は翻訳で変更しません。翻訳説明を原典や検証済み事実と混同しないでください。日本語の全参照文書が校閲済みという意味ではありません。英語・韓国語の維持された手順を参照して説明できます。
