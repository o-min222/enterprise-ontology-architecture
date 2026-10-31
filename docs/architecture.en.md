# Architecture and governance overview

The original Korean documents are preserved: [principles](architecture-principles.md), [concepts](ontology-concepts.md), [governance](data-governance.md), [incremental implementation](implementation-guide.md), [platform comparison](palantir-comparison.md), [references](references.md).

L1 source records and L2 shared entities/definitions/relationships/constraints are shared assets within access policy. Individual, department, and AI interpretations remain separately attributed. Apps, BI, APIs, and AI consume them at L3. AI is not required for the ontology to exist. These are project working definitions, not a universal ontology taxonomy.

Sources are selective representations: record collection purpose, scope, period, method, and missingness. Models also reflect choices. Aim for traceability and independent reinterpretation rather than a claim of perfect neutrality.

Use the five information types and four verification statuses as independent axes. A formally adopted judgment can be disputed; a recorded execution may remain unverified. Decision existence, factual correctness, and execution permission are distinct.

Route source corrections through source owners with evidence/old values/reasons; shared definition changes through model owners and affected functions with impact/version/recovery; interpretation sharing through its author/responsible function; formal decisions through the business authority; real actions through authorized services with audit and recovery. Match governance effort to impact and reuse.

Start small with existing systems: link original IDs, agree on meanings/formulas, keep delivery/recurrence/cost assessments separate, reuse common objects in real workflows, then measure traceability, rework, error, and maintenance burden before expanding. Relational and graph DBs are implementation options, Wiki is a storage/authoring option, RAG is a retrieval use, APIs/MCP are interfaces. Searchability alone is not reliability.

This is platform-independent governance guidance, not a replacement for Palantir or another enterprise platform. The principles can also be implemented on such platforms. Distinguish capabilities from the operating defaults an organization chooses.

Supported concerns include definition conflict, provenance, governance, and model errors. Claims that most ontologies are already contaminated, that interpretation separation is always optimal, or that a particular ROI is guaranteed require further evidence. Separate projected opportunities from realized net savings.

Primary/background references: Gruber (1993), *A Translation Approach to Portable Ontology Specifications*; [W3C OWL](https://www.w3.org/TR/owl-guide/); [W3C PROV-O](https://www.w3.org/TR/prov-o/); [Palantir ontology documentation](https://www.palantir.com/docs/foundry/ontology); [collaborative ontology engineering study](https://pmc.ncbi.nlm.nih.gov/articles/PMC3845806/).
