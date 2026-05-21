import Lake

open Lake DSL

package minif2f where
  leanOptions := #[
    ⟨`pp.unicode.fun, true⟩, -- pretty-prints `fun a ↦ b`
    ⟨`pp.proofs.withType, false⟩,
    ⟨`autoImplicit, false⟩,
    ⟨`relaxedAutoImplicit, false⟩,
    ⟨`warn.sorry, false⟩,
  ]

@[default_target]
lean_lib MiniF2F where
  globs := #[.submodules `MiniF2F]

require "google-deepmind" / "formal_conjectures"

