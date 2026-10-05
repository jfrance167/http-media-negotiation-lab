# HTTP media negotiation lab — approved Tier3 plan

October5,2026. RESEARCH/PLAN ONLY authorized at coordinator SUCCESSORS.md 04:18;
Coordinator approved stages 1–4 at 04:39, recorded in STATE before code. Existing
chat01a10a38-51f7-78a0-be08-65aefc676c4c is sole writer. Local implementation and
verification are complete; VERIFICATION.md records outcomes. This PLAN remains the
authorized design, with the original proposal below retained. Cutoff October6
08:00 Eastern. Preserve parent/shared/previous work, original evidence and GLPI exclusion.

## Problem and success criteria

Explain supplied media preferences without confusing a range's specificity with quality
or an assumed server decision with actual behavior. Distinct from prior HTTP caching,
preconditions and byte ranges. Deliver a reusable Python API and offline local CLI over
invented normalized metadata, with inert JSON/Markdown explanations, after approval.

Success means exact decimal/zero handling; explicit absent versus empty versus unknown;
most-specific per-candidate quality; declared parameter/case matching; honest ambiguity;
all equal-best candidates retained separately from an explicit server tie policy; complete
validation before output; independent pre-code expected records and assertion-detected
mutations; checked help/diagnostics and bounded fresh delivery; documentation/security/
MIT/AI disclosure, focused ECC review and durable vault evidence. No claim of actual
client decoding capability, registry validity, HTTP server conformance or security access.

## Architecture and alternatives

Original stdlib application: medialab/contracts.py validates bytes/tree/schema and exact
decimal quality; model.py calculates preference and separate assumed selection; report.py
creates bounded escaped JSON/Markdown and fresh output; __init__.py exposes parse/evaluate;
__main__.py owns checked CLI delivery. No HTTP, MIME, email or framework parser, network,
callbacks, codecs, subprocesses in application modules or arbitrary execution.

Reuse reviewed strict admission/report/CLI patterns from Jake's MIT range lab, with
explicit attribution and changed-model regression tests. Reuse existing verifier patterns
only after reviewing their fixed commands and restoration behavior. No parent Git edits,
new repo, installs, branch/stage/commit/push/PR/hosted CI. Separate local directory only.

Adopting/forking Werkzeug/WebOb is unnecessary for this scope and imports differing raw
parsing, duplicate/tie/compatibility policies. Raw Accept parsing is an alternate future
project requiring a new concrete plan; it adds list combination, quoted strings, recovery,
parameter ordering and extension syntax. Parameter-free modeling is smaller but misses
the useful specificity lesson. Support only text/plain's declared format=fixed/flowed,
with RFC3676 case-insensitive values; explicitly exclude general registry semantics.

## Proposed exact input contract

Stage1 freezes this proposal and complete independent expectations BEFORE app code.
All fields required; no coercion, truncation or unknown keys. Exact built-in types only.
Root: version exact int1; cases list1..40. Each case exactly:
id, accept, candidates, server_policy, unsupported_features.
ID: visible ASCII [A-Za-z0-9][A-Za-z0-9._-]{0,63}, unique within cases/candidates as relevant.
server_policy: exact honor, ignore or unknown. unsupported_features: list0..8 unique
lowercase [a-z][a-z0-9-]{0,31}; any entry marks the whole case unsupported after validation.

