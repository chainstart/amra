// Finite exact-membership scan of the homogeneous weighted-prefix lemma.
// Integer arithmetic decides P, D, h, and every local support condition.
// The nonnegative triangular weights and final ratio use long double.

#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <vector>
#include <gmpxx.h>

using Big = mpz_class;

static std::vector<int> primes_below(int limit) {
    std::vector<bool> prime(limit, true);
    if (limit > 0) prime[0] = false;
    if (limit > 1) prime[1] = false;
    for (int p = 2; 1LL * p * p < limit; ++p) {
        if (!prime[p]) continue;
        for (int n = p * p; n < limit; n += p) prime[n] = false;
    }
    std::vector<int> answer;
    for (int p = 2; p < limit; ++p) if (prime[p]) answer.push_back(p);
    return answer;
}

static Big integer_power(Big base, int exponent) {
    Big answer = 1;
    for (int i = 0; i < exponent; ++i) answer *= base;
    return answer;
}

int main(int argc, char** argv) {
    if (argc != 4) {
        std::cerr << "usage: scan K C_NUM C_DEN\n";
        return 2;
    }
    const int k = std::stoi(argv[1]);
    const int c_num = std::stoi(argv[2]);
    const int c_den = std::stoi(argv[3]);
    if (k <= 2 || c_num <= 0 || c_den <= 0) return 2;

    std::vector<int> moduli;
    std::vector<int> widths;
    Big period = 1;
    Big width_product = 1;
    for (int p : primes_below(2 * k)) {
        if (p <= k) continue;
        moduli.push_back(p);
        widths.push_back(p - k);
        period *= p;
        width_product *= p - k;
    }
    if (moduli.empty()) throw std::runtime_error("empty full prime system");
    const int m = static_cast<int>(moduli.size());
    const Big h_num = integer_power(Big(c_num), m) * period;
    const Big h_den = integer_power(Big(c_den), m) * width_product;
    const Big h_big = (h_num + h_den - 1) / h_den;
    if (!h_big.fits_slong_p() || h_big > std::numeric_limits<int64_t>::max())
        throw std::runtime_error("h exceeds int64 scan range");
    if (h_big >= period) throw std::runtime_error("h is outside one-period range");
    const int64_t h = h_big.get_si();

    long double l_g = 1.0L;
    for (int i = 0; i < m; ++i) {
        const int d = widths[i];
        const int r = (d + 1) / 2;
        const int s = d + 1 - r;
        l_g *= static_cast<long double>(moduli[i]) * (r + s) /
               (2.0L * r * s);
    }

    uint64_t admitted_positive = 0;
    long double positive_mass = 0.0L;
    for (int64_t ell = 1; ell < h; ++ell) {
        long double local_product = 1.0L;
        for (int i = 0; i < m; ++i) {
            const int p = moduli[i];
            const int d = widths[i];
            const int r = (d + 1) / 2;
            const int s = d + 1 - r;
            int residue = static_cast<int>(ell % p);
            if (2 * residue > p) residue -= p;
            const int absolute = std::abs(residue);
            long double numerator = 0.0L;
            if (absolute < r)
                numerator += static_cast<long double>(s) * (r - absolute) / r;
            if (absolute < s)
                numerator += static_cast<long double>(r) * (s - absolute) / s;
            const long double phi = numerator / (r + s);
            if (phi == 0.0L) {
                local_product = 0.0L;
                break;
            }
            local_product *= phi;
        }
        if (local_product == 0.0L) continue;
        ++admitted_positive;
        positive_mass += (1.0L - static_cast<long double>(ell) / h) *
                         local_product;
    }

    const long double q_h = 1.0L + 2.0L * positive_mass;
    const long double normalized_ratio = q_h * l_g / h;
    std::cout << std::setprecision(18);
    std::cout << "{\n";
    std::cout << "  \"classification\": \"finite_discrete_positive_prefix_diagnostic_only\",\n";
    std::cout << "  \"k\": " << k << ",\n";
    std::cout << "  \"C\": \"" << c_num << "/" << c_den << "\",\n";
    std::cout << "  \"m\": " << m << ",\n";
    std::cout << "  \"P\": \"" << period.get_str() << "\",\n";
    std::cout << "  \"D_integer\": \"" << width_product.get_str() << "\",\n";
    std::cout << "  \"h\": " << h << ",\n";
    std::cout << "  \"L_G\": " << l_g << ",\n";
    std::cout << "  \"admitted_positive_ell\": " << admitted_positive << ",\n";
    std::cout << "  \"Q_h\": " << q_h << ",\n";
    std::cout << "  \"Q_h_L_G_over_h\": " << normalized_ratio << ",\n";
    std::cout << "  \"factor_two_prefix_bound\": "
              << (normalized_ratio < 2.0L ? "true" : "false") << "\n";
    std::cout << "}\n";
    return 0;
}
