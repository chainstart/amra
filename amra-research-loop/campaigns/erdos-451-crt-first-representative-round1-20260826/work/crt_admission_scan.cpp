#include <algorithm>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <string>
#include <vector>

namespace {

std::vector<int> primes_up_to(int n) {
    std::vector<bool> composite(static_cast<std::size_t>(n + 1), false);
    std::vector<int> primes;
    for (int p = 2; p <= n; ++p) {
        if (composite[static_cast<std::size_t>(p)]) continue;
        primes.push_back(p);
        if (static_cast<std::int64_t>(p) * p <= n) {
            for (int q = p * p; q <= n; q += p) {
                composite[static_cast<std::size_t>(q)] = true;
            }
        }
    }
    return primes;
}

std::vector<int> interval_primes(const std::vector<int>& primes, int k) {
    std::vector<int> result;
    for (int p : primes) {
        if (p > k && p < 2 * k) result.push_back(p);
    }
    return result;
}

bool allowed_residue(int r, int k) {
    return r == 0 || r > k;
}

bool is_survivor(std::uint64_t n, int k, const std::vector<int>& ps) {
    for (int p : ps) {
        const int r = static_cast<int>(n % static_cast<std::uint64_t>(p));
        if (r >= 1 && r <= k) return false;
    }
    return true;
}

long double log_inverse_density(int k, const std::vector<int>& ps) {
    long double answer = 0.0L;
    for (int p : ps) {
        answer += std::log(static_cast<long double>(p))
                - std::log(static_cast<long double>(p - k));
    }
    return answer;
}

struct CorrelationSummary {
    int horizon = 0;
    int zero_displacements = 0;
    int max_h = 0;
    long double max_log_ratio = -std::numeric_limits<long double>::infinity();
    int min_h = 0;
    long double min_log_ratio = std::numeric_limits<long double>::infinity();
};

CorrelationSummary correlation_summary(int k, const std::vector<int>& ps) {
    CorrelationSummary summary;
    summary.horizon = 4 * k;
    const long double log_d = -log_inverse_density(k, ps);
    for (int h = 1; h <= summary.horizon; ++h) {
        bool zero = false;
        long double log_joint = 0.0L;
        for (int p : ps) {
            int count = 0;
            const int hp = h % p;
            for (int r = 0; r < p; ++r) {
                if (allowed_residue(r, k)
                    && allowed_residue((r + hp) % p, k)) {
                    ++count;
                }
            }
            if (count == 0) {
                zero = true;
                break;
            }
            log_joint += std::log(static_cast<long double>(count))
                       - std::log(static_cast<long double>(p));
        }
        if (zero) {
            ++summary.zero_displacements;
            continue;
        }
        const long double log_ratio = log_joint - 2.0L * log_d;
        if (log_ratio > summary.max_log_ratio) {
            summary.max_log_ratio = log_ratio;
            summary.max_h = h;
        }
        if (log_ratio < summary.min_log_ratio) {
            summary.min_log_ratio = log_ratio;
            summary.min_h = h;
        }
    }
    return summary;
}

void write_number(std::ostream& out, long double value) {
    out << std::setprecision(18) << static_cast<double>(value);
}

}  // namespace

int main(int argc, char** argv) {
    if (argc != 3) {
        std::cerr << "usage: crt_admission_scan OUTPUT_JSON SCAN_CAP\n";
        return 2;
    }
    const std::string output_path = argv[1];
    const std::uint64_t scan_cap = std::stoull(argv[2]);
    const std::vector<int> scan_ks = {20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75};
    const std::vector<int> barrier_ks = {100, 300, 1000, 3000, 10000, 30000};
    const auto all_primes = primes_up_to(60000);

    std::ofstream out(output_path);
    if (!out) {
        std::cerr << "cannot open output: " << output_path << "\n";
        return 3;
    }
    out << "{\n";
    out << "  \"schema_version\": \"erdos451.crt_admission.v1\",\n";
    out << "  \"scan_cap\": " << scan_cap << ",\n";
    out << "  \"exact_scans\": [\n";
    for (std::size_t index = 0; index < scan_ks.size(); ++index) {
        const int k = scan_ks[index];
        const auto ps = interval_primes(all_primes, k);
        const long double log_inv_d = log_inverse_density(k, ps);
        std::uint64_t first = 0;
        std::uint64_t tested = 0;
        for (std::uint64_t n = static_cast<std::uint64_t>(2 * k + 1);
             n <= scan_cap; ++n) {
            ++tested;
            if (is_survivor(n, k, ps)) {
                first = n;
                break;
            }
        }
        const auto corr = correlation_summary(k, ps);
        out << "    {\"k\": " << k
            << ", \"prime_count\": " << ps.size()
            << ", \"log_inverse_density\": ";
        write_number(out, log_inv_d);
        out << ", \"inverse_density\": ";
        write_number(out, std::exp(log_inv_d));
        out << ", \"first_survivor\": ";
        if (first == 0) out << "null"; else out << first;
        out << ", \"certified_minimal_through\": "
            << (first == 0 ? scan_cap : first)
            << ", \"candidates_tested\": " << tested;
        if (first != 0) {
            out << ", \"log_first_over_inverse_density\": ";
            write_number(out, std::log(static_cast<long double>(first)) - log_inv_d);
        }
        out << ", \"correlation\": {\"horizon\": " << corr.horizon
            << ", \"zero_displacements\": " << corr.zero_displacements
            << ", \"max_h\": " << corr.max_h
            << ", \"max_log_J_over_D2\": ";
        write_number(out, corr.max_log_ratio);
        out << ", \"min_positive_h\": " << corr.min_h
            << ", \"min_positive_log_J_over_D2\": ";
        write_number(out, corr.min_log_ratio);
        out << "}}";
        if (index + 1 != scan_ks.size()) out << ',';
        out << "\n";
    }
    out << "  ],\n";
    out << "  \"support_barrier\": [\n";
    const long double log4 = std::log(4.0L);
    for (std::size_t index = 0; index < barrier_ks.size(); ++index) {
        const int k = barrier_ks[index];
        const auto ps = interval_primes(all_primes, k);
        const long double log_k = std::log(static_cast<long double>(k));
        const long double conjectural_log_h = log4 * k / log_k;
        const int max_support = static_cast<int>(std::floor(conjectural_log_h / log_k));
        out << "    {\"k\": " << k
            << ", \"prime_count\": " << ps.size()
            << ", \"log_inverse_density\": ";
        write_number(out, log_inverse_density(k, ps));
        out << ", \"conjectural_log_H\": ";
        write_number(out, conjectural_log_h);
        out << ", \"max_squarefree_support_below_H\": " << max_support
            << ", \"support_fraction\": ";
        write_number(out, ps.empty() ? 0.0L
                                     : static_cast<long double>(max_support) / ps.size());
        out << "}";
        if (index + 1 != barrier_ks.size()) out << ',';
        out << "\n";
    }
    out << "  ],\n";
    out << "  \"interpretation_boundary\": [\n";
    out << "    \"Exact first-survivor scans are finite evidence only.\",\n";
    out << "    \"Pair correlations are averaged over the full CRT period and do not control the fixed initial translate.\",\n";
    out << "    \"The support ledger is a rigorous obstruction to uncompressed low-level inclusion-exclusion, not a lower bound for every conceivable sieve.\"\n";
    out << "  ]\n";
    out << "}\n";
    return 0;
}