accept exactly {state,ranges}; state absent/present/unknown. ranges list0..16, required
empty for absent or unknown; present with empty ranges is a known empty preference set.
No actual/raw header strings. Each range exactly {type,subtype,parameters,q}; each
candidate exactly {id,type,subtype,parameters}; candidates list1..8, concrete types only.
Type/subtype: ASCII HTTP token spelling1..32, with '*' reserved to entire range fields:
*/*, type/*, type/subtype. Reject */subtype, candidate wildcards and embedded '*'
under this narrower normalized contract. Type/subtype comparisons are case-insensitive;
preserve supplied spelling. Structured suffixes such as application/problem+json are
literal concrete subtypes; no application/*+json wildcard or suffix equivalence.

parameters: list0..4 exact {name,value} pairs. Name/value ASCII token1..32 excluding '*';
name comparisons case-insensitive, duplicate normalized names invalid, reserved q name
invalid (quality has its own field). Preserve order/spelling. Values fixed/flowed match
case-insensitively only for name format on exact text/plain. Unknown names/values, format
on other types or on wildcard ranges are valid-shaped UNSUPPORTED_PARAMETER_CONTEXT.
No charset/DelSp/quoted-string/extension/unknown-registry/default-value normalization.
An empty parameter list means no declared parameter; do not synthesize format=fixed or
claim default body processing. This calculates supplied declaration matching only.

q: exact null (omitted weight, default1000) or exact ASCII decimal string matching
0[.0..3digits] or1[.0..3zeroes]. Accept 0,0.,0.5,0.050,1,1.,1.000; reject .5,00,1.001,
negative/sign/exponent/whitespace, Unicode digits and fourth decimals. Parse integer
thousandths0..1000 by digits, never float/Decimal inference or rounding. Preserve spelling
and null distinction. JSON numeric qualities/booleans are invalid, not unsupported.

Whole document gates: at most65,536 UTF8 bytes input; container depth<=8 (root1), aggregate tree
nodes<=5000 counting keys, each container<=100, scalar strings<=256/key<=64, no C0/DEL
or lone surrogates, cycles/custom containers/generators rejected before methods/coercion.
Repeated acyclic aliases permitted, counted at every occurrence; results are fresh copies.
Byte CLI admission and lexical quote/escape-aware depth gate precede stdlib json.loads;
stdlib remains JSON syntax authority. Reject duplicate keys, floats/constants and integer
tokens over10 decimal digits; version is the only semantic integer input. API compact
UTF8 re-encoding measures admission, not universal canonical JSON. All bounds apply to
API too, before semantic ignore/unknown short-circuits. Final output<=524,288 encoded
bytes measured before delivery; tree/cardinality limits need not be simultaneously reachable.

## Preference computation and unknowns

1. Validate every field in every case first. A malformed late field fails the document,
   including under unknown Accept, ignored preferences or unsupported parameters/features.
2. Features, unknown Accept or parameter-context gaps are global case scope reasons,
   sorted/deduplicated; candidate quality/acceptability are null, preference UNKNOWN,
   best IDs null and assumed selection/status null. No partial mathematical certainty.
3. Absent Accept: each candidate quality1000, match ABSENT_DEFAULT, no governing indices
   or specificity. Present empty ranges: every candidate UNMATCHED, quality0, acceptable
   false. No matching range in nonempty preferences has the same0 result with distinct
   retained input provenance. Zero is known exclusion, never null.
4. Known present ranges match type/subtype wildcards and require each declared range
   parameter to be present/equivalent in the candidate. Supported parameter specificity
   tiers: exact type/subtype+format3; exact unparameterized2; type/*1; */*0. Unparameterized
   exact ranges can match parameterized candidates. Select maximum tier BEFORE quality.
5. Retain every matching index at that maximum tier. Equal integer qualities there give
   one known quality, including0; repeated equal ranges preserve all governing indices.
   Conflicting qualities at equal maximum tier yield AMBIGUOUS_QUALITY for that candidate;
   other candidate mathematics stays known, but global preference/best/selection/status
   are unknown and case unsupported. No first/last/max-quality duplicate resolution.
6. With all candidate qualities known, acceptable iff quality>0. best_candidate_ids is
   every positive candidate at the maximum quality, original candidate order. Preference
   UNIQUE_BEST/TIED_BEST/NONE. Do not rank equal-quality different candidates by their
   range specificity; that is a separate possible server policy, excluded here.

For known preferences: honor selects the first ID in best IDs (explicit invented server
tie policy), hypothetical200; if NONE, selected null and hypothetical406 (lab policy).
ignore selects first offered candidate regardless of quality, hypothetical200, records
IGNORE_PREFERENCES. unknown preserves candidate/preference math but yields
UNSUPPORTED_SERVER_POLICY with null selection/status. Unsupported context/ambiguity
takes priority over every policy, including ignore. No actual response/header/body emitted.
Known rejection under honor is a supported teaching result, not an interface failure.

