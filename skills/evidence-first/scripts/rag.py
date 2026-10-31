"""Local lexical RAG: build an index and return cited context to the calling AI.

No model API or embedding service is contacted. The calling AI performs grounded
generation using the returned records and their verification/provenance metadata.
"""

import argparse
from contextlib import closing
from datetime import datetime, timezone
import json
import os
import re
import sqlite3
import uuid

import workspace
from localization import announce, messages, utf8_output


INDEX = ".evidence-first/rag.sqlite3"
INDEX_VERSION = "2"


def tokens(text):
    values = []
    for word in re.findall(r"[^\W_]+", text.casefold()):
        values.append(word)
        for part in re.findall(r"[가-힣\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]{2,}", word):
            values.extend(part[i:i + 2] for i in range(len(part) - 1))
    return values


def source(root):
    config = workspace.load_config(root)
    if "rag" not in config.get("enabled_features", []):
        raise ValueError("Enable the rag feature first")
    store = config["primary_store"]
    records = workspace.read_store(root, store)
    return store, records, workspace.digest(records)


def build(root):
    with workspace.writer(root):
        store, records, fingerprint = source(root)
        path = workspace.path_at(root, INDEX)
        temporary = path.with_name(f"rag-{uuid.uuid4().hex}.tmp")
        metadata = {"index_version": INDEX_VERSION, "source_store": store, "source_digest": fingerprint,
                    "built_at": datetime.now(timezone.utc).isoformat()}
        try:
            with closing(sqlite3.connect(temporary)) as connection, connection:
                connection.execute("CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
                connection.executemany("INSERT INTO metadata VALUES (?, ?)", metadata.items())
                connection.execute("CREATE VIRTUAL TABLE chunks USING fts5(assertion_id UNINDEXED, terms, payload UNINDEXED)")
                for record in records:
                    text = str(record.get("statement", "")) + " " + " ".join(record.get("entity_ids", []))
                    connection.execute("INSERT INTO chunks VALUES (?, ?, ?)",
                                       (record["id"], " ".join(tokens(text)), workspace.encoded(record)))
            current_store, _, current_digest = source(root)
            if (current_store, current_digest) != (store, fingerprint):
                raise ValueError("Source changed during indexing; existing index retained")
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)
        return dict(metadata, records=len(records), indexed=True)


def retrieve(root, question, limit=5, language="en", search_query=None):
    resolution, text = messages(language)
    if not isinstance(question, str) or not question.strip() or len(question) > 4000 or not 1 <= limit <= 20:
        raise ValueError("Use a nonempty question of at most 4000 characters and a limit from 1 to 20")
    store, current_records, fingerprint = source(root)
    current_by_id = {record["id"]: record for record in current_records}
    path = workspace.path_at(root, INDEX)
    if not path.is_file():
        raise ValueError("No RAG index; build it first")
    if search_query is not None and (not isinstance(search_query, str) or not search_query.strip() or len(search_query) > 4000):
        raise ValueError("Use a nonempty search query of at most 4000 characters")
    query_tokens = list(dict.fromkeys(tokens(question if search_query is None else search_query)))[:32]
    with closing(sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)) as connection:
        metadata = dict(connection.execute("SELECT key, value FROM metadata"))
        if (metadata.get("index_version"), metadata.get("source_store"), metadata.get("source_digest")) != (INDEX_VERSION, store, fingerprint):
            raise ValueError("RAG index is stale or from another store; rebuild it")
        # Tokens are quoted and the whole MATCH expression is a bound parameter.
        match = " OR ".join('"' + token + '"' for token in query_tokens)
        rows = connection.execute(
            "SELECT assertion_id, payload, bm25(chunks) FROM chunks WHERE chunks MATCH ? ORDER BY bm25(chunks), assertion_id LIMIT ?",
            (match, limit),
        ).fetchall() if match else []
    evidence = []
    for number, (identity, payload, rank) in enumerate(rows, 1):
        record = json.loads(payload)
        if not isinstance(record, dict) or record.get("id") != identity or current_by_id.get(identity) != record:
            raise ValueError("RAG indexed payload disagrees with its source; rebuild it")
        evidence.append({"citation_id": f"E{number}", "assertion_id": identity, "rank": rank, "record": record})
    return {"question": question, "retrieval_method": "local_fts5_bm25", "source_store": store,
            "language": resolution, "search_query": question if search_query is None else search_query,
            "query_was_rewritten": search_query is not None and search_query != question,
            "source_digest": fingerprint, "built_at": metadata["built_at"], "query_tokens": query_tokens,
            "evidence_is_untrusted_data": True, "originals_accessed_by_retriever": False,
            "evidence": evidence,
            "generation_rules": text["generation_rules"]}


def main():
    utf8_output()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--lang", default="en", help="Requested answer/message language tag")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("build")
    search = commands.add_parser("retrieve")
    search.add_argument("--question", required=True)
    search.add_argument("--limit", type=int, default=5)
    search.add_argument("--search-query", help="Optional source-language keywords; preserves the original question")
    args = parser.parse_args()
    try:
        announce(args.lang)
        result = build(args.root) if args.command == "build" else retrieve(args.root, args.question, args.limit, args.lang, args.search_query)
        print(workspace.encoded(result), end="")
    except (ValueError, OSError, sqlite3.Error) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
