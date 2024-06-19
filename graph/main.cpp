#include "include/httplib.h"
#include "include/knowledge_graph.hpp"
#include <filesystem>
#include <fstream>
#include <iostream>
#include <memory>
#include <nlohmann/json.hpp>
#include <string>
#include <vector>

#ifndef DATA_DIR
#define DATA_DIR "."
#endif

using Json = nlohmann::json;
using KG = ns::KnowledgeGraph;
using Str = std::string;

const Str DATA = Str(DATA_DIR);
Str path(const Str &index) { return DATA + "/" + index; }
bool exists(const Str &index) { return std::ifstream(path(index)).good(); }
Str CURR_INDEX = "";
std::unique_ptr<KG> graph(nullptr);
httplib::Server svr;

bool validate_req(const httplib::Request &req, httplib::Response &res) {
  if (!req.has_header("Content-Type") ||
      req.get_header_value("Content-Type") != "application/json") {
    res.set_content("415 Unsupported Media Type", "text/plain");
    res.status = 415;
    return false;
  }
  return true;
}

void generate_graph(const std::string &index, const Json &tl) {
  graph = std::make_unique<KG>(tl);
  if (graph->num_nodes == 0)
    return;
  std::filesystem::create_directories(path(index));
  graph->save_graphology_json(path(index) + "/graph.json");
  CURR_INDEX = index;
}

void retrieve_graph(const Str &index) {
  if (CURR_INDEX == index)
    return;
  graph = std::make_unique<KG>();
  std::ifstream file(path(index) + "/graph.json");
  Json json = Json::parse(file);
  graph->read_graph(json);
  CURR_INDEX = index;
}

void handle_generate(const httplib::Request &req, httplib::Response &res) {
  if (!validate_req(req, res)) return;
  std::cout << "HTTP POST /generate received\n";
  try {
    auto json = Json::parse(req.body);
    Str index = json["index"].get<Str>();
    generate_graph(index, json["triplet_lists"]);
    if (graph->num_nodes == 0) {
      res.set_content("error, empty graph", "text/plain");
      return;
    }
    res.set_content(Str("graph generated at " + path(index)), "text/plain");
  } catch (const std::exception &e) {
    res.set_content(e.what(), "text/plain");
    res.status = 400;
  }
}

void handle_get(const httplib::Request &req, httplib::Response &res) {
  std::cout << "HTTP POST /get received\n";
  if (!validate_req(req, res)) return;
  try {
    auto json = Json::parse(req.body);
    Str index = json["index"].get<Str>();
    if (!exists(index)) {
      res.set_content("error index not found", "text/plain");
      return;
    }
    retrieve_graph(index);
    std::vector<int> values = json["values"].get<std::vector<int>>();
    std::cout << "values: " << values.size() << std::endl;
    for (int v : values)
      std::cout << v << std::endl;
    if (!values.empty()) {
      res.set_content(graph->get_subgraph(values).dump(2), "application/json");
      return;
    }
    res.set_content(graph->get_graphology_json().dump(2), "application/json");
  } catch (const std::exception &e) {
    res.set_content(e.what(), "text/plain");
    res.status = 400;
  }
}

void handle_delete(const httplib::Request &req, httplib::Response &res) {
  std::cout << "HTTP POST /delete received\n";
  if (!validate_req(req, res)) return;
  try {
    auto json = Json::parse(req.body);
    Str index = json["index"].get<Str>();
    if (!exists(index)) {
      Str message = "error index " + index + " not found";
      res.set_content(message, "text/plain");
      return;
    }
    std::filesystem::remove_all(path(index));
    Str message = "index " + index + " deleted";
    res.set_content(message, "text/plain");
  } catch (const std::exception &e) {
    res.set_content(e.what(), "text/plain");
    res.status = 400;
  }
}

int main() {
  const Str &host = "localhost";
  const int &port = 8080;

  // (index: str, JSON: TripletLists) -> str
  svr.Post("/generate", handle_generate);

  // (index: str, values: List[int]) -> Graphology-JSON
  svr.Post("/get", handle_get);

  // (index: str) -> void
  svr.Post("/delete", handle_delete);

  std::cout << "Server started at http://" << host << ":" << port << std::endl;
  svr.listen(host, port);
  return 0;
}
