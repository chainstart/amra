#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

namespace {

using i64 = std::int64_t;
using i128 = __int128_t;
using u64 = std::uint64_t;

constexpr int kVertexCount = 9;
constexpr int kMaskCount = 1 << kVertexCount;
constexpr int kChannelCount = 4;
constexpr int kKrylovOrder = 5;
constexpr int kRepeatedNeighbourhoodMask =
    (1 << 1) | (1 << 5) | (1 << 6) | (1 << 7) | (1 << 8);
constexpr std::array<char, 8> kMagic = {
    'A', 'M', '2', 'S', 'D', 'P', '1', '\n',
};
constexpr std::array<std::pair<int, int>, 19> kBaseEdges = {{
    {0, 4},
    {1, 5},
    {2, 5},
    {1, 6},
    {2, 6},
    {5, 6},
    {0, 7},
    {1, 7},
    {3, 7},
    {4, 7},
    {5, 7},
    {6, 7},
    {0, 8},
    {1, 8},
    {3, 8},
    {4, 8},
    {5, 8},
    {6, 8},
    {7, 8},
}};
constexpr int kFirstForcedEdge = 0;
constexpr int kSecondForcedEdge = 2;

using PartitionLabels = std::array<int, kVertexCount>;
using CountVector = std::array<i64, kChannelCount>;
using KrylovValues = std::array<i64, kKrylovOrder>;

u64 encode_partition(const PartitionLabels& labels) {
    u64 encoded = 0;
    for (int vertex = 0; vertex < kVertexCount; ++vertex) {
        encoded |= static_cast<u64>(labels[vertex]) << (4 * vertex);
    }
    return encoded;
}

PartitionLabels decode_partition(u64 encoded) {
    PartitionLabels labels{};
    for (int vertex = 0; vertex < kVertexCount; ++vertex) {
        labels[vertex] =
            static_cast<int>((encoded >> (4 * vertex)) & 15);
    }
    return labels;
}

u64 canonical_partition(PartitionLabels labels) {
    PartitionLabels relabel;
    relabel.fill(-1);
    int next_label = 0;
    for (int& label : labels) {
        if (relabel[label] < 0) {
            relabel[label] = next_label++;
        }
        label = relabel[label];
    }
    return encode_partition(labels);
}

std::pair<bool, u64> apply_star(u64 encoded, int selected_mask) {
    PartitionLabels labels = decode_partition(encoded);
    int seen_labels = 0;
    int representative = -1;
    int selected_count = 0;
    for (int vertex = 0; vertex < kVertexCount; ++vertex) {
        if (!(selected_mask & (1 << vertex))) {
            continue;
        }
        const int label = labels[vertex];
        if (seen_labels & (1 << label)) {
            return {false, 0};
        }
        seen_labels |= 1 << label;
        if (representative < 0) {
            representative = label;
        }
        ++selected_count;
    }
    if (selected_count < 2) {
        return {true, encoded};
    }
    for (int& label : labels) {
        if (
            label != representative
            && (seen_labels & (1 << label))
        ) {
            label = representative;
        }
    }
    return {true, canonical_partition(labels)};
}

class DisjointSet {
  public:
    DisjointSet() {
        std::iota(parent_.begin(), parent_.end(), 0);
    }

    int find(int vertex) {
        if (parent_[vertex] != vertex) {
            parent_[vertex] = find(parent_[vertex]);
        }
        return parent_[vertex];
    }

    bool unite(int left, int right) {
        left = find(left);
        right = find(right);
        if (left == right) {
            return false;
        }
        parent_[left] = right;
        return true;
    }

