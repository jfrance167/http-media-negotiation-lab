"""Independent frozen reports, finite controls and native admission boundaries."""

import ast
import copy
import json
from pathlib import Path
# Only fixed local interpreter/test commands; no case-derived commands or shell.
import subprocess  # nosec B404
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from medialab import Invalid, evaluate, parse
from medialab import contracts
from medialab import report
from medialab import __main__ as cli

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / "fixtures/cases.json").read_text(encoding="utf-8"))
EXPECTED = json.loads((ROOT / "fixtures/expected.json").read_text(encoding="utf-8"))


def one(index=0):
    return {"version": 1, "cases": [copy.deepcopy(CASES["cases"][index])]}


def child(arguments):
    return subprocess.run([sys.executable, *(["-O"] if not __debug__ else []),
                           "-m", "medialab", *arguments], cwd=ROOT, capture_output=True,
                          timeout=15, check=False)  # nosec B603


def barrier_child(arguments, close_stdout=False, close_stderr=False, dirty=False):
    wrapper = ("import json,sys;from medialab.__main__ import main;sys.stdin.buffer.read(1);"
               + ("sys.stdout.close();sys.stderr.close();" if dirty else "")
               + "raise SystemExit(main(json.loads(sys.argv[1])))")
    process = subprocess.Popen([sys.executable, *(["-O"] if not __debug__ else []),
                                "-c", wrapper, json.dumps(arguments)], cwd=ROOT,
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)  # nosec B603
    try:
        if close_stdout:
            process.stdout.close()
            process.stdout = None
        if close_stderr:
            process.stderr.close()
            process.stderr = None
        stdout, stderr = process.communicate(input=b"x", timeout=15)
        return process.returncode, stdout or b"", stderr or b""
    finally:
        if process.poll() is None:
            process.kill()
            process.wait(timeout=5)
        for stream in (process.stdin, process.stdout, process.stderr):
            if stream is not None:
                stream.close()


