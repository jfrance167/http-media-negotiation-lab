"""Bounded inert reports and exclusive output; adapted from Jake's MIT range lab."""

import json
import os

from .contracts import Invalid, OUTPUT_BYTES


def _entities(value):
    return "".join(f"&#{ord(char)};" for char in value)


def encode(report, format_name="json"):
    """Encode evaluated records only; raw untrusted input belongs in evaluate."""
    if format_name == "json":
        source = json.dumps(report, ensure_ascii=True, indent=2) + "\n"
    elif format_name == "markdown":
        lines = ["# Offline media preference and assumed server choice", "",
                 "Declared metadata only; no representation or HTTP response action.", ""]
        for result in report["results"]:
            lines.extend(["## " + _entities(result["id"]), "", "| Field | Value |", "|---|---|"])
            for key, value in result.items():
                if key == "id":
                    continue
                kind = type(value)
                value = json.dumps(value, ensure_ascii=True) if kind is list or kind is dict else str(value)
                lines.append("| " + key + " | " + _entities(value) + " |")
            lines.append("")
        lines.extend(["Assumptions:", ""] + ["- " + _entities(item) for item in report["assumptions"]])
        source = "\n".join(lines) + "\n"
    else:
        raise Invalid("REPORT_FORMAT")
    payload = source.encode("utf-8", "strict")
    if len(payload) > OUTPUT_BYTES:
        raise Invalid("OUTPUT_LIMIT")
    return payload


def write_fresh(path, payload):
    """Create exclusively; cleanup owns only the file created by this call.

    CLI paths are trusted. No hostile filesystem-race or durability guarantee.
    """
    stream = open(path, "xb")
    try:
        with stream:
            written = stream.write(payload)
            if type(written) is not int or written != len(payload):
                raise OSError("SHORT_WRITE")
            stream.flush()
    except (OSError, ValueError):
        try:
            os.unlink(path)
        except OSError as exc:
            raise Invalid("OUTPUT_WRITE_AND_CLEANUP_FAILED") from exc
        raise
