# Verification — October 5, 2026

Windows CPython 3.13.7. The completed command was:

```powershell
python tools/verify.py --output reports/verification-reviewed
```

It exited 0: 11 checks passed and model restoration was true. Use a fresh output directory to repeat. Bandit 1.9.4 was already available in the verification environment; the application has no runtime dependencies and the verifier does not install tools.

| Check | Observed result |
| --- | --- |
| Unit suite, normal / optimized / restored | 20 tests passed in each mode |
| Full independent frozen reports | 40 matched: 27 supported, 13 unsupported |
| Independent finite quality controls | 64 two-candidate table cases |
| Quality before specificity mutant | 9 assertion failures |
| Zero made eligible mutant | 13 assertion failures |
| Omit format tier mutant | 7 assertion failures |
| Tier breaks quality tie mutant | 7 assertion failures |
| Exact model source restoration | True |
| Compilation | Passed |
| Bandit | Zero findings, zero errors |
| JSON / Markdown demos | 40 rows each; expected exit 2; 51,694 / 134,670 bytes |

All four mutants failed through assertions rather than test errors. There are five explanatory nosec comments in trusted test/verifier subprocess scaffolding, none in the application.

[Final receipt](reports/verification-reviewed/results.json) includes commands, exits and ten source/test/tool/fixture/contract SHA-256 hashes. Current hashes were independently recomputed and matched. [Boundary records](reports/verification-reviewed/cli-boundary.json) contain 30 actual process records across normal and optimized Python: 20 physical-pipe-barrier records (including live controls) and ten closed-Python-stream records. Short/bool writes, dirty-buffer flush, open/close/cleanup and reduced report caps are separately labeled controlled seams. NUL paths use a controlled call to main, because OS argv cannot contain NUL. Empty output was tested through the actual module entry point.

[Stress evidence](reports/verification-reviewed/stress.json) records the admitted 60,367-byte, 18-case input in both modes. JSON was 191,828 bytes; measured Markdown was 628,849 bytes and rejected by the ordinary 524,288-byte cap. An enlarged cap was used only to measure size. This does not establish a maximum report bound.

Original red runs and the first failed verifier remain in reports/stage2-red.*, reports/stage3-first.* and reports/verification/. The original pre-code freeze is in research/freeze-v1/; [correction record](research/FREEZE-CORRECTION.md) explains the post-code container-depth clarification. The current freeze binds the clarified contract. Both fixture files remain byte-identical to their originals.

Limits: synthetic normalized declarations, trusted local host, Windows and this runtime only. No actual HTTP/raw parser/server/browser behavior, upstream execution, hosted CI, production security assurance, independent review or secret-history certification was verified.
