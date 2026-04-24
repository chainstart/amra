import Mathlib

namespace MathProject

def projectName : String := "{{PROJECT_NAME}}"

def targetStatement : String := "{{TARGET_STATEMENT}}"

theorem sanity_check : 1 + 1 = (2 : Nat) := by
  decide

end MathProject

