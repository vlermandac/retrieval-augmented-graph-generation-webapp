// code based on https://github.com/olvb/nodesoup/blob/master/include/nodesoup.hpp
#pragma once
#include <cmath>
#include <functional>
#include <vector>

namespace layout {

using std::vector;

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

Point2D operator+(const Point2D& point, const Vector2D& vector);
Point2D operator-(const Point2D& point, const Vector2D& vector);
Vector2D operator-(const Point2D& lhs, const Point2D& rhs);
Vector2D operator+(const Vector2D lhs, const Vector2D& rhs);
Vector2D operator-(const Vector2D& l, const Vector2D& rhs);
Vector2D operator*(const Vector2D& vector, double scalar);
Vector2D operator*(double scalar, const Vector2D& vector);
Vector2D operator/(const Vector2D& vector, double scalar);

void circle(vector<Point2D>& positions);
void center_and_scale(int width, int height, vector<Point2D>& positions);

using iter_callback_t = std::function<void(const vector<Point2D>&, int)>;

vector<Point2D> fr(const vector<vector<int>>& g, const vector<double>& pr, int w, int h, iter_callback_t iter_cb = nullptr);

} // namespace layout
