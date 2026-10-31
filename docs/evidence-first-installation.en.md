> For the complete plugin, onboarding, updates, and removal, start with the [plugin guide](plugin-guide.md). The instructions below also cover standalone core installation and project instruction integration.

# Install and connect Evidence-First

[한국어](evidence-first-installation.md) · [Language support](../skills/evidence-first/references/languages.md)

The portable unit is the **entire** [skills/evidence-first](../skills/evidence-first/SKILL.md) directory. SKILL.md has standard name/description frontmatter and provider-neutral instructions. It does not grant source access, transmit data, or authorize writes.

## Review and pin

Start in a temporary checkout location outside the target project:

```sh
git clone https://github.com/o-min222/enterprise-ontology-architecture.git
cd enterprise-ontology-architecture
git rev-parse HEAD
```

Record and review the commit. Reproduce installation with `git checkout --detach <reviewed-commit-SHA>`, replacing the placeholder. Check the repository's license grant and organizational use policy separately; this package adds no new license declaration.

## Copy to the product's discovery path

| Tool | Project | User-wide | Explicit invocation |
| --- | --- | --- | --- |
| Codex | PROJECT/.agents/skills/evidence-first | ~/.agents/skills/evidence-first | $evidence-first |
| Local Claude Code | PROJECT/.claude/skills/evidence-first | ~/.claude/skills/evidence-first | /evidence-first |
| Other Agent Skills hosts | Documented product-specific skill path | Product-specific | Product-specific |

Paths were checked against [OpenAI documentation](https://learn.chatgpt.com/docs/build-skills) and [Claude Code documentation](https://code.claude.com/docs/en/skills) on 2026-10-31. Managed settings, versions, and remote sessions can differ. Do not assume every product scans the same directory.

PowerShell, from the checkout root. Edit the target and product, then run once for codex or claude:

```powershell
$projectPath = 'C:\Projects\my-project'
$agentName = 'codex'
if ($agentName -notin @('codex', 'claude')) { throw 'Choose codex or claude.' }
$skillSource = (Resolve-Path -LiteralPath './skills/evidence-first').Path
$agentFolder = if ($agentName -eq 'codex') { '.agents' } else { '.claude' }
$skillParent = Join-Path $projectPath "$agentFolder/skills"
$skillTarget = Join-Path $skillParent 'evidence-first'
if (Test-Path -LiteralPath $skillTarget) { throw 'Review and back up the existing installation before replacement.' }
New-Item -ItemType Directory -Path $skillParent -Force | Out-Null
Copy-Item -LiteralPath $skillSource -Destination $skillTarget -Recurse
Get-Content -LiteralPath (Join-Path $skillTarget 'SKILL.md') -TotalCount 5
```

macOS/Linux, also from checkout root; use .claude instead of .agents for Claude Code:

```sh
project_path='/path/to/my-project'
skill_parent="$project_path/.agents/skills"
skill_target="$skill_parent/evidence-first"
if [ -e "$skill_target" ]; then
  echo 'Review and back up the existing installation before replacement.'
else
  mkdir -p "$skill_parent" && cp -R skills/evidence-first "$skill_target"
fi
```

Do not overwrite existing skill folders or replace project instructions wholesale. Check duplicate-name selection rules if user/project scopes both contain the skill. Do not install one skill copy per language: use one skill identity with localized references/catalogs.

## Connect baseline instructions

Merge into the target project's existing AGENTS.md, adjusting the skill path for that host:

```markdown
For evidence-dependent analysis, coding, and operational recommendations,
read and apply `.agents/skills/evidence-first/SKILL.md`.
Use authorized L1 records/L2 definitions; keep interpretations separate.
Keep information type, verification, and execution authority independent.
Verify proportionately and retain provenance for important claims.
AI is an external ontology consumer. Respond in the user's requested language.
```

For Claude Code, put this real import outside a code fence in the sibling CLAUDE.md:

```markdown
@AGENTS.md
```

See [official imports](https://code.claude.com/docs/en/memory#import-additional-files). A Claude-only project may merge baseline rules directly and reference .claude/skills/evidence-first/SKILL.md. Repository-root AGENTS.md/CLAUDE.md in this distribution are maintenance instructions, not files to blindly copy into another project.

Without automatic discovery, explicitly ask the AI to read the installed SKILL.md and relevant references. Real L1/L2 access and write controls remain separate.

## Setup, language, update, removal

Installation and storage setup are distinct. Ask for setup when needed; select storage and features independently using [lifecycle](../skills/evidence-first/references/workspace-lifecycle.en.md). Ordinary tasks can use behavioral guidance alone.

Local helpers need Python 3.10+. Wiki/SQLite/RAG use its standard library and SQLite FTS5; graph storage needs the optional graph requirements. Use [graph/RAG](../skills/evidence-first/references/graph-and-rag.en.md) for actual commands. Existing server stores need explicit adapters.

The AI responds in the requested language. Generated Wiki labels/RAG rules have en/ko/ja/zh catalogs; use --lang before the command. Other valid tags have an English-message fallback. JSON keys/IDs/enum values/original records remain unchanged. Cross-language lexical search may use an explicit --search-query. Older index-version-1 files require a rebuild for the new tokenizer; presentation language alone does not require reindexing. [Language boundaries](../skills/evidence-first/references/languages.md).

Optional [adaptation policy](../skills/evidence-first/references/adaptive-environment.en.md) and [conditional efficiency experience](../skills/evidence-first/references/efficient-work.en.md) use current permission without requiring extra files or repeated approval. Synthetic policies are not authorization.

1. Start a fresh local session and check discovery/explicit invocation.
2. Ask the AI to analyze the [English fictional sources](../skills/evidence-first/examples/synthetic-sources.en.md), distinguish checked facts from hypotheses, and answer in your chosen language.
3. Compare actual response/tool use with [examples](../skills/evidence-first/examples/README.en.md) and [validation](../tests/README.en.md). Confirm that the files were actually read.
4. Update by reviewing a new pinned commit, comparing/backing up the old installation, and replacing the complete folder. Record the installed version.
5. Remove only the installed skill and the exact guidance you merged. Preserve original records, other skills, and policies. Restart to confirm removal.

Format follows [Agent Skills](https://agentskills.io/specification). L1/L2 and the classifications are this project's model, not classifications defined by that format standard.
