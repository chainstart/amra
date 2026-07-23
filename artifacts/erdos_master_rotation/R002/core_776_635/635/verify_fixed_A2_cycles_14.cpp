#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <vector>

// Complete multiplier enumeration for fixed valuation A=2.
//
// A non-backtracking m-cycle in the swap graph supplies positive odd h_i
// with product(h_i)<2^m.  Conversely, the two cyclic seeds are uniquely
// determined by h.  This program enumerates every such tuple for m=13,14,
// extending the inherited complete Python certificate through m=12.

namespace {

bool is_prime(std::uint64_t n) {
  if (n < 2) return false;
  if ((n & 1U) == 0) return n == 2;
  for (std::uint64_t d = 3; d * d <= n; d += 2)
    if (n % d == 0) return false;
  return true;
}

struct Audit {
  int length = 0;
  std::uint64_t tuples = 0;
  std::uint64_t integral_closed_walks = 0;
  std::uint64_t prime_closed_walks = 0;
  std::uint64_t nonbacktracking = 0;
  std::uint64_t immediate_returns = 0;
};

std::uint64_t power2(int exponent) {
  return std::uint64_t{1} << exponent;
}

void test_tuple(const std::vector<std::uint64_t>& h, Audit& audit) {
  ++audit.tuples;
  const int m = static_cast<int>(h.size());
  std::uint64_t product = 1;
  for (auto value : h) product *= value;
  const std::uint64_t denominator = power2(m) - product;
  if (denominator == 0) return;

  std::uint64_t forward = 0;
  std::uint64_t prefix = 1;
  for (int i = 0; i < m; ++i) {
    forward += power2(m - 1 - i) * prefix;
    if (i + 1 < m) prefix *= h[i];
  }
  std::uint64_t reverse = 0;
  std::uint64_t suffix = 1;
  for (int i = 0; i < m; ++i) {
    reverse += power2(m - 1 - i) * suffix;
    if (i + 1 < m) suffix *= h[m - 1 - i];
  }
  if (forward % denominator || reverse % denominator) return;

  std::uint64_t p = forward / denominator;
  std::uint64_t q = reverse / denominator;
  const auto p0 = p;
  const auto q0 = q;
  std::vector<std::pair<std::uint64_t, std::uint64_t>> edges;
  edges.reserve(m);
  bool integral = true;
  bool all_prime = true;
  bool distinct_edges = true;
  for (int i = 0; i < m; ++i) {
    edges.push_back(std::minmax(p, q));
    all_prime = all_prime && is_prime(p) && is_prime(q);
    distinct_edges = distinct_edges && p != q;
    const std::uint64_t p_numerator = 2 * p - 1;
    const std::uint64_t q_numerator = h[i] * q + 1;
    if (p_numerator % h[i] || q_numerator % 2) {
      integral = false;
      break;
    }
    p = p_numerator / h[i];
    q = q_numerator / 2;
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
  if (distinct_edges && !immediate_return) ++audit.nonbacktracking;
}

void enumerate(
    int index,
    std::uint64_t product,
    std::uint64_t limit,
    std::vector<std::uint64_t>& tuple,
    Audit& audit) {
  if (index == audit.length) {
    test_tuple(tuple, audit);
    return;
  }
  const std::uint64_t maximum = (limit - 1) / product;
  for (std::uint64_t value = 1; value <= maximum; value += 2) {
    tuple[index] = value;
    enumerate(index + 1, product * value, limit, tuple, audit);
  }
}

Audit audit_length(int length) {
  Audit audit;
  audit.length = length;
  std::vector<std::uint64_t> tuple(length, 1);
  enumerate(0, 1, power2(length), tuple, audit);
  return audit;
}

}  // namespace

int main() {
  const auto a13 = audit_length(13);
  const auto a14 = audit_length(14);
  if (a13.tuples != 21939776ULL || a14.tuples != 97963582ULL)
    return 2;
  if (a13.nonbacktracking != 0 || a14.nonbacktracking != 0)
    return 3;

  std::cout
      << "{\n"
      << "  \"schema\": \"amra.erdos635.fixed-A2-cycles-13-14.v1\",\n"
      << "  \"status\": \"PASS\",\n"
      << "  \"A\": 2,\n"
      << "  \"audits\": [\n";
  for (int index = 0; index < 2; ++index) {
    const Audit& a = index == 0 ? a13 : a14;
    std::cout
        << "    {\"length\": " << a.length
        << ", \"multiplier_tuples\": " << a.tuples
        << ", \"integral_closed_walks\": " << a.integral_closed_walks
        << ", \"prime_closed_walks\": " << a.prime_closed_walks
        << ", \"immediate_returns\": " << a.immediate_returns
        << ", \"nonbacktracking_candidates\": " << a.nonbacktracking
        << "}" << (index == 0 ? "," : "") << "\n";
  }
  std::cout
      << "  ],\n"
      << "  \"conclusion\": \"No non-backtracking fixed-A=2 cycle has "
         "length 13 or 14\",\n"
      << "  \"scope\": \"Complete multiplier enumeration for lengths 13 "
         "and 14; together with the inherited certificate this reaches "
         "length 14, not unbounded length.\"\n"
      << "}\n";
}
