"""Regression for the independent square/chord sumset certificate."""

from fractions import Fraction
import random
import subprocess
from pathlib import Path

from verify_sumset_expansion import sumset_audit


SCRIPT = Path(__file__).with_name("verify_sumset_expansion.py")


def test_exact_sumset_certificate() -> None:
    completed = subprocess.run(
        ["python3", str(SCRIPT)],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert (
        "SQUARE_CHORD_SUMSET"
        "|rational_cases=4"
        "|algebraic_cases=3"
        "|cyclotomic_cases=4"
        "|transcendental_full_layers=true"
        "|critical_bound=m^(2-o(1))"
    ) in completed.stdout
    assert "CERTIFICATE|sha256=" in completed.stdout
    assert completed.stdout.rstrip().endswith("DONE")


def test_random_rational_layers_with_multiplicity_at_most_two() -> None:
    generator = random.Random(1083)
    for height_count in range(2, 13):
        for angular_size in range(2, 15):
            base_values = generator.sample(
                range(-80, 81), (angular_size + 1) // 2
            )
            layers = [
                (Fraction(3 * value + 1, 3),)
                for value in base_values
                for _ in range(2)
            ][:angular_size]
            generator.shuffle(layers)
            sumset_audit(height_count, tuple(layers))
