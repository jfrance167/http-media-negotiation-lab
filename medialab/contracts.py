"""Strict bounded input admission, adapted from Jake's MIT range lab.

Native types are checked by identity before any caller-controlled operation.
"""

import json
import re

INPUT_BYTES = 65_536
OUTPUT_BYTES = 524_288
TOKEN = re.compile(r"[!#$%&'+.^_`|~0-9A-Za-z-]+", re.ASCII)
IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", re.ASCII)
FEATURE = re.compile(r"[a-z][a-z0-9-]{0,31}", re.ASCII)
QUALITY = re.compile(r"0(?:\.[0-9]{0,3})?|1(?:\.0{0,3})?", re.ASCII)


class Invalid(ValueError):
    """An invalid document or failed delivery, with a fixed diagnostic code."""


def text(value, limit=256):
    if type(value) is not str or len(value) > limit:
        raise Invalid("TEXT_TYPE_OR_LIMIT")
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise Invalid("TEXT_CONTROL")
    try:
        value.encode("utf-8", "strict")
    except UnicodeError as exc:
        raise Invalid("INVALID_UNICODE") from exc


def _walk(value, depth, budget, active):
    kind = type(value)
    # Equality against a tuple/set of types can itself invoke exotic metaclasses.
    if not (kind is dict or kind is list or kind is str or kind is int
            or kind is bool or value is None):
        raise Invalid("TREE_TYPE")
    budget[0] += 1
    if budget[0] > 5_000:
        raise Invalid("NODE_LIMIT")
    if (kind is dict or kind is list) and depth > 8:
        raise Invalid("TREE_DEPTH")
    if kind is str:
        text(value)
    elif kind is int:
        if value < -9_999_999_999 or value > 9_999_999_999:
            raise Invalid("INTEGER_TOKEN_BOUND")
    elif kind is dict or kind is list:
        if id(value) in active:
            raise Invalid("TREE_CYCLE")
        if len(value) > 100:
            raise Invalid("CONTAINER_LIMIT")
        active.add(id(value))
        try:
            if kind is dict:
                for key, item in value.items():
                    if type(key) is not str:
                        raise Invalid("TREE_TYPE")
                    budget[0] += 1
                    if budget[0] > 5_000:
                        raise Invalid("NODE_LIMIT")
                    text(key, 64)
                    _walk(item, depth + 1, budget, active)
            else:
                for item in value:
                    _walk(item, depth + 1, budget, active)
        finally:
            active.remove(id(value))


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Invalid("DUPLICATE_KEY")
        result[key] = value
    return result


def _integer(source):
    if len(source.lstrip("-")) > 10:
        raise Invalid("INTEGER_TOKEN_BOUND")
    return int(source)


def _noninteger(_source):
    raise Invalid("NONINTEGER_JSON")


def parse(raw):
    """Parse bounded UTF8 JSON bytes; evaluate performs full native/schema admission."""
    if type(raw) is not bytes or len(raw) > INPUT_BYTES:
        raise Invalid("INPUT_LIMIT")
    try:
        source = raw.decode("utf-8", "strict")
        quoted = escaped = False
        depth = 0
        for char in source:
            if quoted:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    quoted = False
            elif char == '"':
                quoted = True
            elif char in "[{":
                depth += 1
                if depth > 8:
                    raise Invalid("JSON_DEPTH")
            elif char in "]}":
                depth -= 1
        return json.loads(source, object_pairs_hook=_pairs, parse_int=_integer,
                          parse_float=_noninteger, parse_constant=_noninteger)
    except (UnicodeError, ValueError, RecursionError) as exc:
        if type(exc) is Invalid:
            raise
        raise Invalid("INVALID_JSON") from exc


def _keys(value, fields):
    if type(value) is not dict or set(value) != set(fields):
        raise Invalid("SCHEMA")


def _list(value, lower, upper, code):
    if type(value) is not list or not lower <= len(value) <= upper:
        raise Invalid(code)


def _choice(value, choices, code):
    if type(value) is not str or value not in choices:
        raise Invalid(code)


def _token(value, code):
    text(value, 32)
    if not TOKEN.fullmatch(value):
        raise Invalid(code)


def _id(value):
    text(value, 64)
    if not IDENTIFIER.fullmatch(value):
        raise Invalid("ID_FORMAT")


def quality(value):
    """Convert an admitted decimal spelling to exact thousandths, with no rounding."""
    if value is None:
        return 1000
    if type(value) is not str or not QUALITY.fullmatch(value):
        raise Invalid("QVALUE")
    whole, _, fraction = value.partition(".")
    return int(whole) * 1000 + int((fraction + "000")[:3])


def _parameters(parameters):
    _list(parameters, 0, 4, "PARAMETER_COUNT")
    seen = set()
    for parameter in parameters:
        _keys(parameter, ("name", "value"))
        _token(parameter["name"], "PARAMETER_NAME")
        _token(parameter["value"], "PARAMETER_VALUE")
        name = parameter["name"].lower()
        if name == "q":
            raise Invalid("RESERVED_PARAMETER")
        if name in seen:
            raise Invalid("DUPLICATE_PARAMETER")
        seen.add(name)


def _media(item, is_range):
    for field, code in (("type", "TYPE_TOKEN"), ("subtype", "SUBTYPE_TOKEN")):
        if is_range and item[field] == "*":
            continue
        _token(item[field], code)
    if item["type"] == "*" and item["subtype"] != "*":
        raise Invalid("WILDCARD_SHAPE")
    _parameters(item["parameters"])


def validate(document):
    """Admit the complete exact-builtin document before any case's semantic shortcut."""
    _walk(document, 1, [0], set())
    if len(json.dumps(document, ensure_ascii=False, separators=(",", ":")).encode("utf-8")) > INPUT_BYTES:
        raise Invalid("INPUT_LIMIT")
    _keys(document, ("version", "cases"))
    if type(document["version"]) is not int or document["version"] != 1:
        raise Invalid("VERSION")
    _list(document["cases"], 1, 40, "CASE_COUNT")
    case_ids = set()
    for case in document["cases"]:
        _keys(case, ("id", "accept", "candidates", "server_policy", "unsupported_features"))
        _id(case["id"])
        if case["id"] in case_ids:
            raise Invalid("DUPLICATE_CASE_ID")
        case_ids.add(case["id"])
        accept = case["accept"]
        _keys(accept, ("state", "ranges"))
        _choice(accept["state"], ("absent", "present", "unknown"), "ACCEPT_STATE")
        _list(accept["ranges"], 0, 16, "RANGE_COUNT")
        if accept["state"] != "present" and accept["ranges"]:
            raise Invalid("ACCEPT_SHAPE")
        for item in accept["ranges"]:
            _keys(item, ("type", "subtype", "parameters", "q"))
            _media(item, True)
            quality(item["q"])
        _list(case["candidates"], 1, 8, "CANDIDATE_COUNT")
        ids = set()
        for item in case["candidates"]:
            _keys(item, ("id", "type", "subtype", "parameters"))
            _id(item["id"])
            if item["id"] in ids:
                raise Invalid("DUPLICATE_CANDIDATE_ID")
            ids.add(item["id"])
            _media(item, False)
        _choice(case["server_policy"], ("honor", "ignore", "unknown"), "SERVER_POLICY")
        features = case["unsupported_features"]
        _list(features, 0, 8, "FEATURE_COUNT")
        seen = set()
        for feature in features:
            text(feature, 32)
            if not FEATURE.fullmatch(feature):
                raise Invalid("FEATURE")
            if feature in seen:
                raise Invalid("DUPLICATE_FEATURE")
            seen.add(feature)
