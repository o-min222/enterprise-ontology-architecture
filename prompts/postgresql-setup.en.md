# PostgreSQL shared-model starting prompt

```text
Act as a PostgreSQL data modeler. Design the smallest useful shared semantic
model (roughly 3–5 core entities) for [business task].

Inspect existing schema read-only. Do not change it yet. Prepare:
1. Entities, PK/FK, relationships, shared/source ID mappings.
2. Roles for source_record, entity, entity_link, assertion, interpretation,
   decision_event, execution_event, ontology_schema_version.
3. Five information types and four independent verification statuses.
4. Provenance, correction history, permissions, audit.
5. DDL, clearly fictional data, integrity checks, rollback SQL.
6. Whether the existing RDBMS suffices and the need/cost of additional tools.

Before production access or migration, show impact and backup/recovery.
Use existing explicit authorization or obtain the missing approval.
Never transmit real personal or confidential data outside permitted scope.
Respond in my language while retaining schema keys, IDs, and enum values.
```
