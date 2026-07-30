#!/usr/bin/env python3
"""Strict raw-cube CEGIS for the dim-10 profile (2,2,2,2,1,1)."""

import cegis_dim9_profile_2111121 as engine


engine.PROFILE = (2, 2, 2, 2, 1, 1)
engine.RELEVANT_MAX_DEGREE = 4


if __name__ == "__main__":
    raise SystemExit(engine.main())
