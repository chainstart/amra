/-
Copyright 2026 AMRA contributors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-/

import AmraLibrary.Combinatorics.SimpleGraph.GraphConjectures.LargestInducedTree
import Mathlib.Data.Rat.Floor
import Mathlib.Tactic

/-!
# WOWII Conjecture 58 counterexample

This file records the concrete graph used to refute WOWII Conjecture 58.
The fully formal invariant equalities are intentionally split out as the next
lemmas: `b = 6`, `largestInducedForestSize = 5`, and local-neighbourhood
independence sum `73`.  The theorem at the end verifies the graph shape and
connectivity, and states the exact conjecture inequality failure conditional on
those three invariant equalities.
-/

namespace SimpleGraph

open Classical

/-- A graph containing a triangle is not bipartite. -/
theorem not_isBipartite_of_triangle {α : Type*} {G : SimpleGraph α} {x y z : α}
    (hxy : G.Adj x y) (hyz : G.Adj y z) (hzx : G.Adj z x) :
    ¬ G.IsBipartite := by
  intro hBip
  rcases hBip.exists_isBipartiteWith with ⟨L, R, hLR⟩
  have hdisj : ∀ {v : α}, v ∈ L → v ∈ R → False := by
    intro v hvL hvR
    exact (Set.disjoint_left.mp hLR.disjoint) hvL hvR
  rcases hLR.mem_of_adj hxy with ⟨hxL, hyR⟩ | ⟨hxR, hyL⟩
  · rcases hLR.mem_of_adj hzx with ⟨hzL, hxR⟩ | ⟨hzR, _hxL⟩
    · exact hdisj hxL hxR
    · rcases hLR.mem_of_adj hyz with ⟨hyL, _hzR⟩ | ⟨_hyR, hzL⟩
      · exact hdisj hyL hyR
      · exact hdisj hzL hzR
  · rcases hLR.mem_of_adj hzx with ⟨hzL, _hxR⟩ | ⟨hzR, hxL⟩
    · rcases hLR.mem_of_adj hyz with ⟨_hyL, hzR⟩ | ⟨hyR, _hzL⟩
      · exact hdisj hzL hzR
      · exact hdisj hyL hyR
    · exact hdisj hxL hxR

/-- To prove an upper bound on the largest induced bipartite subgraph size, it
is enough to bound the cardinality of every finset whose induced subgraph is
bipartite. -/
theorem largestInducedBipartiteSubgraphSize_le_of_forall_induce_isBipartite
    {α : Type*} [Fintype α] [DecidableEq α] {G : SimpleGraph α} {N : ℕ}
    (h : ∀ s : Finset α, (G.induce (s : Set α)).IsBipartite → s.card ≤ N) :
    largestInducedBipartiteSubgraphSize G ≤ N := by
  classical
  unfold largestInducedBipartiteSubgraphSize
  apply csSup_le
  · refine ⟨0, ?_⟩
    refine ⟨∅, ?_, by simp⟩
    rw [SimpleGraph.isBipartite_iff_exists_isBipartiteWith]
    refine ⟨∅, ∅, ?_⟩
    constructor
    · simp
    · intro x _y _hxy
      exfalso
      simpa using x.2
  · intro n hn
    rcases hn with ⟨s, hsBip, rfl⟩
    exact h s hsBip

/-- Vertex set for the `k = 55` counterexample:
three `A` vertices, three `B` vertices, and a `55`-clique `C`. -/
inductive Wowii58Vertex where
  | a : Fin 3 -> Wowii58Vertex
  | b : Fin 3 -> Wowii58Vertex
  | c : Fin 55 -> Wowii58Vertex
deriving DecidableEq, Fintype

namespace Wowii58Vertex

/-- Directed presentation of the edge families.  `SimpleGraph.fromRel`
symmetrizes this relation and removes loops. -/
def rel : Wowii58Vertex -> Wowii58Vertex -> Prop
  | a _, b _ => True
  | b _, a _ => True
  | c _, c _ => True
  | c _, a i => i = 0
  | a i, c _ => i = 0
  | c _, b i => i = 0
  | b i, c _ => i = 0
  | _, _ => False

/-- The explicit `k = 55` graph refuting WOWII Conjecture 58. -/
def graph : SimpleGraph Wowii58Vertex :=
  SimpleGraph.fromRel rel

instance instDecidableRelGraphAdj : DecidableRel graph.Adj := by
  intro x y
  unfold graph
  rw [SimpleGraph.fromRel_adj]
  cases x <;> cases y <;> simp [rel] <;> infer_instance

theorem card : Fintype.card Wowii58Vertex = 61 := by
  native_decide

theorem adj_a_b (i j : Fin 3) : graph.Adj (a i) (b j) := by
  simp [graph, rel]

theorem adj_c_c {i j : Fin 55} (hij : i ≠ j) : graph.Adj (c i) (c j) := by
  simp [graph, rel, hij]

theorem adj_a0_c (i : Fin 55) : graph.Adj (a 0) (c i) := by
  simp [graph, rel]

theorem adj_b0_c (i : Fin 55) : graph.Adj (b 0) (c i) := by
  simp [graph, rel]

theorem not_adj_a_nonzero_c {i : Fin 3} (hi : i ≠ 0) (j : Fin 55) :
    ¬ graph.Adj (a i) (c j) := by
  simp [graph, rel, hi]

