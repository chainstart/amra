#include <algorithm>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iomanip>
#include <iostream>
#include <map>
#include <queue>
#include <string>
#include <utility>
#include <vector>

namespace {

std::vector<int> primes_up_to(int n) {
  std::vector<bool> composite(static_cast<size_t>(n) + 1, false);
  std::vector<int> primes;
  for (int i = 2; i <= n; ++i) {
    if (!composite[i]) {
      primes.push_back(i);
      if (static_cast<int64_t>(i) * i <= n) {
        for (int64_t j = static_cast<int64_t>(i) * i; j <= n; j += i) {
          composite[static_cast<size_t>(j)] = true;
        }
      }
    }
  }
  return primes;
}

bool carry_free(uint64_t n, uint64_t p) {
  const uint64_t half = (p - 1) / 2;
  while (n) {
    if (n % p > half) return false;
    n /= p;
  }
  return true;
}

struct Witness {
  uint64_t n = 0;
  uint64_t p = 0;
  uint64_t top_power = 0;
  uint64_t bad_power = 0;
};

Witness top_power_witness() {
  for (uint64_t n = 2; n <= 10000; ++n) {
    const auto ps = primes_up_to(static_cast<int>(n));
    for (uint64_t p : ps) {
      uint64_t top = p;
      while (top <= 2 * n / p) top *= p;
      if (n % top * 2 >= top) continue;
      for (uint64_t power = p; power < top; power *= p) {
        if (n % power * 2 >= power) return {n, p, top, power};
        if (power > top / p) break;
      }
    }
  }
  return {};
}

struct CrtTest {
  uint64_t modulus = 0;
  uint64_t accepted = 0;
  long double expected_density = 0;
  long double max_prefix_ratio = 0;
  uint64_t max_prefix_endpoint = 0;
};

CrtTest crt_prefix_test() {
  const std::vector<std::pair<uint64_t, int>> specs{{3, 3}, {5, 2}, {7, 2}};
  uint64_t modulus = 1;
  long double density = 1;
  for (const auto &[p, depth] : specs) {
    uint64_t power = 1;
    for (int j = 0; j < depth; ++j) power *= p;
    modulus *= power;
    const long double allowed = std::pow(static_cast<long double>((p + 1) / 2), depth);
    density *= allowed / power;
  }
  uint64_t accepted = 0;
  long double best_ratio = 0;
  uint64_t best_at = 0;
  for (uint64_t n = 0; n < modulus; ++n) {
    bool ok = true;
    for (const auto &[p, depth] : specs) {
      uint64_t x = n;
      const uint64_t half = (p - 1) / 2;
      for (int j = 0; j < depth; ++j) {
        if (x % p > half) ok = false;
        x /= p;
      }
    }
    if (ok) ++accepted;
    const uint64_t length = n + 1;
    if (length >= 100) {
      const long double ratio = accepted / (density * length);
      if (ratio > best_ratio) {
        best_ratio = ratio;
        best_at = length;
      }
    }
  }
  return {modulus, accepted, density, best_ratio, best_at};
}

void json_number_array(std::ostream &out, const std::vector<int> &values) {
  out << '[';
  for (size_t i = 0; i < values.size(); ++i) {
    if (i) out << ',';
    out << values[i];
  }
  out << ']';
}

}  // namespace

