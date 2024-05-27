#pragma once
#include "../include/layout.hpp"
#include <utility>
#include <vector>

namespace layout {
class FruchtermanReingold {
public:
    FruchtermanReingold(const adj_list& g, double k = 15.0);
    void operator()(std::vector<Point2D>& positions, std::vector<double>& page_rank);
private:
    const adj_list& graph;
    const double k_;
    const double k_squared;
    double temp;
    std::vector<std::pair<int, int>> edges;
    std::vector<Vector2D> mvmts;
};
}
