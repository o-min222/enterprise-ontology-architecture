"""Small UTF-8 message catalogs; language never changes canonical records."""

import json
from pathlib import Path
import re
import sys


CATALOGS = Path(__file__).resolve().parents[1] / "locales"


def messages(language="en"):
    if not isinstance(language, str) or not re.fullmatch(r"[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*", language):
        raise ValueError("Use a language tag such as en, ko, ja, zh, or fr-CA")
    requested = language.lower()
    registry = json.loads((CATALOGS / "manifest.json").read_text(encoding="utf-8"))
    effective = requested.split("-", 1)[0]
    if effective not in registry["locales"]:
        effective = registry["default"]
    catalog = json.loads((CATALOGS / (effective + ".json")).read_text(encoding="utf-8"))
    return {"requested": requested, "messages": effective}, catalog


def announce(language):
    resolution, _ = messages(language)
    if resolution["requested"].split("-", 1)[0] != resolution["messages"]:
        print(f"Tool messages for {language} are unavailable; using {resolution['messages']}. The AI can still respond in {language}.", file=sys.stderr)


def utf8_output():
    # Python on Windows may otherwise use a legacy encoding when redirected.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