Proposed exact report root {version,results,assumptions}; each result {id,status,reasons,
preference,candidates,best_candidate_ids,handling,selected_id,hypothetical_status,declaration}.
Each candidate row {id,match,governing_range_indices,specificity,quality_milli,acceptable}.
Match enums MATCHED/UNMATCHED/ABSENT_DEFAULT/UNKNOWN_CONTEXT/AMBIGUOUS_QUALITY;
indices are zero-based and always a list; specificity0..3 or null, quality0..1000 or null,
acceptable bool or null. Ambiguous rows retain governing tier/indices, unknown context
rows have empty indices/null tier. Declaration is a fresh complete case sans id; assumptions
state scope/server choices. Status SUPPORTED unless a defined unsupported reason occurs.
Handling ASSUMED_SELECT/ASSUMED_REJECT/IGNORE_PREFERENCES/UNSUPPORTED_CONTEXT/
UNSUPPORTED_AMBIGUOUS_QUALITY/UNSUPPORTED_SERVER_POLICY; reasons include
UNSUPPORTED_FEATURE,UNKNOWN_ACCEPT,UNSUPPORTED_PARAMETER_CONTEXT,AMBIGUOUS_QUALITY,
UNKNOWN_SERVER_POLICY. No additional successful certainty from known policy alone.

## Threat model and delivery contract

Attacker controls synthetic JSON/API objects. Protect bounded evaluation, truthful results,
report inertness and fresh output; threats are malformed hidden fields, type/number confusion,
deep/large/cyclic inputs, wrong precedence/zero/decimal interpretation and report injection.
Mitigate with exact validation, integer math, explicit unsupported gates and escaped reports.
Host filesystem paths/process/interpreter/standard descriptors are trusted; this is no
resource sandbox, hostile path-race defense, credential redactor or real representation
authorization mechanism. No content sniffing, codecs, object loading or remote workers.

CLI input is a trusted selected local file, bounded read+1. Output exclusively fresh,
reject aliases/existing files; explicit empty or NUL paths fail before access. Semantic
failure emits no partial result; stdout delivery remains nontransactional. Exact write-count,
flush/close and cleanup failures use fixed codes without raw argument/path/native exception
text. Checked help, fixed argument errors and one checked diagnostic attempt; failed streams
redirect/detach to avoid shutdown retries in tested Windows boundaries. No diagnostic fallback.
Exit0 all supported reports (including hypothetical406); exit2 valid report with unsupported
cases; exit1 invalid/input/output/delivery error; fixed argument misuse exit2, help0 only after
successful checked delivery. Stderr failure must not replace the selected exit. General host
process failures stay outside guarantees. Output-byte bounds are tested via an honest seam.

## Independent examples and verification design

Freeze at least40 separately calculated scenario records with FULL expected result fields
before application code, with input/expected/contract hashes. Never derive answers by running
the model. Include at least these justified controls:

| Supplied preferences / candidates | Independent expectation |
|---|---|
| absent / HTML, JSON | both1000, TIED_BEST; honor chooses first by lab policy |
| present empty / HTML |0, NONE; honor hypothetical406, ignore first hypothetical200 |
| */*=1, HTML=0 / HTML, JSON |HTML0 tier2; JSON1000 tier0; JSON uniquely best |
| text/*=.9, HTML=.2 / HTML, plain |HTML200 tier2; plain900 tier1; plain best |
| plain=.7, plain format=flowed default / plain flowed, plain fixed |flowed1000 tier3; fixed700 tier2 |
| plain format=fixed=.4 / plain with no format |unmatched0; no implicit parameter injection |
| HTML=.333, JSON=.334 / HTML, JSON |333 versus334, JSON best; exact thousandths |
| HTML=0, HTML=1 / HTML |conflicting top tier, unknown/unsupported; no fabricated winner |
| repeated HTML=.5 / HTML |500, both governing indices, no ambiguity |
| HTML=.5, */*=.5 / HTML, JSON |both500 equal best; range tiers do not rank candidates |
| differently cased TEXT/PLAIN, FORMAT=FLOWED |case-equivalent comparisons; provenance retained |
| unknown/unsupported parameter on otherwise ignored case |unknown context takes priority |

Table shorthand .9/.2 means0.9/0.2 in the actual contract, not admitted leading-dot syntax.
Add q spelling/default equivalence, no-match/zero distinction, wildcard/fixed/flowed mismatch,
literal +json, duplicate normalized parameter names, candidate/Accept order permutations,
unknown policy retaining math, ignored known q0, late-invalid global gate and bounds.
Do not use the erroneous RFC table5 last row or a library's output as an unquestioned oracle.
Finite independent table oracle over invented types/subtypes, quality set{0,1,500,1000}
and four tiers; pre-fix expected comparisons without calling model helper logic. Preserve
input immutability and alias/cycle cases. Full-schema/null/governing-provenance checks.

