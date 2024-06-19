#include "../include/knowledge_graph.hpp"
#include "../include/layout.hpp"
#include <fstream>
#include <iostream>

namespace ns {

KnowledgeGraph::KnowledgeGraph(const Json &json) {
  std::vector<TripletList> triplet_list = json.get<std::vector<TripletList>>();
  if (triplet_list.empty()) return;
  for (const auto &triplets_with_id : triplet_list)
    for (const auto &triplet : triplets_with_id.triplets)
      add_triplet(triplet.entity1, triplet.relation, triplet.entity2,
                  triplets_with_id.id);
  this->get_layout();
}

void KnowledgeGraph::add_triplet(Str node1, Str relation, Str node2, int id) {
  add_node(node1);
  add_node(node2);
  this->edge_list.push_back({node_index[node1], node_index[node2]});
  Attributes_e atts(id, 1, false, relation, "#626880");
  auto e = std::make_shared<Edge>(node1, node2, atts);
  this->edges.push_back(e);
  this->ref_edges[id].push_back(e);
}

void KnowledgeGraph::add_node(Str node_name) {
  if (node_index.count(node_name)) return;
  node_index[node_name] = ++(this->num_nodes);
  Attributes_n atts(num_nodes, 3, 0.0, 0.0, node_name, "#babbf1");
  auto n = std::make_shared<Node>(node_name, atts);
  this->nodes.push_back(n);
  this->ref_nodes[num_nodes] = n;
}

void KnowledgeGraph::get_layout() {
  this->adj_list = std::make_unique<adjacency_list>(num_nodes);
  for (auto &[u, v] : edge_list)
    adj_list->add_edge(u, v);
  std::vector<double> ranks = adj_list->page_rank();
  std::vector<int> sizes = adj_list->assign_size(ranks, 4, 12);
  for (Node_ptr &n : nodes)
    n->attributes.size = sizes[n->attributes.id];
  std::vector<layout::Point2D> pos =
      layout::fr(adj_list->adj_list, ranks, 1000, 2000);
  for (Node_ptr &n : this->nodes)
    n->coords(pos[n->attributes.id].x, pos[n->attributes.id].y);
}

Json KnowledgeGraph::get_graphology_json(std::vector<Node> node_list,
                                         std::vector<Edge> edge_list) {
  json_graph["attributes"] = Json::object();
  json_graph["nodes"] = node_list;
  json_graph["edges"] = edge_list;
  json_graph["options"] = {{"multi", true}};
  return this->json_graph;
}

Json KnowledgeGraph::get_graphology_json() {
  std::vector<Node> node_list;
  for (Node_ptr n : this->nodes)
    node_list.push_back(*n);
  std::vector<Edge> edge_list;
  for (Edge_ptr e : this->edges)
    edge_list.push_back(*e);
  return this->get_graphology_json(node_list, edge_list);
}

void KnowledgeGraph::save_graphology_json(Str path) {
  this->get_graphology_json();
  std::fstream file;
  file.open(path, std::ios::out);
  file << this->json_graph.dump(2);
}

Json KnowledgeGraph::get_subgraph(const std::vector<int> &id_list) {
  std::vector<Node> node_list;
  std::vector<Edge> edge_list;
  std::vector<bool> added(num_nodes, false);
  for (int id : id_list) {
    std::cout << "id: " << id << std::endl;
    if (ref_edges.count(id))
      for (Edge_ptr &e : ref_edges[id]) {
        edge_list.push_back(*e);
        int u = node_index[e->source];
        int v = node_index[e->target];
        if (added[u] || added[v]) continue;
        node_list.push_back(*ref_nodes[u]);
        node_list.push_back(*ref_nodes[v]);
        added[u] = added[v] = true;
      }
  }
  return get_graphology_json(node_list, edge_list);
}

void KnowledgeGraph::read_graph(const Json &json) {
  std::vector<Node> parsed_n = json["nodes"].get<std::vector<Node>>();
  std::vector<Edge> parsed_e = json["edges"].get<std::vector<Edge>>();
  this->num_nodes = parsed_n.size();
  for (const Node &n : parsed_n) {
    this->node_index[n.key] = n.attributes.id;
    auto np = std::make_shared<Node>(n.attributes.label, n.attributes);
    this->nodes.push_back(np);
    this->ref_nodes[n.attributes.id] = np;
  }
  for (const Edge &e : parsed_e) {
    this->edge_list.push_back({node_index[e.source], node_index[e.target]});
    Attributes_e atts = e.attributes;
    auto ep = std::make_shared<Edge>(e.source, e.target, atts);
    this->edges.push_back(ep);
    this->ref_edges[atts.chunk_id].push_back(ep);
  }
  this->get_layout();
}

} // namespace ns
