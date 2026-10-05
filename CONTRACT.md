# Frozen contract v1 — before application code, October5,2026

PLAN input/report/algorithm/bounds remain authoritative with the following exact closure.
No implementation-generated expectations. fixtures/cases.json and expected.json hold
40 full hand-specified reports; research/fixture-freeze.json binds their pre-code bytes.
Corrections require originals and an explicit chronology, never silent label replacement.

## Schema and precedence closure

Exact fields/types/bounds/ASCII grammars in PLAN. Quality grammar is fullmatch
`0(?:\.[0-9]{0,3})?|1(?:\.0{0,3})?`, default null=1000. ASCII HTTP tchar tokens minus
asterisk; whole '*' allowed only in range type/subtype. q media parameter forbidden.
Parameter name/value duplicates: names case-insensitive; no interpretation of unknown
values even if RFC3676 defines processing fallback. Strict declaration-only matching.

Parse precedence: exact bytes/65,536 cap; strict UTF8 (invalid => INVALID_JSON); lexical
depth>8 => JSON_DEPTH; stdlib JSON syntax/hooks. During loads first hook error retained
(duplicate/numeric), other syntax/Unicode/value/recursion errors => INVALID_JSON.
No promise that hooks diagnose every invalid-JSON string in a universal semantic order.

Native evaluate first walks exact builtin tree by identity checks before operations.
Root depth1; every object/list/scalar occurrence and key counts toward5000 nodes; reject
custom scalar/container/key/class/metaclass identities before equality/hash/iteration/
serialization. Builtin null/bool/int/str/list/dict only in the generic walk; semantic
schema rejects inappropriate primitives. No more than100 items/container; key<=64,
scalar string<=256, no C0/DEL/surrogates, depth<=8, active-identity cycles rejected,
acyclic repeated aliases counted again. Depth counts nested containers only, matching
the lexical JSON nesting gate; scalar leaves do not add a container depth. Re-encode compact ensure_ascii:false UTF8
before schema to enforce byte cap, without claiming canonical JSON. No float input.

Semantic validation order: root exact keys/version/case count; cases in order: exact
keys, ID/duplicate, accept exact keys/state/range count/state-empty shape, each range
keys/type/subtype/wildcard/parameters/q, candidate count, each candidate keys/ID/duplicate/
type/subtype/wildcard/parameters, server_policy, feature count/name/duplicate. All cases
validated before any evaluation. Parameter records exact keys/name/value/reserved name/
case-insensitive duplicate; after this, valid-shaped unsupported meanings are context
facts, not malformed input. Schema errors use SCHEMA, not supplied field names.

Case global reasons collected together: UNSUPPORTED_FEATURE, UNKNOWN_ACCEPT,
UNSUPPORTED_PARAMETER_CONTEXT. Sort/deduplicate. If any, every candidate UNKNOWN_CONTEXT,
indices[], specificity/quality/acceptable null; preference UNKNOWN/best IDs null,
handling UNSUPPORTED_CONTEXT/selected/status null. Unknown server policy is not reached.

Otherwise each candidate gets known absence/matching math as PLAN. No match: quality0,
acceptable false, indices[], tier null. Absent:1000/true, indices[], tier null. Matched:
max tier0..3, all governing indices in supplied range order, known unique integer quality,
acceptable iff quality>0. Conflicting max-tier qualities: AMBIGUOUS_QUALITY, retain max
tier/indices; quality/acceptable null. Lower-tier conflicts are irrelevant. Any ambiguous
candidate yields sole reason AMBIGUOUS_QUALITY, UNKNOWN preference/best null,
UNSUPPORTED_AMBIGUOUS_QUALITY handling/selected/status null, preserving all candidate
rows' independent math. Unknown server policy is not reached here either.

