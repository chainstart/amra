// Exact membership scan for the L=2 weighted small-CRT bridge.
//
// The tested interval is small enough to enumerate H directly.  Membership,
// h, P, and D use integer arithmetic; only the final triangular mass is
// accumulated in long double.  This is stronger than relying on floating
// LLL enumeration for completeness.

#include <algorithm>
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

static std::string show(const Big& value) {
    return value.get_str();
}

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

int main(int argc, char** argv) {
    if (argc != 4 && argc != 5) {
        std::cerr << "usage: scan K DELTA C_NUM [C_DEN]\n";
        return 2;
    }
    const int k = std::stoi(argv[1]);
    const int delta = std::stoi(argv[2]);
    const int c_numerator = std::stoi(argv[3]);
    const int c_denominator = argc == 5 ? std::stoi(argv[4]) : 1;
    if (k <= 0 || delta <= 0 || c_numerator <= 0 || c_denominator <= 0) return 2;

    std::vector<int> moduli;
    for (int p : primes_below(2 * k)) {
        const int d = p - k;
        if (d >= delta && d < 2 * delta) moduli.push_back(p);
    }
    if (moduli.empty()) throw std::runtime_error("empty actual prime block");
    const int q = int(moduli.size());
    const int b2 = 2 * ((delta - 1) / 2) + 1;
    Big period = 1;
    Big width_product = 1;
    Big c_power_numerator = 1;
    Big c_power_denominator = 1;
    for (int p : moduli) {
        period *= p;
        width_product *= (p - k);
        c_power_numerator *= c_numerator;
        c_power_denominator *= c_denominator;
    }
    const Big h_numerator = Big(k) * k * c_power_numerator * period;
    const Big h_denominator = c_power_denominator * width_product;
    const Big h_big = (h_numerator + h_denominator - 1) / h_denominator;
    if (!h_big.fits_slong_p() || h_big > std::numeric_limits<int64_t>::max())
        throw std::runtime_error("h exceeds int64 scan range");
    const int64_t h = h_big.get_si();
    if (2 * h_big >= period) throw std::runtime_error("h is outside Fejer alias range");

    uint64_t admitted_positive = 0;
    std::vector<uint64_t> support_histogram(q + 1, 0);
    long double positive_weight = 0.0L;
    for (int64_t global_lift = 1; global_lift < h; ++global_lift) {
        long double local_weight = 1.0L;
        int support = 0;
        bool admitted = true;
        for (int p : moduli) {
            int residue = int(global_lift % p);
            if (2 * residue > p) residue -= p;
            const int absolute = std::abs(residue);
            if (2 * absolute >= b2) {
                admitted = false;
                break;
            }
            support += residue != 0;
            local_weight *= (1.0L - (2.0L * absolute) / b2) * (2.0L / b2);
        }
        if (!admitted) continue;
        ++admitted_positive;
        ++support_histogram[support];
        positive_weight += (1.0L - (long double)global_lift / h) * local_weight;
    }

    long double p_float = std::stold(period.get_str());
    const long double origin_local = std::pow(2.0L / b2, q);
    const long double s_value = p_float / h * (origin_local + 2.0L * positive_weight);
    const uint64_t admitted_total = 1 + 2 * admitted_positive;

    std::cout << std::setprecision(18);
    std::cout << "{\n";
    std::cout << "  \"classification\": \"finite_exact_membership_scan_only\",\n";
    std::cout << "  \"k\": " << k << ",\n";
    std::cout << "  \"Delta\": " << delta << ",\n";
    std::cout << "  \"C\": \"" << c_numerator << "/" << c_denominator << "\",\n";
    std::cout << "  \"q\": " << q << ",\n";
    std::cout << "  \"P\": \"" << show(period) << "\",\n";
    std::cout << "  \"D\": \"" << show(width_product) << "\",\n";
    std::cout << "  \"h\": " << h << ",\n";
    std::cout << "  \"admitted_positive_H\": " << admitted_positive << ",\n";
    std::cout << "  \"admitted_total_H\": " << admitted_total << ",\n";
    std::cout << "  \"support_histogram_positive\": {";
    bool first = true;
    for (int support = 0; support <= q; ++support) {
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
