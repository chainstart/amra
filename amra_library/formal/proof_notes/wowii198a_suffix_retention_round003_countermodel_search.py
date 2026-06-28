from itertools import combinations


def edges_of_path(p):
    return {tuple(sorted((p[i], p[i + 1]))) for i in range(len(p) - 1)}


def all_simple_paths(vertices, edges, start, end):
    adj = {v: [] for v in vertices}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    out = []

    def dfs(u, seen, path):
        if u == end:
            out.append(tuple(path))
            return
        for nb in adj[u]:
            if nb not in seen:
                dfs(nb, seen | {nb}, path + [nb])

    dfs(start, {start}, [start])
    return out


def take_until(path, y):
    return path[: path.index(y) + 1]


def drop_until(path, y):
    return path[path.index(y) :]


def measure(pair, n, v):
    left, right = pair
    common = (set(left) & set(right)) - {v}
    return len(common) * (2 * n + 3) + len(left) + len(right)


def check_candidate(vertices, edges, v, s, t, x, w, z_bad, left, right, rs):
    if len(set(left)) != len(left) or len(set(right)) != len(right) or len(set(rs)) != len(rs):
        return None
    if left[0] != v or left[-1] != s or right[0] != v or right[-1] != t or rs[0] != v or rs[-1] != s:
        return None
    if not (x in left and x in right and x != v and x not in rs):
        return None
    if not (w in rs and w in right and w not in left and w != v):
        return None
    if x not in drop_until(right, w):
        return None
    rs_prefix = set(take_until(rs, w))
    old_union = set(left) | set(right)
    for zz in set(rs):
        if zz in old_union and zz != v:
            if not (zz == w or zz not in rs_prefix):
                return None
    n = len(vertices)
    all_left = all_simple_paths(vertices, edges, v, s)
    all_right = all_simple_paths(vertices, edges, v, t)
    pair = (tuple(left), tuple(right))
    m = measure(pair, n, v)
    if any(measure((l, r), n, v) < m for l in all_left for r in all_right):
        return None
    direct_common = len((set(rs) & set(right)) - {v})
    old_common = len((set(left) & set(right)) - {v})
    if direct_common < old_common:
        return None
    alt_raw = take_until(left, x) + drop_until(right, x)[1:]
    if len(set(alt_raw)) != len(alt_raw):
        return None
    if not (z_bad in rs and z_bad != v and z_bad in alt_raw):
        return None
    conclusion = z_bad in left and z_bad in right and z_bad != x
    if conclusion:
        return None
    return {
        "vertices": vertices,
        "edges": sorted(edges),
        "left": left,
        "right": right,
        "rs": rs,
        "old_common": old_common,
        "direct_common": direct_common,
        "measure": m,
        "alt_raw": alt_raw,
        "bad_z": z_bad,
        "num_left_paths": len(all_left),
        "num_right_paths": len(all_right),
    }


def main():
    # Shaped around the proof-lab branch: right order w < x < z, rs reaches
    # z after w, and old left reaches x through z.  Extra edges are varied to
    # test whether weighted minimality can still hold.
    V = tuple(range(6))
    v, s, t, x, w, z = 0, 1, 2, 3, 4, 5
    left = (v, z, x, s)
    right = (v, w, x, z, t)
    rs = (v, w, z, s)
    required = edges_of_path(left) | edges_of_path(right) | edges_of_path(rs)
    all_edges = {tuple(e) for e in combinations(V, 2)}
    optional = sorted(all_edges - required)
    for mask in range(1 << len(optional)):
        edges = set(required)
        for i, e in enumerate(optional):
            if mask & (1 << i):
                edges.add(e)
        ans = check_candidate(V, edges, v, s, t, x, w, z, left, right, rs)
        if ans is not None:
            print(ans)
            return
    print("no countermodel in shaped six-vertex search")

    import random

    rng = random.Random(198)
    V = tuple(range(6))
    v, s, t = 0, 1, 2
    all_edges = [tuple(e) for e in combinations(V, 2)]
    for trial in range(2000):
      edges = {e for e in all_edges if rng.random() < 0.42}
      left_paths = all_simple_paths(V, edges, v, s)
      right_paths = all_simple_paths(V, edges, v, t)
      if not left_paths or not right_paths:
          continue
      measures = [measure((l, r), len(V), v) for l in left_paths for r in right_paths]
      min_measure = min(measures)
      min_pairs = [
          (l, r) for l in left_paths for r in right_paths
          if measure((l, r), len(V), v) == min_measure
      ]
      rs_paths = left_paths
      for left, right in min_pairs:
          for x in (set(left) & set(right)) - {v}:
              for rs in rs_paths:
                  if x in rs:
                      continue
                  for w in (set(rs) & set(right)) - {v}:
                      if w in left:
                          continue
                      if x not in drop_until(right, w):
                          continue
                      rs_prefix = set(take_until(rs, w))
                      old_union = set(left) | set(right)
                      if any(
                          zz in old_union and zz != v and not (zz == w or zz not in rs_prefix)
                          for zz in set(rs)
                      ):
                          continue
                      direct_common = len((set(rs) & set(right)) - {v})
                      old_common = len((set(left) & set(right)) - {v})
                      if direct_common < old_common:
                          continue
                      alt_raw = take_until(left, x) + drop_until(right, x)[1:]
                      if len(set(alt_raw)) != len(alt_raw):
                          continue
                      for z_bad in (set(rs) & set(alt_raw)) - {v}:
                          if not (z_bad in left and z_bad in right and z_bad != x):
                              print({
                                  "trial": trial,
                                  "vertices": V,
                                  "edges": sorted(edges),
                                  "left": left,
                                  "right": right,
                                  "rs": rs,
                                  "x": x,
                                  "w": w,
                                  "bad_z": z_bad,
                                  "alt_raw": alt_raw,
                                  "old_common": old_common,
                                  "direct_common": direct_common,
                                  "measure": min_measure,
                              })
                              return
    print("no countermodel in 2000 random six-vertex graphs")


if __name__ == "__main__":
    main()
