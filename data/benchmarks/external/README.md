# External Math Benchmarks

Downloaded: 2026-05-20

This directory contains local copies of public mathematics benchmarks used to
exercise AMRA across easy arithmetic reasoning, contest problem solving,
natural-language proof reconstruction, Lean proof generation, and IMO-level
answer/proof/grading evaluation.

The downloaded raw files are intentionally kept under `raw/` and are not yet
normalized into AMRA problem-bank YAML. Use `suite.json` as the source manifest
for future importers.

## Coverage

| Benchmark | Local path | Main use | Difficulty band | Format |
| --- | --- | --- | --- | --- |
| GSM8K | `raw/gsm8k` | Grade-school arithmetic reasoning with natural-language solutions | Easy | JSONL |
| MATH | `raw/math` | Competition math with step-by-step natural-language solutions | Medium to hard | Parquet |
| IMO Bench | `raw/imo_bench` | IMO-style answer prediction, proof writing, and proof grading | Pre-IMO to IMO-hard | CSV |
| miniF2F Lean 3 | `raw/miniF2F_lean3` | Lean theorem-proving targets over olympiad-style problems | Medium to olympiad | Lean |
| miniF2F Lean 4 | `raw/miniF2F_lean4` | Lean 4 theorem-proving targets with natural-language docstrings | Medium to olympiad | Lean 4 |
| ProofNet | `raw/proofnet` | Undergraduate theorem statements with informal proofs and Lean statements | Undergraduate proof | JSONL, Lean, TeX |
| ProofNet Lean 4 | `raw/proofnet_lean4` | Lean 4 version of ProofNet formalization targets | Undergraduate proof | JSONL, Lean 4, TeX |

## Counts

| Benchmark | Count summary |
| --- | --- |
| GSM8K | 7,473 train and 1,319 test examples, plus Socratic variants and example model solutions |
| MATH | 12,500 problems across Algebra, Counting and Probability, Geometry, Intermediate Algebra, Number Theory, Prealgebra, and Precalculus |
| IMO Bench | 400 AnswerBench v2 short-answer problems, 60 ProofBench proof-writing problems, and 1,000 GradingBench human grading records |
| miniF2F Lean 3 | 244 validation and 244 test theorem targets |
| miniF2F Lean 4 | 256 validation and 244 test theorem targets |
| ProofNet | 185 validation and 186 test records |
| ProofNet Lean 4 | 374 records |

## Notes

- Lean benchmark files commonly contain `sorry` placeholders. These are proof
  targets, not completed proofs. AMRA success should mean replacing the target
  `sorry` with a kernel-checked proof under a fixed import policy.
- ProofNet records include natural-language statements and proofs paired with
  formal Lean statements. They are useful for informal-to-formal routing and
  proof-plan evaluation.
- MATH is copied from the Hugging Face dataset referenced by the official MATH
  GitHub repository; the GitHub repository itself contains loader and evaluation
  code, not the primary problem corpus.
- IMO Bench is copied from Google DeepMind's `superhuman` repository. Upstream
  marks `answerbench.csv` as deprecated and recommends `answerbench_v2.csv`.
- PDF duplicates from ProofNet were excluded because equivalent TeX and JSONL
  sources are present.

## Source Manifest

See `suite.json` for source URLs, pinned revisions, licenses, and local file
paths.
