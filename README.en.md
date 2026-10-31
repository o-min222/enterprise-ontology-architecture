# Evidence-First enterprise ontology architecture

[한국어](README.md) · English · [日本語](README.ja.md) · [中文](README.zh.md)

Shared L1 source records and L2 semantic definitions, independent interpretations, proportionate verification, provenance, and separate execution authority. AI is an external L3 consumer; the ontology does not require AI.

## Use the skill

- [Standard SKILL.md](skills/evidence-first/SKILL.md): one portable evidence-first skill; answer in the user's language.
- [Install and connect](docs/evidence-first-installation.en.md): Codex/Claude Code paths, AGENTS.md/CLAUDE.md integration, pinned versions, updates.
- [Multilingual support](skills/evidence-first/references/languages.md): message catalogs, language fallback, translation boundaries, cross-language retrieval.
- [English synthetic examples](skills/evidence-first/examples/README.en.md) and [tests](tests/README.en.md).

Copy the entire skills/evidence-first folder, not just SKILL.md. The skill does not grant data access or enforce security. Do not publish private data or credentials.

## Choose independently, extend later

Storage: none, file Wiki, SQLite, Oxigraph RDF graph DB, or combinations. Features: basic lookup, graph relationship lookup, RAG. Select one primary store. RAG works over Wiki/SQLite/graph and is not a storage type or maturity stage.

[Setup and migration](skills/evidence-first/references/workspace-lifecycle.en.md) support read-only plans, complete-record comparison, primary switching, and retained originals. [Graph/RAG](skills/evidence-first/references/graph-and-rag.en.md) provide a real local RDF DB and lexical search/cited context for the calling AI's generation. Remote DB adapters, vector embeddings, model APIs, synchronization, and scheduling are separate implementation scope.

All five information types—observation, hypothesis, reviewed_assessment, official_decision, execution_result—allow all four statuses—unverified, in_review, verified, disputed. Checking decision existence does not prove correctness or grant execution rights.

## Initiative and efficiency

[Adaptation](skills/evidence-first/references/adaptive-environment.en.md): observe actual need, compare alternatives, propose a concrete change, execute inside existing authority, then verify outcomes. Default task_scoped uses current task permission. Optional propose_only/scoped_auto preferences remain separate from real access controls.

[Efficient work](skills/evidence-first/references/efficient-work.en.md): preserve quality/provenance/permission while comparing total setup, execution, review, and maintenance burden. Start small, keep the current method when sufficient, and reuse conditional local experience without treating it as universal truth or model training.

## Languages

English and Korean core operating guides are authored in this repository. Japanese and Simplified Chinese have quickstarts and tool catalogs. The AI may explain and answer in another requested language using a maintained guide, while clearly distinguishing source text, translation, and unsupported/reviewed localization. Tool labels and RAG generation rules support en/ko/ja/zh; technical CLI diagnostics remain English. Valid unsupported tags use an explicit English-message fallback.

Use --lang before the command. It changes presentation, not records, IDs, permissions, or primary storage:

```sh
python "PATH_TO_SKILL/scripts/workspace.py" --root "PROJECT" --lang en init --mode wiki
python "PATH_TO_SKILL/scripts/rag.py" --root "PROJECT" --lang ja retrieve --question "冷却原因は確認されましたか？" --search-query "cooling cause"
```

Local retrieval is lexical. Source-language keywords may be prepared by the calling AI; the helper retains the original question and reports rewrites. A new index format adds basic CJK bigrams; rebuild older indexes. No automatic external translation is performed.

## Architecture and existing prompts

The original Korean architecture docs and prompts remain intact. The [English architecture overview](docs/architecture.en.md) describes L1/L2/L3, governance, incremental implementation, and claim limits. [English implementation prompts](prompts/README.en.md) support Wiki, PostgreSQL design, and validation. The project is platform-independent guidance, not a replacement enterprise data platform.
