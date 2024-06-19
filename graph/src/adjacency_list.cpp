#include "../include/adjacency_list.hpp"
#include <iostream>
#include <algorithm>
#include <vector>

adjacency_list::adjacency_list(int n) : adj_list((n + 1), std::vector<int>()) {}

std::vector<int>& adjacency_list::operator[](int index) {                          
    return adj_list[index];                                           
}                                                                     

const std::vector<int>& adjacency_list::operator[](int index) const {              
    return adj_list[index];                                           
}                                                                     

void adjacency_list::add_edge(int u, int v) {                                         
    adj_list[u].push_back(v);                                         
}                                                                     

std::vector<double> adjacency_list::page_rank() {
  int n = static_cast<int>(this->adj_list.size());
  std::vector<double> ranks(n, 1.0 / n), new_ranks(n, 0.0);
  int iterations = 100;
  double damping_factor = 0.85;
  while (iterations--) {
    for (double &rank : new_ranks)
      rank = (1.0 - damping_factor) / static_cast<double>(n);
    for (int u = 0; u < n; u++) {
      int out_degree = this->adj_list[u].size();
      if (!out_degree) continue;
      double share = ranks[u] / static_cast<double>(out_degree);
      for (int v : this->adj_list[u])
        new_ranks[v] += damping_factor * share;
    }                                                                     
    ranks = new_ranks;
    std::fill(new_ranks.begin(), new_ranks.end(), 0.0);
  }
  return ranks;
}

std::vector<int> adjacency_list::assign_size(const std::vector<double> &ranks, int min_size, int max_size) {
  std::vector<int> sizes(ranks.size(), min_size);
  if (ranks.empty()) {std::cerr << "No ranks provided.\n"; return sizes;}
  double min_rank = *std::min_element(ranks.begin(), ranks.end());
  double max_rank = *std::max_element(ranks.begin(), ranks.end());
  if (min_rank == max_rank) {std::cerr << "All ranks are equal.\n"; return sizes;}
  for(unsigned int i = 0; i < ranks.size(); i++)
    sizes[i] = min_size + 
      static_cast<int>((ranks[i] - min_rank) / (max_rank - min_rank) * (max_size - min_size));
  return sizes;
}
