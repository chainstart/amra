# AMRA Math Tools Report

- Schema: `amra.math_tools_report.v1`
- Profile: `full`
- Install missing tools: `True`
- Smoke checks: `False`
- All selected available: `True`

## Tools

### Python math stack (`python_math_stack`)

- Available: `True`
- Purpose: Finite search, symbolic checks, numerical sanity checks, graph probes, and counterexample search.
- Missing executables: `<none>`
- Missing Python modules: `<none>`
- Command templates:
  - `python3 $AMRA_AGENT_RUN_DIR/experiments/<experiment>.py`
  - `python3 - <<'PY'
import sympy as sp
# finite or symbolic check
PY`
- Notes:
  - Computation is route evidence unless converted into a checked certificate or Lean proof.

### Z3 (`z3`)

- Available: `True`
- Purpose: Bounded model checks and SMT sanity checks for arithmetic, ordering, graph, and incidence constraints.
- Missing executables: `<none>`
- Missing Python modules: `<none>`
- Command templates:
  - `python3 - <<'PY'
from z3 import *
# bounded model check
PY`
  - `z3 <problem>.smt2`
- Notes:
  - Keep encodings explicit; a SAT/UNSAT result only applies to the encoded finite model.

### Lean 4 / lake / mathlib (`lean4`)

- Available: `True`
- Purpose: Final trusted formal verification and small theorem-shape probes.
- Missing executables: `<none>`
- Missing Python modules: `<none>`
- Command templates:
  - `cd $AMRA_AGENT_WORKSPACE && lake build`
  - `cd $AMRA_AGENT_WORKSPACE && lake env lean $AMRA_AGENT_RUN_DIR/lean_probes/<probe>.lean`
  - `rg -n '<keyword>' .lake/packages/mathlib/Mathlib`
- Notes:
  - AMRA accepts formal completion only after Lean builds without sorry/admit/axiom/constant/opaque.

### PARI/GP (`pari_gp`)

- Available: `True`
- Purpose: Fast number-theory experiments, modular arithmetic, algebraic number checks, and sequence probes.
- Missing executables: `<none>`
- Missing Python modules: `<none>`
- Command templates:
  - `gp -q <script.gp>`
- Notes:
  - Use for candidate generation; certify final facts separately.

### GAP (`gap`)

- Available: `True`
- Purpose: Group theory, finite algebra, combinatorics, and exact discrete computations.
- Missing executables: `<none>`
- Missing Python modules: `<none>`
- Command templates:
  - `gap -q <script.g>`

### Singular (`singular`)

- Available: `True`
- Purpose: Polynomial ideals, Groebner bases, and computational commutative algebra.
- Missing executables: `<none>`
- Missing Python modules: `<none>`
- Command templates:
  - `Singular -q <script.sing>`

### Maxima (`maxima`)

- Available: `True`
- Purpose: Classical symbolic algebra and calculus sanity checks.
- Missing executables: `<none>`
- Missing Python modules: `<none>`
- Command templates:
  - `maxima --batch=<script.mac>`

### cvc5 (`cvc5`)

- Available: `True`
- Purpose: SMT solving complementary to Z3, especially for quantified or arithmetic encodings.
- Missing executables: `<none>`
- Missing Python modules: `<none>`
- Command templates:
  - `cvc5 <problem>.smt2`

### SageMath (`sagemath`)

- Available: `True`
- Purpose: Broad CAS environment for number theory, algebra, combinatorics, and exact computation.
- Missing executables: `<none>`
- Missing Python modules: `<none>`
- Command templates:
  - `sage <script.sage>`
  - `sage -python <script.py>`
- Notes:
  - Large package; full-profile installation can take substantial disk and time.

### Coq / Rocq compatibility (`coq`)

- Available: `True`
- Purpose: External proof assistant experiments when a source theorem already exists in Coq/Rocq.
- Missing executables: `<none>`
- Missing Python modules: `<none>`
- Command templates:
  - `coqc <file.v>`
- Notes:
  - AMRA does not currently translate Coq proofs into Lean automatically.

## Agent Guidance

- Use these tools before committing to a long proof route when a finite search, SMT encoding, CAS check, or Lean probe can falsify the plan quickly.
- Treat CAS/SMT/Python output as evidence or certificate material, not as final proof unless translated into a checked Lean artifact.
- Record every nontrivial tool check in `experiments.jsonl`, `lean_probe_log.md`, or the run-specific proof notes.
