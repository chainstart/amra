// Exact-membership finite scan for the full inhomogeneous L=2 Fejer bridge.
//
// For every prime p=k+d in (k,2k), the parity-safe half-width is b=d/2.
// We enumerate the global centered lift H directly, so membership and h are
// decided by integer arithmetic.  Only the final triangular mass uses long
// double.  This is a finite diagnostic, not an asymptotic proof of S<2.

#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
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
    if (argc != 5) {
        std::cerr << "usage: scan K C_NUM C_DEN K_POWER\n";
        return 2;
    }
    const int k = std::stoi(argv[1]);
    const int c_numerator = std::stoi(argv[2]);
    const int c_denominator = std::stoi(argv[3]);
    const int k_power = std::stoi(argv[4]);
    if (k <= 2 || c_numerator <= 0 || c_denominator <= 0 || k_power < 0)
        return 2;

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

    const Big c_num_power = integer_power(Big(c_numerator), m);
    const Big c_den_power = integer_power(Big(c_denominator), m);
    const Big k_factor = integer_power(Big(k), k_power);
    const Big h_numerator = k_factor * c_num_power * period;
    const Big h_denominator = c_den_power * width_product;
    const Big h_big = (h_numerator + h_denominator - 1) / h_denominator;
    if (!h_big.fits_slong_p() || h_big > std::numeric_limits<int64_t>::max())
        throw std::runtime_error("h exceeds int64 scan range");
    if (2 * h_big >= period)
        throw std::runtime_error("h is outside Fejer alias range");
    const int64_t h = h_big.get_si();

    uint64_t admitted_positive = 0;
    std::vector<uint64_t> support_histogram(m + 1, 0);
    long double positive_weight = 0.0L;
    for (int64_t global_lift = 1; global_lift < h; ++global_lift) {
        long double local_weight = 1.0L;
        int support = 0;
        bool admitted = true;
        for (int i = 0; i < m; ++i) {
            const int p = moduli[i];
            const int d = widths[i];
            int residue = static_cast<int>(global_lift % p);
            if (2 * residue > p) residue -= p;
            const int absolute = std::abs(residue);
            if (2 * absolute >= d) {
                admitted = false;
                break;
            }
            support += residue != 0;
            local_weight *= (2.0L * (d - 2 * absolute)) /
                            (static_cast<long double>(d) * d);
        }
        if (!admitted) continue;
        ++admitted_positive;
        ++support_histogram[support];
        positive_weight += (1.0L - static_cast<long double>(global_lift) / h) *
                           local_weight;
    }

    long double origin_weight = 1.0L;
    for (int d : widths) origin_weight *= 2.0L / d;
    const long double p_float = std::stold(period.get_str());
    const long double s_value = p_float / h *
                                (origin_weight + 2.0L * positive_weight);

    std::cout << std::setprecision(18);
    std::cout << "{\n";
    std::cout << "  \"classification\": \"finite_full_inhomogeneous_exact_membership_scan_only\",\n";
    std::cout << "  \"k\": " << k << ",\n";
    std::cout << "  \"C\": \"" << c_numerator << "/" << c_denominator << "\",\n";
    std::cout << "  \"k_power\": " << k_power << ",\n";
    std::cout << "  \"m\": " << m << ",\n";
    std::cout << "  \"primes\": [";
    for (int i = 0; i < m; ++i) {
        if (i) std::cout << ", ";
        std::cout << moduli[i];
    }
    std::cout << "],\n";
    std::cout << "  \"widths\": [";
    for (int i = 0; i < m; ++i) {
        if (i) std::cout << ", ";
        std::cout << widths[i];
    }
    std::cout << "],\n";
    std::cout << "  \"P\": \"" << period.get_str() << "\",\n";
    std::cout << "  \"D_integer\": \"" << width_product.get_str() << "\",\n";
    std::cout << "  \"h\": " << h << ",\n";
    std::cout << "  \"admitted_positive_H\": " << admitted_positive << ",\n";
    std::cout << "  \"support_histogram_positive\": {";
    bool first = true;
    for (int support = 0; support <= m; ++support) {
        if (!support_histogram[support]) continue;
        if (!first) std::cout << ", ";
        first = false;
        std::cout << "\"" << support << "\": " << support_histogram[support];
    }
    std::cout << "},\n";
    std::cout << "  \"S_long_double\": " << s_value << ",\n";
    std::cout << "  \"S_lt_2\": " << (s_value < 2 ? "true" : "false") << "\n";
    std::cout << "}\n";
    return 0;
}
