# Validation scope and evidence

[한국어 historical record](validation-report.md)

The pre-multilingual baseline is commit `48709dd06f0e5c0a2e4c2d1e3cba26a795fd6e4d`. Its 39 automated checks and isolated behavioral runs covered lossless local migration, real Oxigraph/SPARQL, local lexical RAG, stale-index refusal, execution boundaries, proactive adaptation, and bounded efficiency comparison/reuse. See the retained historical report for environment-specific observations; they are not universal performance or model-compliance guarantees.

## Multilingual implementation

- One standard English SKILL.md and executable implementation; retained Korean SKILL.ko.md and maintenance instructions.
- English/Korean core guides and English synthetic ledger/source material. Japanese/Simplified Chinese quickstarts; four UTF-8 tool catalogs.
- User-requested AI language independent of tool message fallback. Stable keys, IDs, enums, permission, stored originals, and primary-store semantics.
- Explicit original and rewritten retrieval queries. Basic CJK bigrams in index format 2; old format requires rebuild. Language-only changes reuse a current index.

All **47 automated tests passed**, including eight dedicated multilingual checks: catalog completeness/fallback, invalid tags without side effects, English fixture schema/identity/source links, localized migration with complete payload preservation, cross-language questions with explicit source keywords, basic CJK lexical hits, old-index refusal/rebuild, and installed UTF-8 CLI use without test packages. Existing checks cover regression, all repository-language links, one standard skill identity, and package independence. The skill-creator validator and whitespace checks also passed.

## Independent installed-copy walkthrough

An evaluating AI read the English skill/installation guides, not expected answers/tests/Korean versions, and installed a fresh skill copy in an isolated project's .agents/skills/evidence-first directory. It used Python 3.14.4, SQLite 3.50.4, and the existing local test environment.

1. Registered and schema-checked the five English fictional records in SQLite, copied their English source fixture to project root, and previewed/applied migration to Wiki with --lang ja. Japanese labels were observed; every JSON field/value matched DB and Wiki.
2. Enabled/built RAG format 2. A Japanese question used an explicitly prepared English search_query, retained the original Japanese question, and returned requested/message language ja/ja. The actual Japanese answer cited HYP-DEMO-1 and its original, retained hypothesis/unverified, and did not assert a proven cooling cause.
3. A Spanish question used restart decision keywords with requested/message language es/en. The CLI explicitly reported the English-message fallback. The actual answer remained Spanish, cited both decision originals, retained official_decision/disputed and current-applicability scope, and distinguished decision existence from safety.
4. The evaluator separately read the needed original passages. Across response-language changes, config, index, Wiki JSON, Wiki page, existing DB, and original source file were all byte-identical. No language-only rebuild occurred. Unrelated retrieved evidence was excluded from the answer.

No functional defect or instruction conflict was observed in that scope. The original ten architecture/prompt files remain unchanged; Korean skill/maintenance content was retained in .ko.md variants. These two response-language trials over English synthetic material do not establish universal translation quality or cross-language recall.

## Limits

Authored support is tiered: English/Korean core guides, Japanese/Simplified Chinese quickstarts and messages, and on-demand AI explanation for other languages. Technical CLI diagnostics stay English. A valid unsupported tag uses an explicit English-message fallback. This is not a claim that all documents/regions/languages have reviewed translations.

The helper does not automatically translate originals or perform multilingual semantic embedding search. The AI may explicitly rewrite source-language keywords while retaining the original question. Review consequential terminology and source passages independently. Source-language mismatch can cause missed retrieval and does not prove missing events.

The new language behavior is guidance plus local presentation/retrieval support, not added access rights, permission enforcement, model training, external translation, or a multi-user service. Actual product skill-discovery, remote model/DB integration, human professional translation review, and universal language/recall guarantees remain outside this local verification scope.

## Plugin preview 0.1.0

On 2026-10-31, all 55 automated tests passed locally on Windows/Python 3.14.4. Eight new distribution tests exercise temporary Git indexes, copied skills, ZIP determinism/integrity, and refusal/exclusion of unreviewed/runtime paths. Root local-link checks now include contribution/privacy/security/support docs. Both skills passed the skill-creator frontmatter validator. Root plugin.json passed validation against the live declared Agent Plugins 1.0.0 schema.

Claude Code 2.1.220 passed native plugin validation with one expected advisory: preserved root CLAUDE.md is project context and is not automatically loaded as plugin context. Strict plugin validation therefore reports that advisory as a failure; it is not represented here as a strict pass. The marketplace passed strict validation. `claude --plugin-dir . plugin details evidence-first` actually discovered version 0.1.0 and two skills (`evidence-first`, `evidence-first-setup`), with no agents/hooks/MCP/LSP components. This is local loader verification, not installation into a user's global settings. Codex CLI 0.144.3 command syntax was checked via installed help; its global configuration was not changed or an installation claimed.

An independent evaluator used a copied two-skill package and isolated project for a Korean behavior-first then Wiki-add request. It initialized behavior mode, checked status, added Wiki, and checked status again. The Wiki became primary; features stayed empty. Existing AGENTS.md, project description, and owner note remained byte-identical; no RAG index, DB, graph, adaptation file, optional dependency, or external service was added. Project records stayed outside the installed package. The run confirmed Korean generated labels, not a persisted language preference; the setup guide now explicitly distinguishes per-command --lang from future-session preferences.

The package builder uses staged blobs and deterministic ZIP entries, with a source-tree/per-file SHA-256 manifest. Original architecture/prompt preservation and archive inspection are checked before publication. The CI matrix and artifact workflow are configured separately; local success does not claim unobserved remote runs, official directory registration, universal host compatibility, or a reuse license.
