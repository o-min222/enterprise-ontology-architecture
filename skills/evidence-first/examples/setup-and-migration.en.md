# Synthetic setup and migration

All material is fictional. Use the [lifecycle guide](../references/workspace-lifecycle.en.md).

- "Apply behavioral guidance only": init behavior if the user wants persistent settings; create no knowledge store. Instructions alone also work without settings.
- "Add a local DB, no Wiki": add db directly. Do not collect every past conversation or call it verified data.
- "Add a Wiki but keep DB primary": add wiki creates an empty component, not a synchronized copy. Say what was actually done.
- "Move the primary to Wiki; keep DB": preview, copy/compare, then apply migration. Preserve full records, shared material, and old DB. Later Wiki writes do not automatically update DB.
- "Target contains a different assessment": preserve it, compare authors/source/version, and map conflicts rather than overwriting or promoting it to fact.
- "Use our PostgreSQL": inspect the real schema/permissions and design explicit mapping/recovery. Do not report completion from a SQLite option.

## Add graph and RAG

Inspect existing Wiki records, prepare optional dependencies inside authorized scope, preview/apply graph migration, then enable graph_traversal and rag separately. Build a new-primary index. Relationship links do not prove causality.

For "Has the cooling cause been verified? Is restart currently valid?", preserve hypothesis/unverified and official_decision/disputed, connect E-style citations to actual originals, and do not restart the machine.

Switching primary back to SQLite retains graph/source data but invalidates the old source-specific RAG index. Rebuild rather than treating the old index as new-primary evidence.
