# HTTP media negotiation research — October 5, 2026

Research/planning only, assigned at coordinator SUCCESSORS.md 04:18 under Jake's
verified successor mandate. Sole writer: existing chat01a10a38-51f7-78a0-be08-65aefc676c4c.
No application code, new repository, package installation or upstream execution.
Evidence: research/source-records.json preserves connected GitHub responses, including
failed guessed license paths; research/worker-review.md records actual local drafting.

## Reuse and learning gap

Read selected vault Home.md/Codex Integration.md and the range research milestone.
Narrow searches of relevant HTTP/CORS project and research notes found no dedicated
media-negotiation implementation. Existing cache PLAN/README explicitly defer content
negotiation and only support synthetic x-variant Vary matching. Precondition and range
labs calculate different supplied metadata; they do not choose media representations.
This is evidence from these searches, not an exhaustive workspace/vault claim.

Parent tracked .gitignore/install_weekly_cron.sh/nmap_scan_report.py edits remain outside
scope. Existing root/range/cache/precondition graphify-out/graph.json files were absent;
no graph indexing, installation, refresh, scanning of unrelated/private/GLPI material.
Read range contracts.py and its corrected __main__.py, test-boundary design and MIT
notice. Reuse reviewed strict JSON/tree/whole-validation, escaping, exclusive output,
checked help/diagnostics and fixed-command verification patterns after approval, with
fresh model-specific tests. Preserve all earlier projects and original/failure receipts.

## Primary sources and consequences

