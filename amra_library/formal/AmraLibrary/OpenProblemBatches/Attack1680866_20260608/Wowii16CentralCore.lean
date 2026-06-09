import Mathlib.Data.Finset.Basic

namespace Wowii16CentralCore20260609

lemma centralIntervalDeepPredOffBaseCore
    {α : Type*} [DecidableEq α]
    (H0 Avail : Finset α)
    (pred : α → α) (depth : α → ℕ)
    (H0_depth_zero : ∀ x, x ∈ H0 → depth x = 0)
    (pred_depth_succ : ∀ x, x ∈ Avail → 0 < depth x →
      depth x = depth (pred x) + 1)
    {z : α}
    (hzAvail : z ∈ Avail)
    (hzDepth : 2 ≤ depth z) :
    pred z ∉ H0 := by
  intro hzPred
  have hPredDepth : depth (pred z) = 0 :=
    H0_depth_zero (pred z) hzPred
  have hzPos : 0 < depth z :=
    lt_of_lt_of_le (by decide : 0 < 2) hzDepth
  have hStep : depth z = depth (pred z) + 1 :=
    pred_depth_succ z hzAvail hzPos
  have hzOne : depth z = 1 := by
    calc
      depth z = depth (pred z) + 1 := hStep
      _ = 0 + 1 := by rw [hPredDepth]
      _ = 1 := rfl
  have hBad : 2 ≤ 1 := by
    rw [hzOne] at hzDepth
    exact hzDepth
  exact (by decide : ¬ 2 ≤ 1) hBad

lemma centralIntervalSharedFirstStepIndexGapLeTwo
    {α : Type*}
    (dist : α → α → ℕ) (Adj : α → α → Prop)
    (p z : ℕ → α) (pred : α → α)
    (commonNeighbor_dist_le_two :
      ∀ x y a, Adj x a → Adj a y → dist x y ≤ 2)
    {i j : ℕ}
    (hij : i ≤ j)
    (hGeod : dist (p i) (p j) = j - i)
    (hFirst_i : Adj (p i) (pred (z i)))
    (hFirst_j : Adj (pred (z j)) (p j))
    (hShare : pred (z i) = pred (z j)) :
    j - i ≤ 2 := by
  rw [← hGeod]
  exact commonNeighbor_dist_le_two (p i) (p j) (pred (z i))
    hFirst_i (by simpa [hShare] using hFirst_j)

end Wowii16CentralCore20260609