theorem not_adj_b_nonzero_c {i : Fin 3} (hi : i ≠ 0) (j : Fin 55) :
    ¬ graph.Adj (b i) (c j) := by
  simp [graph, rel, hi]

theorem not_adj_a_a (i j : Fin 3) : ¬ graph.Adj (a i) (a j) := by
  simp [graph, rel]

theorem not_adj_b_b (i j : Fin 3) : ¬ graph.Adj (b i) (b j) := by
  simp [graph, rel]

/-- Any induced subgraph containing three distinct `C` vertices contains a
triangle, hence is not acyclic. -/
theorem not_acyclic_induce_of_three_c_mem {s : Finset Wowii58Vertex} {i j k : Fin 55}
    (hi : c i ∈ s) (hj : c j ∈ s) (hk : c k ∈ s)
    (hij : i ≠ j) (hjk : j ≠ k) (hki : k ≠ i) :
    ¬ (graph.induce (s : Set Wowii58Vertex)).IsAcyclic := by
  let x : (s : Set Wowii58Vertex) := ⟨c i, hi⟩
  let y : (s : Set Wowii58Vertex) := ⟨c j, hj⟩
  let z : (s : Set Wowii58Vertex) := ⟨c k, hk⟩
  have hxy : (graph.induce (s : Set Wowii58Vertex)).Adj x y := adj_c_c hij
  have hyz : (graph.induce (s : Set Wowii58Vertex)).Adj y z := adj_c_c hjk
  have hzx : (graph.induce (s : Set Wowii58Vertex)).Adj z x := adj_c_c hki
  have hxy_ne : x ≠ y := by
    intro h
    exact hij (by simpa [x, y] using congrArg Subtype.val h)
  have hyz_ne : y ≠ z := by
    intro h
    exact hjk (by simpa [y, z] using congrArg Subtype.val h)
  have hzx_ne : z ≠ x := by
    intro h
    exact hki (by simpa [z, x] using congrArg Subtype.val h)
  exact not_isAcyclic_of_triangle hxy hyz hzx hxy_ne hyz_ne hzx_ne

/-- Three distinct selected `C` vertices also obstruct bipartiteness. -/
theorem not_bipartite_induce_of_three_c_mem {s : Finset Wowii58Vertex} {i j k : Fin 55}
    (hi : c i ∈ s) (hj : c j ∈ s) (hk : c k ∈ s)
    (hij : i ≠ j) (hjk : j ≠ k) (hki : k ≠ i) :
    ¬ (graph.induce (s : Set Wowii58Vertex)).IsBipartite := by
  let x : (s : Set Wowii58Vertex) := ⟨c i, hi⟩
  let y : (s : Set Wowii58Vertex) := ⟨c j, hj⟩
  let z : (s : Set Wowii58Vertex) := ⟨c k, hk⟩
  have hxy : (graph.induce (s : Set Wowii58Vertex)).Adj x y := adj_c_c hij
  have hyz : (graph.induce (s : Set Wowii58Vertex)).Adj y z := adj_c_c hjk
  have hzx : (graph.induce (s : Set Wowii58Vertex)).Adj z x := adj_c_c hki
  exact not_isBipartite_of_triangle hxy hyz hzx

/-- Any induced subgraph containing two distinct `C` vertices and `a0`
contains a triangle, hence is not acyclic. -/
theorem not_acyclic_induce_of_two_c_a0_mem {s : Finset Wowii58Vertex} {i j : Fin 55}
    (hi : c i ∈ s) (hj : c j ∈ s) (ha0 : a 0 ∈ s) (hij : i ≠ j) :
    ¬ (graph.induce (s : Set Wowii58Vertex)).IsAcyclic := by
  let x : (s : Set Wowii58Vertex) := ⟨c i, hi⟩
  let y : (s : Set Wowii58Vertex) := ⟨c j, hj⟩
  let z : (s : Set Wowii58Vertex) := ⟨a 0, ha0⟩
  have hxy : (graph.induce (s : Set Wowii58Vertex)).Adj x y := adj_c_c hij
  have hyz : (graph.induce (s : Set Wowii58Vertex)).Adj y z := (adj_a0_c j).symm
  have hzx : (graph.induce (s : Set Wowii58Vertex)).Adj z x := adj_a0_c i
  have hxy_ne : x ≠ y := by
    intro h
    exact hij (by simpa [x, y] using congrArg Subtype.val h)
  have hyz_ne : y ≠ z := by
    intro h
    cases congrArg Subtype.val h
  have hzx_ne : z ≠ x := by
    intro h
    cases congrArg Subtype.val h
  exact not_isAcyclic_of_triangle hxy hyz hzx hxy_ne hyz_ne hzx_ne

/-- Two distinct selected `C` vertices and `a0` obstruct bipartiteness. -/
theorem not_bipartite_induce_of_two_c_a0_mem {s : Finset Wowii58Vertex} {i j : Fin 55}
    (hi : c i ∈ s) (hj : c j ∈ s) (ha0 : a 0 ∈ s) (hij : i ≠ j) :
    ¬ (graph.induce (s : Set Wowii58Vertex)).IsBipartite := by
  let x : (s : Set Wowii58Vertex) := ⟨c i, hi⟩
  let y : (s : Set Wowii58Vertex) := ⟨c j, hj⟩
  let z : (s : Set Wowii58Vertex) := ⟨a 0, ha0⟩
  have hxy : (graph.induce (s : Set Wowii58Vertex)).Adj x y := adj_c_c hij
  have hyz : (graph.induce (s : Set Wowii58Vertex)).Adj y z := (adj_a0_c j).symm
  have hzx : (graph.induce (s : Set Wowii58Vertex)).Adj z x := adj_a0_c i
  exact not_isBipartite_of_triangle hxy hyz hzx

