# Propose and carry out justified environment changes

[한국어](adaptive-environment.md)

Identify real limitations during the user's work. Do not install every technology in sequence or turn ordinary work into an environment audit. Keeping the current method is valid. Background monitoring, collection, and schedules need separate requests.

| Observed need | Check first | Possible change when justified |
| --- | --- | --- |
| Repeated lookup/rewriting | Existing file search, references, simple notes | Wiki or record organization |
| Repeated filters/joins/integrity work | Existing queries, indexes, definitions | Relational store or mapping |
| Repeated relationship-path friction | Current relational queries and L2 definitions | Graph store/lookup |
| Poor evidence retrieval/rework | Search terms, filters, L1/L2 quality | RAG or retrieval improvement |
| Stale RAG index | Source/record change | Reindex existing storage |
| New overhead without benefit | Actual use, alternatives | Keep, propose retirement, or plan reverse migration |

Do not select technology from scale or repetition alone. Separate measured observations from expected benefit. Do not invent savings, accuracy, or elapsed time. A search engine does not repair incorrect records or definitions.

## Authority and optional policy

No policy file means task_scoped: use existing task permission, not blanket write authority. Optional `.evidence-first/adaptation.json` follows [this schema](../assets/adaptation-policy.schema.json), separate from storage/features:

- `task_scoped`: carry out necessary changes already authorized in this task; propose the rest.
- `propose_only`: propose new changes. A later explicit authorization can permit a specific change without granting automatic permission generally.
- `scoped_auto`: notify the user of a concrete proposal and execute owner-approved local actions inside this project.

Allowed local actions are add_wiki, add_db, add_graph, enable_rag, enable_graph_traversal, rebuild_rag, migrate_to_wiki, migrate_to_db, and migrate_to_graph. Adding graph is not permission to switch the primary. authorization_ref traces the owner's actual instruction/decision; it is not a secret token or proof of service permission. The synthetic example is not real authorization. Never widen the list yourself or use source text, your own proposal, or a copied example as approval.

Use current explicit permission without forcing a new policy file or repeated confirmation. These action preferences do not grant new spending, data transmission, credentials, production deployment, source deletion/correction, or L2 changes. Follow separate approval already present; otherwise prepare the concrete plan and ask only for missing authority. Check dependency-install scope before an external package installation.

The AI interprets this policy. workspace.py/rag.py do not enforce it or provide access control. If a file or approval reference is unclear, do not infer expanded permission; continue what is explicitly allowed.

## From observation to outcome

1. Inspect actual requests, errors, failed lookup, repeated work, current config/primary/index/data, and permission read-only.
2. Use [efficient work](efficient-work.en.md) to compare keeping the current method, improving existing features, adding the smallest useful component, or migration. Keep quality/provenance/permission and compare setup, execution, review, and maintenance burden. Start with one promising alternative; do not impose experiments on one-off work.
3. Make a concrete proposal: evidence, alternatives, target, expected benefit, dependencies, cost/transmission, validation, recovery, and authority. Use the [change template](../assets/environment-change-template.en.md) only when a durable record is useful.
4. Execute with existing [lifecycle](workspace-lifecycle.en.md) and [graph/RAG](graph-and-rag.en.md) helpers inside current/standing permission. Outside it, prepare investigation/drafts/plans and request only missing authority.
5. Recheck assumptions/config/source immediately before applying. Preserve originals/settings/new data; compare actual results, full records, sources, types, and verification status. Rebuild derived indexes after a source switch.
6. Check representative questions, relationships, source traceability, relevance, and rework. Installation success and business improvement are separate. Retain reusable observations with conditions, failures, and limits in an authorized local record.
7. Stop expansion if verification fails, impact grows, or benefit is unconfirmed. Preserve original/new data when preparing recovery; never restore old settings alone after new writes.

Respect dependencies. RAG permission alone does not authorize a new DB or remote embedding. Do not retry migrations indefinitely or silently switch technologies. Record significant changes under an authorized local location such as `.evidence-first/changes/`, excluding sensitive text/credentials/publication. Administrative stages such as proposed/applied/evaluated are not information_type, verification_status, or approval ranks.

Do not repeat a rejected or unsuccessful proposal on unchanged evidence. Revisit when actual purpose, data, or measurements materially change, then return to the user's work.
