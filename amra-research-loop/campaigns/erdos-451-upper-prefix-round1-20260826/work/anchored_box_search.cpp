#include <algorithm>
#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <limits>
#include <numeric>
#include <random>
#include <string>
#include <vector>

using i64 = std::int64_t;

static i64 product(const std::vector<int>& xs) {
  i64 ans = 1;
  for (int x : xs) ans *= x;
  return ans;
}

static i64 first_anchored(const std::vector<int>& ps,
                          const std::vector<int>& ds,
                          i64 cap) {
  for (i64 n = 1; n <= cap; ++n) {
    bool ok = true;
    for (std::size_t i = 0; i < ps.size(); ++i) {
      const int r = static_cast<int>(n % ps[i]);
      const int minus_r = r == 0 ? 0 : ps[i] - r;
      if (minus_r >= ds[i]) {
        ok = false;
        break;
      }
    }
    if (ok) return n;
  }
  return 0;
}

int main(int argc, char** argv) {
  const i64 trials = argc > 1 ? std::stoll(argv[1]) : 20000;
  const std::vector<std::vector<int>> systems = {
      {5, 7, 11, 13, 17},
      {5, 7, 11, 13, 17, 19},
      {7, 11, 13, 17, 19, 23},
      {5, 7, 11, 13, 17, 19, 23},
      {7, 11, 13, 17, 19, 23, 29},
  };
  std::mt19937_64 rng(45120260826ULL);
  std::cout << std::setprecision(17);
  std::cout << "{\n  \"schema_version\": \"erdos451.anchored_box_search.v1\",\n";
  std::cout << "  \"trials_per_system\": " << trials << ",\n";
  std::cout << "  \"systems\": [\n";
  bool first_system = true;
  for (const auto& ps : systems) {
    const i64 P = product(ps);
    double best_ratio = -1.0;
    std::vector<int> best_ds;
    i64 best_first = 0;
    i64 tested = 0;
    bool violation = false;
    std::vector<int> violation_ds;
    i64 violation_bound = 0;
    for (i64 trial = 0; trial < trials; ++trial) {
      std::vector<int> ds;
      i64 N = 1;
      for (int p : ps) {
        // Bias toward narrow boxes, where the proposed bound has the least
        // slack, but retain full support on widths 1,...,p-1.
        const double u = std::generate_canonical<double, 64>(rng);
        const int d = std::max(1, std::min(p - 1, 1 + static_cast<int>((p - 1) * u * u)));
        ds.push_back(d);
        N *= d;
      }
      const long double raw_bound = std::ldexp(static_cast<long double>(P) / N,
                                                static_cast<int>(ps.size()));
      const i64 bound = std::min<i64>(P, static_cast<i64>(std::ceil(raw_bound)));
      const i64 f = first_anchored(ps, ds, bound);
      ++tested;
      if (f == 0) {
        violation = true;
        violation_ds = ds;
        violation_bound = bound;
        break;
      }
      const double ratio = static_cast<double>(f) * static_cast<double>(N) /
                           static_cast<double>(P);
      if (ratio > best_ratio) {
        best_ratio = ratio;
        best_ds = ds;
        best_first = f;
      }
    }
    if (!first_system) std::cout << ",\n";
    first_system = false;
    std::cout << "    {\"moduli\":[";
    for (std::size_t i = 0; i < ps.size(); ++i) {
      if (i) std::cout << ',';
      std::cout << ps[i];
    }
    std::cout << "],\"period\":" << P << ",\"tested\":" << tested
              << ",\"two_to_m\":" << (i64{1} << ps.size())
              << ",\"best_ratio_first_over_inverse_density\":" << best_ratio
              << ",\"best_first\":" << best_first << ",\"best_widths\":[";
    for (std::size_t i = 0; i < best_ds.size(); ++i) {
      if (i) std::cout << ',';
      std::cout << best_ds[i];
    }
    std::cout << "],\"violation_of_2m_bound\":" << (violation ? "true" : "false");
    if (violation) {
      std::cout << ",\"violation_bound\":" << violation_bound << ",\"violation_widths\":[";
      for (std::size_t i = 0; i < violation_ds.size(); ++i) {
        if (i) std::cout << ',';
        std::cout << violation_ds[i];
      }
      std::cout << ']';
    }
    std::cout << '}';
  }
  std::cout << "\n  ],\n"
            << "  \"interpretation\": \"Finite falsification of a least-positive surrogate only. Absence of a counterexample is not a theorem, and the surrogate does not estimate the successor after 2k.\"\n"
            << "}\n";
}
