#ifndef ADJACENCYLIST_HPP
#define ADJACENCYLIST_HPP

#include <vector>
#include <utility>

namespace adj_list {

using graph = std::vector<std::vector<int>>;
graph from_edge_list(std::vector<std::pair<int, int>> edges, int n);
std::vector<double> page_rank(const graph &g, int iterations = 100, double damping_factor = 0.85);
std::vector<int> assign_size(const std::vector<double> &ranks, int min_size, int max_size);

}

#endif // ADJACENCYLIST_HPP
