#include "include/knowledge_graph.hpp"
#include "include/httplib.h"
#include "include/json_defs.hpp"
#include <fstream>
#include <vector>
#include <memory>
#include <iostream>
#include <nlohmann/json.hpp>

using Json = nlohmann::json;
using KG = ns::KnowledgeGraph;

std::unique_ptr<KG> graph(nullptr);

void generate_graph() {
  if (std::ifstream("../data/pristine_graph.json").good()) {
    std::ifstream file("../data/pristine_graph.json");
    graph = std::make_unique<KG>();
    graph->read_graph("../data/pristine_graph.json");
    return;
  }
  std::ifstream file("../data/triplets.json");
  graph = std::make_unique<KG>(Json::parse(file));
  graph->to_graphology_json("../data/pristine_graph.json");
}

void update_graph(const std::vector<int>& id_list) {
  graph->update_edges(id_list);
}

void handle_generate(const httplib::Request& req, httplib::Response& res) {
  if (graph) res.set_content("\nPrevious graph will be overwritten\n", "text/plain");
  generate_graph();
  res.set_content("Graph generated successfully", "text/plain");
}

void handle_update(const httplib::Request& req, httplib::Response& res) {
  if (!graph) { res.set_content("No graph found to update", "text/plain"); return; }
  if (!req.has_header("Content-Type") || req.get_header_value("Content-Type") != "application/json") {
    res.set_content("Content-Type must be application/json", "text/plain");
    res.status = 415; return; // Unsupported Media Type
  }
  try {
    auto json_payload = Json::parse(req.body);
    if (!json_payload.contains("values") || !json_payload["values"].is_array()) {
      res.set_content("Invalid JSON payload: 'values' array missing or not an array", "text/plain");
      res.status = 400; return;
    }
    std::vector<int> values = json_payload["values"].get<std::vector<int>>();
    update_graph(values);
    res.set_content(graph->to_graphology_json().dump(2), "application/json");
  }
  catch (const std::exception &e) {
    res.status = 400;
    res.set_content(std::string("Invalid JSON payload: ") + e.what(), "text/plain");
  }
}

void handle_get(const httplib::Request& req, httplib::Response& res) {
  if (!graph) { res.set_content("No graph found", "text/plain"); return; }
  res.set_content(graph->to_graphology_json().dump(2), "application/json");
}

int main() {
  httplib::Server svr;
  const int& port = 8080;

  svr.Get("/generate", handle_generate);
  svr.Post("/update", handle_update);
  svr.Get("/get", handle_get);

  std::cout << "Server started at http://localhost:" << port << std::endl;
  generate_graph();
  svr.listen("0.0.0.0", port);

  return 0;
}