class ModelTests(unittest.TestCase):
    def test_frozen_labels(self):
        result = evaluate(parse((ROOT / "fixtures/cases.json").read_bytes()))
        for actual, expected in zip(result["results"], EXPECTED["results"], strict=True):
            with self.subTest(case=actual["id"]):
                self.assertEqual(actual, expected)
        self.assertEqual(result, EXPECTED)
        self.assertEqual(sum(row["status"] == "UNSUPPORTED" for row in result["results"]), 13)

    def test_independent_quality_table(self):
        # 64 hand-table controls: two candidates, exact versus broader matching.
        # The per-candidate oracle is supplied directly, independent of model helpers.
        for wildcard in (0, 1, 500, 1000):
            for exact in (0, 1, 500, 1000):
                for order in (False, True):
                    for policy in ("honor", "ignore"):
                        document = one(16)
                        case = document["cases"][0]
                        case["server_policy"] = policy
                        case["accept"]["ranges"][0]["q"] = f"0.{wildcard:03}" if wildcard < 1000 else "1"
                        case["accept"]["ranges"][1]["q"] = f"0.{exact:03}" if exact < 1000 else "1"
                        if order:
                            case["candidates"].reverse()
                        result = evaluate(document)["results"][0]
                        known = {"html": exact, "json": wildcard}
                        expected_ids = [item["id"] for item in case["candidates"]
                                        if known[item["id"]] == max(exact, wildcard)
                                        and known[item["id"]] != 0]
                        self.assertEqual({row["id"]: row["quality_milli"] for row in result["candidates"]}, known)
                        self.assertEqual(result["best_candidate_ids"], expected_ids)
                        self.assertEqual(result["selected_id"], case["candidates"][0]["id"] if policy == "ignore"
                                         else expected_ids[0] if expected_ids else None)
                        self.assertEqual(result["hypothetical_status"], 200 if policy == "ignore" or expected_ids else 406)

    def test_schema_and_fresh_provenance(self):
        original = copy.deepcopy(CASES)
        report = evaluate(CASES)
        self.assertEqual(CASES, original)
        self.assertEqual(set(report), {"version", "results", "assumptions"})
        for source, result in zip(CASES["cases"], report["results"], strict=True):
            self.assertEqual(set(result), {"id", "status", "reasons", "preference", "candidates",
                                          "best_candidate_ids", "handling", "selected_id",
                                          "hypothetical_status", "declaration"})
            self.assertEqual(result["declaration"], {key: value for key, value in source.items() if key != "id"})
            for row in result["candidates"]:
                self.assertEqual(set(row), {"id", "match", "governing_range_indices", "specificity",
                                           "quality_milli", "acceptable"})
        report["results"][0]["declaration"]["candidates"][0]["type"] = "modified"
        report["assumptions"].clear()
        self.assertEqual(CASES, original)
        self.assertEqual(evaluate(CASES), EXPECTED)

    def test_quality_spellings(self):
        for value, expected in ((None, 1000), ("0", 0), ("0.", 0), ("0.5", 500),
                                ("0.050", 50), ("0.001", 1), ("1", 1000), ("1.", 1000), ("1.000", 1000)):
            document = one(20)
            document["cases"][0]["accept"]["ranges"][0]["q"] = value
            row = evaluate(document)["results"][0]["candidates"][0]
            self.assertEqual(row["quality_milli"], expected)
        for value in (".5", "00", "1.001", "0.0000", "1.0000", "+1", "-0", "1e0", " 1", "1 ", "０.５", 1, True, [], {}):
            document = one(20)
            document["cases"][0]["accept"]["ranges"][0]["q"] = value
            with self.subTest(q=value), self.assertRaises(Invalid):
                evaluate(document)

    def test_whole_validation_before_shortcuts(self):
        for index in (1, 6, 8, 13, 37):
            document = one(index)
            document["cases"][0]["candidates"][0]["unknown"] = "inert"
            with self.subTest(index=index), self.assertRaisesRegex(Invalid, "^SCHEMA$"):
                evaluate(document)
        document = one()
        document["cases"].append(copy.deepcopy(CASES["cases"][7]))
        document["cases"][1]["server_policy"] = []
        with self.assertRaisesRegex(Invalid, "^SERVER_POLICY$"):
            evaluate(document)

    def test_schema_counts_identifiers_and_parameters(self):
        edits = [lambda d: d.update(version=True), lambda d: d.update(cases=[]),
                 lambda d: d["cases"][0].update(id="<inert>"),
                 lambda d: d["cases"][0]["accept"].update(state="unknown", ranges=[{}]),
                 lambda d: d["cases"][0].update(candidates=[]),
                 lambda d: d["cases"][0].update(unsupported_features=["x", "x"]),
                 lambda d: d["cases"][0]["candidates"][0].update(parameters=[{"name":"q", "value":"1"}]),
                 lambda d: d["cases"][0]["candidates"][0].update(parameters=[{"name":"format", "value":"fixed"}, {"name":"FORMAT", "value":"flowed"}]),
                 lambda d: d["cases"][0]["candidates"][0].update(type="*"),
                 lambda d: d["cases"][0]["candidates"][0].update(subtype="*+json")]
        for edit in edits:
            document = one()
            edit(document)
            with self.assertRaises(Invalid):
                evaluate(document)
        document = one()
        document["cases"].append(copy.deepcopy(document["cases"][0]))
        with self.assertRaisesRegex(Invalid, "^DUPLICATE_CASE_ID$"):
            evaluate(document)
        document = one()
        document["cases"][0]["candidates"].append(copy.deepcopy(document["cases"][0]["candidates"][0]))
        with self.assertRaisesRegex(Invalid, "^DUPLICATE_CANDIDATE_ID$"):
            evaluate(document)

    def test_no_native_hooks(self):
        calls = []

        class Meta(type):
            def __eq__(self, other):
                calls.append("meta-eq")
                return False

            def __hash__(self):
                calls.append("meta-hash")
                return 7

        class Exotic(metaclass=Meta):
            def __iter__(self):
                calls.append("iter")
                return iter(())

            def __eq__(self, other):
                calls.append("eq")
                return False

            def __hash__(self):
                calls.append("hash")
                return 7

            def __str__(self):
                calls.append("str")
                return "inert"

        class Text(str):
            def encode(self, *args, **kwargs):
                calls.append("subclass-encode")
                return b"inert"

            def __hash__(self):
                calls.append("subclass-hash")
                return 9

            def __eq__(self, other):
                calls.append("subclass-eq")
                return False

        class Mapping(dict):
            def items(self):
                calls.append("items")
                return ()

        class Sequence(list):
            def __iter__(self):
                calls.append("subclass-iter")
                return iter(())

            def __len__(self):
                calls.append("subclass-len")
                return 0

        values = [Exotic(), Text("x"), Mapping(), Sequence(),
                  type("Number", (int,), {})(1), iter(()), Exotic]
        for value in values:
            for position in ("root", "nested", "key"):
                if position == "root":
                    document = value
                elif position == "nested":
                    document = one()
                    document["cases"][0]["server_policy"] = value
                else:
                    # Builtin container/iterator keys are unhashable; skip only those.
                    if type(value) is Mapping or type(value) is Sequence:
                        continue
                    document = {value: None}
                calls.clear()  # Key construction preceded this API invocation.
                with self.assertRaisesRegex(Invalid, "^TREE_TYPE$"):
                    evaluate(document)
                self.assertEqual(calls, [])
        calls.clear()
        with self.assertRaisesRegex(Invalid, "^INPUT_LIMIT$"):
            parse(Exotic())
        self.assertEqual(calls, [])

    def test_alias_cycle_and_tree_bounds(self):
        document = one()
        shared = document["cases"][0]["candidates"][0]["parameters"]
        document["cases"][0]["candidates"][1]["parameters"] = shared
        self.assertEqual(evaluate(document)["results"][0]["status"], "SUPPORTED")
        cycle = []
        cycle.append(cycle)
        with self.assertRaisesRegex(Invalid, "^TREE_CYCLE$"):
            evaluate(cycle)
        for value in ([0] * 101, [[[[[[[[0]]]]]]]], "x" * 257, {"x" * 65: None}, "\ud800", "\x00", 10**5000):
            with self.assertRaises(Invalid):
                evaluate(value)
        repeated = [list(range(100))] * 100
        with self.assertRaisesRegex(Invalid, "^NODE_LIMIT$"):
            evaluate(repeated)
        with self.assertRaisesRegex(Invalid, "^INPUT_LIMIT$"):
            evaluate([["x" * 256] * 100] * 3)  # Root shape fails only after byte admission.

    def test_maximum_field_cardinality_stress(self):
        document = {"version": 1, "cases": []}
        for index in range(18):
            case = copy.deepcopy(CASES["cases"][25])
            case["id"] = "case" + str(index)
            case["accept"]["ranges"] = [{"type":"t"*32, "subtype":"s"*32,
                                          "parameters":[], "q":None} for _ in range(16)]
            case["candidates"] = [{"id": "id" + str(n) + "x"*60, "type":"t"*32,
                                    "subtype":"s"*32, "parameters":[]} for n in range(8)]
            document["cases"].append(case)
        raw = json.dumps(document, separators=(",", ":")).encode("utf-8")
        evaluated = evaluate(parse(raw))
        payload = report.encode(evaluated)
        with patch.object(report, "OUTPUT_BYTES", 10_000_000):
            markdown_size = len(report.encode(evaluated, "markdown"))
        if markdown_size > contracts.OUTPUT_BYTES:
            with self.assertRaisesRegex(Invalid, "^OUTPUT_LIMIT$"):
                report.encode(evaluated, "markdown")
        else:
            self.assertEqual(len(report.encode(evaluated, "markdown")), markdown_size)
        print("STRESS_RECORD " + json.dumps({"input_bytes":len(raw), "json_bytes":len(payload),
                                           "markdown_bytes":markdown_size, "admitted_cases":18,
                                           "markdown_cap_reachable":markdown_size>contracts.OUTPUT_BYTES,
                                           "maximum_report_proven":False}))

    def test_parser_authority_and_bounds(self):
        self.assertEqual(parse(b'{"x":"[[[[[[[[["}'), {"x":"[[[[[[[[["})
        for raw, code in ((b'{"a":1,"a":2}', "DUPLICATE_KEY"),
                          (b"0.1", "NONINTEGER_JSON"), (b"NaN", "NONINTEGER_JSON"),
                          (b"12345678901", "INTEGER_TOKEN_BOUND"), (b"[" * 9 + b"]" * 9, "JSON_DEPTH"),
                          (b"\xff", "INVALID_JSON"), (b'{"x":"\\q"}', "INVALID_JSON"),
                          (b" " * (contracts.INPUT_BYTES + 1), "INPUT_LIMIT")):
            with self.subTest(code=code), self.assertRaisesRegex(Invalid, "^" + code + "$"):
                parse(raw)

    def test_capability_inventory(self):
        allowed = {"copy", "json", "re", "argparse", "os", "sys"}
        for path in (ROOT / "medialab").glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if type(node) is ast.Import:
                    for alias in node.names:
                        self.assertIn(alias.name.split(".")[0], allowed)
                if type(node) is ast.ImportFrom and node.level == 0:
                    self.assertIn(node.module.split(".")[0], allowed)


