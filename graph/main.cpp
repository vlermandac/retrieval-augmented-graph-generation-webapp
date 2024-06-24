#include "include/httplib.h"
#include "include/knowledge_graph.hpp"
#include <filesystem>
#include <fstream>
#include <iostream>
#include <memory>
#include <nlohmann/json.hpp>
#include <string>
#include <vector>
#include <mutex>

#ifndef DATA_DIR
#define DATA_DIR "."
#endif

using Json = nlohmann::json;
using KG = ns::KnowledgeGraph;
using Str = std::string;

const Str DATA = Str(DATA_DIR);
Str path(const Str &index) { return DATA + "/" + index; }
bool exists(const Str &index) { return std::ifstream(path(index)).good(); }
std::unique_ptr<KG> graph;
httplib::Server svr;
std::mutex request_mutex;

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
  graph = std::make_unique<KG>(tl, "triplet");
  if (graph->num_nodes == 0)
    return;
  std::filesystem::create_directories(path(index));
  graph->save_graph(path(index) + "/graph.json");
}

void retrieve_graph(Str &index) {
  std::cout << "retrieving graph\n";
  std::ifstream file(path(index) + "/graph.json");
  Json json = Json::parse(file);
  graph = std::make_unique<KG>(json, "graph");
}

void handle_generate(const httplib::Request &req, httplib::Response &res) {
  std::lock_guard<std::mutex> guard(request_mutex);
  if (!validate_req(req, res)) return;
  std::cout << "HTTP POST /generate received\n";
  try {
    auto json = Json::parse(req.body);
    std::cout<<"Request body parsed\n";
    Str index = json["index"].get<Str>();
    std::cout<<"Index: "<<index<<" parsed"<<std::endl;
    generate_graph(index, json["triplet_lists"]);
    if (graph->num_nodes == 0) {
      res.set_content("error, empty graph", "text/plain");
      return;
    }
    res.set_content(Str("graph generated at " + path(index)), "text/plain");
  } catch (const std::exception &e) {
    res.set_content(e.what(), "text/plain");
    res.status = 400;
    std::cout<<"Request failed\n";
    std::cout<<e.what()<<std::endl;
    std::cout<<req.body<<std::endl;
  }
}

void handle_get(const httplib::Request &req, httplib::Response &res) {
  std::lock_guard<std::mutex> guard(request_mutex);
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
    std::cout << "values size: " << values.size() << std::endl;
    for (int v : values)
      std::cout << v << std::endl;
    if (!values.empty()) {
      res.set_content(graph->get_subgraph(values).dump(2), "application/json");
      return;
    }
    res.set_content(graph->get_graph().dump(2), "application/json");
  } catch (const std::exception &e) {
    res.set_content(e.what(), "text/plain");
    res.status = 400;
    std::cout<<"Request failed\n";
    std::cout<<e.what()<<std::endl;
  }
}

void handle_delete(const httplib::Request &req, httplib::Response &res) {
  std::lock_guard<std::mutex> guard(request_mutex);
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
  const Str &host = "0.0.0.0";
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
