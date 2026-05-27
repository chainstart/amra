import AmraLibrary.Combinatorics.SimpleGraph.GraphConjectures.WowiiConjecture13
import Mathlib.Tactic

namespace SimpleGraph

open Classical

variable {α : Type*} [Fintype α] [DecidableEq α]

theorem not_adj_neighbor_geodesic_vertex_of_index_ge_three
    {G : SimpleGraph α} {x y a : α} (p : G.Walk x y)
    (hp : p.length = G.dist x y) {i : ℕ}
    (hi3 : 3 ≤ i) (hi : i ≤ p.length)
    (hxa : G.Adj x a) :
    ¬ G.Adj a (p.getVert i) := by
  intro hap
  have hdist_eq : G.dist x (p.getVert i) = i := by
    have hdist_zero :
        G.dist (p.getVert 0) (p.getVert i) = i - 0 :=
      geodesic_getVert_dist_eq_index_sub (G := G) p hp (Nat.zero_le i) hi
    simpa [SimpleGraph.Walk.getVert_zero] using hdist_zero
  let q : G.Walk x (p.getVert i) := hxa.toWalk.append hap.toWalk
  have hdist_le_two : G.dist x (p.getVert i) ≤ 2 := by
    simpa [q] using SimpleGraph.dist_le q
  omega

end SimpleGraph


namespace SimpleGraph

open Classical

variable {α : Type*} [Fintype α] [DecidableEq α] [Nonempty α]

theorem exists_diam_add_indepNeighborsCard_bipartite_witness_of_diam_geodesic_from
    {G : SimpleGraph α} (hG : G.Connected) (v : α) :
    ∃ s : Finset α,
      (G.induce (s : Set α)).IsBipartite ∧
        (G.diam : ℝ) + (indepNeighborsCard G v : ℝ) ≤ (s.card : ℝ) := by
  sorry

end SimpleGraph
