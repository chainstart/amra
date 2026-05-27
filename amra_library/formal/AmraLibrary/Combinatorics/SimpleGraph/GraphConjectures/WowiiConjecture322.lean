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
import AmraLibrary.Combinatorics.SimpleGraph.GraphConjectures.WellTotallyDominated
import Mathlib.Tactic

/-!
# Written on the Wall II - Conjecture 322

Formalization target for the natural-language proof route identified by AMRA.
-/

namespace SimpleGraph

open Classical

set_option linter.unusedSectionVars false
set_option linter.unnecessarySimpa false

variable {α : Type*} [Fintype α] [DecidableEq α]

/-- Local independence at most one forces every open neighbourhood to be a clique. -/
theorem locally_clique_of_indepNeighborsCard_le_one
    (G : SimpleGraph α) [DecidableRel G.Adj]
    (h : ∀ v : α, indepNeighborsCard G v ≤ 1)
    {v x y : α} (hx : G.Adj v x) (hy : G.Adj v y) (hxy : x ≠ y) :
    G.Adj x y := by
  by_contra hnxy
  let sx : G.neighborSet v := ⟨x, hx⟩
  let sy : G.neighborSet v := ⟨y, hy⟩
  let s : Finset (G.neighborSet v) := {sx, sy}
  have hs_indep : (G.induce (G.neighborSet v)).IsIndepSet (s : Set (G.neighborSet v)) := by
    intro a ha b hb hab hadj
    change a ∈ insert sx ({sy} : Finset (G.neighborSet v)) at ha
    change b ∈ insert sx ({sy} : Finset (G.neighborSet v)) at hb
    rw [Finset.mem_insert, Finset.mem_singleton] at ha hb
    rcases ha with rfl | rfl <;> rcases hb with rfl | rfl
    · exact hab rfl
    · exact hnxy hadj
    · exact hnxy hadj.symm
    · exact hab rfl
  have hsx_ne_sy : sx ≠ sy := by
    intro hxy'
    exact hxy (Subtype.ext_iff.mp hxy')
  have hs_card : s.card = 2 := by
    simp [s, hsx_ne_sy]
  have htwo_le : 2 ≤ indepNeighborsCard G v := by
    unfold indepNeighborsCard
    simpa [hs_card] using
      (SimpleGraph.IsIndepSet.card_le_indepNum (G := G.induce (G.neighborSet v))
        (t := s) hs_indep)
  have hcontr : 2 ≤ 1 := le_trans htwo_le (h v)
  omega

/-- A connected graph whose every open neighbourhood has independence number at
most one is complete. -/
theorem connected_eq_top_of_indepNeighborsCard_le_one
    (G : SimpleGraph α) [DecidableRel G.Adj]
    (hG : G.Connected)
    (h : ∀ v : α, indepNeighborsCard G v ≤ 1) :
    G = ⊤ := by
  apply SimpleGraph.ext
  funext x y
  apply propext
  constructor
  · intro hxy
    exact (SimpleGraph.top_adj x y).mpr (G.ne_of_adj hxy)
  · intro hxy_top
    have hxy : x ≠ y := (SimpleGraph.top_adj x y).mp hxy_top
    obtain ⟨p, hp_path, hp_dist⟩ := (hG x y).exists_path_of_dist
    by_cases hp0 : p.length = 0
    · exact False.elim (hxy (p.eq_of_length_eq_zero hp0))
    by_cases hp1 : p.length = 1
    · exact p.adj_of_length_eq_one hp1
    have hp2 : 2 ≤ p.length := by omega
    have h01 : G.Adj (p.getVert 0) (p.getVert 1) := by
      simpa using p.adj_getVert_succ (by omega : 0 < p.length)
    have h12 : G.Adj (p.getVert 1) (p.getVert 2) := by
      simpa using p.adj_getVert_succ (by omega : 1 < p.length)
    have h02_ne : p.getVert 0 ≠ p.getVert 2 := by
      intro h02
      have hidx : (0 : ℕ) = 2 :=
        hp_path.getVert_injOn (by simp) hp2 h02
      omega
    have h02 : G.Adj (p.getVert 0) (p.getVert 2) :=
      locally_clique_of_indepNeighborsCard_le_one (G := G) h
        (v := p.getVert 1) (x := p.getVert 0) (y := p.getVert 2)
        h01.symm h12 h02_ne
    exact False.elim
      (shortest_walk_no_forward_chord p hp_dist
        (i := 0) (j := 2) (by omega) (by omega) (by omega) h02)

/-- Any two-element subset of a complete graph is a total dominating set. -/
theorem isTotalDominatingSet_top_of_two_le_card
    [DecidableEq α] {S : Finset α} (hS : 2 ≤ S.card) :
    IsTotalDominatingSet (⊤ : SimpleGraph α) S := by
  intro v
  obtain ⟨w, hwS, hvw⟩ : ∃ w ∈ S, v ≠ w := by
    by_contra hbad
    push_neg at hbad
    have hsub : S ⊆ {v} := by
      intro w hw
      simp [hbad w hw]
    have hcard_le : S.card ≤ ({v} : Finset α).card := Finset.card_le_card hsub
    simp at hcard_le
    omega
  exact ⟨w, hwS, (SimpleGraph.top_adj v w).mpr hvw⟩

/-- Minimal total dominating sets of a complete graph have cardinality two. -/
theorem card_eq_two_of_isMinimalTotalDominatingSet_top
    [DecidableEq α] (hcard : 2 ≤ Fintype.card α) {S : Finset α}
    (hS : IsMinimalTotalDominatingSet (⊤ : SimpleGraph α) S) :
    S.card = 2 := by
  classical
  haveI : Nonempty α := Fintype.card_pos_iff.mp (by omega : 0 < Fintype.card α)
  have hS_ge : 2 ≤ S.card := by
    obtain ⟨v⟩ := (inferInstance : Nonempty α)
    obtain ⟨w, hwS, _hvw⟩ := hS.1 v
    obtain ⟨z, hzS, hwz⟩ := hS.1 w
    have hw_ne_z : w ≠ z := (SimpleGraph.top_adj w z).mp hwz
    have hpair_subset : ({w, z} : Finset α) ⊆ S := by
      intro u hu
      simp only [Finset.mem_insert, Finset.mem_singleton] at hu
      rcases hu with rfl | rfl
      · exact hwS
      · exact hzS
    have hpair_card : ({w, z} : Finset α).card = 2 := by
      simp [hw_ne_z]
    simpa [hpair_card] using Finset.card_le_card hpair_subset
  have hS_le : S.card ≤ 2 := by
    by_contra hnot
    obtain ⟨T, hTsub, hTcard⟩ :=
      Finset.exists_subset_card_eq (s := S) (n := 2) hS_ge
    have hTssub : T ⊂ S := by
      rw [Finset.ssubset_iff_subset_ne]
      refine ⟨hTsub, ?_⟩
      intro hTS
      have : S.card = 2 := by
        simpa [hTS] using hTcard
      omega
    exact hS.2 T hTssub
      (isTotalDominatingSet_top_of_two_le_card (S := T) (by simpa [hTcard]))
  exact le_antisymm hS_le hS_ge

/-- Complete graphs on at least two vertices are well totally dominated. -/
theorem isWellTotallyDominated_top_of_two_le_card
    [DecidableEq α] (hcard : 2 ≤ Fintype.card α) :
    IsWellTotallyDominated (⊤ : SimpleGraph α) := by
  intro S T hS hT
  rw [card_eq_two_of_isMinimalTotalDominatingSet_top (hcard := hcard) hS,
    card_eq_two_of_isMinimalTotalDominatingSet_top (hcard := hcard) hT]

/--
WOWII Conjecture 322: a connected finite graph on at least five vertices whose
every open neighbourhood has independence number at most one is well totally
dominated.
-/
theorem conjecture322 (G : SimpleGraph α) [DecidableRel G.Adj]
    (hG : G.Connected)
    (hn : 5 ≤ Fintype.card α)
    (h : ∀ v : α, indepNeighborsCard G v ≤ 1) :
    IsWellTotallyDominated G := by
  have htop : G = ⊤ := connected_eq_top_of_indepNeighborsCard_le_one (G := G) hG h
  subst htop
  exact isWellTotallyDominated_top_of_two_le_card (α := α) (by omega : 2 ≤ Fintype.card α)

end SimpleGraph
