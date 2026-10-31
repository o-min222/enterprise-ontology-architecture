# Information model: independent axes

[한국어](information-model.md)

L1 holds source records. L2 defines shared entities, attributes, relationships, meanings, and constraints. Individual, departmental, and AI interpretations remain separate attributed records. Apps, BI, APIs, and AI consume them at L3. These layers do not prescribe a storage technology.

| information_type | Example | Separate verification question |
| --- | --- | --- |
| observation | A sensor recorded a stop | Does the record establish the actual duration? |
| hypothesis | Cooling might be the cause | What conditions or evidence support the hypothesis? |
| reviewed_assessment | Maintenance reviewed risk using criterion R2 | Is the review's conclusion justified? |
| official_decision | A committee adopted a restart | Does the decision exist, remain effective, and establish safety? These are separate claims |
| execution_result | A request was attempted and returned a timeout | Did the downstream action actually complete? |

`verification_status` is `unverified` (not checked), `in_review` (being checked), `verified` (checked within a stated scope), or `disputed` (contradicting evidence exists). Disputed does not mean conclusively false. All five types allow all four statuses. They are not a maturity pipeline, confidence score, or approval rank. A status change does not change the information type. An adopted decision or actual execution is a new linked record, not an overwrite of the hypothesis.

Separate the observation that a statement was made from the truth of its contents. Checking that a committee called a machine safe does not establish technical safety.

## Optional exchange format

[assertion.schema.json](../assets/assertion.schema.json) describes a single durable claim. It does not require JSON for everyday answers. Map existing system fields without changing their meaning.

| Field | Meaning |
| --- | --- |
| schema_version | Exchange format version, `1.0` |
| id / entity_ids | Claim ID and L2 entity IDs; an unknown entity may use an empty list |
| statement | One scoped claim |
| information_type / verification_status | Independent classifications |
| author_or_model / created_at / version | Attribution, creation time, record version |
| source_refs | Source ID, original locator/version, access time, availability |
| semantic_context | L2 model ID/version/definition, or null |
| verification | Scope, method, and evidence source IDs |

Evidence IDs refer to the record's source_refs. Verified records need nonempty evidence. An unsupported hypothesis may have no sources and remain unverified. Mark unavailable originals with `availability: unavailable` and `accessed_at: null`; narrow the checked scope when only some evidence is accessible.

The schema validates shape, not truth, evidence quality, access rights, or execution authority. Resolve links separately. Store no credentials. Translation does not change these contracts; see [languages](languages.md).