/-- Any induced subgraph containing two distinct `C` vertices and `b0`
contains a triangle, hence is not acyclic. -/
theorem not_acyclic_induce_of_two_c_b0_mem {s : Finset Wowii58Vertex} {i j : Fin 55}
    (hi : c i ∈ s) (hj : c j ∈ s) (hb0 : b 0 ∈ s) (hij : i ≠ j) :
    ¬ (graph.induce (s : Set Wowii58Vertex)).IsAcyclic := by
  let x : (s : Set Wowii58Vertex) := ⟨c i, hi⟩
  let y : (s : Set Wowii58Vertex) := ⟨c j, hj⟩
  let z : (s : Set Wowii58Vertex) := ⟨b 0, hb0⟩
  have hxy : (graph.induce (s : Set Wowii58Vertex)).Adj x y := adj_c_c hij
  have hyz : (graph.induce (s : Set Wowii58Vertex)).Adj y z := (adj_b0_c j).symm
  have hzx : (graph.induce (s : Set Wowii58Vertex)).Adj z x := adj_b0_c i
  have hxy_ne : x ≠ y := by
    intro h
    exact hij (by simpa [x, y] using congrArg Subtype.val h)
  have hyz_ne : y ≠ z := by
    intro h
    cases congrArg Subtype.val h
  have hzx_ne : z ≠ x := by
    intro h
    cases congrArg Subtype.val h
  exact not_isAcyclic_of_triangle hxy hyz hzx hxy_ne hyz_ne hzx_ne

/-- Two distinct selected `C` vertices and `b0` obstruct bipartiteness. -/
theorem not_bipartite_induce_of_two_c_b0_mem {s : Finset Wowii58Vertex} {i j : Fin 55}
    (hi : c i ∈ s) (hj : c j ∈ s) (hb0 : b 0 ∈ s) (hij : i ≠ j) :
    ¬ (graph.induce (s : Set Wowii58Vertex)).IsBipartite := by
  let x : (s : Set Wowii58Vertex) := ⟨c i, hi⟩
  let y : (s : Set Wowii58Vertex) := ⟨c j, hj⟩
  let z : (s : Set Wowii58Vertex) := ⟨b 0, hb0⟩
  have hxy : (graph.induce (s : Set Wowii58Vertex)).Adj x y := adj_c_c hij
  have hyz : (graph.induce (s : Set Wowii58Vertex)).Adj y z := (adj_b0_c j).symm
  have hzx : (graph.induce (s : Set Wowii58Vertex)).Adj z x := adj_b0_c i
  exact not_isBipartite_of_triangle hxy hyz hzx

/-- Selected vertices `a0`, `b0`, and any `C` vertex form a triangle and
therefore obstruct bipartiteness. -/
theorem not_bipartite_induce_of_a0_b0_c_mem {s : Finset Wowii58Vertex} {i : Fin 55}
    (ha0 : a 0 ∈ s) (hb0 : b 0 ∈ s) (hi : c i ∈ s) :
    ¬ (graph.induce (s : Set Wowii58Vertex)).IsBipartite := by
  let x : (s : Set Wowii58Vertex) := ⟨a 0, ha0⟩
  let y : (s : Set Wowii58Vertex) := ⟨b 0, hb0⟩
  let z : (s : Set Wowii58Vertex) := ⟨c i, hi⟩
  have hxy : (graph.induce (s : Set Wowii58Vertex)).Adj x y := adj_a_b 0 0
  have hyz : (graph.induce (s : Set Wowii58Vertex)).Adj y z := adj_b0_c i
  have hzx : (graph.induce (s : Set Wowii58Vertex)).Adj z x := (adj_a0_c i).symm
  exact not_isBipartite_of_triangle hxy hyz hzx

/-- Any induced subgraph containing two distinct `A` vertices and two distinct
`B` vertices contains a 4-cycle, hence is not acyclic. -/
theorem not_acyclic_induce_of_two_a_two_b_mem {s : Finset Wowii58Vertex}
    {i j p q : Fin 3}
    (hai : a i ∈ s) (haj : a j ∈ s) (hbp : b p ∈ s) (hbq : b q ∈ s)
    (hij : i ≠ j) (hpq : p ≠ q) :
    ¬ (graph.induce (s : Set Wowii58Vertex)).IsAcyclic := by
  let w : (s : Set Wowii58Vertex) := ⟨a i, hai⟩
  let x : (s : Set Wowii58Vertex) := ⟨b p, hbp⟩
  let y : (s : Set Wowii58Vertex) := ⟨a j, haj⟩
  let z : (s : Set Wowii58Vertex) := ⟨b q, hbq⟩
  have hwx : (graph.induce (s : Set Wowii58Vertex)).Adj w x := adj_a_b i p
  have hxy : (graph.induce (s : Set Wowii58Vertex)).Adj x y := (adj_a_b j p).symm
  have hyz : (graph.induce (s : Set Wowii58Vertex)).Adj y z := adj_a_b j q
  have hzw : (graph.induce (s : Set Wowii58Vertex)).Adj z w := (adj_a_b i q).symm
  have hwx_ne : w ≠ x := by
    intro h
    cases congrArg Subtype.val h
  have hwy_ne : w ≠ y := by
    intro h
    exact hij (by simpa [w, y] using congrArg Subtype.val h)
  have hwz_ne : w ≠ z := by
    intro h
    cases congrArg Subtype.val h
  have hxy_ne : x ≠ y := by
    intro h
    cases congrArg Subtype.val h
  have hxz_ne : x ≠ z := by
    intro h
    exact hpq (by simpa [x, z] using congrArg Subtype.val h)
  have hyz_ne : y ≠ z := by
    intro h
    cases congrArg Subtype.val h
  exact not_isAcyclic_of_four_cycle hwx hxy hyz hzw
    hwx_ne hwy_ne hwz_ne hxy_ne hxz_ne hyz_ne

