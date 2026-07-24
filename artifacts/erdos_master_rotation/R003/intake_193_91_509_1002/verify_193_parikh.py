#!/usr/bin/env python3
"""Exhaustive certificate for the ternary abelian-square threshold used in #193."""

from hashlib import sha256


def has_abelian_square_suffix(word: str) -> bool:
    """The new letter can only create a forbidden factor ending at the suffix."""
    for half_length in range(1, len(word) // 2 + 1):
        left = word[-2 * half_length : -half_length]
        right = word[-half_length:]
        if sorted(left) == sorted(right):
            return True
    return False


words = [""]
counts = []
level_seven = []
for length in range(1, 9):
    words = [
        word + letter
        for word in words
        for letter in "012"
        if not has_abelian_square_suffix(word + letter)
    ]
    counts.append(len(words))
    if length == 7:
        level_seven = sorted(words)

assert counts == [3, 6, 12, 18, 30, 30, 18, 0]
assert len(level_seven) == 18
level_seven_bytes = ("\n".join(level_seven) + "\n").encode()
assert sha256(level_seven_bytes).hexdigest() == (
    "1978bcea27ea2211cca15cf9dd6dacde9a28e1507b50a4e625d9e713c7d16614"
)

# A direct independent scan of every ternary word of length eight checks that
# each contains an abelian-square factor, rather than relying only on the
# incremental search invariant above.
for number in range(3**8):
    digits = []
    value = number
    for _ in range(8):
        digits.append(str(value % 3))
        value //= 3
    word = "".join(reversed(digits))
    found = False
    for start in range(8):
        for half_length in range(1, (8 - start) // 2 + 1):
            left = word[start : start + half_length]
            right = word[start + half_length : start + 2 * half_length]
            if sorted(left) == sorted(right):
                found = True
                break
        if found:
            break
    assert found

print("PASS #193: ternary abelian-square-free counts", counts)
