#include "../include/json_defs.hpp"

namespace ns {

  void to_json(Json& j, const Node& n){
    j = Json{{"key", n.key}, {"attributes", n.attributes}};
  }

  void from_json(const Json& j, Node& n){
    j.at("key").get_to(n.key);
    j.at("attributes").get_to(n.attributes);
  }

  void to_json(Json& j, const Edge& e){
    j = Json{{"source", e.source}, {"target", e.target}, {"attributes", e.attributes}};
  }

  void from_json(const Json& j, Edge& e){
    j.at("source").get_to(e.source);
    j.at("target").get_to(e.target);
    j.at("attributes").get_to(e.attributes);
  }

} 
