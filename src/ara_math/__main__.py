"""Deprecated ``python -m ara_math`` compatibility entrypoint."""

from ara_math.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
