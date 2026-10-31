---
name: evidence-first-setup
description: Set up or reconfigure Evidence-First for a chosen project; select language, storage, optional retrieval, and adaptation preferences. Use for requested onboarding or configuration changes.
---

# Set up Evidence-First

This companion ships with the `evidence-first` core skill. Locate and read its `SKILL.md` and the relevant workspace-lifecycle reference in the installed package. In this repository the core is the sibling `evidence-first` directory. If missing, explain how to install the complete plugin or core; do not improvise a different schema. The core remains usable alone.

Respond in the user's preferred language. Reuse choices and permissions already given. Ordinary analysis needs no onboarding or persistent store.

1. Establish the target project and inspect existing Evidence-First configuration read-only. Installation location and target project are different: never store project knowledge inside the installed plugin. Preserve existing configuration and records.
2. For missing choices, offer a concise selection: behavior only; file Wiki; SQLite; local RDF graph DB; or a justified combination. Choose one primary for multiple stores. Explain the practical cost in the user's language. A small task normally needs behavior only. Separately offer RAG and relationship lookup only where useful; neither grants verification or execution authority.
3. Reuse existing language preferences. Tool catalogs support `en`, `ko`, `ja`, `zh`, with explicit English-message fallback for other valid tags. The AI can answer in the requested language. `--lang` applies to each helper invocation; the workspace config has no saved language-preference field. Do not claim future sessions were configured by that flag. Use authorized project instructions if the user wants a durable response-language preference. Keep source text, IDs, enum values, and permissions intact. No preference is silently inferred from machine paths.
4. Explain a concrete configuration before writes. An explicit setup request authorizes the selected local setup inside its stated scope; do not ask again for that authority. Ask only for genuinely missing choices or authority. Behavior-only operation does not need files. Use the core `workspace.py` helper for persistent setup, after checking its `--help`. Install optional graph dependencies only when graph use is selected and authorized. Do not install dependencies for behavior/Wiki/SQLite alone.
5. Keep default adaptation `task_scoped`. Offer `propose_only` or owner-defined `scoped_auto` only if relevant, using the core adaptation policy. Configuration is a preference, not an access-control grant. Do not invent budgets, permissions, monitors, accounts, or services. Preserve existing policies.
6. Verify actual configuration with helper `status` after a write, then show a small synthetic first-use example in the chosen language. For existing records use the core add/migration procedure and preview before switching; keep originals. Report selected storage, primary, features, created paths, and any missing optional dependency. Do not promise synchronization or runtime enforcement.

Use a short handoff such as: “Behavior only is ready. I will distinguish sources, interpretation, verification, and permission. No persistent store was requested.” For Wiki/DB, report only the actual paths and checks observed. Setup succeeds only after those checks; proposing a configuration is not successful installation.
