#include <algorithm>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <unordered_map>
#include <utility>
#include <vector>

// Finite falsifier for the semiprime-oddpart proper-lower-neighbour graph.
// It deliberately makes no asymptotic claim.  A left vertex x=2^a p q,
// p<q odd primes, is represented by the edge {x-q,x-p}.

struct DSU {
  std::vector<int> p, size;
  explicit DSU(int n) : p(n), size(n, 1) { std::iota(p.begin(), p.end(), 0); }
  int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }
  void join(int x, int y) {
    x = find(x); y = find(y);
    if (x == y) return;
    if (size[x] < size[y]) std::swap(x, y);
    p[y] = x; size[x] += size[y];
  }
};

struct Edge { int x, lo, hi, p, q; };

int main(int argc, char** argv) {
  const int N = argc > 1 ? std::stoi(argv[1]) : 5000000;
  const int only_exponent = argc > 2 ? std::stoi(argv[2]) : -1;
  std::vector<int> spf(N + 1);
  for (int i = 0; i <= N; ++i) spf[i] = i;
  for (int i = 2; int64_t(i) * i <= N; ++i) if (spf[i] == i)
    for (int64_t j = int64_t(i) * i; j <= N; j += i)
      if (spf[j] == j) spf[j] = i;

  // Compress only right vertices that actually occur.
  std::unordered_map<int, int> id;
  std::vector<Edge> edges;
  auto get_id = [&](int value) {
    auto [it, inserted] = id.emplace(value, int(id.size()));
    return it->second;
  };
  // First collect, then construct the exact-size DSU.
  for (int x = 2; x <= N; x += 2) {
    int u = x;
    int exponent = 0;
    while ((u & 1) == 0) { u >>= 1; ++exponent; }
    if (only_exponent >= 0 && exponent != only_exponent) continue;
    if (u <= 1) continue;
    int p = spf[u], q = u / p;
    if (p < q && q <= N && spf[q] == q) {
      int lo = x - q, hi = x - p;
      get_id(lo); get_id(hi);
      edges.push_back({x, lo, hi, p, q});
    }
  }
  DSU dsu(id.size());
  for (const auto& e : edges) dsu.join(id[e.lo], id[e.hi]);
  std::vector<int> vertex_count(id.size()), edge_count(id.size());
  for (const auto& [value, idx] : id) ++vertex_count[dsu.find(idx)];
  for (const auto& e : edges) ++edge_count[dsu.find(id[e.lo])];

  int max_surplus = -1, rich_components = 0, best_root = -1;
  for (int i = 0; i < int(id.size()); ++i) if (dsu.find(i) == i) {
    int surplus = edge_count[i] - vertex_count[i];
    if (surplus > max_surplus) { max_surplus = surplus; best_root = i; }
    if (surplus > 0) ++rich_components;
  }
  std::cout << "N=" << N << " edges=" << edges.size()
            << " exponent=" << only_exponent
            << " right_vertices=" << id.size()
            << " max_E_minus_V=" << max_surplus
            << " multicyclic_components=" << rich_components << "\n";
  if (rich_components) {
    std::cout << "first_multicyclic_component\n";
    int emitted = 0;
    for (const auto& e : edges) if (dsu.find(id[e.lo]) == best_root) {
      std::cout << e.x << " " << e.lo << " " << e.hi << " "
                << e.p << " " << e.q << "\n";
      if (++emitted == 200) break;
    }
  }
}
