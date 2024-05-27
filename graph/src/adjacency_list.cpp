#include "../include/adjacency_list.hpp"
#include <iostream>

namespace adj_list {

graph from_edge_list(std::vector<std::pair<int, int>> edges, int n) {
  graph adj_list;
  adj_list.assign(n, std::vector<int>());
  for (auto &[u, v] : edges) adj_list[u].push_back(v);
  return adj_list;
}

std::vector<double> page_rank(const graph &g, int iterations, double damping_factor) {
  int n = g.size();
  std::vector<double> ranks(n, 1.0 / n);
  std::vector<double> new_ranks(n, 0.0);

  while (iterations--) {
    for (double &rank : new_ranks)
      rank = (1.0 - damping_factor) / n;
    for (int u = 0; u < n; u++) {
      int out_degree = g[u].size();
      if (!out_degree) continue;
      double share = ranks[u] / out_degree;
      for (int v : g[u])
        new_ranks[v] += damping_factor * share;
    }                                                                     
    ranks = new_ranks;
    std::fill(new_ranks.begin(), new_ranks.end(), 0.0);
  }
  return ranks;
}

std::vector<int> assign_size(const std::vector<double> &ranks, int min_size, int max_size) {
  std::vector<int> sizes(ranks.size(), min_size);
  if (ranks.empty()) {std::cerr << "No ranks provided.\n"; return sizes;}

  double min_rank = *std::min_element(ranks.begin(), ranks.end());
  double max_rank = *std::max_element(ranks.begin(), ranks.end());

  if (min_rank == max_rank) {std::cerr << "All ranks are equal.\n"; return sizes;}

  for(int i = 0; i < ranks.size(); i++)
    sizes[i] = min_size + 
      static_cast<int>((ranks[i] - min_rank) / (max_rank - min_rank) * (max_size - min_size));

  return sizes;
}

} // namespace adj_list
