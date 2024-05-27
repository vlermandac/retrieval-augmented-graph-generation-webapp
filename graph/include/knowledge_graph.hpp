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

using Unordered_json = nlohmann::ordered_json;
using Str = const std::string&;
using Node_ptr = std::shared_ptr<Node>;
using Edge_ptr = std::shared_ptr<Edge>;

class KnowledgeGraph {

public:
  KnowledgeGraph() = default;
  KnowledgeGraph(const Json& triplet_chunks);
  Json to_graphology_json();
  void to_graphology_json(Str path);
  void read_graph(Str path);
  void update_edges(std::vector<int> id_list);
  void update_nodes();

private:
  // Graph representations
  adj_list::graph adj_list;
  Json graphology_json;

  // Graph data
  std::vector<Node_ptr> nodes;
  std::vector<Edge_ptr> edges;
  std::vector<std::pair<int, int>> edge_list;

  // Mappings
  std::unordered_map<std::string, int> node_index;
  std::unordered_map<int, Node_ptr> ref_nodes;
  std::unordered_map<int, std::vector<Edge_ptr>> id_ref_edges;

  // Internal methods
  void get_layout(unsigned int width, unsigned int height, unsigned int iters_count);
  void add_triplet(Str node1, Str relation, Str node2, int id);
  void add_node(Str node_name);
};

} // namespace ns

#endif // KNOWLEDGEGRAPH_HPP
