# Separate judgment and execution authority

[한국어](action-policy.md)

Verified describes a checked scope, not permission. An official decision does not grant the current AI account a write token or deployment approval. Installing a skill grants no access.

| Work | Check and retain |
| --- | --- |
| Read, analyze, propose | Authorized access, sources, uncertainty |
| Write/share an independent assessment | Author, purpose, criteria, audience; no automatic shared-fact promotion |
| Correct L1 | Source-owner authority, evidence, previous value, reason, history |
| Change L2 | Model owner/affected functions, impact, version, recovery |
| Adopt a formal decision | Responsible authority, criteria, validity period, withdrawal conditions |
| Execute an action | System/object/action, permission, required approval, impact, audit, recovery |

Compare target, environment, change, and scope with existing authorization. Do not repeatedly request approval already supplied. Verify required organizational approval and real service rights. Prepare a concrete, reviewable plan when a write lacks authority; continue permitted analysis and drafting.

AI-initiated improvements follow [adaptation](adaptive-environment.en.md). Existing task approval or owner-defined local actions can authorize execution after a short proposal. The proposal itself is not approval. A specific user-authorized change may proceed under a propose-only standing preference without rewriting it into blanket automatic permission.

Do not replace read-only credentials with write credentials or bypass service controls. Separate read and write tools/credentials; enforce roles, targets, and approval scope in services, APIs, or databases. Markdown cannot implement those controls.

After execution, inspect responses and actual state. Record request ID, target, time, observed result, verification scope, and remaining uncertainty in an authorized audit location. Distinguish planned, accepted, and completed. Request acceptance is not downstream completion.

A timeout leaves execution uncertain. Inspect state, request IDs, and idempotency information before a necessary authorized retry. Stop unbounded retries or expanding impact. An observed failed attempt can be an execution_result; an unexecuted plan cannot.