/-- The three `A` vertices as a finset. -/
def Averts : Finset Wowii58Vertex :=
  Finset.univ.image a

/-- The three `B` vertices as a finset. -/
def Bverts : Finset Wowii58Vertex :=
  Finset.univ.image b

/-- The fifty-five clique vertices as a finset. -/
def Cverts : Finset Wowii58Vertex :=
  Finset.univ.image c

theorem mem_Averts {v : Wowii58Vertex} : v ∈ Averts ↔ ∃ i : Fin 3, v = a i := by
  rw [Averts, Finset.mem_image]
  constructor
  · rintro ⟨i, _hi, hvi⟩
    exact ⟨i, hvi.symm⟩
  · rintro ⟨i, hvi⟩
    exact ⟨i, by simp, hvi.symm⟩

theorem mem_Bverts {v : Wowii58Vertex} : v ∈ Bverts ↔ ∃ i : Fin 3, v = b i := by
  rw [Bverts, Finset.mem_image]
  constructor
  · rintro ⟨i, _hi, hvi⟩
    exact ⟨i, hvi.symm⟩
  · rintro ⟨i, hvi⟩
    exact ⟨i, by simp, hvi.symm⟩

theorem mem_Cverts {v : Wowii58Vertex} : v ∈ Cverts ↔ ∃ i : Fin 55, v = c i := by
  rw [Cverts, Finset.mem_image]
  constructor
  · rintro ⟨i, _hi, hvi⟩
    exact ⟨i, hvi.symm⟩
  · rintro ⟨i, hvi⟩
    exact ⟨i, by simp, hvi.symm⟩

theorem Averts_card : Averts.card = 3 := by
  native_decide

theorem Bverts_card : Bverts.card = 3 := by
  native_decide

theorem Cverts_card : Cverts.card = 55 := by
  native_decide

/-- A five-vertex induced tree witness for the lower bound on the largest
induced forest. -/
def forestWitness : Finset Wowii58Vertex :=
  {a 0, a 1, a 2, b 1, c 0}

theorem indep_Averts : graph.IsIndepSet (Averts : Set Wowii58Vertex) := by
  intro x hx y hy _hxy hAdj
  simp [Averts] at hx hy
  rcases hx with ⟨i, rfl⟩
  rcases hy with ⟨j, rfl⟩
  exact not_adj_a_a i j hAdj

theorem indep_Bverts : graph.IsIndepSet (Bverts : Set Wowii58Vertex) := by
  intro x hx y hy _hxy hAdj
  simp [Bverts] at hx hy
  rcases hx with ⟨i, rfl⟩
  rcases hy with ⟨j, rfl⟩
  exact not_adj_b_b i j hAdj

theorem disjoint_Averts_Bverts : Disjoint Averts Bverts := by
  rw [Finset.disjoint_left]
  intro x hxA hxB
  simp [Averts] at hxA
  simp [Bverts] at hxB
  rcases hxA with ⟨i, rfl⟩
  simp at hxB

theorem disjoint_Averts_Cverts : Disjoint Averts Cverts := by
  rw [Finset.disjoint_left]
  intro x hxA hxC
  rw [mem_Averts] at hxA
  rw [mem_Cverts] at hxC
  rcases hxA with ⟨i, rfl⟩
  simp at hxC

theorem disjoint_Bverts_Cverts : Disjoint Bverts Cverts := by
  rw [Finset.disjoint_left]
  intro x hxB hxC
  rw [mem_Bverts] at hxB
  rw [mem_Cverts] at hxC
  rcases hxB with ⟨i, rfl⟩
  simp at hxC

theorem Averts_union_Bverts_union_Cverts :
    Averts ∪ Bverts ∪ Cverts = Finset.univ := by
  ext v
  cases v <;> simp [Averts, Bverts, Cverts]