- [RFC9110 §12.5.1](https://httpwg.org/specs/rfc9110.html#field.accept): media ranges,
  wildcard and applicable-parameter precedence; highest-precedence matching range sets
  each candidate's quality. Comparing candidates is a subsequent step.
- [§12.4.2](https://httpwg.org/specs/rfc9110.html#quality.values): default quality1,
  zero exclusion, decimal grammar with at most three fractional digits. Use exact
  thousandths, not floating point or permissive decimal coercion.
- [§12.4.1](https://httpwg.org/specs/rfc9110.html#absence) and
  [§12.1](https://httpwg.org/specs/rfc9110.html#proactive.negotiation): absent preferences
  and server discretion. A highest-preference candidate does not force a real response.
- [§8.3.1](https://httpwg.org/specs/rfc9110.html#media.type) and
  [§5.6.6](https://httpwg.org/specs/rfc9110.html#parameter): type/subtype/name comparisons
  are case-insensitive; value semantics depend on the parameter. Do not lowercase all
  arbitrary parameter values or claim registry validation.
- [RFC3676 §4](https://www.rfc-editor.org/rfc/rfc3676.html#section-4): text/plain Format
  names and Fixed/Flowed values are case-insensitive. This supports the chosen two-value
  profile; body processing, defaults, DelSp and other parameter semantics remain excluded.

[Verified erratum7138](https://www.rfc-editor.org/errata/eid7138) corrects RFC9110 table5's
text/html;level=3 row from0.7 to0.3. Official RFC Editor search results exposed verified
status/date November9,2022 and corrected row; direct erratum-page opens returned internal
errors. Do not silently copy the uncorrected table or claim the page body was fetched.
Record this source-access limit. That unsupported level parameter is a research warning,
not a supported fixture. Independent examples will avoid inheriting its bad expectation.

## Connected GitHub candidate comparison

Repository search for Python HTTP content negotiation returned mimerender, two small
recent repositories and negotiator2. These were discovery results only, not inspected
or certified. Stronger established reference candidates were inspected below. Stars
were not used as quality evidence. No candidate was installed/run or adopted.

### Werkzeug — useful maintained framework, larger than the learning profile

[Repository](https://github.com/pallets/werkzeug), inspected accept.py at commit
594452f6a4fe4de38a544962fbf04bfc9d37fbc2; reported blob3bf3316bb1453c47866b02e7e65eaa135ad18f83.
Read full Accept/MIMEAccept implementation, relevant TestAccept/TestMIMEAccept cases
from tests/test_datastructures.py, parser excerpt in http.py, LICENSE.txt, pyproject.toml,
tests.yaml and recent commit metadata. Other files used dated default-branch snapshots,
not a whole immutable checkout. Source responses retain file/blob provenance.

Accept sorts by specificity then quality; MIME matching lowercases strings and compares
sorted parameter lists for exact subtype matches. from_header treats falsey input as
empty, defaults quality and ignores invalid-quality items. best_match excludes zero,
compares candidate quality then specificity and selects the first candidate on remaining
ties. Those are concrete implementation policies, not this proposed lab's universal
oracle. Tests cover wildcard, q=0, ordering, specificity and level parameters. A plain
exact range's parameter-list equality differs from the lab's declared parameter-subset
matching; do not import it invisibly. Broadly lowering arbitrary parameter values is
unsuitable for asserting general registry semantics; this is a fit observation, not a
validated security vulnerability.

Inspected main manifest: Werkzeug3.2.0.dev, Python>=3.11, MarkupSafe>=3.0.3 runtime;
optional watchdog>=6, flit build and separate test/docs/typing groups. Identity links
match the Pallets repository. Latest inspected head dated October1,2026; defined CI
includes Python3.11–3.15,3.14t,PyPy and Windows/macOS/Linux with full action SHA pins and
checkout persist-credentials:false. No CI run/release/advisory/Scorecard safety claim.
[Issue1686](https://github.com/pallets/werkzeug/issues/1686), closed January16,2020,
documents ordering history; Accept's current versionchanged note/test supports retained
order. It is an historical language-order report, not evidence of a current MIME defect.
Full BSD3 license read: retain copyright/conditions/disclaimer for copied code, reproduce
notice for binary redistribution, no endorsement. No upstream code/vectors will be copied.

### WebOb — closer explanatory API, legacy compatibility policies remain

[Repository](https://github.com/Pylons/webob), acceptparse.py inspected at commit
c0d70f985ff6f04dcc59822ca5216cfd0ada666c. Read AcceptValidHeader.acceptable_offers and
quality, AcceptNoHeader and invalid/no-header handling, parser definitions; selected
actual tests/test_acceptparse.py lines1–220 and900–1080, setup.py, ci-tests.yml and
docs/license.txt (the actual MIT notice, after two failed guessed root license paths).
Raw full parser was fetched, but review focused on these media-accept portions; no claim
that all language/encoding/legacy code was audited.

acceptable_offers assigns per-offer specificity, distinguishes unparameterized ranges,
filters zero after precedence, orders by quality and original offer order. Repeated
equal-specificity ranges take the first occurrence. Deprecated quality explicitly warns
that its old maximum-quality behavior does not implement specificity/parameter matching.
Tests include valid empty headers, malformed raw syntax, absent/invalid constructions,
parameter/case examples and older RFC7231 quality tables. Do not substitute its legacy
API for the proposed model or borrow old tables without standards review. Parser handles
older extension syntax that RFC9110 removed; a normalized profile avoids this extra work.

Main manifest WebOb2.0.0dev0 Python>=3.9, legacy-cgi>=2.6 on Python>=3.13; setuptools build,
pytest/coverage/xdist and docs extras. Latest inspected head August3,2026. Defined CI has
Python3.10–3.14/PyPy on Windows/macOS/Linux and lint/docs/coverage, but mutable action
version tags; no evidence those runs currently pass. Full MIT text read: copyright and
permission notice retained for substantial copying. [Issue403](https://github.com/Pylons/webob/issues/403)
closed August14,2019 records user-reported Accept parameter compatibility changes; its
reported statuses were not reproduced, and are not classified as a present vulnerability.
No package/wheel identity, dependency advisories, complete security scan or Scorecard
was verified. Those missing indicators do not establish insecurity.

## Recommendation and alternatives

Build an original bounded standard-library model after approval. Framework helpers add
raw parsing, compatibility and implicit tie/unknown policies while obscuring the teaching
distinction. Forking creates unnecessary maintenance/license/dependency obligations for
this small offline model. Reference both implementations as design evidence; copy neither.
Stdlib JSON plus exact builtins/integer thousandths suffice for the stated interface;
few dependencies alone do not prove security. Reuse Jake's reviewed MIT boundary patterns.

Prefer normalized type/subtype/parameter/quality fields over a raw Accept parser. Raw
parsing adds field combination, list empties, quote/escape/whitespace, invalid recovery,
parameter ordering and old-extension rules; that materially enlarges scope and test burden.
Restrict supported parameters to declared text/plain format=fixed/flowed, preserving
explicit absence and original spelling. No implicit parameter injection or body/default
interpretation. Unknown parameter semantics and conflicting top-precedence qualities
produce unsupported/unknown results rather than invented best-match answers.

Worker: local qwen3.5:2b extracted three supplied reminders; Codex checked all. EACCES
and app-approved loopback retry preserved; no remote draft or paid call, Laya schema
irrelevant. Tier3 security/scope judgment and independent oracle design stay with Codex.
Next: concrete PLAN review by coordinator before any project code. No new chat, subagent,
scheduler, reply loop, repo, service, real HTTP/headers/data, external action or spending.
