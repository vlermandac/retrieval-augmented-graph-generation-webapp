#ifndef KNOWLEDGEGRAPH_HPP                                                
#define KNOWLEDGEGRAPH_HPP                                                
#include "adjacency_list.hpp"
#include "json_defs.hpp"
#include <string>
#include <vector>
#include <utility>
#include <memory>
#include <unordered_map>
#include <nlohmann/json.hpp>

namespace ns{

using Str = const std::string&;
using Node_ptr = std::shared_ptr<Node>;
using Edge_ptr = std::shared_ptr<Edge>;

class KnowledgeGraph {

public:
  KnowledgeGraph(const Json& json, const std::string& read_from);
  void read_triplets(const Json& triplet_chunks);
  void read_graph(const Json& json);
  Json get_graph();
  Json get_graphology_json(std::vector<Node> node_list, std::vector<Edge> edge_list);
  Json get_subgraph(const std::vector<int>& id_list);
  void save_graph(Str path);
  int num_nodes = 0;

private:
  // Graph representations
  adjacency_list adj_list;

  // Graph data
  std::vector<Node_ptr> nodes;
  std::vector<Edge_ptr> edges;
  std::vector<std::pair<int, int>> edge_list;

  // Mappings
  std::unordered_map<std::string, int> node_index;
  std::unordered_map<int, Node_ptr> ref_nodes;
  std::unordered_map<int, std::vector<Edge_ptr>> ref_edges;

  // Internal methods
  void get_layout();
  void add_triplet(Str node1, Str relation, Str node2, int id);
  void add_node(Str node_name);
};

} // namespace ns

#endif // KNOWLEDGEGRAPH_HPP