theorem inter_parts_card_eq (s : Finset Wowii58Vertex) :
    s.card = (s ∩ Averts).card + (s ∩ Bverts).card + (s ∩ Cverts).card := by
  have hunion : (s ∩ Averts) ∪ (s ∩ Bverts) ∪ (s ∩ Cverts) = s := by
    ext v
    cases v <;> simp [Averts, Bverts, Cverts]
  have hAB : Disjoint (s ∩ Averts) (s ∩ Bverts) := by
    rw [Finset.disjoint_left]
    intro x hxA hxB
    simp only [Finset.mem_inter] at hxA hxB
    exact (Finset.disjoint_left.mp disjoint_Averts_Bverts hxA.2) hxB.2
  have hABC : Disjoint ((s ∩ Averts) ∪ (s ∩ Bverts)) (s ∩ Cverts) := by
    rw [Finset.disjoint_left]
    intro x hxAB hxC
    simp only [Finset.mem_union, Finset.mem_inter] at hxAB hxC
    rcases hxAB with hxA | hxB
    · exact (Finset.disjoint_left.mp disjoint_Averts_Cverts hxA.2) hxC.2
    · exact (Finset.disjoint_left.mp disjoint_Bverts_Cverts hxB.2) hxC.2
  calc
    s.card = (((s ∩ Averts) ∪ (s ∩ Bverts)) ∪ (s ∩ Cverts)).card := by
      rw [hunion]
    _ = ((s ∩ Averts) ∪ (s ∩ Bverts)).card + (s ∩ Cverts).card := by
      rw [Finset.card_union_of_disjoint hABC]
    _ = ((s ∩ Averts).card + (s ∩ Bverts).card) + (s ∩ Cverts).card := by
      rw [Finset.card_union_of_disjoint hAB]
    _ = (s ∩ Averts).card + (s ∩ Bverts).card + (s ∩ Cverts).card := by
      omega

theorem two_le_Averts_inter_card_of_not_a0_mem {s : Finset Wowii58Vertex}
    (ha0 : a 0 ∉ s) : (s ∩ Averts).card ≤ 2 := by
  have hsub : s ∩ Averts ⊆ ({a 1, a 2} : Finset Wowii58Vertex) := by
    intro x hx
    rw [Finset.mem_inter] at hx
    rw [mem_Averts] at hx
    rcases hx with ⟨hxs, i, rfl⟩
    fin_cases i
    · exact False.elim (ha0 hxs)
    · simp
    · simp
  have hcard := Finset.card_le_card hsub
  have hpair : ({a 1, a 2} : Finset Wowii58Vertex).card = 2 := by
    native_decide
  omega

theorem two_le_Bverts_inter_card_of_not_b0_mem {s : Finset Wowii58Vertex}
    (hb0 : b 0 ∉ s) : (s ∩ Bverts).card ≤ 2 := by
  have hsub : s ∩ Bverts ⊆ ({b 1, b 2} : Finset Wowii58Vertex) := by
    intro x hx
    rw [Finset.mem_inter] at hx
    rw [mem_Bverts] at hx
    rcases hx with ⟨hxs, i, rfl⟩
    fin_cases i
    · exact False.elim (hb0 hxs)
    · simp
    · simp
  have hcard := Finset.card_le_card hsub
  have hpair : ({b 1, b 2} : Finset Wowii58Vertex).card = 2 := by
    native_decide
  omega

theorem a0_mem_of_Averts_inter_card_eq_three {s : Finset Wowii58Vertex}
    (hcard : (s ∩ Averts).card = 3) : a 0 ∈ s := by
  by_contra ha0
  have hle := two_le_Averts_inter_card_of_not_a0_mem (s := s) ha0
  omega

theorem b0_mem_of_Bverts_inter_card_eq_three {s : Finset Wowii58Vertex}
    (hcard : (s ∩ Bverts).card = 3) : b 0 ∈ s := by
  by_contra hb0
  have hle := two_le_Bverts_inter_card_of_not_b0_mem (s := s) hb0
  omega

theorem exists_two_Averts_mem {s : Finset Wowii58Vertex}
    (hcard : 2 ≤ (s ∩ Averts).card) :
    ∃ i j : Fin 3, a i ∈ s ∧ a j ∈ s ∧ i ≠ j := by
  have hlt : 1 < (s ∩ Averts).card := by omega
  rcases Finset.one_lt_card.mp hlt with ⟨x, hx, y, hy, hxy⟩
  rw [Finset.mem_inter] at hx hy
  rw [mem_Averts] at hx hy
  rcases hx with ⟨hxs, i, rfl⟩
  rcases hy with ⟨hys, j, hyj⟩
  subst hyj
  refine ⟨i, j, hxs, hys, ?_⟩
  intro hij
  exact hxy (by simp [hij])

theorem exists_two_Bverts_mem {s : Finset Wowii58Vertex}
    (hcard : 2 ≤ (s ∩ Bverts).card) :
    ∃ i j : Fin 3, b i ∈ s ∧ b j ∈ s ∧ i ≠ j := by
  have hlt : 1 < (s ∩ Bverts).card := by omega
  rcases Finset.one_lt_card.mp hlt with ⟨x, hx, y, hy, hxy⟩
  rw [Finset.mem_inter] at hx hy
  rw [mem_Bverts] at hx hy
  rcases hx with ⟨hxs, i, rfl⟩
  rcases hy with ⟨hys, j, hyj⟩
  subst hyj
  refine ⟨i, j, hxs, hys, ?_⟩
  intro hij
  exact hxy (by simp [hij])

theorem exists_two_Cverts_mem {s : Finset Wowii58Vertex}
    (hcard : 2 ≤ (s ∩ Cverts).card) :
    ∃ i j : Fin 55, c i ∈ s ∧ c j ∈ s ∧ i ≠ j := by
  have hlt : 1 < (s ∩ Cverts).card := by omega
  rcases Finset.one_lt_card.mp hlt with ⟨x, hx, y, hy, hxy⟩
  rw [Finset.mem_inter] at hx hy
  rw [mem_Cverts] at hx hy
  rcases hx with ⟨hxs, i, rfl⟩
  rcases hy with ⟨hys, j, hyj⟩
  subst hyj
  refine ⟨i, j, hxs, hys, ?_⟩
  intro hij
  exact hxy (by simp [hij])

