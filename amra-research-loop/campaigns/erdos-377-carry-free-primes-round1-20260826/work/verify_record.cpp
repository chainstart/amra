#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <vector>

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

int legendre_binomial_valuation(int n, int p) {
  int valuation = 0;
  int64_t power = p;
  while (power <= 2LL * n) {
    valuation += (2LL * n) / power - 2 * (n / power);
    if (power > 2LL * n / p) break;
    power *= p;
  }
  return valuation;
}

int main(int argc, char **argv) {
  if (argc != 2) return 64;
  const int n = std::stoi(argv[1]);
  const auto primes = primes_up_to(n);
  uint64_t count = 0;
  uint64_t prime_sum_mod_2_64 = 0;
  long double reciprocal_sum = 0;
  long double compensation = 0;
  for (int p : primes) {
    if (legendre_binomial_valuation(n, p) != 0) continue;
    ++count;
    prime_sum_mod_2_64 += static_cast<uint64_t>(p);
    const long double term = 1.0L / p - compensation;
    const long double next = reciprocal_sum + term;
    compensation = (next - reciprocal_sum) - term;
    reciprocal_sum = next;
  }
  std::cout << std::setprecision(18)
            << "{\"n\":" << n
            << ",\"accepted_prime_count\":" << count
            << ",\"reciprocal_sum\":" << static_cast<double>(reciprocal_sum)
            << ",\"prime_sum_mod_2_64\":" << prime_sum_mod_2_64 << "}\n";
}
