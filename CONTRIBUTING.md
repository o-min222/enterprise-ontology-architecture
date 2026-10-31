# Contributing

Contributions and reports may be written in your preferred language. English summaries help wider review; do not label an unreviewed translation as authoritative.

1. Open an issue describing the observed problem and a small synthetic reproduction, or send a focused pull request.
2. Preserve the original architecture docs and prompts. Keep the five information types and four statuses independent; language changes must not alter IDs, records, or authority.
3. Keep `skills/evidence-first` installable alone. Setup is a companion shipped by the plugin. Add dependencies only for an actual feature; keep behavior-only use dependency-free.
4. Install `requirements-test.txt` in a virtual environment and run `python -m unittest discover -s tests -v` and `git diff --check`. For manifest changes, run `claude plugin validate .claude-plugin/plugin.json` and `claude plugin validate .claude-plugin/marketplace.json --strict` when Claude Code is available. The retained root CLAUDE.md produces an expected advisory: it is project context, not automatically loaded plugin context; the skills carry the plugin instructions. Review any new warnings. See [validation](tests/README.en.md).
5. Stage reviewed changes, then run `python scripts/package_plugin.py`. The packager uses the Git index and rejects unstaged tracked edits. Inspect the archive before sharing. Never stage private records to satisfy packaging.

Keep both plugin manifest versions and the changelog aligned. Document changed behavior, validation limits, and migration implications. For translations, update the [language manifest](skills/evidence-first/locales/manifest.json) and parity tests when adding catalogs. Existing full/quickstart/fallback support tiers must remain explicit.

No contribution license agreement is asserted here. This repository currently has no declared reuse license; discuss licensing with the owner before contributing material you cannot authorize. Do not submit third-party material without the necessary rights. See [support](SUPPORT.md) and [security reporting](SECURITY.md).
