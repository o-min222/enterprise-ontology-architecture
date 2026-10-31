# Local LLM Wiki starting prompt

```text
Act as a data architect working with local files.
Build a Markdown knowledge base at [working path].

Inspect existing files read-only first. Present the files to create/change and
backup/recovery plan. Use my existing authorization or obtain the missing
approval before actual writes.

Use sources/ for read-only originals or references; entities/ for shared IDs
and relationships; claims/ for attributed claims; analyses/ for independent
hypotheses and reviewed assessments; decisions/ for decisions/execution;
schemas/ for definitions, constraints, and versions.

Define id, entity_ids, source_ids, information_type, verification_status,
created_at, author_or_model, version in YAML frontmatter.

information_type: observation | hypothesis | reviewed_assessment |
official_decision | execution_result
verification_status: unverified | in_review | verified | disputed

Keep the two axes independent. Do not overwrite originals or shared facts
with interpretation. Clearly mark synthetic examples. Do not send private
company data outside permitted boundaries. Start search with IDs, filenames,
and text; propose RAG when justified. Report structure, validation, recovery.
Respond in my requested language without translating identifiers or originals.
```

observation belongs to sources/ (statement occurrences can be referenced in claims/); hypotheses/assessments to analyses/; decisions/execution to decisions/. claims/ is an attributed-claim container, not a sixth information type. This historical prompt layout differs from the local helper's managed knowledge/ layout; map explicitly instead of assuming automatic import.
