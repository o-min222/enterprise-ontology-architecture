"""Optional native RDF graph backend (Oxigraph), imported only for graph work."""

import json
from urllib.parse import quote

try:
    from pyoxigraph import Literal, NamedNode, Quad, Store
except ImportError:
    raise ValueError("Graph storage needs the optional requirements-graph.txt packages") from None


NS = "urn:evidence-first:"


def node(kind, identity):
    return NamedNode(NS + kind + ":" + quote(identity, safe=""))


def predicate(name):
    return NamedNode(NS + name)


def quads(records):
    for record in records:
        entities = record.get("entity_ids", [])
        sources = record.get("source_refs", [])
        if not isinstance(entities, list) or any(not isinstance(identity, str) for identity in entities) or not isinstance(sources, list):
            raise ValueError("Graph entity/source references must be lists")
        assertion = node("assertion", record["id"])
        yield Quad(assertion, predicate("id"), Literal(record["id"]))
        yield Quad(assertion, predicate("payload"), Literal(json.dumps(record, ensure_ascii=False, sort_keys=True, allow_nan=False)))
        for field in ("information_type", "verification_status"):
            yield Quad(assertion, predicate(field), Literal(record[field]))
        for identity in entities:
            yield Quad(assertion, predicate("about"), node("entity", identity))
        for source in sources:
            yield Quad(assertion, predicate("derivedFrom"), node("source", source["source_id"]))
        context = record.get("semantic_context")
        if context:
            # Version is part of the model identity, not a property of reality.
            identity = json.dumps([context["model_id"], context["model_version"]], ensure_ascii=False)
            yield Quad(assertion, predicate("usesModel"), node("model", identity))


def mapped(records):
    try:
        return set(quads(records))
    except (KeyError, TypeError, AttributeError) as error:
        raise ValueError("Graph projection needs standard assertion fields and references") from error


def prepare(path):
    store = Store(path)
    store.flush()


def read(path):
    store = Store.read_only(str(path))
    rows = list(store.query(
        f"SELECT ?id ?type ?status ?payload WHERE {{ ?a <{NS}id> ?id ; "
        f"<{NS}information_type> ?type ; <{NS}verification_status> ?status ; <{NS}payload> ?payload }}"
    ))
    records = []
    for row in rows:
        record = json.loads(row["payload"].value)
        if not isinstance(record, dict) or (record.get("id"), record.get("information_type"), record.get("verification_status")) != (row["id"].value, row["type"].value, row["status"].value):
            raise ValueError("Graph projection disagrees with payload")
        records.append(record)
    # Reject incomplete nodes and projection edits rather than silently losing data.
    if set(store) != mapped(records):
        raise ValueError("Graph contains incomplete or unsupported triples; explicit mapping is required")
    return records


def write_empty(path, records):
    store = Store(path)
    if len(store):
        raise ValueError("Graph destination is not empty")
    store.extend(mapped(records))
    store.flush()


def related(path, entity):
    # Only a fixed local SELECT is exposed; no arbitrary SPARQL/SERVICE execution.
    store = Store.read_only(str(path))
    query = f"SELECT ?id WHERE {{ ?a <{NS}about> {node('entity', entity)} ; <{NS}id> ?id }}"
    return sorted({row["id"].value for row in store.query(query)})
