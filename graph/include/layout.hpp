// code based on https://github.com/olvb/nodesoup/blob/master/include/nodesoup.hpp
#pragma once
#include <cmath>
#include <functional>
#include <vector>

namespace layout {

using adj_list = std::vector<std::vector<int>>;

/* Algebra types */

struct Vector2D;

struct Point2D {
    double x, y;
    explicit operator Vector2D() const;
    Point2D& operator+=(const Vector2D& vector);
    Point2D& operator-=(const Vector2D& vector);
};

struct Vector2D {
    double dx, dy;
    double norm() const { return sqrt(dx * dx + dy * dy); }
    explicit operator Point2D() const;
    Vector2D& operator+=(const Vector2D& other);
    Vector2D& operator-=(const Vector2D& other);
    Vector2D& operator*=(double scalar);
    Vector2D& operator/=(double scalar);
};

// Operators between types
Point2D operator+(const Point2D& point, const Vector2D& vector);
Point2D operator-(const Point2D& point, const Vector2D& vector);
Vector2D operator-(const Point2D& lhs, const Point2D& rhs);
Vector2D operator+(const Vector2D lhs, const Vector2D& rhs);
Vector2D operator-(const Vector2D& l, const Vector2D& rhs);
Vector2D operator*(const Vector2D& vector, double scalar);
Vector2D operator*(double scalar, const Vector2D& vector);
Vector2D operator/(const Vector2D& vector, double scalar);

// Distribute vertices equally on a 1.0 radius circle
void circle(std::vector<Point2D>& positions);

// Center and scale vertices so the graph fits on a canvas of given dimensions
void center_and_scale(unsigned int width, unsigned int height, std::vector<Point2D>& positions);


/* Main function */

using iter_callback_t = std::function<void(const std::vector<Point2D>&, int)>;

// Create layout for graph @p in a @p width x @p height frame, in @p iter-count iterations
std::vector<Point2D> fruchterman_reingold(
    const adj_list& g,
    unsigned int width,
    unsigned int height,
    std::vector<double> page_rank,
    unsigned int iters_count = 300,
    double k = 15.0,
    iter_callback_t iter_cb = nullptr);

} // namespace layout
