# ifndef JSON_DEFS_HPP
# define JSON_DEFS_HPP
#include <nlohmann/json.hpp>

namespace ns {

using Json = nlohmann::json;
  
struct Attributes_n {
  int id, size;
  double x, y;
  std::string label, color;
  Attributes_n() : id(0), size(10), x(0), y(0), label(""), color("") {}
  Attributes_n(int id, int size, double x, double y, std::string label, std::string color)
    : id(id), size(size), x(x), y(y), label(label), color(color) {}
};
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(Attributes_n, id, size, x, y, label, color);

struct Attributes_e {
  int chunk_id, size;
  bool forceLabel;
  std::string label, color;
  Attributes_e() : chunk_id(0), size(1), forceLabel(false), label(""), color("") { }
  Attributes_e(int chunk_id, int size, bool forceLabel, std::string label, std::string color)
    : chunk_id(chunk_id), size(size), forceLabel(forceLabel), label(label), color(color) {}
};
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(Attributes_e, chunk_id, size, forceLabel, label, color);

struct Node {
  std::string key;
  Attributes_n attributes;
  Node() : key(), attributes() {}
  Node(std::string key, Attributes_n attributes) : key(key), attributes(attributes) {}
  void coords(double x, double y) { attributes.x = x; attributes.y = y; }
};
void to_json(Json& j, const Node& n);
void from_json(const Json& j, Node& n);

struct Edge {
  std::string source, target;
  Attributes_e attributes;
  Edge() : source(), target(), attributes() {}
  Edge(std::string source, std::string target, Attributes_e attributes)
    : source(source), target(target), attributes(attributes) {}
};
void to_json(Json& j, const Edge& e);
void from_json(const Json& j, Edge& e);

} // namespace ns

# endif // JSON_DEFS_HPP