theorem exists_three_Cverts_mem {s : Finset Wowii58Vertex}
    (hcard : 3 ≤ (s ∩ Cverts).card) :
    ∃ i j k : Fin 55,
      c i ∈ s ∧ c j ∈ s ∧ c k ∈ s ∧ i ≠ j ∧ j ≠ k ∧ k ≠ i := by
  rcases Finset.exists_subset_card_eq hcard with ⟨t, htsub, htcard⟩
  rcases Finset.card_eq_three.mp htcard with ⟨x, y, z, hxy, hxz, hyz, ht⟩
  have hx : x ∈ s ∩ Cverts := htsub (by simp [ht])
  have hy : y ∈ s ∩ Cverts := htsub (by simp [ht])
  have hz : z ∈ s ∩ Cverts := htsub (by simp [ht])
  rw [Finset.mem_inter] at hx hy hz
  rw [mem_Cverts] at hx hy hz
  rcases hx with ⟨hxs, i, rfl⟩
  rcases hy with ⟨hys, j, hyj⟩
  rcases hz with ⟨hzs, k, hzk⟩
  subst hyj
  subst hzk
  refine ⟨i, j, k, hxs, hys, hzs, ?_, ?_, ?_⟩
  · intro hij
    exact hxy (by simp [hij])
  · intro hjk
    exact hyz (by simp [hjk])
  · intro hki
    exact hxz (by simp [hki.symm])

theorem not_acyclic_induce_of_six_le_card {s : Finset Wowii58Vertex}
    (hsix : 6 ≤ s.card) :
    ¬ (graph.induce (s : Set Wowii58Vertex)).IsAcyclic := by
  let aN := (s ∩ Averts).card
  let bN := (s ∩ Bverts).card
  let cN := (s ∩ Cverts).card
  have hcard : s.card = aN + bN + cN := by
    simpa [aN, bN, cN] using inter_parts_card_eq s
  have hAle : aN ≤ 3 := by
    have h := Finset.card_le_card (Finset.inter_subset_right : s ∩ Averts ⊆ Averts)
    simpa [aN, Averts_card] using h
  have hBle : bN ≤ 3 := by
    have h := Finset.card_le_card (Finset.inter_subset_right : s ∩ Bverts ⊆ Bverts)
    simpa [bN, Bverts_card] using h
  by_cases hCthree : 3 ≤ cN
  · rcases exists_three_Cverts_mem (s := s) (by simpa [cN] using hCthree) with
      ⟨i, j, k, hi, hj, hk, hij, hjk, hki⟩
    exact not_acyclic_induce_of_three_c_mem hi hj hk hij hjk hki
  have hCle : cN ≤ 2 := by omega
  by_cases hCtwo : 2 ≤ cN
  · have hCeq : cN = 2 := by omega
    rcases exists_two_Cverts_mem (s := s) (by simpa [cN] using hCtwo) with
      ⟨i, j, hi, hj, hij⟩
    by_cases ha0 : a 0 ∈ s
    · exact not_acyclic_induce_of_two_c_a0_mem hi hj ha0 hij
    by_cases hb0 : b 0 ∈ s
    · exact not_acyclic_induce_of_two_c_b0_mem hi hj hb0 hij
    have hAle' : aN ≤ 2 := by
      simpa [aN] using two_le_Averts_inter_card_of_not_a0_mem (s := s) ha0
    have hBle' : bN ≤ 2 := by
      simpa [bN] using two_le_Bverts_inter_card_of_not_b0_mem (s := s) hb0
    have hAtwo : 2 ≤ aN := by omega
    have hBtwo : 2 ≤ bN := by omega
    rcases exists_two_Averts_mem (s := s) (by simpa [aN] using hAtwo) with
      ⟨p, q, hp, hq, hpq⟩
    rcases exists_two_Bverts_mem (s := s) (by simpa [bN] using hBtwo) with
      ⟨r, t, hr, ht, hrt⟩
    exact not_acyclic_induce_of_two_a_two_b_mem hp hq hr ht hpq hrt
  · have hCle' : cN ≤ 1 := by omega
    have hAtwo : 2 ≤ aN := by omega
    have hBtwo : 2 ≤ bN := by omega
    rcases exists_two_Averts_mem (s := s) (by simpa [aN] using hAtwo) with
      ⟨p, q, hp, hq, hpq⟩
    rcases exists_two_Bverts_mem (s := s) (by simpa [bN] using hBtwo) with
      ⟨r, t, hr, ht, hrt⟩
    exact not_acyclic_induce_of_two_a_two_b_mem hp hq hr ht hpq hrt

/-- The induced `A ∪ B` subgraph is a `K_{3,3}` witness, so `b ≥ 6`. -/
theorem six_le_b : 6 ≤ graph.b := by
  have hBip :
      (graph.induce (((Averts ∪ Bverts : Finset Wowii58Vertex) : Set Wowii58Vertex))).IsBipartite :=
    induce_union_indep_isBipartite (G := graph) indep_Averts indep_Bverts disjoint_Averts_Bverts
  have hle := card_le_largestInducedBipartiteSubgraphSize_of_induce_isBipartite
    (G := graph) (s := Averts ∪ Bverts) hBip
  have hcard : (Averts ∪ Bverts).card = 6 := by
    native_decide
  simpa [b, hcard] using hle

