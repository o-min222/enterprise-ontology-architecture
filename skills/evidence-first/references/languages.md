# Multilingual use

## Choose the response language

Follow an explicit language request first, then the user's established preference, then the conversation language. Do not infer a person's language from their name, repository path, operating system, or source documents. Do not ask again when the preference is clear. The English skill entry point does not require English responses.

Explain results, proposals, permission questions, and uncertainty in the chosen language. If a technical term is clearer in its original form, retain it with a short localized explanation. If reliable translation is uncertain and materially affects a decision, keep the original passage and identify the uncertainty instead of silently choosing a meaning.

## Support layers

| Layer | Shipped support | Fallback |
| --- | --- | --- |
| AI responses and explanations | User-requested language, subject to the AI's language capability | State uncertainty; retain original evidence |
| Core skill, setup and operating guides | English and Korean | Read a maintained version and explain it in the user's language |
| Repository quickstarts | English, Korean, Japanese, Simplified Chinese | English quickstart or an on-demand explanation |
| Generated Wiki labels, relationship description, RAG generation rules | `en`, `ko`, `ja`, `zh` catalogs | English messages with explicit resolution |
| CLI options, JSON keys, technical diagnostics | Stable English identifiers | The AI explains diagnostics in the requested language |

Regional tags use the base catalog: `en-GB` uses `en`; `zh` is the shipped Simplified Chinese catalog. The response language still follows the full requested tag. A base-catalog fallback does not claim a separately reviewed regional translation exists. Other valid tags, such as `es` or `fr-CA`, use English tool messages while the AI can answer in that language. Do not claim that every document or language has a reviewed translation.

Use `--lang` before the command:

```sh
python "PATH_TO_SKILL/scripts/workspace.py" --root "PROJECT" --lang ja init --mode wiki
python "PATH_TO_SKILL/scripts/workspace.py" --root "PROJECT" --lang ko migrate --to wiki --apply
python "PATH_TO_SKILL/scripts/rag.py" --root "PROJECT" --lang zh retrieve --question "冷却原因是否已确认？"
```

The helper default is English. The calling AI passes the user's language when localized tool text is useful. No workspace/schema migration or OS-language guessing is needed. Existing generated pages keep their current labels until an authorized regeneration; stored claims are never translated by a language flag.

## Preserve evidence and contracts

- Never translate schema keys, enum values, assertion/entity/source IDs, versions, timestamps, permission scopes, paths, or source locators into new identifiers.
- Preserve original records and source text. A translated explanation is a derivative interpretation, not a replacement original or evidence of verification.
- Label translated quotations as translations and keep their original location/version. Do not turn an unverified statement into a verified translation of fact.
- Keep `information_type` and `verification_status` independent in every language. `official_decision/verified` can mean the decision's existence was checked, not that its contents are true or execution is authorized.
- Language preference changes presentation only, not permissions, publication scope, storage selection, or the primary store.
- Synthetic language fixtures share IDs for comparison. Load one language variant into a test workspace; do not merge both as distinct events.

## Cross-language retrieval

Local FTS5 retrieval is lexical, not an automatic multilingual embedding or translation service. Index version 2 adds basic Korean/Japanese/Chinese character bigrams. Old version-1 indexes must be rebuilt; changing output language alone does not require rebuilding a current index.

If the question language differs from source language, inspect accessible source vocabulary and optionally prepare source-language keywords. Preserve the original question and use `--search-query` for the alternate query:

```sh
python "PATH_TO_SKILL/scripts/rag.py" --root "PROJECT" --lang ja retrieve --question "冷却原因は確認されましたか？" --search-query "cooling cause"
```

The result reports `question`, `search_query`, `query_was_rewritten`, and requested/effective message language separately. The AI, not the helper, proposes the rewritten terms. Do not invent a claim because a translation or keyword query has no hit. Read originals as needed, verify relevant terms, and state translation/retrieval limits. A language mismatch can cause missing results without proving missing events.

## Add a language

Add a UTF-8 JSON catalog under [locales](../locales/manifest.json) with the same keys as `en.json`, register its base tag, add an appropriate quickstart, and test rendering, fallback, Unicode retrieval, and unchanged payloads. Translate human explanations only; share one executable implementation and one skill identity. Review meanings of permission, verification scope, uncertainty, and source attribution as well as wording. Keep English/Korean skill versions aligned when behavior changes.
