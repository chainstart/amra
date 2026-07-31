import unittest

import verify_reserve_hall as verifier
import falsify_centered_cross_budget as falsifier


class ReserveHallTests(unittest.TestCase):
    def test_zero_shore_reserve(self) -> None:
        verifier.check_zero_shore_reserve()
        self.assertEqual(verifier.check_rectangle_lower_bound(), 4096)

    def test_balanced_chain_range(self) -> None:
        result = verifier.run()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["balanced_chain_instances"], 28)
        self.assertEqual(result["largest_matching"], 900)
        self.assertEqual(result["three_hub_instances"], 117)
        self.assertEqual(result["three_hub_status"], "PASS")

    def test_centered_template_falsifier(self) -> None:
        result = falsifier.run()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["qualifying_full_contract_blowups"], 93)


if __name__ == "__main__":
    unittest.main()
