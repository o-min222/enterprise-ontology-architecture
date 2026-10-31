# Validation

[한국어](README.md)

The skill needs no Python to read. Local helpers require Python 3.10+; Wiki/SQLite/RAG use the standard library and SQLite FTS5, while graph operations need optional pyoxigraph. Full test dependencies include graph testing.

From repository root:

```sh
python -m venv .venv
```

Activate with `.venv\Scripts\Activate.ps1` in Windows PowerShell or `source .venv/bin/activate` on macOS/Linux. If activation is restricted, invoke the virtual environment's Python directly.

```sh
python -m pip install -r requirements-test.txt
python -m unittest discover -s tests -v
git diff --check
```

Checks cover package/frontmatter/local links, installation-unit independence, claim-schema validity, all 20 classification combinations, invalid records/missing verification evidence, source references, storage setup, additions versus migration, complete-record/shared-file preservation, conflicts/failure recovery/locks, real Oxigraph/SPARQL, config compatibility, and local RAG freshness/context integrity. Adaptation policy tests validate a declarative agent contract, not permission enforcement.

Multilingual checks cover complete message catalogs, regional/unsupported fallback, invalid tags, unchanged canonical records across localized rendering, original and rewritten queries, basic CJK lexical retrieval, old-index invalidation, UTF-8 command output, language-fixture schema/IDs, and reference links.

Behavior is assessed separately with actual AI responses and tool traces: original conflict, independent interpretation, permission, source omission, timeout, stale index, authorized adaptation, bounded comparison, and conditional experience reuse. See [English scenarios](scenarios.en.md), [current validation summary](validation-report.en.md), and the retained [Korean historical report](validation-report.md). A passing schema or test suite does not prove universal model compliance, security, translation quality, or performance.

For preservation, compare original docs/prompts against the baseline commit. English translations/additional guides do not replace the originals. Locale display never makes a translated claim verified or grants execution authority.
