import unittest

import verify_adaptive_forest_reserve as verifier


class AdaptiveForestReserveTests(unittest.TestCase):
    def test_strict_fixed_root_separation(self) -> None:
        colours = verifier.strict_separation_instance()
        self.assertTrue(verifier.adaptive_feasible(colours))
        self.assertTrue(verifier.partition_condition(colours))
        self.assertTrue(
            all(
                not verifier.fixed_star_feasible(colours, (root,))
                for root in colours[0].vertices
            )
        )

    def test_global_union_strictly_beats_adaptive_tree(self) -> None:
        colours = verifier.global_over_adaptive_instance()
        self.assertEqual(verifier.global_defect(colours), 3)
        self.assertEqual(len(verifier.global_reserve_union(colours)), 3)
        self.assertTrue(verifier.global_union_closes(colours))
        self.assertFalse(verifier.adaptive_feasible(colours))
        self.assertFalse(verifier.partition_condition(colours))

    def test_complete_small_audit(self) -> None:
        self.assertEqual(verifier.exhaustive_tiny_audit(), 100)

    def test_random_and_tree_packing_guards(self) -> None:
        self.assertEqual(verifier.random_audit(instances=100), 100)
        self.assertTrue(verifier.adaptive_feasible(verifier.base_only_instance(4, 2)))
        self.assertFalse(verifier.adaptive_feasible(verifier.base_only_instance(4, 3)))

    def test_minimal_obstruction_rigidity(self) -> None:
        repeated = verifier.Colour(
            (0, 1), {verifier.edge(0, 1): frozenset({"a"})}
        )
        colours = (repeated, repeated)
        self.assertFalse(verifier.partition_condition(colours))
        self.assertTrue(verifier.check_minimal_obstruction_rigidity(colours))
        self.assertGreater(verifier.rigidity_audit(instances=30), 0)


if __name__ == "__main__":
    unittest.main()