int main(int argc, char **argv) {
  if (argc != 3) {
    std::cerr << "usage: exact_carry_scan MAX_N OUTPUT_JSON\n";
    return 64;
  }
  const int n_max = std::stoi(argv[1]);
  const std::string output_path = argv[2];
  if (n_max < 2) return 65;

  const Witness witness = top_power_witness();
  const CrtTest crt = crt_prefix_test();
  std::cerr << "single-scale witness n=" << witness.n << " p=" << witness.p
            << " top=" << witness.top_power << " bad=" << witness.bad_power << '\n';
  std::cerr << "CRT modulus=" << crt.modulus << " prefix_ratio="
            << static_cast<double>(crt.max_prefix_ratio) << '\n';

  const auto primes = primes_up_to(n_max);
  std::vector<double> difference(static_cast<size_t>(n_max) + 2, 0.0);
  uint64_t interval_updates = 0;
  size_t prime_index = 0;
  for (int p_int : primes) {
    const int64_t p = p_int;
    const int64_t half = (p - 1) / 2;
    const int64_t limit = n_max / p;
    if (limit == 0) continue;

    std::vector<int64_t> stack;
    const int64_t first_limit = std::min(half, limit);
    stack.reserve(static_cast<size_t>(std::min<int64_t>(limit, 1000000)));
    for (int64_t first = 1; first <= first_limit; ++first) stack.push_back(first);
    const double weight = 1.0 / static_cast<double>(p);
    while (!stack.empty()) {
      const int64_t prefix = stack.back();
      stack.pop_back();
      const int64_t left = prefix * p;
      const int64_t right = std::min<int64_t>(n_max, left + half);
      difference[static_cast<size_t>(left)] += weight;
      difference[static_cast<size_t>(right + 1)] -= weight;
      ++interval_updates;

      if (prefix <= limit / p) {
        const int64_t child_base = prefix * p;
        const int64_t last_digit = std::min<int64_t>(half, limit - child_base);
        for (int64_t digit = 0; digit <= last_digit; ++digit) {
          stack.push_back(child_base + digit);
        }
      }
    }
    ++prime_index;
    if (prime_index % 1000000 == 0) {
      std::cerr << "processed_primes=" << prime_index
                << " intervals=" << interval_updates << '\n';
    }
  }

  using Entry = std::pair<double, int>;
  std::priority_queue<Entry, std::vector<Entry>, std::greater<Entry>> top;
  std::vector<Entry> records;
  std::vector<Entry> checkpoint_maxima;
  const std::vector<int> checkpoints{1000, 10000, 100000, 1000000, 10000000,
                                     100000000, n_max};
  size_t checkpoint_index = 0;
  double running = 0;
  double maximum = -1;
  int maximum_n = 1;
  for (int n = 1; n <= n_max; ++n) {
    running += difference[static_cast<size_t>(n)];
    if (running > maximum + 1e-12) {
      maximum = running;
      maximum_n = n;
      records.emplace_back(maximum, n);
    }
    if (top.size() < 25) {
      top.emplace(running, n);
    } else if (running > top.top().first) {
      top.pop();
      top.emplace(running, n);
    }
    while (checkpoint_index < checkpoints.size() && n == std::min(checkpoints[checkpoint_index], n_max)) {
      checkpoint_maxima.emplace_back(maximum, maximum_n);
      ++checkpoint_index;
      if (checkpoint_index < checkpoints.size() && checkpoints[checkpoint_index] > n_max && n == n_max) break;
    }
  }

  std::vector<Entry> top_values;
  while (!top.empty()) {
    top_values.push_back(top.top());
    top.pop();
  }
  std::sort(top_values.rbegin(), top_values.rend());

  std::vector<int> accepted_primes;
  std::map<int, long double> mass_by_digits;
  std::map<int, long double> mass_by_critical_exponent;
  for (int p : primes) {
    if (p > maximum_n) break;
    if (!carry_free(maximum_n, p)) continue;
    accepted_primes.push_back(p);
    uint64_t x = maximum_n;
    int digits = 0;
    while (x) {
      ++digits;
      x /= p;
    }
    mass_by_digits[digits] += 1.0L / p;
    uint64_t power = p;
    int exponent = 1;
    while (power <= static_cast<uint64_t>(maximum_n) / p &&
           power * p <= static_cast<uint64_t>(std::sqrt(maximum_n))) {
      power *= p;
      ++exponent;
    }
    mass_by_critical_exponent[exponent] += 1.0L / p;
  }

  std::ofstream out(output_path);
  out << std::setprecision(17);
  out << "{\n";
  out << "  \"schema_version\": \"amra.erdos377.exact-carry-scan.v1\",\n";
  out << "  \"epistemic_status\": \"finite exact predicate scan; not an all-n proof\",\n";
  out << "  \"max_n_scanned\": " << n_max << ",\n";
  out << "  \"prime_count\": " << primes.size() << ",\n";
  out << "  \"interval_updates\": " << interval_updates << ",\n";
  out << "  \"maximum\": {\"n\": " << maximum_n << ", \"value\": " << maximum << "},\n";
  out << "  \"accepted_primes_at_maximum\": ";
  json_number_array(out, accepted_primes);
  out << ",\n";
  out << "  \"mass_by_base_p_digit_count\": {";
  bool first = true;
  for (const auto &[key, value] : mass_by_digits) {
    if (!first) out << ',';
    first = false;
    out << '\"' << key << "\":" << static_cast<double>(value);
  }
  out << "},\n";
  out << "  \"mass_by_sqrt_critical_exponent\": {";
  first = true;
  for (const auto &[key, value] : mass_by_critical_exponent) {
    if (!first) out << ',';
    first = false;
    out << '\"' << key << "\":" << static_cast<double>(value);
  }
  out << "},\n";
  out << "  \"single_top_power_test\": {\"n\":" << witness.n << ",\"p\":"
      << witness.p << ",\"top_power\":" << witness.top_power
      << ",\"bad_lower_power\":" << witness.bad_power
      << ",\"conclusion\":\"M377-01 killed\"},\n";
  out << "  \"crt_prefix_test\": {\"modulus\":" << crt.modulus
      << ",\"accepted_full_period\":" << crt.accepted
      << ",\"product_density\":" << static_cast<double>(crt.expected_density)
      << ",\"max_prefix_to_product_ratio\":" << static_cast<double>(crt.max_prefix_ratio)
      << ",\"prefix_endpoint\":" << crt.max_prefix_endpoint
      << ",\"interpretation\":\"CRT gives exact full-period independence but not a pointwise or every-prefix bound\"},\n";
  out << "  \"record_count\": " << records.size() << ",\n";
  out << "  \"last_records\": [";
  const size_t record_start = records.size() > 30 ? records.size() - 30 : 0;
  for (size_t i = record_start; i < records.size(); ++i) {
    if (i > record_start) out << ',';
    out << "{\"n\":" << records[i].second << ",\"value\":" << records[i].first << '}';
  }
  out << "],\n";
  out << "  \"top_values\": [";
  for (size_t i = 0; i < top_values.size(); ++i) {
    if (i) out << ',';
    out << "{\"n\":" << top_values[i].second << ",\"value\":" << top_values[i].first << '}';
  }
  out << "]\n}\n";
  out.close();

  std::cout << "max_n=" << n_max << " maximum_n=" << maximum_n
            << " maximum=" << std::setprecision(12) << maximum
            << " accepted_primes=" << accepted_primes.size()
            << " intervals=" << interval_updates << '\n';
  return 0;
}