All known candidate math: positive maximum defines all best IDs in original candidate
order; UNIQUE_BEST/TIED_BEST/NONE, best[] for NONE. honor => ASSUMED_SELECT first best200
or ASSUMED_REJECT selected null406. ignore => IGNORE_PREFERENCES first offered200 even
under NONE. unknown => sole UNKNOWN_SERVER_POLICY, UNSUPPORTED_SERVER_POLICY handling,
selected/status null while math and preference remain. Every no-reason case SUPPORTED;
otherwise UNSUPPORTED. Hypothetical numbers never represent emitted HTTP responses.

Exact report root and row fields are in PLAN; declaration is the complete fresh case
without id. Candidate rows retain IDs; assumptions exact fixed strings, in this order:
1. Offline declared media preferences only; no actual headers, representations or HTTP responses.
2. Parameters are explicit text/plain format declarations; no implicit defaults or body processing.
3. Duplicate-quality ambiguity and honor/ignore/first-offer selection are lab policies, not universal server behavior.

## Diagnostics and exits

Validation raises Invalid with one fixed code; no caller/native text. Walker codes:
TREE_TYPE,TREE_CYCLE,NODE_LIMIT,TREE_DEPTH,CONTAINER_LIMIT,TEXT_TYPE_OR_LIMIT,TEXT_CONTROL,
INVALID_UNICODE. Syntax codes: INPUT_LIMIT,INVALID_JSON,JSON_DEPTH,DUPLICATE_KEY,
INTEGER_TOKEN_BOUND,NONINTEGER_JSON. Schema codes: SCHEMA,VERSION,CASE_COUNT,ID_FORMAT,
DUPLICATE_CASE_ID,DUPLICATE_CANDIDATE_ID,ACCEPT_STATE,ACCEPT_SHAPE,RANGE_COUNT,
CANDIDATE_COUNT,PARAMETER_COUNT,PARAMETER_NAME,PARAMETER_VALUE,DUPLICATE_PARAMETER,
RESERVED_PARAMETER,TYPE_TOKEN,SUBTYPE_TOKEN,WILDCARD_SHAPE,QVALUE,SERVER_POLICY,
FEATURE_COUNT,FEATURE,DUPLICATE_FEATURE.

CLI parse fixed ARGUMENT_ERROR =>2; successfully delivered help=>0. Then explicit empty/
NUL input=>INVALID_INPUT_PATH, explicit empty/NUL output=>INVALID_OUTPUT_PATH; path alias
=>INPUT_OUTPUT_ALIAS. Input/read before evaluation/report; no result delivery if invalid.
Invalid code =>1, other handled OS/ValueError =>IO_ERROR/1; encode unknown format
REPORT_FORMAT and cap OUTPUT_LIMIT. Fresh-file failure cleans only own newly created
file; cleanup failure OUTPUT_WRITE_AND_CLEANUP_FAILED/1. Stdout exact byte-write/flush
failure redirects failed stream; redirection failure detaches stream and returns
STDOUT_WRITE_AND_SILENCE_FAILED/1, otherwise IO_ERROR/1. Diagnostics one checked fixed
text write/flush attempt; stderr failure cannot change chosen exit. No second-channel
fallback. General host/process failure remains outside guarantee.

Successful delivery:0 iff all cases SUPPORTED;2 iff any UNSUPPORTED. Hypothetical406
alone is supported. Every diagnostic exactly `medialab: CODE\n`, fixed prog medialab,
no usage/raw values/native paths on argument errors. Stdout nontransactional; existing
files never replaced. Report encoder accepts evaluated records only, not public raw APIs.

## Four frozen assertion mutation targets

M1: choose governing tier by quality rather than specificity (specificity-before-quality
case must assert wrong exact quality/governing index). M2: change quality>0 to>=0 when
building best candidates (q0 expected NONE/406 asserts). M3: assign format tier2 instead
of3 (parameter-tier expected1000 and index asserts). M4: filter equal-best candidates by
their governing specificity (equal-quality-tier-tie expected both IDs asserts). Isolated
mutation suites require actual frozen-label assertion failures, not a mere crash/nonzero.
Restore exact original model bytes after each, rerun clean suite and bind current hashes.
