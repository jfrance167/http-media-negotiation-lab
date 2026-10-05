"""Declared media preference calculation, separate from invented server selection."""

import copy

from .contracts import quality, validate

ASSUMPTIONS = (
    "Offline declared media preferences only; no actual headers, representations or HTTP responses.",
    "Parameters are explicit text/plain format declarations; no implicit defaults or body processing.",
    "Duplicate-quality ambiguity and honor/ignore/first-offer selection are lab policies, not universal server behavior.",
)


def _parameters(item):
    return {parameter["name"].lower(): parameter["value"].lower()
            for parameter in item["parameters"]}


def _supported(item):
    if not item["parameters"]:
        return True
    return (item["type"].lower() == "text" and item["subtype"].lower() == "plain"
            and all(parameter["name"].lower() == "format"
                    and parameter["value"].lower() in ("fixed", "flowed")
                    for parameter in item["parameters"]))


def _tier(item):
    if item["type"] == "*":
        return 0
    if item["subtype"] == "*":
        return 1
    return 3 if item["parameters"] else 2


def _matches(item, candidate):
    if item["type"] != "*" and item["type"].lower() != candidate["type"].lower():
        return False
    if item["subtype"] != "*" and item["subtype"].lower() != candidate["subtype"].lower():
        return False
    parameters = _parameters(candidate)
    return all(parameters.get(name) == value for name, value in _parameters(item).items())


def _row(candidate, state, ranges):
    row = {"id": candidate["id"], "match": "UNMATCHED", "governing_range_indices": [],
           "specificity": None, "quality_milli": 0, "acceptable": False}
    if state == "unknown":
        row.update(match="UNKNOWN_CONTEXT", quality_milli=None, acceptable=None)
    elif state == "absent":
        row.update(match="ABSENT_DEFAULT", quality_milli=1000, acceptable=True)
    else:
        indices = [index for index, item in enumerate(ranges) if _matches(item, candidate)]
        if indices:
            tier = max(_tier(ranges[index]) for index in indices)
            governing = [index for index in indices if _tier(ranges[index]) == tier]
            qualities = {quality(ranges[index]["q"]) for index in governing}
            row.update(governing_range_indices=governing, specificity=tier)
            if len(qualities) != 1:
                row.update(match="AMBIGUOUS_QUALITY", quality_milli=None, acceptable=None)
            else:
                q = next(iter(qualities))
                row.update(match="MATCHED", quality_milli=q, acceptable=q > 0)
    return row


def _case(case):
    ranges, candidates = case["accept"]["ranges"], case["candidates"]
    reasons = []
    if case["unsupported_features"]:
        reasons.append("UNSUPPORTED_FEATURE")
    if case["accept"]["state"] == "unknown":
        reasons.append("UNKNOWN_ACCEPT")
    if any(not _supported(item) for item in ranges + candidates):
        reasons.append("UNSUPPORTED_PARAMETER_CONTEXT")
    rows = [_row(candidate, "unknown" if reasons else case["accept"]["state"], ranges)
            for candidate in candidates]
    result = {"id": case["id"], "status": "UNSUPPORTED", "reasons": sorted(reasons),
              "preference": "UNKNOWN", "candidates": rows, "best_candidate_ids": None,
              "handling": "UNSUPPORTED_CONTEXT", "selected_id": None,
              "hypothetical_status": None,
              "declaration": {key: copy.deepcopy(value) for key, value in case.items() if key != "id"}}
    if reasons:
        return result
    if any(row["match"] == "AMBIGUOUS_QUALITY" for row in rows):
        result.update(reasons=["AMBIGUOUS_QUALITY"], handling="UNSUPPORTED_AMBIGUOUS_QUALITY")
        return result
    eligible = [row for row in rows if row["quality_milli"] > 0]
    maximum = max((row["quality_milli"] for row in eligible), default=0)
    best = [row["id"] for row in eligible if row["quality_milli"] == maximum]
    result["best_candidate_ids"] = best
    result["preference"] = "NONE" if not best else "UNIQUE_BEST" if len(best) == 1 else "TIED_BEST"
    policy = case["server_policy"]
    if policy == "unknown":
        result.update(reasons=["UNKNOWN_SERVER_POLICY"], handling="UNSUPPORTED_SERVER_POLICY")
    elif policy == "ignore":
        result.update(status="SUPPORTED", handling="IGNORE_PREFERENCES",
                      selected_id=candidates[0]["id"], hypothetical_status=200)
    elif best:
        result.update(status="SUPPORTED", handling="ASSUMED_SELECT", selected_id=best[0],
                      hypothetical_status=200)
    else:
        result.update(status="SUPPORTED", handling="ASSUMED_REJECT", hypothetical_status=406)
    return result


def evaluate(document):
    """Validate all supplied metadata and return fresh, complete explanatory records.

    Unknown context and lab ambiguity never establish actual representation usability.
    """
    validate(document)
    return {"version": 1, "results": [_case(case) for case in document["cases"]],
            "assumptions": list(ASSUMPTIONS)}
