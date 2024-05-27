#include "../include/knowledge_graph.hpp"
#include "../include/layout.hpp"
#include <fstream>
#include <iostream>

namespace ns {

KnowledgeGraph::KnowledgeGraph(const Json& json) {  // TODO: validate json structure
  for (const auto& triplets_list : json) {
    int id = triplets_list["id"];
    for(const auto& triplets : triplets_list["triplets"])
      for(const auto& triplet : triplets)
        add_triplet(triplet["entity1"], triplet["relation"], triplet["entity2"], id);
  }
  this->adj_list = adj_list::from_edge_list(this->edge_list, node_index.size());
  this->get_layout(1920, 800, 5000);
}

void KnowledgeGraph::add_triplet(Str node1, Str relation, Str node2, int id) {
  add_node(node1); add_node(node2);
  this->edge_list.push_back({node_index[node1], node_index[node2]});
  Attributes_e atts(id, 1, true, relation, "gray");
  auto e = std::make_shared<Edge>(node1, node2, atts);
  this->edges.push_back(e);
  this->id_ref_edges[id].push_back(e);
}

void KnowledgeGraph::add_node(Str node_name) {
  if (node_index.count(node_name)) return;
  int node_mapping = node_index.size() + 1;
  node_index[node_name] = node_mapping;
  Attributes_n atts(node_mapping, 3, 0.0, 0.0, node_name, "blue");
  auto n = std::make_shared<Node>(node_name, atts);
  this->nodes.push_back(n);
  this->ref_nodes[node_mapping] = n;
}

void KnowledgeGraph::get_layout(unsigned int width, unsigned int height, unsigned int iters_count) {
    std::vector<double> ranks = adj_list::page_rank(adj_list, 100, 0.85);
    std::vector<int> sizes = adj_list::assign_size(ranks, 4, 12);

    for (Node_ptr &node : nodes)
      node->attributes.size = sizes[node->attributes.id];
    std::cout << "sizes calculated\n";

    std::vector<layout::Point2D> pos = layout::fruchterman_reingold(
        adj_list, width, height, ranks, iters_count, 30);
    std::cout << "layout calculated\n";

    for (Node_ptr &node : this->nodes)
      node->coords(pos[node->attributes.id].x, pos[node->attributes.id].y);
    std::cout << "postitions setted\n";
}

void KnowledgeGraph::update_edges(std::vector<int> id_list){
  if (id_list.empty())
    { std::cout << "No edge id provided for update.\n"; return; }
  for (int id : id_list) 
    if (id_ref_edges.count(id))
      for (Edge_ptr &edge : id_ref_edges[id])
        edge->attributes.color = "cyan";
}

void KnowledgeGraph::update_nodes(){
}

Json KnowledgeGraph::to_graphology_json() {
  std::vector<Node> node_list;
  for (Node_ptr node : nodes)
    node_list.push_back(*node);

  std::vector<Edge> edge_list;
  for (Edge_ptr edge : edges)
    edge_list.push_back(*edge);

  Json graph;
  graph["attributes"] = Json::object();
  graph["nodes"] = node_list;
  graph["edges"] = edge_list;
  graph["options"] = {{"multi", true}};

  return this->graphology_json = graph;
}

void KnowledgeGraph::to_graphology_json(Str path) {
  Str new_path = "./graph.json";
  std::cout << "Graph copy created at " << new_path << std::endl;
  std::cout<<"reading from triplets.json\n";
  this->to_graphology_json();
  std::fstream file;
  file.open(new_path, std::ios::out);
  file << this->graphology_json.dump(2);
}

void KnowledgeGraph::read_graph(Str path) {
  if (this->node_index.size() > 0) 
    { std::cout << "Graph already loaded. Only one graph can be read.\n"; return; }

  std::cout << "Reading graph from " << path << std::endl;
  std::ifstream file(path);
  Json json = Json::parse(file);

  std::vector<Node> parsed_n = json["nodes"].get<std::vector<Node>>();
  std::vector<Edge> parsed_e = json["edges"].get<std::vector<Edge>>();

  for (const Node &node : parsed_n) {
    this->node_index[node.key] = node.attributes.id;
    auto n = std::make_shared<Node>(node.attributes.label, node.attributes);
    this->nodes.push_back(n);
    this->ref_nodes[node.attributes.id] = n;
  }

  for (const Edge &edge : parsed_e) {
    this->edge_list.push_back({node_index[edge.source], node_index[edge.target]});
    Attributes_e atts = edge.attributes;
    auto e = std::make_shared<Edge>(edge.source, edge.target, atts);
    this->edges.push_back(e);
    this->id_ref_edges[atts.chunk_id].push_back(e);
  }

  this->adj_list = adj_list::from_edge_list(this->edge_list, node_index.size());
}

} // namespace ns
