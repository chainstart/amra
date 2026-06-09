import Mathlib.Data.ZMod.Basic
import Mathlib.Algebra.Field.ZMod
import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Data.Nat.Totient
import Mathlib.RingTheory.IntegralDomain
import Mathlib.Algebra.Polynomial.Roots
import Mathlib.Algebra.BigOperators.Intervals
import Mathlib.Tactic.Ring

namespace OeisA357513NextRound20260606

open scoped BigOperators

syntax (name := finsetProdInCompat) "∏ " ident " in " term ", " term : term
macro_rules
  | `(∏ $x:ident in $s:term, $body:term) => `(Finset.prod $s (fun $x => $body))

syntax (name := finsetSumInCompat) "∑ " ident " in " term ", " term : term
macro_rules
  | `(∑ $x:ident in $s:term, $body:term) => `(Finset.sum $s (fun $x => $body))

lemma zmod_nat_cast_mul_self_eq_zero_mod_square (p : ℕ) :
    ((p * p : ℕ) : ZMod (p ^ 2)) = 0 := by
  rw [ZMod.natCast_eq_zero_iff]
  simp [pow_two]

lemma zmod_nat_cast_self_sq_eq_zero_mod_square (p : ℕ) :
    ((p : ZMod (p ^ 2)) ^ 2) = 0 := by
  simpa [pow_two, Nat.cast_mul] using zmod_nat_cast_mul_self_eq_zero_mod_square p

lemma zmod_range_coprime_mod_square (p k : ℕ)
    (hp : p.Prime) (hk1 : 1 ≤ k) (hkp : k ≤ p - 1) :
    Nat.Coprime k (p ^ 2) := by
  have hklt : k < p := by
    exact lt_of_le_of_lt hkp (Nat.sub_one_lt (Nat.ne_of_gt hp.pos))
  have hnot : ¬ p ∣ k := Nat.not_dvd_of_pos_of_lt hk1 hklt
  simpa using hp.coprime_pow_of_not_dvd (m := 2) hnot

lemma zmod_range_coprime_mod_fourth_power (p k : ℕ)
    (hp : p.Prime) (hk1 : 1 ≤ k) (hkp : k ≤ p - 1) :
    Nat.Coprime k (p ^ 4) := by
  have hklt : k < p := by
    exact lt_of_le_of_lt hkp (Nat.sub_one_lt (Nat.ne_of_gt hp.pos))
  have hnot : ¬ p ∣ k := Nat.not_dvd_of_pos_of_lt hk1 hklt
  simpa using hp.coprime_pow_of_not_dvd (m := 4) hnot

lemma zmod_unit_denominator_for_range
    (p k : ℕ) (hp : p.Prime) (hk1 : 1 ≤ k) (hkp : k ≤ p - 1) :
    IsUnit (k : ZMod (p ^ 4)) := by
  rw [ZMod.isUnit_iff_coprime]
  exact zmod_range_coprime_mod_fourth_power p k hp hk1 hkp