  private:
    std::array<int, kVertexCount> parent_{};
};

i64 checked_add(i64 left, i64 right) {
    const i128 value = static_cast<i128>(left) + right;
    if (value > INT64_MAX || value < INT64_MIN) {
        throw std::overflow_error("signed 64-bit addition overflow");
    }
    return static_cast<i64>(value);
}

i64 checked_multiply(i64 left, i64 right) {
    const i128 value = static_cast<i128>(left) * right;
    if (value > INT64_MAX || value < INT64_MIN) {
        throw std::overflow_error("signed 64-bit multiplication overflow");
    }
    return static_cast<i64>(value);
}

std::map<u64, CountVector> build_base_distribution() {
    std::map<u64, CountVector> distribution;
    for (int subset = 0; subset < (1 << kBaseEdges.size()); ++subset) {
        DisjointSet components;
        bool is_forest = true;
        for (
            int edge_index = 0;
            edge_index < static_cast<int>(kBaseEdges.size());
            ++edge_index
        ) {
            if (!(subset & (1 << edge_index))) {
                continue;
            }
            const auto [left, right] = kBaseEdges[edge_index];
            if (!components.unite(left, right)) {
                is_forest = false;
                break;
            }
        }
        if (!is_forest) {
            continue;
        }

        PartitionLabels labels{};
        std::map<int, int> canonical_labels;
        int next_label = 0;
        for (int vertex = 0; vertex < kVertexCount; ++vertex) {
            const int root = components.find(vertex);
            const auto [iterator, inserted] =
                canonical_labels.emplace(root, next_label);
            if (inserted) {
                ++next_label;
            }
            labels[vertex] = iterator->second;
        }

        CountVector& counts = distribution[encode_partition(labels)];
        ++counts[0];
        if (subset & (1 << kFirstForcedEdge)) {
            ++counts[1];
        }
        if (subset & (1 << kSecondForcedEdge)) {
            ++counts[2];
        }
        if (
            (subset & (1 << kFirstForcedEdge))
            && (subset & (1 << kSecondForcedEdge))
        ) {
            ++counts[3];
        }
    }
    return distribution;
}

void generate_partitions(
    int position,
    int maximum_label,
    PartitionLabels& labels,
    std::vector<u64>& output
) {
    if (position == kVertexCount) {
        output.push_back(encode_partition(labels));
        return;
    }
    for (int label = 0; label <= maximum_label + 1; ++label) {
        labels[position] = label;
        generate_partitions(
            position + 1,
            std::max(maximum_label, label),
            labels,
            output
        );
    }
}

std::array<i128, kKrylovOrder> forward_differences(
    std::array<i128, kKrylovOrder> values
) {
    std::array<i128, kKrylovOrder> differences{};
    for (int degree = 0; degree < kKrylovOrder; ++degree) {
        differences[degree] = values[0];
        for (
            int index = 0;
            index < kKrylovOrder - degree - 1;
            ++index
        ) {
            values[index] = values[index + 1] - values[index];
        }
    }
    return differences;
}

void write_i64(std::ofstream& output, i64 value) {
    output.write(
        reinterpret_cast<const char*>(&value),
        sizeof(value)
    );
    if (!output) {
        throw std::runtime_error("failed to write kernel output");
    }
}

}  // namespace

