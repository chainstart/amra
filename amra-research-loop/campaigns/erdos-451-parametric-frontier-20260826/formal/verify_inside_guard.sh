#!/usr/bin/env bash
set -euo pipefail

here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
logs="$here/logs"
mkdir -p "$logs"

"$here/materialize_upstream.sh"

cd "$here"
lake update
lake exe cache get

/usr/bin/time -v lake build ErdosProblem451 2>&1 | tee "$logs/upstream-build.log"
/usr/bin/time -v lake env lean FrontierLemmas.lean 2>&1 | tee "$logs/frontier-build.log"
/usr/bin/time -v lake build ParametricInterface 2>&1 | tee "$logs/interface-build.log"
/usr/bin/time -v lake build ParametricRanges 2>&1 | tee "$logs/ranges-build.log"

grep -Fq "'large_asym_of_margins' depends on axioms: [propext, Classical.choice, Quot.sound]" \
  "$logs/frontier-build.log"
grep -Fq "'erdos451_bhp_frontier' depends on axioms: [bhp, propext, Classical.choice, Quot.sound]" \
  "$logs/frontier-build.log"
if grep -Fq 'sorryAx' "$logs/frontier-build.log"; then
  printf 'frontier axiom audit failed: sorryAx found\n' >&2
  exit 1
fi
grep -Fq "'parametric_frontier_interface' depends on axioms: [propext, Classical.choice, Quot.sound]" \
  "$logs/interface-build.log"
grep -Fq "'erdos451_bhp_frontier_via_interface' depends on axioms: [bhp, propext, Classical.choice, Quot.sound]" \
  "$logs/interface-build.log"
if grep -Fq 'sorryAx' "$logs/interface-build.log"; then
  printf 'parametric interface axiom audit failed: sorryAx found\n' >&2
  exit 1
fi

check_standard_axioms() {
  python3 - "$1" "$2" <<'PY'
import re
import sys

path, theorem = sys.argv[1:]
with open(path, encoding="utf-8") as handle:
    output = re.sub(r"\s+", " ", handle.read())
expected = (
    f"'{theorem}' depends on axioms: "
    "[propext, Classical.choice, Quot.sound]"
)
if expected not in output:
    raise SystemExit(f"axiom audit failed for {theorem}")
PY
}

for theorem in \
  ParametricSmall.case_small \
  ParametricMed.case_medium \
  ParametricML.case_mediumlarge \
  ParametricLarge.large_card_raw_at \
  ParametricLarge.large_asym_of_margins_at \
  ParametricLarge.hasLargeMarginCertificateAt_of_parameters \
  ParametricLarge.case_large_of_margin_certificate_at \
  ParametricLarge.parametricRangeBuilder_complete \
  ParametricLarge.parametric_frontier_complete \
  ParametricLarge.sharpAddExp_lt_theta_iff \
  ParametricLarge.balancedFourRangeParameters_iff \
  ParametricLarge.balancedFourRange_no_go_low \
  ParametricLarge.balancedFourRange_no_go_high \
  ParametricLarge.large_card_raw_adaptive_at \
  ParametricLarge.adaptiveFrontierParameters_of_wide \
  ParametricLarge.adaptiveFrontierParameters_iff \
  ParametricLarge.adaptiveLogV_le_logU \
  ParametricLarge.adaptive_log_selection_budget \
  ParametricLarge.adaptiveLambdaAt_pow \
  ParametricLarge.adaptiveLambdaAt_ge_one \
  ParametricLarge.adaptive_mass_mul_lambda_pow \
  ParametricLarge.locationBlind_first_two_log_invariant \
  ParametricLarge.locationBlind_first_two_invariant_ge_delta_of_W_ge_one \
  ParametricLarge.locationBlind_termwise_block_budget_obstruction \
  ParametricLarge.adaptive_first_two_log_invariant \
  ParametricLarge.adaptive_first_two_budget_obstruction \
  ParametricLarge.locationBlind_endpoint_excess_budget \
  ParametricLarge.locationBlind_endpoint_termwise_no_go_of_excess \
  ParametricLarge.locationBlindTermwiseLeadingCertificate_iff \
  ParametricLarge.locationBlindTermwiseLeadingCertificate_no_go \
  ParametricLarge.locationBlindTermwiseLeadingCertificate_no_go_bhp \
  ParametricLarge.adaptive_actual_selection_budget \
  ParametricLarge.exists_min_adaptive_stopping_order \
  ParametricLarge.adaptive_preceding_failure_log_lower \
  ParametricLarge.adaptive_additive_term_eventual \
  ParametricLarge.adaptiveT3At_eventual \
  ParametricLarge.large_card_raw_adaptive_selected_at \
  ParametricLarge.adaptive_bad_set_asymptotic_of_budgets \
  ParametricLarge.r0Param_eventual_adaptive_admissible_at \
  ParametricLarge.adaptive_small_orders_fail_eventual \
  ParametricLarge.r0Param_eventual_adaptive_bounds_at \
  ParametricLarge.adaptiveAnalyticParameters_of_wide \
  ParametricLarge.hasAdaptiveLargeCertificateAt_of_parameters \
  ParametricLarge.case_large_adaptive_at \
  ParametricLarge.adaptiveRangePackage_of_parameters \
  ParametricLarge.parametricRangeBuilder_adaptive \
  ParametricLarge.parametric_frontier_adaptive \
  ParametricLarge.adaptive_parameter_certificate_wide \
  ParametricLarge.parametricRangeBuilder_wide \
  ParametricLarge.parametric_frontier_wide
do
  check_standard_axioms "$logs/ranges-build.log" "$theorem"
done
if grep -Fq 'sorryAx' "$logs/ranges-build.log"; then
  printf 'parametric ranges axiom audit failed: sorryAx found\n' >&2
  exit 1
fi

sha256sum ErdosProblem451.lean FrontierLemmas.lean ParametricInterface.lean \
  ParametricRanges.lean \
  lakefile.toml lake-manifest.json \
  lean-toolchain upstream.sha256 > "$logs/final-sha256.txt"