/-- Every induced bipartite subgraph has at most six vertices. -/
theorem b_le_six : graph.b ≤ 6 := by
  apply largestInducedBipartiteSubgraphSize_le_of_forall_induce_isBipartite
  intro s hsBip
  let aN := (s ∩ Averts).card
  let bN := (s ∩ Bverts).card
  let cN := (s ∩ Cverts).card
  have hcard : s.card = aN + bN + cN := by
    simpa [aN, bN, cN] using inter_parts_card_eq s
  have hAle : aN ≤ 3 := by
    have h := Finset.card_le_card (Finset.inter_subset_right : s ∩ Averts ⊆ Averts)
    simpa [aN, Averts_card] using h
  have hBle : bN ≤ 3 := by
    have h := Finset.card_le_card (Finset.inter_subset_right : s ∩ Bverts ⊆ Bverts)
    simpa [bN, Bverts_card] using h
  by_contra hle
  have hseven : 7 ≤ s.card := by omega
  by_cases hCthree : 3 ≤ cN
  · rcases exists_three_Cverts_mem (s := s) (by simpa [cN] using hCthree) with
      ⟨i, j, k, hi, hj, hk, hij, hjk, hki⟩
    exact not_bipartite_induce_of_three_c_mem hi hj hk hij hjk hki hsBip
  have hCle_two : cN ≤ 2 := by omega
  by_cases hCtwo : 2 ≤ cN
  · rcases exists_two_Cverts_mem (s := s) (by simpa [cN] using hCtwo) with
      ⟨i, j, hi, hj, hij⟩
    by_cases ha0 : a 0 ∈ s
    · exact not_bipartite_induce_of_two_c_a0_mem hi hj ha0 hij hsBip
    by_cases hb0 : b 0 ∈ s
    · exact not_bipartite_induce_of_two_c_b0_mem hi hj hb0 hij hsBip
    have hAle' : aN ≤ 2 := by
      simpa [aN] using two_le_Averts_inter_card_of_not_a0_mem (s := s) ha0
    have hBle' : bN ≤ 2 := by
      simpa [bN] using two_le_Bverts_inter_card_of_not_b0_mem (s := s) hb0
    omega
  have hCle_one : cN ≤ 1 := by omega
  have hAeq : aN = 3 := by omega
  have hBeq : bN = 3 := by omega
  have hCeq : cN = 1 := by omega
  have ha0 : a 0 ∈ s :=
    a0_mem_of_Averts_inter_card_eq_three (s := s) (by simpa [aN] using hAeq)
  have hb0 : b 0 ∈ s :=
    b0_mem_of_Bverts_inter_card_eq_three (s := s) (by simpa [bN] using hBeq)
  have hCpos : 0 < (s ∩ Cverts).card := by
    simpa [cN] using (by omega : 0 < cN)
  rcases Finset.card_pos.mp hCpos with ⟨x, hx⟩
  rw [Finset.mem_inter] at hx
  rw [mem_Cverts] at hx
  rcases hx with ⟨hxs, i, rfl⟩
  exact not_bipartite_induce_of_a0_b0_c_mem ha0 hb0 hxs hsBip

theorem b_eq_six : graph.b = 6 :=
  le_antisymm b_le_six six_le_b

/-- The induced witness `{a0,a1,a2,b1,c0}` is connected. -/
theorem forestWitness_connected :
    (graph.induce (forestWitness : Set Wowii58Vertex)).Connected := by
  rw [SimpleGraph.connected_iff_exists_forall_reachable]
  let center : (forestWitness : Set Wowii58Vertex) := ⟨a 0, by simp [forestWitness]⟩
  refine ⟨center, ?_⟩
  intro w
  have h_b1 : (graph.induce (forestWitness : Set Wowii58Vertex)).Reachable center
      ⟨b 1, by simp [forestWitness]⟩ :=
    (show (graph.induce (forestWitness : Set Wowii58Vertex)).Adj
      center ⟨b 1, by simp [forestWitness]⟩ from adj_a_b 0 1).reachable
  have h_a1 : (graph.induce (forestWitness : Set Wowii58Vertex)).Reachable center
        ⟨a 1, by simp [forestWitness]⟩ :=
    h_b1.trans
      (show (graph.induce (forestWitness : Set Wowii58Vertex)).Adj
        ⟨b 1, by simp [forestWitness]⟩ ⟨a 1, by simp [forestWitness]⟩
        from (adj_a_b 1 1).symm).reachable
  have h_a2 : (graph.induce (forestWitness : Set Wowii58Vertex)).Reachable center
        ⟨a 2, by simp [forestWitness]⟩ :=
    h_b1.trans
      (show (graph.induce (forestWitness : Set Wowii58Vertex)).Adj
        ⟨b 1, by simp [forestWitness]⟩ ⟨a 2, by simp [forestWitness]⟩
        from (adj_a_b 2 1).symm).reachable
  have h_c0 : (graph.induce (forestWitness : Set Wowii58Vertex)).Reachable center
      ⟨c 0, by simp [forestWitness]⟩ :=
    (show (graph.induce (forestWitness : Set Wowii58Vertex)).Adj
      center ⟨c 0, by simp [forestWitness]⟩ from adj_a0_c 0).reachable
  rcases w with ⟨v, hv⟩
  cases v with
  | a i =>
      fin_cases i
      · exact SimpleGraph.Reachable.rfl
      · simpa using h_a1
      · simpa using h_a2
  | b i =>
      fin_cases i
      · simp [forestWitness] at hv
      · simpa using h_b1
      · simp [forestWitness] at hv
  | c i =>
      have hi : i = 0 := by
        simpa [forestWitness] using hv
      subst i
      simpa using h_c0

