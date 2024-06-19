#ifndef ADJACENCYLIST_HPP
#define ADJACENCYLIST_HPP

#include <vector>

class adjacency_list {                                                    

public:                                                                   
  adjacency_list(int n);
  std::vector<int>& operator[](int index);
  const std::vector<int>& operator[](int index) const;
  std::vector<double> page_rank();
  std::vector<int> assign_size(const std::vector<double> &ranks, int min_size, int max_size);
  void add_edge(int u, int v);
  std::vector<std::vector<int>> adj_list;                               
};

#endif // ADJACENCYLIST_HPP
