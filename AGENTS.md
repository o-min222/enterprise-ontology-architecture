# Repository instructions

[한국어](AGENTS.ko.md)

This public repository distributes shared L1 source-record/L2 semantic-model design guidance and the Evidence-First skill. AI is an external L3 consumer, not a required ontology component.

- Read [Evidence-First](skills/evidence-first/SKILL.md) for evidence-dependent analysis, design, coding, and verification. Keep simple edits proportionate.
- Use accessible shared sources and definitions; separate others' assessments from your own inference. Originals can also be incomplete or wrong.
- Keep the five information types and four verification statuses independent. Decisions, verification, and execution authority do not substitute for each other.
- Follow [workspace lifecycle](skills/evidence-first/references/workspace-lifecycle.en.md) for setup, additions, and migration. Separate storage and features, select one primary, preserve originals, and rebuild derived indexes after a source switch.
- Use [adaptation](skills/evidence-first/references/adaptive-environment.en.md) and [efficient work](skills/evidence-first/references/efficient-work.en.md) to propose and perform justified improvements within existing permission. Keeping the current method is valid. Stop unsuccessful expansion; never expand your own authority.
- Preserve existing Korean docs and prompts. Source corrections, shared definition changes, independent assessments, formal decisions, and actions follow distinct paths.
- Continue work already authorized by the user. Do not turn read/analysis permission into write permission or repeatedly request existing approval.
- Publish only public material or clearly synthetic examples. Exclude private documents, personal data, credentials, internal URLs, and sensitive metadata. Retention rules never require public retention of secrets.
- Use the user's requested language. Maintain one standard skill identity, English SKILL.md and Korean SKILL.ko.md; keep language variants semantically aligned and IDs/enum values stable. Add catalogs with the documented fallback instead of duplicating executable logic.
- Run `python -m unittest discover -s tests -v` and `git diff --check`. Read [test guidance](tests/README.en.md) for scope and limitations.

These instructions and the skill do not replace higher-priority instructions or real access controls.
