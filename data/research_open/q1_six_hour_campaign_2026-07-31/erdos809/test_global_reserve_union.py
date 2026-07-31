import unittest

import verify_global_reserve_union as verifier


class GlobalReserveUnionTests(unittest.TestCase):
    def test_empty_graph_models(self) -> None:
        for order in range(3, 7):
            colours = (tuple(range(order)),) * order
            verifier.audit_instance(order, set(), colours)

    def test_seeded_random_models(self) -> None:
        accepted, obstructed = verifier.random_audit(accepted_target=200)
        self.assertEqual(accepted, 200)
        self.assertGreater(obstructed, 0)


if __name__ == "__main__":
    unittest.main()