Normal and optimized unittest plus real normal/-O CLI children. Deterministic stdin-barrier
tests close stdout, stderr or both BEFORE evaluation: valid reports, parse/path/argument
errors and help. Include empty --output, controlled NUL-path main wrapper (OS argv cannot
contain NUL), short writes/flush/close/cleanup, no native-text disclosure and fixed exits.
No tests of real origins, headers, bodies, browsers, network or framework/server execution.
Four focused mutants: quality before specificity, q0 made acceptable, missed format-tier
precedence, candidate tier used to break equal-quality preference. Each must cause a
specific assertion failure, not merely an exception/nonzero exit, followed by exact source
restoration and passing affected/full suite. Add duplicate-conflict control if a fourth
mutation would otherwise fail only through coupled behavior; freeze targets in stage1.

## Sequential stages and approval checkpoints

1. Freeze exact contract,>=40 full independent oracles, source/fixture receipts and numerical
   edge explanation. Done: manual oracle review, immutable saved hashes before app code;
   retain any later correction transparently with originals. Files<=5: CONTRACT, two fixture
   documents, receipt and explanation. Dependency: coordinator approval of this plan.
2. Implement admission and model slice plus public API/tests. Done: exact gates, all complete
   oracle rows and independent table cases pass normal/-O, immutable inputs and no forbidden
   capabilities. Files<=5 initially; checkpoint before delivery work. Dependency: stage1.
3. Implement report/CLI slice, expand tests and reviewed fixed-command verifier. Done: bounded
   escaped full provenance and all checked delivery/exits, actual process barriers normal/-O,
   fresh paths and no native leak. Files<=5 in this slice. Dependency: stage2 checkpoint.
4. Mutation/restoration, available compile/Bandit checks and ECC actual-change review/fixes;
   final evidence, README/SECURITY/MIT/AI/DECISIONS/LEARNING and vault closeout in small
   documentation batches. Done: all required checks pass, raw evidence/hashes honest and
   coordinator/manual gates explicitly pending. Dependency: stage3. No hosted baseline
   configuration without new-repo/publication scope; assess applicable local checks only.

Standing completion bar: actual runtime results, regression controls and precise limits,
source/test/doc consistency, scoped security review, reusable API usage/assumptions and
discoverable README, preserved unrelated work, verified milestone notes. Tests alone do
not make implementation complete. Manual review/publication/merge/deploy remain separate.

## Risks, worker choice and remaining decisions

Wrong specificity/zero/duplicate policies: high educational impact, frozen independent
controls plus isolated mutations. Parameter-default overclaim: narrow declared matching,
no implicit processing; retain unsupported reasons. Input/output failure: bounded strict
admission, checked every delivery channel and actual process tests. Scope creep: no raw
parser/framework/HTTP integration without a new plan. No universal safe-media conclusion.

Local Ollama reminders accepted after Codex RFC verification; first EACCES plus approved
loopback retry retained. No need for remote OmniRoute/OpenRouter draft or readiness probe.
Laya tested schemas unsuitable. Complex planning/security/oracle judgments are Codex work.
No new services/model downloads/provider changes/spending. Optional learning check after
implementation: explain how an exact q0 range can override a broader q1 range while a
server can still disregard the preference. No teaching pause blocks authorized stages.

Remaining approval: coordinator reviews this concrete plan and authorizes named stages.
Recommended choices are normalized profile, ambiguity instead of duplicate resolution,
all equal-best preferences plus first-offer honor policy and declaration-only parameters.
Until approval, retain this research/plan only; no application/test/verifier code.

## Coordinator04:39 approval addendum (recorded before code)

Stages1–4 approved under Jake's directly verified coordinator mandate, SUCCESSORS.md
04:39. Freeze>=40 full independent reports plus exact status/error precedence before
application code. Identity-only type checks BEFORE equality/hashing/iteration/serialization;
native custom-metaclass/key/subclass no-hook controls, cycles and repeated aliases.
Normal/-O actual help/usage/report/error closed/both-failed streams and distinctly labeled
dirty-stream/output-cap seams. Four distinct assertion mutants/restoration, current hashes,
ECC/SAST/docs/vault; original/failure/oracle-correction evidence preserved. Duplicate
ambiguity and server choice remain explicit incomplete-profile/lab policy. No raw parser,
implicit defaults/body processing, live HTTP, new repo/install/publication. Sole writer/no
reply loops/chats/subagents/schedulers and previous/manual/source-access limits unchanged.
