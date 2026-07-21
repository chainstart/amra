/-
Copyright 2026 The Formal Conjectures Authors.

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

import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.SpecialFunctions.Complex.Circle
import Mathlib.Analysis.InnerProductSpace.Convex
import Mathlib.Analysis.Convex.PathConnected
import Mathlib.Analysis.Convex.Between
import Mathlib.Analysis.Normed.Module.Connected
import Mathlib.Analysis.Normed.Affine.AddTorsor
import Mathlib.Combinatorics.SimpleGraph.Finite
import Mathlib.Combinatorics.SimpleGraph.Paths
import Mathlib.Geometry.Euclidean.Angle.Unoriented.Basic
import FormalConjecturesForMathlib.Geometry.Euclidean
import FormalConjecturesForMathlib.Geometry.Metric
import FormalConjecturesForMathlib.Topology.MetricSpace.MetricSeparated
import FormalConjectures.Util.Attributes.Basic

/-!
# Erdős Problem 1084

*References:*
- [erdosproblems.com/1084](https://www.erdosproblems.com/1084)
- H. Harborth, "Lösung zu Problem 664A", *Elemente der Mathematik* 29 (1974), 14-15
- [Contact numbers for totally separable domains](https://arxiv.org/abs/1601.00145)
  by *Károly Bezdek* and *Muhammad A. Khan*

Let `f_2(n)` be the maximum number of pairs of points at distance exactly `1`
among any set of `n` points in `ℝ²`, under the condition that all pairwise
distances are at least `1`.

Estimate the growth of `f_2(n)`.

Status: open.

The Harborth source theorem is represented below only as an explicit hypothesis:
finite `2`-separated disk-center sets have at most
`⌊3N - sqrt (12N - 3)⌋` contact pairs at distance `2`. The local wrapper proves
the conversion from that contact-number convention to the repository's
`unitDistNum` convention by scaling centers by `2`.

Source-audit note: this promotion relies on the Harborth 1974 planar contact-number
bound as cited by Bezdek--Khan, Theorem 3.1 of arXiv:1601.00145, only through the
explicit source hypothesis below.

Durable source note, 2026-07-09: Bezdek--Khan, "Contact numbers for sphere packings",
arXiv:1601.00145, Section 3.1, Theorem 3.1, cites Harborth and states
`c(n, 2) = floor (3n - sqrt (12n - 3))` for `n >= 2`, where `c(n, d)` is the
maximum number of touching pairs among `n` non-overlapping unit balls in
Euclidean `d`-space. This is recorded as provenance for
`HarborthTwoSeparatedContactUpperGe4Source`; no Lean proof term for that source
theorem is introduced here.
-/

open Finset Filter Metric Real
open scoped EuclideanGeometry InnerProductSpace

/--
Two contact neighbors of a common point in a `2`-separated planar configuration have
real inner product at most `2` after translation to the common point.
-/
@[category API, AMS 52]
theorem Erdos1084.twoSeparated_contact_neighbors_inner_le_two
    {p q r : ℝ^2}
    (hpq : dist p q = 2)
    (hpr : dist p r = 2)
    (hqr : 2 ≤ dist q r) :
    ⟪q - p, r - p⟫_ℝ ≤ 2 := by
  have hqp : ‖q - p‖ = 2 := by
    rw [← dist_eq_norm, dist_comm, hpq]
  have hrp : ‖r - p‖ = 2 := by
    rw [← dist_eq_norm, dist_comm, hpr]
  have hqr_norm : 2 ≤ ‖q - r‖ := by
    simpa [dist_eq_norm] using hqr
  have hqr_sq : 4 ≤ ‖q - r‖ ^ 2 := by
    nlinarith [norm_nonneg (q - r)]
  have h_expand := norm_sub_sq_real (q - p) (r - p)
  rw [show q - p - (r - p) = q - r by abel, hqp, hrp] at h_expand
  nlinarith

/--
Two contact neighbors of a common point in a `2`-separated planar configuration form an
angle of at least `π / 3` after translation to the common point.
-/
@[category API, AMS 52]
theorem Erdos1084.twoSeparated_contact_neighbors_angle_ge_pi_div_three
    {p q r : ℝ^2}
    (hpq : dist p q = 2)
    (hpr : dist p r = 2)
    (hqr : 2 ≤ dist q r) :
    Real.pi / 3 ≤
      InnerProductGeometry.angle (q - p) (r - p) := by
  have hqp : ‖q - p‖ = 2 := by
    rw [← dist_eq_norm, dist_comm, hpq]
  have hrp : ‖r - p‖ = 2 := by
    rw [← dist_eq_norm, dist_comm, hpr]
  have hinner :=
    Erdos1084.twoSeparated_contact_neighbors_inner_le_two hpq hpr hqr
  have hratio :
      ⟪q - p, r - p⟫_ℝ / (‖q - p‖ * ‖r - p‖) ≤ (1 / 2 : ℝ) := by
    rw [hqp, hrp]
    norm_num at ⊢
    linarith
  rw [InnerProductGeometry.angle]
  calc
    Real.pi / 3 = Real.arccos (Real.cos (Real.pi / 3)) := by
      rw [Real.arccos_cos (by positivity) (by nlinarith [Real.pi_pos])]
    _ = Real.arccos (1 / 2) := by rw [Real.cos_pi_div_three]
    _ ≤ Real.arccos (⟪q - p, r - p⟫_ℝ / (‖q - p‖ * ‖r - p‖)) :=
      Real.arccos_le_arccos hratio

/--
Two vertex-disjoint contact edges in a `2`-separated planar configuration have disjoint
open segments.
-/
@[category API, AMS 52]
theorem Erdos1084.twoSeparated_disjoint_contact_openSegments_disjoint
    {p q r s : ℝ^2}
    (hpq : dist p q = 2)
    (hrs : dist r s = 2)
    (hpr : 2 ≤ dist p r)
    (hps : 2 ≤ dist p s)
    (hqr : 2 ≤ dist q r)
    (hqs : 2 ≤ dist q s) :
    Disjoint (openSegment ℝ p q) (openSegment ℝ r s) := by
  rw [Set.disjoint_left]
  intro z hzpq hzrs
  rw [openSegment_eq_image_lineMap] at hzpq hzrs
  rcases hzpq with ⟨a, ha, hza⟩
  rcases hzrs with ⟨b, hb, hzb⟩
  have hpz : dist p z = 2 * a := by
    rw [← hza, dist_left_lineMap, hpq, Real.norm_eq_abs, abs_of_pos ha.1]
    ring
  have hqz : dist q z = 2 * (1 - a) := by
    rw [← hza, dist_right_lineMap, hpq, Real.norm_eq_abs,
      abs_of_pos (sub_pos.mpr ha.2)]
    ring
  have hrz : dist r z = 2 * b := by
    rw [← hzb, dist_left_lineMap, hrs, Real.norm_eq_abs, abs_of_pos hb.1]
    ring
  have hsz : dist s z = 2 * (1 - b) := by
    rw [← hzb, dist_right_lineMap, hrs, Real.norm_eq_abs,
      abs_of_pos (sub_pos.mpr hb.2)]
    ring
  have hpr_tri := dist_triangle p z r
  have hps_tri := dist_triangle p z s
  have hqr_tri := dist_triangle q z r
  have hqs_tri := dist_triangle q z s
  rw [hpz, dist_comm z r, hrz] at hpr_tri
  rw [hpz, dist_comm z s, hsz] at hps_tri
  rw [hqz, dist_comm z r, hrz] at hqr_tri
  rw [hqz, dist_comm z s, hsz] at hqs_tri
  have ha_eq : a = 1 / 2 := by nlinarith
  have hb_eq : b = 1 / 2 := by nlinarith
  have hpz_one : dist p z = 1 := by rw [hpz, ha_eq]; norm_num
  have hrz_one : dist r z = 1 := by rw [hrz, hb_eq]; norm_num
  have hsz_one : dist s z = 1 := by rw [hsz, hb_eq]; norm_num
  have hpr_eq : dist p r = 2 := by nlinarith
  have hps_eq : dist p s = 2 := by nlinarith
  have huz : ‖z - p‖ = 1 := by rw [← dist_eq_norm, dist_comm, hpz_one]
  have hur : ‖r - z‖ = 1 := by rw [← dist_eq_norm, hrz_one]
  have hus : ‖s - z‖ = 1 := by rw [← dist_eq_norm, hsz_one]
  have hur_sum : ‖(z - p) + (r - z)‖ = ‖z - p‖ + ‖r - z‖ := by
    rw [show (z - p) + (r - z) = r - p by abel, huz, hur]
    rw [← dist_eq_norm, dist_comm, hpr_eq]
    norm_num
  have hus_sum : ‖(z - p) + (s - z)‖ = ‖z - p‖ + ‖s - z‖ := by
    rw [show (z - p) + (s - z) = s - p by abel, huz, hus]
    rw [← dist_eq_norm, dist_comm, hps_eq]
    norm_num
  have hur_eq : z - p = r - z :=
    eq_of_norm_eq_of_norm_add_eq (huz.trans hur.symm) hur_sum
  have hus_eq : z - p = s - z :=
    eq_of_norm_eq_of_norm_add_eq (huz.trans hus.symm) hus_sum
  have hrs_eq : r = s := sub_left_injective (hur_eq.symm.trans hus_eq)
  rw [hrs_eq, dist_self] at hrs
  norm_num at hrs

/--
Two contact edges incident to a common point in a `2`-separated planar configuration have
disjoint open segments.
-/
@[category API, AMS 52]
theorem Erdos1084.twoSeparated_incident_contact_openSegments_disjoint
    {p q r : ℝ^2}
    (hpq : dist p q = 2)
    (hpr : dist p r = 2)
    (hqr : 2 ≤ dist q r) :
    Disjoint (openSegment ℝ p q) (openSegment ℝ p r) := by
  rw [Set.disjoint_left]
  intro z hzpq hzpr
  rw [openSegment_eq_image_lineMap] at hzpq hzpr
  rcases hzpq with ⟨a, ha, hza⟩
  rcases hzpr with ⟨b, hb, hzb⟩
  have hpz_a : dist p z = 2 * a := by
    rw [← hza, dist_left_lineMap, hpq, Real.norm_eq_abs, abs_of_pos ha.1]
    ring
  have hpz_b : dist p z = 2 * b := by
    rw [← hzb, dist_left_lineMap, hpr, Real.norm_eq_abs, abs_of_pos hb.1]
    ring
  have hab : a = b := by linarith
  subst b
  have hline : AffineMap.lineMap p q a = AffineMap.lineMap p r a := hza.trans hzb.symm
  rw [AffineMap.lineMap_apply_module', AffineMap.lineMap_apply_module'] at hline
  have hsmul : a • (q - p) = a • (r - p) := add_right_cancel hline
  have hvec : q - p = r - p := by
    have hinv := congrArg (fun x : ℝ^2 => a⁻¹ • x) hsmul
    simpa [smul_smul, ha.1.ne'] using hinv
  have hqr_eq : q = r := sub_left_injective hvec
  rw [hqr_eq, dist_self] at hqr
  norm_num at hqr

/--
A third center in a `2`-separated planar configuration does not lie in the open segment
of a contact edge.
-/
@[category API, AMS 52]
theorem Erdos1084.twoSeparated_third_point_not_mem_contact_openSegment
    {p q r : ℝ^2}
    (hpq : dist p q = 2)
    (hpr : 2 ≤ dist p r)
    (hqr : 2 ≤ dist q r) :
    r ∉ openSegment ℝ p q := by
  by_cases hqr_eq : q = r
  · subst r
    rw [dist_self] at hqr
    norm_num at hqr
  intro hr
  rw [openSegment_eq_image_lineMap] at hr
  rcases hr with ⟨a, ha, hra⟩
  have hpr_eq : dist p r = 2 * a := by
    rw [← hra, dist_left_lineMap, hpq, Real.norm_eq_abs, abs_of_pos ha.1]
    ring
  have hpr_lt : dist p r < 2 := by
    rw [hpr_eq]
    nlinarith [ha.2]
  exact (not_lt_of_ge hpr) hpr_lt

namespace Erdos1084

/--
The distance-`2` contact graph of a finite set of points in the Euclidean plane.
-/
def contactGraph (s : Finset (ℝ^2)) :
    SimpleGraph {x // x ∈ s} :=
  SimpleGraph.fromRel fun p q =>
    dist (p : ℝ^2) (q : ℝ^2) = 2

/--
A certificate that a simple graph is drawn by straight segments in the Euclidean plane,
with no nonendpoint vertex on an edge interior and no overlap between distinct edge interiors.
-/
structure StraightLinePlaneDrawing {V : Type*}
    (G : SimpleGraph V) where
  p : V ↪ ℝ^2
  vertex_not_mem_edgeInterior :
    ∀ {u v w : V}, G.Adj u v → w ≠ u → w ≠ v →
      p w ∉ openSegment ℝ (p u) (p v)
  edgeInteriors_disjoint :
    ∀ {u v x y : V}, G.Adj u v → G.Adj x y →
      s(u, v) ≠ s(x, y) →
      Disjoint
        (openSegment ℝ (p u) (p v))
        (openSegment ℝ (p x) (p y))

/--
In a straight-line plane drawing, the closed segments of two distinct edges can meet only
at points that are endpoints of both edges.
-/
@[category API, AMS 52]
theorem StraightLinePlaneDrawing.edge_segments_inter_subset_common_endpoints
    {V : Type*} {G : SimpleGraph V}
    (D : StraightLinePlaneDrawing G)
    {u v x y : V}
    (huv : G.Adj u v)
    (hxy : G.Adj x y)
    (hne : s(u, v) ≠ s(x, y)) :
    segment ℝ (D.p u) (D.p v) ∩ segment ℝ (D.p x) (D.p y) ⊆
      ({D.p u, D.p v} : Set (ℝ^2)) ∩
        ({D.p x, D.p y} : Set (ℝ^2)) := by
  intro z hz
  have vertex_mem_endpoints :
      ∀ {w a b : V}, G.Adj a b →
        D.p w ∈ segment ℝ (D.p a) (D.p b) →
        D.p w ∈ ({D.p a, D.p b} : Set (ℝ^2)) := by
    intro w a b hab hw
    rw [← insert_endpoints_openSegment] at hw
    rcases hw with hw | hw | hw
    · simp [hw]
    · simp [hw]
    · by_cases hwa : w = a
      · simp [hwa]
      · by_cases hwb : w = b
        · simp [hwb]
        · exact False.elim (D.vertex_not_mem_edgeInterior hab hwa hwb hw)
  have hzuv_parts :
      z = D.p u ∨ z = D.p v ∨ z ∈ openSegment ℝ (D.p u) (D.p v) := by
    have h := hz.1
    rw [← insert_endpoints_openSegment] at h
    exact h
  have hzxy_parts :
      z = D.p x ∨ z = D.p y ∨ z ∈ openSegment ℝ (D.p x) (D.p y) := by
    have h := hz.2
    rw [← insert_endpoints_openSegment] at h
    exact h
  rcases hzuv_parts with rfl | rfl | hzuv
  · exact ⟨by simp, vertex_mem_endpoints hxy hz.2⟩
  · exact ⟨by simp, vertex_mem_endpoints hxy hz.2⟩
  · rcases hzxy_parts with rfl | rfl | hzxy
    · exact ⟨vertex_mem_endpoints huv hz.1, by simp⟩
    · exact ⟨vertex_mem_endpoints huv hz.1, by simp⟩
    · exact False.elim <| Set.disjoint_left.mp
        (D.edgeInteriors_disjoint huv hxy hne) hzuv hzxy

/--
The inclusion of a finite `2`-separated set, together with its distance-`2` contact edges,
is a straight-line plane drawing.
-/
noncomputable def twoSeparated_contactGraph_straightLinePlaneDrawing
    (s : Finset (ℝ^2))
    (hsep : Metric.IsSeparated' 2 (s : Set (ℝ^2))) :
    StraightLinePlaneDrawing (contactGraph s) := by
  have hadjDist : ∀ {u v : {x // x ∈ s}}, (contactGraph s).Adj u v →
      dist (u : ℝ^2) (v : ℝ^2) = 2 := by
    intro u v huv
    rw [contactGraph, SimpleGraph.fromRel_adj] at huv
    rcases huv.2 with huv | huv
    · exact huv
    · exact dist_comm (v : ℝ^2) (u : ℝ^2) ▸ huv
  have hdist : ∀ {u v : {x // x ∈ s}}, u ≠ v →
      2 ≤ dist (u : ℝ^2) (v : ℝ^2) := by
    intro u v huv
    have huv_val : (u : ℝ^2) ≠ (v : ℝ^2) := by
      intro huv_val
      exact huv (Subtype.ext huv_val)
    have huv' : (2 : ENNReal) ≤ edist (u : ℝ^2) (v : ℝ^2) :=
      hsep u.property v.property huv_val
    rw [edist_dist] at huv'
    have huvReal := ENNReal.toReal_mono ENNReal.ofReal_ne_top huv'
    simpa [ENNReal.toReal_ofReal dist_nonneg] using huvReal
  refine {
    p := ⟨fun x ↦ (x : ℝ^2), Subtype.val_injective⟩
    vertex_not_mem_edgeInterior := ?_
    edgeInteriors_disjoint := ?_ }
  · intro u v w huv hwu hwv
    exact twoSeparated_third_point_not_mem_contact_openSegment
      (hadjDist huv) (hdist hwu.symm) (hdist hwv.symm)
  · intro u v x y huv hxy hne
    have huvDist := hadjDist huv
    have hxyDist := hadjDist hxy
    by_cases hux : u = x
    · subst x
      have hvy : v ≠ y := by
        intro hvy
        apply hne
        subst y
        rfl
      exact twoSeparated_incident_contact_openSegments_disjoint
        huvDist hxyDist (hdist hvy)
    by_cases huy : u = y
    · subst y
      have hvx : v ≠ x := by
        intro hvx
        apply hne
        subst x
        exact Sym2.eq_swap
      have h := twoSeparated_incident_contact_openSegments_disjoint
        huvDist (dist_comm (x : ℝ^2) (u : ℝ^2) ▸ hxyDist) (hdist hvx)
      simpa only [openSegment_symm] using h
    by_cases hvx : v = x
    · subst x
      have huy' : u ≠ y := by
        intro huy'
        apply hne
        subst y
        exact Sym2.eq_swap
      have h := twoSeparated_incident_contact_openSegments_disjoint
        (dist_comm (u : ℝ^2) (v : ℝ^2) ▸ huvDist) hxyDist (hdist huy')
      simpa only [openSegment_symm] using h
    by_cases hvy : v = y
    · subst y
      have hux' : u ≠ x := hux
      have h := twoSeparated_incident_contact_openSegments_disjoint
        (dist_comm (u : ℝ^2) (v : ℝ^2) ▸ huvDist)
        (dist_comm (x : ℝ^2) (v : ℝ^2) ▸ hxyDist) (hdist hux')
      simpa only [openSegment_symm] using h
    · exact twoSeparated_disjoint_contact_openSegments_disjoint
        huvDist hxyDist (hdist hux) (hdist huy) (hdist hvx) (hdist hvy)

end Erdos1084

/--
The signed planar orientation of the directed segment from `a` to `b` relative to `q`.
Coordinates `0` and `1` are respectively horizontal and vertical.
-/
def Erdos1084.orient2
    (a b q : EuclideanSpace ℝ (Fin 2)) : ℝ :=
  (b 0 - a 0) * (q 1 - a 1) - (b 1 - a 1) * (q 0 - a 0)

/--
The half-open horizontal ray from `q` crosses the directed segment from `a` to `b`.
The lower endpoint is included and the upper endpoint is excluded.
-/
def Erdos1084.horizontalRayCrosses
    (q a b : EuclideanSpace ℝ (Fin 2)) : Prop :=
  (a 1 ≤ q 1 ∧ q 1 < b 1 ∧ 0 < Erdos1084.orient2 a b q) ∨
  (b 1 ≤ q 1 ∧ q 1 < a 1 ∧ Erdos1084.orient2 a b q < 0)

noncomputable instance Erdos1084.instDecidableHorizontalRayCrosses
    (q a b : EuclideanSpace ℝ (Fin 2)) :
    Decidable (Erdos1084.horizontalRayCrosses q a b) := by
  unfold Erdos1084.horizontalRayCrosses
  infer_instance

/--
If the endpoint heights strictly straddle the height of `q`, the segment has a unique
parameter at that height, and it crosses the rightward horizontal ray exactly when that
intersection lies strictly to the right of `q`.
-/
@[category API, AMS 52]
theorem Erdos1084.horizontalRayCrosses_iff_lineMap_right_of_strict_straddle
    (q a b : EuclideanSpace ℝ (Fin 2))
    (hstraddle :
      (a 1 < q 1 ∧ q 1 < b 1) ∨
      (b 1 < q 1 ∧ q 1 < a 1)) :
    let t₀ : ℝ := (q 1 - a 1) / (b 1 - a 1)
    t₀ ∈ Set.Ioo (0 : ℝ) 1 ∧
      (AffineMap.lineMap a b t₀) 1 = q 1 ∧
      (∀ t : ℝ, (AffineMap.lineMap a b t) 1 = q 1 → t = t₀) ∧
      (Erdos1084.horizontalRayCrosses q a b ↔
        q 0 < (AffineMap.lineMap a b t₀) 0) := by
  dsimp only
  rcases hstraddle with hup | hdown
  · have hdpos : 0 < b 1 - a 1 := by linarith
    have hdne : b 1 - a 1 ≠ 0 := ne_of_gt hdpos
    have htpos : 0 < (q 1 - a 1) / (b 1 - a 1) :=
      div_pos (by linarith) hdpos
    have htlt : (q 1 - a 1) / (b 1 - a 1) < 1 :=
      (div_lt_one hdpos).2 (by linarith)
    refine ⟨⟨htpos, htlt⟩, ?_, ?_, ?_⟩
    · rw [AffineMap.lineMap_apply_module']
      change (q 1 - a 1) / (b 1 - a 1) * (b 1 - a 1) + a 1 = q 1
      rw [div_mul_cancel₀ _ hdne]
      ring
    · intro t ht
      rw [AffineMap.lineMap_apply_module'] at ht
      change t * (b 1 - a 1) + a 1 = q 1 at ht
      apply (eq_div_iff hdne).2
      linarith
    · rw [Erdos1084.horizontalRayCrosses]
      have hnotdown : ¬ b 1 ≤ q 1 := by linarith
      simp only [hup.1.le, hup.2, hnotdown, false_and]
      simp only [true_and, or_false]
      rw [AffineMap.lineMap_apply_module']
      change 0 < Erdos1084.orient2 a b q ↔
        q 0 < (q 1 - a 1) / (b 1 - a 1) * (b 0 - a 0) + a 0
      unfold Erdos1084.orient2
      have hid :
          (b 0 - a 0) * (q 1 - a 1) - (b 1 - a 1) * (q 0 - a 0) =
            (b 1 - a 1) *
              ((q 1 - a 1) / (b 1 - a 1) * (b 0 - a 0) + a 0 - q 0) := by
        field_simp
        ring
      rw [hid, mul_pos_iff_of_pos_left hdpos, sub_pos]
  · have hdneg : b 1 - a 1 < 0 := by linarith
    have hdne : b 1 - a 1 ≠ 0 := ne_of_lt hdneg
    have htpos : 0 < (q 1 - a 1) / (b 1 - a 1) :=
      div_pos_of_neg_of_neg (by linarith) hdneg
    have htlt : (q 1 - a 1) / (b 1 - a 1) < 1 :=
      (div_lt_one_of_neg hdneg).2 (by linarith)
    refine ⟨⟨htpos, htlt⟩, ?_, ?_, ?_⟩
    · rw [AffineMap.lineMap_apply_module']
      change (q 1 - a 1) / (b 1 - a 1) * (b 1 - a 1) + a 1 = q 1
      rw [div_mul_cancel₀ _ hdne]
      ring
    · intro t ht
      rw [AffineMap.lineMap_apply_module'] at ht
      change t * (b 1 - a 1) + a 1 = q 1 at ht
      apply (eq_div_iff hdne).2
      linarith
    · rw [Erdos1084.horizontalRayCrosses]
      have hnotup : ¬ a 1 ≤ q 1 := by linarith
      simp only [hnotup, false_and, hdown.1.le, hdown.2, true_and, false_or]
      rw [AffineMap.lineMap_apply_module']
      change Erdos1084.orient2 a b q < 0 ↔
        q 0 < (q 1 - a 1) / (b 1 - a 1) * (b 0 - a 0) + a 0
      unfold Erdos1084.orient2
      have hid :
          (b 0 - a 0) * (q 1 - a 1) - (b 1 - a 1) * (q 0 - a 0) =
            (b 1 - a 1) *
              ((q 1 - a 1) / (b 1 - a 1) * (b 0 - a 0) + a 0 - q 0) := by
        field_simp
        ring
      rw [hid]
      constructor
      · intro h
        rcases (mul_neg_iff.mp h) with hpos | hneg
        · exfalso
          linarith [hpos.1]
        · linarith [hneg.2]
      · intro hx
        exact mul_neg_iff.mpr (Or.inr ⟨hdneg, by linarith⟩)

/--
At a visible vertex on the query ray, an incident directed edge is counted exactly when
its other endpoint lies strictly above the vertex.
-/
@[category API, AMS 52]
theorem Erdos1084.horizontalRayCrosses_incident_edges_at_visible_vertex
    (q u v w : EuclideanSpace ℝ (Fin 2))
    (hy : q 1 = v 1)
    (hx : q 0 < v 0) :
    (Erdos1084.horizontalRayCrosses q u v ↔ v 1 < u 1) ∧
    (Erdos1084.horizontalRayCrosses q v w ↔ v 1 < w 1) := by
  unfold Erdos1084.horizontalRayCrosses Erdos1084.orient2
  constructor <;> simp [hy] <;> intro h <;> nlinarith

/--
At a visible vertex on the query ray, exactly one of the two incident directed edges is
counted modulo two precisely when exactly one neighboring endpoint lies strictly above
the vertex.
-/
@[category API, AMS 52]
theorem Erdos1084.horizontalRayCrosses_incident_edges_parity_one_iff
    (q u v w : EuclideanSpace ℝ (Fin 2))
    (hy : q 1 = v 1)
    (hx : q 0 < v 0) :
    ((if Erdos1084.horizontalRayCrosses q u v then 1 else 0 : ℕ) +
        (if Erdos1084.horizontalRayCrosses q v w then 1 else 0)) % 2 = 1 ↔
      (v 1 < u 1 ∧ ¬ v 1 < w 1) ∨
      (¬ v 1 < u 1 ∧ v 1 < w 1) := by
  obtain ⟨hu, hw⟩ :=
    Erdos1084.horizontalRayCrosses_incident_edges_at_visible_vertex q u v w hy hx
  simp only [hu, hw]
  by_cases huv : v 1 < u 1 <;> by_cases hvw : v 1 < w 1 <;> simp [huv, hvw]

/--
Two visible terminal edges contribute even horizontal-ray crossing parity precisely when
their nonterminal endpoints lie on the same side of the common terminal height.
-/
@[category API, AMS 52]
theorem Erdos1084.horizontalRayCrosses_two_visible_terminals_parity_even_iff
    (q u v w z : EuclideanSpace ℝ (Fin 2))
    (hyv : q 1 = v 1) (hyw : q 1 = w 1)
    (hxv : q 0 < v 0) (hxw : q 0 < w 0) :
    ((if Erdos1084.horizontalRayCrosses q u v then 1 else 0 : ℕ) +
        (if Erdos1084.horizontalRayCrosses q w z then 1 else 0)) % 2 = 0 ↔
      (v 1 < u 1 ∧ w 1 < z 1) ∨
      (¬ v 1 < u 1 ∧ ¬ w 1 < z 1) := by
  obtain ⟨hu, _⟩ :=
    Erdos1084.horizontalRayCrosses_incident_edges_at_visible_vertex q u v z hyv hxv
  obtain ⟨_, hz⟩ :=
    Erdos1084.horizontalRayCrosses_incident_edges_at_visible_vertex q u w z hyw hxw
  simp only [hu, hz]
  by_cases huv : v 1 < u 1 <;> by_cases hwz : w 1 < z 1 <;> simp [huv, hwz]

namespace Erdos1084
variable {n : ℕ}

/-- The maximal number of pairs of points which are distance 1 apart that a set of `n` 1-separated
points in `ℝ^d` make. -/
noncomputable def f (d n : ℕ) : ℕ :=
  ⨆ (s : Finset (ℝ^ d)) (_ : s.card = n) (_ : IsSeparated' 1 (s : Set (ℝ^ d))), unitDistNum s

/--
The number of contact pairs in a finite set of centers when contact distance is `2`.
-/
noncomputable def contactDistTwoNum (s : Finset (ℝ^2)) : ℕ :=
  (s.sym2.filter fun p => dist p.out.1 p.out.2 = 2).card

/--
The source theorem needed for the queued Erdős #1084 promotion: if `s` is a finite
`1`-separated set of `N ≥ 4` points in the Euclidean plane, then its number of unit-distance
pairs is at most `⌊3N - sqrt (12N - 3)⌋`.
-/
def HarborthUnitDistNumUpperGe4Source : Prop :=
  ∀ (N : ℕ), 4 ≤ N → ∀ (s : Finset (ℝ^2)),
    s.card = N →
    Metric.IsSeparated' 1 (s : Set (ℝ^2)) →
    unitDistNum s ≤ Nat.floor (3 * (N : ℝ) - Real.sqrt (12 * (N : ℝ) - 3))

/--
The external Harborth contact-number source in the disk-center convention: finite
`2`-separated center sets have at most `⌊3N - sqrt (12N - 3)⌋` pairs at distance `2`.
-/
def HarborthTwoSeparatedContactUpperGe4Source : Prop :=
  ∀ (N : ℕ), 4 ≤ N → ∀ (s : Finset (ℝ^2)),
    s.card = N →
    Metric.IsSeparated' 2 (s : Set (ℝ^2)) →
    contactDistTwoNum s ≤ Nat.floor (3 * (N : ℝ) - Real.sqrt (12 * (N : ℝ) - 3))

/--
The explicit theorem shape represented by `HarborthUnitDistNumUpperGe4Source`.
-/
@[category API, AMS 52]
theorem harborth_unitDistNum_upper_ge4_source_iff :
    HarborthUnitDistNumUpperGe4Source ↔
      ∀ (N : ℕ), 4 ≤ N → ∀ (s : Finset (ℝ^2)),
        s.card = N →
        Metric.IsSeparated' 1 (s : Set (ℝ^2)) →
        unitDistNum s ≤
          Nat.floor (3 * (N : ℝ) - Real.sqrt (12 * (N : ℝ) - 3)) := by
  rfl

/--
The explicit theorem shape represented by `HarborthTwoSeparatedContactUpperGe4Source`.
-/
@[category API, AMS 52]
theorem harborth_twoSeparated_contact_upper_ge4_source_iff :
    HarborthTwoSeparatedContactUpperGe4Source ↔
      ∀ (N : ℕ), 4 ≤ N → ∀ (s : Finset (ℝ^2)),
        s.card = N →
        Metric.IsSeparated' 2 (s : Set (ℝ^2)) →
        contactDistTwoNum s ≤
          Nat.floor (3 * (N : ℝ) - Real.sqrt (12 * (N : ℝ) - 3)) := by
  rfl

private lemma two_smul_injective : Function.Injective (fun x : ℝ^2 => (2 : ℝ) • x) := by
  intro x y hxy
  have h := congrArg (fun z : ℝ^2 => ((2 : ℝ)⁻¹) • z) hxy
  simpa [smul_smul] using h

private lemma dist_out_eq_of_eq_sym2_mk {p : Sym2 (ℝ^2)} {x y : ℝ^2} (hp : p = s(x, y)) :
    dist p.out.1 p.out.2 = dist x y := by
  have hmk : Sym2.mk p.out = Sym2.mk (x, y) := by
    exact p.out_eq.trans hp
  have hrel : Sym2.Rel (ℝ^2) p.out (x, y) := Sym2.exact hmk
  rw [Sym2.rel_iff] at hrel
  rcases hrel with ⟨h₁, h₂⟩ | ⟨h₁, h₂⟩
  · simp [h₁, h₂]
  · simp [h₁, h₂, dist_comm]

private lemma dist_out_sym2_map_two_smul (p : Sym2 (ℝ^2)) :
    dist (Sym2.map (fun x : ℝ^2 => (2 : ℝ) • x) p).out.1
        (Sym2.map (fun x : ℝ^2 => (2 : ℝ) • x) p).out.2 =
      2 * dist p.out.1 p.out.2 := by
  have hmap :
      Sym2.map (fun x : ℝ^2 => (2 : ℝ) • x) p =
        s((2 : ℝ) • p.out.1, (2 : ℝ) • p.out.2) := by
    have hmap' :
        Sym2.map (fun x : ℝ^2 => (2 : ℝ) • x) (Sym2.mk p.out) =
          s((2 : ℝ) • p.out.1, (2 : ℝ) • p.out.2) := by
      cases p.out
      rfl
    exact (congrArg (Sym2.map fun x : ℝ^2 => (2 : ℝ) • x) p.out_eq).symm.trans hmap'
  rw [dist_out_eq_of_eq_sym2_mk hmap]
  simp [dist_smul₀]

private lemma dist_out_sym2_map_two_smul_eq_two_iff (p : Sym2 (ℝ^2)) :
    dist (Sym2.map (fun x : ℝ^2 => (2 : ℝ) • x) p).out.1
        (Sym2.map (fun x : ℝ^2 => (2 : ℝ) • x) p).out.2 = 2 ↔
      dist p.out.1 p.out.2 = 1 := by
  rw [dist_out_sym2_map_two_smul]
  constructor
  · intro h
    have hnonneg : 0 ≤ dist p.out.1 p.out.2 := dist_nonneg
    nlinarith
  · intro h
    nlinarith

private lemma contactDistTwoNum_image_two_smul_eq_unitDistNum (s : Finset (ℝ^2)) :
    contactDistTwoNum (s.image fun x : ℝ^2 => (2 : ℝ) • x) = unitDistNum s := by
  classical
  unfold contactDistTwoNum unitDistNum
  rw [Finset.sym2_image]
  rw [Finset.filter_image]
  rw [Finset.card_image_of_injective _ (Sym2.map.injective two_smul_injective)]
  exact congrArg Finset.card (Finset.filter_congr fun p _ =>
    dist_out_sym2_map_two_smul_eq_two_iff p)

private lemma two_smul_image_isSeparated_two {s : Finset (ℝ^2)}
    (hsep : Metric.IsSeparated' 1 (s : Set (ℝ^2))) :
    Metric.IsSeparated' 2 ((s.image fun x : ℝ^2 => (2 : ℝ) • x) : Set (ℝ^2)) := by
  classical
  rw [Metric.IsSeparated'] at hsep ⊢
  intro x hx y hy hxy
  rw [Finset.mem_coe, Finset.mem_image] at hx hy
  rcases hx with ⟨x₀, hx₀, rfl⟩
  rcases hy with ⟨y₀, hy₀, rfl⟩
  have hxy₀ : x₀ ≠ y₀ := by
    intro h
    apply hxy
    simp [h]
  have hsep₀ := hsep (by simpa using hx₀) (by simpa using hy₀) hxy₀
  have hdist₀ : (1 : ℝ) ≤ dist x₀ y₀ := by
    have hsep₀' : (1 : ENNReal) ≤ edist x₀ y₀ := by
      simpa using hsep₀
    rw [edist_dist, ← ENNReal.ofReal_one] at hsep₀'
    exact (ENNReal.ofReal_le_ofReal_iff dist_nonneg).1 hsep₀'
  rw [edist_dist, dist_smul₀]
  have hreal : (2 : ℝ) ≤ ‖(2 : ℝ)‖ * dist x₀ y₀ := by
    norm_num
    nlinarith
  simpa using (ENNReal.ofReal_le_ofReal hreal)

/--
Local wrapper from the Harborth contact-number source theorem in the `2`-separated
disk-center convention to the repository's `unitDistNum` convention.
-/
@[category API, AMS 52]
theorem harborth_unitDistNum_upper_ge4_of_twoSeparated_contact_source
    (hHarborth : HarborthTwoSeparatedContactUpperGe4Source) :
    HarborthUnitDistNumUpperGe4Source := by
  intro N hN s hcard hsep
  have hcard_image :
      (s.image fun x : ℝ^2 => (2 : ℝ) • x).card = N := by
    rw [Finset.card_image_of_injective _ two_smul_injective, hcard]
  have hcontact :=
    hHarborth N hN (s.image fun x : ℝ^2 => (2 : ℝ) • x) hcard_image
      (two_smul_image_isSeparated_two hsep)
  rwa [contactDistTwoNum_image_two_smul_eq_unitDistNum] at hcontact

/--
A one-point finite Euclidean configuration has no unordered unit-distance pair.
-/
@[category API, AMS 52]
theorem unitDistNum_eq_zero_of_card_one {d : ℕ}
    (s : Finset (ℝ^d)) (hcard : s.card = 1) :
    unitDistNum s = 0 := by
  classical
  rw [Finset.card_eq_one] at hcard
  rcases hcard with ⟨x, rfl⟩
  have hdiag :
      dist (Sym2.diag x).out.1 (Sym2.diag x).out.2 = 0 := by
    have hmk : Sym2.mk (Sym2.diag x).out = Sym2.mk (x, x) := by
      simp [Sym2.diag]
    have hrel : Sym2.Rel (ℝ^d) (Sym2.diag x).out (x, x) := Sym2.exact hmk
    rw [Sym2.rel_iff] at hrel
    rcases hrel with ⟨h₁, h₂⟩ | ⟨h₁, h₂⟩ <;> simp [h₁, h₂]
  simp [unitDistNum, hdiag]

/--
A one-point planar configuration has no unordered unit-distance pair.
-/
@[category API, AMS 52]
theorem f_two_one_eq_zero : f 2 1 = 0 := by
  classical
  refine le_antisymm ?_ (Nat.zero_le _)
  unfold f
  refine ciSup_le' ?_
  intro s
  refine ciSup_le' ?_
  intro hcard
  refine ciSup_le' ?_
  intro _hsep
  exact le_of_eq (unitDistNum_eq_zero_of_card_one s hcard)

private lemma triangular_harborth_floor (n : ℕ) :
    Nat.floor
      (3 * ((3 * n ^ 2 + 3 * n + 1 : ℕ) : ℝ) -
        Real.sqrt (12 * ((3 * n ^ 2 + 3 * n + 1 : ℕ) : ℝ) - 3)) =
        9 * n ^ 2 + 3 * n := by
  have hrad :
      12 * ((3 * n ^ 2 + 3 * n + 1 : ℕ) : ℝ) - 3 =
        (((6 * n + 3 : ℕ) : ℝ)) ^ 2 := by
    norm_num [Nat.cast_add, Nat.cast_mul, Nat.cast_pow]
    ring
  have hmain :
      3 * ((3 * n ^ 2 + 3 * n + 1 : ℕ) : ℝ) -
          Real.sqrt (12 * ((3 * n ^ 2 + 3 * n + 1 : ℕ) : ℝ) - 3) =
        ((9 * n ^ 2 + 3 * n : ℕ) : ℝ) := by
    rw [hrad, Real.sqrt_sq_eq_abs, abs_of_nonneg]
    · norm_num [Nat.cast_add, Nat.cast_mul, Nat.cast_pow]
      ring
    · positivity
  rw [hmain, Nat.floor_natCast]

private noncomputable def triangularPoint (i j : ℤ) : ℝ^2 :=
  !₂[(i : ℝ) + (j : ℝ) / 2, (Real.sqrt 3 / 2) * (j : ℝ)]

private lemma triangularPoint_injective :
    Function.Injective (fun p : ℤ × ℤ => triangularPoint p.1 p.2) := by
  rintro ⟨i, j⟩ ⟨i', j'⟩ h
  have h₀ := congrArg (fun x : ℝ^2 => x 0) h
  have h₁ := congrArg (fun x : ℝ^2 => x 1) h
  simp only [triangularPoint, PiLp.toLp_apply, Matrix.cons_val_zero, Matrix.cons_val_one,
    Fin.isValue] at h₀ h₁
  have hsqrt_ne : Real.sqrt 3 / 2 ≠ (0 : ℝ) := by positivity
  have hj_real : (j : ℝ) = j' := by
    exact mul_left_cancel₀ hsqrt_ne h₁
  have hj : j = j' := by exact_mod_cast hj_real
  subst hj
  have hi_real : (i : ℝ) = i' := by nlinarith
  have hi : i = i' := by exact_mod_cast hi_real
  subst hi
  rfl

private lemma triangularPoint_dist_east (i j : ℤ) :
    dist (triangularPoint i j) (triangularPoint (i + 1) j) = 1 := by
  rw [EuclideanSpace.dist_eq, Fin.sum_univ_two]
  simp [triangularPoint]

private lemma triangularPoint_dist_north (i j : ℤ) :
    dist (triangularPoint i j) (triangularPoint i (j + 1)) = 1 := by
  rw [EuclideanSpace.dist_eq, Fin.sum_univ_two]
  simp [triangularPoint, Real.dist_eq]
  have hsqrt_sq : (Real.sqrt 3) ^ 2 = (3 : ℝ) := Real.sq_sqrt (by norm_num)
  ring_nf
  nlinarith

private lemma triangularPoint_dist_southeast (i j : ℤ) :
    dist (triangularPoint i j) (triangularPoint (i + 1) (j - 1)) = 1 := by
  rw [EuclideanSpace.dist_eq, Fin.sum_univ_two]
  simp [triangularPoint, Real.dist_eq]
  have hsqrt_sq : (Real.sqrt 3) ^ 2 = (3 : ℝ) := Real.sq_sqrt (by norm_num)
  ring_nf
  nlinarith

private lemma int_quadratic_ge_one (a b : ℤ) (h : a ≠ 0 ∨ b ≠ 0) :
    (1 : ℤ) ≤ a ^ 2 + a * b + b ^ 2 := by
  have hid : (2 * (a ^ 2 + a * b + b ^ 2) : ℤ) = a ^ 2 + (a + b) ^ 2 + b ^ 2 := by
    ring
  by_cases hb : b = 0
  · subst hb
    rcases h with ha | hbzero
    · ring_nf
      have hpos : (0 : ℤ) < a ^ 2 := sq_pos_of_ne_zero ha
      omega
    · contradiction
  · by_cases hab : a + b = 0
    · have hbpos : (0 : ℤ) < b ^ 2 := sq_pos_of_ne_zero hb
      nlinarith
    · have habpos : (0 : ℤ) < (a + b) ^ 2 := sq_pos_of_ne_zero hab
      have hsq_a : (0 : ℤ) ≤ a ^ 2 := sq_nonneg a
      have hsq_b : (0 : ℤ) ≤ b ^ 2 := sq_nonneg b
      nlinarith

private lemma triangularPoint_dist_sq (i j i' j' : ℤ) :
    dist (triangularPoint i j) (triangularPoint i' j') ^ 2 =
      (((i - i') ^ 2 + (i - i') * (j - j') + (j - j') ^ 2 : ℤ) : ℝ) := by
  rw [EuclideanSpace.dist_sq_eq, Fin.sum_univ_two]
  simp [triangularPoint, Real.dist_eq, sq_abs]
  have hsqrt_sq : (Real.sqrt 3) ^ 2 = (3 : ℝ) := Real.sq_sqrt (by norm_num)
  ring_nf
  rw [hsqrt_sq]
  ring

private lemma triangularPoint_edist_ge_one_of_ne {i j i' j' : ℤ}
    (h : (i, j) ≠ (i', j')) :
    (1 : ENNReal) ≤ edist (triangularPoint i j) (triangularPoint i' j') := by
  have hdiff : i - i' ≠ 0 ∨ j - j' ≠ 0 := by
    by_contra hzero
    push_neg at hzero
    apply h
    ext <;> omega
  have hquad := int_quadratic_ge_one (i - i') (j - j') hdiff
  have hquad_real :
      (1 : ℝ) ≤
        (((i - i') ^ 2 + (i - i') * (j - j') + (j - j') ^ 2 : ℤ) : ℝ) := by
    exact_mod_cast hquad
  have hsq := triangularPoint_dist_sq i j i' j'
  have hdist_nonneg : 0 ≤ dist (triangularPoint i j) (triangularPoint i' j') := dist_nonneg
  rw [edist_dist, ← ENNReal.ofReal_one]
  apply ENNReal.ofReal_le_ofReal
  nlinarith

/--
The axial-coordinate hexagonal ball
`{(i,j) : |i| ≤ n, |j| ≤ n, |i+j| ≤ n}` as a finite set of integer pairs.
-/
private def triangularHexCoords (n : ℕ) : Finset (ℤ × ℤ) :=
  ((Finset.Icc (-(n : ℤ)) (n : ℤ)).product (Finset.Icc (-(n : ℤ)) (n : ℤ))).filter
    fun p => -(n : ℤ) ≤ p.1 + p.2 ∧ p.1 + p.2 ≤ (n : ℤ)

private lemma mem_triangularHexCoords {n : ℕ} {p : ℤ × ℤ} :
    p ∈ triangularHexCoords n ↔
      -(n : ℤ) ≤ p.1 ∧ p.1 ≤ (n : ℤ) ∧
      -(n : ℤ) ≤ p.2 ∧ p.2 ≤ (n : ℤ) ∧
      -(n : ℤ) ≤ p.1 + p.2 ∧ p.1 + p.2 ≤ (n : ℤ) := by
  simp [triangularHexCoords, and_assoc]

/-- The embedded triangular-lattice hexagonal patch. -/
private noncomputable def triangularHexPatch (n : ℕ) : Finset (ℝ^2) :=
  (triangularHexCoords n).image fun p : ℤ × ℤ => triangularPoint p.1 p.2

private lemma triangularHexPatch_card_eq_coords_card (n : ℕ) :
    (triangularHexPatch n).card = (triangularHexCoords n).card := by
  classical
  unfold triangularHexPatch
  rw [Finset.card_image_of_injective _ triangularPoint_injective]

private lemma triangularHexPatch_oneSeparated (n : ℕ) :
    Metric.IsSeparated' 1 ((triangularHexPatch n : Finset (ℝ^2)) : Set (ℝ^2)) := by
  classical
  rw [Metric.IsSeparated']
  intro x hx y hy hxy
  rw [Finset.mem_coe, triangularHexPatch, Finset.mem_image] at hx hy
  rcases hx with ⟨p, _hp, rfl⟩
  rcases hy with ⟨q, _hq, rfl⟩
  have hpq : p ≠ q := by
    intro hpq
    apply hxy
    rw [hpq]
  exact triangularPoint_edist_ge_one_of_ne hpq

private abbrev triangularHexPointIndex (n : ℕ) :=
  (Sigma fun k : Fin (n + 1) => Fin (n + k.1 + 1)) ⊕
    (Sigma fun k : Fin n => Fin (n + k.1 + 1))

private def triangularHexPointCoord (n : ℕ) : triangularHexPointIndex n → ℤ × ℤ
  | Sum.inl p => ((-(p.1.1 : ℤ) + (p.2.1 : ℤ)), (-(n : ℤ) + (p.1.1 : ℤ)))
  | Sum.inr p => ((-(n : ℤ) + (p.2.1 : ℤ)), ((n : ℤ) - (p.1.1 : ℤ)))

private lemma triangularHexPointIndex_card_aux (n : ℕ) :
    (∑ k : Fin (n + 1), (n + k.1 + 1)) + (∑ k : Fin n, (n + k.1 + 1)) =
      3 * n ^ 2 + 3 * n + 1 := by
  induction n with
  | zero => simp
  | succ n ih =>
      rw [Fin.sum_univ_castSucc (fun k : Fin (n + 1 + 1) => n + 1 + k.1 + 1)]
      rw [Fin.sum_univ_castSucc (fun k : Fin (n + 1) => n + 1 + k.1 + 1)]
      simp only [Fin.val_castSucc, Fin.val_last]
      have hfirst : (∑ i : Fin (n + 1), (n + 1 + i.1 + 1)) =
          (∑ i : Fin (n + 1), (n + i.1 + 1)) + (n + 1) := by
        simp_rw [show ∀ i : Fin (n + 1),
            n + 1 + i.1 + 1 = (n + i.1 + 1) + 1 by
          intro i
          omega]
        change (Finset.univ.sum fun i : Fin (n + 1) => (n + i.1 + 1) + 1) =
          (Finset.univ.sum fun i : Fin (n + 1) => n + i.1 + 1) + (n + 1)
        rw [Finset.sum_add_distrib]
        simp
      have hsecond : (∑ i : Fin n, (n + 1 + i.1 + 1)) =
          (∑ i : Fin n, (n + i.1 + 1)) + n := by
        simp_rw [show ∀ i : Fin n, n + 1 + i.1 + 1 = (n + i.1 + 1) + 1 by
          intro i
          omega]
        change (Finset.univ.sum fun i : Fin n => (n + i.1 + 1) + 1) =
          (Finset.univ.sum fun i : Fin n => n + i.1 + 1) + n
        rw [Finset.sum_add_distrib]
        simp
      rw [hfirst, hsecond]
      nlinarith [ih]

private lemma triangularHexPointCoord_injective (n : ℕ) :
    Function.Injective (triangularHexPointCoord n) := by
  intro a b h
  cases a with
  | inl a =>
      rcases a with ⟨ak, av⟩
      cases b with
      | inl b =>
          rcases b with ⟨bk, bv⟩
          simp [triangularHexPointCoord] at h
          have hk : ak = bk := by
            ext
            omega
          subst hk
          have hv : av = bv := by
            ext
            omega
          subst hv
          rfl
      | inr b =>
          rcases b with ⟨bk, _bv⟩
          simp [triangularHexPointCoord] at h
          have hb_lt : (bk.1 : ℤ) < n := by exact_mod_cast bk.2
          have ha_le : (ak.1 : ℤ) ≤ n := by exact_mod_cast Nat.le_of_lt_succ ak.2
          omega
  | inr a =>
      rcases a with ⟨ak, av⟩
      cases b with
      | inl b =>
          rcases b with ⟨bk, _bv⟩
          simp [triangularHexPointCoord] at h
          have ha_lt : (ak.1 : ℤ) < n := by exact_mod_cast ak.2
          have hb_le : (bk.1 : ℤ) ≤ n := by exact_mod_cast Nat.le_of_lt_succ bk.2
          omega
      | inr b =>
          rcases b with ⟨bk, bv⟩
          simp [triangularHexPointCoord] at h
          have hk : ak = bk := by
            ext
            omega
          subst hk
          have hv : av = bv := by
            ext
            omega
          subst hv
          rfl

private lemma triangularHexPointCoord_mem (n : ℕ) (p : triangularHexPointIndex n) :
    triangularHexPointCoord n p ∈ triangularHexCoords n := by
  cases p with
  | inl p =>
      rcases p with ⟨k, v⟩
      rw [mem_triangularHexCoords]
      simp [triangularHexPointCoord]
      omega
  | inr p =>
      rcases p with ⟨k, v⟩
      rw [mem_triangularHexCoords]
      simp [triangularHexPointCoord]
      have hk : (k.1 : ℤ) < n := by exact_mod_cast k.2
      omega

private lemma triangularHexPointCoord_surjective (n : ℕ) :
    ∀ q ∈ triangularHexCoords n, ∃ p : triangularHexPointIndex n,
      triangularHexPointCoord n p = q := by
  rintro ⟨i, j⟩ hq
  rw [mem_triangularHexCoords] at hq
  rcases hq with ⟨hi_low, hi_high, hj_low, hj_high, hij_low, hij_high⟩
  by_cases hj_nonpos : j ≤ 0
  · let kNat : ℕ := Int.toNat (j + (n : ℤ))
    have hk_cast : (kNat : ℤ) = j + (n : ℤ) := by
      exact Int.toNat_of_nonneg (by omega)
    have hk_lt : kNat < n + 1 := by
      omega
    let vNat : ℕ := Int.toNat (i + (kNat : ℤ))
    have hv_cast : (vNat : ℤ) = i + (kNat : ℤ) := by
      exact Int.toNat_of_nonneg (by omega)
    have hv_lt : vNat < n + kNat + 1 := by
      omega
    refine ⟨Sum.inl ⟨⟨kNat, hk_lt⟩, ⟨vNat, hv_lt⟩⟩, ?_⟩
    simp [triangularHexPointCoord, kNat, vNat, hk_cast]
    omega
  · have hj_pos : 0 < j := by omega
    let kNat : ℕ := Int.toNat ((n : ℤ) - j)
    have hk_cast : (kNat : ℤ) = (n : ℤ) - j := by
      exact Int.toNat_of_nonneg (by omega)
    have hk_lt : kNat < n := by
      omega
    let vNat : ℕ := Int.toNat (i + (n : ℤ))
    have hv_cast : (vNat : ℤ) = i + (n : ℤ) := by
      exact Int.toNat_of_nonneg (by omega)
    have hv_lt : vNat < n + kNat + 1 := by
      omega
    refine ⟨Sum.inr ⟨⟨kNat, hk_lt⟩, ⟨vNat, hv_lt⟩⟩, ?_⟩
    simp [triangularHexPointCoord, kNat, vNat, hk_cast, hv_cast]

private lemma triangularHexPointCoord_image_univ (n : ℕ) :
    Finset.univ.image (triangularHexPointCoord n) = triangularHexCoords n := by
  classical
  ext q
  constructor
  · intro hq
    rw [Finset.mem_image] at hq
    rcases hq with ⟨p, _hp, rfl⟩
    exact triangularHexPointCoord_mem n p
  · intro hq
    rcases triangularHexPointCoord_surjective n q hq with ⟨p, rfl⟩
    exact Finset.mem_image.mpr ⟨p, Finset.mem_univ p, rfl⟩

private lemma triangularHexCoords_card (n : ℕ) :
    (triangularHexCoords n).card = 3 * n ^ 2 + 3 * n + 1 := by
  classical
  rw [← triangularHexPointCoord_image_univ n]
  rw [Finset.card_image_of_injective]
  · simp [triangularHexPointIndex, Fintype.card_sum, Fintype.card_sigma,
      triangularHexPointIndex_card_aux]
  · exact triangularHexPointCoord_injective n

private lemma triangularHexPatch_card (n : ℕ) :
    (triangularHexPatch n).card = 3 * n ^ 2 + 3 * n + 1 := by
  rw [triangularHexPatch_card_eq_coords_card, triangularHexCoords_card]

private noncomputable def triangularHexPatchRows (n : ℕ) : Finset (ℝ^2) :=
  Finset.univ.image fun p : triangularHexPointIndex n =>
    triangularPoint (triangularHexPointCoord n p).1 (triangularHexPointCoord n p).2

private lemma triangularHexPatchRows_card (n : ℕ) :
    (triangularHexPatchRows n).card = 3 * n ^ 2 + 3 * n + 1 := by
  classical
  unfold triangularHexPatchRows
  rw [Finset.card_image_of_injective]
  · simp [triangularHexPointIndex, Fintype.card_sum, Fintype.card_sigma,
      triangularHexPointIndex_card_aux]
  · intro a b h
    apply triangularHexPointCoord_injective n
    exact triangularPoint_injective h

private lemma triangularHexPatchRows_oneSeparated (n : ℕ) :
    Metric.IsSeparated' 1 ((triangularHexPatchRows n : Finset (ℝ^2)) : Set (ℝ^2)) := by
  classical
  rw [Metric.IsSeparated']
  intro x hx y hy hxy
  rw [Finset.mem_coe, triangularHexPatchRows, Finset.mem_image] at hx hy
  rcases hx with ⟨p, _hp, rfl⟩
  rcases hy with ⟨q, _hq, rfl⟩
  refine triangularPoint_edist_ge_one_of_ne ?_
  intro hpq
  apply hxy
  have hcoord : triangularHexPointCoord n p = triangularHexPointCoord n q := by
    simpa using hpq
  rw [hcoord]

private abbrev triangularHexEastEdgeIndex (n : ℕ) :=
  (Sigma fun k : Fin (n + 1) => Fin (n + k.1)) ⊕
    (Sigma fun k : Fin n => Fin (n + k.1))

private def triangularHexEastSourceCoord (n : ℕ) : triangularHexEastEdgeIndex n → ℤ × ℤ
  | Sum.inl p => ((-(p.1.1 : ℤ) + (p.2.1 : ℤ)), (-(n : ℤ) + (p.1.1 : ℤ)))
  | Sum.inr p => ((-(n : ℤ) + (p.2.1 : ℤ)), ((n : ℤ) - (p.1.1 : ℤ)))

private def triangularHexEastSourcePointIndex (n : ℕ) :
    triangularHexEastEdgeIndex n → triangularHexPointIndex n
  | Sum.inl p =>
      Sum.inl ⟨p.1, ⟨p.2.1, by omega⟩⟩
  | Sum.inr p =>
      Sum.inr ⟨p.1, ⟨p.2.1, by omega⟩⟩

private def triangularHexEastTargetPointIndex (n : ℕ) :
    triangularHexEastEdgeIndex n → triangularHexPointIndex n
  | Sum.inl p =>
      Sum.inl ⟨p.1, ⟨p.2.1 + 1, by omega⟩⟩
  | Sum.inr p =>
      Sum.inr ⟨p.1, ⟨p.2.1 + 1, by omega⟩⟩

private lemma triangularHexEastSourcePointIndex_coord (n : ℕ)
    (p : triangularHexEastEdgeIndex n) :
    triangularHexPointCoord n (triangularHexEastSourcePointIndex n p) =
      triangularHexEastSourceCoord n p := by
  cases p <;> rfl

private lemma triangularHexEastTargetPointIndex_coord (n : ℕ)
    (p : triangularHexEastEdgeIndex n) :
    triangularHexPointCoord n (triangularHexEastTargetPointIndex n p) =
      ((triangularHexEastSourceCoord n p).1 + 1, (triangularHexEastSourceCoord n p).2) := by
  cases p <;> simp [triangularHexEastTargetPointIndex, triangularHexEastSourceCoord,
    triangularHexPointCoord] <;> ring

private lemma triangularHexEastEdgeIndex_card_aux (n : ℕ) :
    (∑ k : Fin (n + 1), (n + k.1)) + (∑ k : Fin n, (n + k.1)) =
      3 * n ^ 2 + n := by
  induction n with
  | zero => simp
  | succ n ih =>
      rw [Fin.sum_univ_castSucc (fun k : Fin (n + 1 + 1) => n + 1 + k.1)]
      rw [Fin.sum_univ_castSucc (fun k : Fin (n + 1) => n + 1 + k.1)]
      simp only [Fin.val_castSucc, Fin.val_last]
      have hfirst : (∑ i : Fin (n + 1), (n + 1 + i.1)) =
          (∑ i : Fin (n + 1), (n + i.1)) + (n + 1) := by
        simp_rw [show ∀ i : Fin (n + 1), n + 1 + i.1 = (n + i.1) + 1 by
          intro i
          omega]
        change (Finset.univ.sum fun i : Fin (n + 1) => (n + i.1) + 1) =
          (Finset.univ.sum fun i : Fin (n + 1) => n + i.1) + (n + 1)
        rw [Finset.sum_add_distrib]
        simp
      have hsecond : (∑ i : Fin n, (n + 1 + i.1)) =
          (∑ i : Fin n, (n + i.1)) + n := by
        simp_rw [show ∀ i : Fin n, n + 1 + i.1 = (n + i.1) + 1 by
          intro i
          omega]
        change (Finset.univ.sum fun i : Fin n => (n + i.1) + 1) =
          (Finset.univ.sum fun i : Fin n => n + i.1) + n
        rw [Finset.sum_add_distrib]
        simp
      rw [hfirst, hsecond]
      nlinarith [ih]

private lemma triangularHexEastSourceCoord_injective (n : ℕ) :
    Function.Injective (triangularHexEastSourceCoord n) := by
  intro a b h
  cases a with
  | inl a =>
      rcases a with ⟨ak, av⟩
      cases b with
      | inl b =>
          rcases b with ⟨bk, bv⟩
          simp [triangularHexEastSourceCoord] at h
          have hk : ak = bk := by
            ext
            omega
          subst hk
          have hv : av = bv := by
            ext
            omega
          subst hv
          rfl
      | inr b =>
          rcases b with ⟨bk, _bv⟩
          simp [triangularHexEastSourceCoord] at h
          have hb_lt : (bk.1 : ℤ) < n := by exact_mod_cast bk.2
          have ha_le : (ak.1 : ℤ) ≤ n := by exact_mod_cast Nat.le_of_lt_succ ak.2
          omega
  | inr a =>
      rcases a with ⟨ak, av⟩
      cases b with
      | inl b =>
          rcases b with ⟨bk, _bv⟩
          simp [triangularHexEastSourceCoord] at h
          have ha_lt : (ak.1 : ℤ) < n := by exact_mod_cast ak.2
          have hb_le : (bk.1 : ℤ) ≤ n := by exact_mod_cast Nat.le_of_lt_succ bk.2
          omega
      | inr b =>
          rcases b with ⟨bk, bv⟩
          simp [triangularHexEastSourceCoord] at h
          have hk : ak = bk := by
            ext
            omega
          subst hk
          have hv : av = bv := by
            ext
            omega
          subst hv
          rfl

private noncomputable def triangularHexPatchRowsEastUnitPairs (n : ℕ) : Finset (Sym2 (ℝ^2)) :=
  Finset.univ.image fun p : triangularHexEastEdgeIndex n =>
    s(triangularPoint (triangularHexEastSourceCoord n p).1 (triangularHexEastSourceCoord n p).2,
      triangularPoint ((triangularHexEastSourceCoord n p).1 + 1)
        (triangularHexEastSourceCoord n p).2)

private lemma triangularHexPatchRowsEastUnitPairs_card (n : ℕ) :
    (triangularHexPatchRowsEastUnitPairs n).card = 3 * n ^ 2 + n := by
  classical
  unfold triangularHexPatchRowsEastUnitPairs
  rw [Finset.card_image_of_injective]
  · simp [triangularHexEastEdgeIndex, Fintype.card_sum, Fintype.card_sigma,
      triangularHexEastEdgeIndex_card_aux]
  · intro a b h
    have hrel :
        Sym2.Rel (ℝ^2)
          (triangularPoint (triangularHexEastSourceCoord n a).1
              (triangularHexEastSourceCoord n a).2,
            triangularPoint ((triangularHexEastSourceCoord n a).1 + 1)
              (triangularHexEastSourceCoord n a).2)
          (triangularPoint (triangularHexEastSourceCoord n b).1
              (triangularHexEastSourceCoord n b).2,
            triangularPoint ((triangularHexEastSourceCoord n b).1 + 1)
              (triangularHexEastSourceCoord n b).2) :=
      Sym2.exact h
    rw [Sym2.rel_iff] at hrel
    rcases hrel with ⟨h₁, _h₂⟩ | ⟨h₁, h₂⟩
    · apply triangularHexEastSourceCoord_injective n
      exact triangularPoint_injective h₁
    · have hs :
          triangularHexEastSourceCoord n a =
            ((triangularHexEastSourceCoord n b).1 + 1,
              (triangularHexEastSourceCoord n b).2) :=
        triangularPoint_injective h₁
      have ht :
          ((triangularHexEastSourceCoord n a).1 + 1,
              (triangularHexEastSourceCoord n a).2) =
            triangularHexEastSourceCoord n b :=
        triangularPoint_injective h₂
      have hs₁ :
          (triangularHexEastSourceCoord n a).1 =
            (triangularHexEastSourceCoord n b).1 + 1 := congrArg Prod.fst hs
      have ht₁ :
          (triangularHexEastSourceCoord n a).1 + 1 =
            (triangularHexEastSourceCoord n b).1 := congrArg Prod.fst ht
      omega

private lemma triangularHexPatchRowsEastUnitPairs_subset_unitDist (n : ℕ) :
    triangularHexPatchRowsEastUnitPairs n ⊆
      (triangularHexPatchRows n).sym2.filter (fun q => dist q.out.1 q.out.2 = 1) := by
  classical
  intro q hq
  rw [triangularHexPatchRowsEastUnitPairs, Finset.mem_image] at hq
  rcases hq with ⟨p, _hp, rfl⟩
  have h₁ :
      triangularPoint (triangularHexEastSourceCoord n p).1 (triangularHexEastSourceCoord n p).2 ∈
        triangularHexPatchRows n := by
    unfold triangularHexPatchRows
    refine Finset.mem_image.mpr ⟨triangularHexEastSourcePointIndex n p, Finset.mem_univ _, ?_⟩
    rw [triangularHexEastSourcePointIndex_coord]
  have h₂ :
      triangularPoint ((triangularHexEastSourceCoord n p).1 + 1)
          (triangularHexEastSourceCoord n p).2 ∈ triangularHexPatchRows n := by
    unfold triangularHexPatchRows
    refine Finset.mem_image.mpr ⟨triangularHexEastTargetPointIndex n p, Finset.mem_univ _, ?_⟩
    rw [triangularHexEastTargetPointIndex_coord]
  simp [h₁, h₂, dist_out_eq_of_eq_sym2_mk rfl, triangularPoint_dist_east]

private lemma triangularHexPatch_east_pair_mem_unitDist {n : ℕ} {p : ℤ × ℤ}
    (hp : p ∈ triangularHexCoords n)
    (hp' : (p.1 + 1, p.2) ∈ triangularHexCoords n) :
    s(triangularPoint p.1 p.2, triangularPoint (p.1 + 1) p.2) ∈
      (triangularHexPatch n).sym2.filter
        (fun q => dist q.out.1 q.out.2 = 1) := by
  classical
  have h₁ : triangularPoint p.1 p.2 ∈ triangularHexPatch n := by
    unfold triangularHexPatch
    exact Finset.mem_image.mpr ⟨p, hp, rfl⟩
  have h₂ : triangularPoint (p.1 + 1) p.2 ∈ triangularHexPatch n := by
    unfold triangularHexPatch
    exact Finset.mem_image.mpr ⟨(p.1 + 1, p.2), hp', rfl⟩
  simp [h₁, h₂, dist_out_eq_of_eq_sym2_mk rfl, triangularPoint_dist_east]

private lemma triangularHexEastUnitPair_injective :
    Function.Injective
      (fun p : ℤ × ℤ =>
        s(triangularPoint p.1 p.2, triangularPoint (p.1 + 1) p.2)) := by
  intro p q hpq
  have hrel :
      Sym2.Rel (ℝ^2)
        (triangularPoint p.1 p.2, triangularPoint (p.1 + 1) p.2)
        (triangularPoint q.1 q.2, triangularPoint (q.1 + 1) q.2) :=
    Sym2.exact hpq
  rw [Sym2.rel_iff] at hrel
  rcases hrel with ⟨h₁, _h₂⟩ | ⟨h₁, h₂⟩
  · exact triangularPoint_injective h₁
  · have hp : p = (q.1 + 1, q.2) := triangularPoint_injective h₁
    have hq : (p.1 + 1, p.2) = q := triangularPoint_injective h₂
    have hp₁ : p.1 = q.1 + 1 := congrArg Prod.fst hp
    have hq₁ : p.1 + 1 = q.1 := congrArg Prod.fst hq
    omega

private lemma triangularHexPatch_north_pair_mem_unitDist {n : ℕ} {p : ℤ × ℤ}
    (hp : p ∈ triangularHexCoords n)
    (hp' : (p.1, p.2 + 1) ∈ triangularHexCoords n) :
    s(triangularPoint p.1 p.2, triangularPoint p.1 (p.2 + 1)) ∈
      (triangularHexPatch n).sym2.filter
        (fun q => dist q.out.1 q.out.2 = 1) := by
  classical
  have h₁ : triangularPoint p.1 p.2 ∈ triangularHexPatch n := by
    unfold triangularHexPatch
    exact Finset.mem_image.mpr ⟨p, hp, rfl⟩
  have h₂ : triangularPoint p.1 (p.2 + 1) ∈ triangularHexPatch n := by
    unfold triangularHexPatch
    exact Finset.mem_image.mpr ⟨(p.1, p.2 + 1), hp', rfl⟩
  simp [h₁, h₂, dist_out_eq_of_eq_sym2_mk rfl, triangularPoint_dist_north]

private lemma triangularHexNorthUnitPair_injective :
    Function.Injective
      (fun p : ℤ × ℤ =>
        s(triangularPoint p.1 p.2, triangularPoint p.1 (p.2 + 1))) := by
  intro p q hpq
  have hrel :
      Sym2.Rel (ℝ^2)
        (triangularPoint p.1 p.2, triangularPoint p.1 (p.2 + 1))
        (triangularPoint q.1 q.2, triangularPoint q.1 (q.2 + 1)) :=
    Sym2.exact hpq
  rw [Sym2.rel_iff] at hrel
  rcases hrel with ⟨h₁, _h₂⟩ | ⟨h₁, h₂⟩
  · exact triangularPoint_injective h₁
  · have hp : p = (q.1, q.2 + 1) := triangularPoint_injective h₁
    have hq : (p.1, p.2 + 1) = q := triangularPoint_injective h₂
    have hp₂ : p.2 = q.2 + 1 := congrArg Prod.snd hp
    have hq₂ : p.2 + 1 = q.2 := congrArg Prod.snd hq
    omega

private lemma triangularHexPatch_southeast_pair_mem_unitDist {n : ℕ} {p : ℤ × ℤ}
    (hp : p ∈ triangularHexCoords n)
    (hp' : (p.1 + 1, p.2 - 1) ∈ triangularHexCoords n) :
    s(triangularPoint p.1 p.2, triangularPoint (p.1 + 1) (p.2 - 1)) ∈
      (triangularHexPatch n).sym2.filter
        (fun q => dist q.out.1 q.out.2 = 1) := by
  classical
  have h₁ : triangularPoint p.1 p.2 ∈ triangularHexPatch n := by
    unfold triangularHexPatch
    exact Finset.mem_image.mpr ⟨p, hp, rfl⟩
  have h₂ : triangularPoint (p.1 + 1) (p.2 - 1) ∈ triangularHexPatch n := by
    unfold triangularHexPatch
    exact Finset.mem_image.mpr ⟨(p.1 + 1, p.2 - 1), hp', rfl⟩
  simp [h₁, h₂, dist_out_eq_of_eq_sym2_mk rfl, triangularPoint_dist_southeast]

private lemma triangularHexSoutheastUnitPair_injective :
    Function.Injective
      (fun p : ℤ × ℤ =>
        s(triangularPoint p.1 p.2, triangularPoint (p.1 + 1) (p.2 - 1))) := by
  intro p q hpq
  have hrel :
      Sym2.Rel (ℝ^2)
        (triangularPoint p.1 p.2, triangularPoint (p.1 + 1) (p.2 - 1))
        (triangularPoint q.1 q.2, triangularPoint (q.1 + 1) (q.2 - 1)) :=
    Sym2.exact hpq
  rw [Sym2.rel_iff] at hrel
  rcases hrel with ⟨h₁, _h₂⟩ | ⟨h₁, h₂⟩
  · exact triangularPoint_injective h₁
  · have hp : p = (q.1 + 1, q.2 - 1) := triangularPoint_injective h₁
    have hq : (p.1 + 1, p.2 - 1) = q := triangularPoint_injective h₂
    have hp₁ : p.1 = q.1 + 1 := congrArg Prod.fst hp
    have hq₁ : p.1 + 1 = q.1 := congrArg Prod.fst hq
    omega

private def triangularHexEastSources (n : ℕ) : Finset (ℤ × ℤ) :=
  (triangularHexCoords n).filter fun p => (p.1 + 1, p.2) ∈ triangularHexCoords n

private def triangularHexNorthSources (n : ℕ) : Finset (ℤ × ℤ) :=
  (triangularHexCoords n).filter fun p => (p.1, p.2 + 1) ∈ triangularHexCoords n

private def triangularHexSoutheastSources (n : ℕ) : Finset (ℤ × ℤ) :=
  (triangularHexCoords n).filter fun p => (p.1 + 1, p.2 - 1) ∈ triangularHexCoords n

private noncomputable def triangularHexEastUnitPairs (n : ℕ) : Finset (Sym2 (ℝ^2)) :=
  (triangularHexEastSources n).image
    fun p : ℤ × ℤ => s(triangularPoint p.1 p.2, triangularPoint (p.1 + 1) p.2)

private noncomputable def triangularHexNorthUnitPairs (n : ℕ) : Finset (Sym2 (ℝ^2)) :=
  (triangularHexNorthSources n).image
    fun p : ℤ × ℤ => s(triangularPoint p.1 p.2, triangularPoint p.1 (p.2 + 1))

private noncomputable def triangularHexSoutheastUnitPairs (n : ℕ) : Finset (Sym2 (ℝ^2)) :=
  (triangularHexSoutheastSources n).image
    fun p : ℤ × ℤ => s(triangularPoint p.1 p.2, triangularPoint (p.1 + 1) (p.2 - 1))

private lemma triangularHexEastUnitPairs_card (n : ℕ) :
    (triangularHexEastUnitPairs n).card = (triangularHexEastSources n).card := by
  classical
  unfold triangularHexEastUnitPairs
  rw [Finset.card_image_of_injective _ triangularHexEastUnitPair_injective]

private lemma triangularHexNorthUnitPairs_card (n : ℕ) :
    (triangularHexNorthUnitPairs n).card = (triangularHexNorthSources n).card := by
  classical
  unfold triangularHexNorthUnitPairs
  rw [Finset.card_image_of_injective _ triangularHexNorthUnitPair_injective]

private lemma triangularHexSoutheastUnitPairs_card (n : ℕ) :
    (triangularHexSoutheastUnitPairs n).card = (triangularHexSoutheastSources n).card := by
  classical
  unfold triangularHexSoutheastUnitPairs
  rw [Finset.card_image_of_injective _ triangularHexSoutheastUnitPair_injective]

private lemma triangularHexEastUnitPairs_subset_unitDist (n : ℕ) :
    triangularHexEastUnitPairs n ⊆
      (triangularHexPatch n).sym2.filter (fun q => dist q.out.1 q.out.2 = 1) := by
  classical
  intro q hq
  rw [triangularHexEastUnitPairs, Finset.mem_image] at hq
  rcases hq with ⟨p, hp, rfl⟩
  rw [triangularHexEastSources, Finset.mem_filter] at hp
  exact triangularHexPatch_east_pair_mem_unitDist hp.1 hp.2

private lemma triangularHexNorthUnitPairs_subset_unitDist (n : ℕ) :
    triangularHexNorthUnitPairs n ⊆
      (triangularHexPatch n).sym2.filter (fun q => dist q.out.1 q.out.2 = 1) := by
  classical
  intro q hq
  rw [triangularHexNorthUnitPairs, Finset.mem_image] at hq
  rcases hq with ⟨p, hp, rfl⟩
  rw [triangularHexNorthSources, Finset.mem_filter] at hp
  exact triangularHexPatch_north_pair_mem_unitDist hp.1 hp.2

private lemma triangularHexSoutheastUnitPairs_subset_unitDist (n : ℕ) :
    triangularHexSoutheastUnitPairs n ⊆
      (triangularHexPatch n).sym2.filter (fun q => dist q.out.1 q.out.2 = 1) := by
  classical
  intro q hq
  rw [triangularHexSoutheastUnitPairs, Finset.mem_image] at hq
  rcases hq with ⟨p, hp, rfl⟩
  rw [triangularHexSoutheastSources, Finset.mem_filter] at hp
  exact triangularHexPatch_southeast_pair_mem_unitDist hp.1 hp.2

private abbrev triangularHexThreeEdgeIndex (n : ℕ) :=
  triangularHexEastEdgeIndex n ⊕
    (triangularHexEastEdgeIndex n ⊕ triangularHexEastEdgeIndex n)

private def triangularHexThreeEdgeSourceCoord (n : ℕ) :
    triangularHexThreeEdgeIndex n → ℤ × ℤ
  | Sum.inl p => triangularHexEastSourceCoord n p
  | Sum.inr (Sum.inl p) =>
      (-(triangularHexEastSourceCoord n p).2,
        (triangularHexEastSourceCoord n p).1 + (triangularHexEastSourceCoord n p).2)
  | Sum.inr (Sum.inr p) =>
      ((triangularHexEastSourceCoord n p).1 + (triangularHexEastSourceCoord n p).2,
        -(triangularHexEastSourceCoord n p).1)

private def triangularHexThreeEdgeTargetCoord (n : ℕ) :
    triangularHexThreeEdgeIndex n → ℤ × ℤ
  | Sum.inl p =>
      ((triangularHexEastSourceCoord n p).1 + 1, (triangularHexEastSourceCoord n p).2)
  | Sum.inr (Sum.inl p) =>
      (-(triangularHexEastSourceCoord n p).2,
        (triangularHexEastSourceCoord n p).1 + (triangularHexEastSourceCoord n p).2 + 1)
  | Sum.inr (Sum.inr p) =>
      ((triangularHexEastSourceCoord n p).1 + (triangularHexEastSourceCoord n p).2 + 1,
        -(triangularHexEastSourceCoord n p).1 - 1)

private lemma triangularHexEastSourceCoord_mem (n : ℕ) (p : triangularHexEastEdgeIndex n) :
    triangularHexEastSourceCoord n p ∈ triangularHexCoords n := by
  rw [← triangularHexEastSourcePointIndex_coord n p]
  exact triangularHexPointCoord_mem n (triangularHexEastSourcePointIndex n p)

private lemma triangularHexEastTargetCoord_mem (n : ℕ) (p : triangularHexEastEdgeIndex n) :
    ((triangularHexEastSourceCoord n p).1 + 1,
        (triangularHexEastSourceCoord n p).2) ∈ triangularHexCoords n := by
  rw [← triangularHexEastTargetPointIndex_coord n p]
  exact triangularHexPointCoord_mem n (triangularHexEastTargetPointIndex n p)

private lemma triangularHexCoord_rotateNorth_mem {n : ℕ} {p : ℤ × ℤ}
    (hp : p ∈ triangularHexCoords n) :
    (-p.2, p.1 + p.2) ∈ triangularHexCoords n := by
  rw [mem_triangularHexCoords] at hp ⊢
  omega

private lemma triangularHexCoord_rotateSoutheast_mem {n : ℕ} {p : ℤ × ℤ}
    (hp : p ∈ triangularHexCoords n) :
    (p.1 + p.2, -p.1) ∈ triangularHexCoords n := by
  rw [mem_triangularHexCoords] at hp ⊢
  omega

private lemma triangularHexThreeEdgeSourceCoord_mem (n : ℕ)
    (p : triangularHexThreeEdgeIndex n) :
    triangularHexThreeEdgeSourceCoord n p ∈ triangularHexCoords n := by
  cases p with
  | inl p =>
      exact triangularHexEastSourceCoord_mem n p
  | inr p =>
      cases p with
      | inl p =>
          exact triangularHexCoord_rotateNorth_mem (triangularHexEastSourceCoord_mem n p)
      | inr p =>
          exact triangularHexCoord_rotateSoutheast_mem (triangularHexEastSourceCoord_mem n p)

private lemma triangularHexThreeEdgeTargetCoord_mem (n : ℕ)
    (p : triangularHexThreeEdgeIndex n) :
    triangularHexThreeEdgeTargetCoord n p ∈ triangularHexCoords n := by
  cases p with
  | inl p =>
      exact triangularHexEastTargetCoord_mem n p
  | inr p =>
      cases p with
      | inl p =>
          simpa [triangularHexThreeEdgeTargetCoord, add_assoc, add_left_comm, add_comm]
            using triangularHexCoord_rotateNorth_mem (triangularHexEastTargetCoord_mem n p)
      | inr p =>
          simpa [triangularHexThreeEdgeTargetCoord, sub_eq_add_neg, add_assoc, add_left_comm,
            add_comm]
            using triangularHexCoord_rotateSoutheast_mem (triangularHexEastTargetCoord_mem n p)

private lemma triangularHexThreeEdgeIndex_eq_of_source_target_eq (n : ℕ)
    {a b : triangularHexThreeEdgeIndex n}
    (hs : triangularHexThreeEdgeSourceCoord n a = triangularHexThreeEdgeSourceCoord n b)
    (ht : triangularHexThreeEdgeTargetCoord n a = triangularHexThreeEdgeTargetCoord n b) :
    a = b := by
  have hs₁ := congrArg Prod.fst hs
  have hs₂ := congrArg Prod.snd hs
  have ht₁ := congrArg Prod.fst ht
  have ht₂ := congrArg Prod.snd ht
  rcases a with a | a
  · rcases b with b | b
    · exact congrArg Sum.inl (triangularHexEastSourceCoord_injective n hs)
    · rcases b with b | b
      · exfalso
        simp [triangularHexThreeEdgeSourceCoord, triangularHexThreeEdgeTargetCoord] at hs₁ hs₂ ht₁ ht₂
        omega
      · exfalso
        simp [triangularHexThreeEdgeSourceCoord, triangularHexThreeEdgeTargetCoord] at hs₁ hs₂ ht₁ ht₂
        omega
  · rcases a with a | a
    · rcases b with b | b
      · exfalso
        simp [triangularHexThreeEdgeSourceCoord, triangularHexThreeEdgeTargetCoord] at hs₁ hs₂ ht₁ ht₂
        omega
      · rcases b with b | b
        · have hc : triangularHexEastSourceCoord n a = triangularHexEastSourceCoord n b := by
            simp [triangularHexThreeEdgeSourceCoord] at hs₁ hs₂
            ext <;> omega
          exact congrArg (fun e => Sum.inr (Sum.inl e))
            (triangularHexEastSourceCoord_injective n hc)
        · exfalso
          simp [triangularHexThreeEdgeSourceCoord, triangularHexThreeEdgeTargetCoord] at hs₁ hs₂ ht₁ ht₂
          omega
    · rcases b with b | b
      · exfalso
        simp [triangularHexThreeEdgeSourceCoord, triangularHexThreeEdgeTargetCoord] at hs₁ hs₂ ht₁ ht₂
        omega
      · rcases b with b | b
        · exfalso
          simp [triangularHexThreeEdgeSourceCoord, triangularHexThreeEdgeTargetCoord] at hs₁ hs₂ ht₁ ht₂
          omega
        · have hc : triangularHexEastSourceCoord n a = triangularHexEastSourceCoord n b := by
            simp [triangularHexThreeEdgeSourceCoord] at hs₁ hs₂
            ext <;> omega
          exact congrArg (fun e => Sum.inr (Sum.inr e))
            (triangularHexEastSourceCoord_injective n hc)

private lemma triangularHexThreeEdgeIndex_not_reverse (n : ℕ)
    {a b : triangularHexThreeEdgeIndex n}
    (hs : triangularHexThreeEdgeSourceCoord n a = triangularHexThreeEdgeTargetCoord n b)
    (ht : triangularHexThreeEdgeTargetCoord n a = triangularHexThreeEdgeSourceCoord n b) :
    False := by
  have hs₁ := congrArg Prod.fst hs
  have hs₂ := congrArg Prod.snd hs
  have ht₁ := congrArg Prod.fst ht
  have ht₂ := congrArg Prod.snd ht
  rcases a with a | a <;> rcases b with b | b
  · simp [triangularHexThreeEdgeSourceCoord, triangularHexThreeEdgeTargetCoord] at hs₁ hs₂ ht₁ ht₂
    omega
  · rcases b with b | b <;>
      simp [triangularHexThreeEdgeSourceCoord, triangularHexThreeEdgeTargetCoord] at hs₁ hs₂ ht₁ ht₂ <;>
      omega
  · rcases a with a | a <;>
      simp [triangularHexThreeEdgeSourceCoord, triangularHexThreeEdgeTargetCoord] at hs₁ hs₂ ht₁ ht₂ <;>
      omega
  · rcases a with a | a <;> rcases b with b | b <;>
      simp [triangularHexThreeEdgeSourceCoord, triangularHexThreeEdgeTargetCoord] at hs₁ hs₂ ht₁ ht₂ <;>
      omega

private noncomputable def triangularHexThreeUnitPairs (n : ℕ) : Finset (Sym2 (ℝ^2)) :=
  Finset.univ.image fun p : triangularHexThreeEdgeIndex n =>
    s(triangularPoint (triangularHexThreeEdgeSourceCoord n p).1
        (triangularHexThreeEdgeSourceCoord n p).2,
      triangularPoint (triangularHexThreeEdgeTargetCoord n p).1
        (triangularHexThreeEdgeTargetCoord n p).2)

private lemma triangularHexThreeUnitPair_injective (n : ℕ) :
    Function.Injective
      (fun p : triangularHexThreeEdgeIndex n =>
        s(triangularPoint (triangularHexThreeEdgeSourceCoord n p).1
            (triangularHexThreeEdgeSourceCoord n p).2,
          triangularPoint (triangularHexThreeEdgeTargetCoord n p).1
            (triangularHexThreeEdgeTargetCoord n p).2)) := by
  intro a b hab
  have hrel :
      Sym2.Rel (ℝ^2)
        (triangularPoint (triangularHexThreeEdgeSourceCoord n a).1
            (triangularHexThreeEdgeSourceCoord n a).2,
          triangularPoint (triangularHexThreeEdgeTargetCoord n a).1
            (triangularHexThreeEdgeTargetCoord n a).2)
        (triangularPoint (triangularHexThreeEdgeSourceCoord n b).1
            (triangularHexThreeEdgeSourceCoord n b).2,
          triangularPoint (triangularHexThreeEdgeTargetCoord n b).1
            (triangularHexThreeEdgeTargetCoord n b).2) :=
    Sym2.exact hab
  rw [Sym2.rel_iff] at hrel
  rcases hrel with ⟨hs, ht⟩ | ⟨hs, ht⟩
  · exact triangularHexThreeEdgeIndex_eq_of_source_target_eq n
      (triangularPoint_injective hs) (triangularPoint_injective ht)
  · exact False.elim <| triangularHexThreeEdgeIndex_not_reverse n
      (triangularPoint_injective hs) (triangularPoint_injective ht)

private lemma triangularHexThreeUnitPairs_card (n : ℕ) :
    (triangularHexThreeUnitPairs n).card = 9 * n ^ 2 + 3 * n := by
  classical
  unfold triangularHexThreeUnitPairs
  rw [Finset.card_image_of_injective]
  · simp [triangularHexThreeEdgeIndex, triangularHexEastEdgeIndex, Fintype.card_sum,
      Fintype.card_sigma, triangularHexEastEdgeIndex_card_aux]
    ring
  · exact triangularHexThreeUnitPair_injective n

private lemma triangularHexThreeUnitPairs_subset_unitDist (n : ℕ) :
    triangularHexThreeUnitPairs n ⊆
      (triangularHexPatch n).sym2.filter (fun q => dist q.out.1 q.out.2 = 1) := by
  classical
  intro q hq
  rw [triangularHexThreeUnitPairs, Finset.mem_image] at hq
  rcases hq with ⟨p, _hp, rfl⟩
  have h₁ :
      triangularPoint (triangularHexThreeEdgeSourceCoord n p).1
          (triangularHexThreeEdgeSourceCoord n p).2 ∈ triangularHexPatch n := by
    unfold triangularHexPatch
    exact Finset.mem_image.mpr
      ⟨triangularHexThreeEdgeSourceCoord n p, triangularHexThreeEdgeSourceCoord_mem n p, rfl⟩
  have h₂ :
      triangularPoint (triangularHexThreeEdgeTargetCoord n p).1
          (triangularHexThreeEdgeTargetCoord n p).2 ∈ triangularHexPatch n := by
    unfold triangularHexPatch
    exact Finset.mem_image.mpr
      ⟨triangularHexThreeEdgeTargetCoord n p, triangularHexThreeEdgeTargetCoord_mem n p, rfl⟩
  cases p with
  | inl p =>
      have h₁' :
          triangularPoint (triangularHexEastSourceCoord n p).1
              (triangularHexEastSourceCoord n p).2 ∈ triangularHexPatch n := by
        simpa [triangularHexThreeEdgeSourceCoord] using h₁
      have h₂' :
          triangularPoint ((triangularHexEastSourceCoord n p).1 + 1)
              (triangularHexEastSourceCoord n p).2 ∈ triangularHexPatch n := by
        simpa [triangularHexThreeEdgeTargetCoord] using h₂
      simp [h₁', h₂', dist_out_eq_of_eq_sym2_mk rfl, triangularHexThreeEdgeSourceCoord,
        triangularHexThreeEdgeTargetCoord, triangularPoint_dist_east]
  | inr p =>
      cases p with
      | inl p =>
          have h₁' :
              triangularPoint (-(triangularHexEastSourceCoord n p).2)
                  ((triangularHexEastSourceCoord n p).1 +
                    (triangularHexEastSourceCoord n p).2) ∈ triangularHexPatch n := by
            simpa [triangularHexThreeEdgeSourceCoord] using h₁
          have h₂' :
              triangularPoint (-(triangularHexEastSourceCoord n p).2)
                  ((triangularHexEastSourceCoord n p).1 +
                    (triangularHexEastSourceCoord n p).2 + 1) ∈ triangularHexPatch n := by
            simpa [triangularHexThreeEdgeTargetCoord] using h₂
          simp [h₁', h₂', dist_out_eq_of_eq_sym2_mk rfl, triangularHexThreeEdgeSourceCoord,
            triangularHexThreeEdgeTargetCoord, triangularPoint_dist_north]
      | inr p =>
          have h₁' :
              triangularPoint ((triangularHexEastSourceCoord n p).1 +
                    (triangularHexEastSourceCoord n p).2)
                  (-(triangularHexEastSourceCoord n p).1) ∈ triangularHexPatch n := by
            simpa [triangularHexThreeEdgeSourceCoord] using h₁
          have h₂' :
              triangularPoint ((triangularHexEastSourceCoord n p).1 +
                    (triangularHexEastSourceCoord n p).2 + 1)
                  (-(triangularHexEastSourceCoord n p).1 - 1) ∈ triangularHexPatch n := by
            simpa [triangularHexThreeEdgeTargetCoord] using h₂
          simp [h₁', h₂', dist_out_eq_of_eq_sym2_mk rfl, triangularHexThreeEdgeSourceCoord,
            triangularHexThreeEdgeTargetCoord, triangularPoint_dist_southeast]

/--
The axial hexagonal triangular-lattice patch contains at least `9n^2 + 3n`
unordered unit-distance pairs.
-/
@[category API, AMS 52]
theorem triangularHexPatch_unitPairs_lower (n : ℕ) :
    9 * n ^ 2 + 3 * n ≤ unitDistNum (triangularHexPatch n) := by
  classical
  have hcard_le := Finset.card_le_card (triangularHexThreeUnitPairs_subset_unitDist n)
  rw [triangularHexThreeUnitPairs_card] at hcard_le
  exact hcard_le

private lemma unitDistNum_le_sym2_card {d : ℕ} (s : Finset (ℝ^d)) :
    unitDistNum s ≤ s.sym2.card := by
  unfold unitDistNum
  exact Finset.card_filter_le _ _

/--
A local construction certificate for the triangular/hexagonal patch needed for the lower
bound in Erdős Problem 1084.
-/
def TriangularLowerCertificate (n : ℕ) : Prop :=
  ∃ points : Finset (ℝ^2),
    points.card = 3 * n ^ 2 + 3 * n + 1 ∧
    Metric.IsSeparated' 1 (points : Set (ℝ^2)) ∧
    9 * n ^ 2 + 3 * n ≤ unitDistNum points

private lemma f_lower_of_witness {d N m : ℕ} (s : Finset (ℝ^d))
    (hcard : s.card = N)
    (hsep : Metric.IsSeparated' 1 (s : Set (ℝ^d)))
    (hunit : m ≤ unitDistNum s) :
    m ≤ f d N := by
  classical
  unfold f
  refine le_ciSup_of_le ?outer s ?_
  · refine ⟨Nat.choose (N + 1) 2, ?_⟩
    rintro _ ⟨t, rfl⟩
    refine ciSup_le' ?_
    intro ht
    refine ciSup_le' ?_
    intro _htsep
    exact (unitDistNum_le_sym2_card t).trans_eq (by rw [Finset.card_sym2, ht])
  · refine le_ciSup_of_le ?cardBdd hcard ?_
    · refine ⟨unitDistNum s, ?_⟩
      rintro _ ⟨hc, rfl⟩
      exact ciSup_le' fun _ => le_rfl
    · exact le_ciSup_of_le ⟨unitDistNum s, by rintro _ ⟨hs, rfl⟩; exact le_rfl⟩ hsep hunit

/--
The lower-bound packaging step for Erdős Problem 1084: any verified triangular patch with
`3n^2 + 3n + 1` points and at least `9n^2 + 3n` unit-distance pairs gives the desired
lower bound for `f 2`.
-/
@[category API, AMS 52]
theorem erdos_1084.variants.triangular_optimal_d2_lower_of_certificate
    (n : ℕ) (cert : TriangularLowerCertificate n) :
    9 * n ^ 2 + 3 * n ≤ f 2 (3 * n ^ 2 + 3 * n + 1) := by
  rcases cert with ⟨points, hcard, hsep, hunit⟩
  exact f_lower_of_witness points hcard hsep hunit

/--
The axial hexagonal triangular-lattice patch with `3n^2 + 3n + 1` points is
`1`-separated and contains at least `9n^2 + 3n` unordered unit-distance pairs.
-/
theorem erdos_1084.variants.triangular_lower_certificate (n : ℕ) :
    TriangularLowerCertificate n := by
  exact ⟨triangularHexPatch n, triangularHexPatch_card n, triangularHexPatch_oneSeparated n,
    triangularHexPatch_unitPairs_lower n⟩

end Erdos1084

open Erdos1084

/--
A finite polygonal realization of a cycle, with its ordered vertices, closed edge paths,
and the certificates needed to show that its polygonal boundary is simple.
-/
structure Erdos1084.PolygonalCycleCertificate (n : ℕ) where
  three_le : 3 ≤ n
  vertex : Fin (n + 1) → ℝ^2
  closed : vertex 0 = vertex (Fin.last n)
  vertex_injective : Function.Injective (fun i : Fin n => vertex i.castSucc)
  carrier : Set (ℝ^2)
  carrier_eq :
    carrier = ⋃ i : Fin n, Set.range (Path.segment (vertex i.castSucc) (vertex i.succ))
  edge_inter_subset_common_endpoints :
    ∀ i j : Fin n, i ≠ j →
      segment ℝ (vertex i.castSucc) (vertex i.succ) ∩
          segment ℝ (vertex j.castSucc) (vertex j.succ) ⊆
        ({vertex i.castSucc, vertex i.succ} : Set (ℝ^2)) ∩
          ({vertex j.castSucc, vertex j.succ} : Set (ℝ^2))

namespace Erdos1084.PolygonalCycleCertificate

/-- The edge obtained by moving `k` steps cyclically from `start`. -/
def cyclicEdge {n : ℕ} (cert : PolygonalCycleCertificate n) (start : Fin n) (k : ℕ) :
    Fin n :=
  ⟨(start.val + k) % n, Nat.mod_lt _ (by have := cert.three_le; omega)⟩

/-- The canonical (nonduplicated) vertex reached after `k` cyclic edge steps. -/
def cyclicVertex {n : ℕ} (cert : PolygonalCycleCertificate n) (start : Fin n) (k : ℕ) :
    ℝ^2 :=
  cert.vertex (cert.cyclicEdge start k).castSucc

/--
A nonempty proper consecutive cyclic block of horizontal edges in a polygonal-cycle
certificate.  `horizontal` says that all block vertices have one common height.
-/
structure HorizontalEdgeBlock {n : ℕ} (cert : PolygonalCycleCertificate n) where
  start : Fin n
  length : ℕ
  length_pos : 0 < length
  length_lt : length < n
  horizontal : ∀ k ≤ length, cert.cyclicVertex start k 1 = cert.cyclicVertex start 0 1

/-- The initial vertex of a horizontal edge block. -/
def HorizontalEdgeBlock.leftTerminal {n : ℕ} {cert : PolygonalCycleCertificate n}
    (block : cert.HorizontalEdgeBlock) : ℝ^2 :=
  cert.cyclicVertex block.start 0

/-- The terminal vertex of a horizontal edge block. -/
def HorizontalEdgeBlock.rightTerminal {n : ℕ} {cert : PolygonalCycleCertificate n}
    (block : cert.HorizontalEdgeBlock) : ℝ^2 :=
  cert.cyclicVertex block.start block.length

/-- Consecutive canonical cyclic vertices are the endpoints of the corresponding edge. -/
@[category API, AMS 52]
theorem cyclicVertex_succ {n : ℕ} (cert : PolygonalCycleCertificate n)
    (start : Fin n) (k : ℕ) :
    cert.cyclicVertex start (k + 1) =
      cert.vertex (cert.cyclicEdge start k).succ := by
  have hn : 0 < n := by have := cert.three_le; omega
  have hmod : (start.val + (k + 1)) % n = ((start.val + k) % n + 1) % n := by
    rw [show start.val + (k + 1) = (start.val + k) + 1 by omega, Nat.add_mod]
    simp
  by_cases hlast : (cert.cyclicEdge start k).val + 1 = n
  · have hsucc : (cert.cyclicEdge start k).succ = Fin.last n := by
      apply Fin.ext
      simpa using hlast
    rw [hsucc, ← cert.closed]
    apply congrArg cert.vertex
    apply Fin.ext
    change (start.val + (k + 1)) % n = 0
    rw [hmod, show (start.val + k) % n + 1 = n by simpa [cyclicEdge] using hlast]
    exact Nat.mod_self n
  · apply congrArg cert.vertex
    apply Fin.ext
    change (start.val + (k + 1)) % n = (start.val + k) % n + 1
    rw [hmod, Nat.mod_eq_of_lt]
    have hlt := Nat.mod_lt (start.val + k) hn
    simpa [cyclicEdge] using lt_of_le_of_ne (Nat.succ_le_iff.2 hlt) hlast

/-- Every edge of a horizontal edge block is a certified carrier segment. -/
@[category API, AMS 52]
theorem HorizontalEdgeBlock.edge_segment_subset_carrier
    {n : ℕ} {cert : PolygonalCycleCertificate n} (block : cert.HorizontalEdgeBlock)
    {k : ℕ} (_hk : k < block.length) :
    segment ℝ (cert.cyclicVertex block.start k) (cert.cyclicVertex block.start (k + 1)) ⊆
      cert.carrier := by
  rw [cert.cyclicVertex_succ block.start k]
  change segment ℝ (cert.vertex (cert.cyclicEdge block.start k).castSucc)
      (cert.vertex (cert.cyclicEdge block.start k).succ) ⊆ cert.carrier
  rw [cert.carrier_eq]
  refine Set.subset_iUnion_of_subset (cert.cyclicEdge block.start k) ?_
  rw [Path.range_segment]

/-- Three planar points of one height are collinear. -/
@[category API, AMS 52]
theorem collinear_of_coord_one_eq (a b c : ℝ^2)
    (hab : b 1 = a 1) (hac : c 1 = a 1) :
    Collinear ℝ ({a, b, c} : Set (ℝ^2)) := by
  rw [collinear_iff_exists_forall_eq_smul_vadd]
  refine ⟨a, EuclideanSpace.single 0 1, ?_⟩
  intro p hp
  simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hp
  rcases hp with hpa | hpb | hpc
  · subst p
    exact ⟨0, by simp⟩
  · subst p
    refine ⟨b 0 - a 0, ?_⟩
    ext i
    fin_cases i
    · simp [EuclideanSpace.single_apply]
    · simp [EuclideanSpace.single_apply, hab]
  · subst p
    refine ⟨c 0 - a 0, ?_⟩
    ext i
    fin_cases i
    · simp [EuclideanSpace.single_apply]
    · simp [EuclideanSpace.single_apply, hac]

/-- For three collinear points, the outer segment is covered by the two adjacent segments. -/
@[category API, AMS 52]
theorem segment_subset_union_of_collinear {a b c : ℝ^2}
    (hcol : Collinear ℝ ({a, b, c} : Set (ℝ^2))) :
    segment ℝ a c ⊆ segment ℝ a b ∪ segment ℝ b c := by
  rcases hcol.wbtw_or_wbtw_or_wbtw with habc | hbca | hcab
  · intro x hx
    rw [← insert_endpoints_openSegment] at hx
    rcases hx with hxa | hxc | hx
    · subst x
      exact Or.inl (left_mem_segment ℝ a b)
    · subst x
      exact Or.inr (right_mem_segment ℝ b c)
    · have hbline : b ∈ Set.range (AffineMap.lineMap a c : ℝ → ℝ^2) := by
        rcases habc with ⟨t, ht, htb⟩
        exact ⟨t, htb⟩
      have hsplit := openSegment_subset_union a c hbline hx
      rcases hsplit with hxb | hx | hx
      · subst x
        exact Or.inl (right_mem_segment ℝ a b)
      · exact Or.inl (openSegment_subset_segment ℝ a b hx)
      · exact Or.inr (openSegment_subset_segment ℝ b c hx)
  · have hc : c ∈ segment ℝ a b := by
      simpa [segment_symm] using hbca.mem_segment
    exact (convex_segment a b).segment_subset
      (left_mem_segment ℝ a b) hc |>.trans (Set.subset_union_left)
  · have ha : a ∈ segment ℝ b c := by
      simpa [segment_symm] using hcab.mem_segment
    exact (convex_segment b c).segment_subset ha
      (right_mem_segment ℝ b c) |>.trans (Set.subset_union_right)

end Erdos1084.PolygonalCycleCertificate

/-- A horizontal cyclic edge block contains the segment joining its terminal vertices. -/
theorem Erdos1084.PolygonalCycleCertificate.horizontalEdgeBlock_segment_subset_carrier
    {n : ℕ} (cert : Erdos1084.PolygonalCycleCertificate n)
    (block : cert.HorizontalEdgeBlock) :
    segment ℝ block.leftTerminal block.rightTerminal ⊆ cert.carrier := by
  change segment ℝ (cert.cyclicVertex block.start 0)
      (cert.cyclicVertex block.start block.length) ⊆ cert.carrier
  have hprefix : ∀ m ≤ block.length,
      segment ℝ (cert.cyclicVertex block.start 0) (cert.cyclicVertex block.start m) ⊆
        cert.carrier := by
    intro m hm
    induction m with
    | zero =>
        intro x hx
        simpa using block.edge_segment_subset_carrier (k := 0) block.length_pos
          (show x ∈ segment ℝ (cert.cyclicVertex block.start 0)
            (cert.cyclicVertex block.start 1) from
              (show x = cert.cyclicVertex block.start 0 by simpa using hx) ▸
                left_mem_segment ℝ _ _)
    | succ m ih =>
        have hm' : m ≤ block.length := by omega
        have hedge : segment ℝ (cert.cyclicVertex block.start m)
            (cert.cyclicVertex block.start (m + 1)) ⊆ cert.carrier :=
          block.edge_segment_subset_carrier (by omega)
        have hcol : Collinear ℝ
            ({cert.cyclicVertex block.start 0, cert.cyclicVertex block.start m,
              cert.cyclicVertex block.start (m + 1)} : Set (ℝ^2)) :=
          collinear_of_coord_one_eq _ _ _ (block.horizontal m hm')
            (block.horizontal (m + 1) (by omega))
        exact (segment_subset_union_of_collinear hcol).trans (Set.union_subset (ih hm') hedge)
  exact hprefix block.length le_rfl

/--
If a horizontal segment between two certified vertices lies in the carrier, then a point
outside the carrier and at the same height sees either both terminal vertices or neither.
-/
theorem Erdos1084.PolygonalCycleCertificate.horizontal_chain_terminals_visible_iff
    {n : ℕ} (cert : Erdos1084.PolygonalCycleCertificate n)
    (q : EuclideanSpace ℝ (Fin 2)) (i j : Fin (n + 1))
    (hyi : q 1 = cert.vertex i 1)
    (hyj : q 1 = cert.vertex j 1)
    (hsegment :
      segment ℝ (cert.vertex i) (cert.vertex j) ⊆ cert.carrier)
    (hq : q ∉ cert.carrier) :
    q 0 < cert.vertex i 0 ↔ q 0 < cert.vertex j 0 := by
  constructor
  · intro hi
    by_contra hj
    have hji : cert.vertex j 0 < cert.vertex i 0 := by
      exact lt_of_le_of_lt (le_of_not_gt hj) hi
    have hden : cert.vertex j 0 - cert.vertex i 0 < 0 := by linarith
    let t : ℝ := (q 0 - cert.vertex i 0) /
      (cert.vertex j 0 - cert.vertex i 0)
    have ht0 : 0 ≤ t := by
      dsimp [t]
      exact div_nonneg_of_nonpos (by linarith) hden.le
    have ht1 : t ≤ 1 := by
      dsimp [t]
      exact div_le_one_of_ge (by linarith) hden.le
    have hline : AffineMap.lineMap (cert.vertex i) (cert.vertex j) t = q := by
      ext k
      fin_cases k
      · rw [AffineMap.lineMap_apply_module']
        change t * (cert.vertex j 0 - cert.vertex i 0) + cert.vertex i 0 = q 0
        dsimp [t]
        rw [div_mul_cancel₀]
        · ring
        · linarith
      · rw [AffineMap.lineMap_apply_module']
        change t * (cert.vertex j 1 - cert.vertex i 1) + cert.vertex i 1 = q 1
        rw [← hyi, ← hyj]
        ring
    apply hq
    apply hsegment
    rw [segment_eq_image_lineMap]
    exact ⟨t, ⟨ht0, ht1⟩, hline⟩
  · intro hj
    by_contra hi
    have hij : cert.vertex i 0 < cert.vertex j 0 := by
      exact lt_of_le_of_lt (le_of_not_gt hi) hj
    have hden : 0 < cert.vertex j 0 - cert.vertex i 0 := by linarith
    let t : ℝ := (q 0 - cert.vertex i 0) /
      (cert.vertex j 0 - cert.vertex i 0)
    have ht0 : 0 ≤ t := by
      dsimp [t]
      exact div_nonneg (by linarith) hden.le
    have ht1 : t ≤ 1 := by
      dsimp [t]
      exact (div_le_one hden).2 (by linarith)
    have hline : AffineMap.lineMap (cert.vertex i) (cert.vertex j) t = q := by
      ext k
      fin_cases k
      · rw [AffineMap.lineMap_apply_module']
        change t * (cert.vertex j 0 - cert.vertex i 0) + cert.vertex i 0 = q 0
        dsimp [t]
        rw [div_mul_cancel₀]
        · ring
        · linarith
      · rw [AffineMap.lineMap_apply_module']
        change t * (cert.vertex j 1 - cert.vertex i 1) + cert.vertex i 1 = q 1
        rw [← hyi, ← hyj]
        ring
    apply hq
    apply hsegment
    rw [segment_eq_image_lineMap]
    exact ⟨t, ⟨ht0, ht1⟩, hline⟩

/--
A point outside a certified horizontal edge block sees either both terminal vertices or
neither.
-/
theorem Erdos1084.PolygonalCycleCertificate.horizontalEdgeBlock_terminals_visible_iff
    {n : ℕ} (cert : Erdos1084.PolygonalCycleCertificate n)
    (block : cert.HorizontalEdgeBlock)
    (q : EuclideanSpace ℝ (Fin 2))
    (hy : q 1 = block.leftTerminal 1)
    (hq : q ∉ cert.carrier) :
    q 0 < block.leftTerminal 0 ↔ q 0 < block.rightTerminal 0 := by
  apply cert.horizontal_chain_terminals_visible_iff q
    (cert.cyclicEdge block.start 0).castSucc
    (cert.cyclicEdge block.start block.length).castSucc
  · exact hy
  · exact hy.trans (block.horizontal block.length le_rfl).symm
  · exact cert.horizontalEdgeBlock_segment_subset_carrier block
  · exact hq

/--
A horizontal edge block is maximal when the neighboring vertices immediately before and
after the block do not have the common height of the block.
-/
def Erdos1084.PolygonalCycleCertificate.HorizontalEdgeBlock.IsMaximal
    {n : ℕ} {cert : Erdos1084.PolygonalCycleCertificate n}
    (block : cert.HorizontalEdgeBlock) : Prop :=
  cert.cyclicVertex block.start (n - 1) 1 ≠ block.leftTerminal 1 ∧
    cert.cyclicVertex block.start (block.length + 1) 1 ≠ block.rightTerminal 1

/--
The two edges adjoining a visible maximal horizontal block contribute even horizontal-ray
crossing parity exactly when their nonterminal vertices lie on the same side of the block.
-/
theorem Erdos1084.PolygonalCycleCertificate.horizontalEdgeBlock_terminal_crossings_parity_even_iff_sameSide
    {n : ℕ} (cert : Erdos1084.PolygonalCycleCertificate n)
    (block : cert.HorizontalEdgeBlock)
    (hmax : block.IsMaximal)
    (q : EuclideanSpace ℝ (Fin 2))
    (hy : q 1 = block.leftTerminal 1)
    (hq : q ∉ cert.carrier)
    (hvisible : q 0 < block.leftTerminal 0) :
    ((if Erdos1084.horizontalRayCrosses q
          (cert.cyclicVertex block.start (n - 1))
          block.leftTerminal then 1 else 0 : ℕ) +
       (if Erdos1084.horizontalRayCrosses q
          block.rightTerminal
          (cert.cyclicVertex block.start (block.length + 1))
        then 1 else 0)) % 2 = 0 ↔
      (block.leftTerminal 1 <
            cert.cyclicVertex block.start (n - 1) 1 ∧
        block.rightTerminal 1 <
            cert.cyclicVertex block.start (block.length + 1) 1) ∨
      (cert.cyclicVertex block.start (n - 1) 1 <
            block.leftTerminal 1 ∧
        cert.cyclicVertex block.start (block.length + 1) 1 <
            block.rightTerminal 1) := by
  have hyright : q 1 = block.rightTerminal 1 :=
    hy.trans (block.horizontal block.length le_rfl).symm
  have hvisright : q 0 < block.rightTerminal 0 :=
    (cert.horizontalEdgeBlock_terminals_visible_iff block q hy hq).mp hvisible
  have hparity := Erdos1084.horizontalRayCrosses_two_visible_terminals_parity_even_iff
    q (cert.cyclicVertex block.start (n - 1)) block.leftTerminal block.rightTerminal
      (cert.cyclicVertex block.start (block.length + 1))
      hy hyright hvisible hvisright
  rw [hparity]
  rcases hmax with ⟨hleft, hright⟩
  constructor
  · rintro (habove | hbelow)
    · exact Or.inl habove
    · exact Or.inr ⟨lt_of_le_of_ne (le_of_not_gt hbelow.1) hleft,
        lt_of_le_of_ne (le_of_not_gt hbelow.2) hright⟩
  · rintro (habove | hbelow)
    · exact Or.inl habove
    · exact Or.inr ⟨not_lt_of_ge hbelow.1.le, not_lt_of_ge hbelow.2.le⟩

/-- If the terminal vertex of one certified edge equals the initial vertex of another,
then the second edge is its ordinary or cyclic successor. -/
@[category API, AMS 52]
theorem Erdos1084.edge_terminal_eq_initial_imp_cyclic_succ
    {n : ℕ} (cert : Erdos1084.PolygonalCycleCertificate n)
    {i j : Fin n}
    (h : cert.vertex i.succ = cert.vertex j.castSucc) :
    i.val + 1 = j.val ∨
      (i.val + 1 = n ∧ j.val = 0) := by
  by_cases hi : i.val + 1 < n
  · left
    let k : Fin n := ⟨i.val + 1, hi⟩
    have hik : i.succ = k.castSucc := by
      apply Fin.ext
      simp only [Fin.val_succ, Fin.val_castSucc, k]
    have hkj : k = j := cert.vertex_injective (by simpa [hik] using h)
    simpa only [k] using congrArg Fin.val hkj
  · right
    have hin : i.val + 1 = n := by omega
    refine ⟨hin, ?_⟩
    have hi_last : i.succ = Fin.last n := by
      apply Fin.ext
      simp only [Fin.val_succ, Fin.val_last]
      exact hin
    let z : Fin n := ⟨0, by omega⟩
    have hzj : z = j := cert.vertex_injective (by
      have hzero : cert.vertex (0 : Fin (n + 1)) = cert.vertex j.castSucc :=
        cert.closed.trans ((congrArg cert.vertex hi_last).symm.trans h)
      simpa only [z, Fin.castSucc_zero] using hzero)
    simpa only [z] using (congrArg Fin.val hzj).symm

/-- If the initial vertex of one certified edge equals the terminal vertex of another,
then the latter edge is its ordinary or cyclic predecessor. -/
@[category API, AMS 52]
theorem Erdos1084.edge_initial_eq_terminal_imp_cyclic_pred
    {n : ℕ} (cert : Erdos1084.PolygonalCycleCertificate n)
    {i j : Fin n}
    (h : cert.vertex i.castSucc = cert.vertex j.succ) :
    j.val + 1 = i.val ∨
      (j.val + 1 = n ∧ i.val = 0) := by
  exact Erdos1084.edge_terminal_eq_initial_imp_cyclic_succ cert h.symm

/-- Every edge in a polygonal-cycle certificate has distinct endpoints. -/
@[category API, AMS 52]
theorem Erdos1084.PolygonalCycleCertificate.edge_endpoints_ne
    {n : ℕ} (cert : Erdos1084.PolygonalCycleCertificate n)
    (i : Fin n) :
    cert.vertex i.castSucc ≠ cert.vertex i.succ := by
  intro h
  by_cases hi : i.val + 1 < n
  · let j : Fin n := ⟨i.val + 1, hi⟩
    have hij : i = j := cert.vertex_injective (by simpa [j] using h)
    have hval := congrArg Fin.val hij
    simp only [j] at hval
    omega
  · have hi_last : i.succ = Fin.last n := by
      apply Fin.ext
      simp only [Fin.val_succ, Fin.val_last]
      omega
    have hvertex_zero : cert.vertex i.castSucc = cert.vertex (0 : Fin (n + 1)) :=
      h.trans ((congrArg cert.vertex hi_last).trans cert.closed.symm)
    let z : Fin n := ⟨0, by omega⟩
    have hi_zero : i = z :=
      cert.vertex_injective (by simpa [z] using hvertex_zero)
    have hval : i.val = 0 := by
      simpa [z] using congrArg Fin.val hi_zero
    have hn := cert.three_le
    omega

/-- Every edge path in a polygonal-cycle certificate is injective. -/
@[category API, AMS 52]
theorem Erdos1084.PolygonalCycleCertificate.edgePath_injective
    {n : ℕ} (cert : Erdos1084.PolygonalCycleCertificate n)
    (i : Fin n) :
    Function.Injective
      (Path.segment (cert.vertex i.castSucc) (cert.vertex i.succ)) := by
  intro s t hst
  apply Subtype.ext
  apply AffineMap.lineMap_injective ℝ (cert.edge_endpoints_ne i)
  exact hst

/--
If points on two distinct certified edges coincide, then both points are edge endpoints.
-/
@[category API, AMS 52]
theorem Erdos1084.PolygonalCycleCertificate.distinct_edge_eq_imp_parameters_endpoint
    {n : ℕ} (cert : Erdos1084.PolygonalCycleCertificate n)
    {i j : Fin n} (hij : i ≠ j)
    {s t : Set.Icc (0 : ℝ) 1}
    (h :
      Path.segment (cert.vertex i.castSucc) (cert.vertex i.succ) s =
      Path.segment (cert.vertex j.castSucc) (cert.vertex j.succ) t) :
    (s = 0 ∨ s = 1) ∧ (t = 0 ∨ t = 1) := by
  have hi_mem :
      Path.segment (cert.vertex i.castSucc) (cert.vertex i.succ) s ∈
        segment ℝ (cert.vertex i.castSucc) (cert.vertex i.succ) := by
    rw [← Path.range_segment]
    exact ⟨s, rfl⟩
  have hj_mem :
      Path.segment (cert.vertex i.castSucc) (cert.vertex i.succ) s ∈
        segment ℝ (cert.vertex j.castSucc) (cert.vertex j.succ) := by
    rw [h, ← Path.range_segment]
    exact ⟨t, rfl⟩
  have hendpoints :=
    cert.edge_inter_subset_common_endpoints i j hij ⟨hi_mem, hj_mem⟩
  simp only [Set.mem_inter_iff, Set.mem_insert_iff, Set.mem_singleton_iff] at hendpoints
  constructor
  · rcases hendpoints.1 with hs | hs
    · left
      apply cert.edgePath_injective i
      simpa using hs
    · right
      apply cert.edgePath_injective i
      simpa using hs
  · rcases hendpoints.2 with ht | ht
    · left
      apply cert.edgePath_injective j
      simpa [h] using ht
    · right
      apply cert.edgePath_injective j
      simpa [h] using ht

/--
If points on two distinct certified edges coincide, then they are the common endpoint of
cyclically consecutive edges, with the corresponding endpoint parameters.
-/
@[category API, AMS 52]
theorem Erdos1084.distinct_edge_eq_imp_cyclic_incidence
    {n : ℕ} (cert : Erdos1084.PolygonalCycleCertificate n)
    {i j : Fin n} (hij : i ≠ j)
    {s t : Set.Icc (0 : ℝ) 1}
    (h :
      Path.segment (cert.vertex i.castSucc) (cert.vertex i.succ) s =
      Path.segment (cert.vertex j.castSucc) (cert.vertex j.succ) t) :
    (s = 1 ∧ t = 0 ∧
        (i.val + 1 = j.val ∨ (i.val + 1 = n ∧ j.val = 0))) ∨
    (s = 0 ∧ t = 1 ∧
        (j.val + 1 = i.val ∨ (j.val + 1 = n ∧ i.val = 0))) := by
  have terminal_injective :
      Function.Injective (fun k : Fin n => cert.vertex k.succ) := by
    intro a b hab
    change cert.vertex a.succ = cert.vertex b.succ at hab
    by_cases ha : a.val + 1 < n
    · let a' : Fin n := ⟨a.val + 1, ha⟩
      have ha_succ : a.succ = a'.castSucc := by
        apply Fin.ext
        simp only [Fin.val_succ, Fin.val_castSucc, a']
      by_cases hb : b.val + 1 < n
      · let b' : Fin n := ⟨b.val + 1, hb⟩
        have hb_succ : b.succ = b'.castSucc := by
          apply Fin.ext
          simp only [Fin.val_succ, Fin.val_castSucc, b']
        have hab' : a' = b' := cert.vertex_injective (by simpa [ha_succ, hb_succ] using hab)
        apply Fin.ext
        have hval := congrArg Fin.val hab'
        simp only [a', b'] at hval
        omega
      · have hb_last : b.succ = Fin.last n := by
          apply Fin.ext
          simp only [Fin.val_succ, Fin.val_last]
          omega
        let z : Fin n := ⟨0, by omega⟩
        have ha_zero : a' = z := cert.vertex_injective (by
          rw [ha_succ, hb_last, ← cert.closed] at hab
          simpa only [z, Fin.castSucc_zero] using hab)
        have hval := congrArg Fin.val ha_zero
        simp only [a', z] at hval
        omega
    · by_cases hb : b.val + 1 < n
      · let b' : Fin n := ⟨b.val + 1, hb⟩
        have hb_succ : b.succ = b'.castSucc := by
          apply Fin.ext
          simp only [Fin.val_succ, Fin.val_castSucc, b']
        have ha_last : a.succ = Fin.last n := by
          apply Fin.ext
          simp only [Fin.val_succ, Fin.val_last]
          omega
        let z : Fin n := ⟨0, by omega⟩
        have hz_b : z = b' := cert.vertex_injective (by
          rw [ha_last, hb_succ, ← cert.closed] at hab
          simpa only [z, Fin.castSucc_zero] using hab)
        have hval := congrArg Fin.val hz_b
        simp only [z, b'] at hval
        omega
      · apply Fin.ext
        omega
  rcases cert.distinct_edge_eq_imp_parameters_endpoint hij h with ⟨hs, ht⟩
  rcases hs with hs | hs
  · rcases ht with ht | ht
    · have hv : cert.vertex i.castSucc = cert.vertex j.castSucc := by
        simpa [hs, ht] using h
      exact (hij (cert.vertex_injective hv)).elim
    · right
      refine ⟨hs, ht, ?_⟩
      apply Erdos1084.edge_initial_eq_terminal_imp_cyclic_pred cert
      simpa [hs, ht] using h
  · rcases ht with ht | ht
    · left
      refine ⟨hs, ht, ?_⟩
      apply Erdos1084.edge_terminal_eq_initial_imp_cyclic_succ cert
      simpa [hs, ht] using h
    · have hv : cert.vertex i.succ = cert.vertex j.succ := by
        simpa [hs, ht] using h
      exact (hij (terminal_injective hv)).elim

/--
There is a continuous real-period parametrization of a certified polygonal cycle whose
restriction to each half-open unit interval is the corresponding affine edge path.
-/
@[category API, AMS 52]
theorem Erdos1084.exists_polygonalPeriodMap_edgewise
    {n : ℕ} (cert : Erdos1084.PolygonalCycleCertificate n) :
    ∃ f : ℝ → (Fin 2 → ℝ),
      ContinuousOn f (Set.Icc 0 (n : ℝ)) ∧
      f 0 = f n ∧
      ∀ (i : Fin n) (s : Set.Ico (0 : ℝ) 1),
        f ((i.val : ℝ) + s) =
          (Path.segment (cert.vertex i.castSucc) (cert.vertex i.succ)
            (⟨(s : ℝ), s.2.1, s.2.2.le⟩ :
              Set.Icc (0 : ℝ) 1)).ofLp := by
  classical
  let v : ℕ → (Fin 2 → ℝ) := fun k =>
    (cert.vertex ⟨min k n, Nat.lt_succ_iff.mpr (min_le_right k n)⟩).ofLp
  let f : ℝ → (Fin 2 → ℝ) := fun t =>
    v 0 + ∑ k : Fin n,
      (min 1 (max 0 (t - (k.val : ℝ)))) • (v (k.val + 1) - v k.val)
  refine ⟨f, ?_, ?_, ?_⟩
  · exact (by fun_prop : Continuous f).continuousOn
  · simp only [f]
    have hsum (t : ℝ) :
        (∑ k : Fin n, min 1 (max 0 (t - (k.val : ℝ))) •
          (v (k.val + 1) - v k.val)) =
        ∑ k ∈ Finset.range n, min 1 (max 0 (t - (k : ℝ))) • (v (k + 1) - v k) := by
      rw [← Fin.sum_univ_eq_sum_range]
    rw [hsum 0, hsum n]
    have hzero : ∑ k ∈ Finset.range n,
        min 1 (max 0 ((0 : ℝ) - k)) • (v (k + 1) - v k) = 0 := by
      apply Finset.sum_eq_zero
      intro k hk
      simp
    rw [hzero, add_zero]
    have hall : ∑ k ∈ Finset.range n,
        min 1 (max 0 ((n : ℝ) - k)) • (v (k + 1) - v k) = v n - v 0 := by
      calc
        _ = ∑ k ∈ Finset.range n, (v (k + 1) - v k) := by
          apply Finset.sum_congr rfl
          intro k hk
          have hkn : k < n := Finset.mem_range.mp hk
          have hcast : ((k + 1 : ℕ) : ℝ) ≤ (n : ℝ) := by
            exact_mod_cast (Nat.succ_le_iff.mpr hkn)
          have hone : (1 : ℝ) ≤ (n : ℝ) - k := by
            push_cast at hcast
            linarith
          rw [max_eq_right (by positivity : (0 : ℝ) ≤ (n : ℝ) - k), min_eq_left hone]
          simp
        _ = v n - v 0 := Finset.sum_range_sub v n
    rw [hall]
    have hvclosed : v 0 = v n := by
      simpa only [v, min_eq_left (Nat.zero_le n), min_self] using
        congrArg (fun x : ℝ^2 => x.ofLp) cert.closed
    rw [hvclosed]
    abel
  · intro i s
    simp only [f]
    have hsum :
        (∑ k : Fin n, min 1 (max 0 ((i.val : ℝ) + (s : ℝ) - (k.val : ℝ))) •
          (v (k.val + 1) - v k.val)) =
        ∑ k ∈ Finset.range n,
          min 1 (max 0 ((i.val : ℝ) + (s : ℝ) - (k : ℝ))) • (v (k + 1) - v k) := by
      rw [← Fin.sum_univ_eq_sum_range]
    rw [hsum]
    have hin : i.val + 1 ≤ n := Nat.succ_le_iff.mpr i.isLt
    rw [← Finset.sum_range_add_sum_Ico _ hin, Finset.sum_range_succ]
    have hbefore : ∑ k ∈ Finset.range i.val,
        min 1 (max 0 ((i.val : ℝ) + (s : ℝ) - k)) • (v (k + 1) - v k) =
          v i.val - v 0 := by
      calc
        _ = ∑ k ∈ Finset.range i.val, (v (k + 1) - v k) := by
          apply Finset.sum_congr rfl
          intro k hk
          have hki : k < i.val := Finset.mem_range.mp hk
          have hone : (1 : ℝ) ≤ (i.val : ℝ) + (s : ℝ) - k := by
            have hs0 : (0 : ℝ) ≤ s := s.2.1
            have hsucc : (k : ℝ) + 1 ≤ (i.val : ℝ) := by
              exact_mod_cast (Nat.succ_le_iff.mpr hki)
            linarith
          rw [max_eq_right (by linarith : (0 : ℝ) ≤ (i.val : ℝ) + (s : ℝ) - k),
            min_eq_left hone]
          simp
        _ = v i.val - v 0 := Finset.sum_range_sub v i.val
    rw [hbefore]
    have hcurrent :
        min 1 (max 0 ((i.val : ℝ) + (s : ℝ) - i.val)) = (s : ℝ) := by
      rw [show (i.val : ℝ) + (s : ℝ) - i.val = s by ring,
        max_eq_right s.2.1, min_eq_right s.2.2.le]
    rw [hcurrent]
    have hafter : ∑ k ∈ Finset.Ico (i.val + 1) n,
        min 1 (max 0 ((i.val : ℝ) + (s : ℝ) - k)) • (v (k + 1) - v k) = 0 := by
      apply Finset.sum_eq_zero
      intro k hk
      have hik : i.val + 1 ≤ k := (Finset.mem_Ico.mp hk).1
      have hs1 : (s : ℝ) < 1 := s.2.2
      have hik_real : (i.val : ℝ) + 1 ≤ (k : ℝ) := by exact_mod_cast hik
      have hle : (i.val : ℝ) + (s : ℝ) - k ≤ 0 := by linarith
      rw [max_eq_left hle, min_eq_right zero_le_one, zero_smul]
    rw [hafter, add_zero]
    have hvi : v i.val = (cert.vertex i.castSucc).ofLp := by
      simp only [v, min_eq_left (Nat.le_of_lt i.isLt)]
      congr 2
    have hvis : v (i.val + 1) = (cert.vertex i.succ).ofLp := by
      simp only [v, min_eq_left hin]
      congr 2
    rw [hvi, hvis]
    rw [Path.segment_apply, AffineMap.lineMap_apply_module,
      WithLp.ofLp_add, WithLp.ofLp_smul, WithLp.ofLp_smul]
    module

/--
There is a continuous parametrization of a certified polygonal cycle on the additive circle
whose restriction to each half-open unit interval is the corresponding affine edge path.
-/
@[category API, AMS 52]
theorem Erdos1084.exists_polygonalCircleMap_edgewise
    {n : ℕ} (cert : Erdos1084.PolygonalCycleCertificate n) :
    ∃ loop : ContinuousMap (AddCircle (n : ℝ)) (Fin 2 → ℝ),
      ∀ (i : Fin n) (s : Set.Ico (0 : ℝ) 1),
        loop (((i.val : ℝ) + (s : ℝ) : ℝ) : AddCircle (n : ℝ)) =
          Path.segment (cert.vertex i.castSucc) (cert.vertex i.succ)
            (⟨(s : ℝ), s.2.1, s.2.2.le⟩ : Set.Icc (0 : ℝ) 1) := by
  rcases Erdos1084.exists_polygonalPeriodMap_edgewise cert with
    ⟨f, hfcont, hfseam, hfedge⟩
  have hnpos_nat : 0 < n := by
    have hthree : 3 ≤ n := cert.three_le
    omega
  have hnpos : 0 < (n : ℝ) := by exact_mod_cast hnpos_nat
  letI : Fact (0 < (n : ℝ)) := ⟨hnpos⟩
  let loop : ContinuousMap (AddCircle (n : ℝ)) (Fin 2 → ℝ) :=
    ⟨AddCircle.liftIco (n : ℝ) 0 f,
      AddCircle.liftIco_zero_continuous hfseam hfcont⟩
  refine ⟨loop, ?_⟩
  intro i s
  have hmem : (i.val : ℝ) + (s : ℝ) ∈ Set.Ico (0 : ℝ) (n : ℝ) := by
    constructor
    · exact add_nonneg (Nat.cast_nonneg _) s.2.1
    · have hi : (i.val : ℝ) + 1 ≤ (n : ℝ) := by
        exact_mod_cast (Nat.succ_le_iff.mpr i.isLt)
      linarith [s.2.2]
  rw [show loop (((i.val : ℝ) + (s : ℝ) : ℝ) : AddCircle (n : ℝ)) =
      f ((i.val : ℝ) + (s : ℝ)) by
        exact AddCircle.liftIco_zero_coe_apply hmem]
  exact hfedge i s

/--
An edgewise polygonal parametrization on the additive circle is globally injective.
-/
@[category API, AMS 52]
theorem Erdos1084.polygonalCircleMap_injective_of_edgewise
    {n : ℕ} (cert : Erdos1084.PolygonalCycleCertificate n)
    (loop : ContinuousMap (AddCircle (n : ℝ)) (Fin 2 → ℝ))
    (hloop :
      ∀ (i : Fin n) (s : Set.Ico (0 : ℝ) 1),
        loop (((i.val : ℝ) + (s : ℝ) : ℝ) : AddCircle (n : ℝ)) =
          Path.segment (cert.vertex i.castSucc) (cert.vertex i.succ)
            (⟨(s : ℝ), s.2.1, s.2.2.le⟩ : Set.Icc (0 : ℝ) 1)) :
    Function.Injective loop := by
  have hthree : 3 ≤ n := cert.three_le
  have hnpos_nat : 0 < n := by omega
  have hnpos : 0 < (n : ℝ) := by exact_mod_cast hnpos_nat
  letI : Fact (0 < (n : ℝ)) := ⟨hnpos⟩
  intro x y hxy
  rcases AddCircle.eq_coe_Ico x with ⟨rx, hrx, rfl⟩
  rcases AddCircle.eq_coe_Ico y with ⟨ry, hry, rfl⟩
  let i : Fin n := ⟨⌊rx⌋₊, (Nat.floor_lt hrx.1).2 hrx.2⟩
  let j : Fin n := ⟨⌊ry⌋₊, (Nat.floor_lt hry.1).2 hry.2⟩
  let s : Set.Ico (0 : ℝ) 1 := ⟨rx - i.val, by
    constructor
    · simpa [i] using sub_nonneg.mpr (Nat.floor_le hrx.1)
    · simpa [i, sub_lt_iff_lt_add, add_comm] using Nat.lt_floor_add_one rx⟩
  let t : Set.Ico (0 : ℝ) 1 := ⟨ry - j.val, by
    constructor
    · simpa [j] using sub_nonneg.mpr (Nat.floor_le hry.1)
    · simpa [j, sub_lt_iff_lt_add, add_comm] using Nat.lt_floor_add_one ry⟩
  have hrx_eq : rx = (i.val : ℝ) + s := by simp [s]
  have hry_eq : ry = (j.val : ℝ) + t := by simp [t]
  have hedge :
      Path.segment (cert.vertex i.castSucc) (cert.vertex i.succ)
          (⟨(s : ℝ), s.2.1, s.2.2.le⟩ : Set.Icc (0 : ℝ) 1) =
        Path.segment (cert.vertex j.castSucc) (cert.vertex j.succ)
          (⟨(t : ℝ), t.2.1, t.2.2.le⟩ : Set.Icc (0 : ℝ) 1) := by
    have hxy' := hxy
    rw [hrx_eq, hry_eq, hloop i s, hloop j t] at hxy'
    exact WithLp.ofLp_injective 2 hxy'
  by_cases hij : i = j
  · rw [hij] at hedge
    have hst :
        (⟨(s : ℝ), s.2.1, s.2.2.le⟩ : Set.Icc (0 : ℝ) 1) =
          ⟨(t : ℝ), t.2.1, t.2.2.le⟩ := cert.edgePath_injective j hedge
    have hst' : (s : ℝ) = t :=
      congrArg (fun u : Set.Icc (0 : ℝ) 1 => (u : ℝ)) hst
    have hijval : i.val = j.val := congrArg Fin.val hij
    have hrxy : rx = ry := by rw [hrx_eq, hry_eq, hijval, hst']
    exact congrArg (fun z : ℝ => (z : AddCircle (n : ℝ))) hrxy
  · rcases Erdos1084.distinct_edge_eq_imp_cyclic_incidence cert hij hedge with h | h
    · have hs : (s : ℝ) = 1 := congrArg Subtype.val h.1
      exact ((ne_of_lt s.2.2) hs).elim
    · have ht : (t : ℝ) = 1 := congrArg Subtype.val h.2.1
      exact ((ne_of_lt t.2.2) ht).elim

/--
A certified polygonal cycle admits a continuous injective parametrization by the additive circle.
-/
@[category API, AMS 52]
theorem Erdos1084.exists_injective_polygonalCircleMap
    {n : ℕ} (cert : Erdos1084.PolygonalCycleCertificate n) :
    ∃ loop : ContinuousMap (AddCircle (n : ℝ)) (Fin 2 → ℝ),
      Function.Injective loop := by
  rcases Erdos1084.exists_polygonalCircleMap_edgewise cert with ⟨loop, hloop⟩
  exact ⟨loop,
    Erdos1084.polygonalCircleMap_injective_of_edgewise cert loop hloop⟩

/--
Every continuous injective parametrization by a positive-period additive circle can be
reparametrized by the standard circle without changing its range in the Euclidean plane.
-/
@[category API, AMS 52]
theorem Erdos1084.exists_standardCircle_parametrization
    {T : ℝ} [Fact (0 < T)]
    (loop : ContinuousMap (AddCircle T) (Fin 2 → ℝ))
    (hinj : Function.Injective loop) :
    ∃ r : Circle → EuclideanSpace ℝ (Fin 2),
      Continuous r ∧ Function.Injective r ∧
      Set.range r =
        Set.range (fun x ↦ WithLp.toLp 2 (loop x)) := by
  have hT : T ≠ 0 := ne_of_gt (Fact.out : 0 < T)
  let e : AddCircle T ≃ₜ Circle := AddCircle.homeomorphCircle hT
  let r : Circle → EuclideanSpace ℝ (Fin 2) :=
    fun z ↦ WithLp.toLp 2 (loop (e.symm z))
  refine ⟨r, ?_, ?_, ?_⟩
  · exact (PiLp.continuous_toLp 2 (fun _ : Fin 2 ↦ ℝ)).comp
      (loop.continuous.comp e.symm.continuous)
  · exact (WithLp.toLp_injective 2).comp (hinj.comp e.symm.injective)
  · apply Set.Subset.antisymm
    · rintro _ ⟨z, rfl⟩
      exact ⟨e.symm z, rfl⟩
    · rintro _ ⟨x, rfl⟩
      exact ⟨e x, by simp [r]⟩

/-- The exterior of a positive-radius closed ball in the Euclidean plane is path-connected. -/
@[category API, AMS 52]
theorem Erdos1084.exterior_isPathConnected (R : ℝ) (hR : 0 < R) :
    IsPathConnected {x : EuclideanSpace ℝ (Fin 2) | R < ‖x‖} := by
  rw [isPathConnected_iff]
  constructor
  · refine ⟨EuclideanSpace.single 0 (R + 1), ?_⟩
    have hR1 : 0 < R + 1 := by linarith
    simp [EuclideanSpace.norm_single, abs_of_pos hR1]
  · intro x hx y hy
    let q : ℝ := max ‖x‖ ‖y‖
    have hx0 : ‖x‖ ≠ 0 := ne_of_gt (hR.trans hx)
    have hy0 : ‖y‖ ≠ 0 := ne_of_gt (hR.trans hy)
    have hqx : ‖x‖ ≤ q := le_max_left _ _
    have hqy : ‖y‖ ≤ q := le_max_right _ _
    have hqR : R < q := hx.trans_le hqx
    let x' : EuclideanSpace ℝ (Fin 2) := (q / ‖x‖) • x
    let y' : EuclideanSpace ℝ (Fin 2) := (q / ‖y‖) • y
    have hq0 : 0 ≤ q := (norm_nonneg x).trans hqx
    have hx'norm : ‖x'‖ = q := by
      simp [x', norm_smul, hx0, hq0]
    have hy'norm : ‖y'‖ = q := by
      simp [y', norm_smul, hy0, hq0]
    have hxx' : JoinedIn {z : EuclideanSpace ℝ (Fin 2) | R < ‖z‖} x x' := by
      apply JoinedIn.of_segment_subset
      rw [segment_eq_image']
      rintro z ⟨t, ht, rfl⟩
      rcases ht with ⟨ht0, ht1⟩
      have hcoef : 1 ≤ 1 + t * (q / ‖x‖ - 1) := by
        have hdiv : 1 ≤ q / ‖x‖ :=
          (le_div_iff₀ (norm_pos_iff.mpr (norm_ne_zero_iff.mp hx0))).2 (by simpa using hqx)
        nlinarith
      change R < ‖x + t • (x' - x)‖
      rw [show x + t • (x' - x) = (1 + t * (q / ‖x‖ - 1)) • x by
        simp only [x']; module]
      rw [norm_smul, Real.norm_eq_abs, abs_of_nonneg (le_trans zero_le_one hcoef)]
      exact hx.trans_le (by simpa using
        mul_le_mul_of_nonneg_right hcoef (norm_nonneg x))
    have hyy' : JoinedIn {z : EuclideanSpace ℝ (Fin 2) | R < ‖z‖} y y' := by
      apply JoinedIn.of_segment_subset
      rw [segment_eq_image']
      rintro z ⟨t, ht, rfl⟩
      rcases ht with ⟨ht0, ht1⟩
      have hcoef : 1 ≤ 1 + t * (q / ‖y‖ - 1) := by
        have hdiv : 1 ≤ q / ‖y‖ :=
          (le_div_iff₀ (norm_pos_iff.mpr (norm_ne_zero_iff.mp hy0))).2 (by simpa using hqy)
        nlinarith
      change R < ‖y + t • (y' - y)‖
      rw [show y + t • (y' - y) = (1 + t * (q / ‖y‖ - 1)) • y by
        simp only [y']; module]
      rw [norm_smul, Real.norm_eq_abs, abs_of_nonneg (le_trans zero_le_one hcoef)]
      exact hy.trans_le (by simpa using
        mul_le_mul_of_nonneg_right hcoef (norm_nonneg y))
    have hsphere : IsPathConnected (Metric.sphere (0 : EuclideanSpace ℝ (Fin 2)) q) :=
      isPathConnected_sphere (by
        rw [← Module.finrank_eq_rank']
        norm_num) 0 hq0
    have hxy' : JoinedIn {z : EuclideanSpace ℝ (Fin 2) | R < ‖z‖} x' y' := by
      have hxmem : x' ∈ Metric.sphere (0 : EuclideanSpace ℝ (Fin 2)) q := by
        simpa [Metric.mem_sphere, dist_zero_right] using hx'norm
      have hymem : y' ∈ Metric.sphere (0 : EuclideanSpace ℝ (Fin 2)) q := by
        simpa [Metric.mem_sphere, dist_zero_right] using hy'norm
      apply (hsphere.joinedIn x' hxmem y' hymem).mono
      intro z hz
      have hznorm : ‖z‖ = q := by
        simpa [Metric.mem_sphere, dist_zero_right] using hz
      simpa [hznorm] using hqR
    exact hxx'.trans (hxy'.trans hyy'.symm)

set_option linter.unusedVariables false in
/--
In a partition of the Euclidean plane by a compact set and two disjoint open sets,
exactly one of the two open sets is bounded.
-/
@[category API, AMS 52]
theorem Erdos1084.jordanPartition_exactlyOne_bounded
    (C A B : Set (EuclideanSpace ℝ (Fin 2)))
    (hC : IsCompact C)
    (hAo : IsOpen A) (hBo : IsOpen B)
    (hAc : IsConnected A) (hBc : IsConnected B)
    (hAB : Disjoint A B) (hAC : Disjoint A C) (hBC : Disjoint B C)
    (hcover : A ∪ B ∪ C = Set.univ) :
    (Bornology.IsBounded A ∧ ¬ Bornology.IsBounded B) ∨
    (Bornology.IsBounded B ∧ ¬ Bornology.IsBounded A) := by
  obtain ⟨R, hR, hCR⟩ := hC.isBounded.subset_closedBall_lt 0 0
  let E : Set (EuclideanSpace ℝ (Fin 2)) := {x | R < ‖x‖}
  have hEconn : IsConnected E :=
    (Erdos1084.exterior_isPathConnected R hR).isConnected
  have hEcover : E ⊆ A ∪ B := by
    intro x hx
    have hxcover : x ∈ A ∪ B ∪ C := by
      rw [hcover]
      exact Set.mem_univ x
    rcases hxcover with hxAB | hxC
    · exact hxAB
    · exact False.elim ((not_le_of_gt hx) (by
        simpa [Metric.mem_closedBall, dist_zero_right] using hCR hxC))
  have hEunbounded : ¬ Bornology.IsBounded E := by
    intro hEb
    have hunion : E ∪ Metric.closedBall (0 : EuclideanSpace ℝ (Fin 2)) R = Set.univ := by
      ext x
      simp only [E, Set.mem_union, Set.mem_setOf_eq, Metric.mem_closedBall,
        dist_zero_right, Set.mem_univ, iff_true]
      exact lt_or_ge R ‖x‖
    apply NormedSpace.unbounded_univ ℝ (EuclideanSpace ℝ (Fin 2))
    rw [← hunion]
    exact hEb.union Metric.isBounded_closedBall
  rcases hEconn.isPreconnected.subset_or_subset hAo hBo hAB hEcover with hEA | hEB
  · right
    constructor
    · have hBsub : B ⊆ Metric.closedBall (0 : EuclideanSpace ℝ (Fin 2)) R := by
        intro x hxB
        show dist x 0 ≤ R
        by_cases hnorm : ‖x‖ ≤ R
        · simpa only [dist_zero_right] using hnorm
        · have hxE : x ∈ E := by
            exact lt_of_not_ge hnorm
          exact False.elim (Set.disjoint_left.1 hAB (hEA hxE) hxB)
      exact Metric.isBounded_closedBall.subset hBsub
    · exact fun hAb ↦ hEunbounded (hAb.subset hEA)
  · left
    constructor
    · have hAsub : A ⊆ Metric.closedBall (0 : EuclideanSpace ℝ (Fin 2)) R := by
        intro x hxA
        show dist x 0 ≤ R
        by_cases hnorm : ‖x‖ ≤ R
        · simpa only [dist_zero_right] using hnorm
        · have hxE : x ∈ E := by
            exact lt_of_not_ge hnorm
          exact False.elim (Set.disjoint_left.1 hAB hxA (hEB hxE))
      exact Metric.isBounded_closedBall.subset hAsub
    · exact fun hBb ↦ hEunbounded (hBb.subset hEB)

/--
Distinct edges of a cycle in a straight-line plane drawing meet only at endpoints common
to both edges.
-/
@[category API, AMS 52]
theorem Erdos1084.StraightLinePlaneDrawing.isCycle_polygonal_simple
    {V : Type*} {G : SimpleGraph V}
    (D : Erdos1084.StraightLinePlaneDrawing G)
    {v : V} (c : G.Walk v v) (hc : c.IsCycle) :
    ∀ (i j : Fin c.darts.length), i ≠ j →
      segment ℝ (D.p (c.darts.get i).fst) (D.p (c.darts.get i).snd) ∩
          segment ℝ (D.p (c.darts.get j).fst) (D.p (c.darts.get j).snd) ⊆
        ({D.p (c.darts.get i).fst, D.p (c.darts.get i).snd} : Set (ℝ^2)) ∩
          ({D.p (c.darts.get j).fst, D.p (c.darts.get j).snd} : Set (ℝ^2)) := by
  intro i j hij
  apply D.edge_segments_inter_subset_common_endpoints
  · exact (c.darts.get i).adj
  · exact (c.darts.get j).adj
  · intro hedges
    apply hij
    apply Fin.ext
    have hi : i.val < c.edges.length := by
      simpa [SimpleGraph.Walk.edges] using i.isLt
    have hj : j.val < c.edges.length := by
      simpa [SimpleGraph.Walk.edges] using j.isLt
    apply (hc.isTrail.edges_nodup.getElem_inj_iff (hi := hi) (hj := hj)).mp
    simp only [SimpleGraph.Walk.edges, List.getElem_map]
    exact hedges

/--
The nonterminal vertices of a cycle have distinct images in a straight-line plane drawing.
-/
@[category API, AMS 52]
theorem Erdos1084.StraightLinePlaneDrawing.isCycle_vertex_injective
    {V : Type*} {G : SimpleGraph V}
    (D : Erdos1084.StraightLinePlaneDrawing G)
    {v : V} (c : G.Walk v v) (hc : c.IsCycle) :
    Function.Injective (fun i : Fin c.length => D.p (c.getVert i)) := by
  intro i j hij
  apply Fin.ext
  apply hc.getVert_injOn'
  · simp only [Set.mem_setOf_eq]
    omega
  · simp only [Set.mem_setOf_eq]
    omega
  · exact D.p.injective hij

/--
A graph cycle in a straight-line plane drawing determines a finite simple polygonal-cycle
certificate whose ordered vertices are the images of the walk's ordered vertices.
-/
@[category API, AMS 52]
theorem Erdos1084.StraightLinePlaneDrawing.isCycle_polygonalCertificate
    {V : Type*} {G : SimpleGraph V}
    (D : Erdos1084.StraightLinePlaneDrawing G)
    {v : V} (c : G.Walk v v) (hc : c.IsCycle) :
    ∃ cert : Erdos1084.PolygonalCycleCertificate c.length,
      cert.vertex = fun i : Fin (c.length + 1) => D.p (c.getVert i) := by
  let vertex : Fin (c.length + 1) → ℝ^2 := fun i => D.p (c.getVert i)
  refine ⟨{
    three_le := hc.three_le_length
    vertex := vertex
    closed := ?_
    vertex_injective := ?_
    carrier := ⋃ i : Fin c.length,
      Set.range (Path.segment (vertex i.castSucc) (vertex i.succ))
    carrier_eq := rfl
    edge_inter_subset_common_endpoints := ?_
  }, rfl⟩
  · exact congrArg D.p (c.getVert_zero.trans c.getVert_length.symm)
  · simpa only [vertex] using D.isCycle_vertex_injective c hc
  · intro i j hij
    let i' : Fin c.darts.length := Fin.cast c.length_darts.symm i
    let j' : Fin c.darts.length := Fin.cast c.length_darts.symm j
    have hij' : i' ≠ j' := by
      intro h
      apply hij
      apply Fin.ext
      have hv : i'.val = j'.val :=
        congrArg (fun k : Fin c.darts.length => k.val) h
      simpa only [i', j', Fin.val_cast] using hv
    have h := D.isCycle_polygonal_simple c hc i' j' hij'
    have hi_get := c.darts_getElem_eq_getVert i'.val i'.isLt
    have hj_get := c.darts_getElem_eq_getVert j'.val j'.isLt
    simp only [List.get_eq_getElem] at h
    rw [hi_get, hj_get] at h
    simpa only [vertex, i', j', Fin.val_cast, Fin.val_succ, Fin.val_castSucc] using h

/--
The triangular-lattice lower construction for Erdős Problem 1084: for
`3n^2 + 3n + 1` planar `1`-separated points, one can realize at least
`9n^2 + 3n` unit-distance pairs.
-/
@[category API, AMS 52]
theorem Erdos1084.erdos_1084.variants.triangular_optimal_d2_lower (n : ℕ) :
    9 * n ^ 2 + 3 * n ≤ f 2 (3 * n ^ 2 + 3 * n + 1) := by
  exact Erdos1084.erdos_1084.variants.triangular_optimal_d2_lower_of_certificate n
    (Erdos1084.erdos_1084.variants.triangular_lower_certificate n)

/--
Conditional triangular-lattice upper bound obtained directly from Harborth's source theorem
in the repository's `unitDistNum` convention.
-/
@[category API, AMS 52]
theorem Erdos1084.erdos_1084.variants.triangular_optimal_d2_upper_of_unitDistNum_source
    (hHarborth : Erdos1084.HarborthUnitDistNumUpperGe4Source)
    {n : ℕ} (hn : 1 ≤ n) :
    Erdos1084.f 2 (3 * n ^ 2 + 3 * n + 1) ≤ 9 * n ^ 2 + 3 * n := by
  have hN : 4 ≤ 3 * n ^ 2 + 3 * n + 1 := by
    have hn_sq : 1 ≤ n ^ 2 := by
      nlinarith [Nat.mul_le_mul hn hn]
    nlinarith
  unfold Erdos1084.f
  refine ciSup_le' ?_
  intro s
  refine ciSup_le' ?_
  intro hcard
  refine ciSup_le' ?_
  intro hsep
  have hbound :=
    hHarborth (3 * n ^ 2 + 3 * n + 1) hN s hcard hsep
  rwa [Erdos1084.triangular_harborth_floor n] at hbound

/--
Conditional triangular-lattice upper bound obtained from Harborth's source theorem in the
`2`-separated contact convention.
-/
@[category API, AMS 52]
theorem Erdos1084.erdos_1084.variants.triangular_optimal_d2_upper_of_twoSeparated_contact_source
    (hHarborth : Erdos1084.HarborthTwoSeparatedContactUpperGe4Source)
    {n : ℕ} (hn : 1 ≤ n) :
    Erdos1084.f 2 (3 * n ^ 2 + 3 * n + 1) ≤ 9 * n ^ 2 + 3 * n := by
  have hUnit : Erdos1084.HarborthUnitDistNumUpperGe4Source :=
    Erdos1084.harborth_unitDistNum_upper_ge4_of_twoSeparated_contact_source hHarborth
  exact Erdos1084.erdos_1084.variants.triangular_optimal_d2_upper_of_unitDistNum_source
    hUnit hn

namespace Erdos1084
variable {n : ℕ}

-- TODO: Add erdos_1084.

/-- It is easy to check that $f_1(n) = n - 1$. -/
@[category research solved, AMS 52]
theorem erdos_1084.variants.upper_d1 : f 1 n = n - 1 := by
  sorry

/-- It is easy to check that $f_2(n) < 3n$. -/
@[category research solved, AMS 52]
theorem erdos_1084.variants.easy_upper_d2 (hn : n ≠ 0) : f 2 n < 3 * n := by
  sorry

/-- Erdős showed that there is some constant $c > 0$ such that $f_2(n) < 3n - c n^{1/2}$. -/
@[category research solved, AMS 52]
theorem erdos_1084.variants.upper_d2 : ∃ c > (0 : ℝ), ∀ n > 0, f 2 n < 3 * n - c * sqrt n := by
  sorry

/-- Erdős conjectured that the triangular lattice is best possible in 2D, in particular that
$f_2(3n^2 + 3n + 1) < 9n^2 + 3n$.

Note: in [Er75f] is read $9n^2 + 6n$, but this seems to be a typo.
-/
@[category research open, AMS 52]
theorem erdos_1084.variants.triangular_optimal_d2 : f 2 (3 * n ^ 2 + 3 * n + 1) = 9 * n ^ 2 + 3 * n := by
  sorry

/--
Conditional wrapper for the triangular-lattice optimality statement under the explicit
Harborth `unitDistNum` source theorem.
-/
@[category API, AMS 52]
theorem erdos_1084.variants.triangular_optimal_d2_final_of_unitDistNum_source
    (hHarborth : HarborthUnitDistNumUpperGe4Source)
    (n : ℕ) :
    f 2 (3 * n ^ 2 + 3 * n + 1) = 9 * n ^ 2 + 3 * n := by
  by_cases hn0 : n = 0
  · subst n
    simpa using Erdos1084.f_two_one_eq_zero
  · have hn : 1 ≤ n := Nat.succ_le_of_lt (Nat.pos_of_ne_zero hn0)
    exact le_antisymm
      (Erdos1084.erdos_1084.variants.triangular_optimal_d2_upper_of_unitDistNum_source
        hHarborth hn)
      (Erdos1084.erdos_1084.variants.triangular_optimal_d2_lower n)

/--
All-`n` conditional form of the triangular-lattice optimality statement under
Harborth's `unitDistNum` source theorem.
-/
@[category API, AMS 52]
theorem erdos_1084.variants.triangular_optimal_d2_all_final_of_unitDistNum_source
    (hHarborth : HarborthUnitDistNumUpperGe4Source) :
    ∀ n : ℕ, f 2 (3 * n ^ 2 + 3 * n + 1) = 9 * n ^ 2 + 3 * n := by
  intro n
  exact erdos_1084.variants.triangular_optimal_d2_final_of_unitDistNum_source
    hHarborth n

/--
Conditional wrapper for the triangular-lattice optimality statement under the explicit
Harborth `2`-separated contact-number source theorem.
-/
@[category API, AMS 52]
theorem erdos_1084.variants.triangular_optimal_d2_final_of_harborth_source
    (hHarborth : HarborthTwoSeparatedContactUpperGe4Source)
    (n : ℕ) :
    f 2 (3 * n ^ 2 + 3 * n + 1) = 9 * n ^ 2 + 3 * n := by
  by_cases hn0 : n = 0
  · subst n
    simpa using Erdos1084.f_two_one_eq_zero
  · have hn : 1 ≤ n := Nat.succ_le_of_lt (Nat.pos_of_ne_zero hn0)
    exact le_antisymm
      (Erdos1084.erdos_1084.variants.triangular_optimal_d2_upper_of_twoSeparated_contact_source
        hHarborth hn)
      (Erdos1084.erdos_1084.variants.triangular_optimal_d2_lower n)

/--
All-`n` conditional form of the triangular-lattice optimality statement under
Harborth's `2`-separated contact-number source theorem.
-/
@[category API, AMS 52]
theorem erdos_1084.variants.triangular_optimal_d2_all_final_of_harborth_source
    (hHarborth : HarborthTwoSeparatedContactUpperGe4Source) :
    ∀ n : ℕ, f 2 (3 * n ^ 2 + 3 * n + 1) = 9 * n ^ 2 + 3 * n := by
  intro n
  exact erdos_1084.variants.triangular_optimal_d2_final_of_harborth_source
    hHarborth n

/-- Erdős claims the existence of two constants $c_1, c_2 > 0$
such that $6n - c_1 n^{2/3} ≤ f_3(n) \le 6n - c_2 n^{2/3}$. -/
@[category research solved, AMS 52]
theorem erdos_1084.variants.upper_lower_d3 :
    ∃ c₁ : ℝ, ∃ c₂ > (0 : ℝ), ∀ᶠ n in atTop,
      6 * n - c₁ * n ^ (2 / 3 : ℝ) ≤ f 3 n ∧ f 3 n ≤ 6 * n - c₂ * n ^ (2 / 3 : ℝ) := by
  sorry

end Erdos1084
