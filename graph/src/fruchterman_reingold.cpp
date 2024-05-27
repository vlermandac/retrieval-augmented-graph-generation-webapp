#include "../include/fruchterman_reingold.hpp"
#include <algorithm>
#include <cmath>

namespace layout {

using std::vector;

FruchtermanReingold::FruchtermanReingold(const adj_list& g, double k) :
      graph(g), k_(k), k_squared(k * k), temp(10 * sqrt(g.size())), mvmts(graph.size()) {}

void FruchtermanReingold::operator()(vector<Point2D>& positions , std::vector<double>& page_rank) {
  Vector2D zero = { 0.0, 0.0 };
  fill(mvmts.begin(), mvmts.end(), zero);
  double pr_factor = 100;

  // Repulsion force between vertice pairs
  for (int i = 0; i < graph.size(); i++) {
    for (int j = i + 1; j < graph.size(); j++) {
      if (i == j) continue;
      Vector2D delta = positions[i] - positions[j];
      double distance = delta.norm();
      if (distance > 1000.0) continue; // > 1000.0: not worth computing
      double repulsion = (k_squared / distance) * (1 + pr_factor * (1 + std::pow(page_rank[i] + page_rank[j], 4)));
      mvmts[i] += delta / distance * repulsion;
      mvmts[j] -= delta / distance * repulsion;
    }
    // Attraction force between edges
    for (int u : graph[i]) {
      if (u > i) continue;
      Vector2D delta = positions[i] - positions[u];
      double distance = delta.norm();
      if (distance == 0.0) continue;
      double attraction = (distance * distance / k_)/(1 + pr_factor * (1 + std::pow(page_rank[i] + page_rank[u], 4)));
 
      mvmts[i] -= delta / distance * attraction;
      mvmts[u] += delta / distance * attraction;
    }
  }

  // Max movement capped by current temperature
  for (int i = 0; i < graph.size(); i++) {
    double mvmt_norm = mvmts[i].norm();
    if (mvmt_norm < 1.0) continue; // < 1.0: not worth computing
    double capped_mvmt_norm = std::min(mvmt_norm, temp);
    Vector2D capped_mvmt = mvmts[i] / mvmt_norm * capped_mvmt_norm;
    positions[i] += capped_mvmt;
  }

  temp = temp > 1.5 ? temp * 0.85 : 1.5; // Fast cool down until 1.5
}

} // namespace layout
