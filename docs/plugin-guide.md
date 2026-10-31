# Plugin guide

[한국어](plugin-guide.ko.md) · [Home](../README.en.md)

Evidence-First 0.1.0 is a skills-only plugin preview distributed by this repository. It is not listed in an official OpenAI or Anthropic directory. No hosted service, account, API key, MCP server, or background process is required. The AI host still determines available tools and permissions.

## Install and start

### Codex CLI / supported OpenAI plugin clients

```sh
codex plugin marketplace add o-min222/enterprise-ontology-architecture
codex plugin add evidence-first@evidence-first-plugins
```

Start a new conversation and use `$evidence-first-setup` for guided setup or `$evidence-first` for ordinary work. Plugin features and directory interfaces vary by client/version. If your client lacks plugin commands, use the [standalone installation](evidence-first-installation.en.md). The repository marketplace also supports local discovery in supported clients when this repository is the trusted project; use your client's plugin interface to enable it.

### Claude Code

Inside Claude Code:

```text
/plugin marketplace add o-min222/enterprise-ontology-architecture
/plugin install evidence-first@evidence-first-plugins
```

Start a new session. Run `/evidence-first:evidence-first-setup` or `/evidence-first:evidence-first`. A local clone can be loaded temporarily without installing: `claude --plugin-dir "/absolute/path/to/enterprise-ontology-architecture"`. Standard plugin skill names are namespaced by Claude Code.

### Other coding AIs

Copy the entire `skills/evidence-first` folder into the host's supported skill directory, or reference its `SKILL.md` through the host's project instructions. Read [installation and AGENTS.md/CLAUDE.md integration](evidence-first-installation.en.md). For guided setup install both skill folders together, preserving their sibling layout. Core-only installations do not require the setup companion.

Do not overwrite an existing AGENTS.md or CLAUDE.md. Merge a short reference into project instructions when persistent application is wanted; the root repository files are integration examples, not automatically injected into other projects. Plugin installation alone does not guarantee every host selects the skill on every turn.

## First-use examples

| Ask | Expected result |
| --- | --- |
| “Use Evidence-First to summarize these two public sources in Spanish.” | Spanish response, original source links, separated interpretation, proportionate verification; no DB needed |
| “Set up a Korean file Wiki in this project; no RAG yet.” | Inspect target, reuse choices, create authorized local Wiki, check status, Korean labels |
| “Add RAG to my existing SQLite records.” | Check current primary and records; build a derived local lexical index; return cited context to the AI |
| “Repeated relationship lookups are slow. Find a better approach.” | Small comparison/proposal; change only within current authority; report observed benefit or uncertainty |

Initial setup separates storage (none/Wiki/SQLite/graph/combinations), primary store, features (RAG/relationship lookup), language, and adaptation preferences. No mandatory storage or approval ceremony is imposed on ordinary work. Examples in the package are synthetic. Start at [examples](../skills/evidence-first/examples/README.en.md).

Behavior-only use requires no Python dependencies. Local helpers need Python 3.10+; RAG needs SQLite FTS5. Graph support additionally needs the pinned-range dependency in `skills/evidence-first/requirements-graph.txt`. Helpers use explicit `--root` for the target project and `--lang` for presentation. Follow `--help` and the lifecycle guide rather than running commands in the installed plugin directory.

## Update and remove

Review the [changelog](../CHANGELOG.md) and back up project records before updating. For a reproducible review, pin a Git commit and record it; the main branch can move. Codex CLI can add a marketplace with `--ref COMMIT`. For manual installations, keep the previous core folder until the replacement passes checks. Do not mix scripts from different snapshots.

Codex CLI update:

```sh
codex plugin marketplace upgrade evidence-first-plugins
codex plugin list
```

Use the installed command's current help if upgrade behavior differs. After refreshing, inspect the plugin list and start a new conversation. Remove with `codex plugin remove evidence-first@evidence-first-plugins`. Claude Code supports `/plugin marketplace update evidence-first-plugins` followed by `/plugin update evidence-first@evidence-first-plugins`; restart the session. Remove with `/plugin uninstall evidence-first@evidence-first-plugins`.

Removing the plugin does not remove project knowledge, config, indexes, or backups. Remove those separately only with the owner's explicit intent and retention/access requirements. Updating never silently migrates records or starts synchronization. Existing setup changes use preview/copy/compare/switch with originals retained.

## Troubleshooting

- **Plugin unavailable:** check host version, configured marketplace, plugin enabled state, and restart/new session. Fall back to core-folder installation when unsupported.
- **Skill not selected:** explicitly invoke the skill; use project instructions for persistent guidance. Host loaders differ.
- **Graph dependency missing:** install only the optional graph requirements in the chosen environment, or continue with existing storage.
- **RAG says stale:** rebuild from the selected primary after checking source changes; never treat cached ranking as verification.
- **Language fallback:** valid unsupported catalog tags announce English tool-message fallback; the AI may still answer in the requested language. English/Korean full guides, Japanese/Chinese quickstarts/catalogs, and other-language answers are distinct support levels.

See [support](../SUPPORT.md), [privacy](../PRIVACY.md), and [security](../SECURITY.md). The repository currently declares no reuse license; public availability is not an open-source license.

## Packaging and verification

Portable identity is in root `plugin.json`; `.claude-plugin/plugin.json` is the Claude compatibility entry. Both versions must agree. Root `skills/` contains core and setup; OpenAI presentation metadata lives in the root extension and skill `agents/openai.yaml`. Repository marketplaces point to this package root. Empty hooks, MCP, or app stubs are intentionally unnecessary.

Contributors run the [test suite](../tests/README.en.md), native Claude manifest validation where available, and `python scripts/package_plugin.py` after staging reviewed files. The deterministic ZIP contains staged Git blobs plus `BUILD-INFO.json` (source tree and SHA-256 digests). Untracked runtime/private files are never crawled; known runtime paths and unstaged tracked edits are rejected. This does not replace reviewing content for private information. CI builds are workflow artifacts, not GitHub Releases or official directory listings.

Format references checked 2026-10-31: [OpenAI packaging](https://developers.openai.com/plugins/build/plugins), [Agent Plugins schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json), [Claude manifests](https://code.claude.com/docs/en/plugins-reference), [Claude marketplaces](https://code.claude.com/docs/en/plugin-marketplaces). Client commands can evolve; use installed help when it differs. See the [validation report](../tests/validation-report.en.md) for what was actually tested.