int main(int argc, char** argv) {
    try {
        if (argc != 2) {
            throw std::runtime_error(
                "usage: opg_uniform_forest_two_star_kernel OUTPUT"
            );
        }

        const auto base_distribution = build_base_distribution();
        CountVector base_totals{};
        for (const auto& [partition, vector] : base_distribution) {
            static_cast<void>(partition);
            for (int channel = 0; channel < kChannelCount; ++channel) {
                base_totals[channel] = checked_add(
                    base_totals[channel],
                    vector[channel]
                );
            }
        }
        if (
            base_distribution.size() != 3430
            || base_totals
                != CountVector{54124, 19726, 21496, 7834}
        ) {
            throw std::runtime_error(
                "independent base-forest distribution regression"
            );
        }

        std::vector<u64> partitions;
        PartitionLabels labels{};
        labels[0] = 0;
        generate_partitions(1, 0, labels, partitions);
        if (partitions.size() != 21147) {
            throw std::runtime_error("Bell(9) partition count regression");
        }
        std::unordered_map<u64, int> partition_indexes;
        partition_indexes.reserve(partitions.size() * 2);
        for (
            int index = 0;
            index < static_cast<int>(partitions.size());
            ++index
        ) {
            partition_indexes[partitions[index]] = index;
        }

        std::vector<KrylovValues> future_weights(partitions.size());
        for (KrylovValues& weights : future_weights) {
            weights[0] = 1;
        }
        for (
            int twin_count = 1;
            twin_count < kKrylovOrder;
            ++twin_count
        ) {
            for (
                int index = 0;
                index < static_cast<int>(partitions.size());
                ++index
            ) {
                i64 total = 0;
                for (
                    int selected = kRepeatedNeighbourhoodMask;
                    ;
                    selected =
                        (selected - 1) & kRepeatedNeighbourhoodMask
                ) {
                    const auto [valid, target] =
                        apply_star(partitions[index], selected);
                    if (valid) {
                        total = checked_add(
                            total,
                            future_weights[
                                partition_indexes.at(target)
                            ][twin_count - 1]
                        );
                    }
                    if (selected == 0) {
                        break;
                    }
                }
                future_weights[index][twin_count] = total;
            }
        }

        const std::size_t raw_size =
            static_cast<std::size_t>(kKrylovOrder)
            * kChannelCount * kMaskCount * kMaskCount;
        std::vector<i64> raw(raw_size);
        const auto cell = [&raw](
            int twin_count,
            int channel,
            int first_mask,
            int second_mask
        ) -> i64& {
            const std::size_t index =
                (
                    (
                        static_cast<std::size_t>(twin_count)
                        * kChannelCount
                        + channel
                    )
                    * kMaskCount
                    + first_mask
                )
                * kMaskCount
                + second_mask;
            return raw[index];
        };

        i64 legal_selected_pair_count = 0;
        for (const auto& [partition, vector] : base_distribution) {
            for (
                int first_selected = 0;
                first_selected < kMaskCount;
                ++first_selected
            ) {
                const auto [first_valid, after_first] =
                    apply_star(partition, first_selected);
                if (!first_valid) {
                    continue;
                }
                for (
                    int second_selected = 0;
                    second_selected < kMaskCount;
                    ++second_selected
                ) {
                    const auto [second_valid, after_second] =
                        apply_star(after_first, second_selected);
                    if (!second_valid) {
                        continue;
                    }
                    legal_selected_pair_count = checked_add(
                        legal_selected_pair_count,
                        1
                    );
                    const int target_index =
                        partition_indexes.at(after_second);
                    for (
                        int twin_count = 0;
                        twin_count < kKrylovOrder;
                        ++twin_count
                    ) {
                        for (
                            int channel = 0;
                            channel < kChannelCount;
                            ++channel
                        ) {
                            i64& target = cell(
                                twin_count,
                                channel,
                                first_selected,
                                second_selected
                            );
                            target = checked_add(
                                target,
                                checked_multiply(
                                    vector[channel],
                                    future_weights[target_index][
                                        twin_count
                                    ]
                                )
                            );
                        }
                    }
                }
            }
        }
        if (legal_selected_pair_count != 20823456) {
            throw std::runtime_error(
                "legal selected-edge-pair count regression"
            );
        }

        for (
            int twin_count = 0;
            twin_count < kKrylovOrder;
            ++twin_count
        ) {
            for (int channel = 0; channel < kChannelCount; ++channel) {
                for (int bit = 0; bit < kVertexCount; ++bit) {
                    for (
                        int first_mask = 0;
                        first_mask < kMaskCount;
                        ++first_mask
                    ) {
                        if (!(first_mask & (1 << bit))) {
                            continue;
                        }
                        for (
                            int second_mask = 0;
                            second_mask < kMaskCount;
                            ++second_mask
                        ) {
                            i64& target = cell(
                                twin_count,
                                channel,
                                first_mask,
                                second_mask
                            );
                            target = checked_add(
                                target,
                                cell(
                                    twin_count,
                                    channel,
                                    first_mask ^ (1 << bit),
                                    second_mask
                                )
                            );
                        }
                    }
                }
                for (int bit = 0; bit < kVertexCount; ++bit) {
                    for (
                        int second_mask = 0;
                        second_mask < kMaskCount;
                        ++second_mask
                    ) {
                        if (!(second_mask & (1 << bit))) {
                            continue;
                        }
                        for (
                            int first_mask = 0;
                            first_mask < kMaskCount;
                            ++first_mask
                        ) {
                            i64& target = cell(
                                twin_count,
                                channel,
                                first_mask,
                                second_mask
                            );
                            target = checked_add(
                                target,
                                cell(
                                    twin_count,
                                    channel,
                                    first_mask,
                                    second_mask ^ (1 << bit)
                                )
                            );
                        }
                    }
                }
            }
        }

        for (
            int twin_count = 0;
            twin_count < kKrylovOrder;
            ++twin_count
        ) {
            for (int channel = 0; channel < kChannelCount; ++channel) {
                for (
                    int first_mask = 0;
                    first_mask < kMaskCount;
                    ++first_mask
                ) {
                    for (
                        int second_mask = 0;
                        second_mask < kMaskCount;
                        ++second_mask
                    ) {
                        if (
                            cell(
                                twin_count,
                                channel,
                                first_mask,
                                second_mask
                            )
                            != cell(
                                twin_count,
                                channel,
                                second_mask,
                                first_mask
                            )
                        ) {
                            throw std::runtime_error(
                                "two-star symmetry regression"
                            );
                        }
                    }
                }
            }
        }

        std::ofstream output(argv[1], std::ios::binary);
        if (!output) {
            throw std::runtime_error("failed to open kernel output");
        }
        output.write(kMagic.data(), kMagic.size());
        constexpr i64 row_count =
            static_cast<i64>(kMaskCount) * (kMaskCount + 1) / 2;
        constexpr i64 column_count =
            2 + kChannelCount * kKrylovOrder;
        write_i64(output, row_count);
        write_i64(output, column_count);
        write_i64(output, legal_selected_pair_count);

        i64 written_rows = 0;
        for (
            int first_mask = 0;
            first_mask < kMaskCount;
            ++first_mask
        ) {
            for (
                int second_mask = first_mask;
                second_mask < kMaskCount;
                ++second_mask
            ) {
                write_i64(output, first_mask);
                write_i64(output, second_mask);
                for (
                    int channel = 0;
                    channel < kChannelCount;
                    ++channel
                ) {
                    std::array<i128, kKrylovOrder> normalized{};
                    i64 scale = 1296;
                    for (
                        int twin_count = 0;
                        twin_count < kKrylovOrder;
                        ++twin_count
                    ) {
                        normalized[twin_count] =
                            static_cast<i128>(
                                cell(
                                    twin_count,
                                    channel,
                                    first_mask,
                                    second_mask
                                )
                            )
                            * scale;
                        scale /= 6;
                    }
                    const auto differences =
                        forward_differences(normalized);
                    for (const i128 value : differences) {
                        if (value > INT64_MAX || value < INT64_MIN) {
                            throw std::overflow_error(
                                "Newton coefficient exceeds signed 64-bit"
                            );
                        }
                        write_i64(output, static_cast<i64>(value));
                    }
                }
                ++written_rows;
            }
        }
        if (written_rows != row_count) {
            throw std::runtime_error("unordered mask-pair count regression");
        }
        output.close();
        if (!output) {
            throw std::runtime_error("failed to close kernel output");
        }
        std::cout
            << "rows=" << written_rows
            << " legal_selected_pairs=" << legal_selected_pair_count
            << '\n';
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 2;
    }
}
