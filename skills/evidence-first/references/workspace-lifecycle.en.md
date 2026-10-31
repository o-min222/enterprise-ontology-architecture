# Setup, additions, and migration

[한국어](workspace-lifecycle.md)

Ordinary tasks need no setup. When setup is requested, reuse existing choices and ask only for missing storage/feature/location choices. For an observed improvement need, follow [adaptation](adaptive-environment.en.md) first.

Choose storage separately from features:

| Storage | Local implementation |
| --- | --- |
| none / behavior | Instructions only; no knowledge store |
| wiki | JSON claim ledger and derived Markdown |
| db | SQLite |
| graph | Oxigraph RDF DB, optional dependency |
| combination | Selected stores with one primary |

Basic lookup is always available. RAG needs at least one store; relationship lookup needs graph storage. RAG does not require a graph. Existing DBs or Wikis must be inspected/mapped; never replace a requested server DB with SQLite by assumption.

## Local helper and settings

The skill needs no Python to read. The optional [workspace.py](../scripts/workspace.py) uses Python 3.10+. Wiki/SQLite/local RAG use the standard library; graph storage requires [requirements-graph.txt](../requirements-graph.txt). No automatic source collection, model API, scheduler, or production connection is included.

`PROJECT/.evidence-first/config.json` stores storage/features, not permission:

```json
{"config_version":"2.0","behavior":"evidence-first","enabled_components":["wiki","graph"],"primary_store":"wiki","enabled_features":["rag","graph_traversal"]}
```

Version-1 settings remain readable without rewriting. A real addition, feature change, or migration saves a history copy and writes v2. No record rebuild or automatic RAG activation is implied. Optional adaptation policy is separate; see [policy](adaptive-environment.en.md).

Replace PATH_TO_SKILL and PROJECT with actual paths. Choose one init command:

```sh
python "PATH_TO_SKILL/scripts/workspace.py" --root "PROJECT" init --mode behavior
python "PATH_TO_SKILL/scripts/workspace.py" --root "PROJECT" --lang en init --mode wiki
python "PATH_TO_SKILL/scripts/workspace.py" --root "PROJECT" init --mode db
python "PATH_TO_SKILL/scripts/workspace.py" --root "PROJECT" init --mode graph --features rag graph_traversal
python "PATH_TO_SKILL/scripts/workspace.py" --root "PROJECT" init --stores wiki db graph --primary graph --features rag
```

Multiple stores require an explicit primary. The existing hybrid mode remains a Wiki+SQLite shorthand. Init refuses existing configuration. Behavior-only creates a settings file but no knowledge directory. Users may also use instructions without any settings file.

## Records and normal work

- `knowledge/shared/`: accessible source references, separate L2 definitions and independent interpretations. Copy originals only when authorized.
- `knowledge/wiki/records.json`: canonical Wiki claim records. `index.md` is regenerable, with type/status/scope displayed. Keep user-authored text under shared, not only in generated pages.
- `knowledge/db/evidence.sqlite3`: assertions table, full JSON payload plus matching id/type/status projections. Independent CHECK constraints cover type and status.
- `knowledge/graph/`: optional native RDF projection and full JSON payload.
- `.evidence-first/rag.sqlite3`: optional derived search index.

Resolve relative source locators from the project root. Shared sources, definitions, and independent assessments keep their locations during local store migration. Only the primary accepts ordinary writes. Secondary stores are snapshots, not automatically synchronized; do not double-count them or claim they are current.

```sh
python "PATH_TO_SKILL/scripts/workspace.py" --root "PROJECT" status
python "PATH_TO_SKILL/scripts/workspace.py" --root "PROJECT" add graph
python "PATH_TO_SKILL/scripts/workspace.py" --root "PROJECT" enable rag
```

Adding creates an empty store without copying or switching an existing primary. The first store added to behavior-only becomes primary. Registered additions are idempotent; unregistered existing stores require inspection. Enabling RAG records a feature choice but does not build its index. Graph relationship lookup requires graph_traversal.

## Copy, compare, then switch

```sh
python "PATH_TO_SKILL/scripts/workspace.py" --root "PROJECT" migrate --to graph
python "PATH_TO_SKILL/scripts/workspace.py" --root "PROJECT" migrate --to graph --apply
```

The first command is read-only and creates no store or lock. Apply copies/compares before switching the primary, using existing approval without repeated questions.

1. Pause writers; inspect scope, IDs, schema, counts, and locator base. The helper's lock coordinates its own writers, not other apps.
2. Prepare recovery. The helper retains the old source and saves prior settings under history; follow additional backup requirements.
3. Validate the [claim schema](../assets/assertion.schema.json) and mappings. The helper checks identity/classification/duplicates and projections, not full truth, access, or schema quality.
4. Wiki/SQLite/Oxigraph transport retains every JSON field/value. Compare counts and sorted full-JSON SHA-256; abort a switch if the source changes. Identical targets need no duplicate insertion. Unknown graph triples or divergent projections require explicit mapping.
5. Refuse conflicting target data rather than overwriting/merging. Preserve existing targets and agree on a mapping when needed.
6. Switch only after comparison. Keep original stores/shared material and write to the new primary. Rebuild RAG from the new source; old indexes are rejected. Deletion, retirement, synchronization, and scheduling are separate scope.

Only managed claim records are transported, not arbitrary Wiki pages/attachments/server tables. Inventory and preserve other material separately. Preserve original/new locator mappings if locations change. Pause external writers before graph reads too: concurrent read-only Oxigraph access and another process writing are unsupported.

On failure retain the old primary and inspect partial targets; do not delete them automatically. Inspect stale locks before removing them. If no new writes occurred and snapshots match, reverse migrate can switch back. If new data exists, plan a lossless reverse migration rather than restoring old settings alone.

For existing Markdown/YAML, PostgreSQL, remote graph DBs, or custom stores, the AI designs an explicit adapter/schema/key/attachment/permission/concurrency/recovery mapping. Do not claim the local helper connected to or migrated such systems. See [graph/RAG](graph-and-rag.en.md) and [language](languages.md) support.
