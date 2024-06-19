#pragma once
#include "layout.hpp"
#include <utility>

namespace layout {
class FruchtermanReingold {
public:
    FruchtermanReingold(const vector<vector<int>>& g);
    void operator()(vector<Point2D>& positions, const vector<double>& page_rank);
private:
    const vector<vector<int>>& graph;
    const double k_;
    const double k_squared;
    double temp;
    vector<std::pair<int, int>> edges;
    vector<Vector2D> mvmts;
};
}