lemma zmod_p_minus_one_choose_factor_expansion_mod_p4_aux
    (p k : ℕ) (hp : p.Prime) (hkp : k ≤ p - 1) :
    let R := ZMod (p ^ 4)
    (((p - 1).choose k : R)) =
      (-1 : R) ^ k *
        Finset.prod (Finset.Icc 1 k)
          (fun j => 1 - (p : R) * (j : R)⁻¹) := by
  induction k with
  | zero =>
      simp
  | succ k ih =>
      let R := ZMod (p ^ 4)
      change (((p - 1).choose (k + 1) : R)) =
        (-1 : R) ^ (k + 1) *
          Finset.prod (Finset.Icc 1 (k + 1))
            (fun j => 1 - (p : R) * (j : R)⁻¹)
      have hk_le : k ≤ p - 1 := le_trans (Nat.le_succ k) hkp
      have ih' := ih hk_le
      change (((p - 1).choose k : R)) =
        (-1 : R) ^ k *
          Finset.prod (Finset.Icc 1 k)
            (fun j => 1 - (p : R) * (j : R)⁻¹) at ih'
      have hunit : IsUnit (((k + 1 : ℕ) : R)) :=
        zmod_unit_denominator_for_range p (k + 1) hp (Nat.succ_pos k) hkp
      have hrec :
          (((p - 1).choose (k + 1) : R) * ((k + 1 : ℕ) : R)) =
            ((p - 1).choose k : R) * ((p - 1 - k : ℕ) : R) := by
        simpa [Nat.cast_mul] using
          congrArg (fun n : ℕ => (n : R)) (Nat.choose_succ_right_eq (p - 1) k)
      have hcancel :
          (((p - 1).choose (k + 1) : R)) =
            (((p - 1).choose k : R) * ((p - 1 - k : ℕ) : R)) *
              (((k + 1 : ℕ) : R)⁻¹) := by
        calc
          (((p - 1).choose (k + 1) : R))
              = (((p - 1).choose (k + 1) : R)) *
                  (((k + 1 : ℕ) : R) * (((k + 1 : ℕ) : R)⁻¹)) := by
                rw [ZMod.mul_inv_of_unit _ hunit, mul_one]
          _ = (((p - 1).choose (k + 1) : R) * ((k + 1 : ℕ) : R)) *
                  (((k + 1 : ℕ) : R)⁻¹) := by
                rw [mul_assoc]
          _ = (((p - 1).choose k : R) * ((p - 1 - k : ℕ) : R)) *
                  (((k + 1 : ℕ) : R)⁻¹) := by
                rw [hrec]
      have hkp' : k + 1 ≤ p := by
        exact le_trans hkp (Nat.sub_le p 1)
      have hfactor :
          ((p - 1 - k : ℕ) : R) * (((k + 1 : ℕ) : R)⁻¹) =
            (-1 : R) *
              (1 - (p : R) * (((k + 1 : ℕ) : R)⁻¹)) := by
        have hsub_nat : p - 1 - k = p - (k + 1) := by
          rw [Nat.sub_sub, Nat.add_comm]
        have hcast : ((p - 1 - k : ℕ) : R) = (p : R) - ((k + 1 : ℕ) : R) := by
          rw [hsub_nat]
          exact Nat.cast_sub hkp'
        have hmul : ((k + 1 : ℕ) : R) * (((k + 1 : ℕ) : R)⁻¹) = 1 :=
          ZMod.mul_inv_of_unit _ hunit
        calc
          ((p - 1 - k : ℕ) : R) * (((k + 1 : ℕ) : R)⁻¹)
              = ((p : R) - ((k + 1 : ℕ) : R)) *
                  (((k + 1 : ℕ) : R)⁻¹) := by
                rw [hcast]
          _ = (p : R) * (((k + 1 : ℕ) : R)⁻¹) -
                  ((k + 1 : ℕ) : R) * (((k + 1 : ℕ) : R)⁻¹) := by
                rw [sub_mul]
          _ = (p : R) * (((k + 1 : ℕ) : R)⁻¹) - 1 := by
                rw [hmul]
          _ = (-1 : R) *
                (1 - (p : R) * (((k + 1 : ℕ) : R)⁻¹)) := by
                rw [neg_one_mul, neg_sub]
      calc
        (((p - 1).choose (k + 1) : R))
            = (((p - 1).choose k : R) * ((p - 1 - k : ℕ) : R)) *
                (((k + 1 : ℕ) : R)⁻¹) := hcancel
        _ = (((p - 1).choose k : R)) *
              (((p - 1 - k : ℕ) : R) * (((k + 1 : ℕ) : R)⁻¹)) := by
              rw [mul_assoc]
        _ = ((-1 : R) ^ k *
              Finset.prod (Finset.Icc 1 k)
                (fun j => 1 - (p : R) * (j : R)⁻¹)) *
              ((-1 : R) *
                (1 - (p : R) * (((k + 1 : ℕ) : R)⁻¹))) := by
              rw [ih', hfactor]
        _ = (-1 : R) ^ (k + 1) *
              Finset.prod (Finset.Icc 1 (k + 1))
                (fun j => 1 - (p : R) * (j : R)⁻¹) := by
              have hpow : (-1 : R) ^ (k + 1) = (-1 : R) ^ k * (-1 : R) := by
                rw [pow_succ]
              rw [Finset.prod_Icc_succ_top (Nat.succ_pos k), hpow]
              ac_rfl

lemma zmod_p_minus_one_choose_factor_expansion_mod_p4
    (p k : ℕ) (hp : p.Prime) (hk1 : 1 ≤ k) (hkp : k ≤ p - 1) :
    let R := ZMod (p ^ 4)
    (((p - 1).choose k : R)) =
      (-1 : R) ^ k *
        Finset.prod (Finset.Icc 1 k)
          (fun j => 1 - (p : R) * (j : R)⁻¹) := by
  have _ := hk1
  exact zmod_p_minus_one_choose_factor_expansion_mod_p4_aux p k hp hkp

lemma zmod_p_add_choose_factor_expansion_mod_p4_aux
    (p t : ℕ) (hp : p.Prime) (ht : t + 1 ≤ p - 1) :
    let R := ZMod (p ^ 4)
    (((p + t).choose (t + 1) : R)) =
      (p : R) * (((t + 1 : ℕ) : R)⁻¹) *
        Finset.prod (Finset.Icc 1 t)
          (fun j => 1 + (p : R) * (j : R)⁻¹) := by
  induction t with
  | zero =>
      simp
  | succ t ih =>
      let R := ZMod (p ^ 4)
      change (((p + (t + 1)).choose ((t + 1) + 1) : R)) =
        (p : R) * ((((t + 1) + 1 : ℕ) : R)⁻¹) *
          Finset.prod (Finset.Icc 1 (t + 1))
            (fun j => 1 + (p : R) * (j : R)⁻¹)
      have ht_prev : t + 1 ≤ p - 1 := le_trans (Nat.le_succ (t + 1)) ht
      have ih' := ih ht_prev
      change (((p + t).choose (t + 1) : R)) =
        (p : R) * (((t + 1 : ℕ) : R)⁻¹) *
          Finset.prod (Finset.Icc 1 t)
            (fun j => 1 + (p : R) * (j : R)⁻¹) at ih'
      have hunit_prev : IsUnit (((t + 1 : ℕ) : R)) :=
        zmod_unit_denominator_for_range p (t + 1) hp (Nat.succ_pos t) ht_prev
      have hunit_next : IsUnit ((((t + 1) + 1 : ℕ) : R)) :=
        zmod_unit_denominator_for_range p ((t + 1) + 1) hp (Nat.succ_pos (t + 1)) ht
      have hrec :
          (((p + (t + 1)).choose ((t + 1) + 1) : R) *
              (((t + 1) + 1 : ℕ) : R)) =
            ((p + t).choose (t + 1) : R) * (((p + t) + 1 : ℕ) : R) := by
        simpa [Nat.cast_mul, Nat.add_assoc, mul_comm, mul_left_comm, mul_assoc] using
          (congrArg (fun n : ℕ => (n : R)) (Nat.add_one_mul_choose_eq (p + t) (t + 1))).symm
      have hcancel :
          (((p + (t + 1)).choose ((t + 1) + 1) : R)) =
            (((p + t).choose (t + 1) : R) * (((p + t) + 1 : ℕ) : R)) *
              ((((t + 1) + 1 : ℕ) : R)⁻¹) := by
        calc
          (((p + (t + 1)).choose ((t + 1) + 1) : R))
              = (((p + (t + 1)).choose ((t + 1) + 1) : R)) *
                  ((((t + 1) + 1 : ℕ) : R) *
                    ((((t + 1) + 1 : ℕ) : R)⁻¹)) := by
                rw [ZMod.mul_inv_of_unit _ hunit_next, mul_one]
          _ = (((p + (t + 1)).choose ((t + 1) + 1) : R) *
                  (((t + 1) + 1 : ℕ) : R)) *
                  ((((t + 1) + 1 : ℕ) : R)⁻¹) := by
                rw [mul_assoc]
          _ = (((p + t).choose (t + 1) : R) * (((p + t) + 1 : ℕ) : R)) *
                  ((((t + 1) + 1 : ℕ) : R)⁻¹) := by
                rw [hrec]
      have hfactor :
          (((t + 1 : ℕ) : R)⁻¹) * (((p + t) + 1 : ℕ) : R) =
            1 + (p : R) * (((t + 1 : ℕ) : R)⁻¹) := by
        have hcast : (((p + t) + 1 : ℕ) : R) = (p : R) + ((t + 1 : ℕ) : R) := by
          simp [Nat.cast_add, Nat.add_assoc]
        have hmul : (((t + 1 : ℕ) : R)⁻¹) * ((t + 1 : ℕ) : R) = 1 := by
          simpa [mul_comm] using ZMod.mul_inv_of_unit (((t + 1 : ℕ) : R)) hunit_prev
        calc
          (((t + 1 : ℕ) : R)⁻¹) * (((p + t) + 1 : ℕ) : R)
              = (((t + 1 : ℕ) : R)⁻¹) *
                  ((p : R) + ((t + 1 : ℕ) : R)) := by
                rw [hcast]
          _ = (((t + 1 : ℕ) : R)⁻¹) * (p : R) +
                  (((t + 1 : ℕ) : R)⁻¹) * ((t + 1 : ℕ) : R) := by
                rw [mul_add]
          _ = (((t + 1 : ℕ) : R)⁻¹) * (p : R) + 1 := by
                rw [hmul]
          _ = 1 + (p : R) * (((t + 1 : ℕ) : R)⁻¹) := by
                ac_rfl
      calc
        (((p + (t + 1)).choose ((t + 1) + 1) : R))
            = (((p + t).choose (t + 1) : R) * (((p + t) + 1 : ℕ) : R)) *
                ((((t + 1) + 1 : ℕ) : R)⁻¹) := hcancel
        _ = (((p : R) * (((t + 1 : ℕ) : R)⁻¹) *
              Finset.prod (Finset.Icc 1 t)
                (fun j => 1 + (p : R) * (j : R)⁻¹)) *
              (((p + t) + 1 : ℕ) : R)) *
                ((((t + 1) + 1 : ℕ) : R)⁻¹) := by
              rw [ih']
        _ = ((p : R) *
              (Finset.prod (Finset.Icc 1 t)
                (fun j => 1 + (p : R) * (j : R)⁻¹) *
                ((((t + 1 : ℕ) : R)⁻¹) * (((p + t) + 1 : ℕ) : R)))) *
                ((((t + 1) + 1 : ℕ) : R)⁻¹) := by
              ac_rfl
        _ = ((p : R) *
              (Finset.prod (Finset.Icc 1 t)
                (fun j => 1 + (p : R) * (j : R)⁻¹) *
                (1 + (p : R) * (((t + 1 : ℕ) : R)⁻¹)))) *
                ((((t + 1) + 1 : ℕ) : R)⁻¹) := by
              rw [hfactor]
        _ = (p : R) * ((((t + 1) + 1 : ℕ) : R)⁻¹) *
              Finset.prod (Finset.Icc 1 (t + 1))
                (fun j => 1 + (p : R) * (j : R)⁻¹) := by
              rw [Finset.prod_Icc_succ_top (Nat.succ_pos t)]
              ac_rfl

lemma zmod_p_minus_one_add_choose_factor_expansion_mod_p4
    (p k : ℕ) (hp : p.Prime) (hk1 : 1 ≤ k) (hkp : k ≤ p - 1) :
    let R := ZMod (p ^ 4)
    (((p - 1 + k).choose k : R)) =
      (p : R) * ((k : R)⁻¹) *
        Finset.prod (Finset.Icc 1 (k - 1))
          (fun j => 1 + (p : R) * (j : R)⁻¹) := by
  let R := ZMod (p ^ 4)
  have ht : (k - 1) + 1 ≤ p - 1 := by
    simpa [Nat.sub_add_cancel hk1] using hkp
  have htop : p + (k - 1) = p - 1 + k := by
    have hp1 : 1 ≤ p := Nat.succ_le_of_lt hp.pos
    calc
      p + (k - 1) = p + k - 1 := by
        rw [Nat.add_sub_assoc hk1 p]
      _ = p - 1 + k := by
        rw [Nat.sub_add_comm hp1]
  have haux := zmod_p_add_choose_factor_expansion_mod_p4_aux p (k - 1) hp ht
  change (((p - 1 + k).choose k : R)) =
    (p : R) * ((k : R)⁻¹) *
      Finset.prod (Finset.Icc 1 (k - 1))
        (fun j => 1 + (p : R) * (j : R)⁻¹)
  simpa [R, Nat.sub_add_cancel hk1, htop] using haux

lemma square_zero_mul_prod_one_add
    {R : Type*} [CommRing R] {ι : Type*}
    (s : Finset ι) (q : R) (b : ι → R) (hq : q ^ 2 = 0) :
    q * (∏ x in s, (1 + q * b x)) = q := by
  classical
  refine Finset.induction_on s ?base ?step
  · simp
  · intro a s has ih
    rw [Finset.prod_insert has]
    calc
      q * ((1 + q * b a) * ∏ x in s, (1 + q * b x))
          = (q * (1 + q * b a)) * ∏ x in s, (1 + q * b x) := by
            rw [mul_assoc]
      _ = q * ∏ x in s, (1 + q * b x) := by
            have hqa : q * (1 + q * b a) = q := by
              calc
                q * (1 + q * b a) = q + q ^ 2 * b a := by
                  simp only [mul_add, mul_one, pow_two]
                  rw [mul_assoc]
                _ = q := by rw [hq, zero_mul, add_zero]
            rw [hqa]
      _ = q := ih

lemma square_zero_mul_prod_one_add_sq
    {R : Type*} [CommRing R] {ι : Type*}
    (s : Finset ι) (q : R) (b : ι → R) (hq : q ^ 2 = 0) :
    q * (∏ x in s, (1 + q * b x)) ^ 2 = q := by
  classical
  let P := ∏ x in s, (1 + q * b x)
  have hP : q * P = q := square_zero_mul_prod_one_add s q b hq
  calc
    q * P ^ 2 = (q * P) * P := by
      rw [pow_two, mul_assoc]
    _ = q * P := by
      rw [hP]
      exact hP
    _ = q := hP

lemma zmod_pair_factor_collapse_mod_square (p k : ℕ)
    (_hk : Nat.Coprime k (p ^ 2)) :
    (1 - (p : ZMod (p ^ 2)) * (k : ZMod (p ^ 2))⁻¹) *
      (1 + (p : ZMod (p ^ 2)) * (k : ZMod (p ^ 2))⁻¹) = 1 := by
  let R := ZMod (p ^ 2)
  change (1 - (p : R) * (k : R)⁻¹) *
      (1 + (p : R) * (k : R)⁻¹) = 1
  have hp2 : ((p : R) ^ 2) = 0 := by
    simpa [R] using zmod_nat_cast_self_sq_eq_zero_mod_square p
  calc
    (1 - (p : R) * (k : R)⁻¹) * (1 + (p : R) * (k : R)⁻¹)
        = 1 - ((p : R) * (k : R)⁻¹) ^ 2 := by ring
    _ = 1 := by
      rw [mul_pow, hp2, zero_mul, sub_zero]

lemma zmod_pair_factor_product_collapse_mod_square (p : ℕ) (hp : p.Prime) :
    Finset.prod (Finset.Icc 1 (p - 1))
        (fun k => (1 - (p : ZMod (p ^ 2)) * (k : ZMod (p ^ 2))⁻¹)) *
      Finset.prod (Finset.Icc 1 (p - 1))
        (fun k => (1 + (p : ZMod (p ^ 2)) * (k : ZMod (p ^ 2))⁻¹)) = 1 := by
  rw [← Finset.prod_mul_distrib]
  apply Finset.prod_eq_one
  intro k hk
  exact zmod_pair_factor_collapse_mod_square p k
    (zmod_range_coprime_mod_square p k hp (Finset.mem_Icc.mp hk).1 (Finset.mem_Icc.mp hk).2)

lemma zmod_inv_pow_of_unit {n : ℕ} (x : ZMod n) (hx : IsUnit x) (r : ℕ) :
    (x ^ r)⁻¹ = x⁻¹ ^ r := by
  apply ZMod.inv_eq_of_mul_eq_one
  rw [← mul_pow, ZMod.mul_inv_of_unit x hx]
  simp

lemma zmod_nat_cast_self_pow_four_eq_zero_mod_p4 (p : ℕ) :
    ((p : ZMod (p ^ 4)) ^ 4) = 0 := by
  simpa [Nat.cast_pow] using
    (ZMod.natCast_pow_eq_zero_of_le p (m := 4) (n := 4) le_rfl)

lemma zmod_nat_cast_self_sq_sq_eq_zero_mod_p4 (p : ℕ) :
    (((p : ZMod (p ^ 4)) ^ 2) ^ 2) = 0 := by
  rw [← pow_mul]
  exact zmod_nat_cast_self_pow_four_eq_zero_mod_p4 p

lemma zmod_paired_factor_product_sq_kill_by_p2_mod_p4 (p k : ℕ) :
    let R := ZMod (p ^ 4)
    (p : R) ^ 2 *
      (Finset.prod (Finset.Icc 1 (k - 1))
          (fun j => 1 - (p : R) * (j : R)⁻¹) *
        Finset.prod (Finset.Icc 1 (k - 1))
          (fun j => 1 + (p : R) * (j : R)⁻¹)) ^ 2 =
      (p : R) ^ 2 := by
  let R := ZMod (p ^ 4)
  let q : R := (p : R) ^ 2
  change q *
      (Finset.prod (Finset.Icc 1 (k - 1))
          (fun j => 1 - (p : R) * (j : R)⁻¹) *
        Finset.prod (Finset.Icc 1 (k - 1))
          (fun j => 1 + (p : R) * (j : R)⁻¹)) ^ 2 =
      q
  have hq : q ^ 2 = 0 := by
    simpa [q] using zmod_nat_cast_self_sq_sq_eq_zero_mod_p4 p
  calc
    q *
        (Finset.prod (Finset.Icc 1 (k - 1))
            (fun j => 1 - (p : R) * (j : R)⁻¹) *
          Finset.prod (Finset.Icc 1 (k - 1))
            (fun j => 1 + (p : R) * (j : R)⁻¹)) ^ 2
        =
        q *
          (Finset.prod (Finset.Icc 1 (k - 1))
            (fun j =>
              (1 - (p : R) * (j : R)⁻¹) *
                (1 + (p : R) * (j : R)⁻¹))) ^ 2 := by
          rw [Finset.prod_mul_distrib]
    _ =
        q *
          (Finset.prod (Finset.Icc 1 (k - 1))
            (fun j => 1 + q * (-(((j : R)⁻¹) ^ 2)))) ^ 2 := by
          congr 2
          apply Finset.prod_congr rfl
          intro j _hj
          simp [q]
          ring
    _ = q :=
        square_zero_mul_prod_one_add_sq (Finset.Icc 1 (k - 1)) q
          (fun j => -(((j : R)⁻¹) ^ 2)) hq

lemma zmod_hypergeometric_summand_expansion_mod_p4
    (p k m : ℕ) (hp : p.Prime) (hk1 : 1 ≤ k) (hkp : k ≤ p - 1) :
    let R := ZMod (p ^ 4)
    ((((p - 1).choose k : R) ^ 2) *
      (((p - 1 + k).choose k : R) ^ 2) *
      (((k : R) ^ (2 * m + 1))⁻¹)) =
      (p : R) ^ 2 * (((k : R) ^ (2 * m + 3))⁻¹) -
        (2 : R) * (p : R) ^ 3 * (((k : R) ^ (2 * m + 4))⁻¹) := by
  let R := ZMod (p ^ 4)
  change ((((p - 1).choose k : R) ^ 2) *
      (((p - 1 + k).choose k : R) ^ 2) *
      (((k : R) ^ (2 * m + 1))⁻¹)) =
      (p : R) ^ 2 * (((k : R) ^ (2 * m + 3))⁻¹) -
        (2 : R) * (p : R) ^ 3 * (((k : R) ^ (2 * m + 4))⁻¹)
  let Pm : R :=
    Finset.prod (Finset.Icc 1 (k - 1))
      (fun j => 1 - (p : R) * (j : R)⁻¹)
  let Pp : R :=
    Finset.prod (Finset.Icc 1 (k - 1))
      (fun j => 1 + (p : R) * (j : R)⁻¹)
  let u : R := (k : R)⁻¹
  have hunit : IsUnit (k : R) :=
    zmod_unit_denominator_for_range p k hp hk1 hkp
  have hlower := zmod_p_minus_one_choose_factor_expansion_mod_p4 p k hp hk1 hkp
  have hupper := zmod_p_minus_one_add_choose_factor_expansion_mod_p4 p k hp hk1 hkp
  change (((p - 1).choose k : R)) =
      (-1 : R) ^ k *
        Finset.prod (Finset.Icc 1 k)
          (fun j => 1 - (p : R) * (j : R)⁻¹) at hlower
  change (((p - 1 + k).choose k : R)) =
      (p : R) * ((k : R)⁻¹) *
        Finset.prod (Finset.Icc 1 (k - 1))
          (fun j => 1 + (p : R) * (j : R)⁻¹) at hupper
  have hsplit :
      Finset.prod (Finset.Icc 1 k)
          (fun j => 1 - (p : R) * (j : R)⁻¹) =
        Pm * (1 - (p : R) * u) := by
    have hkpred : k - 1 + 1 = k := Nat.sub_add_cancel hk1
    rw [← hkpred]
    change Finset.prod (Finset.Icc 1 (k - 1 + 1))
          (fun j => 1 - (p : R) * (j : R)⁻¹) =
        Pm * (1 - (p : R) * u)
    rw [Finset.prod_Icc_succ_top (by simpa [hkpred] using hk1)]
    simp [Pm, u, hkpred]
  have hcollapse : (p : R) ^ 2 * (Pm * Pp) ^ 2 = (p : R) ^ 2 := by
    simpa [R, Pm, Pp] using zmod_paired_factor_product_sq_kill_by_p2_mod_p4 p k
  have hp4 : (p : R) ^ 4 = 0 := by
    simpa [R] using zmod_nat_cast_self_pow_four_eq_zero_mod_p4 p
  have hinv1 :
      (((k : R) ^ (2 * m + 1))⁻¹) = u ^ (2 * m + 1) := by
    simpa [u] using zmod_inv_pow_of_unit (k : R) hunit (2 * m + 1)
  have hinv3 :
      (((k : R) ^ (2 * m + 3))⁻¹) = u ^ (2 * m + 3) := by
    simpa [u] using zmod_inv_pow_of_unit (k : R) hunit (2 * m + 3)
  have hinv4 :
      (((k : R) ^ (2 * m + 4))⁻¹) = u ^ (2 * m + 4) := by
    simpa [u] using zmod_inv_pow_of_unit (k : R) hunit (2 * m + 4)
  rw [hlower, hupper, hsplit, hinv1, hinv3, hinv4]
  have hsign : ((-1 : R) ^ k * (Pm * (1 - (p : R) * u))) ^ 2 =
      (Pm * (1 - (p : R) * u)) ^ 2 := by
    calc
      ((-1 : R) ^ k * (Pm * (1 - (p : R) * u))) ^ 2
          = ((-1 : R) ^ k) ^ 2 * (Pm * (1 - (p : R) * u)) ^ 2 := by
            rw [mul_pow]
      _ = (Pm * (1 - (p : R) * u)) ^ 2 := by
            have hneg : ((-1 : R) ^ k) ^ 2 = 1 := by
              rw [← pow_mul]
              have hEven : Even (k * 2) := ⟨k, by omega⟩
              exact hEven.neg_one_pow
            rw [hneg, one_mul]
  rw [hsign]
  calc
    (Pm * (1 - (p : R) * u)) ^ 2 *
          ((p : R) * u * Pp) ^ 2 * u ^ (2 * m + 1)
        =
        ((p : R) ^ 2 * (Pm * Pp) ^ 2) *
          (u ^ 2 * u ^ (2 * m + 1)) *
          (1 - (p : R) * u) ^ 2 := by
          ring
    _ =
        (p : R) ^ 2 * u ^ (2 * m + 3) -
          (2 : R) * (p : R) ^ 3 * u ^ (2 * m + 4) := by
          rw [hcollapse]
          have hpow1 : 2 + (2 * m + 1) = 2 * m + 3 := by omega
          rw [← pow_add, hpow1]
          have hsucc : 2 * m + 3 + 1 = 2 * m + 4 := by omega
          have hpowu : u ^ (2 * m + 4) = u ^ (2 * m + 3) * u := by
            rw [← hsucc, pow_succ]
          rw [hpowu]
          calc
            (p : R) ^ 2 * u ^ (2 * m + 3) * (1 - (p : R) * u) ^ 2
                =
                (p : R) ^ 2 * u ^ (2 * m + 3) -
                  (2 : R) * (p : R) ^ 3 * (u ^ (2 * m + 3) * u) +
                    (p : R) ^ 4 * (u ^ (2 * m + 3) * u ^ 2) := by
                  ring
            _ =
                (p : R) ^ 2 * u ^ (2 * m + 3) -
                  (2 : R) * (p : R) ^ 3 * (u ^ (2 * m + 3) * u) := by
                  rw [hp4]
                  ring

lemma finset_mul_sum_left
    {R : Type*} [Semiring R] {ι : Type*}
    (s : Finset ι) (a : R) (f : ι → R) :
    a * Finset.sum s f = Finset.sum s (fun x => a * f x) := by
  classical
  refine Finset.induction_on s ?base ?step
  · simp
  · intro x s hx ih
    rw [Finset.sum_insert hx, Finset.sum_insert hx, mul_add, ih]

lemma zmod_hypergeometric_sum_expansion_mod_p4
    (p m : ℕ) (hp : p.Prime) :
    let R := ZMod (p ^ 4)
    (∑ k in Finset.Icc 1 (p - 1),
      (((p - 1).choose k : R) ^ 2) *
      (((p - 1 + k).choose k : R) ^ 2) *
      (((k : R) ^ (2 * m + 1))⁻¹)) =
      (p : R) ^ 2 *
        (∑ k in Finset.Icc 1 (p - 1), (((k : R) ^ (2 * m + 3))⁻¹)) -
      (2 : R) * (p : R) ^ 3 *
        (∑ k in Finset.Icc 1 (p - 1), (((k : R) ^ (2 * m + 4))⁻¹)) := by
  let R := ZMod (p ^ 4)
  change
    (∑ k in Finset.Icc 1 (p - 1),
      (((p - 1).choose k : R) ^ 2) *
      (((p - 1 + k).choose k : R) ^ 2) *
      (((k : R) ^ (2 * m + 1))⁻¹)) =
      (p : R) ^ 2 *
        (∑ k in Finset.Icc 1 (p - 1), (((k : R) ^ (2 * m + 3))⁻¹)) -
      (2 : R) * (p : R) ^ 3 *
        (∑ k in Finset.Icc 1 (p - 1), (((k : R) ^ (2 * m + 4))⁻¹))
  calc
    (∑ k in Finset.Icc 1 (p - 1),
      (((p - 1).choose k : R) ^ 2) *
      (((p - 1 + k).choose k : R) ^ 2) *
      (((k : R) ^ (2 * m + 1))⁻¹))
        =
        ∑ k in Finset.Icc 1 (p - 1),
          ((p : R) ^ 2 * (((k : R) ^ (2 * m + 3))⁻¹) -
            (2 : R) * (p : R) ^ 3 * (((k : R) ^ (2 * m + 4))⁻¹)) := by
          apply Finset.sum_congr rfl
          intro k hk
          exact zmod_hypergeometric_summand_expansion_mod_p4 p k m hp
            (Finset.mem_Icc.mp hk).1 (Finset.mem_Icc.mp hk).2
    _ =
      (p : R) ^ 2 *
        (∑ k in Finset.Icc 1 (p - 1), (((k : R) ^ (2 * m + 3))⁻¹)) -
      (2 : R) * (p : R) ^ 3 *
        (∑ k in Finset.Icc 1 (p - 1), (((k : R) ^ (2 * m + 4))⁻¹)) := by
      rw [Finset.sum_sub_distrib]
      rw [← finset_mul_sum_left, ← finset_mul_sum_left]

lemma zmod_prime_isUnit_of_ne_zero
    (p : ℕ) [NeZero p] (hp : p.Prime) {x : ZMod p} (hx : x ≠ 0) :
    IsUnit x := by
  rw [← ZMod.natCast_zmod_val x]
  rw [ZMod.isUnit_iff_coprime]
  have hvalne : x.val ≠ 0 := by
    intro h
    exact hx ((ZMod.val_eq_zero x).mp h)
  have hnot : ¬ p ∣ x.val :=
    Nat.not_dvd_of_pos_of_lt (Nat.pos_of_ne_zero hvalne) (ZMod.val_lt x)
  exact (hp.coprime_iff_not_dvd.mpr hnot).symm

lemma zmod_p_dvd_p_fourth_power (p : ℕ) : p ∣ p ^ 4 := by
  rw [show p ^ 4 = p * p ^ 3 by ring]
  exact dvd_mul_right p (p ^ 3)

lemma zmod_p3_mul_eq_zero_of_cast_mod_p_eq_zero
    (p : ℕ) (hp : p.Prime) (x : ZMod (p ^ 4))
    (hx : ZMod.castHom (zmod_p_dvd_p_fourth_power p) (ZMod p) x = 0) :
    (p : ZMod (p ^ 4)) ^ 3 * x = 0 := by
  haveI : NeZero p := ⟨Nat.ne_of_gt hp.pos⟩
  haveI : NeZero (p ^ 4) := ⟨pow_ne_zero 4 (Nat.ne_of_gt hp.pos)⟩
  have hdiv : p ∣ x.val := by
    have hvalzero : (x.val : ZMod p) = 0 := by
      change ZMod.cast x = 0 at hx
      rw [ZMod.cast_eq_val] at hx
      exact hx
    exact (ZMod.natCast_eq_zero_iff x.val p).mp hvalzero
  rw [← ZMod.natCast_zmod_val x]
  rw [← Nat.cast_pow, ← Nat.cast_mul]
  rw [ZMod.natCast_eq_zero_iff]
  rcases hdiv with ⟨a, ha⟩
  refine ⟨a, ?_⟩
  rw [ha]
  ring

lemma zmod_sum_Icc_cast_eq_sum_univ_erase
    {A : Type*} [AddCommMonoid A] (p : ℕ) [NeZero p] (hp : p.Prime)
    (f : ZMod p → A) :
    (∑ k in Finset.Icc 1 (p - 1), f (k : ZMod p)) =
      ∑ x in (Finset.univ.erase (0 : ZMod p)), f x := by
  refine Finset.sum_bij (s := Finset.Icc 1 (p - 1))
    (t := Finset.univ.erase (0 : ZMod p))
    (f := fun k => f (k : ZMod p)) (g := f)
    (fun k _ => (k : ZMod p)) ?_ ?_ ?_ ?_
  · intro k hk
    rw [Finset.mem_erase]
    constructor
    · intro hzero
      have hk' := Finset.mem_Icc.mp hk
      have hklt : k < p :=
        lt_of_le_of_lt hk'.2 (Nat.sub_one_lt (Nat.ne_of_gt hp.pos))
      have hval := congrArg ZMod.val hzero
      rw [ZMod.val_natCast_of_lt hklt, ZMod.val_zero] at hval
      have hkpos : 0 < k := lt_of_lt_of_le zero_lt_one hk'.1
      exact (Nat.ne_of_gt hkpos) hval
    · simp
  · intro a ha b hb hEq
    have ha' := Finset.mem_Icc.mp ha
    have hb' := Finset.mem_Icc.mp hb
    have halt : a < p :=
      lt_of_le_of_lt ha'.2 (Nat.sub_one_lt (Nat.ne_of_gt hp.pos))
    have hblt : b < p :=
      lt_of_le_of_lt hb'.2 (Nat.sub_one_lt (Nat.ne_of_gt hp.pos))
    have hval := congrArg ZMod.val hEq
    rw [ZMod.val_natCast_of_lt halt, ZMod.val_natCast_of_lt hblt] at hval
    exact hval
  · intro x hx
    refine ⟨x.val, ?_, ?_⟩
    · rw [Finset.mem_Icc]
      have hxne : x ≠ 0 := (Finset.mem_erase.mp hx).1
      have hvalne : x.val ≠ 0 := by
        intro h
        exact hxne ((ZMod.val_eq_zero x).mp h)
      constructor
      · exact Nat.succ_le_of_lt (Nat.pos_of_ne_zero hvalne)
      · have hvlt : x.val < p := ZMod.val_lt x
        exact Nat.le_pred_of_lt hvlt
    · exact ZMod.natCast_zmod_val x
  · intro k hk
    rfl

lemma zmod_sum_units_eq_sum_univ_erase_pow
    (p e : ℕ) [Fintype (ZMod p)ˣ] [NeZero p] (hp : p.Prime) :
    Finset.sum (Finset.univ : Finset (ZMod p)ˣ)
        (fun u => ((u : ZMod p) ^ e)) =
      Finset.sum (Finset.univ.erase (0 : ZMod p)) (fun x => x ^ e) := by
  haveI : Fact p.Prime := ⟨hp⟩
  refine Finset.sum_bij (s := (Finset.univ : Finset (ZMod p)ˣ))
    (t := Finset.univ.erase (0 : ZMod p))
    (f := fun u => ((u : ZMod p) ^ e)) (g := fun x => x ^ e)
    (fun u _ => (u : ZMod p)) ?_ ?_ ?_ ?_
  · intro u _hu
    rw [Finset.mem_erase]
    exact ⟨Units.ne_zero u, by simp⟩
  · intro a _ha b _hb h
    exact Units.ext h
  · intro y hy
    have hyne : y ≠ 0 := (Finset.mem_erase.mp hy).1
    have hyunit := zmod_prime_isUnit_of_ne_zero p hp hyne
    rcases hyunit with ⟨u, hu⟩
    refine ⟨u, by simp, ?_⟩
    simpa using hu
  · intro u _hu
    rfl

lemma zmod_sum_univ_erase_inv_pow_eq_sum_univ_erase_pow
    (p e : ℕ) [NeZero p] (hp : p.Prime) :
    Finset.sum (Finset.univ.erase (0 : ZMod p)) (fun x => ((x ^ e)⁻¹)) =
      Finset.sum (Finset.univ.erase (0 : ZMod p)) (fun x => x ^ e) := by
  refine Finset.sum_bij (s := Finset.univ.erase (0 : ZMod p))
    (t := Finset.univ.erase (0 : ZMod p))
    (f := fun x => ((x ^ e)⁻¹)) (g := fun x => x ^ e)
    (fun x _ => x⁻¹) ?_ ?_ ?_ ?_
  · intro x hx
    rw [Finset.mem_erase]
    have hxne : x ≠ 0 := (Finset.mem_erase.mp hx).1
    have hxunit := zmod_prime_isUnit_of_ne_zero p hp hxne
    constructor
    · intro hinvzero
      change x⁻¹ = 0 at hinvzero
      have hxzero : x = 0 := by
        calc
          x = x * (1 : ZMod p) := by rw [mul_one]
          _ = x * (x * x⁻¹) := by rw [ZMod.mul_inv_of_unit x hxunit]
          _ = x * (x * 0) := by rw [hinvzero]
          _ = 0 := by ring
      exact hxne hxzero
    · simp
  · intro a ha b hb hEq
    change a⁻¹ = b⁻¹ at hEq
    have hane : a ≠ 0 := (Finset.mem_erase.mp ha).1
    have hbne : b ≠ 0 := (Finset.mem_erase.mp hb).1
    have haunit := zmod_prime_isUnit_of_ne_zero p hp hane
    have hbunit := zmod_prime_isUnit_of_ne_zero p hp hbne
    calc
      a = (a⁻¹)⁻¹ := by
        exact (ZMod.inv_eq_of_mul_eq_one p (a⁻¹) a
          (ZMod.inv_mul_of_unit a haunit)).symm
      _ = (b⁻¹)⁻¹ := by rw [hEq]
      _ = b := by
        exact ZMod.inv_eq_of_mul_eq_one p (b⁻¹) b
          (ZMod.inv_mul_of_unit b hbunit)
  · intro y hy
    refine ⟨y⁻¹, ?_, ?_⟩
    · rw [Finset.mem_erase]
      have hyne : y ≠ 0 := (Finset.mem_erase.mp hy).1
      have hyunit := zmod_prime_isUnit_of_ne_zero p hp hyne
      constructor
      · intro hinvzero
        have hyzero : y = 0 := by
          calc
            y = y * (1 : ZMod p) := by rw [mul_one]
            _ = y * (y * y⁻¹) := by rw [ZMod.mul_inv_of_unit y hyunit]
            _ = y * (y * 0) := by rw [hinvzero]
            _ = 0 := by ring
        exact hyne hyzero
      · simp
    · have hyne : y ≠ 0 := (Finset.mem_erase.mp hy).1
      have hyunit := zmod_prime_isUnit_of_ne_zero p hp hyne
      exact ZMod.inv_eq_of_mul_eq_one p (y⁻¹) y
        (ZMod.inv_mul_of_unit y hyunit)
  · intro x hx
    have hxne : x ≠ 0 := (Finset.mem_erase.mp hx).1
    have hxunit := zmod_prime_isUnit_of_ne_zero p hp hxne
    simpa using
      (ZMod.inv_eq_of_mul_eq_one p (x ^ e) ((x⁻¹) ^ e)
        (by rw [← mul_pow, ZMod.mul_inv_of_unit x hxunit, one_pow]))

lemma zmod_units_power_sum_eq_zero_of_pos_lt
    (p e : ℕ) [Fintype (ZMod p)ˣ] (hp : p.Prime)
    (hepos : 0 < e) (helt : e < p - 1) :
    Finset.sum (Finset.univ : Finset (ZMod p)ˣ)
        (fun u => ((u : ZMod p) ^ e)) = 0 := by
  haveI : Fact p.Prime := ⟨hp⟩
  haveI : NeZero p := ⟨Nat.ne_of_gt hp.pos⟩
  let φ : (ZMod p)ˣ →* ZMod p :=
    { toFun := fun u => (u : ZMod p) ^ e
      map_one' := by simp
      map_mul' := by intro a b; simp [mul_pow] }
  have hφ : φ ≠ 1 := by
    intro hφone
    let P : Polynomial (ZMod p) := Polynomial.X ^ e - Polynomial.C (1 : ZMod p)
    have hP0 : P ≠ 0 := by
      simpa [P] using
        (Polynomial.X_pow_sub_C_ne_zero (R := ZMod p) hepos (1 : ZMod p))
    let s : Finset (ZMod p) :=
      (Finset.univ : Finset (ZMod p)ˣ).image (fun u : (ZMod p)ˣ => (u : ZMod p))
    have hcard_s : s.card = Fintype.card (ZMod p)ˣ := by
      dsimp [s]
      rw [Finset.card_image_of_injective]
      · simp
      · exact Units.val_injective
    have hsubset : s ⊆ P.roots.toFinset := by
      intro x hx
      rcases Finset.mem_image.mp hx with ⟨u, _hu, rfl⟩
      rw [Multiset.mem_toFinset]
      rw [Polynomial.mem_roots hP0]
      rw [Polynomial.IsRoot.def]
      have hu : (u : ZMod p) ^ e = 1 := by
        have hcongr : φ u = (1 : (ZMod p)ˣ →* ZMod p) u := by rw [hφone]
        simpa [φ] using hcongr
      simp [P, hu]
    have hle1 : Fintype.card (ZMod p)ˣ ≤ P.roots.toFinset.card := by
      rw [← hcard_s]
      exact Finset.card_le_card hsubset
    have hle2 : P.roots.toFinset.card ≤ P.roots.card := Multiset.toFinset_card_le _
    have hle3 : P.roots.card ≤ e := by
      have h := Polynomial.card_roots' P
      have hdeg : P.natDegree = e := by
        simpa [P] using
          (Polynomial.natDegree_X_pow_sub_C (R := ZMod p) (n := e) (r := (1 : ZMod p)))
      exact hdeg ▸ h
    have hcard_units : Fintype.card (ZMod p)ˣ = p - 1 := by
      rw [ZMod.card_units_eq_totient p]
      exact (Nat.totient_eq_iff_prime hp.pos).mpr hp
    have hpminus_le_e : p - 1 ≤ e := by
      rw [← hcard_units]
      exact le_trans hle1 (le_trans hle2 hle3)
    exact (not_le_of_gt helt) hpminus_le_e
  simpa [φ] using (sum_hom_units_eq_zero φ hφ)

lemma zmod_inverse_power_sum_eq_zero_mod_p_of_pos_lt
    (p e : ℕ) (hp : p.Prime) (hepos : 0 < e) (helt : e < p - 1) :
    ∑ k in Finset.Icc 1 (p - 1), (((k : ZMod p) ^ e)⁻¹) = 0 := by
  classical
  haveI : Fact p.Prime := ⟨hp⟩
  haveI : NeZero p := ⟨Nat.ne_of_gt hp.pos⟩
  calc
    (∑ k in Finset.Icc 1 (p - 1), (((k : ZMod p) ^ e)⁻¹))
        =
        Finset.sum (Finset.univ.erase (0 : ZMod p)) (fun x => ((x ^ e)⁻¹)) := by
          exact zmod_sum_Icc_cast_eq_sum_univ_erase p hp (fun x => ((x ^ e)⁻¹))
    _ =
        Finset.sum (Finset.univ.erase (0 : ZMod p)) (fun x => x ^ e) := by
          exact zmod_sum_univ_erase_inv_pow_eq_sum_univ_erase_pow p e hp
    _ =
        Finset.sum (Finset.univ : Finset (ZMod p)ˣ)
          (fun u => ((u : ZMod p) ^ e)) := by
          exact (zmod_sum_units_eq_sum_univ_erase_pow p e hp).symm
    _ = 0 := zmod_units_power_sum_eq_zero_of_pos_lt p e hp hepos helt

lemma zmod_cast_inverse_power_term_mod_p
    (p k e : ℕ) (hp : p.Prime) (hk1 : 1 ≤ k) (hkp : k ≤ p - 1) :
    ZMod.castHom (zmod_p_dvd_p_fourth_power p) (ZMod p)
        ((((k : ZMod (p ^ 4)) ^ e)⁻¹)) =
      (((k : ZMod p) ^ e)⁻¹) := by
  haveI : Fact p.Prime := ⟨hp⟩
  haveI : NeZero p := ⟨Nat.ne_of_gt hp.pos⟩
  have hunit4 : IsUnit (k : ZMod (p ^ 4)) :=
    zmod_unit_denominator_for_range p k hp hk1 hkp
  have hunitp : IsUnit (k : ZMod p) := by
    rw [← ZMod.natCast_zmod_val (k : ZMod p)]
    rw [ZMod.isUnit_iff_coprime]
    have hklt : k < p :=
      lt_of_le_of_lt hkp (Nat.sub_one_lt (Nat.ne_of_gt hp.pos))
    have hval : (k : ZMod p).val = k := ZMod.val_natCast_of_lt hklt
    rw [hval]
    have hnot : ¬ p ∣ k := Nat.not_dvd_of_pos_of_lt hk1 hklt
    exact (hp.coprime_iff_not_dvd.mpr hnot).symm
  have hmap_inv_k :
      ZMod.castHom (zmod_p_dvd_p_fourth_power p) (ZMod p)
          ((k : ZMod (p ^ 4))⁻¹) = ((k : ZMod p)⁻¹) := by
    symm
    apply ZMod.inv_eq_of_mul_eq_one
    calc
      (k : ZMod p) *
          ZMod.castHom (zmod_p_dvd_p_fourth_power p) (ZMod p)
            ((k : ZMod (p ^ 4))⁻¹)
          =
          ZMod.castHom (zmod_p_dvd_p_fourth_power p) (ZMod p)
            ((k : ZMod (p ^ 4)) * ((k : ZMod (p ^ 4))⁻¹)) := by
            rw [map_mul]
            simp
      _ = 1 := by rw [ZMod.mul_inv_of_unit _ hunit4, map_one]
  rw [zmod_inv_pow_of_unit (k : ZMod (p ^ 4)) hunit4 e]
  rw [map_pow]
  rw [hmap_inv_k]
  exact (zmod_inv_pow_of_unit (k : ZMod p) hunitp e).symm

lemma zmod_p3_mul_inverse_power_sum_even_eq_zero_mod_p4_of_large
    (p m : ℕ) (hp : p.Prime) (hlarge : 2 * m + 6 < p) :
    let R := ZMod (p ^ 4)
    (2 : R) * (p : R) ^ 3 *
      (∑ k in Finset.Icc 1 (p - 1), (((k : R) ^ (2 * m + 4))⁻¹)) = 0 := by
  let R := ZMod (p ^ 4)
  change (2 : R) * (p : R) ^ 3 *
      (∑ k in Finset.Icc 1 (p - 1), (((k : R) ^ (2 * m + 4))⁻¹)) = 0
  have hepos : 0 < 2 * m + 4 := by omega
  have helt : 2 * m + 4 < p - 1 := by omega
  let S : R := ∑ k in Finset.Icc 1 (p - 1), (((k : R) ^ (2 * m + 4))⁻¹)
  have hcastS : ZMod.castHom (zmod_p_dvd_p_fourth_power p) (ZMod p) S = 0 := by
    calc
      ZMod.castHom (zmod_p_dvd_p_fourth_power p) (ZMod p) S
          =
          ∑ k in Finset.Icc 1 (p - 1),
            (((k : ZMod p) ^ (2 * m + 4))⁻¹) := by
            change
              ZMod.castHom (zmod_p_dvd_p_fourth_power p) (ZMod p)
                  (∑ k in Finset.Icc 1 (p - 1),
                    (((k : R) ^ (2 * m + 4))⁻¹)) =
                ∑ k in Finset.Icc 1 (p - 1),
                  (((k : ZMod p) ^ (2 * m + 4))⁻¹)
            rw [map_sum]
            apply Finset.sum_congr rfl
            intro k hk
            exact zmod_cast_inverse_power_term_mod_p p k (2 * m + 4) hp
              (Finset.mem_Icc.mp hk).1 (Finset.mem_Icc.mp hk).2
      _ = 0 :=
          zmod_inverse_power_sum_eq_zero_mod_p_of_pos_lt p (2 * m + 4) hp hepos helt
  have hkill : (p : R) ^ 3 * S = 0 :=
    zmod_p3_mul_eq_zero_of_cast_mod_p_eq_zero p hp S hcastS
  rw [mul_assoc, hkill, mul_zero]
end OeisA357513NextRound20260606
