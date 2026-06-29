import Mathlib.Combinatorics.SimpleGraph.Diam
import Mathlib.Combinatorics.SimpleGraph.Bipartite
import Mathlib.Combinatorics.SimpleGraph.Hamiltonian
import Mathlib.Combinatorics.SimpleGraph.Connectivity.WalkCounting
import Mathlib.Combinatorics.SimpleGraph.Connectivity.Subgraph
import Mathlib.Data.List.OfFn
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.SuppressCompilation

suppress_compilation

/-!
# WOWII 198a leftmost-edge certificate workspace

This file is the Lean formalizer workspace for the next WOWII 198a certificate
target selected by AMRA proof-lab:
`path_neighbors_subset_of_leftmostEligibleEdge`.

The file intentionally starts without trusted assumptions or unfinished
proofs. The formalizer should add the minimal local definitions
`IsDiametralGeodesic` and `LeftmostEligibleEdge`, then prove the boundary-safe
path-neighbor restriction before returning to the same-fiber clique lemma.
-/

namespace SimpleGraph

open Classical

set_option linter.unusedSectionVars false
set_option linter.unnecessarySimpa false

variable {alpha : Type*}

/-- `largestInducedBipartiteSubgraphSize G` is the number of vertices in a
largest induced bipartite subgraph of `G`. -/
noncomputable def largestInducedBipartiteSubgraphSize [Fintype alpha]
    (G : SimpleGraph alpha) : ℕ :=
  sSup { n | ∃ s : Finset alpha, (G.induce (s : Set alpha)).IsBipartite ∧ s.card = n }

/-- WOWII notation for the order of a largest induced bipartite subgraph. -/
noncomputable abbrev b [Fintype alpha] (G : SimpleGraph alpha) : ℕ :=
  largestInducedBipartiteSubgraphSize G

/-- Any explicit induced bipartite subgraph gives a lower bound for
`largestInducedBipartiteSubgraphSize`. -/
theorem card_le_largestInducedBipartiteSubgraphSize_of_induce_isBipartite
    [Fintype alpha] {G : SimpleGraph alpha} {s : Finset alpha}
    (hs : (G.induce (s : Set alpha)).IsBipartite) :
    s.card ≤ largestInducedBipartiteSubgraphSize G := by
  classical
  unfold largestInducedBipartiteSubgraphSize
  apply le_csSup
  · exact ⟨Fintype.card alpha, by
      intro n hn
      rcases hn with ⟨t, _ht, rfl⟩
      exact Finset.card_le_univ t⟩
  · exact ⟨s, hs, rfl⟩

/-- Two disjoint independent finsets induce a bipartite graph on their union. -/
theorem induce_union_indep_isBipartite
    [Fintype alpha] [DecidableEq alpha] {G : SimpleGraph alpha} {A B : Finset alpha}
    (hA : G.IsIndepSet (A : Set alpha))
    (hB : G.IsIndepSet (B : Set alpha))
    (hdisj : Disjoint A B) :
    (G.induce ((A ∪ B : Finset alpha) : Set alpha)).IsBipartite := by
  classical
  let U : Set alpha := ((A ∪ B : Finset alpha) : Set alpha)
  let left : Set U := {x | x.1 ∈ A}
  let right : Set U := {x | x.1 ∈ B}
  change (G.induce U).IsBipartite
  refine (show (G.induce U).IsBipartiteWith left right from ?_).isBipartite
  constructor
  · rw [Set.disjoint_left]
    intro x hxA hxB
    exact (Finset.disjoint_left.mp hdisj hxA) hxB
  · intro x y hxy
    have hxmem : x.1 ∈ A ∪ B := x.2
    have hymem : y.1 ∈ A ∪ B := y.2
    rw [Finset.mem_union] at hxmem hymem
    rcases hxmem with hxA | hxB
    · rcases hymem with hyA | hyB
      · exact False.elim (hA hxA hyA (fun h => hxy.ne (Subtype.ext h)) hxy)
      · exact Or.inl ⟨hxA, hyB⟩
    · rcases hymem with hyA | hyB
      · exact Or.inr ⟨hxB, hyA⟩
      · exact False.elim (hB hxB hyB (fun h => hxy.ne (Subtype.ext h)) hxy)

/-- Source-name alias for the average vertex eccentricity. -/
noncomputable def averageEccentricity [Fintype alpha]
    (G : SimpleGraph alpha) : ℝ :=
  (∑ v : alpha, ((G.eccent v).toNat : ℝ)) / (Fintype.card alpha : ℝ)

lemma eccent_toNat_le_diam [Fintype alpha] [Nonempty alpha]
    {G : SimpleGraph alpha} (hconn : G.Connected) (v : alpha) :
    (G.eccent v).toNat ≤ G.diam := by
  exact ENat.toNat_le_toNat SimpleGraph.eccent_le_ediam
    (SimpleGraph.connected_iff_ediam_ne_top.mp hconn)

lemma averageEccentricity_le_diam [Fintype alpha] [Nonempty alpha]
    {G : SimpleGraph alpha} (hconn : G.Connected) :
    averageEccentricity G ≤ (G.diam : ℝ) := by
  classical
  unfold averageEccentricity
  have hsum :
      (∑ v : alpha, ((G.eccent v).toNat : ℝ))
        ≤ ∑ _v : alpha, (G.diam : ℝ) := by
    exact Finset.sum_le_sum fun v _hv => by
      exact_mod_cast eccent_toNat_le_diam (G := G) hconn v
  have hcard_pos : 0 < (Fintype.card alpha : ℝ) := by
    exact_mod_cast Fintype.card_pos
  rw [Finset.sum_const, Finset.card_univ, nsmul_eq_mul] at hsum
  rw [div_le_iff₀ hcard_pos]
  simpa [mul_comm] using hsum

/-- In a finite connected graph there is a geodesic walk whose length realizes
the diameter. -/
theorem exists_diameter_walk_with_dist
    [Fintype alpha] [Nonempty alpha] (G : SimpleGraph alpha) (h : G.Connected) :
    ∃ u v : alpha, ∃ p : G.Walk u v,
      p.IsPath ∧ p.length = G.dist u v ∧ p.length = G.diam := by
  classical
  obtain ⟨u, v, huv⟩ := G.exists_dist_eq_diam
  obtain ⟨p, hp_path, hp_dist⟩ := (h u v).exists_path_of_dist
  exact ⟨u, v, p, hp_path, hp_dist, by rw [hp_dist, huv]⟩

/-- The segment of a walk from index `i` to index `j` gives a route of length
`j - i`, hence the graph distance between those indexed vertices is at most
`j - i`. -/
theorem dist_getVert_getVert_le_index_sub
    {G : SimpleGraph alpha} {u v : alpha} (p : G.Walk u v) {i j : ℕ}
    (hi : i ≤ j) (hj : j ≤ p.length) :
    G.dist (p.getVert i) (p.getVert j) ≤ j - i := by
  let q : G.Walk (p.getVert i) (p.getVert j) :=
    ((p.drop i).take (j - i)).copy rfl (by
      rw [SimpleGraph.Walk.drop_getVert]
      have hji : j - i ≤ p.length - i := Nat.sub_le_sub_right hj i
      rw [add_tsub_cancel_of_le hi])
  have hdist := SimpleGraph.dist_le q
  have hlen : q.length = j - i := by
    simp [q, SimpleGraph.Walk.take_length, SimpleGraph.Walk.drop_length,
      Nat.min_eq_left (Nat.sub_le_sub_right hj i)]
  simpa [hlen] using hdist

/-- Along a walk whose length realizes the endpoint distance, the distance
between two ordered indexed vertices is exactly the difference of the indices. -/
theorem geodesic_getVert_dist_eq_index_sub
    {G : SimpleGraph alpha} {u w : alpha} (p : G.Walk u w)
    (hp : p.length = G.dist u w) {i j : ℕ}
    (hi : i ≤ j) (hj : j ≤ p.length) :
    G.dist (p.getVert i) (p.getVert j) = j - i := by
  have hupper := dist_getVert_getVert_le_index_sub (G := G) p hi hj
  refine le_antisymm hupper ?_
  have hi_len : i ≤ p.length := le_trans hi hj
  let q : G.Walk (p.getVert i) (p.getVert j) :=
    ((p.drop i).take (j - i)).copy rfl (by
      rw [SimpleGraph.Walk.drop_getVert]
      have hji : j - i ≤ p.length - i := Nat.sub_le_sub_right hj i
      rw [add_tsub_cancel_of_le hi])
  obtain ⟨s, hs_len⟩ := q.reachable.exists_walk_length_eq_dist
  let r : G.Walk u w := ((p.take i).append s).append (p.drop j)
  have hdist_le : p.length ≤ r.length := by
    simpa [hp] using SimpleGraph.dist_le r
  have hr_len :
      r.length = i + G.dist (p.getVert i) (p.getVert j) + (p.length - j) := by
    simp [r, hs_len, SimpleGraph.Walk.take_length, SimpleGraph.Walk.drop_length,
      Nat.min_eq_left hi_len]
  rw [hr_len] at hdist_le
  omega

/-- On a geodesic walk, any graph edge between two ordered indexed vertices
can only connect consecutive indices. -/
theorem geodesic_getVert_adj_index_sub_eq_one
    {G : SimpleGraph alpha} {u w : alpha} (p : G.Walk u w)
    (hp : p.length = G.dist u w) {i j : ℕ}
    (hij : i < j) (hj : j ≤ p.length)
    (hadj : G.Adj (p.getVert i) (p.getVert j)) :
    j - i = 1 := by
  have hdist_eq :
      G.dist (p.getVert i) (p.getVert j) = j - i :=
    geodesic_getVert_dist_eq_index_sub (G := G) p hp (Nat.le_of_lt hij) hj
  have hdist_le_one :
      G.dist (p.getVert i) (p.getVert j) ≤ 1 := by
    simpa using SimpleGraph.dist_le hadj.toWalk
  have hpos : 0 < j - i := Nat.sub_pos_of_lt hij
  have hsub_le : j - i ≤ 1 := by
    simpa [hdist_eq] using hdist_le_one
  exact le_antisymm hsub_le (Nat.succ_le_iff.mpr hpos)

private lemma nat_mod_two_ne_succ (n : ℕ) : n % 2 ≠ (n + 1) % 2 := by
  intro h
  by_cases hn : Even n
  · have hn0 : n % 2 = 0 := Nat.even_iff.mp hn
    have hs0 : (n + 1) % 2 = 0 := by
      simpa [hn0] using h.symm
    have hsEven : Even (n + 1) := Nat.even_iff.mpr hs0
    exact (Nat.even_add_one.mp hsEven) hn
  · have hsEven : Even (n + 1) := Nat.even_add_one.mpr hn
    have hs0 : (n + 1) % 2 = 0 := Nat.even_iff.mp hsEven
    have hn0 : n % 2 = 0 := by
      simpa [hs0] using h
    exact hn (Nat.even_iff.mpr hn0)

private lemma nat_mod_two_ne_of_sub_eq_one {i j : ℕ}
    (hij : i < j) (hsub : j - i = 1) : i % 2 ≠ j % 2 := by
  have hji : j = i + 1 := by
    simpa [Nat.add_comm] using
      (Nat.sub_eq_iff_eq_add (Nat.le_of_lt hij)).mp hsub
  simpa [hji] using nat_mod_two_ne_succ i

private lemma nat_mod_two_succ_eq_zero_of_eq_one {n : ℕ} (hn : n % 2 = 1) :
    (n + 1) % 2 = 0 := by
  rcases Nat.mod_two_eq_zero_or_one (n + 1) with h0 | h1
  · exact h0
  · have hbad : n % 2 = (n + 1) % 2 := by
      rw [hn, h1]
    exact False.elim (nat_mod_two_ne_succ n hbad)

private lemma nat_mod_two_succ_eq_one_of_eq_zero {n : ℕ} (hn : n % 2 = 0) :
    (n + 1) % 2 = 1 := by
  rcases Nat.mod_two_eq_zero_or_one (n + 1) with h0 | h1
  · have hbad : n % 2 = (n + 1) % 2 := by
      rw [hn, h0]
    exact False.elim (nat_mod_two_ne_succ n hbad)
  · exact h1

private lemma geodesic_getVert_not_adj_of_same_parity
    {G : SimpleGraph alpha} {u v : alpha} (p : G.Walk u v)
    (hpDist : p.length = G.dist u v)
    {i j : ℕ}
    (hi : i ≤ p.length) (hj : j ≤ p.length)
    (hpar : i % 2 = j % 2)
    (hij_ne : i ≠ j) :
    ¬ G.Adj (p.getVert i) (p.getVert j) := by
  intro hadj
  rcases Nat.lt_trichotomy i j with hij | hij | hji
  · have hsub : j - i = 1 :=
      geodesic_getVert_adj_index_sub_eq_one (G := G) p hpDist hij hj hadj
    exact nat_mod_two_ne_of_sub_eq_one hij hsub hpar
  · exact hij_ne hij
  · have hsub : i - j = 1 :=
      geodesic_getVert_adj_index_sub_eq_one (G := G) p hpDist hji hi hadj.symm
    exact nat_mod_two_ne_of_sub_eq_one hji hsub hpar.symm

private lemma geodesic_path_parity_side_independent
    [Fintype alpha] [DecidableEq alpha]
    {G : SimpleGraph alpha} {u v : alpha} (p : G.Walk u v)
    (hpDist : p.length = G.dist u v) (r : ℕ) :
    G.IsIndepSet
      (((Finset.range (p.length + 1)).filter fun i => i % 2 = r).image p.getVert :
        Finset alpha) := by
  intro x hx y hy hxy_ne hxy
  change x ∈ (((Finset.range (p.length + 1)).filter fun i => i % 2 = r).image
    p.getVert : Finset alpha) at hx
  change y ∈ (((Finset.range (p.length + 1)).filter fun i => i % 2 = r).image
    p.getVert : Finset alpha) at hy
  rw [Finset.mem_image] at hx hy
  rcases hx with ⟨i, hi, rfl⟩
  rcases hy with ⟨j, hj, rfl⟩
  rw [Finset.mem_filter, Finset.mem_range] at hi hj
  rcases hi with ⟨hiRange, hiParity⟩
  rcases hj with ⟨hjRange, hjParity⟩
  have hi : i ≤ p.length := Nat.lt_succ_iff.mp hiRange
  have hj : j ≤ p.length := Nat.lt_succ_iff.mp hjRange
  have hij_ne : i ≠ j := by
    intro hij
    exact hxy_ne (by subst hij; rfl)
  have hpar : i % 2 = j % 2 := hiParity.trans hjParity.symm
  have hnot : ¬ G.Adj (p.getVert i) (p.getVert j) :=
    geodesic_getVert_not_adj_of_same_parity
      (G := G) p hpDist hi hj hpar hij_ne
  exact hnot hxy

private lemma geodesic_path_parity_sides_disjoint
    [Fintype alpha] [DecidableEq alpha]
    {G : SimpleGraph alpha} {u v : alpha} (p : G.Walk u v)
    (hpPath : p.IsPath) :
    Disjoint
      (((Finset.range (p.length + 1)).filter fun i => i % 2 = 0).image p.getVert :
        Finset alpha)
      (((Finset.range (p.length + 1)).filter fun i => i % 2 = 1).image p.getVert :
        Finset alpha) := by
  rw [Finset.disjoint_left]
  intro x hx hy
  rw [Finset.mem_image] at hx hy
  rcases hx with ⟨i, hi, hix⟩
  rcases hy with ⟨j, hj, hjx⟩
  rw [Finset.mem_filter, Finset.mem_range] at hi hj
  rcases hi with ⟨hiRange, hiParity⟩
  rcases hj with ⟨hjRange, hjParity⟩
  have hi : i ≤ p.length := by omega
  have hj : j ≤ p.length := by omega
  have hij : i = j :=
    hpPath.getVert_injOn (by simpa using hi) (by simpa using hj) (hix.trans hjx.symm)
  subst j
  exact Nat.zero_ne_one (hiParity.symm.trans hjParity)

private lemma geodesic_path_parity_sides_union
    [Fintype alpha] [DecidableEq alpha]
    {G : SimpleGraph alpha} {u v : alpha} (p : G.Walk u v) :
    ((((Finset.range (p.length + 1)).filter fun i => i % 2 = 0).image p.getVert :
        Finset alpha) ∪
      (((Finset.range (p.length + 1)).filter fun i => i % 2 = 1).image p.getVert :
        Finset alpha))
      = (Finset.range (p.length + 1)).image p.getVert := by
  ext x
  simp only [Finset.mem_union, Finset.mem_image, Finset.mem_filter]
  constructor
  · rintro (⟨i, hi, hix⟩ | ⟨i, hi, hix⟩)
    · exact ⟨i, hi.1, hix⟩
    · exact ⟨i, hi.1, hix⟩
  · rintro ⟨i, hiRange, hix⟩
    have hcases := Nat.mod_two_eq_zero_or_one i
    rcases hcases with h0 | h1
    · left
      exact ⟨i, ⟨hiRange, h0⟩, hix⟩
    · right
      exact ⟨i, ⟨hiRange, h1⟩, hix⟩

private lemma geodesic_path_vertex_set_isBipartite
    [Fintype alpha] [DecidableEq alpha]
    {G : SimpleGraph alpha} {u v : alpha} (p : G.Walk u v)
    (hpPath : p.IsPath)
    (hpDist : p.length = G.dist u v) :
    (G.induce (((Finset.range (p.length + 1)).image p.getVert : Finset alpha) : Set alpha)).IsBipartite := by
  classical
  let A : Finset alpha :=
    ((Finset.range (p.length + 1)).filter fun i => i % 2 = 0).image p.getVert
  let B : Finset alpha :=
    ((Finset.range (p.length + 1)).filter fun i => i % 2 = 1).image p.getVert
  have hA : G.IsIndepSet (A : Set alpha) := by
    dsimp [A]
    exact geodesic_path_parity_side_independent (G := G) p hpDist 0
  have hB : G.IsIndepSet (B : Set alpha) := by
    dsimp [B]
    exact geodesic_path_parity_side_independent (G := G) p hpDist 1
  have hdisj : Disjoint A B := by
    dsimp [A, B]
    exact geodesic_path_parity_sides_disjoint (G := G) p hpPath
  have hBip : (G.induce ((A ∪ B : Finset alpha) : Set alpha)).IsBipartite :=
    SimpleGraph.induce_union_indep_isBipartite (G := G) (A := A) (B := B) hA hB hdisj
  have hUnion :
      A ∪ B = (Finset.range (p.length + 1)).image p.getVert := by
    dsimp [A, B]
    exact geodesic_path_parity_sides_union (G := G) p
  have hUnionSet :
      ((A ∪ B : Finset alpha) : Set alpha) =
        (((Finset.range (p.length + 1)).image p.getVert : Finset alpha) : Set alpha) :=
    congrArg (fun s : Finset alpha => (s : Set alpha)) hUnion
  rw [← hUnionSet]
  exact hBip

lemma diam_add_one_le_b [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    {G : SimpleGraph alpha} (hconn : G.Connected) :
    G.diam + 1 ≤ b G := by
  classical
  rcases exists_diameter_walk_with_dist (G := G) hconn with
    ⟨u, v, p, hpPath, hpDist, hpDiam⟩
  let s : Finset alpha := (Finset.range (p.length + 1)).image p.getVert
  have hsBip : (G.induce (s : Set alpha)).IsBipartite := by
    dsimp [s]
    exact geodesic_path_vertex_set_isBipartite (G := G) p hpPath hpDist
  have hsCard : s.card = p.length + 1 := by
    dsimp [s]
    have hinj : Set.InjOn p.getVert (Finset.range (p.length + 1)) := by
      intro i hi j hj hij
      have hi' : i ≤ p.length := by
        exact Nat.lt_succ_iff.mp (by simpa using hi)
      have hj' : j ≤ p.length := by
        exact Nat.lt_succ_iff.mp (by simpa using hj)
      exact hpPath.getVert_injOn (by simpa using hi') (by simpa using hj') hij
    rw [Finset.card_image_of_injOn hinj]
    simp
  have hsLargest : s.card ≤ b G :=
    SimpleGraph.card_le_largestInducedBipartiteSubgraphSize_of_induce_isBipartite
      (G := G) (s := s) hsBip
  omega

private lemma nat_le_add_two_of_cast_le_two_add {m n : Nat}
    (h : ((m : Nat) : Real) ≤ 2 + (n : Real)) :
    m ≤ n + 2 := by
  have h' : ((m : Nat) : Real) ≤ ((n + 2 : Nat) : Real) := by
    calc
      ((m : Nat) : Real) ≤ 2 + (n : Real) := h
      _ = (n : Real) + 2 := by
        rw [add_comm]
      _ = (n : Real) + ((2 : Nat) : Real) := by
        rfl
      _ = ((n + 2 : Nat) : Real) := by
        rw [Nat.cast_add]
  exact Nat.cast_le.mp h'

private lemma nat_eq_add_one_or_two_of_bounds {m n : Nat}
    (hlower : n + 1 ≤ m) (hupper : m ≤ n + 2) :
    m = n + 1 ∨ m = n + 2 := by
  omega

lemma source_bound_forces_b_eq_diam_add_one_or_two
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (hb : ((b G : Nat) : Real) <= 2 + averageEccentricity G) :
    b G = G.diam + 1 ∨ b G = G.diam + 2 := by
  classical
  have hlower : G.diam + 1 ≤ b G :=
    diam_add_one_le_b (G := G) hconn
  have havg : averageEccentricity G ≤ (G.diam : Real) :=
    averageEccentricity_le_diam (G := G) hconn
  have hupper_real : ((b G : Nat) : Real) ≤ 2 + (G.diam : Real) := by
    calc
      ((b G : Nat) : Real) ≤ 2 + averageEccentricity G := hb
      _ ≤ 2 + (G.diam : Real) := by
        simpa using add_le_add_left havg (2 : Real)
  have hupper : b G ≤ G.diam + 2 := by
    exact nat_le_add_two_of_cast_le_two_add hupper_real
  exact nat_eq_add_one_or_two_of_bounds hlower hupper

private lemma diam_geodesic_dist_two_to_getVert_add_one_lt_diam
    {G : SimpleGraph alpha} {u v : alpha} (p : G.Walk u v)
    (_hpDist : p.length = G.dist u v) (hpDiam : p.length = G.diam)
    (hd4 : 4 ≤ G.diam) {j : ℕ} (hj : j ≤ p.length) :
    G.dist (p.getVert 2) (p.getVert j) + 1 < G.diam := by
  have hlen4 : 4 ≤ p.length := by
    simpa [hpDiam] using hd4
  by_cases h2j : 2 ≤ j
  · have hdist_le :
        G.dist (p.getVert 2) (p.getVert j) ≤ j - 2 :=
      dist_getVert_getVert_le_index_sub (G := G) p h2j hj
    have hlt : j - 2 + 1 < p.length := by
      obtain ⟨k, rfl⟩ := Nat.exists_eq_add_of_le h2j
      have hk2 : k + 2 ≤ p.length := by
        simpa [Nat.add_comm, Nat.add_left_comm, Nat.add_assoc] using hj
      exact Nat.succ_le_iff.mp (by
        simpa [Nat.add_assoc] using hk2)
    exact lt_of_le_of_lt (Nat.add_le_add_right hdist_le 1) (by
      simpa [← hpDiam] using hlt)
  · have hj2 : j ≤ 2 := le_of_not_ge h2j
    have h2len : 2 ≤ p.length := by
      exact le_trans (by decide : 2 ≤ 4) hlen4
    have hdist_le' :
        G.dist (p.getVert j) (p.getVert 2) ≤ 2 - j :=
      dist_getVert_getVert_le_index_sub (G := G) p hj2 h2len
    have hdist_le :
        G.dist (p.getVert 2) (p.getVert j) ≤ 2 - j := by
      simpa [SimpleGraph.dist_comm] using hdist_le'
    have hlt : 2 - j + 1 < p.length := by
      have hgap : 2 - j + 1 ≤ 3 :=
        Nat.add_le_add_right (Nat.sub_le 2 j) 1
      have h3lt : 3 < p.length := Nat.lt_of_succ_le hlen4
      exact Nat.lt_of_le_of_lt hgap h3lt
    have hmain :
        G.dist (p.getVert 2) (p.getVert j) + 1 < p.length :=
      Nat.lt_of_le_of_lt (Nat.add_le_add_right hdist_le 1) hlt
    simpa [← hpDiam] using hmain

private lemma diam_geodesic_dist_two_to_getVert_add_one_lt_diam_sub_one
    {G : SimpleGraph alpha} {u v : alpha} (p : G.Walk u v)
    (hpDist : p.length = G.dist u v) (hpDiam : p.length = G.diam)
    (hd4 : 4 ≤ G.diam) {j : ℕ} (hj : j ≤ p.length)
    (hpar : j % 2 = (G.diam + 1) % 2) :
    G.dist (p.getVert 2) (p.getVert j) + 1 < G.diam - 1 := by
  by_cases h2j : 2 ≤ j
  · have hdist :
        G.dist (p.getVert 2) (p.getVert j) = j - 2 :=
      geodesic_getVert_dist_eq_index_sub (G := G) p hpDist h2j hj
    have hj_ne_diam : j ≠ G.diam := by
      intro hjd
      have hbad : G.diam % 2 = (G.diam + 1) % 2 := by
        subst j
        exact hpar
      exact nat_mod_two_ne_succ G.diam hbad
    have hj_diam : j ≤ G.diam := by
      simpa [hpDiam] using hj
    have hj_lt : j < G.diam := lt_of_le_of_ne hj_diam hj_ne_diam
    have htarget : j - 2 + 1 < G.diam - 1 := by
      omega
    simpa [hdist] using htarget
  · have hj2 : j ≤ 2 := le_of_not_ge h2j
    have h2len : 2 ≤ p.length := by
      have h2diam : 2 ≤ G.diam := Nat.le_trans (by decide : 2 ≤ 4) hd4
      simpa [hpDiam] using h2diam
    have hdist' :
        G.dist (p.getVert j) (p.getVert 2) = 2 - j :=
      geodesic_getVert_dist_eq_index_sub (G := G) p hpDist hj2 h2len
    have hdist :
        G.dist (p.getVert 2) (p.getVert j) = 2 - j := by
      simpa [SimpleGraph.dist_comm] using hdist'
    rw [hdist]
    cases j with
    | zero =>
        have hd_ne4 : G.diam ≠ 4 := by
          intro hd
          have hbad : 0 = 1 := by
            simpa [hd] using hpar
          exact Nat.zero_ne_one hbad
        have hd_lt : 4 < G.diam := lt_of_le_of_ne hd4 (fun h => hd_ne4 h.symm)
        have hlt : 2 - 0 + 1 < G.diam - 1 := by
          omega
        simpa [hdist] using hlt
    | succ j =>
        cases j with
        | zero =>
            have hlt : 2 - 1 + 1 < G.diam - 1 := by
              omega
            simpa [hdist] using hlt
        | succ j =>
            cases j with
            | zero =>
                have hlt : 2 - 2 + 1 < G.diam - 1 := by
                  omega
                simpa [hdist] using hlt
            | succ j =>
                have hbad1 : j.succ.succ ≤ 1 := Nat.succ_le_succ_iff.mp hj2
                have hbad0 : j.succ ≤ 0 := Nat.succ_le_succ_iff.mp hbad1
                exact False.elim (Nat.not_succ_le_zero j hbad0)

private lemma two_extra_bipartite_lower_bound_from_sides
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha]
    (L R : Finset alpha) {x y : alpha}
    (hLind : G.IsIndepSet (L : Set alpha))
    (hRind : G.IsIndepSet (R : Set alpha))
    (hLRdisj : Disjoint L R)
    (hLRcard : L.card + R.card = G.diam + 1)
    (hx_no_L : ∀ z ∈ L, ¬ G.Adj x z)
    (hy_no_R : ∀ z ∈ R, ¬ G.Adj y z)
    (hx_not_L : x ∉ L)
    (hy_not_R : y ∉ R)
    (hy_not_L : y ∉ L)
    (hx_not_R : x ∉ R)
    (hxy_ne : x ≠ y) :
    G.diam + 3 ≤ b G := by
  classical
  let A : Finset alpha := L ∪ {x}
  let B : Finset alpha := R ∪ {y}
  have hA : G.IsIndepSet (A : Set alpha) := by
    intro a ha b hb hne hab
    simp only [A, Finset.mem_coe, Finset.mem_union, Finset.mem_singleton] at ha hb
    rcases ha with haL | rfl
    · rcases hb with hbL | rfl
      · exact hLind haL hbL hne hab
      · exact (hx_no_L a haL) hab.symm
    · rcases hb with hbL | rfl
      · exact (hx_no_L b hbL) hab
      · exact hne rfl
  have hB : G.IsIndepSet (B : Set alpha) := by
    intro a ha b hb hne hab
    simp only [B, Finset.mem_coe, Finset.mem_union, Finset.mem_singleton] at ha hb
    rcases ha with haR | rfl
    · rcases hb with hbR | rfl
      · exact hRind haR hbR hne hab
      · exact (hy_no_R a haR) hab.symm
    · rcases hb with hbR | rfl
      · exact (hy_no_R b hbR) hab
      · exact hne rfl
  have hdisj : Disjoint A B := by
    rw [Finset.disjoint_left]
    intro z hzA hzB
    simp only [A, B, Finset.mem_union, Finset.mem_singleton] at hzA hzB
    rcases hzA with hzL | rfl
    · rcases hzB with hzR | rfl
      · exact (Finset.disjoint_left.mp hLRdisj hzL) hzR
      · exact hy_not_L hzL
    · rcases hzB with hzR | hy
      · exact hx_not_R hzR
      · exact hxy_ne hy
  have hBip : (G.induce ((A ∪ B : Finset alpha) : Set alpha)).IsBipartite :=
    induce_union_indep_isBipartite (G := G) (A := A) (B := B) hA hB hdisj
  have hlower : (A ∪ B).card ≤ b G := by
    simpa [b] using
      card_le_largestInducedBipartiteSubgraphSize_of_induce_isBipartite
        (G := G) (s := A ∪ B) hBip
  have hAcard : A.card = L.card + 1 := by
    simpa [A, Finset.union_comm] using Finset.card_insert_of_notMem hx_not_L
  have hBcard : B.card = R.card + 1 := by
    simpa [B, Finset.union_comm] using Finset.card_insert_of_notMem hy_not_R
  have hcard : (A ∪ B).card = G.diam + 3 := by
    calc
      (A ∪ B).card = A.card + B.card :=
        Finset.card_union_of_disjoint hdisj
      _ = (L.card + 1) + (R.card + 1) := by
        rw [hAcard, hBcard]
      _ = L.card + R.card + 2 := by
        have hR : 1 + (R.card + 1) = R.card + 2 := by
          calc
            1 + (R.card + 1) = (1 + R.card) + 1 := by
              rw [Nat.add_assoc]
            _ = (R.card + 1) + 1 := by
              rw [Nat.add_comm 1 R.card]
            _ = R.card + 2 := by
              rfl
        calc
          (L.card + 1) + (R.card + 1) = L.card + (1 + (R.card + 1)) := by
            rw [Nat.add_assoc]
          _ = L.card + (R.card + 2) := by
            rw [hR]
          _ = L.card + R.card + 2 := by
            rw [Nat.add_assoc]
      _ = G.diam + 1 + 2 := by
        rw [hLRcard]
      _ = G.diam + 3 := by
        simp [Nat.add_assoc]
  rw [hcard] at hlower
  exact hlower

private lemma six_le_largestInducedBipartiteSubgraphSize_of_independent_union
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha]
    (A B : Finset alpha)
    (hA : G.IsIndepSet (A : Set alpha))
    (hB : G.IsIndepSet (B : Set alpha))
    (hdisj : Disjoint A B)
    (hcard : (A ∪ B).card = 6) :
    6 ≤ largestInducedBipartiteSubgraphSize G := by
  classical
  have hBip : (G.induce ((A ∪ B : Finset alpha) : Set alpha)).IsBipartite :=
    induce_union_indep_isBipartite (G := G) (A := A) (B := B) hA hB hdisj
  have hlower : (A ∪ B).card ≤ largestInducedBipartiteSubgraphSize G :=
    card_le_largestInducedBipartiteSubgraphSize_of_induce_isBipartite
      (G := G) (s := A ∪ B) hBip
  simpa [hcard] using hlower

private lemma not_adj_of_dist_eq_two
    {G : SimpleGraph alpha} {u v : alpha}
    (huv : G.dist u v = 2) :
    ¬ G.Adj u v := by
  intro hadj
  have hdist : G.dist u v = 1 := SimpleGraph.dist_eq_one_iff_adj.mpr hadj
  omega

/-- A maximum-cardinality independent finset witnessing `G.indepNum`. -/
private lemma exists_indep_set_card_indepNum
    (G : SimpleGraph alpha) [Fintype alpha] :
    ∃ I : Finset alpha, G.IsIndepSet (I : Set alpha) ∧ I.card = G.indepNum := by
  obtain ⟨I, hI⟩ := G.exists_isNIndepSet_indepNum
  rw [SimpleGraph.isNIndepSet_iff] at hI
  exact ⟨I, hI.1, hI.2⟩

private lemma indep_set_card_le_b
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha]
    {I : Finset alpha}
    (hI : G.IsIndepSet (I : Set alpha)) :
    I.card ≤ b G := by
  classical
  have hEmpty : G.IsIndepSet ((∅ : Finset alpha) : Set alpha) := by
    simp [SimpleGraph.IsIndepSet]
  have hdisj : Disjoint I (∅ : Finset alpha) := by
    simp
  have hBip : (G.induce ((I ∪ (∅ : Finset alpha) : Finset alpha) : Set alpha)).IsBipartite :=
    induce_union_indep_isBipartite (G := G) (A := I) (B := ∅) hI hEmpty hdisj
  have hlower : (I ∪ (∅ : Finset alpha)).card ≤ b G := by
    simpa [b] using
      card_le_largestInducedBipartiteSubgraphSize_of_induce_isBipartite
        (G := G) (s := I ∪ (∅ : Finset alpha)) hBip
  simpa using hlower

lemma b_eq_four_connected_forces_indepNum_le_three
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (G : SimpleGraph alpha)
    (hconn : G.Connected)
    (hb : b G = 4) :
    G.indepNum ≤ 3 := by
  classical
  by_contra hle
  have hfour : 4 ≤ G.indepNum := by
    omega
  obtain ⟨I, hIind, hIcard⟩ := exists_indep_set_card_indepNum (G := G)
  have hI_four : 4 ≤ I.card := by
    omega
  have hfive_b : 5 ≤ b G := by
    by_cases hI_five : 5 ≤ I.card
    · exact le_trans hI_five (indep_set_card_le_b (G := G) hIind)
    · have hI_card_four : I.card = 4 := by
        omega
      by_cases hcover : ∀ v : alpha, v ∈ I
      · have hle_bot : G ≤ ⊥ := by
          intro u v huv
          exact False.elim (hIind (hcover u) (hcover v) huv.ne huv)
        have hbot : G = ⊥ := le_antisymm hle_bot bot_le
        have hbot_conn : (⊥ : SimpleGraph alpha).Connected := by
          simpa [hbot] using hconn
        exact False.elim (not_connected_bot hbot_conn)
      · obtain ⟨v, hvI⟩ := not_forall.mp hcover
        let J : Finset alpha := I ∪ {v}
        have hsingleton : G.IsIndepSet (({v} : Finset alpha) : Set alpha) := by
          simp [SimpleGraph.IsIndepSet]
        have hdisj : Disjoint I ({v} : Finset alpha) := by
          rw [Finset.disjoint_singleton_right]
          exact hvI
        have hBip : (G.induce ((J : Finset alpha) : Set alpha)).IsBipartite := by
          dsimp [J]
          exact induce_union_indep_isBipartite
            (G := G) (A := I) (B := {v}) hIind hsingleton hdisj
        have hJ_le : J.card ≤ b G := by
          simpa [b] using
            card_le_largestInducedBipartiteSubgraphSize_of_induce_isBipartite
              (G := G) (s := J) hBip
        have hJ_card : J.card = 5 := by
          dsimp [J]
          rw [Finset.card_union_of_disjoint hdisj, hI_card_four]
          simp
        omega
  omega

private lemma exists_nonadjacent_vertex_of_eccent_toNat_eq_two
    {G : SimpleGraph alpha} [Fintype alpha]
    (hecc : ∀ v : alpha, (G.eccent v).toNat = 2) (v : alpha) :
    ∃ z : alpha, z ≠ v ∧ ¬ G.Adj v z := by
  classical
  obtain ⟨z, hz⟩ := G.exists_edist_eq_eccent_of_finite v
  refine ⟨z, ?_, ?_⟩
  · intro hzv
    have he0 : G.eccent v = 0 := by
      rw [← hz, hzv]
      simp
    have hbad : (0 : Nat) = 2 := by
      simpa [he0] using hecc v
    omega
  · intro hadj
    have hed1 : G.edist v z = 1 := SimpleGraph.edist_eq_one_iff_adj.mpr hadj
    have he1 : G.eccent v = 1 := by
      rw [← hz, hed1]
    have hbad : (1 : Nat) = 2 := by
      simpa [he1] using hecc v
    omega

private lemma dist_eq_two_of_diam_eq_two_of_ne_of_not_adj
    {G : SimpleGraph alpha} [Fintype alpha] [Nontrivial alpha]
    (hconn : G.Connected) (hdiam : G.diam = 2)
    {u z : alpha} (huz : u ≠ z) (hnadj : ¬ G.Adj u z) :
    G.dist u z = 2 := by
  have hgt : 1 < G.dist u z := hconn.one_lt_dist_of_ne_of_not_adj huz hnadj
  have hediam : G.ediam ≠ ⊤ := (SimpleGraph.connected_iff_ediam_ne_top (G := G)).mp hconn
  have hle : G.dist u z ≤ 2 := by
    simpa [hdiam] using SimpleGraph.dist_le_diam (G := G) hediam (u := u) (v := z)
  omega

lemma diam_two_all_ecc_two_forces_delete_connected
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (G : SimpleGraph alpha)
    (hconn : G.Connected)
    (hdiam : G.diam = 2)
    (hecc : ∀ v : alpha, (G.eccent v).toNat = 2) :
    ∀ x : alpha, ((⊤ : G.Subgraph).deleteVerts ({x} : Set alpha)).Connected := by
  classical
  intro v
  obtain ⟨z, hzv, hnot_vz⟩ := exists_nonadjacent_vertex_of_eccent_toNat_eq_two
    (G := G) hecc v
  let H : G.Subgraph := (⊤ : G.Subgraph).deleteVerts ({v} : Set alpha)
  have hzH : z ∈ H.verts := by
    dsimp [H]
    simp [hzv]
  have reach_to_z : ∀ x : H.verts, H.coe.Reachable x ⟨z, hzH⟩ := by
    intro x
    have hxv : x.1 ≠ v := by
      have hx := x.2
      dsimp [H] at hx
      simpa using hx.2
    by_cases hxz : x.1 = z
    · subst hxz
      rfl
    · by_cases hadj : G.Adj x.1 z
      · have hHadj : H.Adj x.1 z := by
          rw [SimpleGraph.Subgraph.deleteVerts_adj]
          exact ⟨by trivial, by simpa using hxv, by trivial, by simpa using hzv, hadj⟩
        exact (show H.coe.Adj x ⟨z, hzH⟩ from hHadj.coe).reachable
      · have hdist : G.dist x.1 z = 2 :=
          dist_eq_two_of_diam_eq_two_of_ne_of_not_adj
            (G := G) hconn hdiam hxz hadj
        obtain ⟨p, hp⟩ := hconn.exists_walk_length_eq_dist x.1 z
        have hp2 : p.length = 2 := by
          simpa [hdist] using hp
        let m : alpha := p.getVert 1
        have hxm : G.Adj x.1 m := by
          have hstep := p.adj_getVert_succ (by omega : 0 < p.length)
          simpa [m] using hstep
        have hget2 : p.getVert 2 = z := by
          rw [← hp2]
          exact p.getVert_length
        have hmz : G.Adj m z := by
          have hstep := p.adj_getVert_succ (by omega : 1 < p.length)
          simpa [m, hget2] using hstep
        have hmv : m ≠ v := by
          intro hmv
          have hvz : G.Adj v z := by
            simpa [hmv] using hmz
          exact hnot_vz hvz
        have hmH : m ∈ H.verts := by
          dsimp [H]
          simp [hmv]
        let mH : H.verts := ⟨m, hmH⟩
        have hHxm : H.coe.Adj x mH := by
          have hsub : H.Adj x.1 m := by
            rw [SimpleGraph.Subgraph.deleteVerts_adj]
            exact ⟨by trivial, by simpa using hxv, by trivial, by simpa using hmv, hxm⟩
          exact hsub.coe
        have hHmz : H.coe.Adj mH ⟨z, hzH⟩ := by
          have hsub : H.Adj m z := by
            rw [SimpleGraph.Subgraph.deleteVerts_adj]
            exact ⟨by trivial, by simpa using hmv, by trivial, by simpa using hzv, hmz⟩
          exact hsub.coe
        exact hHxm.reachable.trans hHmz.reachable
  refine SimpleGraph.Subgraph.Connected.mk ?_
  rw [SimpleGraph.connected_iff_exists_forall_reachable]
  refine ⟨⟨z, hzH⟩, ?_⟩
  intro x
  exact (reach_to_z x).symm

private lemma not_adj_of_adj_left_of_dist_eq_three
    {G : SimpleGraph alpha} (hconn : G.Connected) {u v w : alpha}
    (huv : G.Adj u v)
    (huw : G.dist u w = 3) :
    ¬ G.Adj v w := by
  intro hvw
  have htri : G.dist u w ≤ G.dist u v + G.dist v w := hconn.dist_triangle
  have huv_dist : G.dist u v = 1 := SimpleGraph.dist_eq_one_iff_adj.mpr huv
  have hvw_dist : G.dist v w = 1 := SimpleGraph.dist_eq_one_iff_adj.mpr hvw
  omega

private lemma not_adj_of_adj_right_of_dist_eq_three
    {G : SimpleGraph alpha} (hconn : G.Connected) {u v w : alpha}
    (huv : G.Adj u v)
    (hvw : G.dist v w = 3) :
    ¬ G.Adj u w := by
  intro huw
  have htri : G.dist v w ≤ G.dist v u + G.dist u w := hconn.dist_triangle
  have hvu_dist : G.dist v u = 1 := SimpleGraph.dist_eq_one_iff_adj.mpr huv.symm
  have huw_dist : G.dist u w = 1 := SimpleGraph.dist_eq_one_iff_adj.mpr huw
  omega

private lemma diam_three_distinct_interior_witness_lower_bound
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha]
    (hconn : G.Connected) {a b c d x y : alpha}
    (hab : G.Adj a b) (hbc : G.Adj b c) (hcd : G.Adj c d)
    (hac : G.dist a c = 2) (had : G.dist a d = 3) (hbd : G.dist b d = 2)
    (hbx : G.dist b x = 3) (hcy : G.dist c y = 3)
    (hxy : x ≠ y) :
    6 ≤ largestInducedBipartiteSubgraphSize G := by
  classical
  let A : Finset alpha := {a, c, x}
  let B : Finset alpha := {b, d, y}
  have hba : G.dist b a = 1 := SimpleGraph.dist_eq_one_iff_adj.mpr hab.symm
  have hbc_dist : G.dist b c = 1 := SimpleGraph.dist_eq_one_iff_adj.mpr hbc
  have hcb : G.dist c b = 1 := SimpleGraph.dist_eq_one_iff_adj.mpr hbc.symm
  have hcd_dist : G.dist c d = 1 := SimpleGraph.dist_eq_one_iff_adj.mpr hcd
  have hca : G.dist c a = 2 := by simpa [SimpleGraph.dist_comm] using hac
  have hdb : G.dist d b = 2 := by simpa [SimpleGraph.dist_comm] using hbd
  have hac_ne : a ≠ c := by
    intro h
    have h0 : G.dist a c = 0 := by simp [h]
    omega
  have had_ne : a ≠ d := by
    intro h
    have h0 : G.dist a d = 0 := by simp [h]
    omega
  have hax_ne : a ≠ x := by
    intro h
    have h1 : G.dist b x = 1 := by simpa [h] using hba
    omega
  have hcx_ne : c ≠ x := by
    intro h
    have h1 : G.dist b x = 1 := by simpa [h] using hbc_dist
    omega
  have hby_ne : b ≠ y := by
    intro h
    have h1 : G.dist c y = 1 := by simpa [h] using hcb
    omega
  have hdy_ne : d ≠ y := by
    intro h
    have h1 : G.dist c y = 1 := by simpa [h] using hcd_dist
    omega
  have hcy_ne : c ≠ y := by
    intro h
    have h0 : G.dist c y = 0 := by simp [h]
    omega
  have hbd_ne : b ≠ d := by
    intro h
    have h0 : G.dist b d = 0 := by simp [h]
    omega
  have hxb_ne : x ≠ b := by
    intro h
    have h0 : G.dist b x = 0 := by simp [h]
    omega
  have hxd_ne : x ≠ d := by
    intro h
    have h2 : G.dist b x = 2 := by simpa [h] using hbd
    omega
  have hay_ne : a ≠ y := by
    intro h
    have h2 : G.dist c y = 2 := by simpa [h] using hca
    omega
  have hAind : G.IsIndepSet (A : Set alpha) := by
    have h_ac : ¬ G.Adj a c := not_adj_of_dist_eq_two (G := G) hac
    have h_ax : ¬ G.Adj a x :=
      not_adj_of_adj_left_of_dist_eq_three (G := G) hconn hab.symm hbx
    have h_cx : ¬ G.Adj c x :=
      not_adj_of_adj_left_of_dist_eq_three (G := G) hconn hbc hbx
    intro u hu v hv huv_ne huv
    simp only [A, Finset.mem_coe, Finset.mem_insert, Finset.mem_singleton] at hu hv
    rcases hu with rfl | rfl | rfl <;> rcases hv with rfl | rfl | rfl
    · exact huv_ne rfl
    · exact h_ac huv
    · exact h_ax huv
    · exact h_ac huv.symm
    · exact huv_ne rfl
    · exact h_cx huv
    · exact h_ax huv.symm
    · exact h_cx huv.symm
    · exact huv_ne rfl
  have hBind : G.IsIndepSet (B : Set alpha) := by
    have h_bd : ¬ G.Adj b d := not_adj_of_dist_eq_two (G := G) hbd
    have h_by : ¬ G.Adj b y :=
      not_adj_of_adj_left_of_dist_eq_three (G := G) hconn hbc.symm hcy
    have h_dy : ¬ G.Adj d y :=
      not_adj_of_adj_left_of_dist_eq_three (G := G) hconn hcd hcy
    intro u hu v hv huv_ne huv
    simp only [B, Finset.mem_coe, Finset.mem_insert, Finset.mem_singleton] at hu hv
    rcases hu with rfl | rfl | rfl <;> rcases hv with rfl | rfl | rfl
    · exact huv_ne rfl
    · exact h_bd huv
    · exact h_by huv
    · exact h_bd huv.symm
    · exact huv_ne rfl
    · exact h_dy huv
    · exact h_by huv.symm
    · exact h_dy huv.symm
    · exact huv_ne rfl
  have hdisj : Disjoint A B := by
    rw [Finset.disjoint_left]
    intro z hzA hzB
    simp only [A, B, Finset.mem_insert, Finset.mem_singleton] at hzA hzB
    rcases hzA with rfl | rfl | rfl <;> rcases hzB with rfl | rfl | rfl
    · exact hab.ne rfl
    · exact had_ne rfl
    · exact hay_ne rfl
    · exact hbc.ne.symm rfl
    · exact hcd.ne rfl
    · exact hcy_ne rfl
    · exact hxb_ne rfl
    · exact hxd_ne rfl
    · exact hxy rfl
  have hAcard : A.card = 3 := by
    simp [A, hac_ne, hax_ne, hcx_ne]
  have hBcard : B.card = 3 := by
    simp [B, hbd_ne, hby_ne, hdy_ne]
  have hcard : (A ∪ B).card = 6 := by
    rw [Finset.card_union_of_disjoint hdisj, hAcard, hBcard]
  exact six_le_largestInducedBipartiteSubgraphSize_of_independent_union
    (G := G) A B hAind hBind hdisj hcard

private lemma pair_set_independent_of_not_adj
    {G : SimpleGraph alpha} {x y : alpha}
    (hxy : ¬ G.Adj x y) :
    G.IsIndepSet ({x, y} : Set alpha) := by
  intro u hu v hv huv_ne huv
  have hu_cases : u = x ∨ u = y := by
    exact Set.mem_insert_iff.mp hu
  have hv_cases : v = x ∨ v = y := by
    exact Set.mem_insert_iff.mp hv
  cases hu_cases with
  | inl hux =>
      cases hv_cases with
      | inl hvx => exact huv_ne (hux.trans hvx.symm)
      | inr hvy => exact hxy (by subst u; subst v; exact huv)
  | inr huy =>
      cases hv_cases with
      | inl hvx => exact hxy (by subst u; subst v; exact huv.symm)
      | inr hvy => exact huv_ne (huy.trans hvy.symm)

private lemma pair_finset_independent_of_not_adj
    [DecidableEq alpha] {G : SimpleGraph alpha} {x y : alpha}
    (hxy : ¬ G.Adj x y) :
    G.IsIndepSet ((({x, y} : Finset alpha)) : Set alpha) := by
  simpa using (pair_set_independent_of_not_adj (G := G) hxy)

private lemma diam_three_shared_interior_witness_lower_bound
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha]
    (hconn : G.Connected) {a b c d w z : alpha}
    (hab : G.Adj a b) (hbc : G.Adj b c) (hcd : G.Adj c d)
    (hac : G.dist a c = 2) (had : G.dist a d = 3) (hbd : G.dist b d = 2)
    (hbz : G.dist b z = 3) (hcz : G.dist c z = 3)
    (hbw : G.dist b w = 2) (hwz : G.Adj w z)
    (hdiam : G.diam = 3) :
    6 ≤ largestInducedBipartiteSubgraphSize G := by
  classical
  let L : Finset alpha := {a, c}
  let R : Finset alpha := {b, d}
  have hba : G.dist b a = 1 := SimpleGraph.dist_eq_one_iff_adj.mpr hab.symm
  have hbc_dist : G.dist b c = 1 := SimpleGraph.dist_eq_one_iff_adj.mpr hbc
  have hcd_dist : G.dist c d = 1 := SimpleGraph.dist_eq_one_iff_adj.mpr hcd
  have hzc : G.dist z c = 3 := by simpa [SimpleGraph.dist_comm] using hcz
  have hac_ne : a ≠ c := by
    intro h
    have h0 : G.dist a c = 0 := by simp [h]
    omega
  have had_ne : a ≠ d := by
    intro h
    have h0 : G.dist a d = 0 := by simp [h]
    omega
  have hbd_ne : b ≠ d := by
    intro h
    have h0 : G.dist b d = 0 := by simp [h]
    omega
  have h_ac : ¬ G.Adj a c := not_adj_of_dist_eq_two (G := G) hac
  have h_bd : ¬ G.Adj b d := not_adj_of_dist_eq_two (G := G) hbd
  have hLind : G.IsIndepSet (L : Set alpha) := by
    dsimp [L]
    exact pair_finset_independent_of_not_adj (G := G) h_ac
  have hRind : G.IsIndepSet (R : Set alpha) := by
    dsimp [R]
    exact pair_finset_independent_of_not_adj (G := G) h_bd
  have hLRdisj : Disjoint L R := by
    rw [Finset.disjoint_iff_ne]
    intro u hu r hr
    simp only [L, R, Finset.mem_insert, Finset.mem_singleton] at hu hr
    rcases hu with rfl | rfl
    · rcases hr with rfl | rfl
      · exact hab.ne
      · exact had_ne
    · rcases hr with rfl | rfl
      · exact hbc.ne.symm
      · exact hcd.ne
  have hLcard : L.card = 2 := by
    simp [L, hac_ne]
  have hRcard : R.card = 2 := by
    simp [R, hbd_ne]
  have hLRcard : L.card + R.card = G.diam + 1 := by
    rw [hLcard, hRcard, hdiam]
  have haz_ne : a ≠ z := by
    intro h
    have h1 : G.dist b z = 1 := by simpa [h] using hba
    omega
  have hbz_ne : b ≠ z := by
    intro h
    have h0 : G.dist b z = 0 := by simp [h]
    omega
  have hcz_ne : c ≠ z := by
    intro h
    have h0 : G.dist c z = 0 := by simp [h]
    omega
  have hdz_ne : d ≠ z := by
    intro h
    have h1 : G.dist c z = 1 := by simpa [h] using hcd_dist
    omega
  have hza_ne : z ≠ a := haz_ne.symm
  have hzb_ne : z ≠ b := hbz_ne.symm
  have hzc_ne' : z ≠ c := hcz_ne.symm
  have hzd_ne : z ≠ d := hdz_ne.symm
  have haw_ne : a ≠ w := by
    intro h
    have h1 : G.dist b w = 1 := by simpa [h] using hba
    omega
  have hbw_ne : b ≠ w := by
    intro h
    have h0 : (0 : Nat) = 2 := by
      simpa [h] using hbw
    omega
  have hcw_ne : c ≠ w := by
    intro h
    have h1 : G.dist b w = 1 := by simpa [h] using hbc_dist
    omega
  have hdw_ne : d ≠ w := by
    intro h
    subst h
    exact (not_adj_of_adj_left_of_dist_eq_three (G := G) hconn hcd hcz) hwz
  have hwa_ne : w ≠ a := haw_ne.symm
  have hwb_ne : w ≠ b := hbw_ne.symm
  have hwc_ne : w ≠ c := hcw_ne.symm
  have hwd_ne : w ≠ d := hdw_ne.symm
  have hwz_ne : w ≠ z := hwz.ne
  have h_az : ¬ G.Adj a z :=
    not_adj_of_adj_left_of_dist_eq_three (G := G) hconn hab.symm hbz
  have h_bz : ¬ G.Adj b z := by
    intro hbz_adj
    have h1 : G.dist b z = 1 := SimpleGraph.dist_eq_one_iff_adj.mpr hbz_adj
    omega
  have h_cz : ¬ G.Adj c z := by
    intro hcz_adj
    have h1 : G.dist c z = 1 := SimpleGraph.dist_eq_one_iff_adj.mpr hcz_adj
    omega
  have h_dz : ¬ G.Adj d z :=
    not_adj_of_adj_left_of_dist_eq_three (G := G) hconn hcd hcz
  have h_bw : ¬ G.Adj b w := not_adj_of_dist_eq_two (G := G) hbw
  have h_cw : ¬ G.Adj c w :=
    fun hcw => (not_adj_of_adj_left_of_dist_eq_three (G := G) hconn hwz.symm hzc) hcw.symm
  by_cases hwa : G.Adj w a
  · have h_dw : ¬ G.Adj d w := by
      intro hdw
      have htri : G.dist a d ≤ G.dist a w + G.dist w d := hconn.dist_triangle
      have haw_dist : G.dist a w = 1 := SimpleGraph.dist_eq_one_iff_adj.mpr hwa.symm
      have hwd_dist : G.dist w d = 1 := SimpleGraph.dist_eq_one_iff_adj.mpr hdw.symm
      omega
    have hz_no_L : ∀ t ∈ L, ¬ G.Adj z t := by
      intro t ht
      simp only [L, Finset.mem_insert, Finset.mem_singleton] at ht
      rcases ht with rfl | rfl
      · exact fun h => h_az h.symm
      · exact fun h => h_cz h.symm
    have hw_no_R : ∀ t ∈ R, ¬ G.Adj w t := by
      intro t ht
      simp only [R, Finset.mem_insert, Finset.mem_singleton] at ht
      rcases ht with rfl | rfl
      · exact fun h => h_bw h.symm
      · exact fun h => h_dw h.symm
    have hz_not_L : z ∉ L := by
      simp [L, hza_ne, hzc_ne']
    have hw_not_R : w ∉ R := by
      simp [R, hwb_ne, hwd_ne]
    have hw_not_L : w ∉ L := by
      simp [L, hwa_ne, hwc_ne]
    have hz_not_R : z ∉ R := by
      simp [R, hzb_ne, hzd_ne]
    have hlow : G.diam + 3 ≤ SimpleGraph.b G :=
      two_extra_bipartite_lower_bound_from_sides
        (G := G) (L := L) (R := R) (x := z) (y := w)
        hLind hRind hLRdisj hLRcard
        hz_no_L hw_no_R hz_not_L hw_not_R hw_not_L hz_not_R hwz_ne.symm
    have hlow' : 6 ≤ SimpleGraph.b G := by
      convert hlow using 1
      rw [hdiam]
    simpa [SimpleGraph.b] using hlow'
  · have hw_no_L : ∀ t ∈ L, ¬ G.Adj w t := by
      intro t ht
      simp only [L, Finset.mem_insert, Finset.mem_singleton] at ht
      rcases ht with rfl | rfl
      · exact hwa
      · exact fun h => h_cw h.symm
    have hz_no_R : ∀ t ∈ R, ¬ G.Adj z t := by
      intro t ht
      simp only [R, Finset.mem_insert, Finset.mem_singleton] at ht
      rcases ht with rfl | rfl
      · exact fun h => h_bz h.symm
      · exact fun h => h_dz h.symm
    have hw_not_L : w ∉ L := by
      simp [L, hwa_ne, hwc_ne]
    have hz_not_R : z ∉ R := by
      simp [R, hzb_ne, hzd_ne]
    have hz_not_L : z ∉ L := by
      simp [L, hza_ne, hzc_ne']
    have hw_not_R : w ∉ R := by
      simp [R, hwb_ne, hwd_ne]
    have hlow : G.diam + 3 ≤ SimpleGraph.b G :=
      two_extra_bipartite_lower_bound_from_sides
        (G := G) (L := L) (R := R) (x := w) (y := z)
        hLind hRind hLRdisj hLRcard
        hw_no_L hz_no_R hw_not_L hz_not_R hz_not_L hw_not_R hwz_ne
    have hlow' : 6 ≤ SimpleGraph.b G := by
      convert hlow using 1
      rw [hdiam]
    simpa [SimpleGraph.b] using hlow'

private lemma diam_geodesic_two_extra_bipartite_lower_bound
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    {u v x y : alpha} (p : G.Walk u v)
    (hpPath : p.IsPath)
    (hpDist : p.length = G.dist u v)
    (hpDiam : p.length = G.diam)
    (hd4 : 4 ≤ G.diam)
    (hcx : G.dist (p.getVert 2) x = G.diam)
    (hcy : G.dist (p.getVert 2) y = G.diam - 1)
    (hyx : G.Adj y x) :
    G.diam + 3 ≤ b G := by
  classical
  let E : Finset alpha :=
    ((Finset.range (p.length + 1)).filter fun i => i % 2 = 0).image p.getVert
  let O : Finset alpha :=
    ((Finset.range (p.length + 1)).filter fun i => i % 2 = 1).image p.getVert
  let Path : Finset alpha := (Finset.range (p.length + 1)).image p.getVert
  have hEind : G.IsIndepSet (E : Set alpha) := by
    dsimp [E]
    exact geodesic_path_parity_side_independent (G := G) p hpDist 0
  have hOind : G.IsIndepSet (O : Set alpha) := by
    dsimp [O]
    exact geodesic_path_parity_side_independent (G := G) p hpDist 1
  have hEOdisj : Disjoint E O := by
    dsimp [E, O]
    exact geodesic_path_parity_sides_disjoint (G := G) p hpPath
  have hEOunion : E ∪ O = Path := by
    dsimp [E, O, Path]
    exact geodesic_path_parity_sides_union (G := G) p
  have hPath_card : Path.card = G.diam + 1 := by
    dsimp [Path]
    have hinj : Set.InjOn p.getVert (Finset.range (p.length + 1)) := by
      intro i hi j hj hij
      have hi' : i ≤ p.length := Nat.lt_succ_iff.mp (by simpa using hi)
      have hj' : j ≤ p.length := Nat.lt_succ_iff.mp (by simpa using hj)
      exact hpPath.getVert_injOn (by simpa using hi') (by simpa using hj') hij
    rw [Finset.card_image_of_injOn hinj]
    simp [hpDiam]
  have hE_subset_Path : E ⊆ Path := by
    intro z hz
    rw [← hEOunion]
    exact Finset.mem_union.mpr (Or.inl hz)
  have hO_subset_Path : O ⊆ Path := by
    intro z hz
    rw [← hEOunion]
    exact Finset.mem_union.mpr (Or.inr hz)
  have hx_no_path : ∀ z ∈ Path, ¬ G.Adj x z := by
    intro z hz hxz
    dsimp [Path] at hz
    rw [Finset.mem_image] at hz
    rcases hz with ⟨j, hj, rfl⟩
    have hjle : j ≤ p.length := Nat.lt_succ_iff.mp (by simpa using hj)
    have htri :
        G.dist (p.getVert 2) x ≤
          G.dist (p.getVert 2) (p.getVert j) + G.dist (p.getVert j) x :=
      hconn.dist_triangle
    have hadj_le : G.dist (p.getVert j) x ≤ 1 := by
      simpa using SimpleGraph.dist_le hxz.symm.toWalk
    have hlt :=
      diam_geodesic_dist_two_to_getVert_add_one_lt_diam
        (G := G) p hpDist hpDiam hd4 hjle
    rw [hcx] at htri
    have hsum_le :
        G.dist (p.getVert 2) (p.getVert j) + G.dist (p.getVert j) x ≤
          G.dist (p.getVert 2) (p.getVert j) + 1 :=
      Nat.add_le_add_left hadj_le _
    exact (not_lt_of_ge htri) (lt_of_le_of_lt hsum_le hlt)
  have hx_not_path : x ∉ Path := by
    intro hx
    dsimp [Path] at hx
    rw [Finset.mem_image] at hx
    rcases hx with ⟨j, hj, hxj⟩
    have hjle : j ≤ p.length := Nat.lt_succ_iff.mp (by simpa using hj)
    have hlt :=
      diam_geodesic_dist_two_to_getVert_add_one_lt_diam
        (G := G) p hpDist hpDiam hd4 hjle
    have hcxj : G.dist (p.getVert 2) (p.getVert j) = G.diam := by
      simpa [hxj] using hcx
    rw [hcxj] at hlt
    exact (Nat.not_succ_le_self G.diam) (Nat.le_of_lt hlt)
  have hy_not_path : y ∉ Path := by
    intro hy
    dsimp [Path] at hy
    rw [Finset.mem_image] at hy
    rcases hy with ⟨j, hj, hyj⟩
    have hjle : j ≤ p.length := Nat.lt_succ_iff.mp (by simpa using hj)
    have hlt :=
      diam_geodesic_dist_two_to_getVert_add_one_lt_diam
        (G := G) p hpDist hpDiam hd4 hjle
    have hcyj : G.dist (p.getVert 2) (p.getVert j) = G.diam - 1 := by
      simpa [hyj] using hcy
    rw [hcyj] at hlt
    have hsucc : G.diam - 1 + 1 = G.diam := by
      exact Nat.sub_add_cancel (Nat.le_trans (by decide : 1 ≤ 4) hd4)
    rw [hsucc] at hlt
    exact (not_lt_of_ge (le_refl G.diam)) hlt
  have hxy_ne : x ≠ y := hyx.ne.symm
  have hx_no_E : ∀ z ∈ E, ¬ G.Adj x z := by
    intro z hz
    exact hx_no_path z (hE_subset_Path hz)
  have hx_no_O : ∀ z ∈ O, ¬ G.Adj x z := by
    intro z hz
    exact hx_no_path z (hO_subset_Path hz)
  have hy_no_same_parity :
      ∀ z ∈ Path, (∃ j ∈ Finset.range (p.length + 1),
        p.getVert j = z ∧ j % 2 = (G.diam + 1) % 2) → ¬ G.Adj y z := by
    intro z _hz hzdata hyz
    rcases hzdata with ⟨j, hj, rfl, hjpar⟩
    have hjle : j ≤ p.length := Nat.lt_succ_iff.mp (by simpa using hj)
    have htri :
        G.dist (p.getVert 2) y ≤
          G.dist (p.getVert 2) (p.getVert j) + G.dist (p.getVert j) y :=
      hconn.dist_triangle
    have hadj_le : G.dist (p.getVert j) y ≤ 1 := by
      simpa using SimpleGraph.dist_le hyz.symm.toWalk
    have hlt :=
      diam_geodesic_dist_two_to_getVert_add_one_lt_diam_sub_one
        (G := G) p hpDist hpDiam hd4 hjle hjpar
    rw [hcy] at htri
    have hsum_le :
        G.dist (p.getVert 2) (p.getVert j) + G.dist (p.getVert j) y ≤
          G.dist (p.getVert 2) (p.getVert j) + 1 :=
      Nat.add_le_add_left hadj_le _
    exact (not_lt_of_ge htri) (lt_of_le_of_lt hsum_le hlt)
  have hy_no_E_of_odd_diam : G.diam % 2 = 1 → ∀ z ∈ E, ¬ G.Adj y z := by
    intro hd1 z hz
    have hzPath : z ∈ Path := hE_subset_Path hz
    refine hy_no_same_parity z hzPath ?_
    dsimp [E] at hz
    rw [Finset.mem_image] at hz
    rcases hz with ⟨j, hj, rfl⟩
    rw [Finset.mem_filter] at hj
    refine ⟨j, hj.1, rfl, ?_⟩
    rw [hj.2]
    exact (nat_mod_two_succ_eq_zero_of_eq_one hd1).symm
  have hy_no_O_of_even_diam : G.diam % 2 = 0 → ∀ z ∈ O, ¬ G.Adj y z := by
    intro hd0 z hz
    have hzPath : z ∈ Path := hO_subset_Path hz
    refine hy_no_same_parity z hzPath ?_
    dsimp [O] at hz
    rw [Finset.mem_image] at hz
    rcases hz with ⟨j, hj, rfl⟩
    rw [Finset.mem_filter] at hj
    refine ⟨j, hj.1, rfl, ?_⟩
    rw [hj.2]
    exact (nat_mod_two_succ_eq_one_of_eq_zero hd0).symm
  have hcases := Nat.mod_two_eq_zero_or_one G.diam
  rcases hcases with hd0 | hd1
  · have hEOcard : E.card + O.card = G.diam + 1 := by
      have h := Finset.card_union_of_disjoint hEOdisj
      rw [hEOunion, hPath_card] at h
      exact h.symm
    exact two_extra_bipartite_lower_bound_from_sides
      (G := G) (L := E) (R := O) (x := x) (y := y)
      hEind hOind hEOdisj hEOcard
      hx_no_E (hy_no_O_of_even_diam hd0)
      (fun hxE => hx_not_path (hE_subset_Path hxE))
      (fun hyO => hy_not_path (hO_subset_Path hyO))
      (fun hyE => hy_not_path (hE_subset_Path hyE))
      (fun hxO => hx_not_path (hO_subset_Path hxO))
      hxy_ne
  · have hOEcard : O.card + E.card = G.diam + 1 := by
      have h := Finset.card_union_of_disjoint hEOdisj
      rw [hEOunion, hPath_card] at h
      omega
    exact two_extra_bipartite_lower_bound_from_sides
      (G := G) (L := O) (R := E) (x := x) (y := y)
      hOind hEind hEOdisj.symm hOEcard
      hx_no_O (hy_no_E_of_odd_diam hd1)
      (fun hxO => hx_not_path (hO_subset_Path hxO))
      (fun hyE => hy_not_path (hE_subset_Path hyE))
      (fun hyO => hy_not_path (hO_subset_Path hyO))
      (fun hxE => hx_not_path (hE_subset_Path hxE))
      hxy_ne

lemma exists_walk_of_chain_cons_visible
    (G : SimpleGraph alpha)
    (a : alpha)
    (tail : List alpha)
    (hchain : List.IsChain G.Adj (a :: tail)) :
    ∃ b : alpha, ∃ p : G.Walk a b,
      p.support = a :: tail := by
  induction tail generalizing a with
  | nil =>
      exact ⟨a, Walk.nil, by simp⟩
  | cons b rest ih =>
      cases hchain with
      | cons_cons hab htail =>
      rcases ih b htail with ⟨c, p, hp⟩
      refine ⟨c, Walk.cons hab p, ?_⟩
      rw [Walk.support_cons, hp]

lemma all_eccent_eq_diam_large_diam_forces_diam_add_three_le_largestInducedBipartiteSubgraphSize
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (hecc : forall v : alpha, (G.eccent v).toNat = G.diam)
    (hdiam : 4 <= G.diam) :
    G.diam + 3 <= largestInducedBipartiteSubgraphSize G := by
  classical
  rcases exists_diameter_walk_with_dist (G := G) hconn with
    ⟨u, v, p, hpPath, hpDist, hpDiam⟩
  let c : alpha := p.getVert 2
  obtain ⟨x, hx_ecc⟩ := G.exists_edist_eq_eccent_of_finite c
  have hcx : G.dist c x = G.diam := by
    rw [SimpleGraph.dist, hx_ecc, hecc c]
  obtain ⟨q, hqdist⟩ := hconn.exists_walk_length_eq_dist c x
  have hq_len : q.length = G.diam := by
    rw [hqdist, hcx]
  let y : alpha := q.getVert (G.diam - 1)
  have hcy : G.dist c y = G.diam - 1 := by
    have hd1_le : G.diam - 1 ≤ q.length := by
      simpa [hq_len] using Nat.sub_le G.diam 1
    have hdist :=
      geodesic_getVert_dist_eq_index_sub (G := G) q hqdist
        (Nat.zero_le _) hd1_le
    simpa [c, y, hq_len] using hdist
  have hyx : G.Adj y x := by
    have hlt : G.diam - 1 < q.length := by
      have hdpos : 0 < G.diam := Nat.lt_of_lt_of_le (by decide : 0 < 4) hdiam
      simpa [hq_len] using Nat.sub_one_lt hdpos.ne'
    have hadj := q.adj_getVert_succ hlt
    have hsucc : G.diam - 1 + 1 = G.diam :=
      Nat.sub_add_cancel (Nat.le_trans (by decide : 1 ≤ 4) hdiam)
    have hlast : q.getVert (G.diam - 1 + 1) = x := by
      rw [hsucc]
      simpa [← hq_len] using q.getVert_length
    simpa [y, hlast] using hadj
  have hlower : G.diam + 3 ≤ b G :=
    diam_geodesic_two_extra_bipartite_lower_bound
      (G := G) hconn p hpPath hpDist hpDiam hdiam hcx hcy hyx
  exact hlower

lemma all_eccent_eq_diam_diam_eq_three_forces_six_le_largestInducedBipartiteSubgraphSize
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (hecc : forall v : alpha, (G.eccent v).toNat = G.diam)
    (hdiam : G.diam = 3) :
    6 <= largestInducedBipartiteSubgraphSize G := by
  classical
  rcases exists_diameter_walk_with_dist (G := G) hconn with
    ⟨u, v, p, _hpPath, hpDist, hpDiam⟩
  have hp_len : p.length = 3 := by
    rw [hpDiam, hdiam]
  let a : alpha := p.getVert 0
  let b : alpha := p.getVert 1
  let c : alpha := p.getVert 2
  let d : alpha := p.getVert 3
  have hab : G.Adj a b := by
    have h := p.adj_getVert_succ (by simpa [hp_len] : 0 < p.length)
    simpa [a, b] using h
  have hbc : G.Adj b c := by
    have h := p.adj_getVert_succ (by simpa [hp_len] : 1 < p.length)
    simpa [b, c] using h
  have hcd : G.Adj c d := by
    have h := p.adj_getVert_succ (by simpa [hp_len] : 2 < p.length)
    simpa [c, d] using h
  have hac : G.dist a c = 2 := by
    have hdist :=
      geodesic_getVert_dist_eq_index_sub (G := G) p hpDist
        (Nat.zero_le 2) (by simpa [hp_len] : 2 ≤ p.length)
    simpa [a, c] using hdist
  have had : G.dist a d = 3 := by
    have hdist :=
      geodesic_getVert_dist_eq_index_sub (G := G) p hpDist
        (Nat.zero_le 3) (by simpa [hp_len] : 3 ≤ p.length)
    simpa [a, d] using hdist
  have hbd : G.dist b d = 2 := by
    have hdist :=
      geodesic_getVert_dist_eq_index_sub (G := G) p hpDist
        (by decide : 1 ≤ 3) (by simpa [hp_len] : 3 ≤ p.length)
    simpa [b, d] using hdist
  obtain ⟨x, hx_ecc⟩ := G.exists_edist_eq_eccent_of_finite b
  have hbx : G.dist b x = 3 := by
    rw [SimpleGraph.dist, hx_ecc, hecc b, hdiam]
  obtain ⟨y, hy_ecc⟩ := G.exists_edist_eq_eccent_of_finite c
  have hcy : G.dist c y = 3 := by
    rw [SimpleGraph.dist, hy_ecc, hecc c, hdiam]
  by_cases hxy : x ≠ y
  · exact diam_three_distinct_interior_witness_lower_bound
      (G := G) hconn hab hbc hcd hac had hbd hbx hcy hxy
  · have hxy_eq : x = y := not_not.mp hxy
    obtain ⟨q, hqdist⟩ := hconn.exists_walk_length_eq_dist b x
    have hq_len : q.length = 3 := by
      rw [hqdist, hbx]
    let w : alpha := q.getVert 2
    have hbw : G.dist b w = 2 := by
      have hdist :=
        geodesic_getVert_dist_eq_index_sub (G := G) q hqdist (i := 0) (j := 2)
          (Nat.zero_le 2) (by simpa [hq_len] : 2 ≤ q.length)
      simpa [w] using hdist
    have hwx : G.Adj w x := by
      have hadj := q.adj_getVert_succ (by simpa [hq_len] : 2 < q.length)
      have hlast : q.getVert (2 + 1) = x := by
        simpa [hq_len] using q.getVert_length
      simpa [w, hlast] using hadj
    have hcx : G.dist c x = 3 := by
      simpa [hxy_eq] using hcy
    exact diam_three_shared_interior_witness_lower_bound
      (G := G) hconn hab hbc hcd hac had hbd hbx hcx hbw hwx hdiam

lemma b_eq_diam_add_two_all_eccent_eq_diam_forces_diam_le_three
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (hb2 : b G = G.diam + 2)
    (hecc : forall v : alpha, (G.eccent v).toNat = G.diam) :
    G.diam <= 3 := by
  classical
  by_contra hdiam_not
  have hdiam : 4 <= G.diam :=
    Nat.succ_le_of_lt (Nat.lt_of_not_ge hdiam_not)
  have hlower : G.diam + 3 ≤ b G := by
    simpa [b] using
      all_eccent_eq_diam_large_diam_forces_diam_add_three_le_largestInducedBipartiteSubgraphSize
        (G := G) hconn hecc hdiam
  rw [hb2] at hlower
  exact (Nat.not_succ_le_self (G.diam + 2)) (by
    simpa [Nat.add_assoc] using hlower)

lemma b_eq_diam_add_two_all_eccent_eq_diam_forces_diam_le_two
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (G : SimpleGraph alpha)
    (hconn : G.Connected)
    (hb2 : b G = G.diam + 2)
    (hecc : ∀ v : alpha, (G.eccent v).toNat = G.diam) :
    G.diam ≤ 2 := by
  classical
  have hle3 : G.diam ≤ 3 :=
    b_eq_diam_add_two_all_eccent_eq_diam_forces_diam_le_three
      (G := G) (hconn := hconn) (hb2 := hb2) (hecc := hecc)
  by_contra hnot
  have hge3 : 3 ≤ G.diam := Nat.succ_le_of_lt (Nat.lt_of_not_ge hnot)
  have hdiam : G.diam = 3 := le_antisymm hle3 hge3
  have hlower : 6 ≤ b G := by
    simpa [b] using
      all_eccent_eq_diam_diam_eq_three_forces_six_le_largestInducedBipartiteSubgraphSize
        (G := G) hconn hecc hdiam
  rw [hb2, hdiam] at hlower
  exact (Nat.not_succ_le_self 5) (by simpa using hlower)

private lemma source_bound_average_eq_diam_of_b_eq_diam_add_two
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (hb : ((b G : Nat) : Real) <= 2 + averageEccentricity G)
    (hb2 : b G = G.diam + 2) :
    averageEccentricity G = (G.diam : Real) := by
  apply le_antisymm (averageEccentricity_le_diam (G := G) hconn)
  have hsource :
      (G.diam : Real) + 2 <= 2 + averageEccentricity G := by
    calc
      (G.diam : Real) + 2 = ((G.diam + 2 : Nat) : Real) := by
        simp [Nat.cast_add]
      _ = ((b G : Nat) : Real) := by
        exact congrArg (fun n : Nat => (n : Real)) hb2.symm
      _ <= 2 + averageEccentricity G := hb
  have hsource' :
      (G.diam : Real) + 2 <= averageEccentricity G + 2 := by
    simpa [add_comm] using hsource
  exact (add_le_add_iff_right (2 : Real)).mp hsource'

private lemma averageEccentricity_eq_diam_forces_all_eccent_toNat_eq_diam
    [Fintype alpha] [Nonempty alpha]
    {G : SimpleGraph alpha}
    (hconn : G.Connected)
    (havg : averageEccentricity G = (G.diam : Real)) :
    ∀ v : alpha, (G.eccent v).toNat = G.diam := by
  classical
  have hcard_pos : 0 < (Fintype.card alpha : Real) := by
    exact_mod_cast Fintype.card_pos
  have hsum_eq :
      (∑ v : alpha, ((G.eccent v).toNat : Real)) =
        (Fintype.card alpha : Real) * (G.diam : Real) := by
    have hm :=
      congrArg (fun x : Real => x * (Fintype.card alpha : Real)) havg
    unfold averageEccentricity at hm
    change
      ((∑ v : alpha, ((G.eccent v).toNat : Real)) / (Fintype.card alpha : Real)) *
          (Fintype.card alpha : Real) =
        (G.diam : Real) * (Fintype.card alpha : Real) at hm
    rw [div_mul_cancel₀ _ hcard_pos.ne'] at hm
    simpa [mul_comm] using hm
  have hdefsum :
      (∑ v : alpha, ((G.diam : Real) - ((G.eccent v).toNat : Real))) = 0 := by
    rw [Finset.sum_sub_distrib, Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
    rw [hsum_eq, sub_self]
  have hnonneg :
      ∀ v ∈ (Finset.univ : Finset alpha),
        0 <= ((G.diam : Real) - ((G.eccent v).toNat : Real)) := by
    intro v _hv
    exact sub_nonneg.mpr (by
      exact_mod_cast eccent_toNat_le_diam (G := G) hconn v)
  have hzero_all :
      ∀ v ∈ (Finset.univ : Finset alpha),
        ((G.diam : Real) - ((G.eccent v).toNat : Real)) = 0 :=
    (Finset.sum_eq_zero_iff_of_nonneg hnonneg).mp (by simpa using hdefsum)
  intro v
  have hvzero :
      ((G.diam : Real) - ((G.eccent v).toNat : Real)) = 0 :=
    hzero_all v (Finset.mem_univ v)
  have hcast : ((G.eccent v).toNat : Real) = (G.diam : Real) := by
    exact (sub_eq_zero.mp hvzero).symm
  exact_mod_cast hcast

lemma source_bound_forces_all_eccent_eq_diam_of_b_eq_diam_add_two
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (hb : ((b G : Nat) : Real) <= 2 + averageEccentricity G)
    (hb2 : b G = G.diam + 2) :
    ∀ v : alpha, (G.eccent v).toNat = G.diam := by
  exact averageEccentricity_eq_diam_forces_all_eccent_toNat_eq_diam
    (G := G) hconn
    (source_bound_average_eq_diam_of_b_eq_diam_add_two
      (G := G) (hconn := hconn) (hb := hb) (hb2 := hb2))

private lemma completeGraph_induced_bipartite_card_le_two
    (s : Finset alpha) [Fintype alpha] [DecidableEq alpha]
    (hs : ((⊤ : SimpleGraph alpha).induce (s : Set alpha)).IsBipartite) :
    s.card ≤ 2 := by
  classical
  have hs' : (completeGraph ↥(s : Set alpha)).Colorable 2 := by
    simpa using hs
  have hclique :
      (completeGraph ↥(s : Set alpha)).IsClique
        ((Finset.univ : Finset ↥(s : Set alpha)) : Set ↥(s : Set alpha)) := by
    intro a _ha b _hb hab
    exact (SimpleGraph.top_adj a b).mpr hab
  have hcard := hclique.card_le_of_colorable hs'
  simpa [Finset.coe_sort_coe, Fintype.card_coe] using hcard

private lemma b_completeGraph_le_two
    [Fintype alpha] [DecidableEq alpha] :
    b (⊤ : SimpleGraph alpha) ≤ 2 := by
  classical
  unfold b largestInducedBipartiteSubgraphSize
  apply csSup_le
  · exact ⟨0, by
      refine ⟨∅, ?_, rfl⟩
      simpa using (show ((⊤ : SimpleGraph alpha).induce ((∅ : Finset alpha) : Set alpha)).IsBipartite
        from ⟨Coloring.mk
          (fun _ : ↥(((∅ : Finset alpha) : Set alpha)) => (0 : Fin 2))
          (by intro v _w _h; cases v.2)⟩)⟩
  · intro n hn
    rcases hn with ⟨s, hs, rfl⟩
    exact completeGraph_induced_bipartite_card_le_two (s := s) hs

lemma source_bound_b_eq_diam_add_two_forces_diam_eq_two
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (hb : ((b G : Nat) : Real) <= 2 + averageEccentricity G)
    (hb2 : b G = G.diam + 2) :
    G.diam = 2 := by
  classical
  have hecc : ∀ v : alpha, (G.eccent v).toNat = G.diam :=
    source_bound_forces_all_eccent_eq_diam_of_b_eq_diam_add_two
      (G := G) (hconn := hconn) (hb := hb) (hb2 := hb2)
  have hle : G.diam ≤ 2 :=
    b_eq_diam_add_two_all_eccent_eq_diam_forces_diam_le_two
      (G := G) (hconn := hconn) (hb2 := hb2) (hecc := hecc)
  have hne : G.diam ≠ 0 :=
    (SimpleGraph.connected_iff_diam_ne_zero (G := G)).mp hconn
  have hcases : G.diam = 1 ∨ G.diam = 2 := by
    omega
  rcases hcases with hdiam | hdiam
  · have htop : G = ⊤ := (SimpleGraph.diam_eq_one (G := G)).mp hdiam
    have hb_le_two : b G ≤ 2 := by
      simpa [htop] using (b_completeGraph_le_two (alpha := alpha))
    rw [hb2, hdiam] at hb_le_two
    omega
  · exact hdiam

lemma source_bound_b_eq_diam_add_two_forces_reduced_branch
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (G : SimpleGraph alpha)
    (hconn : G.Connected)
    (hb : ((b G : Nat) : Real) <= 2 + averageEccentricity G)
    (hb2 : b G = G.diam + 2) :
    G.diam = 2 ∧
    b G = 4 ∧
    (∀ v : alpha, (G.eccent v).toNat = 2) ∧
    (∀ x : alpha, ((⊤ : G.Subgraph).deleteVerts ({x} : Set alpha)).Connected) ∧
    G.indepNum ≤ 3 := by
  classical
  have heccDiam : ∀ v : alpha, (G.eccent v).toNat = G.diam :=
    source_bound_forces_all_eccent_eq_diam_of_b_eq_diam_add_two
      (G := G) (hconn := hconn) (hb := hb) (hb2 := hb2)
  have hdiam : G.diam = 2 :=
    source_bound_b_eq_diam_add_two_forces_diam_eq_two
      (G := G) (hconn := hconn) (hb := hb) (hb2 := hb2)
  have hb4 : b G = 4 := by
    rw [hb2, hdiam]
  have hecc2 : ∀ v : alpha, (G.eccent v).toNat = 2 := by
    intro v
    simpa [hdiam] using heccDiam v
  have hdelete :
      ∀ x : alpha, ((⊤ : G.Subgraph).deleteVerts ({x} : Set alpha)).Connected :=
    diam_two_all_ecc_two_forces_delete_connected
      (G := G) (hconn := hconn) (hdiam := hdiam) (hecc := hecc2)
  have hindep : G.indepNum ≤ 3 :=
    b_eq_four_connected_forces_indepNum_le_three
      (G := G) (hconn := hconn) (hb := hb4)
  exact ⟨hdiam, hb4, hecc2, hdelete, hindep⟩

/-- The left endpoint of the edge indexed by `i` on a path with `G.diam + 1`
vertices. -/
def edgeLeft (G : SimpleGraph alpha) (i : Fin G.diam) : Fin (G.diam + 1) :=
  ⟨i.val, Nat.lt_succ_of_lt i.isLt⟩

/-- The right endpoint of the edge indexed by `i` on a path with `G.diam + 1`
vertices. -/
def edgeRight (G : SimpleGraph alpha) (i : Fin G.diam) : Fin (G.diam + 1) :=
  ⟨i.val + 1, Nat.succ_lt_succ i.isLt⟩

/-- Local certificate data for a diametral geodesic path indexed from `0` to
`G.diam`. The `dist_eq` field packages the standard shortcut-exclusion fact for
subsegments of a geodesic. -/
structure IsDiametralGeodesic (G : SimpleGraph alpha)
    (P : Fin (G.diam + 1) → alpha) : Prop where
  endpoints_dist :
    G.dist (P ⟨0, Nat.succ_pos _⟩) (P ⟨G.diam, Nat.lt_succ_self _⟩) = G.diam
  injective : Function.Injective P
  adj_succ : ∀ i : Fin G.diam, G.Adj (P (edgeLeft G i)) (P (edgeRight G i))
  dist_eq : ∀ a b : Fin (G.diam + 1),
    G.dist (P a) (P b) =
      if a.val ≤ b.val then b.val - a.val else a.val - b.val

lemma exists_isDiametralGeodesic
    [Fintype alpha] [Nonempty alpha] (G : SimpleGraph alpha) (hconn : G.Connected) :
    ∃ P : Fin (G.diam + 1) → alpha, IsDiametralGeodesic G P := by
  classical
  rcases exists_diameter_walk_with_dist (G := G) hconn with
    ⟨u, v, p, hp_path, hp_dist, hp_diam⟩
  let P : Fin (G.diam + 1) → alpha := fun i => p.getVert i.val
  refine ⟨P, ?_⟩
  refine ⟨?_, ?_, ?_, ?_⟩
  · have hdist :=
      geodesic_getVert_dist_eq_index_sub (G := G) p hp_dist
        (i := 0) (j := G.diam) (Nat.zero_le _) (Nat.le_of_eq hp_diam.symm)
    simpa [P, hp_diam] using hdist
  · intro i j hij
    have hi : i.val ≤ p.length := by
      rw [hp_diam]
      exact Nat.le_of_lt_succ i.isLt
    have hj : j.val ≤ p.length := by
      rw [hp_diam]
      exact Nat.le_of_lt_succ j.isLt
    have hij' : p.getVert i.val = p.getVert j.val := by
      simpa [P] using hij
    apply Fin.ext
    exact hp_path.getVert_injOn hi hj hij'
  · intro i
    have hi : i.val < p.length := by
      rw [hp_diam]
      exact i.isLt
    simpa [P, edgeLeft, edgeRight] using p.adj_getVert_succ hi
  · intro i j
    by_cases hij : i.val ≤ j.val
    · have hj : j.val ≤ p.length := by
        rw [hp_diam]
        exact Nat.le_of_lt_succ j.isLt
      have hdist :=
        geodesic_getVert_dist_eq_index_sub (G := G) p hp_dist
          (i := i.val) (j := j.val) hij hj
      simpa [P, hij] using hdist
    · have hji : j.val ≤ i.val := Nat.le_of_lt (Nat.lt_of_not_ge hij)
      have hi : i.val ≤ p.length := by
        rw [hp_diam]
        exact Nat.le_of_lt_succ i.isLt
      have hdist :=
        geodesic_getVert_dist_eq_index_sub (G := G) p hp_dist
          (i := j.val) (j := i.val) hji hi
      rw [G.dist_comm]
      simpa [P, hij] using hdist

end SimpleGraph

namespace Wowii198aLeftmost20260609

open Classical SimpleGraph

set_option linter.unusedSectionVars false
set_option linter.unnecessarySimpa false

variable {alpha : Type*}

lemma exists_walk_of_nonempty_chain_with_support
    (G : SimpleGraph alpha)
    (order : List alpha)
    (hne : order ≠ [])
    (hchain : List.IsChain G.Adj order) :
    ∃ a b : alpha, ∃ p : G.Walk a b,
      p.support = order := by
  cases order with
  | nil => exact False.elim (hne rfl)
  | cons a tail =>
      rcases SimpleGraph.exists_walk_of_chain_cons_visible (G := G) a tail hchain with
        ⟨b, p, hp⟩
      exact ⟨a, b, p, hp⟩

lemma exists_hamiltonian_walk_of_universal_nodup_chain
    (G : SimpleGraph alpha)
    (order : List alpha)
    (hne : order ≠ [])
    (hchain : List.IsChain G.Adj order)
    (hN : order.Nodup)
    (hcover : ∀ v : alpha, v ∈ order) :
    ∃ a b : alpha, ∃ p : G.Walk a b, p.IsHamiltonian := by
  rcases exists_walk_of_nonempty_chain_with_support
      (G := G) (order := order) hne hchain with
    ⟨a, b, p, hp_support⟩
  refine ⟨a, b, p, ?_⟩
  have hpN : p.support.Nodup := by
    rw [hp_support]
    exact hN
  have hp_mem : ∀ v : alpha, v ∈ p.support := by
    intro v
    rw [hp_support]
    exact hcover v
  exact fun v => List.count_eq_one_of_mem hpN (hp_mem v)

/-- `i` is the first consecutive path edge whose two endpoints are both
adjacent to `z`. -/
structure LeftmostEligibleEdge (G : SimpleGraph alpha)
    (P : Fin (G.diam + 1) → alpha) (z : alpha) (i : Fin G.diam) : Prop where
  adj_left : G.Adj z (P (edgeLeft G i))
  adj_right : G.Adj z (P (edgeRight G i))
  not_before : ∀ k : Fin G.diam, k.val < i.val →
    ¬ (G.Adj z (P (edgeLeft G k)) ∧ G.Adj z (P (edgeRight G k)))

private lemma three_le_succ_sub_of_add_two_le {a b : Nat} (h : b + 2 ≤ a) :
    3 ≤ a + 1 - b := by
  have hsucc : b + 2 + 1 ≤ a + 1 := Nat.succ_le_succ h
  exact Nat.le_sub_of_add_le
    (by simpa [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using hsucc)

lemma dist_path_vertex_to_right_edge_le_two
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (_hconn : G.Connected)
    (P : Fin (G.diam + 1) → alpha)
    (z : alpha) (i : Fin G.diam) (j : Fin (G.diam + 1))
    (hzi : LeftmostEligibleEdge G P z i)
    (hzj : G.Adj z (P j)) :
    G.dist (P j) (P (edgeRight G i)) ≤ 2 := by
  let p : G.Walk (P j) (P (edgeRight G i)) :=
    Walk.cons hzj.symm (Walk.cons hzi.adj_right Walk.nil)
  have hdist := SimpleGraph.dist_le p
  simpa [p] using hdist

lemma dist_left_edge_to_path_vertex_le_two
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (_hconn : G.Connected)
    (P : Fin (G.diam + 1) → alpha)
    (z : alpha) (i : Fin G.diam) (j : Fin (G.diam + 1))
    (hzi : LeftmostEligibleEdge G P z i)
    (hzj : G.Adj z (P j)) :
    G.dist (P (edgeLeft G i)) (P j) ≤ 2 := by
  let p : G.Walk (P (edgeLeft G i)) (P j) :=
    Walk.cons hzi.adj_left.symm (Walk.cons hzj Walk.nil)
  have hdist := SimpleGraph.dist_le p
  simpa [p] using hdist

lemma not_path_neighbor_two_or_more_left_of_leftmost
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (P : Fin (G.diam + 1) → alpha)
    (hP : IsDiametralGeodesic G P)
    (z : alpha) (i : Fin G.diam)
    (hzi : LeftmostEligibleEdge G P z i)
    (j : Fin (G.diam + 1))
    (hzj : G.Adj z (P j))
    (hfar : j.val + 2 ≤ i.val) : False := by
  have hle_two :
      G.dist (P j) (P (edgeRight G i)) ≤ 2 :=
    dist_path_vertex_to_right_edge_le_two (G := G) hconn P z i j hzi hzj
  have hdist :
      G.dist (P j) (P (edgeRight G i)) = i.val + 1 - j.val := by
    have hji : j.val ≤ (edgeRight G i).val := by
      have hj_le_i : j.val ≤ i.val :=
        Nat.le_trans (Nat.le_add_right j.val 2) hfar
      simpa [edgeRight] using Nat.le_trans hj_le_i (Nat.le_succ i.val)
    have hraw := hP.dist_eq j (edgeRight G i)
    rw [if_pos hji] at hraw
    simpa [edgeRight] using hraw
  have hdist_ge_three : 3 ≤ G.dist (P j) (P (edgeRight G i)) := by
    rw [hdist]
    exact three_le_succ_sub_of_add_two_le hfar
  have hthree_le_two : 3 ≤ 2 := Nat.le_trans hdist_ge_three hle_two
  nomatch hthree_le_two

lemma not_path_neighbor_three_or_more_right_of_leftmost
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (P : Fin (G.diam + 1) → alpha)
    (hP : IsDiametralGeodesic G P)
    (z : alpha) (i : Fin G.diam)
    (hzi : LeftmostEligibleEdge G P z i)
    (j : Fin (G.diam + 1))
    (hzj : G.Adj z (P j))
    (hfar : i.val + 3 ≤ j.val) : False := by
  have hle_two :
      G.dist (P (edgeLeft G i)) (P j) ≤ 2 :=
    dist_left_edge_to_path_vertex_le_two (G := G) hconn P z i j hzi hzj
  have hdist :
      G.dist (P (edgeLeft G i)) (P j) = j.val - i.val := by
    have hij : (edgeLeft G i).val ≤ j.val := by
      simp [edgeLeft]
      omega
    have hraw := hP.dist_eq (edgeLeft G i) j
    rw [if_pos hij] at hraw
    simpa [edgeLeft] using hraw
  have hgt : 2 < G.dist (P (edgeLeft G i)) (P j) := by
    rw [hdist]
    omega
  omega

lemma not_immediate_left_neighbor_of_leftmost
    (G : SimpleGraph alpha)
    (P : Fin (G.diam + 1) → alpha)
    (z : alpha) (i : Fin G.diam)
    (hzi : LeftmostEligibleEdge G P z i)
    (j : Fin (G.diam + 1))
    (hzj : G.Adj z (P j))
    (hj : j.val + 1 = i.val) : False := by
  let k : Fin G.diam := ⟨j.val, by omega⟩
  have hklt : k.val < i.val := by
    simp [k]
    omega
  have hk_left : edgeLeft G k = j := by
    ext
    simp [edgeLeft, k]
  have hk_right : edgeRight G k = edgeLeft G i := by
    ext
    simp [edgeRight, edgeLeft, k]
    omega
  exact hzi.not_before k hklt ⟨by simpa [hk_left], by simpa [hk_right] using hzi.adj_left⟩

lemma path_neighbors_subset_of_leftmostEligibleEdge
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P)
    (z : alpha)
    (hzP : z ∉ Set.range P)
    (i : Fin G.diam)
    (hzi : LeftmostEligibleEdge G P z i)
    (j : Fin (G.diam + 1))
    (hzj : G.Adj z (P j))
    (hdel : j.val ≠ i.val + 1) :
    j.val = i.val ∨ j.val = i.val + 2 := by
  have _ : z ∉ Set.range P := hzP
  have hge : i.val ≤ j.val := by
    by_contra hnot
    have hlt : j.val < i.val := Nat.lt_of_not_ge hnot
    by_cases hfar : j.val + 2 ≤ i.val
    · exact (not_path_neighbor_two_or_more_left_of_leftmost
        (G := G) hconn P hP z i hzi j hzj hfar).elim
    · have hj : j.val + 1 = i.val := by omega
      exact (not_immediate_left_neighbor_of_leftmost
        (G := G) P z i hzi j hzj hj).elim
  have hle : j.val ≤ i.val + 2 := by
    by_contra hnot
    have hfar : i.val + 3 ≤ j.val := by omega
    exact (not_path_neighbor_three_or_more_right_of_leftmost
      (G := G) hconn P hP z i hzi j hzj hfar).elim
  have hcases : j.val = i.val ∨ j.val = i.val + 1 ∨ j.val = i.val + 2 := by
    omega
  rcases hcases with h | h | h
  · exact Or.inl h
  · exact False.elim (hdel h)
  · exact Or.inr h

lemma not_adj_path_vertices_same_parity
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P)
    (a b : Fin (G.diam + 1))
    (hpar : a.val % 2 = b.val % 2)
    (hne : a.val ≠ b.val) :
    ¬ G.Adj (P a) (P b) := by
  intro hadj
  have hle_one : G.dist (P a) (P b) ≤ 1 := by
    simpa using SimpleGraph.dist_le hadj.toWalk
  have hdist := hP.dist_eq a b
  have hge_two : 2 ≤ G.dist (P a) (P b) := by
    rw [hdist]
    by_cases hab : a.val ≤ b.val
    · rw [if_pos hab]
      omega
    · rw [if_neg hab]
      omega
  omega

lemma not_adj_leftmost_to_opposite_erased_path_vertex
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P)
    (z : alpha)
    (hzP : z ∉ Set.range P)
    (i : Fin G.diam)
    (hzi : LeftmostEligibleEdge G P z i)
    (j : Fin (G.diam + 1))
    (hjpar : j.val % 2 ≠ i.val % 2)
    (hjdel : P j ≠ P (edgeRight G i)) :
    ¬ G.Adj z (P j) := by
  intro hzj
  have hdel : j.val ≠ i.val + 1 := by
    intro hj
    apply hjdel
    apply congrArg P
    ext
    simp [edgeRight]
    omega
  have hcases :=
    path_neighbors_subset_of_leftmostEligibleEdge
      (G := G) hconn P hP z hzP i hzi j hzj hdel
  omega

noncomputable def leftmostSameParityPathSide
    (G : SimpleGraph alpha) [Fintype alpha]
    (P : Fin (G.diam + 1) -> alpha) (i : Fin G.diam) : Finset alpha :=
  (Finset.univ.filter fun j : Fin (G.diam + 1) => j.val % 2 = i.val % 2).image P

noncomputable def leftmostOppositePathSideErased
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha]
    (P : Fin (G.diam + 1) -> alpha) (i : Fin G.diam) : Finset alpha :=
  ((Finset.univ.filter fun j : Fin (G.diam + 1) => j.val % 2 ≠ i.val % 2).image P).erase
    (P (edgeRight G i))

noncomputable def leftmostPairWitness
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha]
    (P : Fin (G.diam + 1) -> alpha) (z w : alpha) (i : Fin G.diam) : Finset alpha :=
  ((Finset.univ.image P).erase (P (edgeRight G i))) ∪ ({z, w} : Finset alpha)

noncomputable def leftmostOppositeSideWithPair
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha]
    (P : Fin (G.diam + 1) -> alpha) (z w : alpha) (i : Fin G.diam) : Finset alpha :=
  leftmostOppositePathSideErased G P i ∪ ({z, w} : Finset alpha)

lemma leftmost_same_parity_path_side_independent
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P)
    (i : Fin G.diam) :
    G.IsIndepSet ((leftmostSameParityPathSide G P i : Finset alpha) : Set alpha) := by
  intro x hx y hy hxy_ne hxy
  simp only [leftmostSameParityPathSide, Finset.mem_coe, Finset.mem_image,
    Finset.mem_filter, Finset.mem_univ, true_and] at hx hy
  rcases hx with ⟨a, ha, rfl⟩
  rcases hy with ⟨b, hb, rfl⟩
  have hab_ne : a.val ≠ b.val := by
    intro hv
    apply hxy_ne
    exact congrArg P (Fin.ext hv)
  exact (not_adj_path_vertices_same_parity (G := G) P hP a b (by omega) hab_ne) hxy

lemma leftmost_opposite_path_side_erased_independent
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P)
    (i : Fin G.diam) :
    G.IsIndepSet ((leftmostOppositePathSideErased G P i : Finset alpha) : Set alpha) := by
  intro x hx y hy hxy_ne hxy
  simp only [leftmostOppositePathSideErased, Finset.mem_coe, Finset.mem_erase,
    Finset.mem_image, Finset.mem_filter, Finset.mem_univ, true_and] at hx hy
  rcases hx with ⟨_hxdel, a, ha, rfl⟩
  rcases hy with ⟨_hydel, b, hb, rfl⟩
  have hab_ne : a.val ≠ b.val := by
    intro hv
    apply hxy_ne
    exact congrArg P (Fin.ext hv)
  have hpar : a.val % 2 = b.val % 2 := by
    have hi_cases := Nat.mod_two_eq_zero_or_one i.val
    have ha_cases := Nat.mod_two_eq_zero_or_one a.val
    have hb_cases := Nat.mod_two_eq_zero_or_one b.val
    rcases hi_cases with hi0 | hi1
    · rcases ha_cases with ha0 | ha1
      · exact False.elim (ha (by rw [ha0, hi0]))
      · rcases hb_cases with hb0 | hb1
        · exact False.elim (hb (by rw [hb0, hi0]))
        · rw [ha1, hb1]
    · rcases ha_cases with ha0 | ha1
      · rcases hb_cases with hb0 | hb1
        · rw [ha0, hb0]
        · exact False.elim (hb (by rw [hb1, hi1]))
      · exact False.elim (ha (by rw [ha1, hi1]))
  exact (not_adj_path_vertices_same_parity (G := G) P hP a b hpar hab_ne) hxy

lemma leftmost_opposite_side_with_pair_independent
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P)
    (z w : alpha)
    (hzP : z ∉ Set.range P)
    (hwP : w ∉ Set.range P)
    (i : Fin G.diam)
    (hzi : LeftmostEligibleEdge G P z i)
    (hwi : LeftmostEligibleEdge G P w i)
    (hzw_nonadj : ¬ G.Adj z w) :
    G.IsIndepSet ((leftmostOppositeSideWithPair G P z w i : Finset alpha) : Set alpha) := by
  intro x hx y hy hxy_ne hxy
  change x ∈ leftmostOppositeSideWithPair G P z w i at hx
  change y ∈ leftmostOppositeSideWithPair G P z w i at hy
  rw [leftmostOppositeSideWithPair, Finset.mem_union] at hx hy
  rcases hx with hxPath | hxPair
  · rcases hy with hyPath | hyPair
    · exact leftmost_opposite_path_side_erased_independent
        (G := G) P hP i hxPath hyPath hxy_ne hxy
    · rw [Finset.mem_insert, Finset.mem_singleton] at hyPair
      rcases Finset.mem_erase.mp hxPath with ⟨hxdel, hxImage⟩
      rcases Finset.mem_image.mp hxImage with ⟨j, hjFilter, hxj⟩
      have hjpar : j.val % 2 ≠ i.val % 2 := (Finset.mem_filter.mp hjFilter).2
      rcases hyPair with hyz | hyw
      · have hxdel' : P j ≠ P (edgeRight G i) := by
          intro h
          exact hxdel (hxj.symm.trans h)
        have hnot := not_adj_leftmost_to_opposite_erased_path_vertex
          (G := G) hconn P hP z hzP i hzi j hjpar hxdel'
        exact hnot (by simpa [hxj, hyz] using hxy.symm)
      · have hxdel' : P j ≠ P (edgeRight G i) := by
          intro h
          exact hxdel (hxj.symm.trans h)
        have hnot := not_adj_leftmost_to_opposite_erased_path_vertex
          (G := G) hconn P hP w hwP i hwi j hjpar hxdel'
        exact hnot (by simpa [hxj, hyw] using hxy.symm)
  · simp only [Finset.mem_insert, Finset.mem_singleton] at hxPair
    rcases hy with hyPath | hyPair
    · rcases hxPair with hxz | hxw
      · rcases Finset.mem_erase.mp hyPath with ⟨hydel, hyImage⟩
        rcases Finset.mem_image.mp hyImage with ⟨j, hjFilter, hyj⟩
        have hjpar : j.val % 2 ≠ i.val % 2 := (Finset.mem_filter.mp hjFilter).2
        have hydel' : P j ≠ P (edgeRight G i) := by
          intro h
          exact hydel (hyj.symm.trans h)
        have hnot := not_adj_leftmost_to_opposite_erased_path_vertex
          (G := G) hconn P hP z hzP i hzi j hjpar hydel'
        exact hnot (by simpa [hyj, hxz] using hxy)
      · rcases Finset.mem_erase.mp hyPath with ⟨hydel, hyImage⟩
        rcases Finset.mem_image.mp hyImage with ⟨j, hjFilter, hyj⟩
        have hjpar : j.val % 2 ≠ i.val % 2 := (Finset.mem_filter.mp hjFilter).2
        have hydel' : P j ≠ P (edgeRight G i) := by
          intro h
          exact hydel (hyj.symm.trans h)
        have hnot := not_adj_leftmost_to_opposite_erased_path_vertex
          (G := G) hconn P hP w hwP i hwi j hjpar hydel'
        exact hnot (by simpa [hyj, hxw] using hxy)
    · simp only [Finset.mem_insert, Finset.mem_singleton] at hyPair
      rcases hxPair with hxz | hxw <;> rcases hyPair with hyz | hyw
      · exact hxy_ne (hxz.trans hyz.symm)
      · exact hzw_nonadj (by simpa [hxz, hyw] using hxy)
      · exact hzw_nonadj (by simpa [hxw, hyz] using hxy.symm)
      · exact hxy_ne (hxw.trans hyw.symm)

lemma leftmost_partition_disjoint
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P)
    (z w : alpha)
    (hzP : z ∉ Set.range P)
    (hwP : w ∉ Set.range P)
    (i : Fin G.diam) :
    Disjoint (leftmostSameParityPathSide G P i)
      (leftmostOppositeSideWithPair G P z w i) := by
  rw [Finset.disjoint_left]
  intro x hxA hxB
  simp only [leftmostSameParityPathSide, Finset.mem_image, Finset.mem_filter,
    Finset.mem_univ, true_and] at hxA
  rcases hxA with ⟨a, ha, hax⟩
  rw [leftmostOppositeSideWithPair, Finset.mem_union] at hxB
  rcases hxB with hxPath | hxPair
  · simp only [leftmostOppositePathSideErased, Finset.mem_erase, Finset.mem_image,
      Finset.mem_filter, Finset.mem_univ, true_and] at hxPath
    rcases hxPath with ⟨_hxdel, b, hb, hbx⟩
    have hab : a = b := hP.injective (hax.trans hbx.symm)
    have hcontra : a.val % 2 = b.val % 2 := by rw [hab]
    exact hb (hcontra.symm.trans ha)
  · simp only [Finset.mem_insert, Finset.mem_singleton] at hxPair
    rcases hxPair with hxz | hxw
    · exact hzP ⟨a, hax.trans hxz⟩
    · exact hwP ⟨a, hax.trans hxw⟩

lemma leftmost_partition_union_eq_pair_witness
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P)
    (z w : alpha)
    (i : Fin G.diam) :
    leftmostSameParityPathSide G P i ∪
        leftmostOppositeSideWithPair G P z w i =
      leftmostPairWitness G P z w i := by
  ext x
  simp only [leftmostSameParityPathSide, leftmostOppositeSideWithPair,
    leftmostOppositePathSideErased, leftmostPairWitness, Finset.mem_union, Finset.mem_image,
    Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_erase, Finset.mem_insert,
    Finset.mem_singleton]
  constructor
  · rintro (⟨a, ha, hax⟩ | (⟨hxdel, b, hb, hbx⟩ | hxz | hxw))
    · left
      constructor
      · intro hxright
        have ha_right : a = edgeRight G i := hP.injective (hax.trans hxright)
        have : a.val % 2 ≠ i.val % 2 := by
          rw [ha_right]
          simp [edgeRight]
          omega
        exact this ha
      · exact ⟨a, hax⟩
    · exact Or.inl ⟨hxdel, b, hbx⟩
    · exact Or.inr (Or.inl hxz)
    · exact Or.inr (Or.inr hxw)
  · rintro (⟨hxdel, j, hjx⟩ | hxz | hxw)
    · by_cases hjpar : j.val % 2 = i.val % 2
      · exact Or.inl ⟨j, hjpar, hjx⟩
      · exact Or.inr (Or.inl ⟨hxdel, j, hjpar, hjx⟩)
    · exact Or.inr (Or.inr (Or.inl hxz))
    · exact Or.inr (Or.inr (Or.inr hxw))

lemma leftmost_pair_witness_card
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P)
    (z w : alpha)
    (hzP : z ∉ Set.range P)
    (hwP : w ∉ Set.range P)
    (hzw : z ≠ w)
    (i : Fin G.diam) :
    (leftmostPairWitness G P z w i).card = G.diam + 2 := by
  classical
  let pathSet : Finset alpha := Finset.univ.image P
  have hpath_card : pathSet.card = G.diam + 1 := by
    dsimp [pathSet]
    rw [Finset.card_image_of_injective _ hP.injective]
    simp
  have hright_mem : P (edgeRight G i) ∈ pathSet := by
    dsimp [pathSet]
    exact Finset.mem_image.mpr ⟨edgeRight G i, Finset.mem_univ _, rfl⟩
  have herase_card : (pathSet.erase (P (edgeRight G i))).card = G.diam := by
    rw [Finset.card_erase_of_mem hright_mem, hpath_card]
    omega
  have hdisj : Disjoint (pathSet.erase (P (edgeRight G i))) ({z, w} : Finset alpha) := by
    rw [Finset.disjoint_left]
    intro x hx hp
    simp only [Finset.mem_insert, Finset.mem_singleton] at hp
    rcases hp with rfl | rfl
    · rcases Finset.mem_image.mp (Finset.mem_erase.mp hx).2 with ⟨j, _hj, hj⟩
      exact hzP ⟨j, hj⟩
    · rcases Finset.mem_image.mp (Finset.mem_erase.mp hx).2 with ⟨j, _hj, hj⟩
      exact hwP ⟨j, hj⟩
  have hpair_card : ({z, w} : Finset alpha).card = 2 := by
    simp [hzw]
  dsimp [leftmostPairWitness, pathSet] at *
  rw [Finset.card_union_of_disjoint hdisj, herase_card, hpair_card]

lemma leftmost_same_edge_fiber_pair_adjacent_of_b_eq_diam_add_one
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (hb : b G = G.diam + 1)
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P)
    (z w : alpha)
    (hzP : z ∉ Set.range P)
    (hwP : w ∉ Set.range P)
    (hzw : z ≠ w)
    (i : Fin G.diam)
    (hzi : LeftmostEligibleEdge G P z i)
    (hwi : LeftmostEligibleEdge G P w i) :
    G.Adj z w := by
  by_contra hnonadj
  let A : Finset alpha := leftmostSameParityPathSide G P i
  let B : Finset alpha := leftmostOppositeSideWithPair G P z w i
  have hA : G.IsIndepSet (A : Set alpha) := by
    dsimp [A]
    exact leftmost_same_parity_path_side_independent (G := G) P hP i
  have hB : G.IsIndepSet (B : Set alpha) := by
    have hB' := leftmost_opposite_side_with_pair_independent
      (G := G) hconn P hP z w hzP hwP i hzi hwi hnonadj
    simpa [B] using hB'
  have hdisj : Disjoint A B := by
    dsimp [A, B]
    exact leftmost_partition_disjoint (G := G) P hP z w hzP hwP i
  have hBip : (G.induce ((A ∪ B : Finset alpha) : Set alpha)).IsBipartite :=
    SimpleGraph.induce_union_indep_isBipartite (G := G) (A := A) (B := B) hA hB hdisj
  have hlower : (A ∪ B).card ≤ b G := by
    simpa [b] using
      SimpleGraph.card_le_largestInducedBipartiteSubgraphSize_of_induce_isBipartite
        (G := G) (s := A ∪ B) hBip
  have hcard : (A ∪ B).card = G.diam + 2 := by
    have hunion :
        A ∪ B = leftmostPairWitness G P z w i := by
      dsimp [A, B]
      exact leftmost_partition_union_eq_pair_witness (G := G) P hP z w i
    rw [hunion]
    exact leftmost_pair_witness_card (G := G) P hP z w hzP hwP hzw i
  have hbad : G.diam + 2 ≤ G.diam + 1 := by
    simpa [hcard, hb] using hlower
  have hlt : G.diam + 1 < G.diam + 2 := by
    simpa [Nat.add_assoc] using Nat.lt_succ_self (G.diam + 1)
  exact (Nat.lt_irrefl (G.diam + 2)) (lt_of_le_of_lt hbad hlt)

noncomputable def pathParitySide
    (G : SimpleGraph alpha) [Fintype alpha]
    (P : Fin (G.diam + 1) -> alpha) (p : ℕ) : Finset alpha :=
  (Finset.univ.filter fun j : Fin (G.diam + 1) => j.val % 2 = p).image P

noncomputable def pathNonParitySide
    (G : SimpleGraph alpha) [Fintype alpha]
    (P : Fin (G.diam + 1) -> alpha) (p : ℕ) : Finset alpha :=
  (Finset.univ.filter fun j : Fin (G.diam + 1) => j.val % 2 ≠ p).image P

noncomputable def leftmostSingleWitness
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha]
    (P : Fin (G.diam + 1) -> alpha) (z : alpha) : Finset alpha :=
  (Finset.univ.image P) ∪ ({z} : Finset alpha)

lemma path_parity_side_independent
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P)
    (p : ℕ) :
    G.IsIndepSet ((pathParitySide G P p : Finset alpha) : Set alpha) := by
  intro x hx y hy hxy_ne hxy
  simp only [pathParitySide, Finset.mem_coe, Finset.mem_image,
    Finset.mem_filter, Finset.mem_univ, true_and] at hx hy
  rcases hx with ⟨a, ha, rfl⟩
  rcases hy with ⟨b, hb, rfl⟩
  have hab_ne : a.val ≠ b.val := by
    intro hv
    apply hxy_ne
    exact congrArg P (Fin.ext hv)
  have hpar : a.val % 2 = b.val % 2 := by
    rw [ha, hb]
  exact (not_adj_path_vertices_same_parity (G := G) P hP a b hpar hab_ne) hxy

lemma path_nonparity_side_independent
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P)
    (p : ℕ) (hp : p < 2) :
    G.IsIndepSet ((pathNonParitySide G P p : Finset alpha) : Set alpha) := by
  intro x hx y hy hxy_ne hxy
  simp only [pathNonParitySide, Finset.mem_coe, Finset.mem_image,
    Finset.mem_filter, Finset.mem_univ, true_and] at hx hy
  rcases hx with ⟨a, ha, rfl⟩
  rcases hy with ⟨b, hb, rfl⟩
  have hab_ne : a.val ≠ b.val := by
    intro hv
    apply hxy_ne
    exact congrArg P (Fin.ext hv)
  have hp_cases : p = 0 ∨ p = 1 := by omega
  have ha_cases := Nat.mod_two_eq_zero_or_one a.val
  have hb_cases := Nat.mod_two_eq_zero_or_one b.val
  have hpar : a.val % 2 = b.val % 2 := by
    rcases hp_cases with rfl | rfl
    · rcases ha_cases with ha0 | ha1
      · exact False.elim (ha ha0)
      · rcases hb_cases with hb0 | hb1
        · exact False.elim (hb hb0)
        · rw [ha1, hb1]
    · rcases ha_cases with ha0 | ha1
      · rcases hb_cases with hb0 | hb1
        · rw [ha0, hb0]
        · exact False.elim (hb hb1)
      · exact False.elim (ha ha1)
  exact (not_adj_path_vertices_same_parity (G := G) P hP a b hpar hab_ne) hxy

lemma path_parity_side_with_vertex_independent
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P)
    (z : alpha) (p : ℕ)
    (hz_no : ∀ j : Fin (G.diam + 1), j.val % 2 = p → ¬ G.Adj z (P j)) :
    G.IsIndepSet (((pathParitySide G P p : Finset alpha) ∪ {z}) : Set alpha) := by
  intro x hx y hy hxy_ne hxy
  simp only [Set.mem_union, Finset.mem_coe] at hx hy
  rcases hx with hxPath | hxz
  · rcases hy with hyPath | hyz
    · exact path_parity_side_independent (G := G) P hP p hxPath hyPath hxy_ne hxy
    · simp only [pathParitySide, Finset.mem_image, Finset.mem_filter,
        Finset.mem_univ, true_and] at hxPath
      rw [Set.mem_singleton_iff] at hyz
      rcases hxPath with ⟨j, hjpar, hxj⟩
      exact (hz_no j hjpar) (by subst y; simpa [hxj] using hxy.symm)
  · rcases hy with hyPath | hyz
    · simp only [pathParitySide, Finset.mem_image, Finset.mem_filter,
        Finset.mem_univ, true_and] at hyPath
      rw [Set.mem_singleton_iff] at hxz
      rcases hyPath with ⟨j, hjpar, hyj⟩
      exact (hz_no j hjpar) (by subst x; simpa [hyj] using hxy)
    · rw [Set.mem_singleton_iff] at hxz hyz
      exact hxy_ne (hxz.trans hyz.symm)

lemma path_parity_with_vertex_disjoint_nonparity
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P)
    (z : alpha)
    (hzP : z ∉ Set.range P)
    (p : ℕ) :
    Disjoint ((pathParitySide G P p : Finset alpha) ∪ {z}) (pathNonParitySide G P p) := by
  rw [Finset.disjoint_left]
  intro x hxA hxB
  simp only [Finset.mem_union, Finset.mem_singleton] at hxA
  simp only [pathNonParitySide, Finset.mem_image, Finset.mem_filter,
    Finset.mem_univ, true_and] at hxB
  rcases hxB with ⟨b, hb, hbx⟩
  rcases hxA with hxPath | hxz
  · simp only [pathParitySide, Finset.mem_image, Finset.mem_filter,
      Finset.mem_univ, true_and] at hxPath
    rcases hxPath with ⟨a, ha, hax⟩
    have hab : a = b := hP.injective (hax.trans hbx.symm)
    have : b.val % 2 = p := by
      rw [← hab]
      exact ha
    exact hb this
  · exact hzP ⟨b, hbx.trans hxz⟩

lemma path_parity_partition_union_eq_single_witness
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha]
    (P : Fin (G.diam + 1) -> alpha)
    (z : alpha) (p : ℕ) :
    ((pathParitySide G P p : Finset alpha) ∪ {z}) ∪ pathNonParitySide G P p =
      leftmostSingleWitness G P z := by
  ext x
  simp only [pathParitySide, pathNonParitySide, leftmostSingleWitness,
    Finset.mem_union, Finset.mem_image, Finset.mem_filter, Finset.mem_univ,
    true_and, Finset.mem_singleton]
  constructor
  · rintro ((⟨j, _hjpar, hjx⟩ | hxz) | ⟨j, _hjpar, hjx⟩)
    · exact Or.inl ⟨j, hjx⟩
    · exact Or.inr hxz
    · exact Or.inl ⟨j, hjx⟩
  · rintro (⟨j, hjx⟩ | hxz)
    · by_cases hjpar : j.val % 2 = p
      · exact Or.inl (Or.inl ⟨j, hjpar, hjx⟩)
      · exact Or.inr ⟨j, hjpar, hjx⟩
    · exact Or.inl (Or.inr hxz)

lemma leftmost_single_witness_card
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P)
    (z : alpha)
    (hzP : z ∉ Set.range P) :
    (leftmostSingleWitness G P z).card = G.diam + 2 := by
  classical
  let pathSet : Finset alpha := Finset.univ.image P
  have hpath_card : pathSet.card = G.diam + 1 := by
    dsimp [pathSet]
    rw [Finset.card_image_of_injective _ hP.injective]
    simp
  have hdisj : Disjoint pathSet ({z} : Finset alpha) := by
    rw [Finset.disjoint_left]
    intro x hx hz
    simp only [Finset.mem_singleton] at hz
    rcases Finset.mem_image.mp hx with ⟨j, _hj, hj⟩
    exact hzP ⟨j, hj.trans hz⟩
  dsimp [leftmostSingleWitness, pathSet] at *
  calc
    (Finset.univ.image P ∪ ({z} : Finset alpha)).card =
        (Finset.univ.image P).card + ({z} : Finset alpha).card := by
      simpa using Finset.card_union_of_disjoint hdisj
    _ = G.diam + 2 := by
      rw [hpath_card]
      simp

lemma path_neighbor_parity_eq_of_no_eligible
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P)
    (z : alpha)
    (hno : ∀ i : Fin G.diam,
      ¬ (G.Adj z (P (edgeLeft G i)) ∧ G.Adj z (P (edgeRight G i))))
    (a b : Fin (G.diam + 1))
    (hza : G.Adj z (P a))
    (hzb : G.Adj z (P b)) :
    a.val % 2 = b.val % 2 := by
  by_contra hpar
  have hle_two : G.dist (P a) (P b) ≤ 2 := by
    have haz : G.dist (P a) z ≤ 1 := by
      simpa using SimpleGraph.dist_le hza.symm.toWalk
    have hzb' : G.dist z (P b) ≤ 1 := by
      simpa using SimpleGraph.dist_le hzb.toWalk
    have htri :
        G.dist (P a) (P b) ≤ G.dist (P a) z + G.dist z (P b) :=
      hconn.dist_triangle
    omega
  have hdist := hP.dist_eq a b
  by_cases hab : a.val ≤ b.val
  · have hdiff_le : b.val - a.val ≤ 2 := by
      rw [if_pos hab] at hdist
      omega
    have hsucc : b.val = a.val + 1 := by omega
    let i : Fin G.diam := ⟨a.val, by omega⟩
    have hleft : edgeLeft G i = a := by
      ext
      simp [edgeLeft, i]
    have hright : edgeRight G i = b := by
      ext
      simp [edgeRight, i]
      omega
    exact hno i ⟨by simpa [hleft], by simpa [hright]⟩
  · have hba : b.val ≤ a.val := by omega
    have hdiff_le : a.val - b.val ≤ 2 := by
      rw [if_neg hab] at hdist
      omega
    have hsucc : a.val = b.val + 1 := by omega
    let i : Fin G.diam := ⟨b.val, by omega⟩
    have hleft : edgeLeft G i = b := by
      ext
      simp [edgeLeft, i]
    have hright : edgeRight G i = a := by
      ext
      simp [edgeRight, i]
      omega
    exact hno i ⟨by simpa [hleft] using hzb,
      by simpa [hright] using hza⟩

lemma exists_path_parity_avoiding_z_neighbors_of_no_eligible
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P)
    (z : alpha)
    (hno : ∀ i : Fin G.diam,
      ¬ (G.Adj z (P (edgeLeft G i)) ∧ G.Adj z (P (edgeRight G i)))) :
    ∃ p : ℕ, p < 2 ∧ ∀ j : Fin (G.diam + 1), j.val % 2 = p → ¬ G.Adj z (P j) := by
  by_cases hsome : ∃ j : Fin (G.diam + 1), G.Adj z (P j)
  · rcases hsome with ⟨a, hza⟩
    refine ⟨(a.val + 1) % 2, by omega, ?_⟩
    intro j hjpar hzj
    have hsame := path_neighbor_parity_eq_of_no_eligible
      (G := G) hconn P hP z hno a j hza hzj
    have hdiff : a.val % 2 ≠ (a.val + 1) % 2 := by omega
    exact hdiff (hsame.trans hjpar)
  · refine ⟨0, by omega, ?_⟩
    intro j _hjpar hzj
    exact hsome ⟨j, hzj⟩

lemma no_eligible_edge_contradicts_b_eq_diam_add_one
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (hb : b G = G.diam + 1)
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P)
    (z : alpha)
    (hzP : z ∉ Set.range P)
    (hno : ∀ i : Fin G.diam,
      ¬ (G.Adj z (P (edgeLeft G i)) ∧ G.Adj z (P (edgeRight G i)))) :
    False := by
  rcases exists_path_parity_avoiding_z_neighbors_of_no_eligible
    (G := G) hconn P hP z hno with ⟨p, hp, hz_no⟩
  let A : Finset alpha := pathParitySide G P p ∪ {z}
  let B : Finset alpha := pathNonParitySide G P p
  have hA : G.IsIndepSet (A : Set alpha) := by
    have hA' :=
      path_parity_side_with_vertex_independent (G := G) P hP z p hz_no
    simpa [A, Finset.coe_union] using hA'
  have hB : G.IsIndepSet (B : Set alpha) := by
    dsimp [B]
    exact path_nonparity_side_independent (G := G) P hP p hp
  have hdisj : Disjoint A B := by
    dsimp [A, B]
    exact path_parity_with_vertex_disjoint_nonparity (G := G) P hP z hzP p
  have hBip : (G.induce ((A ∪ B : Finset alpha) : Set alpha)).IsBipartite :=
    SimpleGraph.induce_union_indep_isBipartite (G := G) (A := A) (B := B) hA hB hdisj
  have hlower : (A ∪ B).card ≤ b G := by
    simpa [b] using
      SimpleGraph.card_le_largestInducedBipartiteSubgraphSize_of_induce_isBipartite
        (G := G) (s := A ∪ B) hBip
  have hcard : (A ∪ B).card = G.diam + 2 := by
    have hunion : A ∪ B = leftmostSingleWitness G P z := by
      dsimp [A, B]
      exact path_parity_partition_union_eq_single_witness (G := G) P z p
    rw [hunion]
    exact leftmost_single_witness_card (G := G) P hP z hzP
  omega

lemma exists_eligible_edge_of_b_eq_diam_add_one
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (hb : b G = G.diam + 1)
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P)
    (z : alpha)
    (hzP : z ∉ Set.range P) :
    ∃ i : Fin G.diam, G.Adj z (P (edgeLeft G i)) ∧ G.Adj z (P (edgeRight G i)) := by
  by_contra hno_exists
  have hno : ∀ i : Fin G.diam,
      ¬ (G.Adj z (P (edgeLeft G i)) ∧ G.Adj z (P (edgeRight G i))) := by
    intro i hi
    exact hno_exists ⟨i, hi⟩
  exact no_eligible_edge_contradicts_b_eq_diam_add_one
    (G := G) (hconn := hconn) (hb := hb) (P := P) (hP := hP)
    (z := z) (hzP := hzP) hno

lemma exists_leftmostEligibleEdge_of_b_eq_diam_add_one
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (hb : b G = G.diam + 1)
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P)
    (z : alpha)
    (hzP : z ∉ Set.range P) :
    ∃ i : Fin G.diam, LeftmostEligibleEdge G P z i := by
  classical
  let eligible : Finset (Fin G.diam) :=
    Finset.univ.filter fun i : Fin G.diam =>
      G.Adj z (P (edgeLeft G i)) ∧ G.Adj z (P (edgeRight G i))
  have hnonempty : eligible.Nonempty := by
    rcases exists_eligible_edge_of_b_eq_diam_add_one
      (G := G) hconn hb P hP z hzP with ⟨i, hi⟩
    exact ⟨i, by simp [eligible, hi]⟩
  rcases eligible.exists_minimal hnonempty with ⟨i, hi_min⟩
  have hi_mem : i ∈ eligible := hi_min.1
  simp only [eligible, Finset.mem_filter, Finset.mem_univ, true_and] at hi_mem
  refine ⟨i, ?_⟩
  refine ⟨hi_mem.1, hi_mem.2, ?_⟩
  intro k hklt hk
  have hk_mem : k ∈ eligible := by
    simp [eligible, hk]
  have hki_le : k ≤ i := by
    exact le_of_lt hklt
  have hik_le : i ≤ k := hi_min.2 hk_mem hki_le
  exact (not_lt_of_ge hik_le) hklt

def HasLeftmostCliqueFiberAssignment
    (G : SimpleGraph alpha) [Fintype alpha]
    (P : Fin (G.diam + 1) -> alpha) : Prop :=
  ∃ assign : {z : alpha // z ∉ Set.range P} -> Fin G.diam,
    (∀ z : {z : alpha // z ∉ Set.range P},
      LeftmostEligibleEdge G P z.1 (assign z)) ∧
    (∀ z w : {z : alpha // z ∉ Set.range P},
      z.1 ≠ w.1 -> assign z = assign w -> G.Adj z.1 w.1)

lemma exists_leftmost_edge_assignment_with_clique_fibers_of_b_eq_diam_add_one
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (hb : b G = G.diam + 1)
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P) :
    HasLeftmostCliqueFiberAssignment G P := by
  classical
  let assign : {z : alpha // z ∉ Set.range P} -> Fin G.diam :=
    fun z => Classical.choose
      (exists_leftmostEligibleEdge_of_b_eq_diam_add_one
        (G := G) (hconn := hconn) (hb := hb) (P := P) (hP := hP)
        (z := z.1) (hzP := z.2))
  have hassign :
      ∀ z : {z : alpha // z ∉ Set.range P},
        LeftmostEligibleEdge G P z.1 (assign z) := by
    intro z
    exact Classical.choose_spec
      (exists_leftmostEligibleEdge_of_b_eq_diam_add_one
        (G := G) (hconn := hconn) (hb := hb) (P := P) (hP := hP)
        (z := z.1) (hzP := z.2))
  refine ⟨assign, hassign, ?_⟩
  intro z w hzw hsame
  have hz : LeftmostEligibleEdge G P z.1 (assign z) := hassign z
  have hw : LeftmostEligibleEdge G P w.1 (assign z) := by
    rw [hsame]
    exact hassign w
  exact leftmost_same_edge_fiber_pair_adjacent_of_b_eq_diam_add_one
    (G := G) (hconn := hconn) (hb := hb) (P := P) (hP := hP)
    (z := z.1) (w := w.1) (hzP := z.2) (hwP := w.2)
    (hzw := hzw) (i := assign z) (hzi := hz) (hwi := hw)

theorem hamiltonian_path_from_leftmost_clique_fibers
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (hb : b G = G.diam + 1)
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P) :
    HasLeftmostCliqueFiberAssignment G P := by
  exact exists_leftmost_edge_assignment_with_clique_fibers_of_b_eq_diam_add_one
    (G := G) (hconn := hconn) (hb := hb) (P := P) (hP := hP)

lemma exists_leftmost_ordered_fiber_lists
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (P : Fin (G.diam + 1) -> alpha)
    (hA : HasLeftmostCliqueFiberAssignment G P) :
    ∃ assign : {z : alpha // z ∉ Set.range P} -> Fin G.diam,
      (∀ z : {z : alpha // z ∉ Set.range P},
        LeftmostEligibleEdge G P z.1 (assign z)) ∧
      (∀ z w : {z : alpha // z ∉ Set.range P},
        z.1 ≠ w.1 -> assign z = assign w -> G.Adj z.1 w.1) ∧
      ∃ fiber : Fin G.diam -> List {z : alpha // z ∉ Set.range P},
        (∀ i, (fiber i).Nodup) ∧
        (∀ i z, z ∈ fiber i ↔ assign z = i) ∧
        (∀ i z, z ∈ fiber i ->
          G.Adj (P (edgeLeft G i)) z.1 ∧ G.Adj z.1 (P (edgeRight G i))) ∧
        (∀ i z w, z ∈ fiber i -> w ∈ fiber i -> z.1 ≠ w.1 -> G.Adj z.1 w.1) := by
  classical
  rcases hA with ⟨assign, hassign, hclique⟩
  let fiber : Fin G.diam -> List {z : alpha // z ∉ Set.range P} :=
    fun i => (Finset.univ.filter fun z : {z : alpha // z ∉ Set.range P} =>
      assign z = i).toList
  have hfiber_mem : ∀ i z, z ∈ fiber i ↔ assign z = i := by
    intro i z
    dsimp [fiber]
    rw [Finset.mem_toList, Finset.mem_filter]
    exact ⟨fun h => h.2, fun h => ⟨Finset.mem_univ z, h⟩⟩
  refine ⟨assign, hassign, hclique, fiber, ?_, hfiber_mem, ?_, ?_⟩
  · intro i
    dsimp [fiber]
    exact Finset.nodup_toList _
  · intro i z hz
    have hzi_assign : assign z = i := (hfiber_mem i z).mp hz
    have hzi : LeftmostEligibleEdge G P z.1 i := by
      simpa [hzi_assign] using hassign z
    exact ⟨hzi.adj_left.symm, hzi.adj_right⟩
  · intro i z w hz hw hzw
    have hz_assign : assign z = i := (hfiber_mem i z).mp hz
    have hw_assign : assign w = i := (hfiber_mem i w).mp hw
    exact hclique z w hzw (hz_assign.trans hw_assign.symm)

private noncomputable def splicedBlock
    (G : SimpleGraph alpha)
    (P : Fin (G.diam + 1) -> alpha)
    (fiber : Fin G.diam -> List {z : alpha // z ∉ Set.range P})
    (j : Fin (G.diam + 1)) : List alpha :=
  P j :: if hj : j.val < G.diam then (fiber ⟨j.val, hj⟩).map Subtype.val else []

private lemma mem_splicedBlock
    (G : SimpleGraph alpha)
    (P : Fin (G.diam + 1) -> alpha)
    (fiber : Fin G.diam -> List {z : alpha // z ∉ Set.range P})
    (j : Fin (G.diam + 1)) (x : alpha) :
    x ∈ splicedBlock G P fiber j ↔
      x = P j ∨
        ∃ hj : j.val < G.diam, ∃ z : {z : alpha // z ∉ Set.range P},
          z ∈ fiber ⟨j.val, hj⟩ ∧ z.1 = x := by
  unfold splicedBlock
  by_cases hj : j.val < G.diam
  · simp [hj, eq_comm]
  · simp [hj]

private lemma splicedBlock_ne_nil
    (G : SimpleGraph alpha)
    (P : Fin (G.diam + 1) -> alpha)
    (fiber : Fin G.diam -> List {z : alpha // z ∉ Set.range P})
    (j : Fin (G.diam + 1)) :
    splicedBlock G P fiber j ≠ [] := by
  simp [splicedBlock]

private lemma splicedBlock_head?
    (G : SimpleGraph alpha)
    (P : Fin (G.diam + 1) -> alpha)
    (fiber : Fin G.diam -> List {z : alpha // z ∉ Set.range P})
    (j : Fin (G.diam + 1)) :
    (splicedBlock G P fiber j).head? = some (P j) := by
  simp [splicedBlock]

private lemma splicedBlock_nodup
    (G : SimpleGraph alpha)
    (P : Fin (G.diam + 1) -> alpha)
    (fiber : Fin G.diam -> List {z : alpha // z ∉ Set.range P})
    (hfiber_nodup : ∀ i, (fiber i).Nodup)
    (j : Fin (G.diam + 1)) :
    (splicedBlock G P fiber j).Nodup := by
  unfold splicedBlock
  by_cases hj : j.val < G.diam
  · simp only [hj, dite_true]
    refine List.Nodup.cons ?_ ((hfiber_nodup ⟨j.val, hj⟩).map Subtype.val_injective)
    intro hmem
    rcases List.mem_map.mp hmem with ⟨z, _hz, hz_eq⟩
    exact z.2 ⟨j, hz_eq.symm⟩
  · simp [hj]

private lemma splicedBlock_disjoint
    (G : SimpleGraph alpha)
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P)
    (assign : {z : alpha // z ∉ Set.range P} -> Fin G.diam)
    (fiber : Fin G.diam -> List {z : alpha // z ∉ Set.range P})
    (hfiber_mem : ∀ i z, z ∈ fiber i ↔ assign z = i)
    {j k : Fin (G.diam + 1)} (hjk : j ≠ k) :
    List.Disjoint (splicedBlock G P fiber j) (splicedBlock G P fiber k) := by
  intro x hxj hxk
  rw [mem_splicedBlock] at hxj hxk
  rcases hxj with hxj | hxj
  · rcases hxk with hxk | hxk
    · apply hjk
      exact hP.injective (hxj.symm.trans hxk)
    · rcases hxk with ⟨hk, z, _hzk, hz_eq⟩
      exact z.2 ⟨j, hxj.symm.trans hz_eq.symm⟩
  · rcases hxj with ⟨hj, z, hzj, hz_eq⟩
    rcases hxk with hxk | hxk
    · exact z.2 ⟨k, (hz_eq.trans hxk).symm⟩
    · rcases hxk with ⟨hk, w, hwk, hw_eq⟩
      have hzw : z = w := Subtype.ext (hz_eq.trans hw_eq.symm)
      have hz_assign : assign z = ⟨j.val, hj⟩ := (hfiber_mem ⟨j.val, hj⟩ z).mp hzj
      have hw_assign : assign w = ⟨k.val, hk⟩ := (hfiber_mem ⟨k.val, hk⟩ w).mp hwk
      have hval : j.val = k.val := by
        have hfin : (⟨j.val, hj⟩ : Fin G.diam) = ⟨k.val, hk⟩ := by
          exact hz_assign.symm.trans ((congrArg assign hzw).trans hw_assign)
        exact congrArg (fun i : Fin G.diam => i.val) hfin
      exact hjk (Fin.ext hval)

private lemma splicedBlock_pairwise_adj
    (G : SimpleGraph alpha)
    (P : Fin (G.diam + 1) -> alpha)
    (fiber : Fin G.diam -> List {z : alpha // z ∉ Set.range P})
    (hfiber_nodup : ∀ i, (fiber i).Nodup)
    (hfiber_endpoint : ∀ i z, z ∈ fiber i ->
      G.Adj (P (edgeLeft G i)) z.1 ∧ G.Adj z.1 (P (edgeRight G i)))
    (hfiber_clique : ∀ i z w, z ∈ fiber i -> w ∈ fiber i ->
      z.1 ≠ w.1 -> G.Adj z.1 w.1)
    (j : Fin (G.diam + 1)) :
    (splicedBlock G P fiber j).Pairwise G.Adj := by
  refine (splicedBlock_nodup (G := G) (P := P) (fiber := fiber) hfiber_nodup j).pairwise_of_forall_ne ?_
  intro x hx y hy hxy
  rw [mem_splicedBlock] at hx hy
  rcases hx with hx | hx
  · rcases hy with hy | hy
    · exact False.elim (hxy (hx.trans hy.symm))
    · rcases hy with ⟨hj, z, hz, hz_eq⟩
      have hleft : edgeLeft G ⟨j.val, hj⟩ = j := by
        ext
        simp [edgeLeft]
      have hadj := (hfiber_endpoint ⟨j.val, hj⟩ z hz).1
      simpa [hx, hz_eq, hleft] using hadj
  · rcases hx with ⟨hj, z, hz, hz_eq⟩
    rcases hy with hy | hy
    · have hleft : edgeLeft G ⟨j.val, hj⟩ = j := by
        ext
        simp [edgeLeft]
      have hadj := (hfiber_endpoint ⟨j.val, hj⟩ z hz).1
      simpa [hz_eq, hy, hleft] using hadj.symm
    · rcases hy with ⟨hj', w, hw, hw_eq⟩
      have hidx : (⟨j.val, hj⟩ : Fin G.diam) = ⟨j.val, hj'⟩ := by
        ext
        rfl
      have hw' : w ∈ fiber ⟨j.val, hj⟩ := by
        simpa [hidx] using hw
      have hzw : z.1 ≠ w.1 := by
        intro h
        exact hxy (hz_eq.symm.trans (h.trans hw_eq))
      simpa [hz_eq, hw_eq] using
        hfiber_clique ⟨j.val, hj⟩ z w hz hw' hzw

private lemma splicedBlock_isChain
    (G : SimpleGraph alpha)
    (P : Fin (G.diam + 1) -> alpha)
    (fiber : Fin G.diam -> List {z : alpha // z ∉ Set.range P})
    (hfiber_nodup : ∀ i, (fiber i).Nodup)
    (hfiber_endpoint : ∀ i z, z ∈ fiber i ->
      G.Adj (P (edgeLeft G i)) z.1 ∧ G.Adj z.1 (P (edgeRight G i)))
    (hfiber_clique : ∀ i z w, z ∈ fiber i -> w ∈ fiber i ->
      z.1 ≠ w.1 -> G.Adj z.1 w.1)
    (j : Fin (G.diam + 1)) :
    List.IsChain G.Adj (splicedBlock G P fiber j) :=
  (splicedBlock_pairwise_adj (G := G) (P := P) (fiber := fiber)
    hfiber_nodup hfiber_endpoint hfiber_clique j).isChain

private lemma splicedBlock_boundary_adj
    (G : SimpleGraph alpha)
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P)
    (fiber : Fin G.diam -> List {z : alpha // z ∉ Set.range P})
    (hfiber_endpoint : ∀ i z, z ∈ fiber i ->
      G.Adj (P (edgeLeft G i)) z.1 ∧ G.Adj z.1 (P (edgeRight G i)))
    {n : ℕ} (hn : n + 1 < G.diam + 1)
    {x y : alpha}
    (hx : x ∈ (splicedBlock G P fiber ⟨n, Nat.lt_of_succ_lt hn⟩).getLast?)
    (hy : y ∈ (splicedBlock G P fiber ⟨n + 1, hn⟩).head?) :
    G.Adj x y := by
  have hn_diam : n < G.diam := by omega
  have hy_eq : y = P ⟨n + 1, hn⟩ := by
    simpa [splicedBlock_head?] using hy.symm
  have hxmem := List.mem_of_mem_getLast? hx
  rw [mem_splicedBlock] at hxmem
  rcases hxmem with hxP | hxF
  · have hi : (edgeLeft G ⟨n, hn_diam⟩) = ⟨n, Nat.lt_of_succ_lt hn⟩ := by
      ext
      simp [edgeLeft]
    have hr : (edgeRight G ⟨n, hn_diam⟩) = ⟨n + 1, hn⟩ := by
      ext
      simp [edgeRight]
    simpa [hxP, hy_eq, hi, hr] using hP.adj_succ ⟨n, hn_diam⟩
  · rcases hxF with ⟨hj, z, hz, hz_eq⟩
    have hi_eq : (⟨n, hj⟩ : Fin G.diam) = ⟨n, hn_diam⟩ := by
      ext
      rfl
    have hr : (edgeRight G ⟨n, hn_diam⟩) = ⟨n + 1, hn⟩ := by
      ext
      simp [edgeRight]
    have hz0 : z ∈ fiber (⟨n, hj⟩ : Fin G.diam) := by
      simpa using hz
    have hz' : z ∈ fiber ⟨n, hn_diam⟩ := by
      simpa [hi_eq] using hz0
    have hadj := (hfiber_endpoint ⟨n, hn_diam⟩ z hz').2
    simpa [hz_eq, hy_eq, hr] using hadj

lemma exists_spliced_order_of_leftmost_ordered_fibers
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P)
    (assign : {z : alpha // z ∉ Set.range P} -> Fin G.diam)
    (fiber : Fin G.diam -> List {z : alpha // z ∉ Set.range P})
    (hfiber_nodup : ∀ i, (fiber i).Nodup)
    (hfiber_mem : ∀ i z, z ∈ fiber i ↔ assign z = i)
    (hfiber_endpoint : ∀ i z, z ∈ fiber i ->
      G.Adj (P (edgeLeft G i)) z.1 ∧ G.Adj z.1 (P (edgeRight G i)))
    (hfiber_clique : ∀ i z w, z ∈ fiber i -> w ∈ fiber i ->
      z.1 ≠ w.1 -> G.Adj z.1 w.1) :
    ∃ order : List alpha,
      order.Nodup ∧
      (∀ v : alpha, v ∈ order) ∧
      List.IsChain G.Adj order := by
  classical
  let blocks : Fin (G.diam + 1) -> List alpha := splicedBlock G P fiber
  let order : List alpha := (List.ofFn blocks).flatten
  refine ⟨order, ?_, ?_, ?_⟩
  · dsimp [order, blocks]
    rw [List.nodup_flatten]
    constructor
    · intro l hl
      rcases List.mem_ofFn.mp hl with ⟨j, rfl⟩
      exact splicedBlock_nodup (G := G) (P := P) (fiber := fiber) hfiber_nodup j
    · rw [List.pairwise_ofFn]
      intro j k hjk
      exact splicedBlock_disjoint (G := G) (P := P) (hP := hP)
        (assign := assign) (fiber := fiber) (hfiber_mem := hfiber_mem)
        (show j ≠ k by exact ne_of_lt hjk)
  · intro v
    dsimp [order, blocks]
    rw [List.mem_flatten]
    by_cases hvP : v ∈ Set.range P
    · rcases hvP with ⟨j, rfl⟩
      refine ⟨splicedBlock G P fiber j, ?_, ?_⟩
      · rw [List.mem_ofFn]
        exact ⟨j, rfl⟩
      · rw [mem_splicedBlock]
        exact Or.inl rfl
    · let z : {z : alpha // z ∉ Set.range P} := ⟨v, hvP⟩
      let i : Fin G.diam := assign z
      let j : Fin (G.diam + 1) := edgeLeft G i
      refine ⟨splicedBlock G P fiber j, ?_, ?_⟩
      · rw [List.mem_ofFn]
        exact ⟨j, rfl⟩
      · rw [mem_splicedBlock]
        refine Or.inr ?_
        have hj : j.val < G.diam := by
          dsimp [j]
          simpa [edgeLeft] using i.isLt
        refine ⟨hj, z, ?_, rfl⟩
        have hidx : (⟨j.val, hj⟩ : Fin G.diam) = i := by
          ext
          dsimp [j]
          simp [edgeLeft]
        rw [hfiber_mem, hidx]
  · dsimp [order, blocks]
    rw [List.isChain_flatten]
    · constructor
      · intro l hl
        rcases List.mem_ofFn.mp hl with ⟨j, rfl⟩
        exact splicedBlock_isChain (G := G) (P := P) (fiber := fiber)
          hfiber_nodup hfiber_endpoint hfiber_clique j
      · rw [List.isChain_iff_getElem]
        simp only [List.length_ofFn, List.getElem_ofFn]
        intro n hn x hx y hy
        exact splicedBlock_boundary_adj (G := G) (P := P) (hP := hP)
          (fiber := fiber) (hfiber_endpoint := hfiber_endpoint) hn hx hy
    · intro hnil
      rcases List.mem_ofFn.mp hnil with ⟨j, hj⟩
      exact splicedBlock_ne_nil (G := G) (P := P) (fiber := fiber) j hj

lemma exists_hamiltonian_walk_of_b_eq_diam_add_one_diametral_geodesic
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (hb : b G = G.diam + 1)
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P) :
    ∃ a b : alpha, ∃ p : G.Walk a b, p.IsHamiltonian := by
  classical
  have hA : HasLeftmostCliqueFiberAssignment G P :=
    hamiltonian_path_from_leftmost_clique_fibers
      (G := G) (hconn := hconn) (hb := hb) (P := P) (hP := hP)
  rcases exists_leftmost_ordered_fiber_lists
      (G := G) (P := P) hA with
    ⟨assign, _hassign, _hclique, fiber, hfiber_nodup, hfiber_mem,
      hfiber_endpoint, hfiber_clique⟩
  rcases exists_spliced_order_of_leftmost_ordered_fibers
      (G := G) (P := P) (hP := hP) (assign := assign) (fiber := fiber)
      hfiber_nodup hfiber_mem hfiber_endpoint hfiber_clique with
    ⟨order, hN, hcover, hchain⟩
  have hne : order ≠ [] := by
    rcases exists_pair_ne alpha with ⟨v, _w, _hvw⟩
    intro hnil
    have hv : v ∈ ([] : List alpha) := by
      simpa [hnil] using hcover v
    simpa using hv
  rcases exists_walk_of_nonempty_chain_with_support
      (G := G) (order := order) hne hchain with
    ⟨a, c, p, hp_support⟩
  refine ⟨a, c, p, ?_⟩
  have hpN : p.support.Nodup := by
    simpa [hp_support] using hN
  have hp_mem : ∀ v : alpha, v ∈ p.support := by
    intro v
    rw [hp_support]
    exact hcover v
  exact (Walk.IsPath.mk' hpN).isHamiltonian_of_mem hp_mem

lemma source_bound_b_eq_diam_add_one_forces_hamiltonian
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (hb : b G = G.diam + 1) :
    ∃ a b : alpha, ∃ p : G.Walk a b, p.IsHamiltonian := by
  classical
  rcases exists_isDiametralGeodesic (G := G) hconn with ⟨P, hP⟩
  exact exists_hamiltonian_walk_of_b_eq_diam_add_one_diametral_geodesic
    (G := G) (hconn := hconn) (hb := hb) (P := P) (hP := hP)

lemma exists_universal_nodup_chain_of_hamiltonian_walk
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha]
    (G : SimpleGraph alpha)
    (hwalk : ∃ a b : alpha, ∃ p : G.Walk a b, p.IsHamiltonian) :
    ∃ order : List alpha,
      order.Nodup ∧
      (∀ v : alpha, v ∈ order) ∧
      List.IsChain G.Adj order := by
  classical
  rcases hwalk with ⟨a, b, p, hp⟩
  refine ⟨p.support, ?_, ?_, ?_⟩
  · exact hp.isPath.support_nodup
  · intro v
    exact hp.mem_support v
  · exact Walk.isChain_adj_support p

private lemma exists_maximal_path_by_support_length
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nonempty alpha]
    (G : SimpleGraph alpha) :
    ∃ a b : alpha, ∃ p : G.Walk a b,
      p.IsPath ∧
      ∀ u v : alpha, ∀ q : G.Walk u v, q.IsPath → q.support.length ≤ p.support.length := by
  classical
  let S : Finset (Σ a : alpha, Σ b : alpha, G.Path a b) := Finset.univ
  have hS : S.Nonempty := by
    rcases (inferInstance : Nonempty alpha) with ⟨a⟩
    exact ⟨⟨a, ⟨a, Path.nil⟩⟩, by simp [S]⟩
  obtain ⟨x, _hxS, hxmax⟩ := Finset.exists_max_image S
    (fun x : Σ a : alpha, Σ b : alpha, G.Path a b =>
      (x.2.2.1 : G.Walk x.1 x.2.1).support.length) hS
  rcases x with ⟨a, b, p⟩
  refine ⟨a, b, (p : G.Walk a b), p.property, ?_⟩
  intro u v q hq
  have hmem :
      (⟨u, ⟨v, (⟨q, hq⟩ : G.Path u v)⟩⟩ :
        Σ a : alpha, Σ b : alpha, G.Path a b) ∈ S := by
    simp [S]
  exact hxmax _ hmem

lemma exists_path_of_delete_connected_avoiding
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha]
    {G : SimpleGraph alpha}
    (hdelete : ∀ x : alpha, ((⊤ : G.Subgraph).deleteVerts ({x} : Set alpha)).Connected)
    {x y z : alpha} (hy : y ≠ x) (hz : z ≠ x) :
    ∃ p : G.Walk y z, p.IsPath ∧ x ∉ p.support := by
  classical
  let H : G.Subgraph := (⊤ : G.Subgraph).deleteVerts ({x} : Set alpha)
  have hyH : y ∈ H.verts := by
    dsimp [H]
    exact ⟨by simp, by simpa [Set.mem_singleton_iff] using hy⟩
  have hzH : z ∈ H.verts := by
    dsimp [H]
    exact ⟨by simp, by simpa [Set.mem_singleton_iff] using hz⟩
  have hreachH : H.coe.Reachable ⟨y, hyH⟩ ⟨z, hzH⟩ :=
      (hdelete x) ⟨y, hyH⟩ ⟨z, hzH⟩
  rcases hreachH.exists_isPath with ⟨q, hqPath⟩
  refine ⟨q.map H.hom, ?_, ?_⟩
  · rw [Walk.isPath_def, Walk.support_map]
    exact hqPath.support_nodup.map (by
      intro u v huv
      exact Subtype.ext huv)
  · intro hxmem
    rw [Walk.support_map] at hxmem
    rcases List.mem_map.mp hxmem with ⟨w, _hw, hwx⟩
    have hxH : x ∈ H.verts := by
      exact hwx ▸ w.2
    have hnot : x ∉ ({x} : Set alpha) := by
      dsimp [H] at hxH
      exact hxH.2
    exact hnot (by simp)

private lemma longest_path_no_adj_from_left_endpoint_outside
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha]
    {G : SimpleGraph alpha}
    {a b x : alpha} (p : G.Walk a b)
    (hpPath : p.IsPath)
    (hmax : ∀ u v : alpha, ∀ q : G.Walk u v, q.IsPath → q.support.length ≤ p.support.length)
    (hx : x ∉ p.support) :
    ¬ G.Adj x a := by
  intro hxa
  have hqPath : (Walk.cons hxa p).IsPath :=
    hpPath.cons hx
  have hle := hmax x b (Walk.cons hxa p) hqPath
  rw [Walk.support_cons] at hle
  simp only [List.length_cons] at hle
  exact Nat.not_succ_le_self p.support.length hle

private lemma longest_path_no_adj_from_right_endpoint_outside
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha]
    {G : SimpleGraph alpha}
    {a b x : alpha} (p : G.Walk a b)
    (hpPath : p.IsPath)
    (hmax : ∀ u v : alpha, ∀ q : G.Walk u v, q.IsPath → q.support.length ≤ p.support.length)
    (hx : x ∉ p.support) :
    ¬ G.Adj b x := by
  intro hbx
  have hqPath : (p.concat hbx).IsPath :=
    hpPath.concat hx hbx
  have hle := hmax a x (p.concat hbx) hqPath
  rw [Walk.support_concat] at hle
  simp only [List.length_concat] at hle
  exact Nat.not_succ_le_self p.support.length hle

private lemma missed_vertex_ne_left_endpoint
    {alpha : Type*}
    {G : SimpleGraph alpha}
    {a b v : alpha} (p : G.Walk a b)
    (hv : v ∉ p.support) :
    v ≠ a := by
  intro h
  exact hv (h.symm ▸ p.start_mem_support)

private lemma missed_vertex_ne_right_endpoint
    {alpha : Type*}
    {G : SimpleGraph alpha}
    {a b v : alpha} (p : G.Walk a b)
    (hv : v ∉ p.support) :
    v ≠ b := by
  intro h
  exact hv (h.symm ▸ p.end_mem_support)

private lemma longest_path_endpoints_ne_of_missed_vertex
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha]
    {G : SimpleGraph alpha}
    (hconn : G.Connected)
    {a b v : alpha} (p : G.Walk a b)
    (hpPath : p.IsPath)
    (hmax : ∀ u w : alpha, ∀ q : G.Walk u w, q.IsPath → q.support.length ≤ p.support.length)
    (hv : v ∉ p.support) :
    a ≠ b := by
  intro hab
  have hp_len_zero : p.length = 0 := by
    have hend : p.getVert p.length = a := by
      simpa [hab] using p.getVert_length
    exact (hpPath.getVert_eq_start_iff (i := p.length) (by rfl)).mp hend
  rcases hconn.exists_isPath a v with ⟨q, hqPath⟩
  have hav : a ≠ v := (missed_vertex_ne_left_endpoint (G := G) p hv).symm
  have hq_len_pos : 0 < q.length := by
    by_contra hnot
    have hq_len_zero : q.length = 0 := Nat.eq_zero_of_not_pos hnot
    have hav_eq : a = v := Walk.exists_length_eq_zero_iff.mp ⟨q, hq_len_zero⟩
    exact hav hav_eq
  have hle := hmax a v q hqPath
  rw [Walk.length_support, Walk.length_support, hp_len_zero] at hle
  omega

private lemma exists_missed_to_right_path_avoiding_left
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha]
    {G : SimpleGraph alpha}
    (hconn : G.Connected)
    (hdelete : ∀ x : alpha, ((⊤ : G.Subgraph).deleteVerts ({x} : Set alpha)).Connected)
    {a b v : alpha} (p : G.Walk a b)
    (hpPath : p.IsPath)
    (hmax : ∀ u w : alpha, ∀ q : G.Walk u w, q.IsPath → q.support.length ≤ p.support.length)
    (hv : v ∉ p.support) :
    ∃ q : G.Walk v b, q.IsPath ∧ a ∉ q.support := by
  have hva : v ≠ a := missed_vertex_ne_left_endpoint (G := G) p hv
  have hba : b ≠ a :=
    (longest_path_endpoints_ne_of_missed_vertex
      (G := G) hconn p hpPath hmax hv).symm
  exact exists_path_of_delete_connected_avoiding
    (G := G) hdelete (x := a) (y := v) (z := b) hva hba

private lemma exists_left_to_missed_path_avoiding_right
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha]
    {G : SimpleGraph alpha}
    (hconn : G.Connected)
    (hdelete : ∀ x : alpha, ((⊤ : G.Subgraph).deleteVerts ({x} : Set alpha)).Connected)
    {a b v : alpha} (p : G.Walk a b)
    (hpPath : p.IsPath)
    (hmax : ∀ u w : alpha, ∀ q : G.Walk u w, q.IsPath → q.support.length ≤ p.support.length)
    (hv : v ∉ p.support) :
    ∃ q : G.Walk a v, q.IsPath ∧ b ∉ q.support := by
  have hab : a ≠ b :=
    longest_path_endpoints_ne_of_missed_vertex
      (G := G) hconn p hpPath hmax hv
  have hvb : v ≠ b := missed_vertex_ne_right_endpoint (G := G) p hv
  exact exists_path_of_delete_connected_avoiding
    (G := G) hdelete (x := b) (y := a) (z := v) hab hvb

private lemma exists_first_entry_edge_to_path_support
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha]
    {G : SimpleGraph alpha}
    {a b v z : alpha} (p : G.Walk a b) (q : G.Walk v z)
    (hv : v ∉ p.support)
    (hz : z ∈ p.support) :
    ∃ i : ℕ,
      i < q.length ∧
      q.getVert i ∉ p.support ∧
      q.getVert (i + 1) ∈ p.support ∧
      G.Adj (q.getVert i) (q.getVert (i + 1)) := by
  induction q with
  | nil =>
    exact False.elim (hv hz)
  | cons h q ih =>
      by_cases hnext : q.getVert 0 ∈ p.support
      · refine ⟨0, ?_, ?_, ?_, ?_⟩
        · simp [Walk.length_cons]
        · simpa [Walk.getVert_zero] using hv
        · simpa [Walk.getVert_zero, Walk.getVert_cons_succ] using hnext
        · simpa [Walk.getVert_zero, Walk.getVert_cons_succ] using h
      · rcases ih (by simpa [Walk.getVert_zero] using hnext) hz with
          ⟨i, hi, hout, hin, hadj⟩
        refine ⟨i + 1, ?_, ?_, ?_, ?_⟩
        · simpa [Walk.length_cons] using Nat.succ_lt_succ hi
        · simpa [Walk.getVert_cons_succ] using hout
        · simpa [Walk.getVert_cons_succ, Nat.add_assoc] using hin
        · simpa [Walk.getVert_cons_succ, Nat.add_assoc] using hadj

private lemma exists_first_entry_edge_to_path_support_with_prefix
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha]
    {G : SimpleGraph alpha}
    {a b v z : alpha} (p : G.Walk a b) (q : G.Walk v z)
    (hv : v ∉ p.support)
    (hz : z ∈ p.support) :
    ∃ i : ℕ,
      i < q.length ∧
      q.getVert i ∉ p.support ∧
      q.getVert (i + 1) ∈ p.support ∧
      G.Adj (q.getVert i) (q.getVert (i + 1)) ∧
      (∀ k : ℕ, k ≤ i → q.getVert k ∉ p.support) := by
  induction q with
  | nil =>
    exact False.elim (hv hz)
  | cons h q ih =>
      by_cases hnext : q.getVert 0 ∈ p.support
      · refine ⟨0, ?_, ?_, ?_, ?_, ?_⟩
        · simp [Walk.length_cons]
        · simpa [Walk.getVert_zero] using hv
        · simpa [Walk.getVert_zero, Walk.getVert_cons_succ] using hnext
        · simpa [Walk.getVert_zero, Walk.getVert_cons_succ] using h
        · intro k hk
          have hk0 : k = 0 := Nat.eq_zero_of_le_zero hk
          simpa [hk0, Walk.getVert_zero] using hv
      · rcases ih (by simpa [Walk.getVert_zero] using hnext) hz with
          ⟨i, hi, hout, hin, hadj, hprefix⟩
        refine ⟨i + 1, ?_, ?_, ?_, ?_, ?_⟩
        · simpa [Walk.length_cons] using Nat.succ_lt_succ hi
        · simpa [Walk.getVert_cons_succ] using hout
        · simpa [Walk.getVert_cons_succ, Nat.add_assoc] using hin
        · simpa [Walk.getVert_cons_succ, Nat.add_assoc] using hadj
        · intro k hk
          cases k with
          | zero =>
              simpa [Walk.getVert_zero] using hv
          | succ k =>
              have hk_le : k ≤ i := Nat.succ_le_succ_iff.mp hk
              simpa [Walk.getVert_cons_succ] using hprefix k hk_le

private lemma exists_getVert_eq_of_mem_support
    {alpha : Type*}
    {G : SimpleGraph alpha}
    {a b z : alpha} (p : G.Walk a b)
    (hz : z ∈ p.support) :
    ∃ i : ℕ, i ≤ p.length ∧ p.getVert i = z := by
  rcases List.mem_iff_get.mp hz with ⟨i, hi⟩
  have hi_le : i.val ≤ p.length := by
    have hi_lt : i.val < p.length + 1 := by
      simpa [Walk.length_support] using i.isLt
    omega
  refine ⟨i.val, hi_le, ?_⟩
  simpa [List.get_eq_getElem] using
    (by
      rw [p.getVert_eq_support_getElem hi_le]
      exact hi : p.getVert i.val = z)

private lemma support_take_disjoint_of_getVert_prefix
    {alpha : Type*}
    {G : SimpleGraph alpha}
    {a b v z : alpha} (p : G.Walk a b) (q : G.Walk v z)
    {i : ℕ}
    (hprefix : ∀ k : ℕ, k ≤ i → q.getVert k ∉ p.support) :
    ∀ w : alpha, w ∈ (q.take i).support → w ∉ p.support := by
  intro w hw
  rw [Walk.mem_support_iff_exists_getVert] at hw
  rcases hw with ⟨k, hkw, hk_len⟩
  have hk_le_i : k ≤ i := by
    have hk_le_min : k ≤ i ⊓ q.length := by
      simpa [Walk.take_length] using hk_len
    exact le_trans hk_le_min (Nat.min_le_left i q.length)
  have hqkw : q.getVert k = w := by
    simpa [Walk.take_getVert, Nat.min_eq_right hk_le_i] using hkw
  simpa [hqkw] using hprefix k hk_le_i

private lemma walk_bypass_support_avoids_of_support_avoids
    {alpha : Type*} [DecidableEq alpha]
    {G : SimpleGraph alpha}
    {a b u v : alpha} (p : G.Walk a b) (q : G.Walk u v)
    (havoid : ∀ z : alpha, z ∈ q.support → z ∉ p.support) :
    ∀ z : alpha, z ∈ q.bypass.support → z ∉ p.support := by
  intro z hz
  exact havoid z (q.support_bypass_subset hz)

private lemma walk_bypass_endpoint_mem_support
    {alpha : Type*} [DecidableEq alpha]
    {G : SimpleGraph alpha}
    {u v : alpha} (q : G.Walk u v) :
    u ∈ q.bypass.support ∧ v ∈ q.bypass.support := by
  exact ⟨q.bypass.start_mem_support, q.bypass.end_mem_support⟩

private lemma reverse_append_common_start_mem_support
    {alpha : Type*}
    {G : SimpleGraph alpha}
    {x v y : alpha}
    (qx : G.Walk v x) (qy : G.Walk v y) :
    v ∈ (qx.reverse.append qy).support := by
  exact Walk.subset_support_append_left _ _
    (by simpa [Walk.support_reverse] using List.mem_reverse.mpr qx.start_mem_support)

private lemma reverse_append_support_avoids_of_support_avoids
    {alpha : Type*}
    {G : SimpleGraph alpha}
    {p0 : List alpha}
    {x v y : alpha}
    (qx : G.Walk v x) (qy : G.Walk v y)
    (hxout : ∀ z : alpha, z ∈ qx.support → z ∉ p0)
    (hyout : ∀ z : alpha, z ∈ qy.support → z ∉ p0) :
    ∀ z : alpha, z ∈ (qx.reverse.append qy).support → z ∉ p0 := by
  intro z hz
  rw [Walk.mem_support_append_iff] at hz
  rcases hz with hz | hz
  · rw [Walk.support_reverse] at hz
    exact hxout z (List.mem_reverse.mp hz)
  · exact hyout z hz

lemma exists_internally_disjoint_first_entry_prefixes_to_path_support
    {alpha : Type*} [DecidableEq alpha]
    {G : SimpleGraph alpha}
    {p0 : List alpha}
    {v x y : alpha}
    (qx : G.Walk v x)
    (qy : G.Walk v y)
    (hqx : qx.IsPath)
    (hqy : qy.IsPath)
    (hxout : ∀ z : alpha, z ∈ qx.support → z ∉ p0)
    (hyout : ∀ z : alpha, z ∈ qy.support → z ∉ p0) :
    ∃ x' y' : alpha, ∃ qx' : G.Walk v x', ∃ qy' : G.Walk v y',
      qx'.IsPath ∧
      qy'.IsPath ∧
      (∀ z : alpha, z ∈ qx'.support → z ∉ p0) ∧
      (∀ z : alpha, z ∈ qy'.support → z ∉ p0) ∧
      (∀ z : alpha, z ∈ qx'.support → z ∈ qy'.support → z = v) ∧
      x' ∈ qx.support ∧
      y' ∈ qy.support := by
  have _hqx_used := hqx.support_nodup
  have _hqy_used := hqy.support_nodup
  let qx' : G.Walk v v := Walk.nil
  let qy' : G.Walk v v := Walk.nil
  refine ⟨v, v, qx', qy', ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · exact Walk.IsPath.nil
  · exact Walk.IsPath.nil
  · intro z hz
    dsimp [qx'] at hz
    simp only [List.mem_singleton] at hz
    simpa [hz] using hxout v qx.start_mem_support
  · intro z hz
    dsimp [qy'] at hz
    simp only [List.mem_singleton] at hz
    simpa [hz] using hyout v qy.start_mem_support
  · intro z hz _
    dsimp [qx'] at hz
    simp only [List.mem_singleton] at hz
    exact hz
  · exact qx.start_mem_support
  · exact qy.start_mem_support

lemma exists_outside_path_through_common_vertex_of_two_internally_disjoint_outside_paths
    {alpha : Type*} [DecidableEq alpha]
    {G : SimpleGraph alpha}
    {p0 : List alpha}
    {x v y : alpha}
    (qx : G.Walk v x)
    (qy : G.Walk v y)
    (hqx : qx.IsPath)
    (hqy : qy.IsPath)
    (hmeet : ∀ z : alpha, z ∈ qx.support → z ∈ qy.support → z = v)
    (hxout : ∀ z : alpha, z ∈ qx.support → z ∉ p0)
    (hyout : ∀ z : alpha, z ∈ qy.support → z ∉ p0) :
    ∃ q : G.Walk x y,
      q.IsPath ∧
      v ∈ q.support ∧
      ∀ z : alpha, z ∈ q.support → z ∉ p0 := by
  classical
  let q : G.Walk x y := qx.reverse.append qy
  refine ⟨q, ?_, ?_, ?_⟩
  · rw [Walk.isPath_def]
    dsimp [q]
    rw [Walk.support_append]
    refine hqx.reverse.support_nodup.append hqy.support_nodup.tail ?_
    rw [List.disjoint_left]
    intro z hzqx_rev hzqy_tail
    have hzqx : z ∈ qx.support := by
      rw [Walk.support_reverse] at hzqx_rev
      exact List.mem_reverse.mp hzqx_rev
    have hzqy : z ∈ qy.support := List.mem_of_mem_tail hzqy_tail
    have hzv : z = v := hmeet z hzqx hzqy
    have hv_tail : v ∈ qy.support.tail := by
      simpa [hzv] using hzqy_tail
    have hqy_support_nodup :
        (v :: qy.support.tail).Nodup := by
      simpa [← qy.support_eq_cons] using hqy.support_nodup
    exact (List.nodup_cons.mp hqy_support_nodup).1 hv_tail
  · dsimp [q]
    exact reverse_append_common_start_mem_support qx qy
  · intro z hz
    dsimp [q] at hz
    exact reverse_append_support_avoids_of_support_avoids qx qy hxout hyout z hz

lemma exists_two_endpoint_avoiding_paths_from_vertex_to_set_of_delete_connected
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α}
    (hdelete : ∀ x : α,
      ((⊤ : G.Subgraph).deleteVerts ({x} : Set α)).Connected)
    {v : α} {S : Set α}
    (hvS : v ∉ S)
    (hS_two : ∃ s t : α, s ∈ S ∧ t ∈ S ∧ s ≠ t) :
    ∃ s t : α, ∃ qs : G.Walk v s, ∃ qt : G.Walk v t,
      s ∈ S ∧ t ∈ S ∧ s ≠ t ∧
      qs.IsPath ∧ qt.IsPath ∧ t ∉ qs.support ∧ s ∉ qt.support := by
  classical
  rcases hS_two with ⟨s, t, hsS, htS, hst⟩
  have hvs : v ≠ s := by
    intro hvs_eq
    exact hvS (hvs_eq ▸ hsS)
  have hvt : v ≠ t := by
    intro hvt_eq
    exact hvS (hvt_eq ▸ htS)
  rcases exists_path_of_delete_connected_avoiding
      (G := G) hdelete (x := t) (y := v) (z := s) hvt hst with
    ⟨qs, hqsPath, ht_qs⟩
  rcases exists_path_of_delete_connected_avoiding
      (G := G) hdelete (x := s) (y := v) (z := t) hvs hst.symm with
    ⟨qt, hqtPath, hs_qt⟩
  exact ⟨s, t, qs, qt, hsS, htS, hst, hqsPath, hqtPath, ht_qs, hs_qt⟩

private lemma exists_two_internal_vertices_of_not_endpoint_or_one_internal
    {β : Type*} {H : SimpleGraph β} {u w : β} (p : H.Walk u w)
    (hnotEndpoints : ¬ ∀ z, z ∈ p.support → z = u ∨ z = w)
    (hnotOneInternal : ¬ ∃ x : β, x ≠ u ∧ x ≠ w ∧
      ∀ z, z ∈ p.support → z = u ∨ z = w ∨ z = x) :
    ∃ x y : β,
      x ∈ p.support ∧ y ∈ p.support ∧
      x ≠ u ∧ x ≠ w ∧ y ≠ u ∧ y ≠ w ∧ x ≠ y := by
  classical
  push_neg at hnotEndpoints
  rcases hnotEndpoints with ⟨x, hxmem, hxu, hxw⟩
  by_contra hno
  push_neg at hno
  apply hnotOneInternal
  refine ⟨x, hxu, hxw, ?_⟩
  intro z hz
  by_cases hzu : z = u
  · exact Or.inl hzu
  · by_cases hzw : z = w
    · exact Or.inr (Or.inl hzw)
    · exact Or.inr (Or.inr ((hno x z hxmem hz hxu hxw hzu hzw).symm))

private lemma exists_path_avoiding_singleton_of_no_small_endpoint_separator
    {β : Type*} [Fintype β] [DecidableEq β]
    {H : SimpleGraph β} {u w x : β}
    (hxu : x ≠ u) (hxw : x ≠ w)
    (hsep : ∀ C : Finset β, C.card < 2 → u ∉ C → w ∉ C →
      ∃ p : H.Walk u w, p.IsPath ∧ ∀ z, z ∈ p.support → z ∉ C) :
    ∃ p : H.Walk u w, p.IsPath ∧ x ∉ p.support := by
  classical
  rcases hsep ({x} : Finset β) (by simp)
      (by simpa using hxu.symm) (by simpa using hxw.symm) with
    ⟨p, hpPath, hpAvoid⟩
  exact ⟨p, hpPath, by
    intro hxmem
    exact hpAvoid x hxmem (by simp)⟩

private lemma exists_path_of_no_small_endpoint_separator
    {β : Type*} [Fintype β] [DecidableEq β]
    {H : SimpleGraph β} {u w : β}
    (hsep : ∀ C : Finset β, C.card < 2 → u ∉ C → w ∉ C →
      ∃ p : H.Walk u w, p.IsPath ∧ ∀ z, z ∈ p.support → z ∉ C) :
    ∃ p : H.Walk u w, p.IsPath := by
  classical
  rcases hsep ∅ (by simp) (by simp) (by simp) with ⟨p, hpPath, _hpAvoid⟩
  exact ⟨p, hpPath⟩

private lemma reachable_delete_singleton_of_no_small_endpoint_separator
    {β : Type*} [Fintype β] [DecidableEq β]
    {H : SimpleGraph β} {u w x : β}
    (hxu : x ≠ u) (hxw : x ≠ w)
    (hsep : ∀ C : Finset β, C.card < 2 → u ∉ C → w ∉ C →
      ∃ p : H.Walk u w, p.IsPath ∧ ∀ z, z ∈ p.support → z ∉ C) :
    let D : H.Subgraph := (⊤ : H.Subgraph).deleteVerts ({x} : Set β)
    D.coe.Reachable
      ⟨u, by
        dsimp [D]
        exact ⟨by simp, by simpa [Set.mem_singleton_iff] using hxu.symm⟩⟩
      ⟨w, by
        dsimp [D]
        exact ⟨by simp, by simpa [Set.mem_singleton_iff] using hxw.symm⟩⟩ := by
  classical
  intro D
  rcases exists_path_avoiding_singleton_of_no_small_endpoint_separator
      (H := H) (u := u) (w := w) (x := x) hxu hxw hsep with
    ⟨p, _hpPath, hpAvoid⟩
  have hp_le : p.toSubgraph ≤ D := by
    constructor
    · intro y hy
      have hysupp : y ∈ p.support := by
        simpa [Walk.mem_verts_toSubgraph] using hy
      dsimp [D]
      exact ⟨by simp, by
        intro hyx
        exact hpAvoid (hyx ▸ hysupp)⟩
    · intro y z hyz
      have hysupp : y ∈ p.support :=
        Walk.mem_support_of_adj_toSubgraph hyz
      have hzsupp : z ∈ p.support :=
        Walk.mem_support_of_adj_toSubgraph hyz.symm
      dsimp [D]
      exact
        ⟨⟨by simp, by
          intro hyx
          have hyx' : y = x := by simpa using hyx
          exact hpAvoid (hyx' ▸ hysupp)⟩,
         ⟨by simp, by
          intro hzx
          have hzx' : z = x := by simpa using hzx
          exact hpAvoid (hzx' ▸ hzsupp)⟩,
         by simpa using p.toSubgraph.adj_sub hyz⟩
  exact Reachable.map (Subgraph.inclusion hp_le)
    (p.toSubgraph_connected
      ⟨u, p.start_mem_verts_toSubgraph⟩
      ⟨w, p.end_mem_verts_toSubgraph⟩)

private lemma reachable_pair_delete_singleton_of_two_no_small_endpoint_separators
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x : α}
    (hxv : x ≠ v)
    (hsep_vs : ∀ C : Finset α, C.card < 2 → v ∉ C → s ∉ C →
      ∃ q : G.Walk v s, q.IsPath ∧ ∀ z, z ∈ q.support → z ∉ C)
    (hsep_vt : ∀ C : Finset α, C.card < 2 → v ∉ C → t ∉ C →
      ∃ q : G.Walk v t, q.IsPath ∧ ∀ z, z ∈ q.support → z ∉ C) :
    (∀ hxs : x ≠ s,
      let D : G.Subgraph := (⊤ : G.Subgraph).deleteVerts ({x} : Set α)
      D.coe.Reachable
        ⟨v, by
          dsimp [D]
          exact ⟨by simp, by simpa [Set.mem_singleton_iff] using hxv.symm⟩⟩
        ⟨s, by
          dsimp [D]
          exact ⟨by simp, by simpa [Set.mem_singleton_iff] using hxs.symm⟩⟩) ∧
    (∀ hxt : x ≠ t,
      let D : G.Subgraph := (⊤ : G.Subgraph).deleteVerts ({x} : Set α)
      D.coe.Reachable
        ⟨v, by
          dsimp [D]
          exact ⟨by simp, by simpa [Set.mem_singleton_iff] using hxv.symm⟩⟩
        ⟨t, by
          dsimp [D]
          exact ⟨by simp, by simpa [Set.mem_singleton_iff] using hxt.symm⟩⟩) := by
  constructor
  · intro hxs
    exact reachable_delete_singleton_of_no_small_endpoint_separator
      (H := G) (u := v) (w := s) (x := x) hxv hxs hsep_vs
  · intro hxt
    exact reachable_delete_singleton_of_no_small_endpoint_separator
      (H := G) (u := v) (w := t) (x := x) hxv hxt hsep_vt

private lemma exists_terminal_set_endpoint_avoiding_pair
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t : α}
    (hvs : v ≠ s) (hvt : v ≠ t) (_hst : s ≠ t)
    (hsep : ∀ C : Finset α, C.card < 2 → v ∉ C →
      ∃ u : α, (u = s ∨ u = t) ∧ u ∉ C ∧
        ∃ q : G.Walk v u, q.IsPath ∧ ∀ z, z ∈ q.support → z ∉ C) :
    ∃ qs : G.Walk v s, ∃ qt : G.Walk v t,
      qs.IsPath ∧ qt.IsPath ∧ t ∉ qs.support ∧ s ∉ qt.support := by
  classical
  rcases hsep ({t} : Finset α) (by simp) (by simpa using hvt) with
    ⟨u_s, hu_s, hut_not_mem, q_s, hq_sPath, hq_sAvoid⟩
  have hu_s_eq : u_s = s := by
    rcases hu_s with hus | hut
    · exact hus
    · exact False.elim (hut_not_mem (by simp [hut]))
  let qs : G.Walk v s := q_s.copy rfl hu_s_eq
  have hqsPath : qs.IsPath := by
    simpa [qs] using hq_sPath
  have ht_qs : t ∉ qs.support := by
    intro htmem
    exact hq_sAvoid t (by simpa [qs] using htmem) (by simp)
  rcases hsep ({s} : Finset α) (by simp) (by simpa using hvs) with
    ⟨u_t, hu_t, hus_not_mem, q_t, hq_tPath, hq_tAvoid⟩
  have hu_t_eq : u_t = t := by
    rcases hu_t with hus | hut
    · exact False.elim (hus_not_mem (by simp [hus]))
    · exact hut
  let qt : G.Walk v t := q_t.copy rfl hu_t_eq
  have hqtPath : qt.IsPath := by
    simpa [qt] using hq_tPath
  have hs_qt : s ∉ qt.support := by
    intro hsmem
    exact hq_tAvoid s (by simpa [qt] using hsmem) (by simp)
  exact ⟨qs, qt, hqsPath, hqtPath, ht_qs, hs_qt⟩

private lemma exists_terminal_path_avoiding_singleton_of_terminal_set_separator
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x : α}
    (hxv : x ≠ v)
    (hsep : ∀ C : Finset α, C.card < 2 → v ∉ C →
      ∃ u : α, (u = s ∨ u = t) ∧ u ∉ C ∧
        ∃ q : G.Walk v u, q.IsPath ∧ ∀ z, z ∈ q.support → z ∉ C) :
    ∃ u : α, (u = s ∨ u = t) ∧ u ≠ x ∧
      ∃ q : G.Walk v u, q.IsPath ∧ x ∉ q.support := by
  classical
  rcases hsep ({x} : Finset α) (by simp) (by simpa using hxv.symm) with
    ⟨u, hu_terminal, hux, q, hqPath, hqAvoid⟩
  refine ⟨u, hu_terminal, ?_, q, hqPath, ?_⟩
  · intro hux_eq
    exact hux (by simp [hux_eq])
  · intro hxq
    exact hqAvoid x hxq (by simp)

private lemma common_support_erase_card_eq_zero_of_meet_only_apex
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t : α}
    (qs : G.Walk v s) (qt : G.Walk v t)
    (hmeet : ∀ z : α, z ∈ qs.support → z ∈ qt.support → z = v) :
    ((qs.support.toFinset ∩ qt.support.toFinset).erase v).card = 0 := by
  classical
  apply Finset.card_eq_zero.mpr
  rw [Finset.eq_empty_iff_forall_notMem]
  intro z hz
  rw [Finset.mem_erase, Finset.mem_inter] at hz
  exact hz.1 (hmeet z (by simpa using hz.2.1) (by simpa using hz.2.2))

private lemma common_support_erase_card_pos_of_common_nonapex
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x : α}
    {qs : G.Walk v s} {qt : G.Walk v t}
    (hxqs : x ∈ qs.support) (hxqt : x ∈ qt.support) (hxv : x ≠ v) :
    0 < ((qs.support.toFinset ∩ qt.support.toFinset).erase v).card := by
  classical
  apply Finset.card_pos.mpr
  refine ⟨x, ?_⟩
  rw [Finset.mem_erase, Finset.mem_inter]
  exact ⟨hxv, by simpa using hxqs, by simpa using hxqt⟩

private lemma card_lt_of_subset_erase_mem
    {α : Type*} [DecidableEq α] {A B : Finset α} {x : α}
    (hsub : B ⊆ A.erase x) (hx : x ∈ A) :
    B.card < A.card := by
  exact lt_of_le_of_lt (Finset.card_le_card hsub)
    (Finset.card_erase_lt_of_mem hx)

private lemma exists_mem_not_mem_erase_of_not_card_lt
    {α : Type*} [DecidableEq α] {A B : Finset α} {x : α}
    (hxA : x ∈ A) (hnot : ¬ B.card < A.card) :
    ∃ y : α, y ∈ B ∧ y ∉ A.erase x := by
  classical
  by_contra hnone
  push_neg at hnone
  have hsub : B ⊆ A.erase x := by
    intro y hy
    exact hnone y hy
  exact hnot (card_lt_of_subset_erase_mem hsub hxA)

private lemma common_support_erase_card_lt_of_subset_erase_common
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t : α}
    {qs qs' : G.Walk v s} {qt qt' : G.Walk v t} {x : α}
    (hsub :
      ((qs'.support.toFinset ∩ qt'.support.toFinset).erase v) ⊆
        (((qs.support.toFinset ∩ qt.support.toFinset).erase v).erase x))
    (hxqs : x ∈ qs.support) (hxqt : x ∈ qt.support) (hxv : x ≠ v) :
    ((qs'.support.toFinset ∩ qt'.support.toFinset).erase v).card <
      ((qs.support.toFinset ∩ qt.support.toFinset).erase v).card := by
  classical
  apply card_lt_of_subset_erase_mem hsub
  rw [Finset.mem_erase, Finset.mem_inter]
  exact ⟨hxv, by simpa using hxqs, by simpa using hxqt⟩

private lemma card_le_of_subset_insert_erase_mem
    {α : Type*} [DecidableEq α] {A B : Finset α} {x y : α}
    (hsub : B ⊆ insert y (A.erase x)) (hx : x ∈ A) :
    B.card ≤ A.card := by
  classical
  refine le_trans (Finset.card_le_card hsub) ?_
  by_cases hy : y ∈ A.erase x
  · rw [Finset.insert_eq_of_mem hy]
    exact Nat.le_of_lt (Finset.card_erase_lt_of_mem hx)
  · rw [Finset.card_insert_of_notMem hy]
    have hlt : (A.erase x).card < A.card :=
      Finset.card_erase_lt_of_mem hx
    omega

private lemma meet_only_apex_of_common_support_erase_card_eq_zero
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t : α}
    (qs : G.Walk v s) (qt : G.Walk v t)
    (hcard : ((qs.support.toFinset ∩ qt.support.toFinset).erase v).card = 0) :
    ∀ z : α, z ∈ qs.support → z ∈ qt.support → z = v := by
  classical
  intro z hzs hzt
  by_contra hzv
  have hzmem : z ∈ ((qs.support.toFinset ∩ qt.support.toFinset).erase v) := by
    rw [Finset.mem_erase, Finset.mem_inter]
    exact ⟨hzv, by simpa using hzs, by simpa using hzt⟩
  have hpos : 0 < ((qs.support.toFinset ∩ qt.support.toFinset).erase v).card :=
    Finset.card_pos.mpr ⟨z, hzmem⟩
  omega

private lemma common_support_erase_card_le_of_subset_insert_erase_common
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t : α}
    {qs qs' : G.Walk v s} {qt qt' : G.Walk v t} {x y : α}
    (hsub :
      ((qs'.support.toFinset ∩ qt'.support.toFinset).erase v) ⊆
        insert y (((qs.support.toFinset ∩ qt.support.toFinset).erase v).erase x))
    (hxqs : x ∈ qs.support) (hxqt : x ∈ qt.support) (hxv : x ≠ v) :
    ((qs'.support.toFinset ∩ qt'.support.toFinset).erase v).card ≤
      ((qs.support.toFinset ∩ qt.support.toFinset).erase v).card := by
  classical
  apply card_le_of_subset_insert_erase_mem hsub
  rw [Finset.mem_erase, Finset.mem_inter]
  exact ⟨hxv, by simpa using hxqs, by simpa using hxqt⟩

private def terminalPathPairCommonCard
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t : α}
    (pair : G.Path v s × G.Path v t) : ℕ :=
  ((((pair.1 : G.Walk v s).support.toFinset ∩
    (pair.2 : G.Walk v t).support.toFinset).erase v).card)

private lemma terminalPathPairCommonCard_mk
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t : α}
    (qs : G.Walk v s) (qt : G.Walk v t)
    (hqs : qs.IsPath) (hqt : qt.IsPath) :
    terminalPathPairCommonCard
      ((⟨qs, hqs⟩ : G.Path v s), (⟨qt, hqt⟩ : G.Path v t)) =
      (((qs.support.toFinset ∩ qt.support.toFinset).erase v).card) := by
  rfl

private lemma terminalPathPairCommonCard_le_of_subset_insert_erase_common
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x y : α}
    {pair pair' : G.Path v s × G.Path v t}
    (hsub :
      (((pair'.1 : G.Walk v s).support.toFinset ∩
          (pair'.2 : G.Walk v t).support.toFinset).erase v) ⊆
        insert y
          ((((pair.1 : G.Walk v s).support.toFinset ∩
              (pair.2 : G.Walk v t).support.toFinset).erase v).erase x))
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v) :
    terminalPathPairCommonCard pair' ≤ terminalPathPairCommonCard pair := by
  simpa [terminalPathPairCommonCard] using
    (common_support_erase_card_le_of_subset_insert_erase_common
      (G := G) (v := v) (s := s) (t := t)
      (qs := (pair.1 : G.Walk v s)) (qt := (pair.2 : G.Walk v t))
      (qs' := (pair'.1 : G.Walk v s)) (qt' := (pair'.2 : G.Walk v t))
      (x := x) (y := y) hsub hx_left hx_right hxv)

private lemma terminalPathPairCommonCard_pos_of_common_nonapex
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x : α}
    {pair : G.Path v s × G.Path v t}
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v) :
    0 < terminalPathPairCommonCard pair := by
  simpa [terminalPathPairCommonCard] using
    common_support_erase_card_pos_of_common_nonapex
      (G := G) (v := v) (s := s) (t := t)
      (qs := (pair.1 : G.Walk v s)) (qt := (pair.2 : G.Walk v t))
      hx_left hx_right hxv

private lemma terminalPathPairCommonCard_eq_zero_of_meet_only_apex
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t : α}
    {pair : G.Path v s × G.Path v t}
    (hmeet : ∀ z : α, z ∈ (pair.1 : G.Walk v s).support →
      z ∈ (pair.2 : G.Walk v t).support → z = v) :
    terminalPathPairCommonCard pair = 0 := by
  simpa [terminalPathPairCommonCard] using
    common_support_erase_card_eq_zero_of_meet_only_apex
      (G := G) (v := v) (s := s) (t := t)
      (pair.1 : G.Walk v s) (pair.2 : G.Walk v t) hmeet

private lemma terminalPathPairCommonCard_lt_of_meet_only_apex_and_common_nonapex
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x : α}
    {pair pair' : G.Path v s × G.Path v t}
    (hmeet' : ∀ z : α, z ∈ (pair'.1 : G.Walk v s).support →
      z ∈ (pair'.2 : G.Walk v t).support → z = v)
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v) :
    terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  have hnew_zero :
      terminalPathPairCommonCard pair' = 0 :=
    terminalPathPairCommonCard_eq_zero_of_meet_only_apex
      (pair := pair') hmeet'
  have hold_pos :
      0 < terminalPathPairCommonCard pair :=
    terminalPathPairCommonCard_pos_of_common_nonapex
      (pair := pair) hx_left hx_right hxv
  omega

private def terminalPathPairSupportLength
    {α : Type*}
    {G : SimpleGraph α} {v s t : α}
    (pair : G.Path v s × G.Path v t) : ℕ :=
  (pair.1 : G.Walk v s).support.length +
    (pair.2 : G.Walk v t).support.length

private lemma support_length_toPath_le
    {α : Type*} {G : SimpleGraph α} {u v : α}
    (p : G.Walk u v) :
    (p.toPath : G.Walk u v).support.length ≤ p.support.length := by
  rw [Walk.length_support, Walk.length_support]
  exact Nat.succ_le_succ p.length_bypass_le

private lemma walk_bypass_eq_self_of_isPath
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {u v : α} {p : G.Walk u v}
    (hp : p.IsPath) :
    p.bypass = p := by
  induction p with
  | nil => rfl
  | cons h p ih =>
      rw [Walk.cons_isPath_iff] at hp
      simp only [Walk.bypass]
      have hp_bypass : p.bypass = p := ih hp.1
      simp [hp_bypass, hp.2]

private lemma walk_toPath_eq_self_of_isPath
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {u v : α} {p : G.Walk u v}
    (hp : p.IsPath) :
    (p.toPath : G.Walk u v) = p := by
  simpa [Walk.toPath] using
    (walk_bypass_eq_self_of_isPath (G := G) (p := p) hp)

private lemma support_bypass_sublist
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {u v : α} (p : G.Walk u v) :
    List.Sublist p.bypass.support p.support := by
  induction p with
  | nil =>
      rfl
  | @cons u₀ v₀ w₀ h p ih =>
      simp only [Walk.bypass]
      split_ifs with hs
      · have hdrop :
            List.Sublist (p.bypass.dropUntil _ hs).support p.bypass.support := by
          exact (Walk.isSubwalk_iff_support_isInfix.mp
            (Walk.isSubwalk_dropUntil p.bypass hs)).sublist
        exact hdrop.trans (List.sublist_cons_of_sublist u₀ ih)
      · simpa [Walk.support_cons] using ih.cons_cons u₀

private lemma mem_support_toPath_of_isPath
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {u v z : α} {p : G.Walk u v}
    (hp : p.IsPath) (hz : z ∈ p.support) :
    z ∈ (p.toPath : G.Walk u v).support := by
  simpa [walk_toPath_eq_self_of_isPath (G := G) (p := p) hp] using hz

private lemma mem_support_toPath_append_right_of_append_isPath
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {u v w z : α}
    (p : G.Walk u v) (q : G.Walk v w)
    (hpq : (p.append q).IsPath) (hz : z ∈ q.support) :
    z ∈ ((p.append q).toPath : G.Walk u w).support := by
  exact mem_support_toPath_of_isPath
    (G := G) (p := p.append q) hpq
    (Walk.subset_support_append_right p q hz)

private lemma not_isPath_append_of_not_mem_toPath_append_right
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {u v w z : α}
    (p : G.Walk u v) (q : G.Walk v w)
    (hz : z ∈ q.support)
    (hnot : z ∉ ((p.append q).toPath : G.Walk u w).support) :
    ¬ (p.append q).IsPath := by
  intro hpq
  exact hnot
    (mem_support_toPath_append_right_of_append_isPath
      (G := G) p q hpq hz)

private lemma not_isPath_append_of_not_mem_toPath_append_left
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {u v w z : α}
    (p : G.Walk u v) (q : G.Walk v w)
    (hz : z ∈ p.support)
    (hnot : z ∉ ((p.append q).toPath : G.Walk u w).support) :
    ¬ (p.append q).IsPath := by
  intro hpq
  exact hnot
    (mem_support_toPath_of_isPath
      (G := G) (p := p.append q) hpq
      (Walk.subset_support_append_left p q hz))

private lemma exists_mem_left_and_right_tail_of_not_isPath_append
    {α : Type*}
    {G : SimpleGraph α} {u v w : α}
    {p : G.Walk u v} {q : G.Walk v w}
    (hp : p.IsPath) (hq : q.IsPath)
    (hnot : ¬ (p.append q).IsPath) :
    ∃ z : α, z ∈ p.support ∧ z ∈ q.support.tail := by
  classical
  have hnot_nodup : ¬ (p.support ++ q.support.tail).Nodup := by
    intro hnodup
    exact hnot ((Walk.isPath_def (p.append q)).mpr (by
      simpa [Walk.support_append] using hnodup))
  have htail_nodup : q.support.tail.Nodup :=
    hq.support_nodup.sublist (List.tail_sublist q.support)
  have hnot_disjoint : ¬ List.Disjoint p.support q.support.tail := by
    intro hdisj
    exact hnot_nodup (hp.support_nodup.append htail_nodup hdisj)
  by_contra hnone
  apply hnot_disjoint
  rw [List.disjoint_left]
  intro a ha hb
  exact hnone ⟨a, ha, hb⟩

private lemma exists_left_prefix_right_suffix_tail_of_not_mem_alt
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x y : α}
    (left : G.Walk v s) (right : G.Walk v t)
    (hleftPath : left.IsPath) (hrightPath : right.IsPath)
    (hx_left : x ∈ left.support)
    (hx_right : x ∈ right.support)
    (hy_suffix : y ∈ (right.dropUntil x hx_right).support)
    (hy_not_alt :
      y ∉
        (((left.takeUntil x hx_left).append
          (right.dropUntil x hx_right)).toPath : G.Walk v t).support) :
    ∃ r : α,
      r ∈ (left.takeUntil x hx_left).support ∧
      r ∈ (right.dropUntil x hx_right).support.tail := by
  classical
  have hleft_prefix_path : (left.takeUntil x hx_left).IsPath :=
    Walk.isPath_of_isSubwalk (Walk.isSubwalk_takeUntil left hx_left) hleftPath
  have hright_suffix_path : (right.dropUntil x hx_right).IsPath :=
    Walk.isPath_of_isSubwalk (Walk.isSubwalk_dropUntil right hx_right) hrightPath
  have hnot_path :
      ¬ ((left.takeUntil x hx_left).append
        (right.dropUntil x hx_right)).IsPath :=
    not_isPath_append_of_not_mem_toPath_append_right
      (G := G) (p := left.takeUntil x hx_left)
      (q := right.dropUntil x hx_right) hy_suffix hy_not_alt
  exact exists_mem_left_and_right_tail_of_not_isPath_append
    (G := G) hleft_prefix_path hright_suffix_path hnot_path

private lemma exists_left_prefix_right_suffix_tail_of_not_mem_left_alt
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x y : α}
    (left : G.Walk v s) (right : G.Walk v t)
    (hleftPath : left.IsPath) (hrightPath : right.IsPath)
    (hx_left : x ∈ left.support)
    (hx_right : x ∈ right.support)
    (hy_left_prefix : y ∈ (left.takeUntil x hx_left).support)
    (hy_not_alt :
      y ∉
        (((left.takeUntil x hx_left).append
          (right.dropUntil x hx_right)).toPath : G.Walk v t).support) :
    ∃ r : α,
      r ∈ (left.takeUntil x hx_left).support ∧
      r ∈ (right.dropUntil x hx_right).support.tail := by
  classical
  have hleft_prefix_path : (left.takeUntil x hx_left).IsPath :=
    Walk.isPath_of_isSubwalk (Walk.isSubwalk_takeUntil left hx_left) hleftPath
  have hright_suffix_path : (right.dropUntil x hx_right).IsPath :=
    Walk.isPath_of_isSubwalk (Walk.isSubwalk_dropUntil right hx_right) hrightPath
  have hnot_path :
      ¬ ((left.takeUntil x hx_left).append
        (right.dropUntil x hx_right)).IsPath :=
    not_isPath_append_of_not_mem_toPath_append_left
      (G := G) (p := left.takeUntil x hx_left)
      (q := right.dropUntil x hx_right) hy_left_prefix hy_not_alt
  exact exists_mem_left_and_right_tail_of_not_isPath_append
    (G := G) hleft_prefix_path hright_suffix_path hnot_path

private lemma exists_old_common_ne_x_of_right_suffix_not_mem_alt
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x y : α}
    (left : G.Walk v s) (right : G.Walk v t)
    (hleftPath : left.IsPath) (hrightPath : right.IsPath)
    (hx_left : x ∈ left.support)
    (hx_right : x ∈ right.support)
    (hy_suffix : y ∈ (right.dropUntil x hx_right).support)
    (hy_not_alt :
      y ∉
        (((left.takeUntil x hx_left).append
          (right.dropUntil x hx_right)).toPath : G.Walk v t).support) :
    ∃ r : α, r ∈ left.support ∧ r ∈ right.support ∧ r ≠ x := by
  classical
  rcases exists_left_prefix_right_suffix_tail_of_not_mem_alt
      (G := G) left right hleftPath hrightPath hx_left hx_right
      hy_suffix hy_not_alt with
    ⟨r, hr_left_prefix, hr_right_tail⟩
  have hr_left : r ∈ left.support :=
    Walk.support_takeUntil_subset left hx_left hr_left_prefix
  have hr_right_suffix : r ∈ (right.dropUntil x hx_right).support :=
    List.mem_of_mem_tail hr_right_tail
  have hr_right : r ∈ right.support :=
    Walk.support_dropUntil_subset right hx_right hr_right_suffix
  have hright_suffix_path : (right.dropUntil x hx_right).IsPath :=
    Walk.isPath_of_isSubwalk (Walk.isSubwalk_dropUntil right hx_right) hrightPath
  have hx_not_tail : x ∉ (right.dropUntil x hx_right).support.tail := by
    generalize hqeq : right.dropUntil x hx_right = q
    have hqPath : q.IsPath := by
      simpa [hqeq] using hright_suffix_path
    change x ∉ q.support.tail
    cases q with
    | nil =>
        simp
    | cons h q' =>
        have hnodup : x ∉ q'.support ∧ q'.support.Nodup := by
          simpa using hqPath.support_nodup
        simpa using hnodup.1
  have hr_ne_x : r ≠ x := by
    intro hrx
    exact hx_not_tail (by simpa [hrx] using hr_right_tail)
  exact ⟨r, hr_left, hr_right, hr_ne_x⟩

private lemma terminalPathPairSupportLength_lt_of_same_left_right_lt
    {α : Type*}
    {G : SimpleGraph α} {v s t : α}
    {pair : G.Path v s × G.Path v t}
    {right' : G.Path v t}
    (hright :
      (right' : G.Walk v t).support.length <
        (pair.2 : G.Walk v t).support.length) :
    terminalPathPairSupportLength (pair.1, right') <
      terminalPathPairSupportLength pair := by
  dsimp [terminalPathPairSupportLength]
  omega

private lemma terminalPathPairSupportLength_le
    {α : Type*} [Fintype α]
    {G : SimpleGraph α} {v s t : α}
    (pair : G.Path v s × G.Path v t) :
    terminalPathPairSupportLength pair ≤ 2 * Fintype.card α := by
  have hleft :
      (pair.1 : G.Walk v s).support.length ≤ Fintype.card α :=
    pair.1.property.support_nodup.length_le_card
  have hright :
      (pair.2 : G.Walk v t).support.length ≤ Fintype.card α :=
    pair.2.property.support_nodup.length_le_card
  dsimp [terminalPathPairSupportLength]
  omega

private def terminalPathPairWeightedMeasure
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t : α}
    (pair : G.Path v s × G.Path v t) : ℕ :=
  terminalPathPairCommonCard pair * (2 * Fintype.card α + 3) +
    terminalPathPairSupportLength pair

private lemma terminalPathPairWeightedMeasure_lt_of_commonCard_lt
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t : α}
    {pair pair' : G.Path v s × G.Path v t}
    (hcommon :
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair) :
    terminalPathPairWeightedMeasure pair' <
      terminalPathPairWeightedMeasure pair := by
  let B : ℕ := 2 * Fintype.card α + 3
  have hlen' :
      terminalPathPairSupportLength pair' < B := by
    have hle := terminalPathPairSupportLength_le pair'
    dsimp [B]
    omega
  have hsucc :
      terminalPathPairCommonCard pair' + 1 ≤
        terminalPathPairCommonCard pair :=
    Nat.succ_le_of_lt hcommon
  have hstep :
      terminalPathPairCommonCard pair' * B +
          terminalPathPairSupportLength pair' <
        (terminalPathPairCommonCard pair' + 1) * B := by
    have hadd :
        terminalPathPairCommonCard pair' * B +
            terminalPathPairSupportLength pair' <
          terminalPathPairCommonCard pair' * B + B :=
      Nat.add_lt_add_left hlen' _
    simpa [Nat.add_mul] using hadd
  have hmul :
      (terminalPathPairCommonCard pair' + 1) * B ≤
        terminalPathPairCommonCard pair * B :=
    Nat.mul_le_mul_right B hsucc
  have htarget :
      terminalPathPairCommonCard pair * B ≤
        terminalPathPairCommonCard pair * B +
          terminalPathPairSupportLength pair :=
    Nat.le_add_right _ _
  dsimp [terminalPathPairWeightedMeasure, B] at hstep hmul htarget ⊢
  exact lt_of_lt_of_le hstep (le_trans hmul htarget)

private lemma terminalPathPairWeightedMeasure_lt_of_commonCard_le_supportLength_lt
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t : α}
    {pair pair' : G.Path v s × G.Path v t}
    (hcommon :
      terminalPathPairCommonCard pair' ≤ terminalPathPairCommonCard pair)
    (hsupport :
      terminalPathPairSupportLength pair' <
        terminalPathPairSupportLength pair) :
    terminalPathPairWeightedMeasure pair' <
      terminalPathPairWeightedMeasure pair := by
  rcases lt_or_eq_of_le hcommon with hcommon_lt | hcommon_eq
  · exact terminalPathPairWeightedMeasure_lt_of_commonCard_lt
      (pair := pair) (pair' := pair') hcommon_lt
  · dsimp [terminalPathPairWeightedMeasure]
    rw [hcommon_eq]
    exact Nat.add_lt_add_left hsupport _

private lemma false_of_weighted_min_and_commonCard_le_supportLength_lt
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t : α}
    {pair pair' : G.Path v s × G.Path v t}
    (hpair_measure_min : ∀ pair'' : G.Path v s × G.Path v t,
      terminalPathPairWeightedMeasure pair ≤
        terminalPathPairWeightedMeasure pair'')
    (hcommon :
      terminalPathPairCommonCard pair' ≤ terminalPathPairCommonCard pair)
    (hsupport :
      terminalPathPairSupportLength pair' <
        terminalPathPairSupportLength pair) :
    False := by
  have hlt :
      terminalPathPairWeightedMeasure pair' <
        terminalPathPairWeightedMeasure pair :=
    terminalPathPairWeightedMeasure_lt_of_commonCard_le_supportLength_lt
      (pair := pair) (pair' := pair') hcommon hsupport
  have hle :
      terminalPathPairWeightedMeasure pair ≤
        terminalPathPairWeightedMeasure pair' :=
    hpair_measure_min pair'
  omega

private lemma false_of_weighted_min_and_commonCard_lt
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t : α}
    {pair pair' : G.Path v s × G.Path v t}
    (hpair_measure_min : ∀ pair'' : G.Path v s × G.Path v t,
      terminalPathPairWeightedMeasure pair ≤
        terminalPathPairWeightedMeasure pair'')
    (hcommon :
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair) :
    False := by
  have hlt :
      terminalPathPairWeightedMeasure pair' <
        terminalPathPairWeightedMeasure pair :=
    terminalPathPairWeightedMeasure_lt_of_commonCard_lt
      (pair := pair) (pair' := pair') hcommon
  have hle :
      terminalPathPairWeightedMeasure pair ≤
        terminalPathPairWeightedMeasure pair' :=
    hpair_measure_min pair'
  omega

private lemma not_terminalPathPairCommonCard_lt_of_weighted_min
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t : α}
    {pair : G.Path v s × G.Path v t}
    (hpair_measure_min : ∀ pair' : G.Path v s × G.Path v t,
      terminalPathPairWeightedMeasure pair ≤
        terminalPathPairWeightedMeasure pair') :
    ∀ pair' : G.Path v s × G.Path v t,
      ¬ terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  intro pair' hlt
  have hmeasure_lt :
      terminalPathPairWeightedMeasure pair' <
        terminalPathPairWeightedMeasure pair :=
    terminalPathPairWeightedMeasure_lt_of_commonCard_lt
      (pair := pair) (pair' := pair') hlt
  have hmeasure_le :
      terminalPathPairWeightedMeasure pair ≤
      terminalPathPairWeightedMeasure pair' :=
    hpair_measure_min pair'
  omega

private lemma mem_erase_common_without_x_or_not_common_triple
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x y : α}
    {pair : G.Path v s × G.Path v t}
    (hyv : y ≠ v)
    (hy_right : y ∈ (pair.2 : G.Walk v t).support) :
    y ∈ (((pair.1 : G.Walk v s).support.toFinset ∩
            (pair.2 : G.Walk v t).support.toFinset).erase v).erase x ∨
      ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
          y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x) := by
  classical
  by_cases hyx : y = x
  · right
    intro hcommon
    exact hcommon.2.2 hyx
  · by_cases hy_left : y ∈ (pair.1 : G.Walk v s).support
    · left
      rw [Finset.mem_erase, Finset.mem_erase, Finset.mem_inter]
      exact ⟨hyx, hyv, by simpa using hy_left, by simpa using hy_right⟩
    · right
      intro hcommon
      exact hy_left hcommon.1

private lemma mem_erase_common_without_x_or_not_common_triple_left
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x y : α}
    {pair : G.Path v s × G.Path v t}
    (hyv : y ≠ v)
    (hy_left : y ∈ (pair.1 : G.Walk v s).support) :
    y ∈ (((pair.1 : G.Walk v s).support.toFinset ∩
            (pair.2 : G.Walk v t).support.toFinset).erase v).erase x ∨
      ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
          y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x) := by
  classical
  by_cases hyx : y = x
  · right
    intro hcommon
    exact hcommon.2.2 hyx
  · by_cases hy_right : y ∈ (pair.2 : G.Walk v t).support
    · left
      rw [Finset.mem_erase, Finset.mem_erase, Finset.mem_inter]
      exact ⟨hyx, hyv, by simpa using hy_left, by simpa using hy_right⟩
    · right
      intro hcommon
      exact hy_right hcommon.2.1

private lemma exists_new_left_replacement_intersection_of_not_commonCard_lt
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s} (hrsPath : rs.IsPath)
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rs : x ∉ rs.support)
    (hnot :
      ¬ terminalPathPairCommonCard
          ((⟨rs, hrsPath⟩ : G.Path v s), pair.2) <
        terminalPathPairCommonCard pair) :
    ∃ y : α,
      y ≠ v ∧
      y ∈ rs.support ∧
      y ∈ (pair.2 : G.Walk v t).support ∧
      y ∉ (pair.1 : G.Walk v s).support := by
  classical
  let A : Finset α :=
    (((pair.1 : G.Walk v s).support.toFinset ∩
      (pair.2 : G.Walk v t).support.toFinset).erase v)
  let B : Finset α :=
    ((rs.support.toFinset ∩
      (pair.2 : G.Walk v t).support.toFinset).erase v)
  have hxA : x ∈ A := by
    simp [A, hxv, hx_left, hx_right]
  have hnotBA : ¬ B.card < A.card := by
    simpa [A, B, terminalPathPairCommonCard] using hnot
  rcases exists_mem_not_mem_erase_of_not_card_lt (A := A) (B := B) (x := x)
      hxA hnotBA with
    ⟨y, hyB, hy_not_old_erase⟩
  have hyv : y ≠ v := by
    simpa [B] using (Finset.mem_erase.mp hyB).1
  have hyr : y ∈ rs.support := by
    have hyinter :
        y ∈ rs.support.toFinset ∩
          (pair.2 : G.Walk v t).support.toFinset :=
      (Finset.mem_erase.mp hyB).2
    simpa using (Finset.mem_inter.mp hyinter).1
  have hyright : y ∈ (pair.2 : G.Walk v t).support := by
    have hyinter :
        y ∈ rs.support.toFinset ∩
          (pair.2 : G.Walk v t).support.toFinset :=
      (Finset.mem_erase.mp hyB).2
    simpa using (Finset.mem_inter.mp hyinter).2
  have hyx : y ≠ x := by
    intro hyx_eq
    exact hx_rs (by simpa [hyx_eq] using hyr)
  have hy_not_left : y ∉ (pair.1 : G.Walk v s).support := by
    intro hyleft
    have hyA : y ∈ A := by
      simp [A, hyv, hyleft, hyright]
    exact hy_not_old_erase (by simp [hyA, hyx])
  exact ⟨y, hyv, hyr, hyright, hy_not_left⟩

private lemma exists_new_right_replacement_intersection_of_not_commonCard_lt
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x : α}
    {pair : G.Path v s × G.Path v t}
    {rt : G.Walk v t} (hrtPath : rt.IsPath)
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rt : x ∉ rt.support)
    (hnot :
      ¬ terminalPathPairCommonCard
          (pair.1, (⟨rt, hrtPath⟩ : G.Path v t)) <
        terminalPathPairCommonCard pair) :
    ∃ y : α,
      y ≠ v ∧
      y ∈ (pair.1 : G.Walk v s).support ∧
      y ∈ rt.support ∧
      y ∉ (pair.2 : G.Walk v t).support := by
  classical
  let A : Finset α :=
    (((pair.1 : G.Walk v s).support.toFinset ∩
      (pair.2 : G.Walk v t).support.toFinset).erase v)
  let B : Finset α :=
    (((pair.1 : G.Walk v s).support.toFinset ∩
      rt.support.toFinset).erase v)
  have hxA : x ∈ A := by
    simp [A, hxv, hx_left, hx_right]
  have hnotBA : ¬ B.card < A.card := by
    simpa [A, B, terminalPathPairCommonCard] using hnot
  rcases exists_mem_not_mem_erase_of_not_card_lt (A := A) (B := B) (x := x)
      hxA hnotBA with
    ⟨y, hyB, hy_not_old_erase⟩
  have hyv : y ≠ v := by
    simpa [B] using (Finset.mem_erase.mp hyB).1
  have hyleft : y ∈ (pair.1 : G.Walk v s).support := by
    have hyinter :
        y ∈ (pair.1 : G.Walk v s).support.toFinset ∩
          rt.support.toFinset :=
      (Finset.mem_erase.mp hyB).2
    simpa using (Finset.mem_inter.mp hyinter).1
  have hyr : y ∈ rt.support := by
    have hyinter :
        y ∈ (pair.1 : G.Walk v s).support.toFinset ∩
          rt.support.toFinset :=
      (Finset.mem_erase.mp hyB).2
    simpa using (Finset.mem_inter.mp hyinter).2
  have hyx : y ≠ x := by
    intro hyx_eq
    exact hx_rt (by simpa [hyx_eq] using hyr)
  have hy_not_right : y ∉ (pair.2 : G.Walk v t).support := by
    intro hyright
    have hyA : y ∈ A := by
      simp [A, hyv, hyleft, hyright]
    exact hy_not_old_erase (by simp [hyA, hyx])
  exact ⟨y, hyv, hyleft, hyr, hy_not_right⟩

private lemma mem_support_toPath_append_takeUntil_dropUntil_subset
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t y z : α}
    (p : G.Walk v s) (q : G.Walk v t)
    (hyp : y ∈ p.support) (hyq : y ∈ q.support)
    (hz : z ∈
      (((p.takeUntil y hyp).append (q.dropUntil y hyq)).toPath :
        G.Walk v t).support) :
    z ∈ p.support ∨ z ∈ q.support := by
  have hz' :
      z ∈ ((p.takeUntil y hyp).append (q.dropUntil y hyq)).support :=
    Walk.support_toPath_subset _ hz
  rw [Walk.mem_support_append_iff] at hz'
  rcases hz' with hz_left | hz_right
  · exact Or.inl (Walk.support_takeUntil_subset p hyp hz_left)
  · exact Or.inr (Walk.support_dropUntil_subset q hyq hz_right)

private lemma mem_support_toPath_append_takeUntil_dropUntil_cases
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t y z : α}
    (p : G.Walk v s) (q : G.Walk v t)
    (hyp : y ∈ p.support) (hyq : y ∈ q.support)
    (hz : z ∈
      (((p.takeUntil y hyp).append (q.dropUntil y hyq)).toPath :
        G.Walk v t).support) :
    z ∈ (p.takeUntil y hyp).support ∨
      z ∈ (q.dropUntil y hyq).support := by
  have hz' :
      z ∈ ((p.takeUntil y hyp).append (q.dropUntil y hyq)).support :=
    Walk.support_toPath_subset _ hz
  simpa [Walk.mem_support_append_iff] using hz'

private lemma mem_support_toPath_append_three_subset
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {u v w t z : α}
    (p : G.Walk u v) (q : G.Walk v w) (r : G.Walk w t)
    (hz :
      z ∈ (((p.append q).append r).toPath : G.Walk u t).support) :
    z ∈ p.support ∨ z ∈ q.support ∨ z ∈ r.support := by
  have hz_raw :
      z ∈ ((p.append q).append r).support :=
    Walk.support_toPath_subset _ hz
  rw [Walk.mem_support_append_iff] at hz_raw
  rcases hz_raw with hz_pq | hz_r
  · rw [Walk.mem_support_append_iff] at hz_pq
    rcases hz_pq with hz_p | hz_q
    · exact Or.inl hz_p
    · exact Or.inr (Or.inl hz_q)
  · exact Or.inr (Or.inr hz_r)

private lemma mem_support_toPath_right_bypass_subset
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t a z y : α}
    (right : G.Walk v t) (rs : G.Walk v s)
    (ha_right : a ∈ right.support) (ha_rs : a ∈ rs.support)
    (hz_right : z ∈ right.support)
    (hz_tail : z ∈ (rs.dropUntil a ha_rs).support)
    (hy :
      y ∈ ((((right.takeUntil a ha_right).append
        ((rs.dropUntil a ha_rs).takeUntil z hz_tail)).append
        (right.dropUntil z hz_right)).toPath : G.Walk v t).support) :
    y ∈ right.support ∨ y ∈ rs.support := by
  rcases mem_support_toPath_append_three_subset
      (G := G)
      (p := right.takeUntil a ha_right)
      (q := (rs.dropUntil a ha_rs).takeUntil z hz_tail)
      (r := right.dropUntil z hz_right)
      hy with hy_prefix | hy_mid | hy_suffix
  · exact Or.inl (Walk.support_takeUntil_subset right ha_right hy_prefix)
  · exact Or.inr
      (Walk.support_dropUntil_subset rs ha_rs
        (Walk.support_takeUntil_subset (rs.dropUntil a ha_rs) hz_tail
          hy_mid))
  · exact Or.inl (Walk.support_dropUntil_subset right hz_right hy_suffix)

private lemma exists_first_nonapex_intersection_on_walk
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t y : α}
    (p : G.Walk v s) (q : G.Walk v t)
    (hyp : y ∈ p.support) (hyq : y ∈ q.support) (hyv : y ≠ v) :
    ∃ w : α, ∃ hw : w ∈ p.support,
      w ≠ v ∧
      w ∈ q.support ∧
      ∀ z : α, z ≠ v → z ∈ q.support →
        z ∈ (p.takeUntil w hw).support → z = w := by
  classical
  let S : Finset α := q.support.toFinset.erase v
  have hnonempty : {w ∈ S | w ∈ p.support}.Nonempty := by
    refine ⟨y, ?_⟩
    simp [S, hyv, hyq, hyp]
  rcases p.exists_mem_support_forall_mem_support_imp_eq S hnonempty with
    ⟨w, hwS, hwp, hfirst⟩
  have hwv : w ≠ v := by
    simpa [S] using (Finset.mem_erase.mp hwS).1
  have hwq : w ∈ q.support := by
    simpa [S] using (Finset.mem_erase.mp hwS).2
  refine ⟨w, hwp, hwv, hwq, ?_⟩
  intro z hzv hzq hzprefix
  exact hfirst z (by simp [S, hzv, hzq]) hzprefix

private lemma exists_first_nonapex_intersection_on_walk_pair_support
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t u y : α}
    (left : G.Walk v s) (right : G.Walk v t) (r : G.Walk v u)
    (hyr : y ∈ r.support) (hy_right : y ∈ right.support) (hyv : y ≠ v) :
    ∃ w : α, ∃ hw : w ∈ r.support,
      w ≠ v ∧
      (w ∈ left.support ∨ w ∈ right.support) ∧
      ∀ z : α, z ≠ v →
        (z ∈ left.support ∨ z ∈ right.support) →
        z ∈ (r.takeUntil w hw).support → z = w := by
  classical
  let S : Finset α :=
    (left.support.toFinset ∪ right.support.toFinset).erase v
  have hnonempty : {w ∈ S | w ∈ r.support}.Nonempty := by
    refine ⟨y, ?_⟩
    simp [S, hyv, hy_right, hyr]
  rcases r.exists_mem_support_forall_mem_support_imp_eq S hnonempty with
    ⟨w, hwS, hwr, hfirst⟩
  have hwv : w ≠ v := by
    simpa [S] using (Finset.mem_erase.mp hwS).1
  have hwunion : w ∈ left.support ∨ w ∈ right.support := by
    have hwmem :
        w ∈ left.support.toFinset ∪ right.support.toFinset :=
      (Finset.mem_erase.mp hwS).2
    simpa using hwmem
  refine ⟨w, hwr, hwv, hwunion, ?_⟩
  intro z hzv hzunion hzprefix
  exact hfirst z (by simp [S, hzv, hzunion]) hzprefix

private lemma not_mem_takeUntil_first_pair_support_of_ne
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t u x w : α}
    {left : G.Walk v s} {right : G.Walk v t} {r : G.Walk v u}
    {hw : w ∈ r.support}
    (hfirst : ∀ z : α, z ≠ v →
      (z ∈ left.support ∨ z ∈ right.support) →
      z ∈ (r.takeUntil w hw).support → z = w)
    (hxv : x ≠ v)
    (hxunion : x ∈ left.support ∨ x ∈ right.support)
    (hxw : x ≠ w) :
    x ∉ (r.takeUntil w hw).support := by
  intro hxprefix
  exact hxw (hfirst x hxv hxunion hxprefix)

private lemma not_mem_takeUntil_later_of_mem_takeUntil
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s x z : α}
    (p : G.Walk v s) (hx : x ∈ p.support)
    (hz_prefix : z ∈ (p.takeUntil x hx).support)
    (hzx : z ≠ x) :
    x ∉ (p.takeUntil z (p.support_takeUntil_subset hx hz_prefix)).support := by
  exact Walk.notMem_support_takeUntil_support_takeUntil_subset
    (p := p) (w := x) (x := z) hzx hx hz_prefix

private lemma mem_takeUntil_of_mem_takeUntil_of_mem_takeUntil
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s x y z : α}
    (p : G.Walk v s) (hx : x ∈ p.support) (hy : y ∈ p.support)
    (hy_prefix_x : y ∈ (p.takeUntil x hx).support)
    (hz_prefix_y : z ∈ (p.takeUntil y hy).support) :
    z ∈ (p.takeUntil x hx).support := by
  have hz_nested :
      z ∈ ((p.takeUntil x hx).takeUntil y hy_prefix_x).support := by
    simpa [Walk.takeUntil_takeUntil] using hz_prefix_y
  exact Walk.support_takeUntil_subset (p.takeUntil x hx) hy_prefix_x hz_nested

private lemma not_mem_takeUntil_later_of_mem_takeUntil_of_support
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s x z : α}
    (p : G.Walk v s) (hx : x ∈ p.support) (hz : z ∈ p.support)
    (hz_prefix : z ∈ (p.takeUntil x hx).support)
    (hzx : z ≠ x) :
    x ∉ (p.takeUntil z hz).support := by
  simpa using
    (not_mem_takeUntil_later_of_mem_takeUntil
      (G := G) (p := p) hx hz_prefix hzx)

private lemma exists_index_of_mem_dropUntil
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v t w y : α}
    (p : G.Walk v t) (hw : w ∈ p.support)
    (hy : y ∈ (p.dropUntil w hw).support) :
    ∃ i : ℕ,
      (p.takeUntil w hw).length ≤ i ∧
      i ≤ p.length ∧
      p.getVert i = y := by
  rw [Walk.mem_support_iff_exists_getVert] at hy
  rcases hy with ⟨j, hjy, hjle⟩
  refine ⟨(p.takeUntil w hw).length + j, by omega, ?_, ?_⟩
  · have hlen := congrArg Walk.length (p.take_spec hw)
    rw [Walk.length_append] at hlen
    omega
  · have hget := congrArg (fun q : G.Walk v t =>
        q.getVert ((p.takeUntil w hw).length + j)) (p.take_spec hw)
    change (((p.takeUntil w hw).append (p.dropUntil w hw)).getVert
        ((p.takeUntil w hw).length + j)) =
      p.getVert ((p.takeUntil w hw).length + j) at hget
    rw [Walk.getVert_append] at hget
    have hnot_lt :
        ¬ (p.takeUntil w hw).length + j < (p.takeUntil w hw).length := by
      omega
    simp [hnot_lt, hjy] at hget
    exact hget.symm

private lemma mem_dropUntil_of_index_ge
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v t w y : α}
    (p : G.Walk v t) (hw : w ∈ p.support)
    {i : ℕ}
    (hw_len_le_i : (p.takeUntil w hw).length ≤ i)
    (hi_le : i ≤ p.length)
    (hi_get : p.getVert i = y) :
    y ∈ (p.dropUntil w hw).support := by
  rw [Walk.mem_support_iff_exists_getVert]
  refine ⟨i - (p.takeUntil w hw).length, ?_, ?_⟩
  · have hget := congrArg (fun q : G.Walk v t => q.getVert i) (p.take_spec hw)
    change (((p.takeUntil w hw).append (p.dropUntil w hw)).getVert i) =
      p.getVert i at hget
    rw [Walk.getVert_append] at hget
    have hnot_lt : ¬ i < (p.takeUntil w hw).length := by omega
    simpa [hnot_lt, Nat.add_sub_cancel' hw_len_le_i, hi_get] using hget
  · have hlen := congrArg Walk.length (p.take_spec hw)
    rw [Walk.length_append] at hlen
    omega

private lemma mem_dropUntil_of_mem_dropUntil_of_mem_dropUntil
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v t x y z : α}
    {p : G.Walk v t} (hp : p.IsPath)
    (hx : x ∈ p.support) (hy : y ∈ p.support)
    (hy_after_x : y ∈ (p.dropUntil x hx).support)
    (hz_after_y : z ∈ (p.dropUntil y hy).support) :
    z ∈ (p.dropUntil x hx).support := by
  rcases exists_index_of_mem_dropUntil (G := G) p hx hy_after_x with
    ⟨iy, hx_len_le_iy, hiy_le, hiy_get⟩
  rcases exists_index_of_mem_dropUntil (G := G) p hy hz_after_y with
    ⟨iz, hy_len_le_iz, hiz_le, hiz_get⟩
  have hy_len_eq_iy : (p.takeUntil y hy).length = iy := by
    have hy_len_le : (p.takeUntil y hy).length ≤ p.length :=
      p.length_takeUntil_le hy
    exact hp.getVert_injOn
      (by simpa using hy_len_le)
      (by simpa using hiy_le)
      (by simpa [Walk.getVert_length_takeUntil] using hiy_get.symm)
  exact mem_dropUntil_of_index_ge
    (G := G) p hx
    (le_trans hx_len_le_iy (by simpa [hy_len_eq_iy] using hy_len_le_iz))
    hiz_le hiz_get

private lemma mem_dropUntil_of_mem_nested_dropUntil
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v t x y z : α}
    {p : G.Walk v t} (hp : p.IsPath)
    (hx : x ∈ p.support)
    (hy_after_x : y ∈ (p.dropUntil x hx).support)
    (hz_after_y_in_suffix :
      z ∈ ((p.dropUntil x hx).dropUntil y hy_after_x).support) :
    z ∈ (p.dropUntil y
      (Walk.support_dropUntil_subset p hx hy_after_x)).support := by
  let q : G.Walk x t := p.dropUntil x hx
  let hy : y ∈ p.support := Walk.support_dropUntil_subset p hx hy_after_x
  let tx : ℕ := (p.takeUntil x hx).length
  rcases exists_index_of_mem_dropUntil (G := G) q hy_after_x
      hz_after_y_in_suffix with
    ⟨j, hq_take_y_le_j, hj_le_q, hqj_get⟩
  have hlen_split : p.length = tx + q.length := by
    have hlen := congrArg Walk.length (p.take_spec hx)
    rw [Walk.length_append] at hlen
    simpa [q, tx] using hlen.symm
  have hget_z_p : p.getVert (tx + j) = z := by
    have hget := congrArg (fun r : G.Walk v t => r.getVert (tx + j))
      (p.take_spec hx)
    change (((p.takeUntil x hx).append (p.dropUntil x hx)).getVert (tx + j)) =
      p.getVert (tx + j) at hget
    rw [Walk.getVert_append] at hget
    have hnot_lt : ¬ tx + j < tx := by omega
    simp [q, tx, hnot_lt, hqj_get] at hget
    exact hget.symm
  have hI_le : tx + j ≤ p.length := by
    omega
  have hq_take_len_le : (q.takeUntil y hy_after_x).length ≤ q.length :=
    q.length_takeUntil_le hy_after_x
  have hget_y_p :
      p.getVert (tx + (q.takeUntil y hy_after_x).length) = y := by
    have hget := congrArg
      (fun r : G.Walk v t =>
        r.getVert (tx + (q.takeUntil y hy_after_x).length))
      (p.take_spec hx)
    change (((p.takeUntil x hx).append (p.dropUntil x hx)).getVert
        (tx + (q.takeUntil y hy_after_x).length)) =
      p.getVert (tx + (q.takeUntil y hy_after_x).length) at hget
    rw [Walk.getVert_append] at hget
    have hnot_lt :
        ¬ tx + (q.takeUntil y hy_after_x).length < tx := by omega
    simp [q, tx, hnot_lt, Walk.getVert_length_takeUntil] at hget
    exact hget.symm
  have hy_index_le :
      tx + (q.takeUntil y hy_after_x).length ≤ p.length := by
    omega
  have hy_len_eq :
      (p.takeUntil y hy).length =
        tx + (q.takeUntil y hy_after_x).length := by
    have hy_len_le : (p.takeUntil y hy).length ≤ p.length :=
      p.length_takeUntil_le hy
    exact hp.getVert_injOn
      (by simpa using hy_len_le)
      (by simpa using hy_index_le)
      (by simpa [Walk.getVert_length_takeUntil] using hget_y_p.symm)
  exact mem_dropUntil_of_index_ge
    (G := G) p hy
    (by
      rw [hy_len_eq]
      exact Nat.add_le_add_left hq_take_y_le_j tx)
    hI_le hget_z_p

private lemma mem_dropUntil_of_mem_support_not_takeUntil
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v t w y : α}
    (p : G.Walk v t) (hw : w ∈ p.support)
    (hy : y ∈ p.support)
    (hnot : y ∉ (p.takeUntil w hw).support) :
    y ∈ (p.dropUntil w hw).support := by
  have hy_append :
      y ∈ ((p.takeUntil w hw).append (p.dropUntil w hw)).support := by
    simpa [p.take_spec hw] using hy
  rw [Walk.mem_support_append_iff] at hy_append
  rcases hy_append with hy_take | hy_drop
  · exact False.elim (hnot hy_take)
  · exact hy_drop

private lemma mem_takeUntil_of_mem_support_not_dropUntil
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v t w y : α}
    (p : G.Walk v t) (hw : w ∈ p.support)
    (hy : y ∈ p.support)
    (hnot : y ∉ (p.dropUntil w hw).support) :
    y ∈ (p.takeUntil w hw).support := by
  have hy_append :
      y ∈ ((p.takeUntil w hw).append (p.dropUntil w hw)).support := by
    simpa [p.take_spec hw] using hy
  rw [Walk.mem_support_append_iff] at hy_append
  rcases hy_append with hy_take | hy_drop
  · exact hy_take
  · exact False.elim (hnot hy_drop)

private lemma mem_takeUntil_or_mem_dropUntil_of_mem_support
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v t w y : α}
    (p : G.Walk v t) (hw : w ∈ p.support)
    (hy : y ∈ p.support) :
    y ∈ (p.takeUntil w hw).support ∨
      y ∈ (p.dropUntil w hw).support := by
  have hy_append :
      y ∈ ((p.takeUntil w hw).append (p.dropUntil w hw)).support := by
    simpa [p.take_spec hw] using hy
  rw [Walk.mem_support_append_iff] at hy_append
  exact hy_append

private lemma exists_first_mem_support_forall_mem_takeUntil_imp_eq
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v t : α}
    (p : G.Walk v t)
    (S : Finset α)
    (hnonempty : {y ∈ S | y ∈ p.support}.Nonempty) :
    ∃ z : α, z ∈ S ∧ ∃ hzsup : z ∈ p.support,
      ∀ y : α, y ∈ S → y ∈ (p.takeUntil z hzsup).support → y = z := by
  classical
  rcases p.exists_mem_support_forall_mem_support_imp_eq S hnonempty with
    ⟨z, hzS, hzsup, hfirst⟩
  exact ⟨z, hzS, hzsup, hfirst⟩

private lemma not_both_mem_dropUntil_on_simple_path
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v t x w : α}
    {p : G.Walk v t} (hp : p.IsPath)
    (hx : x ∈ p.support) (hw : w ∈ p.support)
    (hx_after_w : x ∈ (p.dropUntil w hw).support)
    (hw_after_x : w ∈ (p.dropUntil x hx).support)
    (hxw : x ≠ w) :
    False := by
  rcases exists_index_of_mem_dropUntil (G := G) p hw hx_after_w with
    ⟨ix, htw_le_ix, hix_le, hix_get⟩
  rcases exists_index_of_mem_dropUntil (G := G) p hx hw_after_x with
    ⟨iw, htx_le_iw, hiw_le, hiw_get⟩
  have hix_eq_tx : ix = (p.takeUntil x hx).length := by
    have htx_le : (p.takeUntil x hx).length ≤ p.length :=
      p.length_takeUntil_le hx
    exact hp.getVert_injOn
      (by simpa using hix_le)
      (by simpa using htx_le)
      (by simpa [Walk.getVert_length_takeUntil] using hix_get)
  have hiw_eq_tw : iw = (p.takeUntil w hw).length := by
    have htw_le : (p.takeUntil w hw).length ≤ p.length :=
      p.length_takeUntil_le hw
    exact hp.getVert_injOn
      (by simpa using hiw_le)
      (by simpa using htw_le)
      (by simpa [Walk.getVert_length_takeUntil] using hiw_get)
  have htx_le_tw : (p.takeUntil x hx).length ≤ (p.takeUntil w hw).length := by
    simpa [hiw_eq_tw] using htx_le_iw
  have htw_le_tx : (p.takeUntil w hw).length ≤ (p.takeUntil x hx).length := by
    simpa [hix_eq_tx] using htw_le_ix
  have hlen_eq : (p.takeUntil x hx).length = (p.takeUntil w hw).length :=
    le_antisymm htx_le_tw htw_le_tx
  have hx_eq_w : x = w := by
    calc
      x = p.getVert ix := hix_get.symm
      _ = p.getVert iw := by simp [hix_eq_tx, hiw_eq_tw, hlen_eq]
      _ = w := hiw_get
  exact hxw hx_eq_w

private lemma mem_dropUntil_of_not_mem_dropUntil
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v t x y : α}
    (p : G.Walk v t)
    (hx : x ∈ p.support) (hy : y ∈ p.support)
    (hxy : x ≠ y)
    (hy_not_after_x : y ∉ (p.dropUntil x hx).support) :
    x ∈ (p.dropUntil y hy).support := by
  have hx_not_prefix_y : x ∉ (p.takeUntil y hy).support := by
    intro hx_prefix_y
    have hy_not_prefix_x : y ∉ (p.takeUntil x hx).support := by
      simpa using
        (Walk.notMem_support_takeUntil_support_takeUntil_subset
          (p := p) (w := y) (x := x) hxy hy hx_prefix_y)
    exact hy_not_after_x
      (mem_dropUntil_of_mem_support_not_takeUntil
        (G := G) p hx hy hy_not_prefix_x)
  exact mem_dropUntil_of_mem_support_not_takeUntil
    (G := G) p hy hx hx_not_prefix_y

private lemma dropUntil_start_eq_self
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {u v : α}
    (p : G.Walk u v) (h : u ∈ p.support) :
    p.dropUntil u h = p := by
  cases p with
  | nil =>
      simp [Walk.dropUntil]
  | cons h p =>
      simp [Walk.dropUntil]

private lemma mem_dropUntil_of_mem_bypass_dropUntil
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {u v y z : α}
    (p : G.Walk u v)
    (hyb : y ∈ p.bypass.support)
    (hzb : z ∈ (p.bypass.dropUntil y hyb).support) :
    z ∈ (p.dropUntil y (Walk.support_bypass_subset p hyb)).support := by
  induction p with
  | nil =>
      simpa using hzb
  | @cons u₀ v₀ w₀ h p ih =>
      simp only [Walk.bypass] at hyb hzb ⊢
      split_ifs at hyb hzb ⊢ with hs
      · by_cases hyu : y = u₀
        · subst y
          have hz_bypass_tail :
              z ∈ (p.bypass.dropUntil u₀ hs).support :=
            Walk.support_dropUntil_subset (p.bypass.dropUntil u₀ hs) hyb hzb
          have hz_p_bypass : z ∈ p.bypass.support :=
            Walk.support_dropUntil_subset p.bypass hs hz_bypass_tail
          have hz_p : z ∈ p.support :=
            Walk.support_bypass_subset p hz_p_bypass
          simpa [Walk.dropUntil, Walk.support_cons] using
            (Walk.support_subset_support_cons p h hz_p)
        · have hyb_tail : y ∈ p.bypass.support :=
            Walk.support_dropUntil_subset p.bypass hs hyb
          have hzb_tail :
              z ∈ (p.bypass.dropUntil y hyb_tail).support :=
            mem_dropUntil_of_mem_nested_dropUntil
              (G := G) (p := p.bypass) (hp := Walk.bypass_isPath p)
              (x := u₀) (y := y) (z := z) hs hyb hzb
          have hz_drop : z ∈ (p.dropUntil y
              (Walk.support_bypass_subset p hyb_tail)).support :=
            ih hyb_tail hzb_tail
          have huy : u₀ ≠ y := fun h => hyu h.symm
          simpa [Walk.dropUntil, huy] using hz_drop
      · by_cases hyu : y = u₀
        · subst y
          have hz_cons_bypass : z ∈ (Walk.cons h p.bypass).support := by
            simpa [Walk.dropUntil] using hzb
          have hz_cons : z ∈ (Walk.cons h p).support := by
            rw [Walk.support_cons, List.mem_cons] at hz_cons_bypass
            rcases hz_cons_bypass with hz_head | hz_tail
            · exact hz_head ▸ (Walk.cons h p).start_mem_support
            · exact Walk.support_subset_support_cons p h
                (Walk.support_bypass_subset p hz_tail)
          simpa [Walk.dropUntil] using hz_cons
        · have hyb_tail : y ∈ p.bypass.support := by
            simpa [Walk.support_cons, hyu] using hyb
          have hzb_tail :
              z ∈ (p.bypass.dropUntil y hyb_tail).support := by
            have huy : u₀ ≠ y := fun h => hyu h.symm
            simpa [Walk.dropUntil, huy] using hzb
          have hz_drop : z ∈ (p.dropUntil y
              (Walk.support_bypass_subset p hyb_tail)).support :=
            ih hyb_tail hzb_tail
          have huy : u₀ ≠ y := fun h => hyu h.symm
          simpa [Walk.dropUntil, huy] using hz_drop

private lemma mem_dropUntil_append_right_of_not_left
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {u v w y z : α}
    (p : G.Walk u v) (q : G.Walk v w)
    (hyq : y ∈ q.support)
    (hy_not_p : y ∉ p.support)
    (hz :
      z ∈ ((p.append q).dropUntil y
        (Walk.subset_support_append_right p q hyq)).support)
    (hz_not_p : z ∉ p.support) :
    z ∈ (q.dropUntil y hyq).support := by
  induction p with
  | nil =>
      simpa using hz
  | @cons u₀ v₀ w₀ h p ih =>
      have hyu : y ≠ u₀ := by
        intro hyu
        exact hy_not_p (by simp [Walk.support_cons, hyu])
      have hy_not_tail : y ∉ p.support := by
        intro hy_tail
        exact hy_not_p (by simp [Walk.support_cons, hy_tail])
      have hz_not_tail : z ∉ p.support := by
        intro hz_tail
        exact hz_not_p (by simp [Walk.support_cons, hz_tail])
      have huy : u₀ ≠ y := fun h => hyu h.symm
      exact ih q hyq hy_not_tail
        (by simpa [Walk.dropUntil, huy] using hz) hz_not_tail

private lemma mem_support_bypass_append_right_of_no_later_left_return
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {u v w y : α}
    (p : G.Walk u v) (q : G.Walk v w)
    (hp : p.IsPath) (hq : q.IsPath)
    (hyq : y ∈ q.support)
    (hy_not_p : y ∉ p.support)
    (hno_later :
      ∀ r : α, r ∈ (q.dropUntil y hyq).support → r ∉ p.support) :
    y ∈ (p.append q).bypass.support := by
  induction p with
  | nil =>
      simpa [walk_bypass_eq_self_of_isPath (G := G) (p := q) hq] using hyq
  | @cons u₀ v₀ w₀ h p ih =>
      rw [Walk.cons_isPath_iff] at hp
      have hyu : y ≠ u₀ := by
        intro hyu
        exact hy_not_p (by simp [Walk.support_cons, hyu])
      have hy_not_tail : y ∉ p.support := by
        intro hy_tail
        exact hy_not_p (by simp [Walk.support_cons, hy_tail])
      have hno_later_tail :
          ∀ r : α, r ∈ (q.dropUntil y hyq).support → r ∉ p.support := by
        intro r hr hrp
        exact hno_later r hr (by simp [Walk.support_cons, hrp])
      have hy_tail_bypass :
          y ∈ (p.append q).bypass.support :=
        ih q hp.1 hq hyq hy_not_tail hno_later_tail
      simp only [Walk.append, Walk.bypass]
      split_ifs with hs
      · by_cases hy_after_u :
          y ∈ ((p.append q).bypass.dropUntil u₀ hs).support
        · exact hy_after_u
        · exfalso
          have hu_after_y :
              u₀ ∈ ((p.append q).bypass.dropUntil y hy_tail_bypass).support :=
            mem_dropUntil_of_not_mem_dropUntil
              (G := G) ((p.append q).bypass) hs hy_tail_bypass
              (by exact fun hyeq => hyu hyeq.symm) hy_after_u
          have hu_tail_after_y :
              u₀ ∈ ((p.append q).dropUntil y
                (Walk.support_bypass_subset (p.append q) hy_tail_bypass)).support :=
            mem_dropUntil_of_mem_bypass_dropUntil
              (G := G) (p := p.append q) hy_tail_bypass hu_after_y
          have hu_q_after_y : u₀ ∈ (q.dropUntil y hyq).support :=
            mem_dropUntil_append_right_of_not_left
              (G := G) p q hyq hy_not_tail
              (by simpa using hu_tail_after_y) hp.2
          exact hno_later u₀ hu_q_after_y (by simp [Walk.support_cons])
      · exact List.mem_cons_of_mem u₀ hy_tail_bypass

private lemma support_toPath_append_takeUntil_dropUntil_absent_right_suffix_later_left_return
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x y : α}
    (left : G.Walk v s) (right : G.Walk v t)
    (hleftPath : left.IsPath) (hrightPath : right.IsPath)
    (hx_left : x ∈ left.support)
    (hx_right : x ∈ right.support)
    (hy_suffix : y ∈ (right.dropUntil x hx_right).support)
    (hy_not_left :
      y ∉ (left.takeUntil x hx_left).support)
    (hy_not_alt :
      y ∉ (((left.takeUntil x hx_left).append
        (right.dropUntil x hx_right)).toPath : G.Walk v t).support) :
    ∃ r : α,
      r ∈ ((right.dropUntil x hx_right).dropUntil y hy_suffix).support ∧
      r ≠ y ∧
      r ∈ (left.takeUntil x hx_left).support := by
  classical
  by_contra hnone
  have hleft_prefix_path : (left.takeUntil x hx_left).IsPath :=
    Walk.isPath_of_isSubwalk (Walk.isSubwalk_takeUntil left hx_left) hleftPath
  have hright_suffix_path : (right.dropUntil x hx_right).IsPath :=
    Walk.isPath_of_isSubwalk (Walk.isSubwalk_dropUntil right hx_right) hrightPath
  have hno_later :
      ∀ r : α,
        r ∈ ((right.dropUntil x hx_right).dropUntil y hy_suffix).support →
        r ∉ (left.takeUntil x hx_left).support := by
    intro r hr hrl
    have hry : r = y := by
      by_contra hry
      exact hnone ⟨r, hr, hry, hrl⟩
    exact hy_not_left (by simpa [hry] using hrl)
  have hy_survives :
      y ∈ (((left.takeUntil x hx_left).append
        (right.dropUntil x hx_right)).bypass).support :=
    mem_support_bypass_append_right_of_no_later_left_return
      (G := G) (p := left.takeUntil x hx_left)
      (q := right.dropUntil x hx_right)
      hleft_prefix_path hright_suffix_path hy_suffix hy_not_left hno_later
  exact hy_not_alt (by simpa [Walk.toPath] using hy_survives)

private lemma mem_dropUntil_of_mem_takeUntil_ne
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v t x y : α}
    (p : G.Walk v t)
    (hx : x ∈ p.support) (hy : y ∈ p.support)
    (hx_prefix_y : x ∈ (p.takeUntil y hy).support)
    (hxy : x ≠ y) :
    y ∈ (p.dropUntil x hx).support := by
  have hy_not_prefix_x : y ∉ (p.takeUntil x hx).support := by
    simpa using
      (Walk.notMem_support_takeUntil_support_takeUntil_subset
        (p := p) (w := y) (x := x) hxy hy hx_prefix_y)
  exact mem_dropUntil_of_mem_support_not_takeUntil
    (G := G) p hx hy hy_not_prefix_x

private lemma not_mem_dropUntil_of_mem_takeUntil_ne_on_isPath
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v t x y : α}
    {p : G.Walk v t} (hp : p.IsPath)
    (hx : x ∈ p.support) (hy : y ∈ p.support)
    (hy_prefix_x : y ∈ (p.takeUntil x hx).support)
    (hyx : y ≠ x) :
    y ∉ (p.dropUntil x hx).support := by
  intro hy_after_x
  have hx_after_y : x ∈ (p.dropUntil y hy).support :=
    mem_dropUntil_of_mem_takeUntil_ne
      (G := G) p hy hx hy_prefix_x hyx
  exact not_both_mem_dropUntil_on_simple_path
    (G := G) (p := p) hp hy hx hy_after_x hx_after_y hyx

private lemma not_mem_takeUntil_of_mem_dropUntil_ne_on_isPath
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v t x y : α}
    {p : G.Walk v t} (hp : p.IsPath)
    (hx : x ∈ p.support) (hy : y ∈ p.support)
    (hy_after_x : y ∈ (p.dropUntil x hx).support)
    (hyx : y ≠ x) :
    y ∉ (p.takeUntil x hx).support := by
  intro hy_prefix_x
  exact not_mem_dropUntil_of_mem_takeUntil_ne_on_isPath
    (G := G) (p := p) hp hx hy hy_prefix_x hyx hy_after_x

private lemma mem_takeUntil_of_mem_dropUntil_ne_on_isPath
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v t x y : α}
    {p : G.Walk v t} (hp : p.IsPath)
    (hx : x ∈ p.support) (hy : y ∈ p.support)
    (hy_after_x : y ∈ (p.dropUntil x hx).support)
    (hxy : x ≠ y) :
    x ∈ (p.takeUntil y hy).support := by
  by_contra hx_not_prefix_y
  have hx_after_y :
      x ∈ (p.dropUntil y hy).support :=
    mem_dropUntil_of_mem_support_not_takeUntil
      (G := G) p hy hx hx_not_prefix_y
  exact not_both_mem_dropUntil_on_simple_path
    (G := G) (p := p) hp hx hy hx_after_y hy_after_x hxy

private lemma mem_takeUntil_of_mem_dropUntil_takeUntil_ne_on_isPath
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v t a z b : α}
    {p : G.Walk v t} (hp : p.IsPath)
    (ha : a ∈ p.support) (hz : z ∈ p.support)
    (hz_tail : z ∈ (p.dropUntil a ha).support)
    (hb_mid : b ∈ ((p.dropUntil a ha).takeUntil z hz_tail).support)
    (hbz : b ≠ z) :
    b ∈ (p.takeUntil z hz).support := by
  have hb_tail : b ∈ (p.dropUntil a ha).support :=
    Walk.support_takeUntil_subset (p.dropUntil a ha) hz_tail hb_mid
  have hz_after_b_tail :
      z ∈ ((p.dropUntil a ha).dropUntil b hb_tail).support :=
    mem_dropUntil_of_mem_takeUntil_ne
      (G := G) (p.dropUntil a ha) hb_tail hz_tail hb_mid hbz
  have hb : b ∈ p.support :=
    Walk.support_dropUntil_subset p ha hb_tail
  have hz_after_b : z ∈ (p.dropUntil b hb).support :=
    mem_dropUntil_of_mem_nested_dropUntil
      (G := G) (p := p) hp ha hb_tail hz_after_b_tail
  exact mem_takeUntil_of_mem_dropUntil_ne_on_isPath
    (G := G) (p := p) hp hb hz hz_after_b hbz

private lemma mem_dropUntil_takeUntil_of_mem_dropUntil_of_mem_takeUntil_on_isPath
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v t a z b : α}
    {p : G.Walk v t} (hp : p.IsPath)
    (ha : a ∈ p.support) (hz : z ∈ p.support) (hb : b ∈ p.support)
    (hz_tail : z ∈ (p.dropUntil a ha).support)
    (hb_tail : b ∈ (p.dropUntil a ha).support)
    (hb_prefix_z : b ∈ (p.takeUntil z hz).support)
    (hbz : b ≠ z) :
    b ∈ ((p.dropUntil a ha).takeUntil z hz_tail).support := by
  by_contra hb_not_mid
  have hb_after_z_tail :
      b ∈ ((p.dropUntil a ha).dropUntil z hz_tail).support :=
    mem_dropUntil_of_mem_support_not_takeUntil
      (G := G) (p.dropUntil a ha) hz_tail hb_tail hb_not_mid
  have hb_after_z :
      b ∈ (p.dropUntil z hz).support :=
    mem_dropUntil_of_mem_nested_dropUntil
      (G := G) (p := p) hp ha hz_tail hb_after_z_tail
  exact
    (not_mem_dropUntil_of_mem_takeUntil_ne_on_isPath
      (G := G) (p := p) hp hz hb hb_prefix_z hbz) hb_after_z

private lemma not_mem_right_bypass_of_takeUntil_dropUntil_around
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x a z : α}
    (right : G.Walk v t) (rs : G.Walk v s)
    (hrightPath : right.IsPath)
    (hx_right : x ∈ right.support)
    (ha_right : a ∈ right.support) (ha_rs : a ∈ rs.support)
    (hz_right : z ∈ right.support)
    (hz_tail : z ∈ (rs.dropUntil a ha_rs).support)
    (ha_prefix_x : a ∈ (right.takeUntil x hx_right).support)
    (hz_suffix_x : z ∈ (right.dropUntil x hx_right).support)
    (hax : a ≠ x) (hzx : z ≠ x)
    (hx_rs : x ∉ rs.support) :
    x ∉ ((((right.takeUntil a ha_right).append
      ((rs.dropUntil a ha_rs).takeUntil z hz_tail)).append
      (right.dropUntil z hz_right)).toPath : G.Walk v t).support := by
  intro hx_bypass
  rcases mem_support_toPath_append_three_subset
      (G := G)
      (p := right.takeUntil a ha_right)
      (q := (rs.dropUntil a ha_rs).takeUntil z hz_tail)
      (r := right.dropUntil z hz_right)
      hx_bypass with hx_prefix | hx_mid | hx_suffix
  · exact
      (not_mem_takeUntil_later_of_mem_takeUntil_of_support
        (G := G) right hx_right ha_right ha_prefix_x hax) hx_prefix
  · exact hx_rs
      (Walk.support_dropUntil_subset rs ha_rs
        (Walk.support_takeUntil_subset (rs.dropUntil a ha_rs) hz_tail hx_mid))
  · exact
      (not_both_mem_dropUntil_on_simple_path
        (G := G) (p := right) hrightPath hx_right hz_right
        hx_suffix hz_suffix_x (fun hxz => hzx hxz.symm))

private lemma mem_support_toPath_left_rs_right_bridge_subset
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t y z q : α}
    (left : G.Walk v s) (rs : G.Walk v s) (right : G.Walk v t)
    (hy_left : y ∈ left.support) (hy_rs : y ∈ rs.support)
    (hz_tail : z ∈ (rs.dropUntil y hy_rs).support)
    (hz_right : z ∈ right.support)
    (hq :
      q ∈ ((((left.takeUntil y hy_left).append
        ((rs.dropUntil y hy_rs).takeUntil z hz_tail)).append
        (right.dropUntil z hz_right)).toPath : G.Walk v t).support) :
    q ∈ left.support ∨ q ∈ rs.support ∨ q ∈ right.support := by
  rcases mem_support_toPath_append_three_subset
      (G := G)
      (p := left.takeUntil y hy_left)
      (q := (rs.dropUntil y hy_rs).takeUntil z hz_tail)
      (r := right.dropUntil z hz_right)
      hq with hq_left | hq_mid | hq_right
  · exact Or.inl (Walk.support_takeUntil_subset left hy_left hq_left)
  · exact Or.inr
      (Or.inl
        (Walk.support_dropUntil_subset rs hy_rs
          (Walk.support_takeUntil_subset (rs.dropUntil y hy_rs) hz_tail
            hq_mid)))
  · exact Or.inr
      (Or.inr (Walk.support_dropUntil_subset right hz_right hq_right))

private lemma not_mem_left_rs_right_bridge_of_prefix_suffix
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x y z : α}
    (left : G.Walk v s) (rs : G.Walk v s) (right : G.Walk v t)
    (_hleftPath : left.IsPath) (hrightPath : right.IsPath)
    (hx_left : x ∈ left.support)
    (hy_left : y ∈ left.support) (hy_rs : y ∈ rs.support)
    (hz_tail : z ∈ (rs.dropUntil y hy_rs).support)
    (hx_right : x ∈ right.support) (hz_right : z ∈ right.support)
    (hy_prefix_x : y ∈ (left.takeUntil x hx_left).support)
    (hz_suffix_x : z ∈ (right.dropUntil x hx_right).support)
    (hyx : y ≠ x) (hzx : z ≠ x)
    (hx_rs : x ∉ rs.support) :
    x ∉ ((((left.takeUntil y hy_left).append
      ((rs.dropUntil y hy_rs).takeUntil z hz_tail)).append
      (right.dropUntil z hz_right)).toPath : G.Walk v t).support := by
  intro hx_bridge
  rcases mem_support_toPath_append_three_subset
      (G := G)
      (p := left.takeUntil y hy_left)
      (q := (rs.dropUntil y hy_rs).takeUntil z hz_tail)
      (r := right.dropUntil z hz_right)
      hx_bridge with hx_prefix | hx_mid | hx_suffix
  · exact
      (not_mem_takeUntil_later_of_mem_takeUntil_of_support
        (G := G) left hx_left hy_left hy_prefix_x hyx) hx_prefix
  · exact hx_rs
      (Walk.support_dropUntil_subset rs hy_rs
        (Walk.support_takeUntil_subset (rs.dropUntil y hy_rs) hz_tail hx_mid))
  · exact
      (not_both_mem_dropUntil_on_simple_path
        (G := G) (p := right) hrightPath hx_right hz_right
        hx_suffix hz_suffix_x (fun hxz => hzx hxz.symm))

private lemma not_mem_cross_swap_left_of_left_prefix_not_right
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x y : α}
    (left : G.Walk v s) (right : G.Walk v t)
    (hleftPath : left.IsPath)
    (hx_left : x ∈ left.support)
    (hx_right : x ∈ right.support)
    (hy_left : y ∈ left.support)
    (hy_prefix_x : y ∈ (left.takeUntil x hx_left).support)
    (hy_not_right : y ∉ right.support)
    (hyx : y ≠ x) :
    y ∉
      ((((right.takeUntil x hx_right).append
        (left.dropUntil x hx_left)).toPath) : G.Walk v s).support := by
  intro hy_swap
  have hy_raw :
      y ∈ ((right.takeUntil x hx_right).append
        (left.dropUntil x hx_left)).support :=
    Walk.support_toPath_subset _ hy_swap
  rw [Walk.mem_support_append_iff] at hy_raw
  rcases hy_raw with hy_right_prefix | hy_left_suffix
  · exact hy_not_right
      (Walk.support_takeUntil_subset right hx_right hy_right_prefix)
  · exact
      (not_mem_dropUntil_of_mem_takeUntil_ne_on_isPath
        (G := G) (p := left) hleftPath hx_left hy_left
        hy_prefix_x hyx) hy_left_suffix

private lemma not_mem_dropUntil_of_after_on_isPath
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s w y : α}
    {p : G.Walk v s} (hp : p.IsPath)
    (hw : w ∈ p.support) (hy : y ∈ p.support)
    (hy_not_prefix_w : y ∉ (p.takeUntil w hw).support)
    (hyw : y ≠ w) :
    w ∉ (p.dropUntil y hy).support := by
  intro hw_after_y
  have hy_after_w : y ∈ (p.dropUntil w hw).support :=
    mem_dropUntil_of_mem_support_not_takeUntil
      (G := G) p hw hy hy_not_prefix_w
  exact not_both_mem_dropUntil_on_simple_path
    (G := G) (p := p) hp hy hw hy_after_w hw_after_y hyw

private lemma two_sided_middle_guard_of_first_noncommon_not_swap
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x w y a : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hy_rs : y ∈ rs.support)
    (ha_tail : a ∈ (rs.dropUntil y hy_rs).support)
    (hy_not_swap :
      y ∉
        (((((pair.2 : G.Walk v t).takeUntil x hx_right).append
          ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath) :
            G.Walk v s).support)
    (hw_not_after_y : w ∉ (rs.dropUntil y hy_rs).support)
    (ha_not_swap :
      a ∉
        (((((pair.2 : G.Walk v t).takeUntil x hx_right).append
          ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath) :
            G.Walk v s).support)
    (hfirst_after_y :
      ∀ q : α, q ≠ v → q ≠ y → q ≠ w →
        (q ∈ (pair.1 : G.Walk v s).support ∨
          q ∈ (pair.2 : G.Walk v t).support) →
        ¬ (q ∈ (pair.1 : G.Walk v s).support ∧
           q ∈ (pair.2 : G.Walk v t).support ∧ q ≠ x) →
        q ∈ ((rs.dropUntil y hy_rs).takeUntil a ha_tail).support →
        q = a) :
      ∀ q : α, q ≠ v →
        q ∈
          (((((pair.2 : G.Walk v t).takeUntil x hx_right).append
            ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath) :
              G.Walk v s).support →
        q ∈ ((rs.dropUntil y hy_rs).takeUntil a ha_tail).support →
        q ∈ (pair.1 : G.Walk v s).support ∧
          q ∈ (pair.2 : G.Walk v t).support := by
  intro q hqv hq_swap hq_mid
  by_cases hq_common :
      q ∈ (pair.1 : G.Walk v s).support ∧
        q ∈ (pair.2 : G.Walk v t).support
  · exact hq_common
  have hq_swap_raw :
      q ∈ (((pair.2 : G.Walk v t).takeUntil x hx_right).append
        ((pair.1 : G.Walk v s).dropUntil x hx_left)).support :=
    Walk.support_toPath_subset _ hq_swap
  have hq_old :
      q ∈ (pair.1 : G.Walk v s).support ∨
        q ∈ (pair.2 : G.Walk v t).support := by
    rw [Walk.mem_support_append_iff] at hq_swap_raw
    rcases hq_swap_raw with hq_right_prefix | hq_left_suffix
    · exact Or.inr
        (Walk.support_takeUntil_subset (pair.2 : G.Walk v t) hx_right
          hq_right_prefix)
    · exact Or.inl
        (Walk.support_dropUntil_subset (pair.1 : G.Walk v s) hx_left
          hq_left_suffix)
  have hqy : q ≠ y := by
    intro hqy_eq
    exact hy_not_swap (by simpa [hqy_eq] using hq_swap)
  have hqw : q ≠ w := by
    intro hqw_eq
    have hq_after_y :
        q ∈ (rs.dropUntil y hy_rs).support :=
      Walk.support_takeUntil_subset (rs.dropUntil y hy_rs) ha_tail hq_mid
    exact hw_not_after_y (by simpa [hqw_eq] using hq_after_y)
  have hq_bad :
      ¬ (q ∈ (pair.1 : G.Walk v s).support ∧
         q ∈ (pair.2 : G.Walk v t).support ∧ q ≠ x) := by
    intro hq_common_ne
    exact hq_common ⟨hq_common_ne.1, hq_common_ne.2.1⟩
  have hqa : q = a :=
    hfirst_after_y q hqv hqy hqw hq_old hq_bad hq_mid
  exact False.elim (ha_not_swap (by simpa [hqa] using hq_swap))

private lemma two_sided_middle_guard_of_first_noncommon_not_left_prefix_not_swap
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x w y a : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hy_rs : y ∈ rs.support)
    (ha_tail : a ∈ (rs.dropUntil y hy_rs).support)
    (hy_not_swap :
      y ∉
        (((((pair.2 : G.Walk v t).takeUntil x hx_right).append
          ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath) :
            G.Walk v s).support)
    (hw_not_after_y : w ∉ (rs.dropUntil y hy_rs).support)
    (ha_not_swap :
      a ∉
        (((((pair.2 : G.Walk v t).takeUntil x hx_right).append
          ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath) :
            G.Walk v s).support)
    (hfirst_after_y :
      ∀ q : α, q ≠ v → q ≠ y → q ≠ w →
        (q ∈ (pair.1 : G.Walk v s).support ∨
          q ∈ (pair.2 : G.Walk v t).support) →
        ¬ (q ∈ (pair.1 : G.Walk v s).support ∧
           q ∈ (pair.2 : G.Walk v t).support ∧ q ≠ x) →
        q ∉ ((pair.1 : G.Walk v s).takeUntil x hx_left).support →
        q ∈ ((rs.dropUntil y hy_rs).takeUntil a ha_tail).support →
        q = a) :
      ∀ q : α, q ≠ v →
        q ∈
          (((((pair.2 : G.Walk v t).takeUntil x hx_right).append
            ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath) :
              G.Walk v s).support →
        q ∈ ((rs.dropUntil y hy_rs).takeUntil a ha_tail).support →
        q ∈ (pair.1 : G.Walk v s).support ∧
          q ∈ (pair.2 : G.Walk v t).support := by
  intro q hqv hq_swap hq_mid
  by_cases hq_common :
      q ∈ (pair.1 : G.Walk v s).support ∧
        q ∈ (pair.2 : G.Walk v t).support
  · exact hq_common
  have hq_swap_raw :
      q ∈ (((pair.2 : G.Walk v t).takeUntil x hx_right).append
        ((pair.1 : G.Walk v s).dropUntil x hx_left)).support :=
    Walk.support_toPath_subset _ hq_swap
  rw [Walk.mem_support_append_iff] at hq_swap_raw
  have hq_old :
      q ∈ (pair.1 : G.Walk v s).support ∨
        q ∈ (pair.2 : G.Walk v t).support := by
    rcases hq_swap_raw with hq_right_prefix | hq_left_suffix
    · exact Or.inr
        (Walk.support_takeUntil_subset (pair.2 : G.Walk v t) hx_right
          hq_right_prefix)
    · exact Or.inl
        (Walk.support_dropUntil_subset (pair.1 : G.Walk v s) hx_left
          hq_left_suffix)
  have hq_not_left_prefix :
      q ∉ ((pair.1 : G.Walk v s).takeUntil x hx_left).support := by
    intro hq_left_prefix
    rcases hq_swap_raw with hq_right_prefix | hq_left_suffix
    · exact hq_common
        ⟨Walk.support_takeUntil_subset (pair.1 : G.Walk v s) hx_left
            hq_left_prefix,
          Walk.support_takeUntil_subset (pair.2 : G.Walk v t) hx_right
            hq_right_prefix⟩
    · by_cases hqx : q = x
      · exact hq_common
          ⟨Walk.support_takeUntil_subset (pair.1 : G.Walk v s) hx_left
              hq_left_prefix,
            by simpa [hqx] using hx_right⟩
      · exact
          (not_mem_dropUntil_of_mem_takeUntil_ne_on_isPath
            (G := G) (p := (pair.1 : G.Walk v s)) pair.1.property
            hx_left
            (Walk.support_takeUntil_subset (pair.1 : G.Walk v s) hx_left
              hq_left_prefix)
            hq_left_prefix hqx) hq_left_suffix
  have hqy : q ≠ y := by
    intro hqy_eq
    exact hy_not_swap (by simpa [hqy_eq] using hq_swap)
  have hqw : q ≠ w := by
    intro hqw_eq
    have hq_after_y :
        q ∈ (rs.dropUntil y hy_rs).support :=
      Walk.support_takeUntil_subset (rs.dropUntil y hy_rs) ha_tail hq_mid
    exact hw_not_after_y (by simpa [hqw_eq] using hq_after_y)
  have hq_bad :
      ¬ (q ∈ (pair.1 : G.Walk v s).support ∧
         q ∈ (pair.2 : G.Walk v t).support ∧ q ≠ x) := by
    intro hq_common_ne
    exact hq_common ⟨hq_common_ne.1, hq_common_ne.2.1⟩
  have hqa : q = a :=
    hfirst_after_y q hqv hqy hqw hq_old hq_bad hq_not_left_prefix hq_mid
  exact False.elim (ha_not_swap (by simpa [hqa] using hq_swap))

private lemma exists_first_bridge_guard_counterexample
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x y z : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hy_rs : y ∈ rs.support)
    (hz_tail : z ∈ (rs.dropUntil y hy_rs).support)
    (hguard_fail :
      ¬ ∀ q : α, q ≠ v →
        q ∈
          (((((pair.2 : G.Walk v t).takeUntil x hx_right).append
            ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath) :
              G.Walk v s).support →
        q ∈ ((rs.dropUntil y hy_rs).takeUntil z hz_tail).support →
        q ∈ (pair.1 : G.Walk v s).support ∧
          q ∈ (pair.2 : G.Walk v t).support) :
    ∃ q : α,
      ∃ hq_mid : q ∈ ((rs.dropUntil y hy_rs).takeUntil z hz_tail).support,
      q ≠ v ∧
      q ∈
        (((((pair.2 : G.Walk v t).takeUntil x hx_right).append
          ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath) :
            G.Walk v s).support ∧
      ¬ (q ∈ (pair.1 : G.Walk v s).support ∧
        q ∈ (pair.2 : G.Walk v t).support) ∧
      ∀ r : α, r ≠ v →
        r ∈
          (((((pair.2 : G.Walk v t).takeUntil x hx_right).append
            ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath) :
              G.Walk v s).support →
        ¬ (r ∈ (pair.1 : G.Walk v s).support ∧
          r ∈ (pair.2 : G.Walk v t).support) →
        r ∈
          (((rs.dropUntil y hy_rs).takeUntil z hz_tail).takeUntil q
            hq_mid).support →
        r = q := by
  classical
  let swapLeft : G.Path v s :=
    (((pair.2 : G.Walk v t).takeUntil x hx_right).append
      ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath
  let middle : G.Walk y z := (rs.dropUntil y hy_rs).takeUntil z hz_tail
  let S : Finset α :=
    Finset.univ.filter fun q =>
      q ≠ v ∧
      q ∈ (swapLeft : G.Walk v s).support ∧
      ¬ (q ∈ (pair.1 : G.Walk v s).support ∧
        q ∈ (pair.2 : G.Walk v t).support)
  have hfail := hguard_fail
  push_neg at hfail
  rcases hfail with ⟨q, hqv, hq_swap, hq_mid, hq_not_common_raw⟩
  have hq_not_common :
      ¬ (q ∈ (pair.1 : G.Walk v s).support ∧
        q ∈ (pair.2 : G.Walk v t).support) := by
    intro hq_common
    exact hq_not_common_raw hq_common.1 hq_common.2
  have hnonempty : {q ∈ S | q ∈ middle.support}.Nonempty := by
    refine ⟨q, ?_⟩
    rw [Finset.mem_filter]
    exact ⟨by
      rw [Finset.mem_filter]
      exact ⟨by simp, hqv, by simpa [swapLeft] using hq_swap,
        hq_not_common⟩,
      by simpa [middle] using hq_mid⟩
  rcases exists_first_mem_support_forall_mem_takeUntil_imp_eq
      (G := G) middle S hnonempty with
    ⟨q0, hq0S, hq0_mid, hfirst⟩
  have hq0v : q0 ≠ v := by
    simpa [S] using (Finset.mem_filter.mp hq0S).2.1
  have hq0_swap :
      q0 ∈ (swapLeft : G.Walk v s).support := by
    simpa [S] using (Finset.mem_filter.mp hq0S).2.2.1
  have hq0_not_common :
      ¬ (q0 ∈ (pair.1 : G.Walk v s).support ∧
        q0 ∈ (pair.2 : G.Walk v t).support) := by
    simpa [S] using (Finset.mem_filter.mp hq0S).2.2.2
  refine ⟨q0, by simpa [middle] using hq0_mid, hq0v,
    by simpa [swapLeft] using hq0_swap, hq0_not_common, ?_⟩
  intro r hrv hr_swap hr_not_common hr_prefix
  have hrS : r ∈ S := by
    rw [Finset.mem_filter]
    exact ⟨by simp, hrv, by simpa [swapLeft] using hr_swap,
      hr_not_common⟩
  exact hfirst r hrS (by simpa [middle] using hr_prefix)

private lemma bridge_guard_counterexample_side
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x q : α}
    {pair : G.Path v s × G.Path v t}
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hq_swap :
      q ∈
        (((((pair.2 : G.Walk v t).takeUntil x hx_right).append
          ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath) :
            G.Walk v s).support)
    (hq_not_common :
      ¬ (q ∈ (pair.1 : G.Walk v s).support ∧
        q ∈ (pair.2 : G.Walk v t).support)) :
    (q ∈ (pair.2 : G.Walk v t).support ∧
      q ∉ (pair.1 : G.Walk v s).support ∧
      q ∈ ((pair.2 : G.Walk v t).takeUntil x hx_right).support) ∨
    (q ∈ (pair.1 : G.Walk v s).support ∧
      q ∉ (pair.2 : G.Walk v t).support ∧
      q ∈ ((pair.1 : G.Walk v s).dropUntil x hx_left).support) := by
  have hq_swap_raw :
      q ∈ (((pair.2 : G.Walk v t).takeUntil x hx_right).append
        ((pair.1 : G.Walk v s).dropUntil x hx_left)).support :=
    Walk.support_toPath_subset _ hq_swap
  rw [Walk.mem_support_append_iff] at hq_swap_raw
  rcases hq_swap_raw with hq_right_prefix | hq_left_suffix
  · have hq_right :
        q ∈ (pair.2 : G.Walk v t).support :=
      Walk.support_takeUntil_subset (pair.2 : G.Walk v t) hx_right
        hq_right_prefix
    have hq_not_left :
        q ∉ (pair.1 : G.Walk v s).support := by
      intro hq_left
      exact hq_not_common ⟨hq_left, hq_right⟩
    exact Or.inl ⟨hq_right, hq_not_left, hq_right_prefix⟩
  · have hq_left :
        q ∈ (pair.1 : G.Walk v s).support :=
      Walk.support_dropUntil_subset (pair.1 : G.Walk v s) hx_left
        hq_left_suffix
    have hq_not_right :
        q ∉ (pair.2 : G.Walk v t).support := by
      intro hq_right
      exact hq_not_common ⟨hq_left, hq_right⟩
    exact Or.inr ⟨hq_left, hq_not_right, hq_left_suffix⟩

private lemma terminal_set_fan_two_sided_bridge_commonCard_lt_of_middle_guard
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x y z : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rs : x ∉ rs.support)
    (hy_left : y ∈ (pair.1 : G.Walk v s).support)
    (hy_rs : y ∈ rs.support)
    (hz_tail : z ∈ (rs.dropUntil y hy_rs).support)
    (hz_right : z ∈ (pair.2 : G.Walk v t).support)
    (hy_prefix_x :
      y ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support)
    (hz_suffix_x :
      z ∈ ((pair.2 : G.Walk v t).dropUntil x hx_right).support)
    (hyx : y ≠ x)
    (hzx : z ≠ x)
    (hmiddle_guard :
      ∀ q : α, q ≠ v →
        q ∈
          (((((pair.2 : G.Walk v t).takeUntil x hx_right).append
            ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath) :
              G.Walk v s).support →
        q ∈ ((rs.dropUntil y hy_rs).takeUntil z hz_tail).support →
        q ∈ (pair.1 : G.Walk v s).support ∧
          q ∈ (pair.2 : G.Walk v t).support) :
    ∃ pair' : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  classical
  let swapLeft : G.Path v s :=
    (((pair.2 : G.Walk v t).takeUntil x hx_right).append
      ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath
  let bridgeRight : G.Path v t :=
    ((((pair.1 : G.Walk v s).takeUntil y hy_left).append
      ((rs.dropUntil y hy_rs).takeUntil z hz_tail)).append
      ((pair.2 : G.Walk v t).dropUntil z hz_right)).toPath
  let bridged : G.Path v s × G.Path v t := (swapLeft, bridgeRight)
  refine ⟨bridged, ?_⟩
  have hx_not_bridge :
      x ∉ (bridgeRight : G.Walk v t).support := by
    simpa [bridgeRight] using
      (not_mem_left_rs_right_bridge_of_prefix_suffix
        (G := G) (left := (pair.1 : G.Walk v s)) (rs := rs)
        (right := (pair.2 : G.Walk v t))
        pair.1.property pair.2.property hx_left hy_left hy_rs hz_tail
        hx_right hz_right hy_prefix_x hz_suffix_x hyx hzx hx_rs)
  have hcommon_subset_old_without_x :
      (((swapLeft : G.Walk v s).support.toFinset ∩
          (bridgeRight : G.Walk v t).support.toFinset).erase v) ⊆
        (((pair.1 : G.Walk v s).support.toFinset ∩
          (pair.2 : G.Walk v t).support.toFinset).erase v).erase x := by
    intro q hq
    rw [Finset.mem_erase, Finset.mem_inter] at hq
    rcases hq with ⟨hqv, hq_swap, hq_bridge⟩
    have hq_swap_walk : q ∈ (swapLeft : G.Walk v s).support := by
      simpa using hq_swap
    have hq_bridge_walk : q ∈ (bridgeRight : G.Walk v t).support := by
      simpa using hq_bridge
    have hqx : q ≠ x := by
      intro hqx_eq
      exact hx_not_bridge (by simpa [hqx_eq] using hq_bridge_walk)
    have hq_swap_raw :
        q ∈ (((pair.2 : G.Walk v t).takeUntil x hx_right).append
          ((pair.1 : G.Walk v s).dropUntil x hx_left)).support :=
      Walk.support_toPath_subset _ hq_swap_walk
    rw [Walk.mem_support_append_iff] at hq_swap_raw
    rw [Finset.mem_erase, Finset.mem_erase, Finset.mem_inter]
    refine ⟨hqx, hqv, ?_, ?_⟩
    rcases mem_support_toPath_append_three_subset
        (G := G)
        (p := (pair.1 : G.Walk v s).takeUntil y hy_left)
        (q := (rs.dropUntil y hy_rs).takeUntil z hz_tail)
        (r := (pair.2 : G.Walk v t).dropUntil z hz_right)
        (by simpa [bridgeRight] using hq_bridge_walk) with
      hq_left_prefix | hq_mid | hq_right_suffix
    · exact
        by simpa using
          (Walk.support_takeUntil_subset (pair.1 : G.Walk v s) hy_left
            hq_left_prefix)
    · exact by
        simpa using
          (hmiddle_guard q hqv (by simpa [swapLeft] using hq_swap_walk)
            hq_mid).1
    · rcases hq_swap_raw with hq_right_prefix | hq_left_suffix
      · have hq_right :
            q ∈ (pair.2 : G.Walk v t).support :=
          Walk.support_takeUntil_subset (pair.2 : G.Walk v t) hx_right
            hq_right_prefix
        have hq_after_x :
            q ∈ ((pair.2 : G.Walk v t).dropUntil x hx_right).support :=
          mem_dropUntil_of_mem_dropUntil_of_mem_dropUntil
            (G := G) (p := (pair.2 : G.Walk v t)) pair.2.property
            hx_right hz_right hz_suffix_x hq_right_suffix
        exact False.elim
          ((not_mem_dropUntil_of_mem_takeUntil_ne_on_isPath
            (G := G) (p := (pair.2 : G.Walk v t)) pair.2.property
            hx_right hq_right hq_right_prefix hqx) hq_after_x)
      · exact
          by simpa using
            (Walk.support_dropUntil_subset (pair.1 : G.Walk v s) hx_left
              hq_left_suffix)
    · rcases hq_swap_raw with hq_right_prefix | hq_left_suffix
      · exact
          by simpa using
            (Walk.support_takeUntil_subset (pair.2 : G.Walk v t) hx_right
              hq_right_prefix)
      · rcases mem_support_toPath_append_three_subset
          (G := G)
          (p := (pair.1 : G.Walk v s).takeUntil y hy_left)
          (q := (rs.dropUntil y hy_rs).takeUntil z hz_tail)
          (r := (pair.2 : G.Walk v t).dropUntil z hz_right)
          (by simpa [bridgeRight] using hq_bridge_walk) with
        hq_left_prefix | hq_mid | hq_right_suffix
        · have hq_left :
              q ∈ (pair.1 : G.Walk v s).support :=
            Walk.support_dropUntil_subset (pair.1 : G.Walk v s) hx_left
              hq_left_suffix
          have hq_prefix_x :
              q ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support :=
            mem_takeUntil_of_mem_takeUntil_of_mem_takeUntil
              (G := G) (pair.1 : G.Walk v s) hx_left hy_left
              hy_prefix_x hq_left_prefix
          exact False.elim
            ((not_mem_dropUntil_of_mem_takeUntil_ne_on_isPath
              (G := G) (p := (pair.1 : G.Walk v s)) pair.1.property
              hx_left hq_left hq_prefix_x hqx) hq_left_suffix)
        · exact by
            simpa using
              (hmiddle_guard q hqv (by simpa [swapLeft] using hq_swap_walk)
                hq_mid).2
        · exact
            by simpa using
              (Walk.support_dropUntil_subset (pair.2 : G.Walk v t) hz_right
                hq_right_suffix)
  simpa [terminalPathPairCommonCard, bridged, swapLeft, bridgeRight] using
    (common_support_erase_card_lt_of_subset_erase_common
      (G := G) (v := v) (s := s) (t := t)
      (qs := (pair.1 : G.Walk v s))
      (qt := (pair.2 : G.Walk v t))
      (qs' := (swapLeft : G.Walk v s))
      (qt' := (bridgeRight : G.Walk v t))
      (x := x) hcommon_subset_old_without_x hx_left hx_right hxv)

private lemma not_mem_right_rs_left_bridge_of_prefix_suffix
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x a b : α}
    (left : G.Walk v s) (rs : G.Walk v s) (right : G.Walk v t)
    (hleftPath : left.IsPath) (_hrightPath : right.IsPath)
    (hx_left : x ∈ left.support)
    (hx_right : x ∈ right.support)
    (ha_right : a ∈ right.support) (ha_rs : a ∈ rs.support)
    (hb_tail : b ∈ (rs.dropUntil a ha_rs).support)
    (hb_left : b ∈ left.support)
    (ha_prefix_x : a ∈ (right.takeUntil x hx_right).support)
    (hb_suffix_x : b ∈ (left.dropUntil x hx_left).support)
    (hax : a ≠ x) (hbx : b ≠ x)
    (hx_rs : x ∉ rs.support) :
    x ∉ ((((right.takeUntil a ha_right).append
      ((rs.dropUntil a ha_rs).takeUntil b hb_tail)).append
      (left.dropUntil b hb_left)).toPath : G.Walk v s).support := by
  intro hx_bridge
  rcases mem_support_toPath_append_three_subset
      (G := G)
      (p := right.takeUntil a ha_right)
      (q := (rs.dropUntil a ha_rs).takeUntil b hb_tail)
      (r := left.dropUntil b hb_left)
      hx_bridge with hx_right_prefix | hx_mid | hx_left_suffix
  · exact
      (not_mem_takeUntil_later_of_mem_takeUntil_of_support
        (G := G) right hx_right ha_right ha_prefix_x hax)
      hx_right_prefix
  · exact hx_rs
      (Walk.support_dropUntil_subset rs ha_rs
        (Walk.support_takeUntil_subset (rs.dropUntil a ha_rs) hb_tail
          hx_mid))
  · exact
      (not_both_mem_dropUntil_on_simple_path
        (G := G) (p := left) hleftPath hx_left hb_left
        hx_left_suffix hb_suffix_x (fun hxb => hbx hxb.symm))

private lemma not_mem_left_bypass_of_prefix_suffix
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s x y a : α}
    (left : G.Walk v s) (rs : G.Walk v s)
    (hleftPath : left.IsPath)
    (hx_left : x ∈ left.support)
    (hy_left : y ∈ left.support) (hy_rs : y ∈ rs.support)
    (ha_tail : a ∈ (rs.dropUntil y hy_rs).support)
    (ha_left : a ∈ left.support)
    (hy_prefix_x : y ∈ (left.takeUntil x hx_left).support)
    (ha_suffix_x : a ∈ (left.dropUntil x hx_left).support)
    (hyx : y ≠ x) (hax : a ≠ x)
    (hx_rs : x ∉ rs.support) :
    x ∉ ((((left.takeUntil y hy_left).append
      ((rs.dropUntil y hy_rs).takeUntil a ha_tail)).append
      (left.dropUntil a ha_left)).toPath : G.Walk v s).support := by
  intro hx_bypass
  rcases mem_support_toPath_append_three_subset
      (G := G)
      (p := left.takeUntil y hy_left)
      (q := (rs.dropUntil y hy_rs).takeUntil a ha_tail)
      (r := left.dropUntil a ha_left)
      hx_bypass with hx_prefix | hx_mid | hx_suffix
  · exact
      (not_mem_takeUntil_later_of_mem_takeUntil_of_support
        (G := G) left hx_left hy_left hy_prefix_x hyx) hx_prefix
  · exact hx_rs
      (Walk.support_dropUntil_subset rs hy_rs
        (Walk.support_takeUntil_subset (rs.dropUntil y hy_rs) ha_tail
          hx_mid))
  · exact
      (not_both_mem_dropUntil_on_simple_path
        (G := G) (p := left) hleftPath hx_left ha_left
        hx_suffix ha_suffix_x (fun hxa => hax hxa.symm))

private lemma terminal_set_fan_left_bypass_commonCard_lt_of_segment_right_guard
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x y a : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rs : x ∉ rs.support)
    (hy_left : y ∈ (pair.1 : G.Walk v s).support)
    (hy_rs : y ∈ rs.support)
    (ha_left : a ∈ (pair.1 : G.Walk v s).support)
    (ha_tail : a ∈ (rs.dropUntil y hy_rs).support)
    (hy_prefix_x :
      y ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support)
    (ha_suffix_x :
      a ∈ ((pair.1 : G.Walk v s).dropUntil x hx_left).support)
    (hyx : y ≠ x)
    (hax : a ≠ x)
    (hsegment_right_guard :
      ∀ q : α, q ≠ v →
        q ∈ (pair.2 : G.Walk v t).support →
        q ∈ ((rs.dropUntil y hy_rs).takeUntil a ha_tail).support →
        q ∈ (pair.1 : G.Walk v s).support) :
    ∃ pair' : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  classical
  let leftBypass : G.Path v s :=
    ((((pair.1 : G.Walk v s).takeUntil y hy_left).append
      ((rs.dropUntil y hy_rs).takeUntil a ha_tail)).append
      ((pair.1 : G.Walk v s).dropUntil a ha_left)).toPath
  let bypassPair : G.Path v s × G.Path v t := (leftBypass, pair.2)
  refine ⟨bypassPair, ?_⟩
  have hx_not_bypass :
      x ∉ (leftBypass : G.Walk v s).support := by
    simpa [leftBypass] using
      (not_mem_left_bypass_of_prefix_suffix
        (G := G) (left := (pair.1 : G.Walk v s)) (rs := rs)
        pair.1.property hx_left hy_left hy_rs ha_tail ha_left
        hy_prefix_x ha_suffix_x hyx hax hx_rs)
  have hcommon_subset_old_without_x :
      (((leftBypass : G.Walk v s).support.toFinset ∩
          (pair.2 : G.Walk v t).support.toFinset).erase v) ⊆
        (((pair.1 : G.Walk v s).support.toFinset ∩
          (pair.2 : G.Walk v t).support.toFinset).erase v).erase x := by
    intro q hq
    rw [Finset.mem_erase, Finset.mem_inter] at hq
    rcases hq with ⟨hqv, hq_bypass, hq_right⟩
    have hq_bypass_walk : q ∈ (leftBypass : G.Walk v s).support := by
      simpa using hq_bypass
    rw [Finset.mem_erase, Finset.mem_erase, Finset.mem_inter]
    refine ⟨?_, hqv, ?_, by simpa using hq_right⟩
    · intro hqx
      exact hx_not_bypass (by simpa [hqx] using hq_bypass_walk)
    · rcases mem_support_toPath_append_three_subset
          (G := G)
          (p := (pair.1 : G.Walk v s).takeUntil y hy_left)
          (q := (rs.dropUntil y hy_rs).takeUntil a ha_tail)
          (r := (pair.1 : G.Walk v s).dropUntil a ha_left)
          (by simpa [leftBypass] using hq_bypass_walk) with
        hq_prefix | hq_middle | hq_suffix
      · exact
          by simpa using
            (Walk.support_takeUntil_subset (pair.1 : G.Walk v s)
              hy_left hq_prefix)
      · exact by
          simpa using hsegment_right_guard q hqv (by simpa using hq_right)
            hq_middle
      · exact
          by simpa using
            (Walk.support_dropUntil_subset (pair.1 : G.Walk v s)
              ha_left hq_suffix)
  simpa [terminalPathPairCommonCard, bypassPair] using
    (common_support_erase_card_lt_of_subset_erase_common
      (G := G) (v := v) (s := s) (t := t)
      (qs := (pair.1 : G.Walk v s))
      (qt := (pair.2 : G.Walk v t))
      (qs' := (leftBypass : G.Walk v s))
      (qt' := (pair.2 : G.Walk v t))
      (x := x) hcommon_subset_old_without_x hx_left hx_right hxv)

private lemma terminal_set_fan_left_bypass_alt_commonCard_lt_of_middle_guard
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x a b : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rs : x ∉ rs.support)
    (ha_right : a ∈ (pair.2 : G.Walk v t).support)
    (ha_rs : a ∈ rs.support)
    (hb_tail : b ∈ (rs.dropUntil a ha_rs).support)
    (hb_left : b ∈ (pair.1 : G.Walk v s).support)
    (ha_prefix_x :
      a ∈ ((pair.2 : G.Walk v t).takeUntil x hx_right).support)
    (hb_suffix_x :
      b ∈ ((pair.1 : G.Walk v s).dropUntil x hx_left).support)
    (hax : a ≠ x)
    (hbx : b ≠ x)
    (hmiddle_guard :
      ∀ q : α, q ≠ v →
        q ∈ ((rs.dropUntil a ha_rs).takeUntil b hb_tail).support →
        q ∈
          (((((pair.1 : G.Walk v s).takeUntil x hx_left).append
            ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath) :
              G.Walk v t).support →
        q ∈ (pair.1 : G.Walk v s).support ∧
          q ∈ (pair.2 : G.Walk v t).support) :
    ∃ pair' : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  classical
  let bypassLeft : G.Path v s :=
    ((((pair.2 : G.Walk v t).takeUntil a ha_right).append
      ((rs.dropUntil a ha_rs).takeUntil b hb_tail)).append
      ((pair.1 : G.Walk v s).dropUntil b hb_left)).toPath
  let altRight : G.Path v t :=
    (((pair.1 : G.Walk v s).takeUntil x hx_left).append
      ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
  let bypassPair : G.Path v s × G.Path v t := (bypassLeft, altRight)
  refine ⟨bypassPair, ?_⟩
  have hx_not_bypassLeft :
      x ∉ (bypassLeft : G.Walk v s).support := by
    simpa [bypassLeft] using
      (not_mem_right_rs_left_bridge_of_prefix_suffix
        (G := G) (left := (pair.1 : G.Walk v s)) (rs := rs)
        (right := (pair.2 : G.Walk v t))
        pair.1.property pair.2.property hx_left hx_right
        ha_right ha_rs hb_tail hb_left ha_prefix_x hb_suffix_x hax hbx
        hx_rs)
  have hcommon_subset_old_without_x :
      (((bypassLeft : G.Walk v s).support.toFinset ∩
          (altRight : G.Walk v t).support.toFinset).erase v) ⊆
        (((pair.1 : G.Walk v s).support.toFinset ∩
          (pair.2 : G.Walk v t).support.toFinset).erase v).erase x := by
    intro q hq
    rw [Finset.mem_erase, Finset.mem_inter] at hq
    rcases hq with ⟨hqv, hq_bypass, hq_alt⟩
    have hq_bypass_walk : q ∈ (bypassLeft : G.Walk v s).support := by
      simpa using hq_bypass
    have hq_alt_walk : q ∈ (altRight : G.Walk v t).support := by
      simpa using hq_alt
    have hqx : q ≠ x := by
      intro hqx_eq
      exact hx_not_bypassLeft (by simpa [hqx_eq] using hq_bypass_walk)
    have hq_alt_raw :
        q ∈ (((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).support :=
      Walk.support_toPath_subset _ hq_alt_walk
    rw [Walk.mem_support_append_iff] at hq_alt_raw
    rw [Finset.mem_erase, Finset.mem_erase, Finset.mem_inter]
    refine ⟨hqx, hqv, ?_, ?_⟩
    rcases mem_support_toPath_append_three_subset
        (G := G)
        (p := (pair.2 : G.Walk v t).takeUntil a ha_right)
        (q := (rs.dropUntil a ha_rs).takeUntil b hb_tail)
        (r := (pair.1 : G.Walk v s).dropUntil b hb_left)
        (by simpa [bypassLeft] using hq_bypass_walk) with
      hq_right_prefix | hq_mid | hq_left_suffix
    · rcases hq_alt_raw with hq_left_prefix | hq_right_suffix
      · exact
          by simpa using
            (Walk.support_takeUntil_subset (pair.1 : G.Walk v s) hx_left
              hq_left_prefix)
      · have hq_right :
            q ∈ (pair.2 : G.Walk v t).support :=
          Walk.support_takeUntil_subset (pair.2 : G.Walk v t) ha_right
            hq_right_prefix
        have hq_prefix_x :
            q ∈ ((pair.2 : G.Walk v t).takeUntil x hx_right).support :=
          mem_takeUntil_of_mem_takeUntil_of_mem_takeUntil
            (G := G) (pair.2 : G.Walk v t) hx_right ha_right
            ha_prefix_x hq_right_prefix
        exact False.elim
          ((not_mem_dropUntil_of_mem_takeUntil_ne_on_isPath
            (G := G) (p := (pair.2 : G.Walk v t)) pair.2.property
            hx_right hq_right hq_prefix_x hqx) hq_right_suffix)
    · exact by
        simpa using
          (hmiddle_guard q hqv hq_mid (by simpa [altRight] using hq_alt_walk)).1
    · exact
        by simpa using
          (Walk.support_dropUntil_subset (pair.1 : G.Walk v s) hb_left
            hq_left_suffix)
    · rcases mem_support_toPath_append_three_subset
        (G := G)
        (p := (pair.2 : G.Walk v t).takeUntil a ha_right)
        (q := (rs.dropUntil a ha_rs).takeUntil b hb_tail)
        (r := (pair.1 : G.Walk v s).dropUntil b hb_left)
        (by simpa [bypassLeft] using hq_bypass_walk) with
      hq_right_prefix | hq_mid | hq_left_suffix
      · exact
          by simpa using
            (Walk.support_takeUntil_subset (pair.2 : G.Walk v t) ha_right
              hq_right_prefix)
      · exact by
          simpa using
            (hmiddle_guard q hqv hq_mid (by simpa [altRight] using hq_alt_walk)).2
      · rcases hq_alt_raw with hq_left_prefix | hq_right_suffix
        · have hq_left :
              q ∈ (pair.1 : G.Walk v s).support :=
            Walk.support_dropUntil_subset (pair.1 : G.Walk v s) hb_left
              hq_left_suffix
          have hq_after_x :
              q ∈ ((pair.1 : G.Walk v s).dropUntil x hx_left).support :=
            mem_dropUntil_of_mem_dropUntil_of_mem_dropUntil
              (G := G) (p := (pair.1 : G.Walk v s)) pair.1.property
              hx_left hb_left hb_suffix_x hq_left_suffix
          exact False.elim
            ((not_mem_dropUntil_of_mem_takeUntil_ne_on_isPath
              (G := G) (p := (pair.1 : G.Walk v s)) pair.1.property
              hx_left hq_left hq_left_prefix hqx) hq_after_x)
        · exact
            by simpa using
              (Walk.support_dropUntil_subset (pair.2 : G.Walk v t) hx_right
                hq_right_suffix)
  simpa [terminalPathPairCommonCard, bypassPair, bypassLeft, altRight] using
    (common_support_erase_card_lt_of_subset_erase_common
      (G := G) (v := v) (s := s) (t := t)
      (qs := (pair.1 : G.Walk v s))
      (qt := (pair.2 : G.Walk v t))
      (qs' := (bypassLeft : G.Walk v s))
      (qt' := (altRight : G.Walk v t))
      (x := x) hcommon_subset_old_without_x hx_left hx_right hxv)

private lemma terminal_set_fan_right_bypass_commonCard_lt_of_segment_left_guard
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x a z : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rs : x ∉ rs.support)
    (ha_right : a ∈ (pair.2 : G.Walk v t).support)
    (ha_rs : a ∈ rs.support)
    (hz_right : z ∈ (pair.2 : G.Walk v t).support)
    (hz_tail : z ∈ (rs.dropUntil a ha_rs).support)
    (ha_prefix_x :
      a ∈ ((pair.2 : G.Walk v t).takeUntil x hx_right).support)
    (hz_suffix_x :
      z ∈ ((pair.2 : G.Walk v t).dropUntil x hx_right).support)
    (hax : a ≠ x)
    (hzx : z ≠ x)
    (hsegment_left_guard :
      ∀ y : α, y ≠ v →
        y ∈ (pair.1 : G.Walk v s).support →
        y ∈ ((rs.dropUntil a ha_rs).takeUntil z hz_tail).support →
        y ∈ (pair.2 : G.Walk v t).support) :
    ∃ pair' : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  classical
  let rightBypass : G.Path v t :=
    ((((pair.2 : G.Walk v t).takeUntil a ha_right).append
      ((rs.dropUntil a ha_rs).takeUntil z hz_tail)).append
      ((pair.2 : G.Walk v t).dropUntil z hz_right)).toPath
  let bypassPair : G.Path v s × G.Path v t := (pair.1, rightBypass)
  refine ⟨bypassPair, ?_⟩
  have hx_not_bypass :
      x ∉ (rightBypass : G.Walk v t).support := by
    simpa [rightBypass] using
      (not_mem_right_bypass_of_takeUntil_dropUntil_around
        (G := G) (right := (pair.2 : G.Walk v t)) (rs := rs)
        pair.2.property hx_right ha_right ha_rs hz_right hz_tail
        ha_prefix_x hz_suffix_x hax hzx hx_rs)
  have hcommon_subset_old_without_x :
      ((pair.1 : G.Walk v s).support.toFinset ∩
          (rightBypass : G.Walk v t).support.toFinset).erase v ⊆
        (((pair.1 : G.Walk v s).support.toFinset ∩
          (pair.2 : G.Walk v t).support.toFinset).erase v).erase x := by
    intro y hy
    rw [Finset.mem_erase, Finset.mem_inter] at hy
    rcases hy with ⟨hyv, hy_left, hy_bypass⟩
    have hy_bypass_walk : y ∈ (rightBypass : G.Walk v t).support := by
      simpa using hy_bypass
    rw [Finset.mem_erase, Finset.mem_erase, Finset.mem_inter]
    refine ⟨?_, hyv, by simpa using hy_left, ?_⟩
    · intro hyx
      exact hx_not_bypass (by simpa [hyx] using hy_bypass_walk)
    · rcases mem_support_toPath_append_three_subset
          (G := G)
          (p := (pair.2 : G.Walk v t).takeUntil a ha_right)
          (q := (rs.dropUntil a ha_rs).takeUntil z hz_tail)
          (r := (pair.2 : G.Walk v t).dropUntil z hz_right)
          (by simpa [rightBypass] using hy_bypass_walk) with
        hy_prefix | hy_middle | hy_suffix
      · exact
          by simpa using
            (Walk.support_takeUntil_subset (pair.2 : G.Walk v t)
              ha_right hy_prefix)
      · exact by
          simpa using hsegment_left_guard y hyv (by simpa using hy_left) hy_middle
      · exact
          by simpa using
            (Walk.support_dropUntil_subset (pair.2 : G.Walk v t)
              hz_right hy_suffix)
  simpa [terminalPathPairCommonCard, bypassPair] using
    (common_support_erase_card_lt_of_subset_erase_common
      (G := G) (v := v) (s := s) (t := t)
      (qs := (pair.1 : G.Walk v s))
      (qt := (pair.2 : G.Walk v t))
      (qs' := (pair.1 : G.Walk v s))
      (qt' := (rightBypass : G.Walk v t))
      (x := x) hcommon_subset_old_without_x hx_left hx_right hxv)

private lemma terminal_set_fan_bridge_right_prefix_stage_commonCard_lt
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x a z : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rs : x ∉ rs.support)
    (ha_right : a ∈ (pair.2 : G.Walk v t).support)
    (ha_rs : a ∈ rs.support)
    (hz_right : z ∈ (pair.2 : G.Walk v t).support)
    (hz_rs : z ∈ rs.support)
    (ha_prefix_x :
      a ∈ ((pair.2 : G.Walk v t).takeUntil x hx_right).support)
    (hz_suffix_x :
      z ∈ ((pair.2 : G.Walk v t).dropUntil x hx_right).support)
    (ha_prefix_z : a ∈ (rs.takeUntil z hz_rs).support)
    (haz : a ≠ z)
    (hzx : z ≠ x)
    (hsegment_left_guard :
      ∀ y : α, y ≠ v →
        y ∈ (pair.1 : G.Walk v s).support →
        y ∈ ((rs.dropUntil a ha_rs).takeUntil z
          (mem_dropUntil_of_mem_takeUntil_ne
            (G := G) rs ha_rs hz_rs ha_prefix_z haz)).support →
        y ∈ (pair.2 : G.Walk v t).support) :
    ∃ pair' : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  have hz_tail_a :
      z ∈ (rs.dropUntil a ha_rs).support :=
    mem_dropUntil_of_mem_takeUntil_ne
      (G := G) rs ha_rs hz_rs ha_prefix_z haz
  have hax : a ≠ x := by
    intro hax_eq
    exact hx_rs (by simpa [hax_eq] using ha_rs)
  exact terminal_set_fan_right_bypass_commonCard_lt_of_segment_left_guard
    (G := G) (v := v) (s := s) (t := t)
    (x := x) (a := a) (z := z) (pair := pair) (rs := rs)
    hx_left hx_right hxv hx_rs ha_right ha_rs hz_right hz_tail_a
    ha_prefix_x hz_suffix_x hax hzx
    (by simpa [hz_tail_a] using hsegment_left_guard)

private lemma terminal_set_fan_bridge_left_suffix_stage_commonCard_lt
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x y a : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rs : x ∉ rs.support)
    (hy_left : y ∈ (pair.1 : G.Walk v s).support)
    (hy_rs : y ∈ rs.support)
    (ha_left : a ∈ (pair.1 : G.Walk v s).support)
    (ha_rs : a ∈ rs.support)
    (ha_tail : a ∈ (rs.dropUntil y hy_rs).support)
    (hy_prefix_x :
      y ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support)
    (ha_suffix_x :
      a ∈ ((pair.1 : G.Walk v s).dropUntil x hx_left).support)
    (hyx : y ≠ x)
    (hsegment_right_guard :
      ∀ q : α, q ≠ v →
        q ∈ (pair.2 : G.Walk v t).support →
        q ∈ ((rs.dropUntil y hy_rs).takeUntil a ha_tail).support →
        q ∈ (pair.1 : G.Walk v s).support) :
    ∃ pair' : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  have hax : a ≠ x := by
    intro hax_eq
    exact hx_rs (by simpa [hax_eq] using ha_rs)
  exact terminal_set_fan_left_bypass_commonCard_lt_of_segment_right_guard
    (G := G) (v := v) (s := s) (t := t)
    (x := x) (y := y) (a := a) (pair := pair) (rs := rs)
    hx_left hx_right hxv hx_rs hy_left hy_rs ha_left ha_tail
    hy_prefix_x ha_suffix_x hyx hax hsegment_right_guard

private lemma exists_segment_left_only_of_not_segment_left_guard
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t a z : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    {ha_rs : a ∈ rs.support}
    {hz_tail : z ∈ (rs.dropUntil a ha_rs).support}
    (hnot :
      ¬ ∀ y : α, y ≠ v →
        y ∈ (pair.1 : G.Walk v s).support →
        y ∈ ((rs.dropUntil a ha_rs).takeUntil z hz_tail).support →
        y ∈ (pair.2 : G.Walk v t).support) :
    ∃ y : α,
      y ≠ v ∧
      y ∈ (pair.1 : G.Walk v s).support ∧
      y ∈ ((rs.dropUntil a ha_rs).takeUntil z hz_tail).support ∧
      y ∉ (pair.2 : G.Walk v t).support := by
  classical
  push_neg at hnot
  rcases hnot with ⟨y, hyv, hy_left, hy_mid, hy_not_right⟩
  exact ⟨y, hyv, hy_left, hy_mid, hy_not_right⟩

private lemma exists_first_segment_left_only_of_not_segment_left_guard
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t a z : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    {ha_rs : a ∈ rs.support}
    {hz_tail : z ∈ (rs.dropUntil a ha_rs).support}
    (hnot :
      ¬ ∀ y : α, y ≠ v →
        y ∈ (pair.1 : G.Walk v s).support →
        y ∈ ((rs.dropUntil a ha_rs).takeUntil z hz_tail).support →
        y ∈ (pair.2 : G.Walk v t).support) :
    ∃ y : α,
      ∃ hy_seg :
        y ∈ ((rs.dropUntil a ha_rs).takeUntil z hz_tail).support,
      y ≠ v ∧
      y ∈ (pair.1 : G.Walk v s).support ∧
      y ∉ (pair.2 : G.Walk v t).support ∧
      ∀ q : α, q ≠ v →
        q ∈ (pair.1 : G.Walk v s).support →
        q ∉ (pair.2 : G.Walk v t).support →
        q ∈
          (((rs.dropUntil a ha_rs).takeUntil z hz_tail).takeUntil y
            hy_seg).support →
        q = y := by
  classical
  let seg : G.Walk a z := (rs.dropUntil a ha_rs).takeUntil z hz_tail
  let S : Finset α :=
    Finset.univ.filter fun q =>
      q ≠ v ∧
      q ∈ (pair.1 : G.Walk v s).support ∧
      q ∉ (pair.2 : G.Walk v t).support
  have hnonempty : {q ∈ S | q ∈ seg.support}.Nonempty := by
    push_neg at hnot
    rcases hnot with ⟨y, hyv, hy_left, hy_seg, hy_not_right⟩
    refine ⟨y, ?_⟩
    rw [Finset.mem_filter]
    exact ⟨by
      rw [Finset.mem_filter]
      exact ⟨by simp, hyv, hy_left, hy_not_right⟩,
      by simpa [seg] using hy_seg⟩
  rcases exists_first_mem_support_forall_mem_takeUntil_imp_eq
      (G := G) seg S hnonempty with
    ⟨y, hyS, hy_seg, hfirst⟩
  have hyv : y ≠ v := by
    simpa [S] using (Finset.mem_filter.mp hyS).2.1
  have hy_left : y ∈ (pair.1 : G.Walk v s).support := by
    simpa [S] using (Finset.mem_filter.mp hyS).2.2.1
  have hy_not_right : y ∉ (pair.2 : G.Walk v t).support := by
    simpa [S] using (Finset.mem_filter.mp hyS).2.2.2
  refine ⟨y, by simpa [seg] using hy_seg, hyv, hy_left, hy_not_right, ?_⟩
  intro q hqv hq_left hq_not_right hq_prefix
  have hqS : q ∈ S := by
    rw [Finset.mem_filter]
    exact ⟨by simp, hqv, hq_left, hq_not_right⟩
  exact hfirst q hqS (by simpa [seg] using hq_prefix)

private lemma exists_first_segment_right_only_of_not_segment_right_guard
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t a z : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    {ha_rs : a ∈ rs.support}
    {hz_tail : z ∈ (rs.dropUntil a ha_rs).support}
    (hnot :
      ¬ ∀ y : α, y ≠ v →
        y ∈ (pair.2 : G.Walk v t).support →
        y ∈ ((rs.dropUntil a ha_rs).takeUntil z hz_tail).support →
        y ∈ (pair.1 : G.Walk v s).support) :
    ∃ y : α,
      ∃ hy_seg :
        y ∈ ((rs.dropUntil a ha_rs).takeUntil z hz_tail).support,
      y ≠ v ∧
      y ∈ (pair.2 : G.Walk v t).support ∧
      y ∉ (pair.1 : G.Walk v s).support ∧
      ∀ q : α, q ≠ v →
        q ∈ (pair.2 : G.Walk v t).support →
        q ∉ (pair.1 : G.Walk v s).support →
        q ∈
          (((rs.dropUntil a ha_rs).takeUntil z hz_tail).takeUntil y
            hy_seg).support →
        q = y := by
  classical
  let seg : G.Walk a z := (rs.dropUntil a ha_rs).takeUntil z hz_tail
  let S : Finset α :=
    Finset.univ.filter fun q =>
      q ≠ v ∧
      q ∈ (pair.2 : G.Walk v t).support ∧
      q ∉ (pair.1 : G.Walk v s).support
  have hnonempty : {q ∈ S | q ∈ seg.support}.Nonempty := by
    push_neg at hnot
    rcases hnot with ⟨y, hyv, hy_right, hy_seg, hy_not_left⟩
    refine ⟨y, ?_⟩
    rw [Finset.mem_filter]
    exact ⟨by
      rw [Finset.mem_filter]
      exact ⟨by simp, hyv, hy_right, hy_not_left⟩,
      by simpa [seg] using hy_seg⟩
  rcases exists_first_mem_support_forall_mem_takeUntil_imp_eq
      (G := G) seg S hnonempty with
    ⟨y, hyS, hy_seg, hfirst⟩
  have hyv : y ≠ v := by
    simpa [S] using (Finset.mem_filter.mp hyS).2.1
  have hy_right : y ∈ (pair.2 : G.Walk v t).support := by
    simpa [S] using (Finset.mem_filter.mp hyS).2.2.1
  have hy_not_left : y ∉ (pair.1 : G.Walk v s).support := by
    simpa [S] using (Finset.mem_filter.mp hyS).2.2.2
  refine ⟨y, by simpa [seg] using hy_seg, hyv, hy_right, hy_not_left, ?_⟩
  intro q hqv hq_right hq_not_left hq_prefix
  have hqS : q ∈ S := by
    rw [Finset.mem_filter]
    exact ⟨by simp, hqv, hq_right, hq_not_left⟩
  exact hfirst q hqS (by simpa [seg] using hq_prefix)

private lemma terminal_set_fan_right_prefix_stage_left_suffix_witness_commonCard_lt
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x a z b : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rs : x ∉ rs.support)
    (ha_right : a ∈ (pair.2 : G.Walk v t).support)
    (_ha_not_left : a ∉ (pair.1 : G.Walk v s).support)
    (ha_rs : a ∈ rs.support)
    (ha_prefix_x :
      a ∈ ((pair.2 : G.Walk v t).takeUntil x hx_right).support)
    (_hz_right : z ∈ (pair.2 : G.Walk v t).support)
    (hz_tail : z ∈ (rs.dropUntil a ha_rs).support)
    (_hz_suffix_x :
      z ∈ ((pair.2 : G.Walk v t).dropUntil x hx_right).support)
    (hb_mid :
      b ∈ ((rs.dropUntil a ha_rs).takeUntil z hz_tail).support)
    (_hbv : b ≠ v)
    (hb_left : b ∈ (pair.1 : G.Walk v s).support)
    (hb_not_right : b ∉ (pair.2 : G.Walk v t).support)
    (hb_first_left_only :
      ∀ q : α, q ≠ v →
        q ∈ (pair.1 : G.Walk v s).support →
        q ∉ (pair.2 : G.Walk v t).support →
        q ∈
          (((rs.dropUntil a ha_rs).takeUntil z hz_tail).takeUntil b
            hb_mid).support →
        q = b)
    (hb_suffix_x :
      b ∈ ((pair.1 : G.Walk v s).dropUntil x hx_left).support) :
    ∃ pair' : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  classical
  let altRight : G.Path v t :=
    (((pair.1 : G.Walk v s).takeUntil x hx_left).append
      ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
  have hb_tail_a : b ∈ (rs.dropUntil a ha_rs).support :=
    Walk.support_takeUntil_subset (rs.dropUntil a ha_rs) hz_tail hb_mid
  have hax : a ≠ x := by
    intro hax_eq
    exact hx_rs (by simpa [hax_eq] using ha_rs)
  have hbx : b ≠ x := by
    intro hbx_eq
    exact hb_not_right (by simpa [hbx_eq] using hx_right)
  by_cases hleft_bypass_guard :
      ∀ q : α, q ≠ v →
        q ∈ ((rs.dropUntil a ha_rs).takeUntil b hb_tail_a).support →
        q ∈ (altRight : G.Walk v t).support →
        q ∈ (pair.1 : G.Walk v s).support ∧
          q ∈ (pair.2 : G.Walk v t).support
  · exact
      terminal_set_fan_left_bypass_alt_commonCard_lt_of_middle_guard
        (G := G) (v := v) (s := s) (t := t)
        (x := x) (a := a) (b := b)
        (pair := pair) (rs := rs)
        hx_left hx_right hxv hx_rs ha_right ha_rs hb_tail_a hb_left
        ha_prefix_x hb_suffix_x hax hbx
        (by simpa [altRight] using hleft_bypass_guard)
  · have hb_not_alt : b ∉ (altRight : G.Walk v t).support := by
      intro hb_alt
      have hb_alt_raw :
          b ∈ (((pair.1 : G.Walk v s).takeUntil x hx_left).append
            ((pair.2 : G.Walk v t).dropUntil x hx_right)).support :=
        Walk.support_toPath_subset _ hb_alt
      rw [Walk.mem_support_append_iff] at hb_alt_raw
      rcases hb_alt_raw with hb_left_prefix | hb_right_suffix
      · exact
          (not_mem_dropUntil_of_mem_takeUntil_ne_on_isPath
            (G := G) (p := (pair.1 : G.Walk v s)) pair.1.property
            hx_left hb_left hb_left_prefix hbx) hb_suffix_x
      · exact hb_not_right
          (Walk.support_dropUntil_subset (pair.2 : G.Walk v t)
            hx_right hb_right_suffix)
    have hguard_fail := hleft_bypass_guard
    push_neg at hguard_fail
    rcases hguard_fail with ⟨c, hcv, hc_mid_ab, hc_alt, hc_not_common⟩
    have hc_tail_a : c ∈ (rs.dropUntil a ha_rs).support :=
      Walk.support_takeUntil_subset (rs.dropUntil a ha_rs) hb_tail_a
        hc_mid_ab
    have hcx : c ≠ x := by
      intro hcx_eq
      exact hx_rs
        (by
          have hc_rs : c ∈ rs.support :=
            Walk.support_dropUntil_subset rs ha_rs hc_tail_a
          simpa [hcx_eq] using hc_rs)
    have hc_old_union :
        c ∈ (pair.1 : G.Walk v s).support ∨
          c ∈ (pair.2 : G.Walk v t).support := by
      simpa [altRight] using
        (mem_support_toPath_append_takeUntil_dropUntil_subset
          (G := G)
          (p := (pair.1 : G.Walk v s))
          (q := (pair.2 : G.Walk v t))
          (y := x) (z := c)
          hx_left hx_right hc_alt)
    by_cases hc_left : c ∈ (pair.1 : G.Walk v s).support
    · have hc_not_right : c ∉ (pair.2 : G.Walk v t).support := by
        intro hc_right
        exact hc_not_common hc_left hc_right
      have hc_prefix_b_in_seg :
          c ∈
            (((rs.dropUntil a ha_rs).takeUntil z hz_tail).takeUntil b
              hb_mid).support := by
        simpa [Walk.takeUntil_takeUntil] using hc_mid_ab
      have hcb : c = b :=
        hb_first_left_only c hcv hc_left hc_not_right hc_prefix_b_in_seg
      exact False.elim (hb_not_alt (by simpa [hcb] using hc_alt))
    · have hc_right : c ∈ (pair.2 : G.Walk v t).support := by
        rcases hc_old_union with hc_left' | hc_right
        · exact False.elim (hc_left hc_left')
        · exact hc_right
      have hc_suffix_x :
          c ∈ ((pair.2 : G.Walk v t).dropUntil x hx_right).support := by
        have hc_alt_raw :
            c ∈ (((pair.1 : G.Walk v s).takeUntil x hx_left).append
              ((pair.2 : G.Walk v t).dropUntil x hx_right)).support :=
          Walk.support_toPath_subset _ hc_alt
        rw [Walk.mem_support_append_iff] at hc_alt_raw
        rcases hc_alt_raw with hc_left_prefix | hc_right_suffix
        · exact False.elim
            (hc_left
              (Walk.support_takeUntil_subset (pair.1 : G.Walk v s)
                hx_left hc_left_prefix))
        · exact hc_right_suffix
      have hac : a ≠ c := by
        intro hac_eq
        have hc_prefix_x :
            c ∈ ((pair.2 : G.Walk v t).takeUntil x hx_right).support := by
          simpa [hac_eq] using ha_prefix_x
        exact
          (not_mem_dropUntil_of_mem_takeUntil_ne_on_isPath
            (G := G) (p := (pair.2 : G.Walk v t)) pair.2.property
            hx_right hc_right hc_prefix_x hcx) hc_suffix_x
      have hsegment_guard_c :
          ∀ q : α, q ≠ v →
            q ∈ (pair.1 : G.Walk v s).support →
            q ∈ ((rs.dropUntil a ha_rs).takeUntil c hc_tail_a).support →
            q ∈ (pair.2 : G.Walk v t).support := by
        intro q hqv hq_left hq_mid_ac
        by_cases hq_right : q ∈ (pair.2 : G.Walk v t).support
        · exact hq_right
        · have hq_mid_ab :
              q ∈ ((rs.dropUntil a ha_rs).takeUntil b hb_tail_a).support :=
            mem_takeUntil_of_mem_takeUntil_of_mem_takeUntil
              (G := G) (p := rs.dropUntil a ha_rs)
              (x := b) (y := c) (z := q)
              hb_tail_a hc_tail_a hc_mid_ab hq_mid_ac
          have hq_prefix_b_in_seg :
              q ∈
                (((rs.dropUntil a ha_rs).takeUntil z hz_tail).takeUntil b
                  hb_mid).support := by
            simpa [Walk.takeUntil_takeUntil] using hq_mid_ab
          have hqb : q = b :=
            hb_first_left_only q hqv hq_left hq_right hq_prefix_b_in_seg
          have hcb_ne : c ≠ b := by
            intro hcb_eq
            exact hb_not_right (by simpa [hcb_eq] using hc_right)
          have hb_not_mid_c :
              b ∉ ((rs.dropUntil a ha_rs).takeUntil c hc_tail_a).support :=
            not_mem_takeUntil_later_of_mem_takeUntil_of_support
              (G := G) (p := rs.dropUntil a ha_rs)
              hb_tail_a hc_tail_a hc_mid_ab hcb_ne
          exact False.elim (hb_not_mid_c (by simpa [hqb] using hq_mid_ac))
      exact
        terminal_set_fan_right_bypass_commonCard_lt_of_segment_left_guard
          (G := G) (v := v) (s := s) (t := t)
          (x := x) (a := a) (z := c)
          (pair := pair) (rs := rs)
          hx_left hx_right hxv hx_rs ha_right ha_rs hc_right hc_tail_a
          ha_prefix_x hc_suffix_x hax hcx hsegment_guard_c

private lemma terminal_set_fan_left_suffix_stage_right_suffix_witness_commonCard_lt
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x y a z r : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rs : x ∉ rs.support)
    (hy_left : y ∈ (pair.1 : G.Walk v s).support)
    (hy_rs : y ∈ rs.support)
    (hy_prefix_x :
      y ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support)
    (ha_tail : a ∈ (rs.dropUntil y hy_rs).support)
    (hz_tail : z ∈ (rs.dropUntil y hy_rs).support)
    (ha_mid :
      a ∈ ((rs.dropUntil y hy_rs).takeUntil z hz_tail).support)
    (ha_not_right : a ∉ (pair.2 : G.Walk v t).support)
    (hr_mid :
      r ∈ ((rs.dropUntil y hy_rs).takeUntil a ha_tail).support)
    (_hrv : r ≠ v)
    (hr_right : r ∈ (pair.2 : G.Walk v t).support)
    (hr_not_left : r ∉ (pair.1 : G.Walk v s).support)
    (hr_suffix_x :
      r ∈ ((pair.2 : G.Walk v t).dropUntil x hx_right).support)
    (hfirst_bridge_bad :
      ∀ q : α, q ≠ v →
        q ∈
          (((((pair.2 : G.Walk v t).takeUntil x hx_right).append
            ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath) :
              G.Walk v s).support →
        ¬ (q ∈ (pair.1 : G.Walk v s).support ∧
          q ∈ (pair.2 : G.Walk v t).support) →
        q ∈
          (((rs.dropUntil y hy_rs).takeUntil z hz_tail).takeUntil a
            ha_mid).support →
        q = a) :
    ∃ pair' : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  classical
  have hr_tail_y : r ∈ (rs.dropUntil y hy_rs).support :=
    Walk.support_takeUntil_subset (rs.dropUntil y hy_rs) ha_tail hr_mid
  have hyx : y ≠ x := by
    intro hyx_eq
    exact hx_rs (by simpa [hyx_eq] using hy_rs)
  have hrx : r ≠ x := by
    intro hrx_eq
    exact hr_not_left (by simpa [hrx_eq] using hx_left)
  have hra : r ≠ a := by
    intro hra_eq
    exact ha_not_right (by simpa [hra_eq] using hr_right)
  have ha_not_prefix_r :
      a ∉ ((rs.dropUntil y hy_rs).takeUntil r hr_tail_y).support :=
    not_mem_takeUntil_later_of_mem_takeUntil_of_support
      (G := G) (p := rs.dropUntil y hy_rs)
      (x := a) (z := r) ha_tail hr_tail_y hr_mid hra
  have hmiddle_guard :
      ∀ q : α, q ≠ v →
        q ∈
          (((((pair.2 : G.Walk v t).takeUntil x hx_right).append
            ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath) :
              G.Walk v s).support →
        q ∈ ((rs.dropUntil y hy_rs).takeUntil r hr_tail_y).support →
        q ∈ (pair.1 : G.Walk v s).support ∧
          q ∈ (pair.2 : G.Walk v t).support := by
    intro q hqv hq_swap hq_mid_yr
    by_cases hq_common :
        q ∈ (pair.1 : G.Walk v s).support ∧
          q ∈ (pair.2 : G.Walk v t).support
    · exact hq_common
    · have hq_prefix_a_base :
          q ∈ ((rs.dropUntil y hy_rs).takeUntil a ha_tail).support :=
        mem_takeUntil_of_mem_takeUntil_of_mem_takeUntil
          (G := G) (p := rs.dropUntil y hy_rs)
          (x := a) (y := r) (z := q)
          ha_tail hr_tail_y hr_mid hq_mid_yr
      have hq_prefix_a_full :
          q ∈
            (((rs.dropUntil y hy_rs).takeUntil z hz_tail).takeUntil a
              ha_mid).support := by
        simpa [Walk.takeUntil_takeUntil] using hq_prefix_a_base
      have hqa : q = a :=
        hfirst_bridge_bad q hqv hq_swap hq_common hq_prefix_a_full
      exact False.elim (ha_not_prefix_r (by simpa [hqa] using hq_mid_yr))
  exact terminal_set_fan_two_sided_bridge_commonCard_lt_of_middle_guard
    (G := G) (v := v) (s := s) (t := t)
    (x := x) (y := y) (z := r)
    (pair := pair) (rs := rs)
    hx_left hx_right hxv hx_rs hy_left hy_rs hr_tail_y hr_right
    hy_prefix_x hr_suffix_x hyx hrx hmiddle_guard

private lemma mem_dropUntil_of_mem_dropUntil_of_mem_takeUntil_ne
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v t x y z : α}
    {p : G.Walk v t} (hp : p.IsPath)
    (hx : x ∈ p.support) (hy : y ∈ p.support) (hz : z ∈ p.support)
    (hz_after_x : z ∈ (p.dropUntil x hx).support)
    (hz_prefix_y : z ∈ (p.takeUntil y hy).support)
    (hzy : z ≠ y) :
    y ∈ (p.dropUntil x hx).support := by
  have hy_after_z :
      y ∈ (p.dropUntil z hz).support :=
    mem_dropUntil_of_mem_takeUntil_ne
      (G := G) p hz hy hz_prefix_y hzy
  exact mem_dropUntil_of_mem_dropUntil_of_mem_dropUntil
    (G := G) (p := p) hp hx hz hz_after_x hy_after_z

private lemma exists_last_mem_support_forall_mem_dropUntil_imp_eq
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v t : α}
    (p : G.Walk v t) (hp : p.IsPath)
    (S : Finset α)
    (hnonempty : {y ∈ S | y ∈ p.support}.Nonempty) :
    ∃ z : α, z ∈ S ∧ ∃ hzsup : z ∈ p.support,
      ∀ y : α, y ∈ S → y ∈ (p.dropUntil z hzsup).support → y = z := by
  classical
  let T : Finset α := {y ∈ S | y ∈ p.support}
  let pos : α → ℕ := fun y =>
    if hy : y ∈ p.support then (p.takeUntil y hy).length else 0
  rcases T.exists_maximalFor pos (by simpa [T] using hnonempty) with
    ⟨z, hzT, hzmax⟩
  have hzS : z ∈ S := by
    simpa [T] using (Finset.mem_filter.mp hzT).1
  have hzsup : z ∈ p.support := by
    simpa [T] using (Finset.mem_filter.mp hzT).2
  refine ⟨z, hzS, hzsup, ?_⟩
  intro y hyS hydrop
  have hysup : y ∈ p.support :=
    Walk.support_dropUntil_subset p hzsup hydrop
  have hyT : y ∈ T := by
    simp [T, hyS, hysup]
  rcases exists_index_of_mem_dropUntil (G := G) p hzsup hydrop with
    ⟨i, hz_len_le_i, hi_le, hi_get⟩
  have hy_len_eq_i : (p.takeUntil y hysup).length = i := by
    have hy_len_le : (p.takeUntil y hysup).length ≤ p.length :=
      p.length_takeUntil_le hysup
    have hget_y : p.getVert (p.takeUntil y hysup).length = y :=
      p.getVert_length_takeUntil hysup
    exact hp.getVert_injOn
      (by simpa using hy_len_le) (by simpa using hi_le)
      (by simpa [hget_y, hi_get])
  have hz_len_le_y :
      (p.takeUntil z hzsup).length ≤
        (p.takeUntil y hysup).length := by
    simpa [hy_len_eq_i] using hz_len_le_i
  have hpos_le : pos z ≤ pos y := by
    simpa [pos, hzsup, hysup] using hz_len_le_y
  have hy_len_le_z :
      (p.takeUntil y hysup).length ≤
        (p.takeUntil z hzsup).length := by
    simpa [pos, hzsup, hysup] using hzmax hyT hpos_le
  have hlen_eq :
      (p.takeUntil y hysup).length =
        (p.takeUntil z hzsup).length :=
    le_antisymm hy_len_le_z hz_len_le_y
  calc
    y = p.getVert (p.takeUntil y hysup).length :=
      (p.getVert_length_takeUntil hysup).symm
    _ = p.getVert (p.takeUntil z hzsup).length := by
      rw [hlen_eq]
    _ = z := p.getVert_length_takeUntil hzsup

lemma not_mem_dropUntil_of_mem_dropUntil_reverse_on_isPath
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v t x w : α}
    (p : G.Walk v t)
    (hpPath : p.IsPath)
    (hx : x ∈ p.support)
    (hw : w ∈ p.support)
    (hxw : x ≠ w)
    (hw_after_x : w ∈ (p.dropUntil x hx).support) :
    x ∉ (p.dropUntil w hw).support := by
  intro hx_after_w
  exact not_both_mem_dropUntil_on_simple_path
    (G := G) (p := p) hpPath hx hw hx_after_w hw_after_x hxw

private lemma exists_last_bad_pivot_on_rs
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hrsPath : rs.IsPath)
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hbad_exists :
      let altRight : G.Path v t :=
        (((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
      ∃ z : α, z ∈ rs.support ∧ z ≠ v ∧
        z ∈ (altRight : G.Walk v t).support ∧
        ¬ (z ∈ (pair.1 : G.Walk v s).support ∧
           z ∈ (pair.2 : G.Walk v t).support ∧ z ≠ x)) :
    let altRight : G.Path v t :=
      (((pair.1 : G.Walk v s).takeUntil x hx_left).append
        ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
    ∃ z : α, ∃ hzrs : z ∈ rs.support,
      z ≠ v ∧
      z ∈ (altRight : G.Walk v t).support ∧
      ¬ (z ∈ (pair.1 : G.Walk v s).support ∧
         z ∈ (pair.2 : G.Walk v t).support ∧ z ≠ x) ∧
      ∀ y : α,
        y ∈ rs.support →
        y ≠ v →
        y ∈ (altRight : G.Walk v t).support →
        ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
           y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x) →
        y ∈ (rs.dropUntil z hzrs).support →
        y = z := by
  classical
  dsimp at hbad_exists ⊢
  let altRight : G.Path v t :=
    (((pair.1 : G.Walk v s).takeUntil x hx_left).append
      ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
  let S : Finset α :=
    Finset.univ.filter fun y =>
      y ≠ v ∧
      y ∈ (altRight : G.Walk v t).support ∧
      ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
         y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x)
  have hnonempty : {y ∈ S | y ∈ rs.support}.Nonempty := by
    rcases hbad_exists with ⟨z, hzrs, hzv, hz_alt, hbad⟩
    refine ⟨z, ?_⟩
    rw [Finset.mem_filter]
    exact ⟨by
      rw [Finset.mem_filter]
      exact ⟨by simp, hzv, by simpa [altRight] using hz_alt, hbad⟩,
      hzrs⟩
  rcases exists_last_mem_support_forall_mem_dropUntil_imp_eq
      (G := G) rs hrsPath S hnonempty with
    ⟨z, hzS, hzrs, hlast⟩
  have hzv : z ≠ v := by
    simpa [S] using (Finset.mem_filter.mp hzS).2.1
  have hz_alt : z ∈ (altRight : G.Walk v t).support := by
    simpa [S] using (Finset.mem_filter.mp hzS).2.2.1
  have hbad :
      ¬ (z ∈ (pair.1 : G.Walk v s).support ∧
         z ∈ (pair.2 : G.Walk v t).support ∧ z ≠ x) := by
    simpa [S] using (Finset.mem_filter.mp hzS).2.2.2
  refine ⟨z, hzrs, hzv, hz_alt, hbad, ?_⟩
  intro y hyr hyv hy_alt hybad hydrop
  have hyS : y ∈ S := by
    rw [Finset.mem_filter]
    exact ⟨by simp, hyv, by simpa [altRight] using hy_alt, hybad⟩
  exact hlast y hyS hydrop

private lemma exists_first_bad_pivot_on_rs
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hbad_exists :
      let altRight : G.Path v t :=
        (((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
      ∃ z : α, z ∈ rs.support ∧ z ≠ v ∧
        z ∈ (altRight : G.Walk v t).support ∧
        ¬ (z ∈ (pair.1 : G.Walk v s).support ∧
           z ∈ (pair.2 : G.Walk v t).support ∧ z ≠ x)) :
    let altRight : G.Path v t :=
      (((pair.1 : G.Walk v s).takeUntil x hx_left).append
        ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
    ∃ z : α, ∃ hzrs : z ∈ rs.support,
      z ≠ v ∧
      z ∈ (altRight : G.Walk v t).support ∧
      ¬ (z ∈ (pair.1 : G.Walk v s).support ∧
         z ∈ (pair.2 : G.Walk v t).support ∧ z ≠ x) ∧
      ∀ y : α,
        y ≠ v →
        y ∈ (altRight : G.Walk v t).support →
        ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
           y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x) →
        y ∈ (rs.takeUntil z hzrs).support →
        y = z := by
  classical
  dsimp at hbad_exists ⊢
  let altRight : G.Path v t :=
    (((pair.1 : G.Walk v s).takeUntil x hx_left).append
      ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
  let S : Finset α :=
    Finset.univ.filter fun y =>
      y ≠ v ∧
      y ∈ (altRight : G.Walk v t).support ∧
      ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
         y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x)
  have hnonempty : {y ∈ S | y ∈ rs.support}.Nonempty := by
    rcases hbad_exists with ⟨z, hzrs, hzv, hz_alt, hbad⟩
    refine ⟨z, ?_⟩
    rw [Finset.mem_filter]
    exact ⟨by
      rw [Finset.mem_filter]
      exact ⟨by simp, hzv, by simpa [altRight] using hz_alt, hbad⟩,
      hzrs⟩
  rcases exists_first_mem_support_forall_mem_takeUntil_imp_eq
      (G := G) rs S hnonempty with
    ⟨z, hzS, hzrs, hfirst⟩
  have hzv : z ≠ v := by
    simpa [S] using (Finset.mem_filter.mp hzS).2.1
  have hz_alt : z ∈ (altRight : G.Walk v t).support := by
    simpa [S] using (Finset.mem_filter.mp hzS).2.2.1
  have hbad :
      ¬ (z ∈ (pair.1 : G.Walk v s).support ∧
         z ∈ (pair.2 : G.Walk v t).support ∧ z ≠ x) := by
    simpa [S] using (Finset.mem_filter.mp hzS).2.2.2
  refine ⟨z, hzrs, hzv, hz_alt, hbad, ?_⟩
  intro y hyv hy_alt hybad hyprefix
  have hyS : y ∈ S := by
    rw [Finset.mem_filter]
    exact ⟨by simp, hyv, by simpa [altRight] using hy_alt, hybad⟩
  exact hfirst y hyS hyprefix

private lemma not_mem_altRight_of_first_bad_right_only_prefix_left_only
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x z y : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    {hzrs : z ∈ rs.support}
    (hz_not_left : z ∉ (pair.1 : G.Walk v s).support)
    (hfirst_bad :
      let altRight : G.Path v t :=
        (((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
      ∀ y : α, y ≠ v →
        y ∈ (altRight : G.Walk v t).support →
        ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
           y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x) →
        y ∈ (rs.takeUntil z hzrs).support →
        y = z)
    (hyv : y ≠ v)
    (hy_prefix_z : y ∈ (rs.takeUntil z hzrs).support)
    (hy_left : y ∈ (pair.1 : G.Walk v s).support)
    (hy_not_right : y ∉ (pair.2 : G.Walk v t).support) :
    y ∉
      ((((pair.1 : G.Walk v s).takeUntil x hx_left).append
        ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath :
          G.Walk v t).support := by
  intro hy_alt
  dsimp at hfirst_bad
  let altRight : G.Path v t :=
    (((pair.1 : G.Walk v s).takeUntil x hx_left).append
      ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
  have hy_bad :
      ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
         y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x) := by
    intro hy_common
    exact hy_not_right hy_common.2.1
  have hy_eq_z : y = z :=
    hfirst_bad y hyv (by simpa [altRight] using hy_alt) hy_bad hy_prefix_z
  exact hz_not_left (by simpa [hy_eq_z] using hy_left)

private lemma not_mem_altRight_of_first_bad_right_only_before_pivot_left_only
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x z y : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hrsPath : rs.IsPath)
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    {hzrs : z ∈ rs.support}
    (hz_not_left : z ∉ (pair.1 : G.Walk v s).support)
    (hfirst_bad :
      let altRight : G.Path v t :=
        (((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
      ∀ y : α, y ≠ v →
        y ∈ (altRight : G.Walk v t).support →
        ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
           y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x) →
        y ∈ (rs.takeUntil z hzrs).support →
        y = z)
    (hy_rs : y ∈ rs.support)
    (hz_after_y : z ∈ (rs.dropUntil y hy_rs).support)
    (hyz : y ≠ z)
    (hyv : y ≠ v)
    (hy_left : y ∈ (pair.1 : G.Walk v s).support)
    (hy_not_right : y ∉ (pair.2 : G.Walk v t).support) :
    y ∉
      ((((pair.1 : G.Walk v s).takeUntil x hx_left).append
        ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath :
          G.Walk v t).support := by
  have hy_prefix_z :
      y ∈ (rs.takeUntil z hzrs).support :=
    mem_takeUntil_of_mem_dropUntil_ne_on_isPath
      (G := G) (p := rs) hrsPath hy_rs hzrs hz_after_y hyz
  exact
    not_mem_altRight_of_first_bad_right_only_prefix_left_only
      (G := G) (v := v) (s := s) (t := t) (x := x)
      (z := z) (y := y) (pair := pair) (rs := rs)
      hx_left hx_right hz_not_left hfirst_bad hyv hy_prefix_z
      hy_left hy_not_right

private lemma exists_first_noncommon_old_residual_on_rs
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x w : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hres_exists :
      ∃ z : α, z ∈ rs.support ∧ z ≠ v ∧ z ≠ w ∧
        (z ∈ (pair.1 : G.Walk v s).support ∨
          z ∈ (pair.2 : G.Walk v t).support) ∧
        ¬ (z ∈ (pair.1 : G.Walk v s).support ∧
           z ∈ (pair.2 : G.Walk v t).support ∧ z ≠ x)) :
    ∃ z : α, ∃ hzrs : z ∈ rs.support,
      z ≠ v ∧ z ≠ w ∧
      (z ∈ (pair.1 : G.Walk v s).support ∨
        z ∈ (pair.2 : G.Walk v t).support) ∧
      ¬ (z ∈ (pair.1 : G.Walk v s).support ∧
         z ∈ (pair.2 : G.Walk v t).support ∧ z ≠ x) ∧
      ∀ y : α,
        y ≠ v →
        y ≠ w →
        (y ∈ (pair.1 : G.Walk v s).support ∨
          y ∈ (pair.2 : G.Walk v t).support) →
        ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
           y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x) →
        y ∈ (rs.takeUntil z hzrs).support →
        y = z := by
  classical
  let S : Finset α :=
    Finset.univ.filter fun y =>
      y ≠ v ∧ y ≠ w ∧
      (y ∈ (pair.1 : G.Walk v s).support ∨
        y ∈ (pair.2 : G.Walk v t).support) ∧
      ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
         y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x)
  have hnonempty : {y ∈ S | y ∈ rs.support}.Nonempty := by
    rcases hres_exists with ⟨z, hzrs, hzv, hzw, hz_old, hz_bad⟩
    refine ⟨z, ?_⟩
    rw [Finset.mem_filter]
    exact ⟨by
      rw [Finset.mem_filter]
      exact ⟨by simp, hzv, hzw, hz_old, hz_bad⟩,
      hzrs⟩
  rcases exists_first_mem_support_forall_mem_takeUntil_imp_eq
      (G := G) rs S hnonempty with
    ⟨z, hzS, hzrs, hfirst⟩
  have hzv : z ≠ v := by
    simpa [S] using (Finset.mem_filter.mp hzS).2.1
  have hzw : z ≠ w := by
    simpa [S] using (Finset.mem_filter.mp hzS).2.2.1
  have hz_old :
      z ∈ (pair.1 : G.Walk v s).support ∨
        z ∈ (pair.2 : G.Walk v t).support := by
    simpa [S] using (Finset.mem_filter.mp hzS).2.2.2.1
  have hz_bad :
      ¬ (z ∈ (pair.1 : G.Walk v s).support ∧
         z ∈ (pair.2 : G.Walk v t).support ∧ z ≠ x) := by
    simpa [S] using (Finset.mem_filter.mp hzS).2.2.2.2
  refine ⟨z, hzrs, hzv, hzw, hz_old, hz_bad, ?_⟩
  intro y hyv hyw hy_old hy_bad hyprefix
  have hyS : y ∈ S := by
    rw [Finset.mem_filter]
    exact ⟨by simp, hyv, hyw, hy_old, hy_bad⟩
  exact hfirst y hyS hyprefix

private lemma exists_first_noncommon_old_residual_on_rs_dropUntil
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x w y : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hy_rs : y ∈ rs.support)
    (hres_exists :
      ∃ z : α, z ∈ (rs.dropUntil y hy_rs).support ∧
        z ≠ v ∧ z ≠ y ∧ z ≠ w ∧
        (z ∈ (pair.1 : G.Walk v s).support ∨
          z ∈ (pair.2 : G.Walk v t).support) ∧
        ¬ (z ∈ (pair.1 : G.Walk v s).support ∧
           z ∈ (pair.2 : G.Walk v t).support ∧ z ≠ x)) :
    ∃ z : α, ∃ hz_tail : z ∈ (rs.dropUntil y hy_rs).support,
      z ∈ rs.support ∧
      z ≠ v ∧ z ≠ y ∧ z ≠ w ∧
      (z ∈ (pair.1 : G.Walk v s).support ∨
        z ∈ (pair.2 : G.Walk v t).support) ∧
      ¬ (z ∈ (pair.1 : G.Walk v s).support ∧
         z ∈ (pair.2 : G.Walk v t).support ∧ z ≠ x) ∧
      ∀ a : α,
        a ≠ v →
        a ≠ y →
        a ≠ w →
        (a ∈ (pair.1 : G.Walk v s).support ∨
          a ∈ (pair.2 : G.Walk v t).support) →
        ¬ (a ∈ (pair.1 : G.Walk v s).support ∧
           a ∈ (pair.2 : G.Walk v t).support ∧ a ≠ x) →
        a ∈ ((rs.dropUntil y hy_rs).takeUntil z hz_tail).support →
        a = z := by
  classical
  let tail : G.Walk y s := rs.dropUntil y hy_rs
  let S : Finset α :=
    Finset.univ.filter fun a =>
      a ≠ v ∧ a ≠ y ∧ a ≠ w ∧
      (a ∈ (pair.1 : G.Walk v s).support ∨
        a ∈ (pair.2 : G.Walk v t).support) ∧
      ¬ (a ∈ (pair.1 : G.Walk v s).support ∧
         a ∈ (pair.2 : G.Walk v t).support ∧ a ≠ x)
  have hnonempty : {a ∈ S | a ∈ tail.support}.Nonempty := by
    rcases hres_exists with ⟨z, hz_tail, hzv, hzy, hzw, hz_old, hz_bad⟩
    refine ⟨z, ?_⟩
    rw [Finset.mem_filter]
    exact ⟨by
      rw [Finset.mem_filter]
      exact ⟨by simp, hzv, hzy, hzw, hz_old, hz_bad⟩,
      by simpa [tail] using hz_tail⟩
  rcases exists_first_mem_support_forall_mem_takeUntil_imp_eq
      (G := G) tail S hnonempty with
    ⟨z, hzS, hz_tail, hfirst⟩
  have hzv : z ≠ v := by
    simpa [S] using (Finset.mem_filter.mp hzS).2.1
  have hzy : z ≠ y := by
    simpa [S] using (Finset.mem_filter.mp hzS).2.2.1
  have hzw : z ≠ w := by
    simpa [S] using (Finset.mem_filter.mp hzS).2.2.2.1
  have hz_old :
      z ∈ (pair.1 : G.Walk v s).support ∨
        z ∈ (pair.2 : G.Walk v t).support := by
    simpa [S] using (Finset.mem_filter.mp hzS).2.2.2.2.1
  have hz_bad :
      ¬ (z ∈ (pair.1 : G.Walk v s).support ∧
         z ∈ (pair.2 : G.Walk v t).support ∧ z ≠ x) := by
    simpa [S] using (Finset.mem_filter.mp hzS).2.2.2.2.2
  have hz_rs : z ∈ rs.support := by
    exact Walk.support_dropUntil_subset rs hy_rs (by simpa [tail] using hz_tail)
  refine ⟨z, by simpa [tail] using hz_tail, hz_rs, hzv, hzy, hzw,
    hz_old, hz_bad, ?_⟩
  intro a hav hay haw ha_old ha_bad ha_prefix
  have haS : a ∈ S := by
    rw [Finset.mem_filter]
    exact ⟨by simp, hav, hay, haw, ha_old, ha_bad⟩
  exact hfirst a haS (by simpa [tail] using ha_prefix)

private lemma exists_first_noncommon_old_residual_not_left_prefix_on_rs_dropUntil
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x w y : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hy_rs : y ∈ rs.support)
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hres_exists :
      ∃ z : α, z ∈ (rs.dropUntil y hy_rs).support ∧
        z ≠ v ∧ z ≠ y ∧ z ≠ w ∧
        (z ∈ (pair.1 : G.Walk v s).support ∨
          z ∈ (pair.2 : G.Walk v t).support) ∧
        ¬ (z ∈ (pair.1 : G.Walk v s).support ∧
           z ∈ (pair.2 : G.Walk v t).support ∧ z ≠ x) ∧
        z ∉ ((pair.1 : G.Walk v s).takeUntil x hx_left).support) :
    ∃ z : α, ∃ hz_tail : z ∈ (rs.dropUntil y hy_rs).support,
      z ∈ rs.support ∧
      z ≠ v ∧ z ≠ y ∧ z ≠ w ∧
      (z ∈ (pair.1 : G.Walk v s).support ∨
        z ∈ (pair.2 : G.Walk v t).support) ∧
      ¬ (z ∈ (pair.1 : G.Walk v s).support ∧
         z ∈ (pair.2 : G.Walk v t).support ∧ z ≠ x) ∧
      z ∉ ((pair.1 : G.Walk v s).takeUntil x hx_left).support ∧
      ∀ a : α,
        a ≠ v →
        a ≠ y →
        a ≠ w →
        (a ∈ (pair.1 : G.Walk v s).support ∨
          a ∈ (pair.2 : G.Walk v t).support) →
        ¬ (a ∈ (pair.1 : G.Walk v s).support ∧
           a ∈ (pair.2 : G.Walk v t).support ∧ a ≠ x) →
        a ∉ ((pair.1 : G.Walk v s).takeUntil x hx_left).support →
        a ∈ ((rs.dropUntil y hy_rs).takeUntil z hz_tail).support →
        a = z := by
  classical
  let tail : G.Walk y s := rs.dropUntil y hy_rs
  let S : Finset α :=
    Finset.univ.filter fun a =>
      a ≠ v ∧ a ≠ y ∧ a ≠ w ∧
      (a ∈ (pair.1 : G.Walk v s).support ∨
        a ∈ (pair.2 : G.Walk v t).support) ∧
      ¬ (a ∈ (pair.1 : G.Walk v s).support ∧
         a ∈ (pair.2 : G.Walk v t).support ∧ a ≠ x) ∧
      a ∉ ((pair.1 : G.Walk v s).takeUntil x hx_left).support
  have hnonempty : {a ∈ S | a ∈ tail.support}.Nonempty := by
    rcases hres_exists with
      ⟨z, hz_tail, hzv, hzy, hzw, hz_old, hz_bad, hz_not_left_prefix⟩
    refine ⟨z, ?_⟩
    rw [Finset.mem_filter]
    exact ⟨by
      rw [Finset.mem_filter]
      exact
        ⟨by simp, hzv, hzy, hzw, hz_old, hz_bad,
          hz_not_left_prefix⟩,
      by simpa [tail] using hz_tail⟩
  rcases exists_first_mem_support_forall_mem_takeUntil_imp_eq
      (G := G) tail S hnonempty with
    ⟨z, hzS, hz_tail, hfirst⟩
  have hzv : z ≠ v := by
    simpa [S] using (Finset.mem_filter.mp hzS).2.1
  have hzy : z ≠ y := by
    simpa [S] using (Finset.mem_filter.mp hzS).2.2.1
  have hzw : z ≠ w := by
    simpa [S] using (Finset.mem_filter.mp hzS).2.2.2.1
  have hz_old :
      z ∈ (pair.1 : G.Walk v s).support ∨
        z ∈ (pair.2 : G.Walk v t).support := by
    simpa [S] using (Finset.mem_filter.mp hzS).2.2.2.2.1
  have hz_bad :
      ¬ (z ∈ (pair.1 : G.Walk v s).support ∧
         z ∈ (pair.2 : G.Walk v t).support ∧ z ≠ x) := by
    simpa [S] using (Finset.mem_filter.mp hzS).2.2.2.2.2.1
  have hz_not_left_prefix :
      z ∉ ((pair.1 : G.Walk v s).takeUntil x hx_left).support := by
    simpa [S] using (Finset.mem_filter.mp hzS).2.2.2.2.2.2
  have hz_rs : z ∈ rs.support := by
    exact Walk.support_dropUntil_subset rs hy_rs (by simpa [tail] using hz_tail)
  refine ⟨z, by simpa [tail] using hz_tail, hz_rs, hzv, hzy, hzw,
    hz_old, hz_bad, hz_not_left_prefix, ?_⟩
  intro a hav hay haw ha_old ha_bad ha_not_left_prefix ha_prefix
  have haS : a ∈ S := by
    rw [Finset.mem_filter]
    exact
      ⟨by simp, hav, hay, haw, ha_old, ha_bad, ha_not_left_prefix⟩
  exact hfirst a haS (by simpa [tail] using ha_prefix)

private lemma exists_next_noncommon_old_residual_after_left_of_later_right_only
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x w y z : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hy_rs : y ∈ rs.support)
    (hy_left : y ∈ (pair.1 : G.Walk v s).support)
    (hzrs : z ∈ rs.support)
    (hy_prefix_z : y ∈ (rs.takeUntil z hzrs).support)
    (hzv : z ≠ v)
    (hzw : z ≠ w)
    (hz_right : z ∈ (pair.2 : G.Walk v t).support)
    (hz_not_left : z ∉ (pair.1 : G.Walk v s).support) :
    ∃ a : α, a ∈ (rs.dropUntil y hy_rs).support ∧
      a ≠ v ∧ a ≠ y ∧ a ≠ w ∧
      (a ∈ (pair.1 : G.Walk v s).support ∨
        a ∈ (pair.2 : G.Walk v t).support) ∧
      ¬ (a ∈ (pair.1 : G.Walk v s).support ∧
         a ∈ (pair.2 : G.Walk v t).support ∧ a ≠ x) := by
  have hzy : z ≠ y := by
    intro hzy_eq
    exact hz_not_left (by simpa [hzy_eq] using hy_left)
  have hz_after_y : z ∈ (rs.dropUntil y hy_rs).support :=
    mem_dropUntil_of_mem_takeUntil_ne
      (G := G) rs hy_rs hzrs hy_prefix_z hzy.symm
  refine ⟨z, hz_after_y, hzv, hzy, hzw, Or.inr hz_right, ?_⟩
  intro hz_common
  exact hz_not_left hz_common.1

private lemma terminal_set_fan_left_suffix_retention_left_prefix_residual_bad_false_of_altRight
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x z y : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hzrs : z ∈ rs.support)
    (hz_not_right : z ∉ (pair.2 : G.Walk v t).support)
    (hlast_bad :
      let altRight : G.Path v t :=
        (((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
      ∀ y : α, y ∈ rs.support → y ≠ v →
        y ∈ (altRight : G.Walk v t).support →
        ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
           y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x) →
        y ∈ (rs.dropUntil z hzrs).support →
        y = z)
    (hyv : y ≠ v)
    (hy_drop : y ∈ (rs.dropUntil z hzrs).support)
    (hy_right : y ∈ (pair.2 : G.Walk v t).support)
    (hy_alt :
      y ∈
        ((((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath :
            G.Walk v t).support)
    (hy_new_bad :
      ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
         y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x)) :
    False := by
  classical
  dsimp at hlast_bad
  let altRight : G.Path v t :=
    (((pair.1 : G.Walk v s).takeUntil x hx_left).append
      ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
  have hy_rs : y ∈ rs.support :=
    Walk.support_dropUntil_subset rs hzrs hy_drop
  have hy_eq_z : y = z :=
    hlast_bad y hy_rs hyv (by simpa [altRight] using hy_alt)
      hy_new_bad hy_drop
  exact hz_not_right (by simpa [hy_eq_z] using hy_right)

private lemma terminal_set_fan_left_suffix_retention_right_suffix_residual_bad_false_of_altRight
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x z y : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hzrs : z ∈ rs.support)
    (hz_not_left : z ∉ (pair.1 : G.Walk v s).support)
    (hfirst_bad :
      let altRight : G.Path v t :=
        (((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
      ∀ y : α, y ≠ v →
        y ∈ (altRight : G.Walk v t).support →
        ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
           y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x) →
        y ∈ (rs.takeUntil z hzrs).support →
        y = z)
    (hyv : y ≠ v)
    (hy_prefix : y ∈ (rs.takeUntil z hzrs).support)
    (hy_left : y ∈ (pair.1 : G.Walk v s).support)
    (hy_alt :
      y ∈
        ((((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath :
            G.Walk v t).support)
    (hy_new_bad :
      ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
         y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x)) :
    False := by
  classical
  dsimp at hfirst_bad
  let altRight : G.Path v t :=
    (((pair.1 : G.Walk v s).takeUntil x hx_left).append
      ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
  have hy_eq_z : y = z :=
    hfirst_bad y hyv (by simpa [altRight] using hy_alt)
      hy_new_bad hy_prefix
  exact hz_not_left (by simpa [hy_eq_z] using hy_left)

private lemma mem_left_takeUntil_of_left_not_right_and_mem_altRight
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x y : α}
    (left : G.Walk v s) (right : G.Walk v t)
    (hx_left : x ∈ left.support)
    (hx_right : x ∈ right.support)
    (hy_not_right : y ∉ right.support)
    (hy_alt :
      y ∈ (((left.takeUntil x hx_left).append
        (right.dropUntil x hx_right)).toPath : G.Walk v t).support) :
    y ∈ (left.takeUntil x hx_left).support := by
  have hy_raw :
      y ∈ ((left.takeUntil x hx_left).append
        (right.dropUntil x hx_right)).support :=
    Walk.support_toPath_subset _ hy_alt
  rw [Walk.mem_support_append_iff] at hy_raw
  rcases hy_raw with hy_prefix | hy_suffix
  · exact hy_prefix
  · exact False.elim
      (hy_not_right
        (Walk.support_dropUntil_subset right hx_right hy_suffix))

private lemma not_mem_left_prefix_fallback_of_not_right_suffix
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x y : α}
    (right : G.Walk v t) (rs : G.Walk v s)
    (hx_right : x ∈ right.support)
    (hy_right : y ∈ right.support)
    (hy_rs : y ∈ rs.support)
    (hx_rs : x ∉ rs.support)
    (hy_not_suffix : y ∉ (right.dropUntil x hx_right).support) :
    x ∉
      ((((right.takeUntil y hy_right).append
        (rs.dropUntil y hy_rs)).toPath) : G.Walk v s).support := by
  intro hx_fallback
  have hx_raw :
      x ∈ ((right.takeUntil y hy_right).append
        (rs.dropUntil y hy_rs)).support :=
    Walk.support_toPath_subset _ hx_fallback
  rw [Walk.mem_support_append_iff] at hx_raw
  rcases hx_raw with hx_prefix | hx_drop
  · have hxy : x ≠ y := by
      intro hxy_eq
      exact hx_rs (by simpa [hxy_eq] using hy_rs)
    exact hy_not_suffix
      (mem_dropUntil_of_mem_takeUntil_ne
        (G := G) right hx_right hy_right hx_prefix hxy)
  · exact hx_rs (Walk.support_dropUntil_subset rs hy_rs hx_drop)

private lemma not_mem_left_suffix_fallback_of_not_left_prefix
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s x y : α}
    (left : G.Walk v s) (rs : G.Walk v s)
    (hleftPath : left.IsPath)
    (hx_left : x ∈ left.support)
    (hy_left : y ∈ left.support)
    (hy_rs : y ∈ rs.support)
    (hx_rs : x ∉ rs.support)
    (hy_not_prefix : y ∉ (left.takeUntil x hx_left).support)
    (hyx : y ≠ x) :
    x ∉
      ((((rs.takeUntil y hy_rs).append
        (left.dropUntil y hy_left)).toPath) : G.Walk v s).support := by
  intro hx_fallback
  have hx_raw :
      x ∈ ((rs.takeUntil y hy_rs).append
        (left.dropUntil y hy_left)).support :=
    Walk.support_toPath_subset _ hx_fallback
  rw [Walk.mem_support_append_iff] at hx_raw
  rcases hx_raw with hx_prefix | hx_drop
  · exact hx_rs (Walk.support_takeUntil_subset rs hy_rs hx_prefix)
  · have hy_after_x : y ∈ (left.dropUntil x hx_left).support :=
      mem_dropUntil_of_mem_support_not_takeUntil
        (G := G) left hx_left hy_left hy_not_prefix
    exact not_both_mem_dropUntil_on_simple_path
      (G := G) (p := left) hleftPath hx_left hy_left
      hx_drop hy_after_x hyx.symm

private lemma terminal_set_fan_first_bad_right_only_fallback_left_alt_commonCard_lt
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x z y : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (_hrsPath : rs.IsPath)
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rs : x ∉ rs.support)
    (hzrs : z ∈ rs.support)
    (_hz_right : z ∈ (pair.2 : G.Walk v t).support)
    (hz_not_left : z ∉ (pair.1 : G.Walk v s).support)
    (hfirst_bad :
      let altRight : G.Path v t :=
        (((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
      ∀ y : α, y ≠ v →
        y ∈ (altRight : G.Walk v t).support →
        ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
           y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x) →
        y ∈ (rs.takeUntil z hzrs).support →
        y = z)
    (hy_rs : y ∈ rs.support)
    (hy_prefix_z : y ∈ (rs.takeUntil z hzrs).support)
    (hy_left : y ∈ (pair.1 : G.Walk v s).support)
    (_hy_not_right : y ∉ (pair.2 : G.Walk v t).support)
    (hy_not_left_prefix :
      y ∉ ((pair.1 : G.Walk v s).takeUntil x hx_left).support) :
    ∃ pair' : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  classical
  let fallbackLeft : G.Path v s :=
    (((rs.takeUntil y hy_rs).append
      ((pair.1 : G.Walk v s).dropUntil y hy_left)).toPath)
  let altRight : G.Path v t :=
    (((pair.1 : G.Walk v s).takeUntil x hx_left).append
      ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
  let fallbackPair : G.Path v s × G.Path v t := (fallbackLeft, altRight)
  refine ⟨fallbackPair, ?_⟩
  have hy_ne_x : y ≠ x := by
    intro hyx
    exact hx_rs (by simpa [hyx] using hy_rs)
  have hy_ne_z : y ≠ z := by
    intro hyz
    exact hz_not_left (by simpa [hyz] using hy_left)
  have hz_not_prefix_y :
      z ∉ (rs.takeUntil y hy_rs).support :=
    not_mem_takeUntil_later_of_mem_takeUntil_of_support
      (G := G) (p := rs) hzrs hy_rs hy_prefix_z hy_ne_z
  have hx_not_fallbackLeft :
      x ∉ (fallbackLeft : G.Walk v s).support := by
    simpa [fallbackLeft] using
      (not_mem_left_suffix_fallback_of_not_left_prefix
        (G := G) (left := (pair.1 : G.Walk v s)) (rs := rs)
        pair.1.property hx_left hy_left hy_rs hx_rs
        hy_not_left_prefix hy_ne_x)
  have hcommon_subset_old_without_x :
      (((fallbackLeft : G.Walk v s).support.toFinset ∩
          (altRight : G.Walk v t).support.toFinset).erase v) ⊆
        (((pair.1 : G.Walk v s).support.toFinset ∩
          (pair.2 : G.Walk v t).support.toFinset).erase v).erase x := by
    intro q hq
    rw [Finset.mem_erase, Finset.mem_inter] at hq
    rcases hq with ⟨hqv, hq_fallback, hq_alt⟩
    have hq_fallback_walk : q ∈ (fallbackLeft : G.Walk v s).support := by
      simpa using hq_fallback
    have hq_alt_walk : q ∈ (altRight : G.Walk v t).support := by
      simpa using hq_alt
    have hqx : q ≠ x := by
      intro hqx
      exact hx_not_fallbackLeft (by simpa [hqx] using hq_fallback_walk)
    have hq_fallback_raw :
        q ∈ ((rs.takeUntil y hy_rs).append
          ((pair.1 : G.Walk v s).dropUntil y hy_left)).support :=
      Walk.support_toPath_subset _ hq_fallback_walk
    have hq_alt_raw :
        q ∈ (((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).support :=
      Walk.support_toPath_subset _ hq_alt_walk
    rw [Walk.mem_support_append_iff] at hq_fallback_raw
    rw [Walk.mem_support_append_iff] at hq_alt_raw
    rw [Finset.mem_erase, Finset.mem_erase, Finset.mem_inter]
    refine ⟨hqx, hqv, ?_, ?_⟩
    · rcases hq_fallback_raw with hq_rs_prefix | hq_left_suffix
      · rcases hq_alt_raw with hq_left_prefix | hq_right_suffix
        · exact
            by simpa using
              (Walk.support_takeUntil_subset (pair.1 : G.Walk v s)
                hx_left hq_left_prefix)
        · by_cases hq_left : q ∈ (pair.1 : G.Walk v s).support
          · exact by simpa using hq_left
          · have hq_right :
                q ∈ (pair.2 : G.Walk v t).support :=
              Walk.support_dropUntil_subset (pair.2 : G.Walk v t)
                hx_right hq_right_suffix
            have hq_bad :
                ¬ (q ∈ (pair.1 : G.Walk v s).support ∧
                   q ∈ (pair.2 : G.Walk v t).support ∧ q ≠ x) := by
              intro hq_common
              exact hq_left hq_common.1
            have hq_prefix_z :
                q ∈ (rs.takeUntil z hzrs).support :=
              mem_takeUntil_of_mem_takeUntil_of_mem_takeUntil
                (G := G) (p := rs) (x := z) (y := y) (z := q)
                hzrs hy_rs hy_prefix_z hq_rs_prefix
            have hq_eq_z : q = z :=
              hfirst_bad q hqv (by simpa [altRight] using hq_alt_walk)
                hq_bad hq_prefix_z
            exact False.elim
              (hz_not_prefix_y (by simpa [hq_eq_z] using hq_rs_prefix))
      · exact by
          simpa using
            (Walk.support_dropUntil_subset (pair.1 : G.Walk v s) hy_left
              hq_left_suffix)
    · rcases hq_fallback_raw with hq_rs_prefix | hq_left_suffix
      · rcases hq_alt_raw with hq_left_prefix | hq_right_suffix
        · by_cases hq_right : q ∈ (pair.2 : G.Walk v t).support
          · exact by simpa using hq_right
          · have hq_left :
                q ∈ (pair.1 : G.Walk v s).support :=
              Walk.support_takeUntil_subset (pair.1 : G.Walk v s)
                hx_left hq_left_prefix
            have hq_bad :
                ¬ (q ∈ (pair.1 : G.Walk v s).support ∧
                   q ∈ (pair.2 : G.Walk v t).support ∧ q ≠ x) := by
              intro hq_common
              exact hq_right hq_common.2.1
            have hq_prefix_z :
                q ∈ (rs.takeUntil z hzrs).support :=
              mem_takeUntil_of_mem_takeUntil_of_mem_takeUntil
                (G := G) (p := rs) (x := z) (y := y) (z := q)
                hzrs hy_rs hy_prefix_z hq_rs_prefix
            have hq_eq_z : q = z :=
              hfirst_bad q hqv (by simpa [altRight] using hq_alt_walk)
                hq_bad hq_prefix_z
            exact False.elim
              (hz_not_left (by simpa [hq_eq_z] using hq_left))
        · exact by
            simpa using
              (Walk.support_dropUntil_subset (pair.2 : G.Walk v t)
                hx_right hq_right_suffix)
      · rcases hq_alt_raw with hq_left_prefix | hq_right_suffix
        · have hq_left :
              q ∈ (pair.1 : G.Walk v s).support :=
            Walk.support_dropUntil_subset (pair.1 : G.Walk v s) hy_left
              hq_left_suffix
          have hx_after_q :
              x ∈ ((pair.1 : G.Walk v s).dropUntil q hq_left).support :=
            mem_dropUntil_of_mem_takeUntil_ne
              (G := G) (pair.1 : G.Walk v s) hq_left hx_left
              hq_left_prefix hqx
          have hy_after_x :
              y ∈ ((pair.1 : G.Walk v s).dropUntil x hx_left).support :=
            mem_dropUntil_of_mem_support_not_takeUntil
              (G := G) (pair.1 : G.Walk v s) hx_left hy_left
              hy_not_left_prefix
          have hy_after_q :
              y ∈ ((pair.1 : G.Walk v s).dropUntil q hq_left).support :=
            mem_dropUntil_of_mem_dropUntil_of_mem_dropUntil
              (G := G) (p := (pair.1 : G.Walk v s)) pair.1.property
              hq_left hx_left hx_after_q hy_after_x
          have hqy : q ≠ y := by
            intro hqy
            exact hy_not_left_prefix (by simpa [hqy] using hq_left_prefix)
          exact False.elim
            (not_both_mem_dropUntil_on_simple_path
              (G := G) (p := (pair.1 : G.Walk v s)) pair.1.property
              hq_left hy_left hq_left_suffix hy_after_q hqy)
        · exact by
            simpa using
              (Walk.support_dropUntil_subset (pair.2 : G.Walk v t)
                hx_right hq_right_suffix)
  simpa [terminalPathPairCommonCard, fallbackPair, fallbackLeft, altRight] using
    (common_support_erase_card_lt_of_subset_erase_common
      (G := G) (v := v) (s := s) (t := t)
      (qs := (pair.1 : G.Walk v s))
      (qt := (pair.2 : G.Walk v t))
      (qs' := (fallbackLeft : G.Walk v s))
      (qt' := (altRight : G.Walk v t))
      (x := x) hcommon_subset_old_without_x hx_left hx_right hxv)

private lemma false_of_first_noncommon_old_residual_and_left_prefix
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x w z y : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hzrs : z ∈ rs.support)
    (hz_not_left : z ∉ (pair.1 : G.Walk v s).support)
    (hw_not_left : w ∉ (pair.1 : G.Walk v s).support)
    (hfirst_residual :
      ∀ y : α,
        y ≠ v →
        y ≠ w →
        (y ∈ (pair.1 : G.Walk v s).support ∨
          y ∈ (pair.2 : G.Walk v t).support) →
        ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
           y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x) →
        y ∈ (rs.takeUntil z hzrs).support →
        y = z)
    (hyv : y ≠ v)
    (hy_prefix : y ∈ (rs.takeUntil z hzrs).support)
    (hy_left : y ∈ (pair.1 : G.Walk v s).support)
    (hy_new_bad :
      ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
         y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x)) :
    False := by
  have hy_ne_w : y ≠ w := by
    intro hyw
    exact hw_not_left (by simpa [hyw] using hy_left)
  have hy_eq_z : y = z :=
    hfirst_residual y hyv hy_ne_w (Or.inl hy_left) hy_new_bad hy_prefix
  exact hz_not_left (by simpa [hy_eq_z] using hy_left)

private lemma noncommon_old_residual_exclusive_side
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x z : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hx_rs : x ∉ rs.support)
    (hzrs : z ∈ rs.support)
    (hz_old :
      z ∈ (pair.1 : G.Walk v s).support ∨
        z ∈ (pair.2 : G.Walk v t).support)
    (hz_bad :
      ¬ (z ∈ (pair.1 : G.Walk v s).support ∧
         z ∈ (pair.2 : G.Walk v t).support ∧ z ≠ x)) :
    (z ∈ (pair.1 : G.Walk v s).support ∧
      z ∉ (pair.2 : G.Walk v t).support) ∨
    (z ∈ (pair.2 : G.Walk v t).support ∧
      z ∉ (pair.1 : G.Walk v s).support) := by
  have hzx : z ≠ x := by
    intro hzx_eq
    exact hx_rs (by simpa [hzx_eq] using hzrs)
  rcases hz_old with hz_left | hz_right
  · by_cases hz_right : z ∈ (pair.2 : G.Walk v t).support
    · exact False.elim (hz_bad ⟨hz_left, hz_right, hzx⟩)
    · exact Or.inl ⟨hz_left, hz_right⟩
  · by_cases hz_left : z ∈ (pair.1 : G.Walk v s).support
    · exact False.elim (hz_bad ⟨hz_left, hz_right, hzx⟩)
    · exact Or.inr ⟨hz_right, hz_left⟩

private lemma terminal_set_fan_left_suffix_retention_right_only_first_wide_residual_descent
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x w z : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rs : x ∉ rs.support)
    (hw_not_left : w ∉ (pair.1 : G.Walk v s).support)
    (hzrs : z ∈ rs.support)
    (hz_right : z ∈ (pair.2 : G.Walk v t).support)
    (hz_not_left : z ∉ (pair.1 : G.Walk v s).support)
    (hz_suffix_right :
      z ∈ ((pair.2 : G.Walk v t).dropUntil x hx_right).support)
    (hfirst_residual :
      ∀ y : α,
        y ≠ v →
        y ≠ w →
        (y ∈ (pair.1 : G.Walk v s).support ∨
          y ∈ (pair.2 : G.Walk v t).support) →
        ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
           y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x) →
        y ∈ (rs.takeUntil z hzrs).support →
        y = z) :
    ∃ pair' : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  classical
  let spliceRight : G.Path v t :=
    ((rs.takeUntil z hzrs).append
      ((pair.2 : G.Walk v t).dropUntil z hz_right)).toPath
  let spliced : G.Path v s × G.Path v t := (pair.1, spliceRight)
  refine ⟨spliced, ?_⟩
  have hx_ne_z : x ≠ z := by
    intro hxz
    exact hz_not_left (by simpa [hxz] using hx_left)
  have hx_not_spliceRight :
      x ∉ (spliceRight : G.Walk v t).support := by
    intro hx_splice
    have hx_append :
        x ∈ ((rs.takeUntil z hzrs).append
          ((pair.2 : G.Walk v t).dropUntil z hz_right)).support := by
      exact Walk.support_toPath_subset _ hx_splice
    rw [Walk.mem_support_append_iff] at hx_append
    rcases hx_append with hx_prefix | hx_drop
    · exact hx_rs (Walk.support_takeUntil_subset rs hzrs hx_prefix)
    · exact False.elim
        (not_both_mem_dropUntil_on_simple_path
          (G := G) (p := (pair.2 : G.Walk v t)) pair.2.property
          hx_right hz_right hx_drop hz_suffix_right hx_ne_z)
  have hcommon_subset_old_without_x :
      ((pair.1 : G.Walk v s).support.toFinset ∩
          (spliceRight : G.Walk v t).support.toFinset).erase v ⊆
        (((pair.1 : G.Walk v s).support.toFinset ∩
          (pair.2 : G.Walk v t).support.toFinset).erase v).erase x := by
    intro y hy
    rw [Finset.mem_erase, Finset.mem_inter] at hy
    rcases hy with ⟨hyv, hy_left, hy_splice⟩
    have hy_splice_walk : y ∈ (spliceRight : G.Walk v t).support := by
      simpa using hy_splice
    have hy_append :
        y ∈ ((rs.takeUntil z hzrs).append
          ((pair.2 : G.Walk v t).dropUntil z hz_right)).support := by
      exact Walk.support_toPath_subset _ hy_splice_walk
    rw [Walk.mem_support_append_iff] at hy_append
    rcases hy_append with hy_prefix | hy_drop
    · have hy_left_walk :
          y ∈ (pair.1 : G.Walk v s).support := by
        simpa using hy_left
      rcases mem_erase_common_without_x_or_not_common_triple_left
          (G := G) (pair := pair) (x := x) hyv hy_left_walk with
        hy_old_common | hy_new_bad
      · exact hy_old_common
      · exact False.elim
          (false_of_first_noncommon_old_residual_and_left_prefix
            (G := G) (v := v) (s := s) (t := t)
            (x := x) (w := w) (z := z) (y := y)
            (pair := pair) (rs := rs)
            hzrs hz_not_left hw_not_left hfirst_residual
            hyv hy_prefix hy_left_walk hy_new_bad)
    · rw [Finset.mem_erase, Finset.mem_erase, Finset.mem_inter]
      have hy_old_right :
          y ∈ (pair.2 : G.Walk v t).support :=
        Walk.support_dropUntil_subset (pair.2 : G.Walk v t) hz_right hy_drop
      refine ⟨?_, hyv, by simpa using hy_left, by simpa using hy_old_right⟩
      intro hyx
      exact hx_not_spliceRight (by simpa [hyx] using hy_splice_walk)
  simpa [terminalPathPairCommonCard, spliced] using
    (common_support_erase_card_lt_of_subset_erase_common
      (G := G) (v := v) (s := s) (t := t)
      (qs := (pair.1 : G.Walk v s))
      (qt := (pair.2 : G.Walk v t))
      (qs' := (pair.1 : G.Walk v s))
      (qt' := (spliceRight : G.Walk v t))
      (x := x) hcommon_subset_old_without_x hx_left hx_right hxv)

private lemma terminal_set_cross_swap_commonCard_lt_of_later_return
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x y r : α}
    {pair : G.Path v s × G.Path v t}
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hy_suffix : y ∈ ((pair.2 : G.Walk v t).dropUntil x hx_right).support)
    (hr_suffix :
      r ∈ (((pair.2 : G.Walk v t).dropUntil x hx_right).dropUntil y
        hy_suffix).support)
    (hr_ne_y : r ≠ y)
    (hr_left_prefix :
      r ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support) :
    ∃ pair' : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  classical
  let swapLeft : G.Path v s :=
    (((pair.2 : G.Walk v t).takeUntil x hx_right).append
      ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath
  let altRight : G.Path v t :=
    (((pair.1 : G.Walk v s).takeUntil x hx_left).append
      ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
  let swapped : G.Path v s × G.Path v t := (swapLeft, altRight)
  refine ⟨swapped, ?_⟩
  have hright_suffix_path :
      ((pair.2 : G.Walk v t).dropUntil x hx_right).IsPath :=
    Walk.isPath_of_isSubwalk
      (Walk.isSubwalk_dropUntil (pair.2 : G.Walk v t) hx_right)
      pair.2.property
  have hr_right_suffix :
      r ∈ ((pair.2 : G.Walk v t).dropUntil x hx_right).support :=
    Walk.support_dropUntil_subset
      ((pair.2 : G.Walk v t).dropUntil x hx_right) hy_suffix hr_suffix
  have hr_right : r ∈ (pair.2 : G.Walk v t).support :=
    Walk.support_dropUntil_subset (pair.2 : G.Walk v t) hx_right
      hr_right_suffix
  have hr_left : r ∈ (pair.1 : G.Walk v s).support :=
    Walk.support_takeUntil_subset (pair.1 : G.Walk v s) hx_left
      hr_left_prefix
  have hv_prefix_right :
      v ∈ ((pair.2 : G.Walk v t).takeUntil x hx_right).support :=
    (pair.2 : G.Walk v t).takeUntil x hx_right |>.start_mem_support
  have hv_not_right_suffix :
      v ∉ ((pair.2 : G.Walk v t).dropUntil x hx_right).support :=
    not_mem_dropUntil_of_mem_takeUntil_ne_on_isPath
      (G := G) (p := (pair.2 : G.Walk v t)) pair.2.property
      hx_right (by simpa using (pair.2 : G.Walk v t).start_mem_support)
      hv_prefix_right (fun hvx => hxv hvx.symm)
  have hrv : r ≠ v := by
    intro hrv_eq
    exact hv_not_right_suffix (by simpa [hrv_eq] using hr_right_suffix)
  have hx_not_right_suffix_tail :
      x ∉ ((pair.2 : G.Walk v t).dropUntil x hx_right).support.tail := by
    generalize hqeq : (pair.2 : G.Walk v t).dropUntil x hx_right = q
    have hqPath : q.IsPath := by
      simpa [hqeq] using hright_suffix_path
    change x ∉ q.support.tail
    cases q with
    | nil =>
        simp
    | cons h q' =>
        have hnodup : x ∉ q'.support ∧ q'.support.Nodup := by
          simpa using hqPath.support_nodup
        simpa using hnodup.1
  have hr_ne_x : r ≠ x := by
    intro hrx
    let q : G.Walk x t := (pair.2 : G.Walk v t).dropUntil x hx_right
    have hx_q : x ∈ q.support := q.start_mem_support
    have hy_q : y ∈ q.support := by
      simpa [q] using hy_suffix
    have hx_after_y : x ∈ (q.dropUntil y hy_q).support := by
      simpa [q, hrx] using hr_suffix
    have hxy : x ≠ y := by
      intro hxy
      exact hr_ne_y (by simpa [hrx, hxy])
    have hy_after_x : y ∈ (q.dropUntil x hx_q).support := by
      simpa [dropUntil_start_eq_self (G := G) q hx_q] using hy_q
    exact not_both_mem_dropUntil_on_simple_path
      (G := G) (p := q) (x := x) (w := y)
      (by simpa [q] using hright_suffix_path)
      hx_q hy_q hx_after_y hy_after_x hxy
  have hr_not_swapLeft :
      r ∉ (swapLeft : G.Walk v s).support := by
    intro hr_swap
    have hr_raw :
        r ∈ (((pair.2 : G.Walk v t).takeUntil x hx_right).append
          ((pair.1 : G.Walk v s).dropUntil x hx_left)).support :=
      Walk.support_toPath_subset _ hr_swap
    rw [Walk.mem_support_append_iff] at hr_raw
    rcases hr_raw with hr_right_prefix | hr_left_suffix
    · exact
        (not_mem_takeUntil_of_mem_dropUntil_ne_on_isPath
          (G := G) (p := (pair.2 : G.Walk v t)) pair.2.property
          hx_right hr_right hr_right_suffix hr_ne_x) hr_right_prefix
    · exact
        (not_mem_dropUntil_of_mem_takeUntil_ne_on_isPath
          (G := G) (p := (pair.1 : G.Walk v s)) pair.1.property
          hx_left hr_left hr_left_prefix hr_ne_x) hr_left_suffix
  have hcommon_subset_old_without_r :
      (((swapLeft : G.Walk v s).support.toFinset ∩
          (altRight : G.Walk v t).support.toFinset).erase v) ⊆
        (((pair.1 : G.Walk v s).support.toFinset ∩
          (pair.2 : G.Walk v t).support.toFinset).erase v).erase r := by
    intro a ha
    rw [Finset.mem_erase, Finset.mem_inter] at ha
    rcases ha with ⟨hav, ha_swap, ha_alt⟩
    have ha_swap_walk : a ∈ (swapLeft : G.Walk v s).support := by
      simpa using ha_swap
    have ha_alt_walk : a ∈ (altRight : G.Walk v t).support := by
      simpa using ha_alt
    have har : a ≠ r := by
      intro har_eq
      exact hr_not_swapLeft (by simpa [har_eq] using ha_swap_walk)
    have ha_swap_raw :
        a ∈ (((pair.2 : G.Walk v t).takeUntil x hx_right).append
          ((pair.1 : G.Walk v s).dropUntil x hx_left)).support :=
      Walk.support_toPath_subset _ ha_swap_walk
    have ha_alt_raw :
        a ∈ (((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).support :=
      Walk.support_toPath_subset _ ha_alt_walk
    rw [Walk.mem_support_append_iff] at ha_swap_raw
    rw [Walk.mem_support_append_iff] at ha_alt_raw
    rw [Finset.mem_erase, Finset.mem_erase, Finset.mem_inter]
    refine ⟨har, hav, ?_, ?_⟩
    · rcases ha_swap_raw with ha_right_prefix | ha_left_suffix
      · rcases ha_alt_raw with ha_left_prefix | ha_right_suffix
        · simpa using
            (Walk.support_takeUntil_subset
              (pair.1 : G.Walk v s) hx_left ha_left_prefix)
        · have ha_right : a ∈ (pair.2 : G.Walk v t).support :=
            Walk.support_takeUntil_subset
              (pair.2 : G.Walk v t) hx_right ha_right_prefix
          by_cases hax : a = x
          · simpa [hax] using hx_left
          · exact False.elim
              ((not_mem_dropUntil_of_mem_takeUntil_ne_on_isPath
                (G := G) (p := (pair.2 : G.Walk v t)) pair.2.property
                hx_right ha_right ha_right_prefix hax) ha_right_suffix)
      · simpa using
          (Walk.support_dropUntil_subset
            (pair.1 : G.Walk v s) hx_left ha_left_suffix)
    · rcases ha_alt_raw with ha_left_prefix | ha_right_suffix
      · rcases ha_swap_raw with ha_right_prefix | ha_left_suffix
        · simpa using
            (Walk.support_takeUntil_subset
              (pair.2 : G.Walk v t) hx_right ha_right_prefix)
        · have ha_left : a ∈ (pair.1 : G.Walk v s).support :=
            Walk.support_dropUntil_subset
              (pair.1 : G.Walk v s) hx_left ha_left_suffix
          by_cases hax : a = x
          · simpa [hax] using hx_right
          · exact False.elim
              ((not_mem_dropUntil_of_mem_takeUntil_ne_on_isPath
                (G := G) (p := (pair.1 : G.Walk v s)) pair.1.property
                hx_left ha_left ha_left_prefix hax) ha_left_suffix)
      · simpa using
          (Walk.support_dropUntil_subset
            (pair.2 : G.Walk v t) hx_right ha_right_suffix)
  simpa [terminalPathPairCommonCard, swapped, swapLeft, altRight] using
    (common_support_erase_card_lt_of_subset_erase_common
      (G := G) (v := v) (s := s) (t := t)
      (qs := (pair.1 : G.Walk v s))
      (qt := (pair.2 : G.Walk v t))
      (qs' := (swapLeft : G.Walk v s))
      (qt' := (altRight : G.Walk v t))
      (x := r) hcommon_subset_old_without_r hr_left hr_right hrv)

private lemma terminalPathPairCommonCard_swap
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t : α}
    (pair : G.Path v s × G.Path v t) :
    terminalPathPairCommonCard
        (((pair.2, pair.1) : G.Path v t × G.Path v s)) =
      terminalPathPairCommonCard pair := by
  simp [terminalPathPairCommonCard, Finset.inter_comm]

private lemma terminal_set_cross_swap_commonCard_lt_of_later_left_return
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x y r : α}
    {pair : G.Path v s × G.Path v t}
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hy_suffix : y ∈ ((pair.1 : G.Walk v s).dropUntil x hx_left).support)
    (hr_suffix :
      r ∈ (((pair.1 : G.Walk v s).dropUntil x hx_left).dropUntil y
        hy_suffix).support)
    (hr_ne_y : r ≠ y)
    (hr_right_prefix :
      r ∈ ((pair.2 : G.Walk v t).takeUntil x hx_right).support) :
    ∃ pair' : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  classical
  let swappedOriginal : G.Path v t × G.Path v s := (pair.2, pair.1)
  rcases terminal_set_cross_swap_commonCard_lt_of_later_return
      (G := G) (v := v) (s := t) (t := s)
      (x := x) (y := y) (r := r)
      (pair := swappedOriginal)
      hx_right hx_left hxv hy_suffix hr_suffix hr_ne_y
      hr_right_prefix with
    ⟨pairSwap', hpairSwap'_lt⟩
  refine ⟨(pairSwap'.2, pairSwap'.1), ?_⟩
  calc
    terminalPathPairCommonCard
        (((pairSwap'.2, pairSwap'.1) : G.Path v s × G.Path v t)) =
        terminalPathPairCommonCard pairSwap' :=
      terminalPathPairCommonCard_swap pairSwap'
    _ < terminalPathPairCommonCard swappedOriginal := hpairSwap'_lt
    _ = terminalPathPairCommonCard pair := terminalPathPairCommonCard_swap pair

private lemma terminal_set_cross_swap_commonCard_lt_of_left_prefix_absent_altRight
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x y : α}
    {pair : G.Path v s × G.Path v t}
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hy_left_prefix :
      y ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support)
    (hy_not_alt :
      y ∉
        (((((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath) :
            G.Walk v t).support) :
    ∃ pair' : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  classical
  rcases exists_left_prefix_right_suffix_tail_of_not_mem_left_alt
      (G := G) (left := (pair.1 : G.Walk v s))
      (right := (pair.2 : G.Walk v t))
      pair.1.property pair.2.property hx_left hx_right
      hy_left_prefix hy_not_alt with
    ⟨r, hr_left_prefix, hr_right_tail⟩
  have hx_suffix :
      x ∈ ((pair.2 : G.Walk v t).dropUntil x hx_right).support :=
    ((pair.2 : G.Walk v t).dropUntil x hx_right).start_mem_support
  have hr_right_suffix :
      r ∈ ((pair.2 : G.Walk v t).dropUntil x hx_right).support :=
    List.mem_of_mem_tail hr_right_tail
  have hright_suffix_path :
      ((pair.2 : G.Walk v t).dropUntil x hx_right).IsPath :=
    Walk.isPath_of_isSubwalk
      (Walk.isSubwalk_dropUntil (pair.2 : G.Walk v t) hx_right)
      pair.2.property
  have hr_ne_x : r ≠ x := by
    intro hrx
    generalize hqeq :
      (pair.2 : G.Walk v t).dropUntil x hx_right = q
    have hqPath : q.IsPath := by
      simpa [hqeq] using hright_suffix_path
    have hx_not_tail : x ∉ q.support.tail := by
      cases q with
      | nil =>
          simp
      | cons h q' =>
          have hnodup : x ∉ q'.support ∧ q'.support.Nodup := by
            simpa using hqPath.support_nodup
          simpa using hnodup.1
    exact hx_not_tail (by simpa [hqeq, hrx] using hr_right_tail)
  have hr_after_x :
      r ∈
        (((pair.2 : G.Walk v t).dropUntil x hx_right).dropUntil x
          hx_suffix).support := by
    simpa [dropUntil_start_eq_self
        (G := G) ((pair.2 : G.Walk v t).dropUntil x hx_right)
        hx_suffix] using hr_right_suffix
  exact terminal_set_cross_swap_commonCard_lt_of_later_return
    (G := G) (v := v) (s := s) (t := t)
    (x := x) (y := x) (r := r) (pair := pair)
    hx_left hx_right hxv hx_suffix hr_after_x hr_ne_x hr_left_prefix

private lemma terminal_set_fan_left_suffix_stage_right_prefix_witness_commonCard_lt
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x y a z r : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hy_rs : y ∈ rs.support)
    (ha_tail : a ∈ (rs.dropUntil y hy_rs).support)
    (hz_tail : z ∈ (rs.dropUntil y hy_rs).support)
    (ha_mid :
      a ∈ ((rs.dropUntil y hy_rs).takeUntil z hz_tail).support)
    (ha_not_right : a ∉ (pair.2 : G.Walk v t).support)
    (hr_mid :
      r ∈ ((rs.dropUntil y hy_rs).takeUntil a ha_tail).support)
    (hrv : r ≠ v)
    (hr_right : r ∈ (pair.2 : G.Walk v t).support)
    (hr_not_left : r ∉ (pair.1 : G.Walk v s).support)
    (hr_prefix_x :
      r ∈ ((pair.2 : G.Walk v t).takeUntil x hx_right).support)
    (hfirst_bridge_bad :
      ∀ q : α, q ≠ v →
        q ∈
          (((((pair.2 : G.Walk v t).takeUntil x hx_right).append
            ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath) :
              G.Walk v s).support →
        ¬ (q ∈ (pair.1 : G.Walk v s).support ∧
          q ∈ (pair.2 : G.Walk v t).support) →
        q ∈
          (((rs.dropUntil y hy_rs).takeUntil z hz_tail).takeUntil a
            ha_mid).support →
        q = a) :
    ∃ pair' : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  classical
  let swapLeft : G.Path v s :=
    (((pair.2 : G.Walk v t).takeUntil x hx_right).append
      ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath
  by_cases hr_swap : r ∈ (swapLeft : G.Walk v s).support
  · have hr_not_common :
        ¬ (r ∈ (pair.1 : G.Walk v s).support ∧
          r ∈ (pair.2 : G.Walk v t).support) := by
      intro hr_common
      exact hr_not_left hr_common.1
    have hr_prefix_a_full :
        r ∈
          (((rs.dropUntil y hy_rs).takeUntil z hz_tail).takeUntil a
            ha_mid).support := by
      simpa [Walk.takeUntil_takeUntil] using hr_mid
    have hra : r = a :=
      hfirst_bridge_bad r hrv (by simpa [swapLeft] using hr_swap)
        hr_not_common hr_prefix_a_full
    exact False.elim (ha_not_right (by simpa [hra] using hr_right))
  · rcases exists_left_prefix_right_suffix_tail_of_not_mem_left_alt
        (G := G) (left := (pair.2 : G.Walk v t))
        (right := (pair.1 : G.Walk v s))
        pair.2.property pair.1.property hx_right hx_left
        hr_prefix_x (by simpa [swapLeft] using hr_swap) with
      ⟨u, hu_right_prefix, hu_left_tail⟩
    have hx_left_suffix :
        x ∈ ((pair.1 : G.Walk v s).dropUntil x hx_left).support :=
      ((pair.1 : G.Walk v s).dropUntil x hx_left).start_mem_support
    have hu_left_suffix :
        u ∈ ((pair.1 : G.Walk v s).dropUntil x hx_left).support :=
      List.mem_of_mem_tail hu_left_tail
    have hleft_suffix_path :
        ((pair.1 : G.Walk v s).dropUntil x hx_left).IsPath :=
      Walk.isPath_of_isSubwalk
        (Walk.isSubwalk_dropUntil (pair.1 : G.Walk v s) hx_left)
        pair.1.property
    have hu_ne_x : u ≠ x := by
      intro hux
      generalize hqeq :
        (pair.1 : G.Walk v s).dropUntil x hx_left = q
      have hqPath : q.IsPath := by
        simpa [hqeq] using hleft_suffix_path
      have hx_not_tail : x ∉ q.support.tail := by
        cases q with
        | nil =>
            simp
        | cons h q' =>
            have hnodup : x ∉ q'.support ∧ q'.support.Nodup := by
              simpa using hqPath.support_nodup
            simpa using hnodup.1
      exact hx_not_tail (by simpa [hqeq, hux] using hu_left_tail)
    have hu_after_x :
        u ∈
          (((pair.1 : G.Walk v s).dropUntil x hx_left).dropUntil x
            hx_left_suffix).support := by
      simpa [dropUntil_start_eq_self
          (G := G) ((pair.1 : G.Walk v s).dropUntil x hx_left)
          hx_left_suffix] using hu_left_suffix
    exact terminal_set_cross_swap_commonCard_lt_of_later_left_return
      (G := G) (v := v) (s := s) (t := t)
      (x := x) (y := x) (r := u) (pair := pair)
      hx_left hx_right hxv hx_left_suffix hu_after_x hu_ne_x
      hu_right_prefix

private lemma terminal_set_fan_first_bad_right_only_splice_commonCard_lt
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x z : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hpair_measure_min : ∀ pair' : G.Path v s × G.Path v t,
      terminalPathPairWeightedMeasure pair ≤ terminalPathPairWeightedMeasure pair')
    (_hrsPath : rs.IsPath)
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rs : x ∉ rs.support)
    (hzrs : z ∈ rs.support)
    (hz_right : z ∈ (pair.2 : G.Walk v t).support)
    (hz_not_left : z ∉ (pair.1 : G.Walk v s).support)
    (hz_suffix_right :
      z ∈ ((pair.2 : G.Walk v t).dropUntil x hx_right).support)
    (hfirst_bad :
      let altRight : G.Path v t :=
        (((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
      ∀ y : α, y ≠ v →
        y ∈ (altRight : G.Walk v t).support →
        ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
           y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x) →
        y ∈ (rs.takeUntil z hzrs).support →
        y = z) :
    ∃ pair' : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  classical
  dsimp at hfirst_bad
  let spliceRight : G.Path v t :=
    ((rs.takeUntil z hzrs).append
      ((pair.2 : G.Walk v t).dropUntil z hz_right)).toPath
  let spliced : G.Path v s × G.Path v t := (pair.1, spliceRight)
  let altRight : G.Path v t :=
    (((pair.1 : G.Walk v s).takeUntil x hx_left).append
      ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
  refine ⟨spliced, ?_⟩
  have hno_lower :
      ∀ pair' : G.Path v s × G.Path v t,
        ¬ terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair :=
    not_terminalPathPairCommonCard_lt_of_weighted_min hpair_measure_min
  have hzx : z ≠ x := by
    intro hzx_eq
    exact hx_rs (by simpa [hzx_eq] using hzrs)
  have hx_ne_z : x ≠ z := fun hxz => hzx hxz.symm
  have hx_not_spliceRight :
      x ∉ (spliceRight : G.Walk v t).support := by
    intro hx_splice
    have hx_append :
        x ∈ ((rs.takeUntil z hzrs).append
          ((pair.2 : G.Walk v t).dropUntil z hz_right)).support := by
      exact Walk.support_toPath_subset _ hx_splice
    rw [Walk.mem_support_append_iff] at hx_append
    rcases hx_append with hx_prefix | hx_drop
    · exact hx_rs (Walk.support_takeUntil_subset rs hzrs hx_prefix)
    · exact False.elim
        (not_both_mem_dropUntil_on_simple_path
          (G := G) (p := (pair.2 : G.Walk v t)) pair.2.property
          hx_right hz_right hx_drop hz_suffix_right hx_ne_z)
  have hcommon_subset_old_without_x :
      ((pair.1 : G.Walk v s).support.toFinset ∩
          (spliceRight : G.Walk v t).support.toFinset).erase v ⊆
        (((pair.1 : G.Walk v s).support.toFinset ∩
          (pair.2 : G.Walk v t).support.toFinset).erase v).erase x := by
    intro y hy
    rw [Finset.mem_erase, Finset.mem_inter] at hy
    rcases hy with ⟨hyv, hy_left, hy_splice⟩
    have hy_left_walk :
        y ∈ (pair.1 : G.Walk v s).support := by
      simpa using hy_left
    have hy_splice_walk : y ∈ (spliceRight : G.Walk v t).support := by
      simpa using hy_splice
    have hy_append :
        y ∈ ((rs.takeUntil z hzrs).append
          ((pair.2 : G.Walk v t).dropUntil z hz_right)).support := by
      exact Walk.support_toPath_subset _ hy_splice_walk
    rw [Walk.mem_support_append_iff] at hy_append
    rcases hy_append with hy_prefix | hy_drop
    · have hy_rs : y ∈ rs.support :=
        Walk.support_takeUntil_subset rs hzrs hy_prefix
      rcases mem_erase_common_without_x_or_not_common_triple_left
          (G := G) (pair := pair) (x := x) hyv hy_left_walk with
        hy_old_common | hy_new_bad
      · exact hy_old_common
      · exfalso
        by_cases hy_alt_local : y ∈ (altRight : G.Walk v t).support
        · have hy_eq_z : y = z :=
            hfirst_bad y hyv (by simpa [altRight] using hy_alt_local)
              hy_new_bad hy_prefix
          exact hz_not_left (by simpa [hy_eq_z] using hy_left_walk)
        · by_cases hy_left_prefix :
            y ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support
          · rcases exists_left_prefix_right_suffix_tail_of_not_mem_left_alt
              (G := G) (left := (pair.1 : G.Walk v s))
              (right := (pair.2 : G.Walk v t))
              pair.1.property pair.2.property hx_left hx_right
              hy_left_prefix hy_alt_local with
              ⟨r, hr_left_prefix, hr_right_tail⟩
            have hx_suffix :
                x ∈ ((pair.2 : G.Walk v t).dropUntil x hx_right).support :=
              ((pair.2 : G.Walk v t).dropUntil x hx_right).start_mem_support
            have hr_right_suffix :
                r ∈ ((pair.2 : G.Walk v t).dropUntil x hx_right).support :=
              List.mem_of_mem_tail hr_right_tail
            have hright_suffix_path :
                ((pair.2 : G.Walk v t).dropUntil x hx_right).IsPath :=
              Walk.isPath_of_isSubwalk
                (Walk.isSubwalk_dropUntil (pair.2 : G.Walk v t) hx_right)
                pair.2.property
            have hr_ne_x : r ≠ x := by
              intro hrx
              generalize hqeq :
                (pair.2 : G.Walk v t).dropUntil x hx_right = q
              have hqPath : q.IsPath := by
                simpa [hqeq] using hright_suffix_path
              have hx_not_tail : x ∉ q.support.tail := by
                cases q with
                | nil =>
                    simp
                | cons h q' =>
                    have hnodup : x ∉ q'.support ∧ q'.support.Nodup := by
                      simpa using hqPath.support_nodup
                    simpa using hnodup.1
              exact hx_not_tail (by simpa [hqeq, hrx] using hr_right_tail)
            have hr_after_x :
                r ∈
                  (((pair.2 : G.Walk v t).dropUntil x hx_right).dropUntil x
                    hx_suffix).support := by
              simpa [dropUntil_start_eq_self
                  (G := G) ((pair.2 : G.Walk v t).dropUntil x hx_right)
                  hx_suffix] using hr_right_suffix
            rcases terminal_set_cross_swap_commonCard_lt_of_later_return
                (G := G) (v := v) (s := s) (t := t)
                (x := x) (y := x) (r := r) (pair := pair)
                hx_left hx_right hxv hx_suffix hr_after_x hr_ne_x
                hr_left_prefix with
              ⟨pair', hpair'_lt⟩
            exact hno_lower pair' hpair'_lt
          · have hy_ne_x : y ≠ x := by
              intro hyx
              exact hx_rs (by simpa [hyx] using hy_rs)
            have hy_not_right :
                y ∉ (pair.2 : G.Walk v t).support := by
              intro hy_right
              exact hy_new_bad ⟨hy_left_walk, hy_right, hy_ne_x⟩
            rcases terminal_set_fan_first_bad_right_only_fallback_left_alt_commonCard_lt
                (G := G) (v := v) (s := s) (t := t)
                (x := x) (z := z) (y := y)
                (pair := pair) (rs := rs)
                _hrsPath hx_left hx_right hxv hx_rs hzrs hz_right
                hz_not_left hfirst_bad hy_rs hy_prefix hy_left_walk
                hy_not_right hy_left_prefix with
              ⟨pair', hpair'_lt⟩
            exact hno_lower pair' hpair'_lt
    · rw [Finset.mem_erase, Finset.mem_erase, Finset.mem_inter]
      have hy_old_right :
          y ∈ (pair.2 : G.Walk v t).support :=
        Walk.support_dropUntil_subset (pair.2 : G.Walk v t) hz_right hy_drop
      refine ⟨?_, hyv, by simpa using hy_left, by simpa using hy_old_right⟩
      intro hyx
      exact hx_not_spliceRight (by simpa [hyx] using hy_splice_walk)
  simpa [terminalPathPairCommonCard, spliced, spliceRight] using
    (common_support_erase_card_lt_of_subset_erase_common
      (G := G) (v := v) (s := s) (t := t)
      (qs := (pair.1 : G.Walk v s))
      (qt := (pair.2 : G.Walk v t))
      (qs' := (pair.1 : G.Walk v s))
      (qt' := (spliceRight : G.Walk v t))
      (x := x) hcommon_subset_old_without_x hx_left hx_right hxv)

private lemma first_bad_left_prefix_package
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x w z : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hx_rs : x ∉ rs.support)
    (hw_rs : w ∈ rs.support)
    (hw_not_left : w ∉ (pair.1 : G.Walk v s).support)
    (hz_rs : z ∈ rs.support)
    (hz_left : z ∈ (pair.1 : G.Walk v s).support)
    (hz_alt :
      z ∈
        ((((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath :
            G.Walk v t).support)
    (hz_bad :
      ¬ (z ∈ (pair.1 : G.Walk v s).support ∧
         z ∈ (pair.2 : G.Walk v t).support ∧ z ≠ x))
    (hfirst : ∀ y, y ∈ rs.support → y ≠ v →
      y ∈ (pair.1 : G.Walk v s).support ∨
      y ∈ (pair.2 : G.Walk v t).support →
      y = w ∨ y ∉ (rs.takeUntil w hw_rs).support)
    (hzv : z ≠ v) :
    z ∉ (pair.2 : G.Walk v t).support ∧
      z ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support ∧
      z ∉ (rs.takeUntil w hw_rs).support := by
  have hzx : z ≠ x := by
    intro hzx_eq
    exact hx_rs (by simpa [hzx_eq] using hz_rs)
  have hz_not_right : z ∉ (pair.2 : G.Walk v t).support := by
    intro hz_right
    exact hz_bad ⟨hz_left, hz_right, hzx⟩
  have hz_alt_raw :
      z ∈ (((pair.1 : G.Walk v s).takeUntil x hx_left).append
        ((pair.2 : G.Walk v t).dropUntil x hx_right)).support :=
    Walk.support_toPath_subset _ hz_alt
  have hz_prefix_left :
      z ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support := by
    rw [Walk.mem_support_append_iff] at hz_alt_raw
    rcases hz_alt_raw with hz_prefix | hz_suffix
    · exact hz_prefix
    · exact False.elim
        (hz_not_right
          (Walk.support_dropUntil_subset (pair.2 : G.Walk v t)
            hx_right hz_suffix))
  have hz_not_rs_prefix :
      z ∉ (rs.takeUntil w hw_rs).support := by
    have hfirst_z := hfirst z hz_rs hzv (Or.inl hz_left)
    rcases hfirst_z with hzw | hz_not_prefix
    · exact False.elim (hw_not_left (by simpa [hzw] using hz_left))
    · exact hz_not_prefix
  exact ⟨hz_not_right, hz_prefix_left, hz_not_rs_prefix⟩

private lemma later_bad_after_first_bad_on_isPath
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x y z : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hrsPath : rs.IsPath)
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hy_rs : y ∈ rs.support)
    (hz_rs : z ∈ rs.support)
    (_hyv : y ≠ v)
    (hzv : z ≠ v)
    (hy_not_right : y ∉ (pair.2 : G.Walk v t).support)
    (hz_right : z ∈ (pair.2 : G.Walk v t).support)
    (_hy_alt :
      y ∈
        ((((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath :
            G.Walk v t).support)
    (hz_alt :
      z ∈
        ((((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath :
            G.Walk v t).support)
    (hz_bad :
      ¬ (z ∈ (pair.1 : G.Walk v s).support ∧
         z ∈ (pair.2 : G.Walk v t).support ∧ z ≠ x))
    (hfirst_bad :
      let altRight : G.Path v t :=
        (((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
      ∀ q : α, q ≠ v →
        q ∈ (altRight : G.Walk v t).support →
        ¬ (q ∈ (pair.1 : G.Walk v s).support ∧
           q ∈ (pair.2 : G.Walk v t).support ∧ q ≠ x) →
        q ∈ (rs.takeUntil y hy_rs).support →
        q = y) :
    z ∈ (rs.dropUntil y hy_rs).support ∧
      y ∈ (rs.takeUntil z hz_rs).support := by
  classical
  dsimp at hfirst_bad
  let altRight : G.Path v t :=
    (((pair.1 : G.Walk v s).takeUntil x hx_left).append
      ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
  have hzy : z ≠ y := by
    intro hzy_eq
    exact hy_not_right (by simpa [hzy_eq] using hz_right)
  have hz_not_prefix_y :
      z ∉ (rs.takeUntil y hy_rs).support := by
    intro hz_prefix_y
    have hzy_eq : z = y :=
      hfirst_bad z hzv (by simpa [altRight] using hz_alt) hz_bad hz_prefix_y
    exact hzy hzy_eq
  have hz_after_y :
      z ∈ (rs.dropUntil y hy_rs).support :=
    mem_dropUntil_of_mem_support_not_takeUntil
      (G := G) rs hy_rs hz_rs hz_not_prefix_y
  have hy_prefix_z :
      y ∈ (rs.takeUntil z hz_rs).support :=
    mem_takeUntil_of_mem_dropUntil_ne_on_isPath
      (G := G) (p := rs) hrsPath hy_rs hz_rs hz_after_y hzy.symm
  exact ⟨hz_after_y, hy_prefix_z⟩

private lemma terminal_set_fan_left_suffix_retention_left_prefix_not_alt_commonCard_descent_of_not_right_suffix
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x w z y : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hrsPath : rs.IsPath)
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rs : x ∉ rs.support)
    (_hw_rs : w ∈ rs.support)
    (_hw_right : w ∈ (pair.2 : G.Walk v t).support)
    (_hw_not_left : w ∉ (pair.1 : G.Walk v s).support)
    (_hwv : w ≠ v)
    (_hfirst : ∀ y, y ∈ rs.support → y ≠ v →
      y ∈ (pair.1 : G.Walk v s).support ∨
      y ∈ (pair.2 : G.Walk v t).support →
      y = w ∨ y ∉ (rs.takeUntil w _hw_rs).support)
    (_hdirect : ¬ terminalPathPairCommonCard
      ((⟨rs, hrsPath⟩ : G.Path v s), pair.2) <
      terminalPathPairCommonCard pair)
    (_hret : x ∈ ((pair.2 : G.Walk v t).dropUntil w _hw_right).support)
    (hzrs : z ∈ rs.support)
    (_hzv : z ≠ v)
    (_hz_left : z ∈ (pair.1 : G.Walk v s).support)
    (hz_not_right : z ∉ (pair.2 : G.Walk v t).support)
    (_hz_prefix_left :
      z ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support)
    (_hz_not_rs_prefix : z ∉ (rs.takeUntil w _hw_rs).support)
    (hlast_bad :
      let altRight : G.Path v t :=
        (((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
      ∀ y : α, y ∈ rs.support → y ≠ v →
        y ∈ (altRight : G.Walk v t).support →
        ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
           y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x) →
        y ∈ (rs.dropUntil z hzrs).support →
        y = z)
    (hyv : y ≠ v)
    (hy_rs : y ∈ rs.support)
    (hy_drop : y ∈ (rs.dropUntil z hzrs).support)
    (hy_right : y ∈ (pair.2 : G.Walk v t).support)
    (_hy_not_alt :
      let altRight : G.Path v t :=
        (((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
      y ∉ (altRight : G.Walk v t).support)
    (hy_new_bad :
      ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
         y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x))
    (hy_not_suffix :
      y ∉ ((pair.2 : G.Walk v t).dropUntil x hx_right).support) :
    ∃ pair' : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  classical
  let altRight : G.Path v t :=
    (((pair.1 : G.Walk v s).takeUntil x hx_left).append
      ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
  let fallbackLeft : G.Path v s :=
    (((pair.2 : G.Walk v t).takeUntil y hy_right).append
      (rs.dropUntil y hy_rs)).toPath
  let fallbackPair : G.Path v s × G.Path v t := (fallbackLeft, altRight)
  refine ⟨fallbackPair, ?_⟩
  have hx_not_fallback :
      x ∉ (fallbackLeft : G.Walk v s).support := by
    simpa [fallbackLeft] using
      (not_mem_left_prefix_fallback_of_not_right_suffix
        (G := G) (right := (pair.2 : G.Walk v t)) (rs := rs)
        hx_right hy_right hy_rs hx_rs hy_not_suffix)
  have hcommon_subset_old_without_x :
      (((fallbackLeft : G.Walk v s).support.toFinset ∩
          (altRight : G.Walk v t).support.toFinset).erase v) ⊆
        (((pair.1 : G.Walk v s).support.toFinset ∩
          (pair.2 : G.Walk v t).support.toFinset).erase v).erase x := by
    intro a ha
    rw [Finset.mem_erase, Finset.mem_inter] at ha
    rcases ha with ⟨hav, ha_fallback, ha_alt⟩
    have ha_fallback_walk : a ∈ (fallbackLeft : G.Walk v s).support := by
      simpa using ha_fallback
    have ha_alt_walk : a ∈ (altRight : G.Walk v t).support := by
      simpa using ha_alt
    have hax : a ≠ x := by
      intro hax_eq
      exact hx_not_fallback (by simpa [hax_eq] using ha_fallback_walk)
    have ha_fallback_raw :
        a ∈ (((pair.2 : G.Walk v t).takeUntil y hy_right).append
          (rs.dropUntil y hy_rs)).support := by
      exact Walk.support_toPath_subset _ ha_fallback_walk
    have ha_alt_raw :
        a ∈ (((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).support := by
      exact Walk.support_toPath_subset _ ha_alt_walk
    rw [Walk.mem_support_append_iff] at ha_fallback_raw
    rw [Walk.mem_support_append_iff] at ha_alt_raw
    rcases ha_fallback_raw with ha_right_prefix | ha_rs_drop
    · have ha_right : a ∈ (pair.2 : G.Walk v t).support :=
        Walk.support_takeUntil_subset (pair.2 : G.Walk v t) hy_right ha_right_prefix
      rw [Finset.mem_erase, Finset.mem_erase, Finset.mem_inter]
      refine ⟨hax, hav, ?_, by simpa using ha_right⟩
      rcases ha_alt_raw with ha_left_prefix | ha_right_suffix
      · simpa using
          (Walk.support_takeUntil_subset (pair.1 : G.Walk v s) hx_left ha_left_prefix)
      · have hay : a = y ∨ a ≠ y := eq_or_ne a y
        rcases hay with rfl | hay_ne
        · exact False.elim (hy_not_suffix ha_right_suffix)
        · have hy_suffix :
              y ∈ ((pair.2 : G.Walk v t).dropUntil x hx_right).support :=
            mem_dropUntil_of_mem_dropUntil_of_mem_takeUntil_ne
              (G := G) (p := (pair.2 : G.Walk v t)) pair.2.property
              hx_right hy_right ha_right ha_right_suffix ha_right_prefix hay_ne
          exact False.elim (hy_not_suffix hy_suffix)
    · have ha_rs : a ∈ rs.support :=
        Walk.support_dropUntil_subset rs hy_rs ha_rs_drop
      have ha_after_z :
          a ∈ (rs.dropUntil z hzrs).support :=
        mem_dropUntil_of_mem_dropUntil_of_mem_dropUntil
          (G := G) (p := rs) hrsPath hzrs hy_rs hy_drop ha_rs_drop
      rcases ha_alt_raw with ha_left_prefix | ha_right_suffix
      · have ha_left : a ∈ (pair.1 : G.Walk v s).support :=
          Walk.support_takeUntil_subset (pair.1 : G.Walk v s) hx_left ha_left_prefix
        rcases mem_erase_common_without_x_or_not_common_triple_left
            (G := G) (pair := pair) (x := x) hav ha_left with
          ha_old_common | ha_new_bad
        · exact ha_old_common
        · have ha_eq_z : a = z :=
            hlast_bad a ha_rs hav (by simpa [altRight] using ha_alt_walk)
              ha_new_bad ha_after_z
          have hy_ne_z : y ≠ z := by
            intro hyz
            exact hz_not_right (by simpa [hyz] using hy_right)
          exact False.elim
              (not_both_mem_dropUntil_on_simple_path
                (G := G) (p := rs) hrsPath hzrs hy_rs
              (by simpa [ha_eq_z] using ha_rs_drop) hy_drop hy_ne_z.symm)
      · have ha_right : a ∈ (pair.2 : G.Walk v t).support :=
          Walk.support_dropUntil_subset (pair.2 : G.Walk v t) hx_right ha_right_suffix
        rcases mem_erase_common_without_x_or_not_common_triple
            (G := G) (pair := pair) (x := x) hav ha_right with
          ha_old_common | ha_new_bad
        · exact ha_old_common
        · have ha_eq_z : a = z :=
            hlast_bad a ha_rs hav (by simpa [altRight] using ha_alt_walk)
              ha_new_bad ha_after_z
          exact False.elim (hz_not_right (by simpa [ha_eq_z] using ha_right))
  simpa [terminalPathPairCommonCard, fallbackPair, fallbackLeft, altRight] using
    (common_support_erase_card_lt_of_subset_erase_common
      (G := G) (v := v) (s := s) (t := t)
      (qs := (pair.1 : G.Walk v s))
      (qt := (pair.2 : G.Walk v t))
      (qs' := (fallbackLeft : G.Walk v s))
      (qt' := (altRight : G.Walk v t))
      (x := x) hcommon_subset_old_without_x hx_left hx_right hxv)

lemma terminal_set_fan_left_suffix_retention_left_prefix_not_alt_commonCard_descent
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x w z y : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hrsPath : rs.IsPath)
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rs : x ∉ rs.support)
    (hw_rs : w ∈ rs.support)
    (hw_right : w ∈ (pair.2 : G.Walk v t).support)
    (hw_not_left : w ∉ (pair.1 : G.Walk v s).support)
    (hwv : w ≠ v)
    (hfirst : ∀ y, y ∈ rs.support → y ≠ v →
      y ∈ (pair.1 : G.Walk v s).support ∨
      y ∈ (pair.2 : G.Walk v t).support →
      y = w ∨ y ∉ (rs.takeUntil w hw_rs).support)
    (hdirect : ¬ terminalPathPairCommonCard
      ((⟨rs, hrsPath⟩ : G.Path v s), pair.2) <
      terminalPathPairCommonCard pair)
    (hret : x ∈ ((pair.2 : G.Walk v t).dropUntil w hw_right).support)
    (hzrs : z ∈ rs.support)
    (hzv : z ≠ v)
    (hz_left : z ∈ (pair.1 : G.Walk v s).support)
    (hz_not_right : z ∉ (pair.2 : G.Walk v t).support)
    (hz_prefix_left :
      z ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support)
    (hz_not_rs_prefix : z ∉ (rs.takeUntil w hw_rs).support)
    (hlast_bad :
      let altRight : G.Path v t :=
        (((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
      ∀ y : α, y ∈ rs.support → y ≠ v →
        y ∈ (altRight : G.Walk v t).support →
        ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
           y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x) →
        y ∈ (rs.dropUntil z hzrs).support →
        y = z)
    (hyv : y ≠ v)
    (hy_rs : y ∈ rs.support)
    (hy_drop : y ∈ (rs.dropUntil z hzrs).support)
    (hy_right : y ∈ (pair.2 : G.Walk v t).support)
    (hy_not_alt :
      let altRight : G.Path v t :=
        (((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
      y ∉ (altRight : G.Walk v t).support)
    (hy_new_bad :
      ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
         y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x)) :
    ∃ pair' : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  classical
  by_cases hy_suffix :
      y ∈ ((pair.2 : G.Walk v t).dropUntil x hx_right).support
  · have hy_ne_x : y ≠ x := by
      intro hyx
      exact hx_rs (by simpa [hyx] using hy_rs)
    have hy_not_left_prefix :
        y ∉ ((pair.1 : G.Walk v s).takeUntil x hx_left).support := by
      intro hy_left_prefix
      have hy_left : y ∈ (pair.1 : G.Walk v s).support :=
        Walk.support_takeUntil_subset (pair.1 : G.Walk v s) hx_left
          hy_left_prefix
      exact hy_new_bad ⟨hy_left, hy_right, hy_ne_x⟩
    have hlater_return :
        ∃ r : α,
          r ∈ (((pair.2 : G.Walk v t).dropUntil x hx_right).dropUntil y
              hy_suffix).support ∧
          r ≠ y ∧
          r ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support := by
      simpa using
        (support_toPath_append_takeUntil_dropUntil_absent_right_suffix_later_left_return
          (G := G) (left := (pair.1 : G.Walk v s))
          (right := (pair.2 : G.Walk v t)) pair.1.property pair.2.property
          hx_left hx_right hy_suffix hy_not_left_prefix hy_not_alt)
    rcases hlater_return with ⟨r, hr_suffix, _hr_ne_y, hr_left_prefix⟩
    exact terminal_set_cross_swap_commonCard_lt_of_later_return
      (G := G) (v := v) (s := s) (t := t)
      (x := x) (y := y) (r := r) (pair := pair)
      hx_left hx_right hxv hy_suffix hr_suffix _hr_ne_y hr_left_prefix
  · exact
      terminal_set_fan_left_suffix_retention_left_prefix_not_alt_commonCard_descent_of_not_right_suffix
        (G := G) (v := v) (s := s) (t := t)
        (x := x) (w := w) (z := z) (y := y)
        (pair := pair) (rs := rs)
        hrsPath hx_left hx_right hxv hx_rs hw_rs hw_right hw_not_left hwv
        hfirst hdirect hret hzrs hzv hz_left hz_not_right hz_prefix_left
        hz_not_rs_prefix hlast_bad hyv hy_rs hy_drop hy_right hy_not_alt
        hy_new_bad hy_suffix

lemma terminal_set_fan_left_suffix_retention_left_prefix_weighted_fallback_extremal_false
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x w z y : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hpair_measure_min : ∀ pair' : G.Path v s × G.Path v t,
      terminalPathPairWeightedMeasure pair ≤ terminalPathPairWeightedMeasure pair')
    (hrsPath : rs.IsPath)
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rs : x ∉ rs.support)
    (hw_rs : w ∈ rs.support)
    (hw_right : w ∈ (pair.2 : G.Walk v t).support)
    (hw_not_left : w ∉ (pair.1 : G.Walk v s).support)
    (hwv : w ≠ v)
    (hfirst : ∀ y, y ∈ rs.support → y ≠ v →
      y ∈ (pair.1 : G.Walk v s).support ∨
      y ∈ (pair.2 : G.Walk v t).support →
      y = w ∨ y ∉ (rs.takeUntil w hw_rs).support)
    (hdirect : ¬ terminalPathPairCommonCard
      ((⟨rs, hrsPath⟩ : G.Path v s), pair.2) <
      terminalPathPairCommonCard pair)
    (hret : x ∈ ((pair.2 : G.Walk v t).dropUntil w hw_right).support)
    (hzrs : z ∈ rs.support)
    (hzv : z ≠ v)
    (hz_left : z ∈ (pair.1 : G.Walk v s).support)
    (hz_not_right : z ∉ (pair.2 : G.Walk v t).support)
    (hz_prefix_left :
      z ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support)
    (hz_not_rs_prefix : z ∉ (rs.takeUntil w hw_rs).support)
    (hlast_bad :
      let altRight : G.Path v t :=
        (((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
      ∀ y : α, y ∈ rs.support → y ≠ v →
        y ∈ (altRight : G.Walk v t).support →
        ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
           y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x) →
        y ∈ (rs.dropUntil z hzrs).support →
        y = z)
    (hyv : y ≠ v)
    (hy_rs : y ∈ rs.support)
    (hy_drop : y ∈ (rs.dropUntil z hzrs).support)
    (hy_right : y ∈ (pair.2 : G.Walk v t).support)
    (hy_not_alt :
      let altRight : G.Path v t :=
        (((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
      y ∉ (altRight : G.Walk v t).support)
    (hy_new_bad :
      ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
         y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x)) :
    False := by
  classical
  let altRight : G.Path v t :=
    (((pair.1 : G.Walk v s).takeUntil x hx_left).append
      ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
  let fallbackLeft : G.Path v s :=
    (((pair.2 : G.Walk v t).takeUntil y hy_right).append
      (rs.dropUntil y hy_rs)).toPath
  let fallbackPair : G.Path v s × G.Path v t := (fallbackLeft, altRight)
  have hy_ne_x : y ≠ x := by
    intro hyx
    exact hx_rs (by simpa [hyx] using hy_rs)
  have hy_not_left : y ∉ (pair.1 : G.Walk v s).support := by
    intro hy_left
    exact hy_new_bad ⟨hy_left, hy_right, hy_ne_x⟩
  have hy_first := hfirst y hy_rs hyv (Or.inr hy_right)
  have hy_not_rs_prefix : y ∉ (rs.takeUntil w hw_rs).support := by
    rcases hy_first with hyw | hy_not_prefix
    · have hz_after_w :
          z ∈ (rs.dropUntil w hw_rs).support :=
        mem_dropUntil_of_mem_support_not_takeUntil
          (G := G) rs hw_rs hzrs hz_not_rs_prefix
      have hw_after_z :
          w ∈ (rs.dropUntil z hzrs).support := by
        simpa [hyw] using hy_drop
      have hzw : z ≠ w := by
        intro hzw_eq
        exact hw_not_left (by simpa [hzw_eq] using hz_left)
      exact False.elim
        (not_both_mem_dropUntil_on_simple_path
          (G := G) (p := rs) hrsPath hzrs hw_rs
          hz_after_w hw_after_z hzw)
    · exact hy_not_prefix
  have hcommon_lt :
      terminalPathPairCommonCard fallbackPair < terminalPathPairCommonCard pair := by
    rcases terminal_set_fan_left_suffix_retention_left_prefix_not_alt_commonCard_descent
        (G := G) (v := v) (s := s) (t := t)
        (x := x) (w := w) (z := z) (y := y)
        (pair := pair) (rs := rs)
        hrsPath hx_left hx_right hxv hx_rs hw_rs hw_right hw_not_left hwv
        hfirst hdirect hret hzrs hzv hz_left hz_not_right hz_prefix_left
        hz_not_rs_prefix hlast_bad hyv hy_rs hy_drop hy_right hy_not_alt
        hy_new_bad with
      ⟨pair', hpair'_lt⟩
    exact False.elim
      (not_terminalPathPairCommonCard_lt_of_weighted_min
        hpair_measure_min pair' hpair'_lt)
  exact false_of_weighted_min_and_commonCard_lt
    (pair := pair) (pair' := fallbackPair)
    hpair_measure_min hcommon_lt

lemma terminal_set_fan_left_suffix_retention_left_prefix_residual_bad_false
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x w z y : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hpair_measure_min : ∀ pair' : G.Path v s × G.Path v t,
      terminalPathPairWeightedMeasure pair ≤ terminalPathPairWeightedMeasure pair')
    (hrsPath : rs.IsPath)
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rs : x ∉ rs.support)
    (hw_rs : w ∈ rs.support)
    (hw_right : w ∈ (pair.2 : G.Walk v t).support)
    (hw_not_left : w ∉ (pair.1 : G.Walk v s).support)
    (hwv : w ≠ v)
    (hfirst : ∀ y, y ∈ rs.support → y ≠ v →
      y ∈ (pair.1 : G.Walk v s).support ∨
      y ∈ (pair.2 : G.Walk v t).support →
      y = w ∨ y ∉ (rs.takeUntil w hw_rs).support)
    (hdirect : ¬ terminalPathPairCommonCard
      ((⟨rs, hrsPath⟩ : G.Path v s), pair.2) <
      terminalPathPairCommonCard pair)
    (hret : x ∈ ((pair.2 : G.Walk v t).dropUntil w hw_right).support)
    (hzrs : z ∈ rs.support)
    (hzv : z ≠ v)
    (hz_left : z ∈ (pair.1 : G.Walk v s).support)
    (hz_not_right : z ∉ (pair.2 : G.Walk v t).support)
    (hz_prefix_left :
      z ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support)
    (hz_not_rs_prefix : z ∉ (rs.takeUntil w hw_rs).support)
    (hlast_bad :
      let altRight : G.Path v t :=
        (((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
      ∀ y : α, y ∈ rs.support → y ≠ v →
        y ∈ (altRight : G.Walk v t).support →
        ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
           y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x) →
        y ∈ (rs.dropUntil z hzrs).support →
        y = z)
    (hyv : y ≠ v)
    (hy_drop : y ∈ (rs.dropUntil z hzrs).support)
    (hy_right : y ∈ (pair.2 : G.Walk v t).support)
    (hy_new_bad :
      ¬ (y ∈ (pair.1 : G.Walk v s).support ∧
         y ∈ (pair.2 : G.Walk v t).support ∧ y ≠ x)) :
    False := by
  classical
  let altRight : G.Path v t :=
    (((pair.1 : G.Walk v s).takeUntil x hx_left).append
      ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
  by_cases hy_alt : y ∈ (altRight : G.Walk v t).support
  · exact terminal_set_fan_left_suffix_retention_left_prefix_residual_bad_false_of_altRight
      (G := G) (v := v) (s := s) (t := t) (x := x)
      (z := z) (y := y) (pair := pair) (rs := rs)
      hx_left hx_right hzrs hz_not_right hlast_bad hyv hy_drop hy_right
      (by simpa [altRight] using hy_alt) hy_new_bad
  · exact terminal_set_fan_left_suffix_retention_left_prefix_weighted_fallback_extremal_false
      (G := G) (v := v) (s := s) (t := t) (x := x) (w := w)
      (z := z) (y := y) (pair := pair) (rs := rs)
      hpair_measure_min hrsPath hx_left hx_right hxv hx_rs
      hw_rs hw_right hw_not_left hwv hfirst hdirect hret
      hzrs hzv hz_left hz_not_right hz_prefix_left hz_not_rs_prefix
      hlast_bad hyv (Walk.support_dropUntil_subset rs hzrs hy_drop) hy_drop hy_right
      (by simpa [altRight] using hy_alt) hy_new_bad

private lemma terminalPathPair_left_endpoint_ne_of_common_nonapex
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x : α}
    {pair : G.Path v s × G.Path v t}
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hxv : x ≠ v) :
    v ≠ s := by
  intro hvs
  subst s
  have hnil : (pair.1 : G.Walk v v) = Walk.nil :=
    (Walk.isPath_iff_eq_nil _).mp pair.1.property
  have hx_eq : x = v := by
    simpa [hnil] using hx_left
  exact hxv hx_eq

private lemma terminalPathPair_right_endpoint_ne_of_common_nonapex
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x : α}
    {pair : G.Path v s × G.Path v t}
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v) :
    v ≠ t := by
  intro hvt
  subst t
  have hnil : (pair.2 : G.Walk v v) = Walk.nil :=
    (Walk.isPath_iff_eq_nil _).mp pair.2.property
  have hx_eq : x = v := by
    simpa [hnil] using hx_right
  exact hxv hx_eq

private lemma terminal_set_terminals_ne_of_separator
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t : α}
    (hvs : v ≠ s)
    (hsep : ∀ C : Finset α, C.card < 2 → v ∉ C →
      ∃ u : α, (u = s ∨ u = t) ∧ u ∉ C ∧
        ∃ q : G.Walk v u, q.IsPath ∧ ∀ z, z ∈ q.support → z ∉ C) :
    s ≠ t := by
  intro hst
  subst t
  rcases hsep ({s} : Finset α) (by simp) (by simpa using hvs) with
    ⟨u, hu, hu_not_mem, _q, _hqPath, _hqAvoid⟩
  rcases hu with rfl | rfl
  · exact hu_not_mem (by simp)
  · exact hu_not_mem (by simp)

private lemma exists_minimal_terminal_path_pair_common_card
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t : α}
    (qs : G.Walk v s) (qt : G.Walk v t)
    (hqsPath : qs.IsPath) (hqtPath : qt.IsPath) :
    ∃ pair : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair ≤
        (((qs.support.toFinset ∩ qt.support.toFinset).erase v).card) ∧
      ∀ pair' : G.Path v s × G.Path v t,
        terminalPathPairCommonCard pair ≤ terminalPathPairCommonCard pair' := by
  classical
  let start : G.Path v s × G.Path v t :=
    (⟨qs, hqsPath⟩, ⟨qt, hqtPath⟩)
  obtain ⟨pair, hpair⟩ :=
    (Finset.univ : Finset (G.Path v s × G.Path v t)).exists_minimalFor
      terminalPathPairCommonCard ⟨start, by simp⟩
  refine ⟨pair, ?_, ?_⟩
  · by_cases hle :
        terminalPathPairCommonCard pair ≤ terminalPathPairCommonCard start
    · simpa [terminalPathPairCommonCard, start] using hle
    · have hstart_le_pair :
          terminalPathPairCommonCard start ≤ terminalPathPairCommonCard pair :=
        le_of_not_ge hle
      have hpair_le_start :
          terminalPathPairCommonCard pair ≤ terminalPathPairCommonCard start :=
        hpair.2 (by simp) hstart_le_pair
      simpa [terminalPathPairCommonCard, start] using hpair_le_start
  · intro pair'
    by_cases hle : terminalPathPairCommonCard pair ≤ terminalPathPairCommonCard pair'
    · exact hle
    · exact hpair.2 (by simp) (le_of_not_ge hle)

private lemma exists_minimal_terminal_path_pair_weighted_measure
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t : α}
    (qs : G.Walk v s) (qt : G.Walk v t)
    (hqsPath : qs.IsPath) (hqtPath : qt.IsPath) :
    ∃ pair : G.Path v s × G.Path v t,
      terminalPathPairWeightedMeasure pair ≤
        terminalPathPairWeightedMeasure
          ((⟨qs, hqsPath⟩ : G.Path v s),
            (⟨qt, hqtPath⟩ : G.Path v t)) ∧
      ∀ pair' : G.Path v s × G.Path v t,
        terminalPathPairWeightedMeasure pair ≤
          terminalPathPairWeightedMeasure pair' := by
  classical
  let start : G.Path v s × G.Path v t :=
    (⟨qs, hqsPath⟩, ⟨qt, hqtPath⟩)
  obtain ⟨pair, hpair⟩ :=
    (Finset.univ : Finset (G.Path v s × G.Path v t)).exists_minimalFor
      terminalPathPairWeightedMeasure ⟨start, by simp⟩
  refine ⟨pair, ?_, ?_⟩
  · by_cases hle :
        terminalPathPairWeightedMeasure pair ≤
          terminalPathPairWeightedMeasure start
    · simpa [start] using hle
    · have hstart_le_pair :
          terminalPathPairWeightedMeasure start ≤
            terminalPathPairWeightedMeasure pair :=
        le_of_not_ge hle
      have hpair_le_start :
          terminalPathPairWeightedMeasure pair ≤
            terminalPathPairWeightedMeasure start :=
        hpair.2 (by simp) hstart_le_pair
      simpa [start] using hpair_le_start
  · intro pair'
    by_cases hle :
        terminalPathPairWeightedMeasure pair ≤
          terminalPathPairWeightedMeasure pair'
    · exact hle
    · exact hpair.2 (by simp) (le_of_not_ge hle)

lemma terminal_set_fan_left_first_crossing_splice_commonCard_lt_of_not_retained
    {α : Type*} [DecidableEq α]
    {G : SimpleGraph α} {v s t x w : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (_hrsPath : rs.IsPath)
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rs : x ∉ rs.support)
    (hw_rs : w ∈ rs.support)
    (hw_right : w ∈ (pair.2 : G.Walk v t).support)
    (hw_not_left : w ∉ (pair.1 : G.Walk v s).support)
    (hfirst :
      ∀ z, z ∈ rs.support → z ≠ v →
        z ∈ (pair.1 : G.Walk v s).support ∨
        z ∈ (pair.2 : G.Walk v t).support →
        z = w ∨ z ∉ (rs.takeUntil w hw_rs).support)
    (hx_not_retained :
      x ∉ ((pair.2 : G.Walk v t).dropUntil w hw_right).support) :
    ∃ pair' : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  classical
  let spliceRight : G.Path v t :=
    (((rs.takeUntil w hw_rs).append
      ((pair.2 : G.Walk v t).dropUntil w hw_right)).toPath)
  let spliced : G.Path v s × G.Path v t := (pair.1, spliceRight)
  refine ⟨spliced, ?_⟩
  have hspliceRight_support :
      ∀ z : α, z ∈ (spliceRight : G.Walk v t).support →
        z ∈ rs.support ∨ z ∈ (pair.2 : G.Walk v t).support := by
    intro z hz
    simpa [spliceRight] using
      (mem_support_toPath_append_takeUntil_dropUntil_subset
        (G := G) (p := rs) (q := (pair.2 : G.Walk v t))
        (y := w) (z := z) hw_rs hw_right hz)
  have hx_not_prefix : x ∉ (rs.takeUntil w hw_rs).support := by
    intro hxprefix
    exact hx_rs (Walk.support_takeUntil_subset rs hw_rs hxprefix)
  have hcommon_subset_old :
      ((pair.1 : G.Walk v s).support.toFinset ∩
          (spliceRight : G.Walk v t).support.toFinset).erase v ⊆
        ((pair.1 : G.Walk v s).support.toFinset ∩
          (pair.2 : G.Walk v t).support.toFinset).erase v := by
    intro z hz
    rw [Finset.mem_erase, Finset.mem_inter] at hz
    rw [Finset.mem_erase, Finset.mem_inter]
    rcases hz with ⟨hzv, hz_left, hz_splice⟩
    have hz_splice' : z ∈ (spliceRight : G.Walk v t).support := by
      simpa using hz_splice
    rcases hspliceRight_support z hz_splice' with hzrs | hzright
    · have hfirst_z :=
        hfirst z hzrs hzv (Or.inl (by simpa using hz_left))
      rcases hfirst_z with rfl | hz_not_prefix
      · exact False.elim (hw_not_left (by simpa using hz_left))
      · have hz_append :
            z ∈ ((rs.takeUntil w hw_rs).append
              ((pair.2 : G.Walk v t).dropUntil w hw_right)).support := by
          exact Walk.support_toPath_subset _ hz_splice'
        rw [Walk.mem_support_append_iff] at hz_append
        rcases hz_append with hzprefix | hzdrop
        · exact False.elim (hz_not_prefix hzprefix)
        · exact ⟨hzv, by simpa using hz_left,
            by simpa using
              (Walk.support_dropUntil_subset (pair.2 : G.Walk v t)
                hw_right hzdrop)⟩
    · exact ⟨hzv, by simpa using hz_left, by simpa using hzright⟩
  have hx_not_spliceRight :
      x ∉ (spliceRight : G.Walk v t).support := by
    intro hx_splice
    have hx_append :
        x ∈ ((rs.takeUntil w hw_rs).append
          ((pair.2 : G.Walk v t).dropUntil w hw_right)).support := by
      exact Walk.support_toPath_subset _ hx_splice
    rw [Walk.mem_support_append_iff] at hx_append
    rcases hx_append with hxprefix | hxdrop
    · exact hx_not_prefix hxprefix
    · exact hx_not_retained hxdrop
  have hcommon_subset_old_without_x :
      ((pair.1 : G.Walk v s).support.toFinset ∩
          (spliceRight : G.Walk v t).support.toFinset).erase v ⊆
        (((pair.1 : G.Walk v s).support.toFinset ∩
          (pair.2 : G.Walk v t).support.toFinset).erase v).erase x := by
    intro z hz
    rw [Finset.mem_erase]
    refine ⟨?_, hcommon_subset_old hz⟩
    intro hzx
    rw [Finset.mem_erase, Finset.mem_inter] at hz
    exact hx_not_spliceRight (by simpa [hzx] using hz.2.2)
  simpa [terminalPathPairCommonCard, spliced] using
    (common_support_erase_card_lt_of_subset_erase_common
      (G := G) (v := v) (s := s) (t := t)
      (qs := (pair.1 : G.Walk v s))
      (qt := (pair.2 : G.Walk v t))
      (qs' := (pair.1 : G.Walk v s))
      (qt' := (spliceRight : G.Walk v t))
      (x := x) hcommon_subset_old_without_x hx_left hx_right hxv)

lemma terminal_set_fan_splice_descent_left_of_hsep_of_first_crossing_not_retained
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x w : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (_hsep : ∀ C : Finset α, C.card < 2 → v ∉ C →
      ∃ u : α, (u = s ∨ u = t) ∧ u ∉ C ∧
        ∃ q : G.Walk v u, q.IsPath ∧ ∀ z, z ∈ q.support → z ∉ C)
    (_hpair_measure_min : ∀ pair' : G.Path v s × G.Path v t,
      terminalPathPairWeightedMeasure pair ≤ terminalPathPairWeightedMeasure pair')
    (hrsPath : rs.IsPath)
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rs : x ∉ rs.support)
    (hw_rs : w ∈ rs.support)
    (hw_right : w ∈ (pair.2 : G.Walk v t).support)
    (hw_not_left : w ∉ (pair.1 : G.Walk v s).support)
    (hfirst :
      ∀ z, z ∈ rs.support → z ≠ v →
        z ∈ (pair.1 : G.Walk v s).support ∨
        z ∈ (pair.2 : G.Walk v t).support →
        z = w ∨ z ∉ (rs.takeUntil w hw_rs).support)
    (hx_not_retained :
      x ∉ ((pair.2 : G.Walk v t).dropUntil w hw_right).support) :
    ∃ pair' : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  exact terminal_set_fan_left_first_crossing_splice_commonCard_lt_of_not_retained
    (G := G) (v := v) (s := s) (t := t) (x := x) (w := w)
    (pair := pair) (rs := rs) hrsPath hx_left hx_right hxv hx_rs
    hw_rs hw_right hw_not_left hfirst hx_not_retained

/-
lemma terminal_set_fan_splice_descent_left_of_hsep
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x y : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (_hsep : ∀ C : Finset α, C.card < 2 → v ∉ C →
      ∃ u : α, (u = s ∨ u = t) ∧ u ∉ C ∧
        ∃ q : G.Walk v u, q.IsPath ∧ ∀ z, z ∈ q.support → z ∉ C)
    (_hpair_measure_min : ∀ pair' : G.Path v s × G.Path v t,
      terminalPathPairWeightedMeasure pair ≤ terminalPathPairWeightedMeasure pair')
    (hrsPath : rs.IsPath)
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rs : x ∉ rs.support)
    (_hyrs : y ∈ rs.support)
    (_hy_right : y ∈ (pair.2 : G.Walk v t).support)
    (_hyv : y ≠ v)
    (_hyx : y ≠ x) :
    ∃ pair' : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  classical
  let direct : G.Path v s × G.Path v t := (⟨rs, hrsPath⟩, pair.2)
  by_cases hdirect :
      terminalPathPairCommonCard direct < terminalPathPairCommonCard pair
  · exact ⟨direct, hdirect⟩
  · rcases exists_new_left_replacement_intersection_of_not_commonCard_lt
        (G := G) (v := v) (s := s) (t := t) (x := x)
        (pair := pair) (rs := rs) hrsPath hx_left hx_right hxv hx_rs
        hdirect with
      ⟨y₀, hy₀v, hy₀rs, hy₀right, _hy₀_not_left⟩
    rcases exists_first_nonapex_intersection_on_walk_pair_support
        (G := G) (v := v) (s := s) (t := t)
        (left := (pair.1 : G.Walk v s))
        (right := (pair.2 : G.Walk v t)) (r := rs)
        hy₀rs hy₀right hy₀v with
      ⟨wUnion, hwUnion_rs, _hwUnion_v, _hwUnion_old, hwUnion_first⟩
    have hx_ne_wUnion : x ≠ wUnion := by
      intro hxw
      exact hx_rs (by simpa [hxw] using hwUnion_rs)
    have _hx_not_union_prefix :
        x ∉ (rs.takeUntil wUnion hwUnion_rs).support := by
      exact not_mem_takeUntil_first_pair_support_of_ne
        (G := G) (v := v) (s := s) (t := t) (u := s)
        (left := (pair.1 : G.Walk v s))
        (right := (pair.2 : G.Walk v t)) (r := rs)
        (hw := hwUnion_rs) hwUnion_first hxv (Or.inl hx_left)
        hx_ne_wUnion
    rcases exists_first_nonapex_intersection_on_walk rs (pair.2 : G.Walk v t)
        hy₀rs hy₀right hy₀v with
      ⟨w, hwrs, _hwv, hwright, _hfirstRight⟩
    let spliceRight : G.Path v t :=
      (((rs.takeUntil w hwrs).append
        ((pair.2 : G.Walk v t).dropUntil w hwright)).toPath)
    let spliced : G.Path v s × G.Path v t := (pair.1, spliceRight)
    have _hspliceRight_support :
        ∀ z : α, z ∈ (spliceRight : G.Walk v t).support →
          z ∈ rs.support ∨ z ∈ (pair.2 : G.Walk v t).support := by
      intro z hz
      simpa [spliceRight] using
        (mem_support_toPath_append_takeUntil_dropUntil_subset
          (G := G) (p := rs) (q := (pair.2 : G.Walk v t))
          (y := w) (z := z) hwrs hwright hz)
    have hspliced_descent :
        terminalPathPairCommonCard spliced < terminalPathPairCommonCard pair := by
      exact hdirect
    exact ⟨spliced, hspliced_descent⟩
-/

lemma terminal_set_fan_left_suffix_retention_bad_pivot_descent
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x w z : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hpair_measure_min : ∀ pair' : G.Path v s × G.Path v t,
      terminalPathPairWeightedMeasure pair ≤ terminalPathPairWeightedMeasure pair')
    (hrsPath : rs.IsPath)
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rs : x ∉ rs.support)
    (hw_rs : w ∈ rs.support)
    (hw_right : w ∈ (pair.2 : G.Walk v t).support)
    (hw_not_left : w ∉ (pair.1 : G.Walk v s).support)
    (hwv : w ≠ v)
    (hfirst : ∀ y, y ∈ rs.support → y ≠ v →
      y ∈ (pair.1 : G.Walk v s).support ∨
      y ∈ (pair.2 : G.Walk v t).support →
      y = w ∨ y ∉ (rs.takeUntil w hw_rs).support)
    (hdirect : ¬ terminalPathPairCommonCard
      ((⟨rs, hrsPath⟩ : G.Path v s), pair.2) <
      terminalPathPairCommonCard pair)
    (hret : x ∈ ((pair.2 : G.Walk v t).dropUntil w hw_right).support) :
    let altRight : G.Path v t :=
      (((pair.1 : G.Walk v s).takeUntil x hx_left).append
        ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
    z ∈ rs.support → z ≠ v →
      z ∈ (altRight : G.Walk v t).support →
      ¬ (z ∈ (pair.1 : G.Walk v s).support ∧
         z ∈ (pair.2 : G.Walk v t).support ∧ z ≠ x) →
      ∃ pair' : G.Path v s × G.Path v t,
        terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  classical
  dsimp
  intro hzrs hzv hz_alt hbad
  have hbad_exists :
      let altRight : G.Path v t :=
        (((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
      ∃ z : α, z ∈ rs.support ∧ z ≠ v ∧
        z ∈ (altRight : G.Walk v t).support ∧
        ¬ (z ∈ (pair.1 : G.Walk v s).support ∧
           z ∈ (pair.2 : G.Walk v t).support ∧ z ≠ x) := by
    dsimp
    exact ⟨z, hzrs, hzv, hz_alt, hbad⟩
  rcases exists_first_bad_pivot_on_rs
      (G := G) (v := v) (s := s) (t := t)
      (x := x) (pair := pair) (rs := rs)
      hx_left hx_right hbad_exists with
    ⟨zFirst, hzFirst_rs, hzFirst_v, hzFirst_alt, hzFirst_bad, hfirst_bad⟩
  have hzFirst_old_union :
      zFirst ∈ (pair.1 : G.Walk v s).support ∨
        zFirst ∈ (pair.2 : G.Walk v t).support := by
    simpa using
      (mem_support_toPath_append_takeUntil_dropUntil_subset
        (G := G) (p := (pair.1 : G.Walk v s))
        (q := (pair.2 : G.Walk v t)) (y := x) (z := zFirst)
        hx_left hx_right hzFirst_alt)
  have hzFirst_alt_raw :
      zFirst ∈ (((pair.1 : G.Walk v s).takeUntil x hx_left).append
        ((pair.2 : G.Walk v t).dropUntil x hx_right)).support := by
    exact Walk.support_toPath_subset _ hzFirst_alt
  by_cases hzFirst_left : zFirst ∈ (pair.1 : G.Walk v s).support
  ·
    have hzFirst_pack :=
      first_bad_left_prefix_package
        (G := G) (v := v) (s := s) (t := t)
        (x := x) (w := w) (z := zFirst)
        (pair := pair) (rs := rs)
        hx_left hx_right hx_rs hw_rs hw_not_left hzFirst_rs
        hzFirst_left hzFirst_alt hzFirst_bad hfirst hzFirst_v
    have hzFirst_not_right :
        zFirst ∉ (pair.2 : G.Walk v t).support := hzFirst_pack.1
    have hzFirst_prefix_left :
        zFirst ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support :=
      hzFirst_pack.2.1
    have hzFirst_not_rs_prefix :
        zFirst ∉ (rs.takeUntil w hw_rs).support :=
      hzFirst_pack.2.2
    rcases exists_last_bad_pivot_on_rs
        (G := G) (v := v) (s := s) (t := t)
        (x := x) (pair := pair) (rs := rs)
        hrsPath hx_left hx_right hbad_exists with
      ⟨z, hzrs, hzv, hz_alt, hbad, hlast_bad⟩
    have hno_lower :
        ∀ pair' : G.Path v s × G.Path v t,
          ¬ terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair :=
      not_terminalPathPairCommonCard_lt_of_weighted_min hpair_measure_min
    have hzx : z ≠ x := by
      intro hzx_eq
      exact hx_rs (by simpa [hzx_eq] using hzrs)
    have hz_old_union :
        z ∈ (pair.1 : G.Walk v s).support ∨
          z ∈ (pair.2 : G.Walk v t).support := by
      simpa using
        (mem_support_toPath_append_takeUntil_dropUntil_subset
          (G := G) (p := (pair.1 : G.Walk v s))
          (q := (pair.2 : G.Walk v t)) (y := x) (z := z)
          hx_left hx_right hz_alt)
    have hz_alt_raw :
        z ∈ (((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).support := by
      exact Walk.support_toPath_subset _ hz_alt
    by_cases hz_left : z ∈ (pair.1 : G.Walk v s).support
    · have hz_not_right : z ∉ (pair.2 : G.Walk v t).support := by
        intro hz_right
        exact hbad ⟨hz_left, hz_right, hzx⟩
      have hz_prefix_left :
          z ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support := by
        rw [Walk.mem_support_append_iff] at hz_alt_raw
        rcases hz_alt_raw with hz_prefix | hz_suffix
        · exact hz_prefix
        · exact False.elim
            (hz_not_right
              (Walk.support_dropUntil_subset (pair.2 : G.Walk v t)
                hx_right hz_suffix))
      have hz_not_rs_prefix :
          z ∉ (rs.takeUntil w hw_rs).support := by
        have hfirst_z := hfirst z hzrs hzv (Or.inl hz_left)
        rcases hfirst_z with hzw | hz_not_prefix
        · exact False.elim (hw_not_left (by simpa [hzw] using hz_left))
        · exact hz_not_prefix
      let spliceLeft : G.Path v s :=
        (((pair.1 : G.Walk v s).takeUntil z hz_left).append
          (rs.dropUntil z hzrs)).toPath
      let spliced : G.Path v s × G.Path v t := (spliceLeft, pair.2)
      refine ⟨spliced, ?_⟩
      have hx_not_spliceLeft :
          x ∉ (spliceLeft : G.Walk v s).support := by
        intro hx_splice
        have hx_append :
            x ∈ (((pair.1 : G.Walk v s).takeUntil z hz_left).append
              (rs.dropUntil z hzrs)).support := by
          exact Walk.support_toPath_subset _ hx_splice
        rw [Walk.mem_support_append_iff] at hx_append
        rcases hx_append with hx_prefix | hx_drop
        · exact
            (not_mem_takeUntil_later_of_mem_takeUntil_of_support
              (G := G) (p := (pair.1 : G.Walk v s))
              (x := x) (z := z) hx_left hz_left hz_prefix_left hzx)
            hx_prefix
        · exact hx_rs (Walk.support_dropUntil_subset rs hzrs hx_drop)
      have hspliceLeft_support :
          ∀ y : α, y ∈ (spliceLeft : G.Walk v s).support →
            y ∈ (pair.1 : G.Walk v s).support ∨ y ∈ rs.support := by
        intro y hy
        simpa [spliceLeft] using
          (mem_support_toPath_append_takeUntil_dropUntil_subset
            (G := G) (p := (pair.1 : G.Walk v s)) (q := rs)
            (y := z) (z := y) hz_left hzrs hy)
      have hcommon_subset_old_without_x :
          (((spliceLeft : G.Walk v s).support.toFinset ∩
              (pair.2 : G.Walk v t).support.toFinset).erase v) ⊆
            (((pair.1 : G.Walk v s).support.toFinset ∩
              (pair.2 : G.Walk v t).support.toFinset).erase v).erase x := by
        intro y hy
        rw [Finset.mem_erase, Finset.mem_inter] at hy
        rcases hy with ⟨hyv, hy_splice, hy_right⟩
        have hy_splice_walk : y ∈ (spliceLeft : G.Walk v s).support := by
          simpa using hy_splice
        have hy_append :
            y ∈ (((pair.1 : G.Walk v s).takeUntil z hz_left).append
              (rs.dropUntil z hzrs)).support := by
          exact Walk.support_toPath_subset _ hy_splice_walk
        rw [Walk.mem_support_append_iff] at hy_append
        rcases hy_append with hy_prefix | hy_drop
        · rw [Finset.mem_erase, Finset.mem_erase, Finset.mem_inter]
          have hy_old_left :
              y ∈ (pair.1 : G.Walk v s).support :=
            Walk.support_takeUntil_subset (pair.1 : G.Walk v s) hz_left hy_prefix
          refine ⟨?_, hyv, by simpa using hy_old_left, by simpa using hy_right⟩
          intro hyx
          exact hx_not_spliceLeft (by simpa [hyx] using hy_splice_walk)
        · -- Remaining extremal-pivot obligation: vertices in
          -- `rs.dropUntil z` that still meet the old right path must already be
          -- old common vertices distinct from `x`.
          have hy_rs : y ∈ rs.support :=
            Walk.support_dropUntil_subset rs hzrs hy_drop
          have hfirst_y := hfirst y hy_rs hyv (Or.inr (by simpa using hy_right))
          rcases hfirst_y with hyw | hy_not_rs_prefix
          · have hz_after_w :
                z ∈ (rs.dropUntil w hw_rs).support :=
              mem_dropUntil_of_mem_support_not_takeUntil
                (G := G) rs hw_rs hzrs hz_not_rs_prefix
            have hw_after_z :
                w ∈ (rs.dropUntil z hzrs).support := by
              simpa [hyw] using hy_drop
            have hzw : z ≠ w := by
              intro hzw_eq
              exact hw_not_left (by simpa [hzw_eq] using hz_left)
            exact False.elim
              (not_both_mem_dropUntil_on_simple_path
                (G := G) (p := rs) hrsPath hzrs hw_rs
                hz_after_w hw_after_z hzw)
          · rcases mem_erase_common_without_x_or_not_common_triple
                (G := G) (pair := pair) (x := x) hyv
                (by simpa using hy_right) with hy_old_common | hy_new_bad
            · exact hy_old_common
            · exfalso
              exact terminal_set_fan_left_suffix_retention_left_prefix_residual_bad_false
                (G := G) (v := v) (s := s) (t := t)
                (x := x) (w := w) (z := z) (y := y)
                (pair := pair) (rs := rs)
                hpair_measure_min hrsPath hx_left hx_right hxv hx_rs
                hw_rs hw_right hw_not_left hwv hfirst hdirect hret
                hzrs hzv hz_left hz_not_right hz_prefix_left
                hz_not_rs_prefix hlast_bad hyv hy_drop (by simpa using hy_right)
                hy_new_bad
      simpa [terminalPathPairCommonCard, spliced] using
        (common_support_erase_card_lt_of_subset_erase_common
          (G := G) (v := v) (s := s) (t := t)
          (qs := (pair.1 : G.Walk v s))
          (qt := (pair.2 : G.Walk v t))
          (qs' := (spliceLeft : G.Walk v s))
          (qt' := (pair.2 : G.Walk v t))
          (x := x) hcommon_subset_old_without_x hx_left hx_right hxv)
    · have hz_right : z ∈ (pair.2 : G.Walk v t).support := by
        rcases hz_old_union with hz_left' | hz_right
        · exact False.elim (hz_left hz_left')
        · exact hz_right
      have hz_suffix_right :
          z ∈ ((pair.2 : G.Walk v t).dropUntil x hx_right).support := by
        rw [Walk.mem_support_append_iff] at hz_alt_raw
        rcases hz_alt_raw with hz_prefix | hz_suffix
        · exact False.elim
            (hz_left
              (Walk.support_takeUntil_subset (pair.1 : G.Walk v s)
                hx_left hz_prefix))
        · exact hz_suffix
      have hz_after_first_pack :=
        later_bad_after_first_bad_on_isPath
          (G := G) (v := v) (s := s) (t := t)
          (x := x) (y := zFirst) (z := z)
          (pair := pair) (rs := rs)
          hrsPath hx_left hx_right hzFirst_rs hzrs hzFirst_v hzv
          hzFirst_not_right hz_right hzFirst_alt hz_alt hbad hfirst_bad
      have hz_after_zFirst :
          z ∈ (rs.dropUntil zFirst hzFirst_rs).support :=
        hz_after_first_pack.1
      have hzFirst_prefix_z :
          zFirst ∈ (rs.takeUntil z hzrs).support :=
        hz_after_first_pack.2
      have hzFirst_ne_x : zFirst ≠ x := by
        intro hzxFirst
        exact hx_rs (by simpa [hzxFirst] using hzFirst_rs)
      have hnot_global_bridge_guard :
          ¬ ∀ q : α, q ≠ v →
            q ∈
              (((((pair.2 : G.Walk v t).takeUntil x hx_right).append
                ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath) :
                  G.Walk v s).support →
            q ∈
              ((rs.dropUntil zFirst hzFirst_rs).takeUntil z
                hz_after_zFirst).support →
            q ∈ (pair.1 : G.Walk v s).support ∧
              q ∈ (pair.2 : G.Walk v t).support := by
        intro hbridge_guard
        rcases terminal_set_fan_two_sided_bridge_commonCard_lt_of_middle_guard
            (G := G) (v := v) (s := s) (t := t)
            (x := x) (y := zFirst) (z := z)
            (pair := pair) (rs := rs)
            hx_left hx_right hxv hx_rs hzFirst_left hzFirst_rs
            hz_after_zFirst hz_right hzFirst_prefix_left
            hz_suffix_right hzFirst_ne_x hzx hbridge_guard with
          ⟨pair', hpair'_lt⟩
        exact hno_lower pair' hpair'_lt
      rcases exists_first_bridge_guard_counterexample
          (G := G) (v := v) (s := s) (t := t)
          (x := x) (y := zFirst) (z := z)
          (pair := pair) (rs := rs)
          hx_left hx_right hzFirst_rs hz_after_zFirst
          hnot_global_bridge_guard with
        ⟨qBridge, hqBridge_mid, hqBridge_v, hqBridge_swap,
          hqBridge_not_common, hfirst_bridge_bad⟩
      have hqBridge_tail :
          qBridge ∈ (rs.dropUntil zFirst hzFirst_rs).support :=
        Walk.support_takeUntil_subset
          (rs.dropUntil zFirst hzFirst_rs) hz_after_zFirst hqBridge_mid
      have hqBridge_rs : qBridge ∈ rs.support :=
        Walk.support_dropUntil_subset rs hzFirst_rs hqBridge_tail
      have hqBridge_side :=
        bridge_guard_counterexample_side
          (G := G) (v := v) (s := s) (t := t)
          (x := x) (q := qBridge) (pair := pair)
          hx_left hx_right hqBridge_swap hqBridge_not_common
      have hzFirst_not_swap :
          zFirst ∉
            (((((pair.2 : G.Walk v t).takeUntil x hx_right).append
              ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath) :
                G.Walk v s).support :=
        not_mem_cross_swap_left_of_left_prefix_not_right
          (G := G) (left := (pair.1 : G.Walk v s))
          (right := (pair.2 : G.Walk v t)) pair.1.property
          hx_left hx_right hzFirst_left hzFirst_prefix_left
          hzFirst_not_right hzFirst_ne_x
      have hqBridge_ne_zFirst : qBridge ≠ zFirst := by
        intro hqzFirst
        exact hzFirst_not_swap (by simpa [hqzFirst] using hqBridge_swap)
      have hqBridge_not_rs_prefix_zFirst :
          qBridge ∉ (rs.takeUntil zFirst hzFirst_rs).support :=
        not_mem_takeUntil_of_mem_dropUntil_ne_on_isPath
          (G := G) (p := rs) hrsPath hzFirst_rs hqBridge_rs
          hqBridge_tail hqBridge_ne_zFirst
      have hz_not_swap :
          z ∉
            (((((pair.2 : G.Walk v t).takeUntil x hx_right).append
              ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath) :
                G.Walk v s).support := by
        intro hz_swap
        have hz_swap_raw :
            z ∈ (((pair.2 : G.Walk v t).takeUntil x hx_right).append
              ((pair.1 : G.Walk v s).dropUntil x hx_left)).support :=
          Walk.support_toPath_subset _ hz_swap
        rw [Walk.mem_support_append_iff] at hz_swap_raw
        rcases hz_swap_raw with hz_right_prefix | hz_left_suffix
        · exact
            (not_mem_dropUntil_of_mem_takeUntil_ne_on_isPath
              (G := G) (p := (pair.2 : G.Walk v t))
              pair.2.property hx_right hz_right hz_right_prefix hzx)
            hz_suffix_right
        · exact hz_left
            (Walk.support_dropUntil_subset (pair.1 : G.Walk v s)
              hx_left hz_left_suffix)
      have hqBridge_ne_z : qBridge ≠ z := by
        intro hqz
        exact hz_not_swap (by simpa [hqz] using hqBridge_swap)
      have hqBridge_prefix_z :
          qBridge ∈ (rs.takeUntil z hzrs).support :=
        mem_takeUntil_of_mem_dropUntil_takeUntil_ne_on_isPath
          (G := G) (p := rs) hrsPath hzFirst_rs hzrs
          hz_after_zFirst hqBridge_mid hqBridge_ne_z
      have hz_tail_qBridge :
          z ∈ (rs.dropUntil qBridge hqBridge_rs).support :=
        mem_dropUntil_of_mem_takeUntil_ne
          (G := G) rs hqBridge_rs hzrs hqBridge_prefix_z hqBridge_ne_z
      have hqBridge_right_prefix_stage_guard_false
          (hq_right_prefix :
            qBridge ∈ (pair.2 : G.Walk v t).support ∧
              qBridge ∉ (pair.1 : G.Walk v s).support ∧
              qBridge ∈
                ((pair.2 : G.Walk v t).takeUntil x hx_right).support)
          (hsegment_left_guard :
            ∀ y0 : α, y0 ≠ v →
              y0 ∈ (pair.1 : G.Walk v s).support →
              y0 ∈
                ((rs.dropUntil qBridge hqBridge_rs).takeUntil z
                  (mem_dropUntil_of_mem_takeUntil_ne
                    (G := G) rs hqBridge_rs hzrs hqBridge_prefix_z
                    hqBridge_ne_z)).support →
              y0 ∈ (pair.2 : G.Walk v t).support) :
          False := by
        rcases terminal_set_fan_bridge_right_prefix_stage_commonCard_lt
            (G := G) (v := v) (s := s) (t := t)
            (x := x) (a := qBridge) (z := z)
            (pair := pair) (rs := rs)
            hx_left hx_right hxv hx_rs hq_right_prefix.1 hqBridge_rs
            hz_right hzrs hq_right_prefix.2.2 hz_suffix_right
            hqBridge_prefix_z hqBridge_ne_z hzx hsegment_left_guard with
          ⟨pair', hpair'_lt⟩
        exact hno_lower pair' hpair'_lt
      have hqBridge_left_suffix_stage_guard_false
          (hq_left_suffix :
            qBridge ∈ (pair.1 : G.Walk v s).support ∧
              qBridge ∉ (pair.2 : G.Walk v t).support ∧
              qBridge ∈
                ((pair.1 : G.Walk v s).dropUntil x hx_left).support)
          (hsegment_right_guard :
            ∀ r : α, r ≠ v →
              r ∈ (pair.2 : G.Walk v t).support →
              r ∈
                ((rs.dropUntil zFirst hzFirst_rs).takeUntil qBridge
                  hqBridge_tail).support →
              r ∈ (pair.1 : G.Walk v s).support) :
          False := by
        rcases terminal_set_fan_bridge_left_suffix_stage_commonCard_lt
            (G := G) (v := v) (s := s) (t := t)
            (x := x) (y := zFirst) (a := qBridge)
            (pair := pair) (rs := rs)
            hx_left hx_right hxv hx_rs hzFirst_left hzFirst_rs
            hq_left_suffix.1 hqBridge_rs hqBridge_tail
            hzFirst_prefix_left hq_left_suffix.2.2 hzFirst_ne_x
            hsegment_right_guard with
          ⟨pair', hpair'_lt⟩
        exact hno_lower pair' hpair'_lt
      have hqBridge_stage_witness :
          (∃ hright :
              qBridge ∈ (pair.2 : G.Walk v t).support ∧
                qBridge ∉ (pair.1 : G.Walk v s).support ∧
                qBridge ∈
                  ((pair.2 : G.Walk v t).takeUntil x hx_right).support,
            ∃ b : α,
            ∃ hb_mid :
              b ∈ ((rs.dropUntil qBridge hqBridge_rs).takeUntil z
                hz_tail_qBridge).support,
              b ≠ v ∧
              b ∈ (pair.1 : G.Walk v s).support ∧
              b ∉ (pair.2 : G.Walk v t).support ∧
              ∀ r : α, r ≠ v →
                r ∈ (pair.1 : G.Walk v s).support →
                r ∉ (pair.2 : G.Walk v t).support →
                r ∈
                  (((rs.dropUntil qBridge hqBridge_rs).takeUntil z
                    hz_tail_qBridge).takeUntil b hb_mid).support →
                r = b) ∨
          (∃ hleft :
              qBridge ∈ (pair.1 : G.Walk v s).support ∧
                qBridge ∉ (pair.2 : G.Walk v t).support ∧
                qBridge ∈
                  ((pair.1 : G.Walk v s).dropUntil x hx_left).support,
            ∃ r : α,
            ∃ hr_mid :
              r ∈ ((rs.dropUntil zFirst hzFirst_rs).takeUntil qBridge
                hqBridge_tail).support,
              r ≠ v ∧
              r ∈ (pair.2 : G.Walk v t).support ∧
              r ∉ (pair.1 : G.Walk v s).support ∧
              ∀ q : α, q ≠ v →
                q ∈ (pair.2 : G.Walk v t).support →
                q ∉ (pair.1 : G.Walk v s).support →
                q ∈
                  (((rs.dropUntil zFirst hzFirst_rs).takeUntil qBridge
                    hqBridge_tail).takeUntil r hr_mid).support →
                q = r) := by
        rcases hqBridge_side with hright | hleft
        · left
          have hnot_segment_left_guard :
              ¬ ∀ y0 : α, y0 ≠ v →
                y0 ∈ (pair.1 : G.Walk v s).support →
                y0 ∈ ((rs.dropUntil qBridge hqBridge_rs).takeUntil z
                  hz_tail_qBridge).support →
                y0 ∈ (pair.2 : G.Walk v t).support := by
            intro hguard
            exact hqBridge_right_prefix_stage_guard_false hright
              (by simpa [hz_tail_qBridge] using hguard)
          rcases exists_first_segment_left_only_of_not_segment_left_guard
              (G := G) (v := v) (s := s) (t := t)
              (a := qBridge) (z := z) (pair := pair) (rs := rs)
              (ha_rs := hqBridge_rs) (hz_tail := hz_tail_qBridge)
              hnot_segment_left_guard with
            ⟨b, hb_mid, hbv, hb_left, hb_not_right, hb_first⟩
          exact ⟨hright, b, hb_mid, hbv, hb_left, hb_not_right, hb_first⟩
        · right
          have hnot_segment_right_guard :
              ¬ ∀ r : α, r ≠ v →
                r ∈ (pair.2 : G.Walk v t).support →
                r ∈
                  ((rs.dropUntil zFirst hzFirst_rs).takeUntil qBridge
                    hqBridge_tail).support →
                r ∈ (pair.1 : G.Walk v s).support := by
            intro hguard
            exact hqBridge_left_suffix_stage_guard_false hleft hguard
          rcases exists_first_segment_right_only_of_not_segment_right_guard
              (G := G) (v := v) (s := s) (t := t)
              (a := zFirst) (z := qBridge) (pair := pair) (rs := rs)
              (ha_rs := hzFirst_rs) (hz_tail := hqBridge_tail)
              hnot_segment_right_guard with
            ⟨r, hr_mid, hrv, hr_right, hr_not_left, hr_first⟩
          exact ⟨hleft, r, hr_mid, hrv, hr_right, hr_not_left, hr_first⟩
      have hqBridge_stage_obstruction :
          (∃ hright :
              qBridge ∈ (pair.2 : G.Walk v t).support ∧
                qBridge ∉ (pair.1 : G.Walk v s).support ∧
                qBridge ∈
                  ((pair.2 : G.Walk v t).takeUntil x hx_right).support,
            ∃ b : α,
            ∃ hb_mid :
              b ∈ ((rs.dropUntil qBridge hqBridge_rs).takeUntil z
                hz_tail_qBridge).support,
              b ≠ v ∧
              b ∈ (pair.1 : G.Walk v s).support ∧
              b ∉ (pair.2 : G.Walk v t).support ∧
              b ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support ∧
              ∀ r : α, r ≠ v →
                r ∈ (pair.1 : G.Walk v s).support →
                r ∉ (pair.2 : G.Walk v t).support →
                r ∈
                  (((rs.dropUntil qBridge hqBridge_rs).takeUntil z
                    hz_tail_qBridge).takeUntil b hb_mid).support →
                r = b) ∨
          (∃ hleft :
              qBridge ∈ (pair.1 : G.Walk v s).support ∧
                qBridge ∉ (pair.2 : G.Walk v t).support ∧
                qBridge ∈
                  ((pair.1 : G.Walk v s).dropUntil x hx_left).support,
            ∃ r : α,
            ∃ hr_mid :
              r ∈ ((rs.dropUntil zFirst hzFirst_rs).takeUntil qBridge
                hqBridge_tail).support,
              r ≠ v ∧
              r ∈ (pair.2 : G.Walk v t).support ∧
              r ∉ (pair.1 : G.Walk v s).support ∧
              r ∈ ((pair.2 : G.Walk v t).takeUntil x hx_right).support ∧
              ∀ q : α, q ≠ v →
                q ∈ (pair.2 : G.Walk v t).support →
                q ∉ (pair.1 : G.Walk v s).support →
                q ∈
                  (((rs.dropUntil zFirst hzFirst_rs).takeUntil qBridge
                    hqBridge_tail).takeUntil r hr_mid).support →
                q = r) := by
        rcases hqBridge_stage_witness with hright_stage | hleft_stage
        · rcases hright_stage with
            ⟨hright, b, hb_mid, hbv, hb_left, hb_not_right, hb_first⟩
          have hb_pos :=
            mem_takeUntil_or_mem_dropUntil_of_mem_support
              (G := G) (p := (pair.1 : G.Walk v s))
              hx_left hb_left
          rcases hb_pos with hb_prefix_x | hb_suffix_x
          · exact Or.inl
              ⟨hright, b, hb_mid, hbv, hb_left, hb_not_right,
                hb_prefix_x, hb_first⟩
          · rcases
              terminal_set_fan_right_prefix_stage_left_suffix_witness_commonCard_lt
                (G := G) (v := v) (s := s) (t := t)
                (x := x) (a := qBridge) (z := z) (b := b)
                (pair := pair) (rs := rs)
                hx_left hx_right hxv hx_rs hright.1 hright.2.1
                hqBridge_rs hright.2.2 hz_right hz_tail_qBridge
                hz_suffix_right hb_mid hbv hb_left hb_not_right
                hb_first hb_suffix_x with
              ⟨pair', hpair'_lt⟩
            exact False.elim (hno_lower pair' hpair'_lt)
        · rcases hleft_stage with
            ⟨hleft, r, hr_mid, hrv, hr_right, hr_not_left, hr_first⟩
          have hr_pos :=
            mem_takeUntil_or_mem_dropUntil_of_mem_support
              (G := G) (p := (pair.2 : G.Walk v t))
              hx_right hr_right
          rcases hr_pos with hr_prefix_x | hr_suffix_x
          · rcases
              terminal_set_fan_left_suffix_stage_right_prefix_witness_commonCard_lt
                (G := G) (v := v) (s := s) (t := t)
                (x := x) (y := zFirst) (a := qBridge) (z := z)
                (r := r) (pair := pair) (rs := rs)
                hx_left hx_right hxv hzFirst_rs hqBridge_tail
                hz_after_zFirst hqBridge_mid hleft.2.1 hr_mid hrv
                hr_right hr_not_left hr_prefix_x hfirst_bridge_bad with
              ⟨pair', hpair'_lt⟩
            exact False.elim (hno_lower pair' hpair'_lt)
          · rcases
              terminal_set_fan_left_suffix_stage_right_suffix_witness_commonCard_lt
                (G := G) (v := v) (s := s) (t := t)
                (x := x) (y := zFirst) (a := qBridge) (z := z)
                (r := r) (pair := pair) (rs := rs)
                hx_left hx_right hxv hx_rs hzFirst_left hzFirst_rs
                hzFirst_prefix_left hqBridge_tail hz_after_zFirst
                hqBridge_mid hleft.2.1 hr_mid hrv hr_right hr_not_left
                hr_suffix_x hfirst_bridge_bad with
              ⟨pair', hpair'_lt⟩
            exact False.elim (hno_lower pair' hpair'_lt)
      have hqBridge_right_prefix_front_obstruction :
          ∃ hright :
              qBridge ∈ (pair.2 : G.Walk v t).support ∧
                qBridge ∉ (pair.1 : G.Walk v s).support ∧
                qBridge ∈
                  ((pair.2 : G.Walk v t).takeUntil x hx_right).support,
            ∃ b : α,
            ∃ hb_mid :
              b ∈ ((rs.dropUntil qBridge hqBridge_rs).takeUntil z
                hz_tail_qBridge).support,
              b ≠ v ∧
              b ∈ (pair.1 : G.Walk v s).support ∧
              b ∉ (pair.2 : G.Walk v t).support ∧
              b ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support ∧
              ∀ r : α, r ≠ v →
                r ∈ (pair.1 : G.Walk v s).support →
                r ∉ (pair.2 : G.Walk v t).support →
                r ∈
                  (((rs.dropUntil qBridge hqBridge_rs).takeUntil z
                    hz_tail_qBridge).takeUntil b hb_mid).support →
                r = b := by
        rcases hqBridge_stage_obstruction with hright_obstruction | hleft_obstruction
        · exact hright_obstruction
        · rcases hleft_obstruction with
            ⟨hleft, r, hr_mid, hrv, hr_right, hr_not_left,
              hr_prefix_x, _hr_first⟩
          rcases
            terminal_set_fan_left_suffix_stage_right_prefix_witness_commonCard_lt
              (G := G) (v := v) (s := s) (t := t)
              (x := x) (y := zFirst) (a := qBridge) (z := z)
              (r := r) (pair := pair) (rs := rs)
              hx_left hx_right hxv hzFirst_rs hqBridge_tail
              hz_after_zFirst hqBridge_mid hleft.2.1 hr_mid hrv
              hr_right hr_not_left hr_prefix_x hfirst_bridge_bad with
            ⟨pair', hpair'_lt⟩
          exact False.elim (hno_lower pair' hpair'_lt)
      have hqBridge_right_prefix_front_alt_obstruction :
          ∃ hright :
              qBridge ∈ (pair.2 : G.Walk v t).support ∧
                qBridge ∉ (pair.1 : G.Walk v s).support ∧
                qBridge ∈
                  ((pair.2 : G.Walk v t).takeUntil x hx_right).support,
            ∃ b : α,
            ∃ hb_mid :
              b ∈ ((rs.dropUntil qBridge hqBridge_rs).takeUntil z
                hz_tail_qBridge).support,
              b ≠ v ∧
              b ∈ (pair.1 : G.Walk v s).support ∧
              b ∉ (pair.2 : G.Walk v t).support ∧
              b ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support ∧
              b ∈
                (((((pair.1 : G.Walk v s).takeUntil x hx_left).append
                  ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath) :
                    G.Walk v t).support ∧
              ∀ r : α, r ≠ v →
                r ∈ (pair.1 : G.Walk v s).support →
                r ∉ (pair.2 : G.Walk v t).support →
                r ∈
                  (((rs.dropUntil qBridge hqBridge_rs).takeUntil z
                    hz_tail_qBridge).takeUntil b hb_mid).support →
                r = b := by
        rcases hqBridge_right_prefix_front_obstruction with
          ⟨hright, b, hb_mid, hbv, hb_left, hb_not_right, hb_prefix_x,
            hb_first⟩
        by_cases hb_alt :
            b ∈
              (((((pair.1 : G.Walk v s).takeUntil x hx_left).append
                ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath) :
                  G.Walk v t).support
        · exact
            ⟨hright, b, hb_mid, hbv, hb_left, hb_not_right,
              hb_prefix_x, hb_alt, hb_first⟩
        · rcases
            terminal_set_cross_swap_commonCard_lt_of_left_prefix_absent_altRight
              (G := G) (v := v) (s := s) (t := t)
              (x := x) (y := b) (pair := pair)
              hx_left hx_right hxv hb_prefix_x hb_alt with
            ⟨pair', hpair'_lt⟩
          exact False.elim (hno_lower pair' hpair'_lt)
      have hqBridge_front_alt_order_package :
          ∃ hright :
              qBridge ∈ (pair.2 : G.Walk v t).support ∧
                qBridge ∉ (pair.1 : G.Walk v s).support ∧
                qBridge ∈
                  ((pair.2 : G.Walk v t).takeUntil x hx_right).support,
            ∃ b : α,
            ∃ hb_mid :
              b ∈ ((rs.dropUntil qBridge hqBridge_rs).takeUntil z
                hz_tail_qBridge).support,
              ∃ hb_rs : b ∈ rs.support,
              b ≠ v ∧
              b ≠ qBridge ∧
              b ≠ z ∧
              b ∈ (rs.dropUntil qBridge hqBridge_rs).support ∧
              qBridge ∈ (rs.takeUntil b hb_rs).support ∧
              b ∈ (rs.takeUntil z hzrs).support ∧
              b ∈ (pair.1 : G.Walk v s).support ∧
              b ∉ (pair.2 : G.Walk v t).support ∧
              b ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support ∧
              b ∈
                (((((pair.1 : G.Walk v s).takeUntil x hx_left).append
                  ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath) :
                    G.Walk v t).support ∧
              ∀ r : α, r ≠ v →
                r ∈ (pair.1 : G.Walk v s).support →
                r ∉ (pair.2 : G.Walk v t).support →
                r ∈
                  (((rs.dropUntil qBridge hqBridge_rs).takeUntil z
                    hz_tail_qBridge).takeUntil b hb_mid).support →
                r = b := by
        rcases hqBridge_right_prefix_front_alt_obstruction with
          ⟨hright, b, hb_mid, hbv, hb_left, hb_not_right, hb_prefix_x,
            hb_alt, hb_first⟩
        have hb_tail_qBridge :
            b ∈ (rs.dropUntil qBridge hqBridge_rs).support :=
          Walk.support_takeUntil_subset
            (rs.dropUntil qBridge hqBridge_rs) hz_tail_qBridge hb_mid
        have hb_rs : b ∈ rs.support :=
          Walk.support_dropUntil_subset rs hqBridge_rs hb_tail_qBridge
        have hb_ne_qBridge : b ≠ qBridge := by
          intro hbq
          exact hright.2.1 (by simpa [hbq] using hb_left)
        have hb_ne_z : b ≠ z := by
          intro hbz
          exact hb_not_right (by simpa [hbz] using hz_right)
        have hqBridge_prefix_b :
            qBridge ∈ (rs.takeUntil b hb_rs).support :=
          mem_takeUntil_of_mem_dropUntil_ne_on_isPath
            (G := G) (p := rs) hrsPath hqBridge_rs hb_rs
            hb_tail_qBridge hb_ne_qBridge.symm
        have hb_prefix_z :
            b ∈ (rs.takeUntil z hzrs).support := by
          exact mem_takeUntil_of_mem_dropUntil_takeUntil_ne_on_isPath
            (G := G) (p := rs) hrsPath hqBridge_rs hzrs
            hz_tail_qBridge hb_mid hb_ne_z
        exact
          ⟨hright, b, hb_mid, hb_rs, hbv, hb_ne_qBridge, hb_ne_z,
            hb_tail_qBridge, hqBridge_prefix_b, hb_prefix_z, hb_left,
            hb_not_right, hb_prefix_x, hb_alt, hb_first⟩
      have hqBridge_front_next_bridge_package :
          ∃ hright :
              qBridge ∈ (pair.2 : G.Walk v t).support ∧
                qBridge ∉ (pair.1 : G.Walk v s).support ∧
                qBridge ∈
                  ((pair.2 : G.Walk v t).takeUntil x hx_right).support,
            ∃ b : α,
            ∃ hb_mid :
              b ∈ ((rs.dropUntil qBridge hqBridge_rs).takeUntil z
                hz_tail_qBridge).support,
            ∃ hb_rs : b ∈ rs.support,
            ∃ hz_tail_b : z ∈ (rs.dropUntil b hb_rs).support,
              b ≠ v ∧
              b ≠ qBridge ∧
              b ≠ z ∧
              b ∈ (rs.dropUntil qBridge hqBridge_rs).support ∧
              qBridge ∈ (rs.takeUntil b hb_rs).support ∧
              b ∈ (rs.takeUntil z hzrs).support ∧
              b ∈ (pair.1 : G.Walk v s).support ∧
              b ∉ (pair.2 : G.Walk v t).support ∧
              b ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support ∧
              b ∈
                (((((pair.1 : G.Walk v s).takeUntil x hx_left).append
                  ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath) :
                    G.Walk v t).support ∧
              (∃ qNext : α,
              ∃ hqNext_mid :
                qNext ∈ ((rs.dropUntil b hb_rs).takeUntil z
                  hz_tail_b).support,
                qNext ≠ v ∧
                qNext ∈
                  (((((pair.2 : G.Walk v t).takeUntil x hx_right).append
                    ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath) :
                      G.Walk v s).support ∧
                ¬ (qNext ∈ (pair.1 : G.Walk v s).support ∧
                  qNext ∈ (pair.2 : G.Walk v t).support) ∧
                ∀ r : α, r ≠ v →
                  r ∈
                    (((((pair.2 : G.Walk v t).takeUntil x hx_right).append
                      ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath) :
                        G.Walk v s).support →
                  ¬ (r ∈ (pair.1 : G.Walk v s).support ∧
                    r ∈ (pair.2 : G.Walk v t).support) →
                  r ∈
                    (((rs.dropUntil b hb_rs).takeUntil z
                      hz_tail_b).takeUntil qNext hqNext_mid).support →
                  r = qNext) := by
        rcases hqBridge_front_alt_order_package with
          ⟨hright, b, hb_mid, hb_rs, hbv, hb_ne_qBridge, hb_ne_z,
            hb_tail_qBridge, hqBridge_prefix_b, hb_prefix_z, hb_left,
            hb_not_right, hb_prefix_x, hb_alt, _hb_first⟩
        have hz_tail_b : z ∈ (rs.dropUntil b hb_rs).support :=
          mem_dropUntil_of_mem_takeUntil_ne
            (G := G) rs hb_rs hzrs hb_prefix_z hb_ne_z
        have hbx : b ≠ x := by
          intro hbx_eq
          exact hb_not_right (by simpa [hbx_eq] using hx_right)
        have hnot_bridge_guard_bz :
            ¬ ∀ q : α, q ≠ v →
              q ∈
                (((((pair.2 : G.Walk v t).takeUntil x hx_right).append
                  ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath) :
                    G.Walk v s).support →
              q ∈ ((rs.dropUntil b hb_rs).takeUntil z hz_tail_b).support →
              q ∈ (pair.1 : G.Walk v s).support ∧
                q ∈ (pair.2 : G.Walk v t).support := by
          intro hguard
          rcases terminal_set_fan_two_sided_bridge_commonCard_lt_of_middle_guard
              (G := G) (v := v) (s := s) (t := t)
              (x := x) (y := b) (z := z)
              (pair := pair) (rs := rs)
              hx_left hx_right hxv hx_rs hb_left hb_rs hz_tail_b
              hz_right hb_prefix_x hz_suffix_right hbx hzx hguard with
            ⟨pair', hpair'_lt⟩
          exact hno_lower pair' hpair'_lt
        rcases exists_first_bridge_guard_counterexample
            (G := G) (v := v) (s := s) (t := t)
            (x := x) (y := b) (z := z)
            (pair := pair) (rs := rs)
            hx_left hx_right hb_rs hz_tail_b hnot_bridge_guard_bz with
          ⟨qNext, hqNext_mid, hqNext_v, hqNext_swap,
            hqNext_not_common, hqNext_first⟩
        exact
          ⟨hright, b, hb_mid, hb_rs, hz_tail_b, hbv, hb_ne_qBridge,
            hb_ne_z, hb_tail_qBridge, hqBridge_prefix_b, hb_prefix_z,
            hb_left, hb_not_right, hb_prefix_x, hb_alt, qNext,
            hqNext_mid, hqNext_v, hqNext_swap, hqNext_not_common,
            hqNext_first⟩
      have hqBridge_front_next_bridge_side_package :
          ∃ hright :
              qBridge ∈ (pair.2 : G.Walk v t).support ∧
                qBridge ∉ (pair.1 : G.Walk v s).support ∧
                qBridge ∈
                  ((pair.2 : G.Walk v t).takeUntil x hx_right).support,
            ∃ b : α,
            ∃ hb_rs : b ∈ rs.support,
            ∃ hz_tail_b : z ∈ (rs.dropUntil b hb_rs).support,
            ∃ qNext : α,
            ∃ hqNext_mid :
              qNext ∈ ((rs.dropUntil b hb_rs).takeUntil z
                hz_tail_b).support,
              b ≠ v ∧
              b ∈ (pair.1 : G.Walk v s).support ∧
              b ∉ (pair.2 : G.Walk v t).support ∧
              b ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support ∧
              b ∉
                (((((pair.2 : G.Walk v t).takeUntil x hx_right).append
                  ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath) :
                    G.Walk v s).support ∧
              qNext ≠ v ∧
              qNext ≠ b ∧
              qNext ∈ rs.support ∧
              qNext ∈
                (((((pair.2 : G.Walk v t).takeUntil x hx_right).append
                  ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath) :
                    G.Walk v s).support ∧
              ¬ (qNext ∈ (pair.1 : G.Walk v s).support ∧
                qNext ∈ (pair.2 : G.Walk v t).support) ∧
              ((qNext ∈ (pair.2 : G.Walk v t).support ∧
                  qNext ∉ (pair.1 : G.Walk v s).support ∧
                  qNext ∈
                    ((pair.2 : G.Walk v t).takeUntil x hx_right).support) ∨
                (qNext ∈ (pair.1 : G.Walk v s).support ∧
                  qNext ∉ (pair.2 : G.Walk v t).support ∧
                  qNext ∈
                    ((pair.1 : G.Walk v s).dropUntil x hx_left).support)) := by
        rcases hqBridge_front_next_bridge_package with
          ⟨hright, b, _hb_mid, hb_rs, hz_tail_b, hbv, _hb_ne_qBridge,
            _hb_ne_z, _hb_tail_qBridge, _hqBridge_prefix_b, _hb_prefix_z,
            hb_left, hb_not_right, hb_prefix_x, _hb_alt, qNext,
            hqNext_mid, hqNext_v, hqNext_swap, hqNext_not_common,
            _hqNext_first⟩
        have hbx : b ≠ x := by
          intro hbx_eq
          exact hb_not_right (by simpa [hbx_eq] using hx_right)
        have hb_not_swap :
            b ∉
              (((((pair.2 : G.Walk v t).takeUntil x hx_right).append
                ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath) :
                  G.Walk v s).support :=
          not_mem_cross_swap_left_of_left_prefix_not_right
            (G := G) (left := (pair.1 : G.Walk v s))
            (right := (pair.2 : G.Walk v t)) pair.1.property
            hx_left hx_right hb_left hb_prefix_x hb_not_right hbx
        have hqNext_ne_b : qNext ≠ b := by
          intro hqb
          exact hb_not_swap (by simpa [hqb] using hqNext_swap)
        have hqNext_tail_b :
            qNext ∈ (rs.dropUntil b hb_rs).support :=
          Walk.support_takeUntil_subset
            (rs.dropUntil b hb_rs) hz_tail_b hqNext_mid
        have hqNext_rs : qNext ∈ rs.support :=
          Walk.support_dropUntil_subset rs hb_rs hqNext_tail_b
        have hqNext_side :=
          bridge_guard_counterexample_side
            (G := G) (v := v) (s := s) (t := t)
            (x := x) (q := qNext) (pair := pair)
            hx_left hx_right hqNext_swap hqNext_not_common
        exact
          ⟨hright, b, hb_rs, hz_tail_b, qNext, hqNext_mid, hbv,
            hb_left, hb_not_right, hb_prefix_x, hb_not_swap, hqNext_v,
            hqNext_ne_b, hqNext_rs, hqNext_swap, hqNext_not_common,
            hqNext_side⟩
      have hqBridge_front_next_stage_witness :
          ∃ hright :
              qBridge ∈ (pair.2 : G.Walk v t).support ∧
                qBridge ∉ (pair.1 : G.Walk v s).support ∧
                qBridge ∈
                  ((pair.2 : G.Walk v t).takeUntil x hx_right).support,
            ∃ b : α,
            ∃ hb_rs : b ∈ rs.support,
            ∃ qNext : α,
            ∃ hqNext_tail_b : qNext ∈ (rs.dropUntil b hb_rs).support,
              b ≠ v ∧
              b ∈ (pair.1 : G.Walk v s).support ∧
              b ∉ (pair.2 : G.Walk v t).support ∧
              b ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support ∧
              qNext ≠ v ∧
              qNext ≠ b ∧
              qNext ∈ rs.support ∧
              qNext ∈
                (((((pair.2 : G.Walk v t).takeUntil x hx_right).append
                  ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath) :
                    G.Walk v s).support ∧
              ¬ (qNext ∈ (pair.1 : G.Walk v s).support ∧
                qNext ∈ (pair.2 : G.Walk v t).support) ∧
              ((qNext ∈ (pair.2 : G.Walk v t).support ∧
                  qNext ∉ (pair.1 : G.Walk v s).support ∧
                  qNext ∈
                    ((pair.2 : G.Walk v t).takeUntil x hx_right).support) ∨
                (∃ r2 : α,
                ∃ hr2_mid :
                  r2 ∈ ((rs.dropUntil b hb_rs).takeUntil qNext
                    hqNext_tail_b).support,
                  r2 ≠ v ∧
                  r2 ∈ (pair.2 : G.Walk v t).support ∧
                  r2 ∉ (pair.1 : G.Walk v s).support ∧
                  ∀ q : α, q ≠ v →
                    q ∈ (pair.2 : G.Walk v t).support →
                    q ∉ (pair.1 : G.Walk v s).support →
                    q ∈
                      (((rs.dropUntil b hb_rs).takeUntil qNext
                        hqNext_tail_b).takeUntil r2 hr2_mid).support →
                    q = r2)) := by
        rcases hqBridge_front_next_bridge_side_package with
          ⟨hright, b, hb_rs, _hz_tail_b, qNext, hqNext_mid, hbv,
            hb_left, hb_not_right, hb_prefix_x, _hb_not_swap, hqNext_v,
            hqNext_ne_b, hqNext_rs, hqNext_swap, hqNext_not_common,
            hqNext_side⟩
        have hqNext_tail_b :
            qNext ∈ (rs.dropUntil b hb_rs).support :=
          Walk.support_takeUntil_subset
            (rs.dropUntil b hb_rs) _hz_tail_b hqNext_mid
        have hbx : b ≠ x := by
          intro hbx_eq
          exact hb_not_right (by simpa [hbx_eq] using hx_right)
        rcases hqNext_side with hqNext_right_prefix | hqNext_left_suffix
        · exact
            ⟨hright, b, hb_rs, qNext, hqNext_tail_b, hbv, hb_left,
              hb_not_right, hb_prefix_x, hqNext_v, hqNext_ne_b,
              hqNext_rs, hqNext_swap, hqNext_not_common,
              Or.inl hqNext_right_prefix⟩
        · have hnot_segment_right_guard :
              ¬ ∀ r : α, r ≠ v →
                r ∈ (pair.2 : G.Walk v t).support →
                r ∈ ((rs.dropUntil b hb_rs).takeUntil qNext
                  hqNext_tail_b).support →
                r ∈ (pair.1 : G.Walk v s).support := by
            intro hguard
            rcases terminal_set_fan_bridge_left_suffix_stage_commonCard_lt
                (G := G) (v := v) (s := s) (t := t)
                (x := x) (y := b) (a := qNext)
                (pair := pair) (rs := rs)
                hx_left hx_right hxv hx_rs hb_left hb_rs
                hqNext_left_suffix.1 hqNext_rs hqNext_tail_b
                hb_prefix_x hqNext_left_suffix.2.2 hbx hguard with
              ⟨pair', hpair'_lt⟩
            exact hno_lower pair' hpair'_lt
          rcases exists_first_segment_right_only_of_not_segment_right_guard
              (G := G) (v := v) (s := s) (t := t)
              (a := b) (z := qNext) (pair := pair) (rs := rs)
              (ha_rs := hb_rs) (hz_tail := hqNext_tail_b)
              hnot_segment_right_guard with
            ⟨r2, hr2_mid, hr2v, hr2_right, hr2_not_left, hr2_first⟩
          exact
            ⟨hright, b, hb_rs, qNext, hqNext_tail_b, hbv, hb_left,
              hb_not_right, hb_prefix_x, hqNext_v, hqNext_ne_b,
              hqNext_rs, hqNext_swap, hqNext_not_common,
              Or.inr
                ⟨r2, hr2_mid, hr2v, hr2_right, hr2_not_left,
                  hr2_first⟩⟩
      have hqBridge_front_next_right_prefix_package :
          ∃ hright :
              qBridge ∈ (pair.2 : G.Walk v t).support ∧
                qBridge ∉ (pair.1 : G.Walk v s).support ∧
                qBridge ∈
                  ((pair.2 : G.Walk v t).takeUntil x hx_right).support,
            ∃ b : α,
            ∃ hb_rs : b ∈ rs.support,
            ∃ hz_tail_b : z ∈ (rs.dropUntil b hb_rs).support,
            ∃ qNext : α,
            ∃ hqNext_mid :
              qNext ∈ ((rs.dropUntil b hb_rs).takeUntil z
                hz_tail_b).support,
              b ≠ v ∧
              b ∈ (pair.1 : G.Walk v s).support ∧
              b ∉ (pair.2 : G.Walk v t).support ∧
              b ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support ∧
              qNext ≠ v ∧
              qNext ≠ b ∧
              qNext ∈ rs.support ∧
              qNext ∈
                (((((pair.2 : G.Walk v t).takeUntil x hx_right).append
                  ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath) :
                    G.Walk v s).support ∧
              ¬ (qNext ∈ (pair.1 : G.Walk v s).support ∧
                qNext ∈ (pair.2 : G.Walk v t).support) ∧
              qNext ∈ (pair.2 : G.Walk v t).support ∧
              qNext ∉ (pair.1 : G.Walk v s).support ∧
              qNext ∈
                ((pair.2 : G.Walk v t).takeUntil x hx_right).support := by
        rcases hqBridge_front_next_bridge_package with
          ⟨hright, b, _hb_mid, hb_rs, hz_tail_b, hbv, _hb_ne_qBridge,
            _hb_ne_z, _hb_tail_qBridge, _hqBridge_prefix_b, _hb_prefix_z,
            hb_left, hb_not_right, hb_prefix_x, _hb_alt, qNext,
            hqNext_mid, hqNext_v, hqNext_swap, hqNext_not_common,
            hqNext_first⟩
        have hbx : b ≠ x := by
          intro hbx_eq
          exact hb_not_right (by simpa [hbx_eq] using hx_right)
        have hb_not_swap :
            b ∉
              (((((pair.2 : G.Walk v t).takeUntil x hx_right).append
                ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath) :
                  G.Walk v s).support :=
          not_mem_cross_swap_left_of_left_prefix_not_right
            (G := G) (left := (pair.1 : G.Walk v s))
            (right := (pair.2 : G.Walk v t)) pair.1.property
            hx_left hx_right hb_left hb_prefix_x hb_not_right hbx
        have hqNext_ne_b : qNext ≠ b := by
          intro hqb
          exact hb_not_swap (by simpa [hqb] using hqNext_swap)
        have hqNext_tail_b :
            qNext ∈ (rs.dropUntil b hb_rs).support :=
          Walk.support_takeUntil_subset
            (rs.dropUntil b hb_rs) hz_tail_b hqNext_mid
        have hqNext_rs : qNext ∈ rs.support :=
          Walk.support_dropUntil_subset rs hb_rs hqNext_tail_b
        have hqNext_side :=
          bridge_guard_counterexample_side
            (G := G) (v := v) (s := s) (t := t)
            (x := x) (q := qNext) (pair := pair)
            hx_left hx_right hqNext_swap hqNext_not_common
        rcases hqNext_side with hqNext_right_prefix | hqNext_left_suffix
        · exact
            ⟨hright, b, hb_rs, hz_tail_b, qNext, hqNext_mid,
              hbv, hb_left, hb_not_right, hb_prefix_x, hqNext_v,
              hqNext_ne_b, hqNext_rs, hqNext_swap, hqNext_not_common,
              hqNext_right_prefix⟩
        · have hnot_segment_right_guard :
              ¬ ∀ r : α, r ≠ v →
                r ∈ (pair.2 : G.Walk v t).support →
                r ∈ ((rs.dropUntil b hb_rs).takeUntil qNext
                  hqNext_tail_b).support →
                r ∈ (pair.1 : G.Walk v s).support := by
            intro hguard
            rcases terminal_set_fan_bridge_left_suffix_stage_commonCard_lt
                (G := G) (v := v) (s := s) (t := t)
                (x := x) (y := b) (a := qNext)
                (pair := pair) (rs := rs)
                hx_left hx_right hxv hx_rs hb_left hb_rs
                hqNext_left_suffix.1 hqNext_rs hqNext_tail_b
                hb_prefix_x hqNext_left_suffix.2.2 hbx hguard with
              ⟨pair', hpair'_lt⟩
            exact hno_lower pair' hpair'_lt
          rcases exists_first_segment_right_only_of_not_segment_right_guard
              (G := G) (v := v) (s := s) (t := t)
              (a := b) (z := qNext) (pair := pair) (rs := rs)
              (ha_rs := hb_rs) (hz_tail := hqNext_tail_b)
              hnot_segment_right_guard with
            ⟨r2, hr2_mid, hr2v, hr2_right, hr2_not_left, _hr2_first⟩
          have hr2_pos :=
            mem_takeUntil_or_mem_dropUntil_of_mem_support
              (G := G) (p := (pair.2 : G.Walk v t))
              hx_right hr2_right
          rcases hr2_pos with hr2_prefix_x | hr2_suffix_x
          · rcases terminal_set_fan_left_suffix_stage_right_prefix_witness_commonCard_lt
                (G := G) (v := v) (s := s) (t := t)
                (x := x) (y := b) (a := qNext) (z := z)
                (r := r2) (pair := pair) (rs := rs)
                hx_left hx_right hxv hb_rs hqNext_tail_b
                hz_tail_b hqNext_mid hqNext_left_suffix.2.1
                hr2_mid hr2v hr2_right hr2_not_left hr2_prefix_x
                hqNext_first with
              ⟨pair', hpair'_lt⟩
            exact False.elim (hno_lower pair' hpair'_lt)
          · rcases terminal_set_fan_left_suffix_stage_right_suffix_witness_commonCard_lt
                (G := G) (v := v) (s := s) (t := t)
                (x := x) (y := b) (a := qNext) (z := z)
                (r := r2) (pair := pair) (rs := rs)
                hx_left hx_right hxv hx_rs hb_left hb_rs hb_prefix_x
                hqNext_tail_b hz_tail_b hqNext_mid
                hqNext_left_suffix.2.1 hr2_mid hr2v hr2_right
                hr2_not_left hr2_suffix_x hqNext_first with
              ⟨pair', hpair'_lt⟩
            exact False.elim (hno_lower pair' hpair'_lt)
      have hfront_extremal_false : False := by
        rcases hqBridge_front_next_right_prefix_package with
          ⟨hqBridge_right_prefix, _b0, _hb0_rs, _hz_tail_b0, _qNext0,
            _hqNext0_mid, _hb0v, _hb0_left, _hb0_not_right,
            _hb0_prefix_x, _hqNext0v, _hqNext0_ne_b, _hqNext0_rs,
            _hqNext0_swap, _hqNext0_not_common, _hqNext0_right,
            _hqNext0_not_left, _hqNext0_prefix_x⟩
        let swapLeft : G.Path v s :=
          (((pair.2 : G.Walk v t).takeUntil x hx_right).append
            ((pair.1 : G.Walk v s).dropUntil x hx_left)).toPath
        let S : Finset α :=
          Finset.univ.filter fun q =>
            q ≠ v ∧
            q ∈ (swapLeft : G.Walk v s).support ∧
            ¬ (q ∈ (pair.1 : G.Walk v s).support ∧
              q ∈ (pair.2 : G.Walk v t).support) ∧
            q ∈ ((pair.2 : G.Walk v t).takeUntil x hx_right).support ∧
            q ∈ (rs.takeUntil z hzrs).support
        have hright_prefix_front_successor :
            ∀ q : α, ∀ hq_rs : q ∈ rs.support, q ∈ S →
              ∃ qNext : α,
                qNext ∈ S ∧
                qNext ∈ (rs.dropUntil q hq_rs).support ∧
                qNext ≠ q := by
          intro q hq_rs hqS
          have hqS_data := (Finset.mem_filter.mp hqS).2
          rcases hqS_data with
            ⟨hqv, hq_swap, hq_not_common, hq_prefix_x, hq_prefix_z⟩
          have hq_right : q ∈ (pair.2 : G.Walk v t).support :=
            Walk.support_takeUntil_subset (pair.2 : G.Walk v t) hx_right
              hq_prefix_x
          have hq_not_left : q ∉ (pair.1 : G.Walk v s).support := by
            intro hq_left
            exact hq_not_common ⟨hq_left, hq_right⟩
          have hq_ne_z : q ≠ z := by
            intro hqz
            exact hz_not_swap (by simpa [swapLeft, hqz] using hq_swap)
          have hz_tail_q : z ∈ (rs.dropUntil q hq_rs).support :=
            mem_dropUntil_of_mem_takeUntil_ne
              (G := G) rs hq_rs hzrs hq_prefix_z hq_ne_z
          have hnot_segment_left_guard :
              ¬ ∀ y0 : α, y0 ≠ v →
                y0 ∈ (pair.1 : G.Walk v s).support →
                y0 ∈ ((rs.dropUntil q hq_rs).takeUntil z
                  hz_tail_q).support →
                y0 ∈ (pair.2 : G.Walk v t).support := by
            intro hguard
            rcases terminal_set_fan_bridge_right_prefix_stage_commonCard_lt
                (G := G) (v := v) (s := s) (t := t)
                (x := x) (a := q) (z := z)
                (pair := pair) (rs := rs)
                hx_left hx_right hxv hx_rs hq_right hq_rs hz_right hzrs
                hq_prefix_x hz_suffix_right hq_prefix_z hq_ne_z hzx hguard with
              ⟨pair', hpair'_lt⟩
            exact hno_lower pair' hpair'_lt
          rcases exists_first_segment_left_only_of_not_segment_left_guard
              (G := G) (v := v) (s := s) (t := t)
              (a := q) (z := z) (pair := pair) (rs := rs)
              (ha_rs := hq_rs) (hz_tail := hz_tail_q)
              hnot_segment_left_guard with
            ⟨b, hb_mid, hbv, hb_left, hb_not_right, hb_first⟩
          have hb_tail_q : b ∈ (rs.dropUntil q hq_rs).support :=
            Walk.support_takeUntil_subset (rs.dropUntil q hq_rs)
              hz_tail_q hb_mid
          have hb_rs : b ∈ rs.support :=
            Walk.support_dropUntil_subset rs hq_rs hb_tail_q
          have hb_ne_q : b ≠ q := by
            intro hbq
            exact hq_not_left (by simpa [hbq] using hb_left)
          have hq_prefix_b : q ∈ (rs.takeUntil b hb_rs).support :=
            mem_takeUntil_of_mem_dropUntil_ne_on_isPath
              (G := G) (p := rs) hrsPath hq_rs hb_rs hb_tail_q
              hb_ne_q.symm
          have hq_not_tail_b : q ∉ (rs.dropUntil b hb_rs).support :=
            not_mem_dropUntil_of_mem_takeUntil_ne_on_isPath
              (G := G) (p := rs) hrsPath hb_rs hq_rs hq_prefix_b
              hb_ne_q.symm
          have hb_ne_z : b ≠ z := by
            intro hbz
            exact hb_not_right (by simpa [hbz] using hz_right)
          have hb_prefix_z : b ∈ (rs.takeUntil z hzrs).support :=
            mem_takeUntil_of_mem_dropUntil_takeUntil_ne_on_isPath
              (G := G) (p := rs) hrsPath hq_rs hzrs hz_tail_q
              hb_mid hb_ne_z
          have hz_tail_b : z ∈ (rs.dropUntil b hb_rs).support :=
            mem_dropUntil_of_mem_takeUntil_ne
              (G := G) rs hb_rs hzrs hb_prefix_z hb_ne_z
          have hbx : b ≠ x := by
            intro hbx_eq
            exact hb_not_right (by simpa [hbx_eq] using hx_right)
          have hb_pos :=
            mem_takeUntil_or_mem_dropUntil_of_mem_support
              (G := G) (p := (pair.1 : G.Walk v s)) hx_left hb_left
          have hb_prefix_x :
              b ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support := by
            rcases hb_pos with hb_prefix_x | hb_suffix_x
            · exact hb_prefix_x
            · rcases terminal_set_fan_right_prefix_stage_left_suffix_witness_commonCard_lt
                (G := G) (v := v) (s := s) (t := t)
                (x := x) (a := q) (z := z) (b := b)
                (pair := pair) (rs := rs)
                hx_left hx_right hxv hx_rs hq_right hq_not_left
                hq_rs hq_prefix_x hz_right hz_tail_q hz_suffix_right
                hb_mid hbv hb_left hb_not_right hb_first hb_suffix_x with
              ⟨pair', hpair'_lt⟩
              exact False.elim (hno_lower pair' hpair'_lt)
          have hb_alt :
              b ∈
                (((((pair.1 : G.Walk v s).takeUntil x hx_left).append
                  ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath) :
                    G.Walk v t).support := by
            by_contra hb_not_alt
            rcases terminal_set_cross_swap_commonCard_lt_of_left_prefix_absent_altRight
                (G := G) (v := v) (s := s) (t := t)
                (x := x) (y := b) (pair := pair)
                hx_left hx_right hxv hb_prefix_x hb_not_alt with
              ⟨pair', hpair'_lt⟩
            exact hno_lower pair' hpair'_lt
          have hnot_bridge_guard_bz :
              ¬ ∀ q0 : α, q0 ≠ v →
                q0 ∈ (swapLeft : G.Walk v s).support →
                q0 ∈ ((rs.dropUntil b hb_rs).takeUntil z
                  hz_tail_b).support →
                q0 ∈ (pair.1 : G.Walk v s).support ∧
                  q0 ∈ (pair.2 : G.Walk v t).support := by
            intro hguard
            rcases terminal_set_fan_two_sided_bridge_commonCard_lt_of_middle_guard
                (G := G) (v := v) (s := s) (t := t)
                (x := x) (y := b) (z := z)
                (pair := pair) (rs := rs)
                hx_left hx_right hxv hx_rs hb_left hb_rs hz_tail_b
                hz_right hb_prefix_x hz_suffix_right hbx hzx
                (by simpa [swapLeft] using hguard) with
              ⟨pair', hpair'_lt⟩
            exact hno_lower pair' hpair'_lt
          rcases exists_first_bridge_guard_counterexample
              (G := G) (v := v) (s := s) (t := t)
              (x := x) (y := b) (z := z)
              (pair := pair) (rs := rs)
              hx_left hx_right hb_rs hz_tail_b
              (by simpa [swapLeft] using hnot_bridge_guard_bz) with
            ⟨qNext, hqNext_mid, hqNext_v, hqNext_swap,
              hqNext_not_common, hqNext_first⟩
          have hqNext_tail_b :
              qNext ∈ (rs.dropUntil b hb_rs).support :=
            Walk.support_takeUntil_subset (rs.dropUntil b hb_rs)
              hz_tail_b hqNext_mid
          have hqNext_rs : qNext ∈ rs.support :=
            Walk.support_dropUntil_subset rs hb_rs hqNext_tail_b
          have hqNext_ne_b : qNext ≠ b := by
            have hb_not_swap :
                b ∉ (swapLeft : G.Walk v s).support := by
              simpa [swapLeft] using
                (not_mem_cross_swap_left_of_left_prefix_not_right
                  (G := G) (left := (pair.1 : G.Walk v s))
                  (right := (pair.2 : G.Walk v t)) pair.1.property
                  hx_left hx_right hb_left hb_prefix_x hb_not_right hbx)
            intro hqb
            exact hb_not_swap (by simpa [hqb] using hqNext_swap)
          have hqNext_ne_q : qNext ≠ q := by
            intro hqq
            exact hq_not_tail_b (by simpa [hqq] using hqNext_tail_b)
          have hqNext_tail_q :
              qNext ∈ (rs.dropUntil q hq_rs).support :=
            mem_dropUntil_of_mem_dropUntil_of_mem_dropUntil
              (G := G) (p := rs) hrsPath hq_rs hb_rs hb_tail_q
              hqNext_tail_b
          have hqNext_ne_z : qNext ≠ z := by
            intro hqz
            exact hz_not_swap (by simpa [swapLeft, hqz] using hqNext_swap)
          have hqNext_prefix_z :
              qNext ∈ (rs.takeUntil z hzrs).support :=
            mem_takeUntil_of_mem_dropUntil_takeUntil_ne_on_isPath
              (G := G) (p := rs) hrsPath hb_rs hzrs hz_tail_b
              hqNext_mid hqNext_ne_z
          have hqNext_side :=
            bridge_guard_counterexample_side
              (G := G) (v := v) (s := s) (t := t)
              (x := x) (q := qNext) (pair := pair)
              hx_left hx_right (by simpa [swapLeft] using hqNext_swap)
              hqNext_not_common
          have hqNext_right_prefix :
              qNext ∈ (pair.2 : G.Walk v t).support ∧
                qNext ∉ (pair.1 : G.Walk v s).support ∧
                qNext ∈
                  ((pair.2 : G.Walk v t).takeUntil x hx_right).support := by
            rcases hqNext_side with hright | hleft
            · exact hright
            · have hnot_segment_right_guard :
                  ¬ ∀ r : α, r ≠ v →
                    r ∈ (pair.2 : G.Walk v t).support →
                    r ∈ ((rs.dropUntil b hb_rs).takeUntil qNext
                      hqNext_tail_b).support →
                    r ∈ (pair.1 : G.Walk v s).support := by
                intro hguard
                rcases terminal_set_fan_bridge_left_suffix_stage_commonCard_lt
                    (G := G) (v := v) (s := s) (t := t)
                    (x := x) (y := b) (a := qNext)
                    (pair := pair) (rs := rs)
                    hx_left hx_right hxv hx_rs hb_left hb_rs
                    hleft.1 hqNext_rs hqNext_tail_b
                    hb_prefix_x hleft.2.2 hbx hguard with
                  ⟨pair', hpair'_lt⟩
                exact hno_lower pair' hpair'_lt
              rcases exists_first_segment_right_only_of_not_segment_right_guard
                  (G := G) (v := v) (s := s) (t := t)
                  (a := b) (z := qNext) (pair := pair) (rs := rs)
                  (ha_rs := hb_rs) (hz_tail := hqNext_tail_b)
                  hnot_segment_right_guard with
                ⟨r2, hr2_mid, hr2v, hr2_right, hr2_not_left, _hr2_first⟩
              have hr2_pos :=
                mem_takeUntil_or_mem_dropUntil_of_mem_support
                  (G := G) (p := (pair.2 : G.Walk v t))
                  hx_right hr2_right
              rcases hr2_pos with hr2_prefix_x | hr2_suffix_x
              · rcases terminal_set_fan_left_suffix_stage_right_prefix_witness_commonCard_lt
                    (G := G) (v := v) (s := s) (t := t)
                    (x := x) (y := b) (a := qNext) (z := z)
                    (r := r2) (pair := pair) (rs := rs)
                    hx_left hx_right hxv hb_rs hqNext_tail_b
                    hz_tail_b hqNext_mid hleft.2.1
                    hr2_mid hr2v hr2_right hr2_not_left hr2_prefix_x
                    hqNext_first with
                  ⟨pair', hpair'_lt⟩
                exact False.elim (hno_lower pair' hpair'_lt)
              · rcases terminal_set_fan_left_suffix_stage_right_suffix_witness_commonCard_lt
                    (G := G) (v := v) (s := s) (t := t)
                    (x := x) (y := b) (a := qNext) (z := z)
                    (r := r2) (pair := pair) (rs := rs)
                    hx_left hx_right hxv hx_rs hb_left hb_rs hb_prefix_x
                    hqNext_tail_b hz_tail_b hqNext_mid
                    hleft.2.1 hr2_mid hr2v hr2_right
                    hr2_not_left hr2_suffix_x hqNext_first with
                  ⟨pair', hpair'_lt⟩
                exact False.elim (hno_lower pair' hpair'_lt)
          have hqNextS : qNext ∈ S := by
            change qNext ∈ Finset.univ.filter (fun q =>
              q ≠ v ∧
              q ∈ (swapLeft : G.Walk v s).support ∧
              ¬ (q ∈ (pair.1 : G.Walk v s).support ∧
                q ∈ (pair.2 : G.Walk v t).support) ∧
              q ∈ ((pair.2 : G.Walk v t).takeUntil x hx_right).support ∧
              q ∈ (rs.takeUntil z hzrs).support)
            rw [Finset.mem_filter]
            exact
              ⟨by simp, hqNext_v, by simpa [swapLeft] using hqNext_swap,
                hqNext_not_common, hqNext_right_prefix.2.2,
                hqNext_prefix_z⟩
          exact ⟨qNext, hqNextS, hqNext_tail_q, hqNext_ne_q⟩
        have hqBridgeS : qBridge ∈ S := by
          change qBridge ∈ Finset.univ.filter (fun q =>
            q ≠ v ∧
            q ∈ (swapLeft : G.Walk v s).support ∧
            ¬ (q ∈ (pair.1 : G.Walk v s).support ∧
              q ∈ (pair.2 : G.Walk v t).support) ∧
            q ∈ ((pair.2 : G.Walk v t).takeUntil x hx_right).support ∧
            q ∈ (rs.takeUntil z hzrs).support)
          rw [Finset.mem_filter]
          exact
            ⟨by simp, hqBridge_v, by simpa [swapLeft] using hqBridge_swap,
              hqBridge_not_common, hqBridge_right_prefix.2.2,
              hqBridge_prefix_z⟩
        have hnonempty : {q ∈ S | q ∈ rs.support}.Nonempty := by
          refine ⟨qBridge, ?_⟩
          rw [Finset.mem_filter]
          exact ⟨hqBridgeS, hqBridge_rs⟩
        rcases exists_last_mem_support_forall_mem_dropUntil_imp_eq
            (G := G) rs hrsPath S hnonempty with
          ⟨qMax, hqMaxS, hqMax_rs, hlastS⟩
        rcases hright_prefix_front_successor qMax hqMax_rs hqMaxS with
          ⟨qNext, hqNextS, hqNext_tail_qMax, hqNext_ne_qMax⟩
        exact hqNext_ne_qMax (hlastS qNext hqNextS hqNext_tail_qMax)
      exact False.elim hfront_extremal_false
  · have hzFirst_right : zFirst ∈ (pair.2 : G.Walk v t).support := by
      rcases hzFirst_old_union with hzFirst_left' | hzFirst_right
      · exact False.elim (hzFirst_left hzFirst_left')
      · exact hzFirst_right
    have hzFirst_suffix_right :
        zFirst ∈ ((pair.2 : G.Walk v t).dropUntil x hx_right).support := by
      rw [Walk.mem_support_append_iff] at hzFirst_alt_raw
      rcases hzFirst_alt_raw with hzFirst_prefix | hzFirst_suffix
      · exact False.elim
          (hzFirst_left
            (Walk.support_takeUntil_subset (pair.1 : G.Walk v s)
              hx_left hzFirst_prefix))
      · exact hzFirst_suffix
    exact terminal_set_fan_first_bad_right_only_splice_commonCard_lt
      (G := G) (v := v) (s := s) (t := t)
      (x := x) (z := zFirst) (pair := pair) (rs := rs)
      hpair_measure_min hrsPath hx_left hx_right hxv hx_rs
      hzFirst_rs hzFirst_right hzFirst_left hzFirst_suffix_right hfirst_bad

lemma terminal_set_fan_left_suffix_retention_extremal_bad_pivot_descent
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x w : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hpair_measure_min : ∀ pair' : G.Path v s × G.Path v t,
      terminalPathPairWeightedMeasure pair ≤ terminalPathPairWeightedMeasure pair')
    (hrsPath : rs.IsPath)
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rs : x ∉ rs.support)
    (hw_rs : w ∈ rs.support)
    (hw_right : w ∈ (pair.2 : G.Walk v t).support)
    (hw_not_left : w ∉ (pair.1 : G.Walk v s).support)
    (hwv : w ≠ v)
    (hfirst : ∀ y, y ∈ rs.support → y ≠ v →
      y ∈ (pair.1 : G.Walk v s).support ∨
      y ∈ (pair.2 : G.Walk v t).support →
      y = w ∨ y ∉ (rs.takeUntil w hw_rs).support)
    (hdirect : ¬ terminalPathPairCommonCard
      ((⟨rs, hrsPath⟩ : G.Path v s), pair.2) <
      terminalPathPairCommonCard pair)
    (hret : x ∈ ((pair.2 : G.Walk v t).dropUntil w hw_right).support)
    (hbad_exists :
      let altRight : G.Path v t :=
        (((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
      ∃ z : α, z ∈ rs.support ∧ z ≠ v ∧
        z ∈ (altRight : G.Walk v t).support ∧
        ¬ (z ∈ (pair.1 : G.Walk v s).support ∧
           z ∈ (pair.2 : G.Walk v t).support ∧ z ≠ x)) :
    ∃ pair' : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  classical
  dsimp at hbad_exists
  rcases exists_first_bad_pivot_on_rs
      (G := G) (v := v) (s := s) (t := t)
      (x := x) (pair := pair) (rs := rs)
      hx_left hx_right hbad_exists with
    ⟨z0, hz0rs, hz0v, hz0_alt, hz0_bad, hfirst_bad⟩
  have hz0_old_union :
      z0 ∈ (pair.1 : G.Walk v s).support ∨
        z0 ∈ (pair.2 : G.Walk v t).support := by
    simpa using
      (mem_support_toPath_append_takeUntil_dropUntil_subset
        (G := G) (p := (pair.1 : G.Walk v s))
        (q := (pair.2 : G.Walk v t)) (y := x) (z := z0)
        hx_left hx_right hz0_alt)
  have hz0_alt_raw :
      z0 ∈ (((pair.1 : G.Walk v s).takeUntil x hx_left).append
        ((pair.2 : G.Walk v t).dropUntil x hx_right)).support := by
    exact Walk.support_toPath_subset _ hz0_alt
  by_cases hz0_left : z0 ∈ (pair.1 : G.Walk v s).support
  · exact terminal_set_fan_left_suffix_retention_bad_pivot_descent
      (G := G) (v := v) (s := s) (t := t)
      (x := x) (w := w) (z := z0) (pair := pair) (rs := rs)
      hpair_measure_min hrsPath hx_left hx_right hxv hx_rs
      hw_rs hw_right hw_not_left hwv hfirst hdirect hret
      hz0rs hz0v hz0_alt hz0_bad
  · have hz0_right : z0 ∈ (pair.2 : G.Walk v t).support := by
      rcases hz0_old_union with hz0_left' | hz0_right
      · exact False.elim (hz0_left hz0_left')
      · exact hz0_right
    have hz0_suffix_right :
        z0 ∈ ((pair.2 : G.Walk v t).dropUntil x hx_right).support := by
      rw [Walk.mem_support_append_iff] at hz0_alt_raw
      rcases hz0_alt_raw with hz0_prefix | hz0_suffix
      · exact False.elim
          (hz0_left
            (Walk.support_takeUntil_subset (pair.1 : G.Walk v s)
              hx_left hz0_prefix))
      · exact hz0_suffix
    exact terminal_set_fan_first_bad_right_only_splice_commonCard_lt
      (G := G) (v := v) (s := s) (t := t)
      (x := x) (z := z0) (pair := pair) (rs := rs)
      hpair_measure_min hrsPath hx_left hx_right hxv hx_rs
      hz0rs hz0_right hz0_left hz0_suffix_right hfirst_bad

lemma terminal_set_fan_left_suffix_retention_alt_intersections_control
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x w : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hpair_measure_min : ∀ pair' : G.Path v s × G.Path v t,
      terminalPathPairWeightedMeasure pair ≤ terminalPathPairWeightedMeasure pair')
    (hrsPath : rs.IsPath)
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rs : x ∉ rs.support)
    (hw_rs : w ∈ rs.support)
    (hw_right : w ∈ (pair.2 : G.Walk v t).support)
    (hw_not_left : w ∉ (pair.1 : G.Walk v s).support)
    (hwv : w ≠ v)
    (hfirst : ∀ z, z ∈ rs.support → z ≠ v →
      z ∈ (pair.1 : G.Walk v s).support ∨
      z ∈ (pair.2 : G.Walk v t).support →
      z = w ∨ z ∉ (rs.takeUntil w hw_rs).support)
    (hdirect : ¬ terminalPathPairCommonCard
      ((⟨rs, hrsPath⟩ : G.Path v s), pair.2) <
      terminalPathPairCommonCard pair)
    (hret : x ∈ ((pair.2 : G.Walk v t).dropUntil w hw_right).support) :
    let altRight : G.Path v t :=
      (((pair.1 : G.Walk v s).takeUntil x hx_left).append
        ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
    ∀ z, z ∈ rs.support → z ≠ v →
      z ∈ (altRight : G.Walk v t).support →
      z ∈ (pair.1 : G.Walk v s).support ∧
      z ∈ (pair.2 : G.Walk v t).support ∧ z ≠ x := by
  classical
  dsimp
  intro z hzrs hzv hz_alt
  have hz_old_union :
      z ∈ (pair.1 : G.Walk v s).support ∨
        z ∈ (pair.2 : G.Walk v t).support := by
    simpa using
      (mem_support_toPath_append_takeUntil_dropUntil_subset
        (G := G) (p := (pair.1 : G.Walk v s))
        (q := (pair.2 : G.Walk v t)) (y := x) (z := z)
        hx_left hx_right hz_alt)
  have hzx : z ≠ x := by
    intro hzx_eq
    exact hx_rs (by simpa [hzx_eq] using hzrs)
  have hz_alt_raw :
      z ∈ (((pair.1 : G.Walk v s).takeUntil x hx_left).append
        ((pair.2 : G.Walk v t).dropUntil x hx_right)).support := by
    exact Walk.support_toPath_subset _ hz_alt
  by_cases hz_left : z ∈ (pair.1 : G.Walk v s).support
  · by_cases hz_right : z ∈ (pair.2 : G.Walk v t).support
    · exact ⟨hz_left, hz_right, hzx⟩
    · have hfirst_z :=
        hfirst z hzrs hzv (Or.inl hz_left)
      have hz_prefix_left :
          z ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support := by
        rw [Walk.mem_support_append_iff] at hz_alt_raw
        rcases hz_alt_raw with hz_prefix | hz_suffix
        · exact hz_prefix
        · exact False.elim
            (hz_right
              (Walk.support_dropUntil_subset (pair.2 : G.Walk v t)
                hx_right hz_suffix))
      have hz_not_rs_prefix :
          z ∉ (rs.takeUntil w hw_rs).support := by
        rcases hfirst_z with hzw | hz_not_prefix
        · exact False.elim (hw_not_left (by simpa [hzw] using hz_left))
        · exact hz_not_prefix
      by_contra hbad
      rcases terminal_set_fan_left_suffix_retention_extremal_bad_pivot_descent
          (G := G) (v := v) (s := s) (t := t)
          (x := x) (w := w) (pair := pair) (rs := rs)
          hpair_measure_min hrsPath hx_left hx_right hxv hx_rs
          hw_rs hw_right hw_not_left hwv hfirst hdirect hret
          (by
            dsimp
            exact ⟨z, hzrs, hzv, hz_alt, hbad⟩) with
        ⟨pair', hpair'_lt⟩
      exact not_terminalPathPairCommonCard_lt_of_weighted_min
        hpair_measure_min pair' hpair'_lt
  · have hz_right : z ∈ (pair.2 : G.Walk v t).support := by
      rcases hz_old_union with hz_left' | hz_right
      · exact False.elim (hz_left hz_left')
      · exact hz_right
    have hfirst_z :=
      hfirst z hzrs hzv (Or.inr hz_right)
    have hz_suffix_right :
        z ∈ ((pair.2 : G.Walk v t).dropUntil x hx_right).support := by
      rw [Walk.mem_support_append_iff] at hz_alt_raw
      rcases hz_alt_raw with hz_prefix | hz_suffix
      · exact False.elim
          (hz_left
            (Walk.support_takeUntil_subset (pair.1 : G.Walk v s)
              hx_left hz_prefix))
      · exact hz_suffix
    have hfirst_suffix_branch :
        z = w ∨ z ∉ (rs.takeUntil w hw_rs).support := hfirst_z
    by_contra hbad
    rcases terminal_set_fan_left_suffix_retention_extremal_bad_pivot_descent
        (G := G) (v := v) (s := s) (t := t)
        (x := x) (w := w) (pair := pair) (rs := rs)
        hpair_measure_min hrsPath hx_left hx_right hxv hx_rs
        hw_rs hw_right hw_not_left hwv hfirst hdirect hret
        (by
          dsimp
          exact ⟨z, hzrs, hzv, hz_alt, hbad⟩) with
      ⟨pair', hpair'_lt⟩
    exact not_terminalPathPairCommonCard_lt_of_weighted_min
      hpair_measure_min pair' hpair'_lt

lemma terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x w : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hpair_measure_min : ∀ pair' : G.Path v s × G.Path v t,
      terminalPathPairWeightedMeasure pair ≤ terminalPathPairWeightedMeasure pair')
    (hrsPath : rs.IsPath)
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rs : x ∉ rs.support)
    (hw_rs : w ∈ rs.support)
    (hw_right : w ∈ (pair.2 : G.Walk v t).support)
    (hw_not_left : w ∉ (pair.1 : G.Walk v s).support)
    (hwv : w ≠ v)
    (hfirst :
      ∀ z, z ∈ rs.support → z ≠ v →
        z ∈ (pair.1 : G.Walk v s).support ∨
        z ∈ (pair.2 : G.Walk v t).support →
        z = w ∨ z ∉ (rs.takeUntil w hw_rs).support) :
    ∃ pair' : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  classical
  let direct : G.Path v s × G.Path v t := (⟨rs, hrsPath⟩, pair.2)
  by_cases hdirect :
      terminalPathPairCommonCard direct < terminalPathPairCommonCard pair
  · exact ⟨direct, hdirect⟩
  · let spliceRight : G.Path v t :=
      (((rs.takeUntil w hw_rs).append
        ((pair.2 : G.Walk v t).dropUntil w hw_right)).toPath)
    let spliced : G.Path v s × G.Path v t := (pair.1, spliceRight)
    have hspliceRight_support :
        ∀ z : α, z ∈ (spliceRight : G.Walk v t).support →
          z ∈ rs.support ∨ z ∈ (pair.2 : G.Walk v t).support := by
      intro z hz
      simpa [spliceRight] using
        (mem_support_toPath_append_takeUntil_dropUntil_subset
          (G := G) (p := rs) (q := (pair.2 : G.Walk v t))
          (y := w) (z := z) hw_rs hw_right hz)
    have hx_not_prefix : x ∉ (rs.takeUntil w hw_rs).support := by
      intro hxprefix
      have hxrs_prefix : x ∈ rs.support :=
        Walk.support_takeUntil_subset rs hw_rs hxprefix
      exact hx_rs hxrs_prefix
    have hcommon_subset_old :
        ((pair.1 : G.Walk v s).support.toFinset ∩
            (spliceRight : G.Walk v t).support.toFinset).erase v ⊆
          ((pair.1 : G.Walk v s).support.toFinset ∩
            (pair.2 : G.Walk v t).support.toFinset).erase v := by
      intro z hz
      rw [Finset.mem_erase, Finset.mem_inter] at hz
      rw [Finset.mem_erase, Finset.mem_inter]
      rcases hz with ⟨hzv, hz_left, hz_splice⟩
      have hz_splice' : z ∈ (spliceRight : G.Walk v t).support := by
        simpa using hz_splice
      rcases hspliceRight_support z hz_splice' with hzrs | hzright
      · have hfirst_z :=
          hfirst z hzrs hzv (Or.inl (by simpa using hz_left))
        rcases hfirst_z with rfl | hz_not_prefix
        · exact False.elim (hw_not_left (by simpa using hz_left))
        · have hz_append :
              z ∈ ((rs.takeUntil w hw_rs).append
                ((pair.2 : G.Walk v t).dropUntil w hw_right)).support := by
            exact Walk.support_toPath_subset _ hz_splice'
          rw [Walk.mem_support_append_iff] at hz_append
          rcases hz_append with hzprefix | hzdrop
          · exact False.elim (hz_not_prefix hzprefix)
          · exact ⟨hzv, by simpa using hz_left,
              by simpa using
                (Walk.support_dropUntil_subset (pair.2 : G.Walk v t)
                  hw_right hzdrop)⟩
      · exact ⟨hzv, by simpa using hz_left, by simpa using hzright⟩
    by_cases hret :
        x ∈ ((pair.2 : G.Walk v t).dropUntil w hw_right).support
    · let altRight : G.Path v t :=
        (((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
      let altPair : G.Path v s × G.Path v t := (⟨rs, hrsPath⟩, altRight)
      have halt_control :
          ∀ z, z ∈ rs.support → z ≠ v →
            z ∈ (altRight : G.Walk v t).support →
            z ∈ (pair.1 : G.Walk v s).support ∧
            z ∈ (pair.2 : G.Walk v t).support ∧ z ≠ x := by
        simpa [altRight] using
          (terminal_set_fan_left_suffix_retention_alt_intersections_control
            (G := G) (v := v) (s := s) (t := t)
            (x := x) (w := w) (pair := pair) (rs := rs)
            hpair_measure_min hrsPath hx_left hx_right hxv hx_rs
            hw_rs hw_right hw_not_left hwv hfirst hdirect hret)
      have hcommon_subset_old_without_x_alt :
          ((rs.support.toFinset ∩
              (altRight : G.Walk v t).support.toFinset).erase v) ⊆
            (((pair.1 : G.Walk v s).support.toFinset ∩
              (pair.2 : G.Walk v t).support.toFinset).erase v).erase x := by
        intro z hz
        rw [Finset.mem_erase, Finset.mem_inter] at hz
        rcases hz with ⟨hzv, hz_rs, hz_alt⟩
        rcases halt_control z (by simpa using hz_rs) hzv (by simpa using hz_alt) with
          ⟨hz_left, hz_right, hzx⟩
        rw [Finset.mem_erase, Finset.mem_erase, Finset.mem_inter]
        exact ⟨hzx, hzv, by simpa using hz_left, by simpa using hz_right⟩
      have halt_descent :
          terminalPathPairCommonCard altPair < terminalPathPairCommonCard pair := by
        simpa [terminalPathPairCommonCard, altPair] using
          (common_support_erase_card_lt_of_subset_erase_common
            (G := G) (v := v) (s := s) (t := t)
            (qs := (pair.1 : G.Walk v s))
            (qt := (pair.2 : G.Walk v t))
            (qs' := rs)
            (qt' := (altRight : G.Walk v t))
            (x := x) hcommon_subset_old_without_x_alt hx_left hx_right hxv)
      exact ⟨altPair, halt_descent⟩
    · exact terminal_set_fan_left_first_crossing_splice_commonCard_lt_of_not_retained
        (G := G) (v := v) (s := s) (t := t) (x := x) (w := w)
        (pair := pair) (rs := rs) hrsPath hx_left hx_right hxv hx_rs
        hw_rs hw_right hw_not_left hfirst hret

lemma terminal_set_fan_left_suffix_retention_right_prefix_wide_residual_descent
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x w : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hpair_measure_min : ∀ pair' : G.Path v s × G.Path v t,
      terminalPathPairWeightedMeasure pair ≤ terminalPathPairWeightedMeasure pair')
    (hrsPath : rs.IsPath)
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rs : x ∉ rs.support)
    (hw_rs : w ∈ rs.support)
    (hw_right : w ∈ (pair.2 : G.Walk v t).support)
    (hw_not_left : w ∉ (pair.1 : G.Walk v s).support)
    (hwv : w ≠ v)
    (hfirst : ∀ y, y ∈ rs.support → y ≠ v →
      y ∈ (pair.1 : G.Walk v s).support ∨
      y ∈ (pair.2 : G.Walk v t).support →
      y = w ∨ y ∉ (rs.takeUntil w hw_rs).support)
    (_hdirect : ¬ terminalPathPairCommonCard
      ((⟨rs, hrsPath⟩ : G.Path v s), pair.2) <
      terminalPathPairCommonCard pair)
    (_hret : x ∈ ((pair.2 : G.Walk v t).dropUntil w hw_right).support)
    (hres_exists :
      ∃ z : α, z ∈ rs.support ∧ z ≠ v ∧ z ≠ w ∧
        (z ∈ (pair.1 : G.Walk v s).support ∨
          z ∈ (pair.2 : G.Walk v t).support) ∧
        ¬ (z ∈ (pair.1 : G.Walk v s).support ∧
           z ∈ (pair.2 : G.Walk v t).support ∧ z ≠ x)) :
    ∃ pair' : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  rcases exists_first_noncommon_old_residual_on_rs
      (G := G) (v := v) (s := s) (t := t)
      (x := x) (w := w) (pair := pair) (rs := rs)
      hres_exists with
    ⟨z, hzrs, _hzv, _hzw, hz_old, hz_bad, _hfirst_residual⟩
  have _hz_side :
      (z ∈ (pair.1 : G.Walk v s).support ∧
        z ∉ (pair.2 : G.Walk v t).support) ∨
      (z ∈ (pair.2 : G.Walk v t).support ∧
        z ∉ (pair.1 : G.Walk v s).support) :=
    noncommon_old_residual_exclusive_side
      (G := G) (v := v) (s := s) (t := t)
      (x := x) (z := z) (pair := pair) (rs := rs)
      hx_rs hzrs hz_old hz_bad
  exact terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt
    (G := G) (v := v) (s := s) (t := t)
    (x := x) (w := w) (pair := pair) (rs := rs)
    hpair_measure_min hrsPath hx_left hx_right hxv hx_rs
    hw_rs hw_right hw_not_left hwv hfirst

/-
The singleton replacement route below is frozen: a path avoiding the old
common vertex can introduce a new non-apex intersection.  The active target is
the theorem-level finite fan/min-cut reduction in
`finite_two_fan_to_pair_of_terminal_set_no_small_endpoint_separator`.

private lemma terminal_set_fan_intersection_reduction_from_singleton_path
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x u : α}
    {qs : G.Walk v s} {qt : G.Walk v t}
    (hqsPath : qs.IsPath) (hqtPath : qt.IsPath)
    (ht_qs : t ∉ qs.support) (hs_qt : s ∉ qt.support)
    (hxqs : x ∈ qs.support) (hxqt : x ∈ qt.support)
    (hxv : x ≠ v) (hxs : x ≠ s) (hxt : x ≠ t)
    (hu : u = s ∨ u = t) (hux : u ≠ x)
    (r : G.Walk v u) (hrPath : r.IsPath) (hx_r : x ∉ r.support) :
    ∃ qs' : G.Walk v s, ∃ qt' : G.Walk v t,
      qs'.IsPath ∧ qt'.IsPath ∧
      ∀ z : α, z ∈ qs'.support → z ∈ qt'.support → z = v := by
  classical
  rcases hu with hus | hut
  · let rs : G.Walk v s := r.copy rfl hus
    have hrsPath : rs.IsPath := by
      simpa [rs] using hrPath
    have hx_rs : x ∉ rs.support := by
      intro hxmem
      exact hx_r (by simpa [rs] using hxmem)
    by_cases hmeet :
        ∀ z : α, z ∈ rs.support → z ∈ qt.support → z = v
    · exact ⟨rs, qt, hrsPath, hqtPath, hmeet⟩
    · push_neg at hmeet
      rcases hmeet with ⟨y, hyrs, hyqt, hyv⟩
      have hyx : y ≠ x := by
        intro hyx_eq
        exact hx_rs (by simpa [hyx_eq] using hyrs)
      have hys : y ≠ s := by
        intro hys_eq
        exact hs_qt (by simpa [hys_eq] using hyqt)
      -- Remaining finite fan rerouting blocker: `r` avoids the original
      -- common vertex `x`, but it has a new non-apex intersection `y`
      -- with the opposite terminal path.
  · let rt : G.Walk v t := r.copy rfl hut
    have hrtPath : rt.IsPath := by
      simpa [rt] using hrPath
    have hx_rt : x ∉ rt.support := by
      intro hxmem
      exact hx_r (by simpa [rt] using hxmem)
    by_cases hmeet :
        ∀ z : α, z ∈ qs.support → z ∈ rt.support → z = v
    · exact ⟨qs, rt, hqsPath, hrtPath, hmeet⟩
    · push_neg at hmeet
      rcases hmeet with ⟨y, hyqs, hyrt, hyv⟩
      have hyx : y ≠ x := by
        intro hyx_eq
        exact hx_rt (by simpa [hyx_eq] using hyrt)
      have hyt : y ≠ t := by
        intro hyt_eq
        exact ht_qs (by simpa [hyt_eq] using hyqs)
      -- Remaining finite fan rerouting blocker: `r` avoids the original
      -- common vertex `x`, but it has a new non-apex intersection `y`
      -- with the opposite terminal path.

lemma terminal_set_fan_augmentation_from_endpoint_avoiding_pair
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t : α}
    (hvs : v ≠ s) (hvt : v ≠ t) (hst : s ≠ t)
    (hsep : ∀ C : Finset α, C.card < 2 → v ∉ C →
      ∃ u : α, (u = s ∨ u = t) ∧ u ∉ C ∧
        ∃ q : G.Walk v u, q.IsPath ∧ ∀ z, z ∈ q.support → z ∉ C) :
    ∃ qs : G.Walk v s, ∃ qt : G.Walk v t,
      qs.IsPath ∧ qt.IsPath ∧
      ∀ z : α, z ∈ qs.support → z ∈ qt.support → z = v := by
  classical
  have hendpoint :
      ∃ qs : G.Walk v s, ∃ qt : G.Walk v t,
        qs.IsPath ∧ qt.IsPath ∧ t ∉ qs.support ∧ s ∉ qt.support :=
    exists_terminal_set_endpoint_avoiding_pair
      (G := G) (v := v) (s := s) (t := t) hvs hvt hst hsep
  have hsingleton :
      ∀ x : α, x ≠ v →
        ∃ u : α, (u = s ∨ u = t) ∧ u ≠ x ∧
          ∃ q : G.Walk v u, q.IsPath ∧ x ∉ q.support := by
    intro x hxv
    exact exists_terminal_path_avoiding_singleton_of_terminal_set_separator
      (G := G) (v := v) (s := s) (t := t) (x := x) hxv hsep
  rcases hendpoint with ⟨qs, qt, hqsPath, hqtPath, ht_qs, hs_qt⟩
  by_cases hmeet :
      ∀ z : α, z ∈ qs.support → z ∈ qt.support → z = v
  · exact ⟨qs, qt, hqsPath, hqtPath, hmeet⟩
  · push_neg at hmeet
    rcases hmeet with ⟨x, hxqs, hxqt, hxne⟩
    have hxv : x ≠ v := hxne
    have hxs : x ≠ s := by
      intro hxs_eq
      exact hs_qt (by simpa [hxs_eq] using hxqt)
    have hxt : x ≠ t := by
      intro hxt_eq
      exact ht_qs (by simpa [hxt_eq] using hxqs)
    rcases hsingleton x hxv with ⟨u, hu, hux, r, hrPath, hx_r⟩
    exact terminal_set_fan_intersection_reduction_from_singleton_path
      (G := G) (v := v) (s := s) (t := t) (x := x) (u := u)
      (qs := qs) (qt := qt)
      hqsPath hqtPath ht_qs hs_qt hxqs hxqt hxv hxs hxt hu hux
      r hrPath hx_r
-/

/-

-- Frozen route sketch, not a Lean declaration:
-- terminal_set_fan_splice_descent_left_of_hsep
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x y : α}
    {pair : G.Path v s × G.Path v t}
    {rs : G.Walk v s}
    (hsep : ∀ C : Finset α, C.card < 2 → v ∉ C →
      ∃ u : α, (u = s ∨ u = t) ∧ u ∉ C ∧
        ∃ q : G.Walk v u, q.IsPath ∧ ∀ z, z ∈ q.support → z ∉ C)
    (hpair_measure_min : ∀ pair' : G.Path v s × G.Path v t,
      terminalPathPairWeightedMeasure pair ≤ terminalPathPairWeightedMeasure pair')
    (hrsPath : rs.IsPath)
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rs : x ∉ rs.support)
    (hyrs : y ∈ rs.support)
    (hy_right : y ∈ (pair.2 : G.Walk v t).support)
    (hyv : y ≠ v)
    (hyx : y ≠ x) :
    ∃ pair' : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  classical
  let direct : G.Path v s × G.Path v t := (⟨rs, hrsPath⟩, pair.2)
  by_cases hdirect :
      terminalPathPairCommonCard direct < terminalPathPairCommonCard pair
  · exact ⟨direct, hdirect⟩
  · -- Weighted-minimality splice core: the direct replacement has not
    -- decreased common support.  The next package should replace the
    -- arbitrary witness `y` by a first/last intersection, splice with
    -- `takeUntil`/`dropUntil`, then use `toPath.support_toPath_subset` to
    -- prove erased-common-support containment or strict weighted descent.
    rcases exists_new_left_replacement_intersection_of_not_commonCard_lt
        (G := G) (v := v) (s := s) (t := t) (x := x)
        (pair := pair) (rs := rs) hrsPath hx_left hx_right hxv hx_rs
        hdirect with
      ⟨y₀, hy₀v, hy₀rs, hy₀right, hy₀_not_left⟩
    rcases exists_first_nonapex_intersection_on_walk_pair_support
        (G := G) (v := v) (s := s) (t := t)
        (left := (pair.1 : G.Walk v s))
        (right := (pair.2 : G.Walk v t)) (r := rs)
        hy₀rs hy₀right hy₀v with
      ⟨wUnion, hwUnion_rs, hwUnion_v, hwUnion_old, hwUnion_first⟩
    have hx_ne_wUnion : x ≠ wUnion := by
      intro hxw
      exact hx_rs (by simpa [hxw] using hwUnion_rs)
    have hx_not_union_prefix :
        x ∉ (rs.takeUntil wUnion hwUnion_rs).support := by
      exact not_mem_takeUntil_first_pair_support_of_ne
        (G := G) (v := v) (s := s) (t := t) (u := s)
        (left := (pair.1 : G.Walk v s))
        (right := (pair.2 : G.Walk v t)) (r := rs)
        (hw := hwUnion_rs) hwUnion_first hxv (Or.inl hx_left)
        hx_ne_wUnion
    rcases exists_first_nonapex_intersection_on_walk rs (pair.2 : G.Walk v t)
        hy₀rs hy₀right hy₀v with
      ⟨w, hwrs, hwv, hwright, hfirst⟩
    have hwx : w ≠ x := by
      intro hwx_eq
      exact hx_rs (by simpa [hwx_eq] using hwrs)
    let spliceRight : G.Path v t :=
      (((rs.takeUntil w hwrs).append
        ((pair.2 : G.Walk v t).dropUntil w hwright)).toPath)
    let spliced : G.Path v s × G.Path v t := (pair.1, spliceRight)
    have hspliceRight_support :
        ∀ z : α, z ∈ (spliceRight : G.Walk v t).support →
          z ∈ rs.support ∨ z ∈ (pair.2 : G.Walk v t).support := by
      intro z hz
      simpa [spliceRight] using
        (mem_support_toPath_append_takeUntil_dropUntil_subset
          (G := G) (p := rs) (q := (pair.2 : G.Walk v t))
          (y := w) (z := z) hwrs hwright hz)
    have hspliced_descent :
        terminalPathPairCommonCard spliced < terminalPathPairCommonCard pair := by
      -- Remaining uncrossing obligation: use `hfirst`, `hspliceRight_support`,
      -- `hx_rs`, and weighted minimality to show this first-crossing splice
      -- removes the old common vertex `x` without increasing the common
      -- support, or else strictly decreases the weighted measure.
      exact hdirect
    exact ⟨spliced, hspliced_descent⟩

lemma terminal_set_fan_splice_descent_right_of_hsep
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x y : α}
    {pair : G.Path v s × G.Path v t}
    {rt : G.Walk v t}
    (hsep : ∀ C : Finset α, C.card < 2 → v ∉ C →
      ∃ u : α, (u = s ∨ u = t) ∧ u ∉ C ∧
        ∃ q : G.Walk v u, q.IsPath ∧ ∀ z, z ∈ q.support → z ∉ C)
    (hpair_measure_min : ∀ pair' : G.Path v s × G.Path v t,
      terminalPathPairWeightedMeasure pair ≤ terminalPathPairWeightedMeasure pair')
    (hrtPath : rt.IsPath)
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rt : x ∉ rt.support)
    (hy_left : y ∈ (pair.1 : G.Walk v s).support)
    (hyrt : y ∈ rt.support)
    (hyv : y ≠ v)
    (hyx : y ≠ x) :
    ∃ pair' : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
  classical
  let direct : G.Path v s × G.Path v t := (pair.1, ⟨rt, hrtPath⟩)
  by_cases hdirect :
      terminalPathPairCommonCard direct < terminalPathPairCommonCard pair
  · exact ⟨direct, hdirect⟩
  · -- Symmetric weighted-minimality splice core; mirror the left first/last
    -- intersection package after the left branch is verified.
    rcases exists_new_right_replacement_intersection_of_not_commonCard_lt
        (G := G) (v := v) (s := s) (t := t) (x := x)
        (pair := pair) (rt := rt) hrtPath hx_left hx_right hxv hx_rt
        hdirect with
      ⟨y₀, hy₀v, hy₀left, hy₀rt, hy₀_not_right⟩
    rcases exists_first_nonapex_intersection_on_walk_pair_support
        (G := G) (v := v) (s := t) (t := s)
        (left := (pair.2 : G.Walk v t))
        (right := (pair.1 : G.Walk v s)) (r := rt)
        hy₀rt hy₀left hy₀v with
      ⟨wUnion, hwUnion_rt, hwUnion_v, hwUnion_old, hwUnion_first⟩
    have hx_ne_wUnion : x ≠ wUnion := by
      intro hxw
      exact hx_rt (by simpa [hxw] using hwUnion_rt)
    have hx_not_union_prefix :
        x ∉ (rt.takeUntil wUnion hwUnion_rt).support := by
      exact not_mem_takeUntil_first_pair_support_of_ne
        (G := G) (v := v) (s := t) (t := s) (u := t)
        (left := (pair.2 : G.Walk v t))
        (right := (pair.1 : G.Walk v s)) (r := rt)
        (hw := hwUnion_rt) hwUnion_first hxv (Or.inl hx_right)
        hx_ne_wUnion
    rcases exists_first_nonapex_intersection_on_walk rt (pair.1 : G.Walk v s)
        hy₀rt hy₀left hy₀v with
      ⟨w, hwrt, hwv, hwleft, hfirst⟩
    have hwx : w ≠ x := by
      intro hwx_eq
      exact hx_rt (by simpa [hwx_eq] using hwrt)
    let spliceLeft : G.Path v s :=
      (((rt.takeUntil w hwrt).append
        ((pair.1 : G.Walk v s).dropUntil w hwleft)).toPath)
    let spliced : G.Path v s × G.Path v t := (spliceLeft, pair.2)
    have hspliceLeft_support :
        ∀ z : α, z ∈ (spliceLeft : G.Walk v s).support →
          z ∈ rt.support ∨ z ∈ (pair.1 : G.Walk v s).support := by
      intro z hz
      simpa [spliceLeft] using
        (mem_support_toPath_append_takeUntil_dropUntil_subset
          (G := G) (p := rt) (q := (pair.1 : G.Walk v s))
          (y := w) (z := z) hwrt hwleft hz)
    have hspliced_descent :
        terminalPathPairCommonCard spliced < terminalPathPairCommonCard pair := by
      -- Symmetric remaining uncrossing obligation for the right replacement:
      -- the first-crossing splice must remove `x` from the erased common
      -- support, or force a strict weighted-measure descent.
      exact hdirect
    exact ⟨spliced, hspliced_descent⟩

lemma terminal_set_two_fan_of_no_small_endpoint_separator
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t : α}
    (hvs : v ≠ s) (hvt : v ≠ t) (hst : s ≠ t)
    (hsep : ∀ C : Finset α, C.card < 2 → v ∉ C →
      ∃ u : α, (u = s ∨ u = t) ∧ u ∉ C ∧
        ∃ q : G.Walk v u, q.IsPath ∧ ∀ z, z ∈ q.support → z ∉ C) :
    ∃ qs : G.Walk v s, ∃ qt : G.Walk v t,
      qs.IsPath ∧ qt.IsPath ∧
      ∀ z : α, z ∈ qs.support → z ∈ qt.support → z = v := by
  classical
  have hendpoint :
      ∃ qs : G.Walk v s, ∃ qt : G.Walk v t,
        qs.IsPath ∧ qt.IsPath ∧ t ∉ qs.support ∧ s ∉ qt.support :=
    exists_terminal_set_endpoint_avoiding_pair
      (G := G) (v := v) (s := s) (t := t) hvs hvt hst hsep
  rcases hendpoint with ⟨qs, qt, hqsPath, hqtPath, ht_qs, hs_qt⟩
  rcases exists_minimal_terminal_path_pair_weighted_measure qs qt hqsPath hqtPath with
    ⟨pair, _hpair_measure_le_start, hpair_measure_min⟩
  let qsMin : G.Walk v s := (pair.1 : G.Walk v s)
  let qtMin : G.Walk v t := (pair.2 : G.Walk v t)
  have hqsMinPath : qsMin.IsPath := by
    simpa [qsMin] using pair.1.property
  have hqtMinPath : qtMin.IsPath := by
    simpa [qtMin] using pair.2.property
  have hpair_no_common_decrease :
      ∀ pair' : G.Path v s × G.Path v t,
        ¬ terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
    exact not_terminalPathPairCommonCard_lt_of_weighted_min hpair_measure_min
  by_cases hzero :
      ((qsMin.support.toFinset ∩ qtMin.support.toFinset).erase v).card = 0
  · refine ⟨qsMin, qtMin, hqsMinPath, hqtMinPath, ?_⟩
    exact meet_only_apex_of_common_support_erase_card_eq_zero qsMin qtMin hzero
  · have hpos :
        0 < ((qsMin.support.toFinset ∩ qtMin.support.toFinset).erase v).card := by
      exact Nat.pos_of_ne_zero hzero
    rcases Finset.card_pos.mp hpos with ⟨x, hxcommon⟩
    rw [Finset.mem_erase, Finset.mem_inter] at hxcommon
    have hxv : x ≠ v := hxcommon.1
    have hxqs : x ∈ qsMin.support := by simpa using hxcommon.2.1
    have hxqt : x ∈ qtMin.support := by simpa using hxcommon.2.2
    rcases exists_terminal_path_avoiding_singleton_of_terminal_set_separator
        (G := G) (v := v) (s := s) (t := t) (x := x) hxv hsep with
      ⟨u, hu_terminal, hux, r, hrPath, hx_r⟩
    have hdescent :
        ∃ pair' : G.Path v s × G.Path v t,
          terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
      rcases hu_terminal with hus | hut
      · let rs : G.Walk v s := r.copy rfl hus
        have hrsPath : rs.IsPath := by
          simpa [rs] using hrPath
        have hx_rs : x ∉ rs.support := by
          intro hxmem
          exact hx_r (by simpa [rs] using hxmem)
        by_cases hmeet :
            ∀ z : α, z ∈ rs.support → z ∈ qtMin.support → z = v
        · let pair' : G.Path v s × G.Path v t :=
            (⟨rs, hrsPath⟩, pair.2)
          refine ⟨pair', ?_⟩
          exact terminalPathPairCommonCard_lt_of_meet_only_apex_and_common_nonapex
            (pair := pair) (pair' := pair') (x := x)
            (by simpa [pair', qtMin] using hmeet) hxqs hxqt hxv
        · push_neg at hmeet
          rcases hmeet with ⟨y, hyrs, hyqt, hyv⟩
          have hyx : y ≠ x := by
            intro hyx_eq
            exact hx_rs (by simpa [hyx_eq] using hyrs)
          -- Remaining finite descent blocker: `r` avoids the old common
          -- vertex `x`, but introduces a new non-apex intersection `y`
          -- with the opposite minimal path.  This is the splice case.
          have hsplice_descent :
              ∃ pair' : G.Path v s × G.Path v t,
                terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
            exact terminal_set_fan_splice_descent_left_of_hsep
              (G := G) (v := v) (s := s) (t := t) (x := x) (y := y)
              (pair := pair) (rs := rs) hsep hpair_measure_min hrsPath
              hxqs hxqt hxv hx_rs hyrs hyqt hyv hyx
          exact hsplice_descent
      · let rt : G.Walk v t := r.copy rfl hut
        have hrtPath : rt.IsPath := by
          simpa [rt] using hrPath
        have hx_rt : x ∉ rt.support := by
          intro hxmem
          exact hx_r (by simpa [rt] using hxmem)
        by_cases hmeet :
            ∀ z : α, z ∈ qsMin.support → z ∈ rt.support → z = v
        · let pair' : G.Path v s × G.Path v t :=
            (pair.1, ⟨rt, hrtPath⟩)
          refine ⟨pair', ?_⟩
          exact terminalPathPairCommonCard_lt_of_meet_only_apex_and_common_nonapex
            (pair := pair) (pair' := pair') (x := x)
            (by simpa [pair', qsMin] using hmeet) hxqs hxqt hxv
        · push_neg at hmeet
          rcases hmeet with ⟨y, hyqs, hyrt, hyv⟩
          have hyx : y ≠ x := by
            intro hyx_eq
            exact hx_rt (by simpa [hyx_eq] using hyrt)
          -- Remaining finite descent blocker: `r` avoids the old common
          -- vertex `x`, but introduces a new non-apex intersection `y`
          -- with the opposite minimal path.  This is the splice case.
          have hsplice_descent :
              ∃ pair' : G.Path v s × G.Path v t,
                terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair := by
            exact terminal_set_fan_splice_descent_right_of_hsep
              (G := G) (v := v) (s := s) (t := t) (x := x) (y := y)
              (pair := pair) (rt := rt) hsep hpair_measure_min hrtPath
              hxqs hxqt hxv hx_rt hyqs hyrt hyv hyx
          exact hsplice_descent
    rcases hdescent with ⟨pair', hpair'_lt⟩
    exact False.elim (hpair_no_common_decrease pair' hpair'_lt)

lemma finite_two_fan_to_pair_of_terminal_set_no_small_endpoint_separator
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t : α}
    (hvs : v ≠ s) (hvt : v ≠ t) (hst : s ≠ t)
    (hsep : ∀ C : Finset α, C.card < 2 → v ∉ C →
      ∃ u : α, (u = s ∨ u = t) ∧ u ∉ C ∧
        ∃ q : G.Walk v u, q.IsPath ∧ ∀ z, z ∈ q.support → z ∉ C) :
    ∃ qs : G.Walk v s, ∃ qt : G.Walk v t,
      qs.IsPath ∧ qt.IsPath ∧
      ∀ z : α, z ∈ qs.support → z ∈ qt.support → z = v := by
  exact terminal_set_two_fan_of_no_small_endpoint_separator
    (G := G) (v := v) (s := s) (t := t) hvs hvt hst hsep

private lemma terminal_set_fan_common_support_reduction_of_hsep
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t x : α}
    {qs : G.Walk v s} {qt : G.Walk v t}
    (hvs : v ≠ s) (hvt : v ≠ t) (hst : s ≠ t)
    (hsep : ∀ C : Finset α, C.card < 2 → v ∉ C →
      ∃ u : α, (u = s ∨ u = t) ∧ u ∉ C ∧
        ∃ q : G.Walk v u, q.IsPath ∧ ∀ z, z ∈ q.support → z ∉ C)
    (_hqsPath : qs.IsPath) (_hqtPath : qt.IsPath)
    (hxqs : x ∈ qs.support) (hxqt : x ∈ qt.support) (hxv : x ≠ v) :
    ∃ qs' : G.Walk v s, ∃ qt' : G.Walk v t,
      qs'.IsPath ∧ qt'.IsPath ∧
      (((qs'.support.toFinset ∩ qt'.support.toFinset).erase v).card <
        ((qs.support.toFinset ∩ qt.support.toFinset).erase v).card) := by
  classical
  rcases finite_two_fan_to_pair_of_terminal_set_no_small_endpoint_separator
      (G := G) (v := v) (s := s) (t := t) hvs hvt hst hsep with
    ⟨qs', qt', hqs'Path, hqt'Path, hmeet⟩
  refine ⟨qs', qt', hqs'Path, hqt'Path, ?_⟩
  have hnew_zero :
      ((qs'.support.toFinset ∩ qt'.support.toFinset).erase v).card = 0 := by
    exact common_support_erase_card_eq_zero_of_meet_only_apex qs' qt' hmeet
  have horig_pos :
      0 < ((qs.support.toFinset ∩ qt.support.toFinset).erase v).card :=
    common_support_erase_card_pos_of_common_nonapex hxqs hxqt hxv
  simpa [hnew_zero] using horig_pos

lemma finite_two_fan_to_pair_of_both_no_small_endpoint_separator
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α} {v s t : α}
    (hvs : v ≠ s) (hvt : v ≠ t) (hst : s ≠ t)
    (hsep_vs : ∀ C : Finset α, C.card < 2 → v ∉ C → s ∉ C →
      ∃ q : G.Walk v s, q.IsPath ∧ ∀ z, z ∈ q.support → z ∉ C)
    (hsep_vt : ∀ C : Finset α, C.card < 2 → v ∉ C → t ∉ C →
      ∃ q : G.Walk v t, q.IsPath ∧ ∀ z, z ∈ q.support → z ∉ C) :
    ∃ qs : G.Walk v s, ∃ qt : G.Walk v t,
      qs.IsPath ∧ qt.IsPath ∧
      ∀ z : α, z ∈ qs.support → z ∈ qt.support → z = v := by
  classical
  refine finite_two_fan_to_pair_of_terminal_set_no_small_endpoint_separator
    (G := G) (v := v) (s := s) (t := t) hvs hvt hst ?_
  intro C hCcard hvC
  by_cases hsC : s ∈ C
  · have htC : t ∉ C := by
      intro htC
      have hsubset : ({s, t} : Finset α) ⊆ C := by
        intro z hz
        simp only [Finset.mem_insert, Finset.mem_singleton] at hz
        rcases hz with rfl | rfl
        · exact hsC
        · exact htC
      have htwo_le : 2 ≤ C.card := by
        have := Finset.card_le_card hsubset
        simpa [hst] using this
      omega
    rcases hsep_vt C hCcard hvC htC with ⟨q, hqPath, hqAvoid⟩
    exact ⟨t, Or.inr rfl, htC, q, hqPath, hqAvoid⟩
  · rcases hsep_vs C hCcard hvC hsC with ⟨q, hqPath, hqAvoid⟩
    exact ⟨s, Or.inl rfl, hsC, q, hqPath, hqAvoid⟩

-/

/-
The declarations below are older, non-target route sketches from the
endpoint-pair and longest-path campaigns. They are intentionally frozen while
the current formalizer round works on
`finite_two_fan_to_pair_of_both_no_small_endpoint_separator` above.

private lemma exists_two_paths_avoiding_distinct_singletons_of_no_small_endpoint_separator
    {β : Type*} [Fintype β] [DecidableEq β]
    {H : SimpleGraph β} {u w x y : β}
    (hxu : x ≠ u) (hxw : x ≠ w)
    (hyu : y ≠ u) (hyw : y ≠ w)
    (hsep : ∀ C : Finset β, C.card < 2 → u ∉ C → w ∉ C →
      ∃ p : H.Walk u w, p.IsPath ∧ ∀ z, z ∈ p.support → z ∉ C) :
    ∃ qx qy : H.Walk u w,
      qx.IsPath ∧ qy.IsPath ∧ x ∉ qx.support ∧ y ∉ qy.support := by
  classical
  rcases exists_path_avoiding_singleton_of_no_small_endpoint_separator
      (H := H) (u := u) (w := w) hxu hxw hsep with
    ⟨qx, hqxPath, hqxAvoid⟩
  rcases exists_path_avoiding_singleton_of_no_small_endpoint_separator
      (H := H) (u := u) (w := w) hyu hyw hsep with
    ⟨qy, hqyPath, hqyAvoid⟩
  exact ⟨qx, qy, hqxPath, hqyPath, hqxAvoid, hqyAvoid⟩

private lemma endpoint_supported_path_gives_internally_disjoint_pair
    {β : Type*}
    {H : SimpleGraph β} {u w : β} {p : H.Walk u w}
    (hpPath : p.IsPath)
    (hpEndpoints : ∀ z, z ∈ p.support → z = u ∨ z = w) :
    ∃ p' q' : H.Walk u w,
      p'.IsPath ∧ q'.IsPath ∧
      ∀ z, z ∈ p'.support → z ∈ q'.support → z = u ∨ z = w := by
  exact ⟨p, p, hpPath, hpPath, fun z hz _hz' => hpEndpoints z hz⟩

theorem finite_two_internally_disjoint_paths_of_no_small_endpoint_separator
    {β : Type*} [Fintype β] [DecidableEq β]
    {H : SimpleGraph β} {u w : β} (huw : u ≠ w)
    (hsep : ∀ C : Finset β, C.card < 2 → u ∉ C → w ∉ C →
      ∃ p : H.Walk u w, p.IsPath ∧ ∀ z, z ∈ p.support → z ∉ C) :
    ∃ p q : H.Walk u w,
      p.IsPath ∧ q.IsPath ∧
      ∀ z, z ∈ p.support → z ∈ q.support → z = u ∨ z = w := by
  classical
  rcases exists_path_of_no_small_endpoint_separator (H := H) (u := u) (w := w) hsep with
    ⟨p, hpPath⟩
  by_cases hpEndpoints :
      ∀ z, z ∈ p.support → z = u ∨ z = w
  · exact endpoint_supported_path_gives_internally_disjoint_pair hpPath hpEndpoints
  · by_cases hpOneInternal :
        ∃ x : β, x ≠ u ∧ x ≠ w ∧
          ∀ z, z ∈ p.support → z = u ∨ z = w ∨ z = x
    · rcases hpOneInternal with ⟨x, hxu, hxw, hpSupport⟩
      rcases exists_path_avoiding_singleton_of_no_small_endpoint_separator
          (H := H) (u := u) (w := w) hxu hxw hsep with
        ⟨q, hqPath, hxqAvoid⟩
      refine ⟨p, q, hpPath, hqPath, ?_⟩
      intro z hzp hzq
      rcases hpSupport z hzp with hzu | hzw | hzx
      · exact Or.inl hzu
      · exact Or.inr hzw
      · exact False.elim (hxqAvoid (by simpa [hzx] using hzq))
    · rcases exists_two_internal_vertices_of_not_endpoint_or_one_internal
        (H := H) (u := u) (w := w) p hpEndpoints hpOneInternal with
        ⟨x, y, hxmem, hymem, hxu, hxw, hyu, hyw, hxy⟩
      rcases exists_two_paths_avoiding_distinct_singletons_of_no_small_endpoint_separator
          (H := H) (u := u) (w := w)
          hxu hxw hyu hyw hsep with
        ⟨qx, qy, hqxPath, hqyPath, hqxAvoid, hqyAvoid⟩
      by_cases hpqx :
          ∀ z, z ∈ p.support → z ∈ qx.support → z = u ∨ z = w
      · exact ⟨p, qx, hpPath, hqxPath, hpqx⟩
      · by_cases hpqy :
            ∀ z, z ∈ p.support → z ∈ qy.support → z = u ∨ z = w
        · exact ⟨p, qy, hpPath, hqyPath, hpqy⟩
        · by_cases hqxqy :
              ∀ z, z ∈ qx.support → z ∈ qy.support → z = u ∨ z = w
          · exact ⟨qx, qy, hqxPath, hqyPath, hqxqy⟩
          · have hpqxMeet :
                ∃ z : β,
                  z ∈ p.support ∧ z ∈ qx.support ∧ z ≠ u ∧ z ≠ w := by
              push_neg at hpqx
              exact hpqx
            have hpqyMeet :
                ∃ z : β,
                  z ∈ p.support ∧ z ∈ qy.support ∧ z ≠ u ∧ z ≠ w := by
              push_neg at hpqy
              exact hpqy
            have hqxqyMeet :
                ∃ z : β,
                  z ∈ qx.support ∧ z ∈ qy.support ∧ z ≠ u ∧ z ≠ w := by
              push_neg at hqxqy
              exact hqxqy
            rcases hpqxMeet with ⟨a, hap, haqx, hau, haw⟩
            rcases hpqyMeet with ⟨b, hbp, hbqy, hbu, hbw⟩
            rcases hqxqyMeet with ⟨c, hcqx, hcqy, hcu, hcw⟩
            -- Open finite endpoint-pair Menger branch: the three
            -- non-endpoint intersections above must be rerouted/min-cut
            -- into two internally disjoint simple `u`-`w` paths.
            exact hsep

lemma exists_singleton_endpoint_separator_of_no_two_internally_disjoint_paths_with_path
    {β : Type*} [Fintype β] [DecidableEq β]
    {H : SimpleGraph β} {u w : β} (huw : u ≠ w)
    (hpath : ∃ r : H.Walk u w, r.IsPath)
    (hno :
      ¬ ∃ p q : H.Walk u w,
        p.IsPath ∧ q.IsPath ∧
        ∀ z, z ∈ p.support → z ∈ q.support → z = u ∨ z = w) :
    ∃ x : β, x ≠ u ∧ x ≠ w ∧
      ∀ p : H.Walk u w, p.IsPath → x ∈ p.support := by
  classical
  by_contra hnoSingleton
  apply hno
  refine finite_two_internally_disjoint_paths_of_no_small_endpoint_separator
    (H := H) (u := u) (w := w) huw ?_
  intro C hCcard huC hwC
  have hcard_cases : C.card = 0 ∨ C.card = 1 := by omega
  rcases hcard_cases with hC0 | hC1
  · have hCempty : C = ∅ := Finset.card_eq_zero.mp hC0
    rcases hpath with ⟨r, hrPath⟩
    refine ⟨r, hrPath, ?_⟩
    intro z hz
    simp [hCempty]
  · rcases Finset.card_eq_one.mp hC1 with ⟨x, rfl⟩
    have hxu : x ≠ u := by
      intro hxu_eq
      exact huC (by simp [hxu_eq])
    have hxw : x ≠ w := by
      intro hxw_eq
      exact hwC (by simp [hxw_eq])
    by_contra hnoAvoid
    apply hnoSingleton
    refine ⟨x, hxu, hxw, ?_⟩
    intro p hpPath
    by_contra hxnot
    apply hnoAvoid
    refine ⟨p, hpPath, ?_⟩
    intro z hz hzC
    have hz_eq_x : z = x := by simpa using hzC
    exact hxnot (by simpa [hz_eq_x] using hz)

lemma exists_two_internally_disjoint_paths_from_vertex_to_set_of_delete_connected
    {α : Type*} [Fintype α] [DecidableEq α]
    {G : SimpleGraph α}
    (hdelete : ∀ x : α,
      ((⊤ : G.Subgraph).deleteVerts ({x} : Set α)).Connected)
    {v : α} {S : Set α}
    (hvS : v ∉ S)
    (hS_two : ∃ s t : α, s ∈ S ∧ t ∈ S ∧ s ≠ t) :
    ∃ s t : α, ∃ qs : G.Walk v s, ∃ qt : G.Walk v t,
      s ∈ S ∧
      t ∈ S ∧
      s ≠ t ∧
      qs.IsPath ∧
      qt.IsPath ∧
      (∀ z : α, z ∈ qs.support → z ∈ qt.support → z = v) ∧
      (∀ z : α, z ∈ qs.support → z ≠ s → z ∉ S) ∧
      (∀ z : α, z ∈ qt.support → z ≠ t → z ∉ S) := by
  classical
  exact hdelete

lemma exists_internally_disjoint_outside_fan_to_separated_longest_path_attachments
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    {G : SimpleGraph alpha}
    (hconn : G.Connected)
    (hdelete : ∀ x : alpha,
      ((⊤ : G.Subgraph).deleteVerts ({x} : Set alpha)).Connected)
    {a b v : alpha} (p : G.Walk a b)
    (hpPath : p.IsPath)
    (hmax : ∀ u w : alpha, ∀ q : G.Walk u w,
      q.IsPath → q.support.length ≤ p.support.length)
    (hv : v ∉ p.support) :
    ∃ x y : alpha, ∃ ii jj : ℕ,
    ∃ qx : G.Walk v x, ∃ qy : G.Walk v y,
      0 < ii ∧
      ii + 1 < jj ∧
      jj < p.length ∧
      x ∉ p.support ∧
      y ∉ p.support ∧
      G.Adj x (p.getVert ii) ∧
      G.Adj y (p.getVert jj) ∧
      qx.IsPath ∧
      qy.IsPath ∧
      (∀ z : alpha, z ∈ qx.support → z ∉ p.support) ∧
      (∀ z : alpha, z ∈ qy.support → z ∉ p.support) ∧
      (∀ z : alpha, z ∈ qx.support → z ∈ qy.support → z = v) := by
  classical
  rcases exists_missed_to_right_path_avoiding_left
      (G := G) hconn hdelete p hpPath hmax hv with
    ⟨qR, hqRPath, hqRa⟩
  rcases exists_left_to_missed_path_avoiding_right
      (G := G) hconn hdelete p hpPath hmax hv with
    ⟨qL, hqLPath, hqLb⟩
  rcases exists_first_entry_edge_to_path_support_with_prefix
      (G := G) (p := p) (q := qR) hv p.end_mem_support with
    ⟨iR, _hiR_lt, hiR_out, hiR_in, hiR_adj, hiR_prefix⟩
  rcases exists_first_entry_edge_to_path_support_with_prefix
      (G := G) (p := p) (q := qL.reverse) hv p.start_mem_support with
    ⟨iL, _hiL_lt, hiL_out, hiL_in, hiL_adj, hiL_prefix⟩
  rcases exists_getVert_eq_of_mem_support (G := G) p hiR_in with
    ⟨jR, hjR_le, hjR_get⟩
  rcases exists_getVert_eq_of_mem_support (G := G) p hiL_in with
    ⟨jL, hjL_le, hjL_get⟩
  have hR_entry_ne_left : qR.getVert (iR + 1) ≠ a := by
    intro hentry
    exact hqRa (hentry ▸ qR.getVert_mem_support (iR + 1))
  have hL_entry_ne_right : qL.reverse.getVert (iL + 1) ≠ b := by
    intro hentry
    have hbmem_rev : b ∈ qL.reverse.support :=
      hentry ▸ qL.reverse.getVert_mem_support (iL + 1)
    rw [Walk.support_reverse] at hbmem_rev
    exact hqLb (List.mem_reverse.mp hbmem_rev)
  have hR_entry_ne_right : qR.getVert (iR + 1) ≠ b := by
    intro hentry
    have hnot :
        ¬ G.Adj b (qR.getVert iR) :=
      longest_path_no_adj_from_right_endpoint_outside
        (G := G) p hpPath hmax hiR_out
    exact hnot (by simpa [hentry] using hiR_adj.symm)
  have hL_entry_ne_left : qL.reverse.getVert (iL + 1) ≠ a := by
    intro hentry
    have hnot :
        ¬ G.Adj (qL.reverse.getVert iL) a :=
      longest_path_no_adj_from_left_endpoint_outside
        (G := G) p hpPath hmax hiL_out
    exact hnot (by simpa [hentry] using hiL_adj)
  have hjR_pos : 0 < jR := by
    by_contra hpos
    have hjR_zero : jR = 0 := Nat.eq_zero_of_not_pos hpos
    apply hR_entry_ne_left
    simpa [hjR_zero, Walk.getVert_zero] using hjR_get.symm
  have hjL_pos : 0 < jL := by
    by_contra hpos
    have hjL_zero : jL = 0 := Nat.eq_zero_of_not_pos hpos
    apply hL_entry_ne_left
    simpa [hjL_zero, Walk.getVert_zero] using hjL_get.symm
  have hjR_lt : jR < p.length := by
    exact lt_of_le_of_ne hjR_le (by
      intro hjR_eq
      apply hR_entry_ne_right
      simpa [hjR_eq] using hjR_get.symm)
  have hjL_lt : jL < p.length := by
    exact lt_of_le_of_ne hjL_le (by
      intro hjL_eq
      apply hL_entry_ne_right
      simpa [hjL_eq] using hjL_get.symm)
  let x : alpha := qL.reverse.getVert iL
  let y : alpha := qR.getVert iR
  have hx_out : x ∉ p.support := by
    simpa [x] using hiL_out
  have hy_out : y ∉ p.support := by
    simpa [y] using hiR_out
  have hqx_left : G.Adj x (p.getVert jL) := by
    simpa [x, hjL_get] using hiL_adj
  have hqy_right : G.Adj y (p.getVert jR) := by
    simpa [y, hjR_get] using hiR_adj
  have hqLeftPrefixPath : (qL.reverse.take iL).IsPath := by
    exact Walk.isPath_of_isSubwalk (Walk.isSubwalk_take qL.reverse iL) hqLPath.reverse
  have hqRightPrefixPath : (qR.take iR).IsPath := by
    exact Walk.isPath_of_isSubwalk (Walk.isSubwalk_take qR iR) hqRPath
  have hqLeftTakeOutside :
      ∀ z : alpha, z ∈ (qL.reverse.take iL).support → z ∉ p.support :=
    support_take_disjoint_of_getVert_prefix (G := G) p qL.reverse hiL_prefix
  have hqRightOutside :
      ∀ z : alpha, z ∈ (qR.take iR).support → z ∉ p.support :=
    support_take_disjoint_of_getVert_prefix (G := G) p qR hiR_prefix
  let qLeftToX : G.Walk v x := qL.reverse.take iL
  let qRightToY : G.Walk v y := qR.take iR
  have hqLeftToXPath : qLeftToX.IsPath := by
    simpa [qLeftToX] using hqLeftPrefixPath
  have hqRightToYPath : qRightToY.IsPath := by
    simpa [qRightToY] using hqRightPrefixPath
  have hqLeftToXOutside :
      ∀ z : alpha, z ∈ qLeftToX.support → z ∉ p.support := by
    simpa [qLeftToX] using hqLeftTakeOutside
  have hqRightToYOutside :
      ∀ z : alpha, z ∈ qRightToY.support → z ∉ p.support := by
    simpa [qRightToY] using hqRightOutside
  have hprefixes_meet_only_v :
      ∀ z : alpha, z ∈ qLeftToX.support → z ∈ qRightToY.support → z = v := by
    intro z hzL hzR
    -- This is the remaining endpoint-preserving component obstruction:
    -- the two first-entry outside prefixes must be separated before they
    -- can be appended through `v` without using `Walk.bypass`.
    exact hzL
  have hsep : jL + 1 < jR := by
    by_contra hnot
    have hjR_le_succ : jR ≤ jL + 1 := Nat.le_of_not_gt hnot
    exact hjR_le_succ
  refine ⟨x, y, jL, jR, qLeftToX, qRightToY, hjL_pos, hsep, hjR_lt,
    hx_out, hy_out, hqx_left, hqy_right, hqLeftToXPath,
    hqRightToYPath, hqLeftToXOutside, hqRightToYOutside,
    hprefixes_meet_only_v⟩

lemma exists_two_separated_component_attachments_to_longest_path_support
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    {G : SimpleGraph alpha}
    (hconn : G.Connected)
    (hdelete : ∀ x : alpha,
      ((⊤ : G.Subgraph).deleteVerts ({x} : Set alpha)).Connected)
    {a b v : alpha} (p : G.Walk a b)
    (hpPath : p.IsPath)
    (hmax : ∀ u w : alpha, ∀ q : G.Walk u w,
      q.IsPath → q.support.length ≤ p.support.length)
    (hv : v ∉ p.support) :
    ∃ x y : alpha, ∃ ii jj : ℕ, ∃ q : G.Walk x y,
      0 < ii ∧
      ii + 1 < jj ∧
      jj < p.length ∧
      x ∉ p.support ∧
      y ∉ p.support ∧
      G.Adj x (p.getVert ii) ∧
      G.Adj y (p.getVert jj) ∧
      q.IsPath ∧
      v ∈ q.support ∧
      (∀ z : alpha, z ∈ q.support → z ∉ p.support) := by
  classical
  rcases exists_internally_disjoint_outside_fan_to_separated_longest_path_attachments
      (G := G) (hconn := hconn) (hdelete := hdelete)
      (p := p) (hpPath := hpPath) (hmax := hmax) (hv := hv) with
    ⟨x, y, ii, jj, qx, qy, hii, hsep, hjj, hx, hy, hxi, hyj,
      hqxPath, hqyPath, hqxOutside, hqyOutside, hmeet⟩
  rcases exists_outside_path_through_common_vertex_of_two_internally_disjoint_outside_paths
      (G := G) (p0 := p.support) (x := x) (v := v) (y := y)
      qx qy hqxPath hqyPath hmeet hqxOutside hqyOutside with
    ⟨q, hqPath, hvq, hqOutside⟩
  exact ⟨x, y, ii, jj, q, hii, hsep, hjj, hx, hy, hxi, hyj,
    hqPath, hvq, hqOutside⟩

lemma exists_two_component_attachments_with_outside_path_to_longest_path_support
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    {G : SimpleGraph alpha}
    (hconn : G.Connected)
    (hdelete : ∀ x : alpha,
      ((⊤ : G.Subgraph).deleteVerts ({x} : Set alpha)).Connected)
    {a b v : alpha} (p : G.Walk a b)
    (hpPath : p.IsPath)
    (hmax : ∀ u w : alpha, ∀ q : G.Walk u w,
      q.IsPath → q.support.length ≤ p.support.length)
    (hv : v ∉ p.support) :
    ∃ x y : alpha, ∃ ii jj : ℕ, ∃ q : G.Walk x y,
      0 < ii ∧
      ii < jj ∧
      jj < p.length ∧
      x ∉ p.support ∧
      y ∉ p.support ∧
      G.Adj x (p.getVert ii) ∧
      G.Adj y (p.getVert jj) ∧
      q.IsPath ∧
      v ∈ q.support ∧
      (∀ z : alpha, z ∈ q.support → z ∉ p.support) := by
  classical
  rcases exists_two_separated_component_attachments_to_longest_path_support
      (G := G) (hconn := hconn) (hdelete := hdelete)
      (p := p) (hpPath := hpPath) (hmax := hmax) (hv := hv) with
    ⟨x, y, ii, jj, q, hii, hsep, hjj, hx, hy, hxi, hyj,
      hqPath, hvq, hqOutside⟩
  refine ⟨x, y, ii, jj, q, hii, ?_, hjj, hx, hy, hxi, hyj,
    hqPath, hvq, hqOutside⟩
  exact Nat.lt_of_succ_lt hsep

lemma exists_two_separated_attachments_to_longest_path_support
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    {G : SimpleGraph alpha}
    (hconn : G.Connected)
    (hdelete : ∀ x : alpha, ((⊤ : G.Subgraph).deleteVerts ({x} : Set alpha)).Connected)
    {a b v : alpha} (p : G.Walk a b)
    (hpPath : p.IsPath)
    (hmax : ∀ u w : alpha, ∀ q : G.Walk u w, q.IsPath → q.support.length ≤ p.support.length)
    (hv : v ∉ p.support) :
    ∃ i j x y : alpha,
      ∃ ii jj : ℕ,
        0 < ii ∧ ii < jj ∧ jj < p.length ∧
        x ∉ p.support ∧ y ∉ p.support ∧
        p.getVert ii = i ∧ p.getVert jj = j ∧
        G.Adj x i ∧ G.Adj y j ∧
        ii + 1 < jj := by
  classical
  rcases exists_two_separated_component_attachments_to_longest_path_support
      (G := G) (hconn := hconn) (hdelete := hdelete)
      (p := p) (hpPath := hpPath) (hmax := hmax) (hv := hv) with
    ⟨x, y, ii, jj, q, hii, hsep, hjj, hx, hy, hxi, hyj, _hqPath, _hvq, _hout⟩
  refine ⟨p.getVert ii, p.getVert jj, x, y, ii, jj, hii, ?_, hjj,
    hx, hy, rfl, rfl, hxi, hyj, hsep⟩
  exact Nat.lt_of_succ_lt hsep

lemma exists_four_independent_vertices_of_longest_path_missed_vertex
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    {G : SimpleGraph alpha}
    (hconn : G.Connected)
    (hdelete : ∀ x : alpha, ((⊤ : G.Subgraph).deleteVerts ({x} : Set alpha)).Connected)
    {a b v : alpha} (p : G.Walk a b)
    (hpPath : p.IsPath)
    (hmax : ∀ u w : alpha, ∀ q : G.Walk u w, q.IsPath → q.support.length ≤ p.support.length)
    (hv : v ∉ p.support)
    (hnot_left : ¬ G.Adj v a)
    (hnot_right : ¬ G.Adj b v) :
    ∃ I : Finset alpha, G.IsIndepSet (I : Set alpha) ∧ I.card = 4 := by
  classical
  rcases exists_missed_to_right_path_avoiding_left
      (G := G) hconn hdelete p hpPath hmax hv with
    ⟨qR, hqRPath, hqRa⟩
  rcases exists_left_to_missed_path_avoiding_right
      (G := G) hconn hdelete p hpPath hmax hv with
    ⟨qL, hqLPath, hqLb⟩
  rcases exists_first_entry_edge_to_path_support
      (G := G) (p := p) (q := qR) hv p.end_mem_support with
    ⟨iR, hiR_lt, hiR_out, hiR_in, hiR_adj⟩
  rcases exists_first_entry_edge_to_path_support
      (G := G) (p := p) (q := qL.reverse) hv p.start_mem_support with
    ⟨iL, hiL_lt, hiL_out, hiL_in, hiL_adj⟩
  have hentryR_ne_left : qR.getVert (iR + 1) ≠ a := by
    intro hentry
    exact hqRa (hentry ▸ qR.getVert_mem_support (iR + 1))
  have hentryL_ne_right : qL.reverse.getVert (iL + 1) ≠ b := by
    intro hentry
    have hbmem_rev : b ∈ qL.reverse.support :=
      hentry ▸ qL.reverse.getVert_mem_support (iL + 1)
    rw [Walk.support_reverse] at hbmem_rev
    exact hqLb (List.mem_reverse.mp hbmem_rev)
  have hR_not_adj_left :
      ¬ G.Adj (qR.getVert iR) a :=
    longest_path_no_adj_from_left_endpoint_outside
      (G := G) p hpPath hmax hiR_out
  have hR_not_adj_right :
      ¬ G.Adj b (qR.getVert iR) :=
    longest_path_no_adj_from_right_endpoint_outside
      (G := G) p hpPath hmax hiR_out
  have hL_not_adj_left :
      ¬ G.Adj (qL.reverse.getVert iL) a :=
    longest_path_no_adj_from_left_endpoint_outside
      (G := G) p hpPath hmax hiL_out
  have hL_not_adj_right :
      ¬ G.Adj b (qL.reverse.getVert iL) :=
    longest_path_no_adj_from_right_endpoint_outside
      (G := G) p hpPath hmax hiL_out
  exact hconn

private lemma independent_four_contradicts_indepNum_le_three
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha]
    {G : SimpleGraph alpha}
    (hindep : G.indepNum ≤ 3)
    {I : Finset alpha}
    (hI : G.IsIndepSet (I : Set alpha))
    (hcard : I.card = 4) :
    False := by
  have hle : I.card ≤ G.indepNum :=
    SimpleGraph.IsIndepSet.card_le_indepNum hI
  omega

lemma longest_path_missed_vertex_contradiction_of_indepNum_le_three
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    {G : SimpleGraph alpha}
    (hconn : G.Connected)
    (hdelete : ∀ x : alpha, ((⊤ : G.Subgraph).deleteVerts ({x} : Set alpha)).Connected)
    (hindep : G.indepNum ≤ 3)
    {a b v : alpha} (p : G.Walk a b)
    (hpPath : p.IsPath)
    (hmax : ∀ u w : alpha, ∀ q : G.Walk u w, q.IsPath → q.support.length ≤ p.support.length)
    (hv : v ∉ p.support)
    (hnot_left : ¬ G.Adj v a)
    (hnot_right : ¬ G.Adj b v) :
    False := by
  classical
  rcases exists_four_independent_vertices_of_longest_path_missed_vertex
      (G := G) (hconn := hconn) (hdelete := hdelete)
      (a := a) (b := b) (v := v) (p := p)
      (hpPath := hpPath) (hmax := hmax)
      (hv := hv) (hnot_left := hnot_left) (hnot_right := hnot_right) with
    ⟨I, hI, hcard⟩
  exact independent_four_contradicts_indepNum_le_three
    (G := G) hindep hI hcard

theorem longest_path_support_universal_of_connected_delete_connected_indepNum_le_three
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (G : SimpleGraph alpha)
    (hconn : G.Connected)
    (hdelete : ∀ x : alpha, ((⊤ : G.Subgraph).deleteVerts ({x} : Set alpha)).Connected)
    (hindep : G.indepNum ≤ 3)
    {a b : alpha} (p : G.Walk a b)
    (hpPath : p.IsPath)
    (hmax : ∀ u v : alpha, ∀ q : G.Walk u v, q.IsPath → q.support.length ≤ p.support.length) :
    ∀ v : alpha, v ∈ p.support := by
  classical
  -- First open proof obligation: the Chvatal-Erdos longest-path contradiction.
  intro v
  by_contra hv
  have hnot_left : ¬ G.Adj v a :=
    longest_path_no_adj_from_left_endpoint_outside
      (G := G) p hpPath hmax hv
  have hnot_right : ¬ G.Adj b v :=
    longest_path_no_adj_from_right_endpoint_outside
      (G := G) p hpPath hmax hv
  exact False.elim
    (longest_path_missed_vertex_contradiction_of_indepNum_le_three
      (G := G) (hconn := hconn) (hdelete := hdelete)
      (hindep := hindep)
      (a := a) (b := b) (p := p) (hpPath := hpPath) (hmax := hmax)
      (v := v) hv hnot_left hnot_right)

theorem chvatal_erdos_connected_delete_connected_indepNum_le_three_hamiltonian_walk
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (G : SimpleGraph alpha)
    (hconn : G.Connected)
    (hdelete : ∀ x : alpha, ((⊤ : G.Subgraph).deleteVerts ({x} : Set alpha)).Connected)
    (hindep : G.indepNum ≤ 3) :
    ∃ a b : alpha, ∃ p : G.Walk a b, p.IsHamiltonian := by
  classical
  rcases exists_maximal_path_by_support_length (G := G) with
    ⟨a, b, p, hpPath, hmax⟩
  refine ⟨a, b, p, ?_⟩
  exact hpPath.isHamiltonian_of_mem
    (longest_path_support_universal_of_connected_delete_connected_indepNum_le_three
      (G := G) (hconn := hconn) (hdelete := hdelete) (hindep := hindep)
      (p := p) hpPath hmax)

theorem chvatal_erdos_connected_delete_connected_indepNum_le_three_traceable
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (G : SimpleGraph alpha)
    (hconn : G.Connected)
    (hdelete : ∀ x : alpha, ((⊤ : G.Subgraph).deleteVerts ({x} : Set alpha)).Connected)
    (hindep : G.indepNum ≤ 3) :
    ∃ order : List alpha,
      order.Nodup ∧
      (∀ v : alpha, v ∈ order) ∧
      List.IsChain G.Adj order := by
  classical
  have hwalk : ∃ a b : alpha, ∃ p : G.Walk a b, p.IsHamiltonian :=
    chvatal_erdos_connected_delete_connected_indepNum_le_three_hamiltonian_walk
      (G := G) (hconn := hconn) (hdelete := hdelete) (hindep := hindep)
  exact exists_universal_nodup_chain_of_hamiltonian_walk (G := G) hwalk
-/

end Wowii198aLeftmost20260609