/-- The counterexample graph has an induced forest on five vertices. -/
theorem five_le_largestInducedForestSize :
    5 ≤ graph.largestInducedForestSize := by
  have hcard : Nat.card (graph.induce (forestWitness : Set Wowii58Vertex)).edgeSet + 1 =
      Nat.card (forestWitness : Set Wowii58Vertex) := by
    rw [Nat.card_eq_fintype_card, Nat.card_eq_fintype_card]
    native_decide
  have hacyc : (graph.induce (forestWitness : Set Wowii58Vertex)).IsAcyclic :=
    ((isTree_iff_connected_and_card
      (G := graph.induce (forestWitness : Set Wowii58Vertex))).mpr
        ⟨forestWitness_connected, hcard⟩).IsAcyclic
  have hle := card_le_largestInducedForestSize_of_induce_isAcyclic
    (G := graph) (s := forestWitness) hacyc
  have hfw : forestWitness.card = 5 := by
    native_decide
  simpa [hfw] using hle

/-- No six-vertex induced subgraph is acyclic, so every induced forest has at
most five vertices. -/
theorem largestInducedForestSize_le_five :
    graph.largestInducedForestSize ≤ 5 := by
  apply largestInducedForestSize_le_of_forall_induce_isAcyclic
  intro s hs
  by_contra hle
  have hsix : 6 ≤ s.card := by omega
  exact not_acyclic_induce_of_six_le_card hsix hs

theorem largestInducedForestSize_eq_five :
    graph.largestInducedForestSize = 5 :=
  le_antisymm largestInducedForestSize_le_five five_le_largestInducedForestSize

theorem connected : graph.Connected := by
  rw [SimpleGraph.connected_iff_exists_forall_reachable]
  refine ⟨a 0, ?_⟩
  intro w
  cases w with
  | a i =>
      by_cases hi : i = 0
      · subst i
        exact SimpleGraph.Reachable.rfl
      · exact
          (adj_a_b 0 0).reachable.trans
            (adj_a_b i 0).symm.reachable
  | b i =>
      exact (adj_a_b 0 i).reachable
  | c i =>
      exact (adj_a0_c i).reachable

end Wowii58Vertex

/-- Arithmetic part of the counterexample after substituting the invariant
values `b = 6`, `l_avg = 73 / 61`, and forest size `5`. -/
theorem wowii58_audited_values_violate_bound :
    ¬ Nat.ceil ((6 : ℚ) / ((73 : ℚ) / 61)) ≤ 5 := by
  norm_num [Nat.ceil_eq_iff]

/-- Strengthened counterexample package after certifying `b = 6` and
`largestInducedForestSize = 5`; the local-neighbourhood average remains the
only invariant equality still supplied as a hypothesis. -/
theorem wowii_conjecture58_counterexample_certified_except_lavg :
    Wowii58Vertex.graph.Connected ∧
      Fintype.card Wowii58Vertex = 61 ∧
        Wowii58Vertex.graph.b = 6 ∧
          Wowii58Vertex.graph.largestInducedForestSize = 5 ∧
            (Wowii58Vertex.graph.l_avg = (73 : ℚ) / 61 →
              ¬ Nat.ceil ((Wowii58Vertex.graph.b : ℚ) / Wowii58Vertex.graph.l_avg)
                  ≤ Wowii58Vertex.graph.largestInducedForestSize) := by
  refine ⟨Wowii58Vertex.connected, Wowii58Vertex.card, Wowii58Vertex.b_eq_six,
    Wowii58Vertex.largestInducedForestSize_eq_five, ?_⟩
  intro hlavg
  rw [Wowii58Vertex.b_eq_six, Wowii58Vertex.largestInducedForestSize_eq_five, hlavg]
  exact wowii58_audited_values_violate_bound

/-- Verified core of the WOWII Conjecture 58 counterexample.

The hard graph-invariant equalities remain the next formalization targets.
This declaration keeps the concrete graph and the original conjecture
inequality in the Lean namespace required by the benchmark: once the three
invariant equalities are supplied, the conjectured bound is false for
`Wowii58Vertex.graph`. -/
theorem wowii_conjecture58_counterexample :
    Wowii58Vertex.graph.Connected ∧
      Fintype.card Wowii58Vertex = 61 ∧
        (Wowii58Vertex.graph.b = 6 →
          Wowii58Vertex.graph.largestInducedForestSize = 5 →
            Wowii58Vertex.graph.l_avg = (73 : ℚ) / 61 →
              ¬ Nat.ceil ((Wowii58Vertex.graph.b : ℚ) / Wowii58Vertex.graph.l_avg)
                  ≤ Wowii58Vertex.graph.largestInducedForestSize) := by
  refine ⟨Wowii58Vertex.connected, Wowii58Vertex.card, ?_⟩
  intro hb hf hlavg
  rw [hb, hf, hlavg]
  exact wowii58_audited_values_violate_bound

end SimpleGraph