class DeliveryTests(unittest.TestCase):
    def test_reports_inert_and_bounded(self):
        evaluated = evaluate(CASES)
        self.assertEqual(json.loads(report.encode(evaluated)), EXPECTED)
        document = one(25)
        document["cases"][0]["accept"]["ranges"][0]["type"] = "image"
        document["cases"][0]["accept"]["ranges"][0]["subtype"] = "`inert|text`"
        encoded = report.encode(evaluate(document), "markdown")
        self.assertNotIn(b"`inert|text`", encoded)
        self.assertIn(b"&#96;", encoded)
        self.assertIn(b"&#124;", encoded)
        self.assertEqual(encoded.count(b"## "), 1)
        with patch.object(report, "OUTPUT_BYTES", 10), self.assertRaisesRegex(Invalid, "^OUTPUT_LIMIT$"):
            report.encode(evaluated)
        with self.assertRaisesRegex(Invalid, "^REPORT_FORMAT$"):
            report.encode(evaluated, "html")

    def test_actual_cli_and_fresh_alias_paths(self):
        result = child(["fixtures/cases.json"])
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout), EXPECTED)
        self.assertEqual(result.stderr, b"")
        with tempfile.TemporaryDirectory(dir=ROOT / "reports") as directory:
            source = Path(directory) / "input.json"
            source.write_text(json.dumps(one(3)), encoding="utf-8")
            target = Path(directory) / "report.json"
            result = child([str(source), "--output", str(target)])
            self.assertEqual(result.returncode, 0)  # Hypothetical406 is a supported result.
            saved = target.read_bytes()
            self.assertEqual(json.loads(saved)["results"][0]["hypothetical_status"], 406)
            result = child([str(source), "--output", str(target)])
            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stdout, b"")
            self.assertEqual(result.stderr, b"medialab: IO_ERROR\n")
            self.assertEqual(target.read_bytes(), saved)
            original = source.read_bytes()
            result = child([str(source), "--output", str(source)])
            self.assertEqual(result.stderr, b"medialab: INPUT_OUTPUT_ALIAS\n")
            self.assertEqual(source.read_bytes(), original)

    def test_actual_empty_output_and_nul(self):
        result = child(["fixtures/cases.json", "--output", ""])
        self.assertEqual((result.returncode, result.stdout, result.stderr),
                         (1, b"", b"medialab: INVALID_OUTPUT_PATH\n"))
        for arguments, code in ((["\x00"], "INVALID_INPUT_PATH"),
                                (["fixtures/cases.json", "--output", "\x00"], "INVALID_OUTPUT_PATH")):
            # NUL is passed through controlled JSON to main, not as impossible OS argv.
            result = barrier_child(arguments)
            self.assertEqual(result, (1, b"", ("medialab: " + code + "\n").encode()))

    def test_actual_process_stream_boundaries(self):
        entries = [
            ("missing-stderr", ["inert-missing.json"], False, True, False, 1),
            ("missing-both", ["inert-missing.json"], True, True, False, 1),
            ("usage-both", ["--format", "inert-private-value"], True, True, False, 2),
            ("empty-input-both", [""], True, True, False, 1),
            ("report-stdout", ["fixtures/cases.json"], True, False, False, 1),
            ("report-both", ["fixtures/cases.json"], True, True, False, 1),
            ("help-alive", ["--help"], False, False, False, 0),
            ("help-stdout", ["--help"], True, False, False, 1),
            ("help-both", ["--help"], True, True, False, 1),
            ("dirty-report", ["fixtures/cases.json"], False, False, True, 1),
            ("dirty-missing", ["inert-missing.json"], False, False, True, 1),
            ("dirty-usage", ["--format", "inert-private-value"], False, False, True, 2),
            ("dirty-help", ["--help"], False, False, True, 1),
        ]
        records = []
        for name, args, close_stdout, close_stderr, dirty, expected in entries:
            with self.subTest(name=name):
                code, stdout, stderr = barrier_child(args, close_stdout, close_stderr, dirty)
                self.assertEqual(code, expected)
                self.assertNotIn(b"Traceback", stderr)
                self.assertNotIn(b"Exception ignored", stderr)
                self.assertNotIn(b"inert-private", stderr)
                if name == "help-alive":
                    self.assertIn(b"usage: medialab", stdout)
                    self.assertLess(len(stdout), 4096)
                else:
                    self.assertEqual(stdout, b"")
                if name in ("report-stdout", "help-stdout"):
                    self.assertEqual(stderr, b"medialab: IO_ERROR\n")
                records.append({"name":name, "kind":"python_stream_close" if dirty else "physical_pipe_barrier",
                                "optimized":not __debug__, "exit_code":code,
                                "stdout_bytes":len(stdout), "stderr_bytes":len(stderr)})
        print("BOUNDARY_RECORDS " + json.dumps(records))

    def test_actual_parse_error_both_closed(self):
        records = []
        with tempfile.TemporaryDirectory(dir=ROOT / "reports") as directory:
            source = Path(directory) / "invalid.json"
            source.write_text('{"version":1,"version":1}', encoding="utf-8")
            for dirty in (False, True):
                code, stdout, stderr = barrier_child([str(source)], not dirty, not dirty, dirty)
                self.assertEqual((code, stdout, stderr), (1, b"", b""))
                records.append({"name":"parse-error-both", "kind":"python_stream_close" if dirty else "physical_pipe_barrier",
                                "optimized":not __debug__, "exit_code":code, "stdout_bytes":0, "stderr_bytes":0})
        print("BOUNDARY_RECORDS " + json.dumps(records))

    def test_actual_invalid_and_argument_diagnostics(self):
        result = child(["--format", "inert-private-value"])
        self.assertEqual((result.returncode, result.stdout, result.stderr),
                         (2, b"", b"medialab: ARGUMENT_ERROR\n"))
        with tempfile.TemporaryDirectory(dir=ROOT / "reports") as directory:
            source = Path(directory) / "invalid.json"
            source.write_text('{"version":1,"version":1}', encoding="utf-8")
            result = child([str(source)])
            self.assertEqual((result.returncode, result.stdout, result.stderr),
                             (1, b"", b"medialab: DUPLICATE_KEY\n"))

    def test_checked_stdout_and_diagnostics_seams(self):
        # Labeled dirty-sink seams, separate from actual child process evidence.
        for mode in ("short", "bool", "write", "flush"):
            class Sink:
                @property
                def buffer(self):
                    return self

                def write(self, payload):
                    if mode == "write":
                        raise OSError("inert-native-text")
                    return 0 if mode == "short" else True if mode == "bool" else len(payload)

                def flush(self):
                    if mode == "flush":
                        raise ValueError("inert-native-text")

                def fileno(self):
                    raise ValueError("unusable")

            sink = Sink()
            with patch.object(cli.sys, "stdout", SimpleNamespace(buffer=sink)), patch.object(cli.sys, "stderr", sink), \
                    patch.object(cli.os, "open", side_effect=OSError("unavailable")):
                self.assertEqual(cli.main(["fixtures/cases.json"]), 1)
                self.assertIsNone(cli.sys.stdout)
                self.assertIsNone(cli.sys.stderr)
            for args, expected in ((["inert-missing.json"], 1), (["--format", "invalid"], 2)):
                with patch.object(cli.sys, "stderr", sink), patch.object(cli.os, "open", side_effect=OSError("unavailable")):
                    self.assertEqual(cli.main(args), expected)
                    self.assertIsNone(cli.sys.stderr)

    def test_checked_help_and_redirection_seams(self):
        sink = SimpleNamespace(write=lambda payload: 0, flush=lambda: None)
        errors = []
        diagnostic = SimpleNamespace(buffer=SimpleNamespace(write=lambda text: errors.append(text) or len(text), flush=lambda: None))
        with patch.object(cli.sys, "stdout", SimpleNamespace(buffer=sink)), patch.object(cli.sys, "stderr", diagnostic), \
                patch.object(cli.os, "open", side_effect=OSError("unavailable")):
            self.assertEqual(cli.main(["--help"]), 1)
            self.assertEqual(errors, [b"medialab: STDOUT_WRITE_AND_SILENCE_FAILED\n"])
        stream = SimpleNamespace(fileno=lambda: 1)
        with patch.object(cli.sys, "stdout", stream), patch.object(cli.os, "open", return_value=99), \
                patch.object(cli.os, "dup2"), patch.object(cli.os, "close", side_effect=OSError("close failed")):
            self.assertFalse(cli._silence_failed_stream(stream))
            self.assertIsNone(cli.sys.stdout)

    def test_fresh_short_flush_close_cleanup_seams(self):
        for mode in ("short", "bool", "flush", "close"):
            class Stream:
                def __enter__(self):
                    return self

                def __exit__(self, *args):
                    if mode == "close":
                        raise OSError("close failed")

                def write(self, payload):
                    return 0 if mode == "short" else True if mode == "bool" else len(payload)

                def flush(self):
                    if mode == "flush":
                        raise ValueError("closed")

            with patch("builtins.open", return_value=Stream()), patch.object(report.os, "unlink") as cleanup:
                with self.assertRaises((OSError, ValueError)):
                    report.write_fresh("owned-new-file", b"x")
                cleanup.assert_called_once_with("owned-new-file")
            with patch("builtins.open", return_value=Stream()), patch.object(report.os, "unlink", side_effect=OSError("cleanup failed")):
                with self.assertRaisesRegex(Invalid, "^OUTPUT_WRITE_AND_CLEANUP_FAILED$"):
                    report.write_fresh("owned-new-file", b"x")


if __name__ == "__main__":
    unittest.main()
