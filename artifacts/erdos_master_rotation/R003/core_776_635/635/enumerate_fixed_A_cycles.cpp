#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <numeric>
#include <utility>
#include <vector>

// Complete fixed-(A,m) multiplier enumeration for the semiprime swap graph.
// This is a cycle generator used as the first stage of the short-bicyclic-core
// classification.  It has no prime cutoff: prod(h_i)<A^m makes the search
// finite and the two cyclic seeds are then forced.

namespace {

using u64 = std::uint64_t;
using u128 = __uint128_t;

bool is_prime(u64 n) {
  if (n < 2) return false;
  if ((n & 1U) == 0) return n == 2;
  for (u64 d = 3; d <= n / d; d += 2)
    if (n % d == 0) return false;
  return true;
}

u64 checked_power(u64 base, int exponent) {
  u128 result = 1;
  for (int i = 0; i < exponent; ++i) {
    result *= base;
    if (result > std::numeric_limits<u64>::max())
      throw std::overflow_error("A^m exceeds uint64");
  }
  return static_cast<u64>(result);
}

struct Audit {
  u64 A = 0;
  int length = 0;
  u64 limit = 0;
  u64 tuples = 0;
  u64 integral_closed_walks = 0;
  u64 prime_closed_walks = 0;
  u64 immediate_returns = 0;
  u64 nonbacktracking = 0;
  std::vector<std::vector<u64>> nonbacktracking_multipliers;
};

void test_tuple(const std::vector<u64>& h, Audit& audit) {
  ++audit.tuples;
  const int m = audit.length;
  u64 product = 1;
  for (u64 value : h) product *= value;
  const u64 denominator = audit.limit - product;
  if (denominator == 0) return;

  u128 forward = 0;
  u128 prefix = 1;
  for (int i = 0; i < m; ++i) {
    forward += static_cast<u128>(checked_power(audit.A, m - 1 - i))
               * prefix;
    if (i + 1 < m) prefix *= h[i];
  }
  u128 reverse = 0;
  u128 suffix = 1;
  for (int i = 0; i < m; ++i) {
    reverse += static_cast<u128>(checked_power(audit.A, m - 1 - i))
               * suffix;
    if (i + 1 < m) suffix *= h[m - 1 - i];
  }
  if (forward % denominator || reverse % denominator) return;
  if (forward / denominator > std::numeric_limits<u64>::max()
      || reverse / denominator > std::numeric_limits<u64>::max())
    throw std::overflow_error("seed exceeds uint64");

  u64 p = static_cast<u64>(forward / denominator);
  u64 q = static_cast<u64>(reverse / denominator);
  const u64 p0 = p, q0 = q;
  std::vector<std::pair<u64, u64>> edges;
  edges.reserve(m);
  bool integral = true, all_prime = true, valid_edges = true;
  for (int i = 0; i < m; ++i) {
    edges.push_back(std::minmax(p, q));
    all_prime = all_prime && is_prime(p) && is_prime(q);
    valid_edges = valid_edges && p != q;
    const u128 p_numerator = static_cast<u128>(audit.A) * p - 1;
    const u128 q_numerator = static_cast<u128>(h[i]) * q + 1;
    if (p_numerator % h[i] || q_numerator % audit.A) {
      integral = false;
      break;
    }
    if (p_numerator / h[i] > std::numeric_limits<u64>::max()
        || q_numerator / audit.A > std::numeric_limits<u64>::max())
      throw std::overflow_error("orbit exceeds uint64");
    p = static_cast<u64>(p_numerator / h[i]);
    q = static_cast<u64>(q_numerator / audit.A);
  }
  if (!integral || p != p0 || q != q0) return;
  ++audit.integral_closed_walks;
  if (!all_prime) return;
  ++audit.prime_closed_walks;

  bool immediate_return = false;
  for (int i = 0; i < m; ++i)
    if (edges[i] == edges[(i + m - 1) % m])
      immediate_return = true;
  if (immediate_return) ++audit.immediate_returns;
  if (valid_edges && !immediate_return) {
    ++audit.nonbacktracking;
    if (audit.nonbacktracking_multipliers.size() < 20)
      audit.nonbacktracking_multipliers.push_back(h);
  }
}

void enumerate(
    int index,
    u64 product,
    std::vector<u64>& tuple,
    Audit& audit) {
  if (index == audit.length) {
    test_tuple(tuple, audit);
    return;
  }
  const u64 maximum = (audit.limit - 1) / product;
  for (u64 value = 1; value <= maximum; value += 2) {
    tuple[index] = value;
    enumerate(index + 1, product * value, tuple, audit);
  }
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 3) {
    std::cerr << "usage: enumerate_fixed_A_cycles A length\n";
    return 2;
  }
  Audit audit;
  audit.A = std::stoull(argv[1]);
  audit.length = std::stoi(argv[2]);
  if (audit.A < 2 || (audit.A & (audit.A - 1)) != 0
      || audit.length < 2)
    return 2;
  audit.limit = checked_power(audit.A, audit.length);
  std::vector<u64> tuple(audit.length, 1);
  enumerate(0, 1, tuple, audit);

  std::cout
      << "{\"A\":" << audit.A
      << ",\"length\":" << audit.length
      << ",\"multiplier_tuples\":" << audit.tuples
      << ",\"integral_closed_walks\":" << audit.integral_closed_walks
      << ",\"prime_closed_walks\":" << audit.prime_closed_walks
      << ",\"immediate_returns\":" << audit.immediate_returns
      << ",\"nonbacktracking_candidates\":" << audit.nonbacktracking
      << ",\"sample_multipliers\":[";
  for (std::size_t i = 0; i < audit.nonbacktracking_multipliers.size(); ++i) {
    if (i) std::cout << ",";
    std::cout << "[";
    for (std::size_t j = 0; j < audit.nonbacktracking_multipliers[i].size();
         ++j) {
      if (j) std::cout << ",";
      std::cout << audit.nonbacktracking_multipliers[i][j];
    }
    std::cout << "]";
  }
  std::cout << "]}\n";
}
