// code based on https://github.com/olvb/nodesoup/blob/master/include/nodesoup.hpp
#include "../include/layout.hpp"
#include "../include/fruchterman_reingold.hpp"
#include <cmath>
#include <limits>

namespace layout {

using std::vector;

Point2D::operator Vector2D() const {
  return { x, y };
}

Point2D& Point2D::operator+=(const Vector2D& vector) {
  x += vector.dx;
  y += vector.dy;
  return *this;
}

Point2D& Point2D::operator-=(const Vector2D& vector) {
  x -= vector.dx;
  y -= vector.dy;
  return *this;
}

Vector2D::operator Point2D() const {
  return { dx, dy };
}

Vector2D& Vector2D::operator+=(const Vector2D& other) {
  dx += other.dx;
  dy += other.dy;
  return *this;
}

Vector2D& Vector2D::operator-=(const Vector2D& other) {
  dx -= other.dx;
  dy -= other.dy;
  return *this;
}

Vector2D& Vector2D::operator*=(double scalar) {
  dx *= scalar;
  dy *= scalar;
  return *this;
}

Vector2D& Vector2D::operator/=(double scalar) {
  dx /= scalar;
  dy /= scalar;
  return *this;
}

Point2D operator+(const Point2D& point, const Vector2D& vector) {
  return { point.x + vector.dx, point.y + vector.dy };
}

Point2D operator-(const Point2D& point, const Vector2D& vector) {
  return { point.x - vector.dx, point.y - vector.dy };
}

Vector2D operator-(const Point2D& lhs, const Point2D& rhs) {
  return { lhs.x - rhs.x, lhs.y - rhs.y };
}

Vector2D operator+(const Vector2D& lhs, const Vector2D& rhs) {
  return { lhs.dx + rhs.dx, lhs.dy + rhs.dy };
}

Vector2D operator-(const Vector2D& lhs, const Vector2D& rhs) {
  return { lhs.dx - rhs.dx, lhs.dy - rhs.dy };
}

Vector2D operator*(const Vector2D& vector, double scalar) {
  return { vector.dx * scalar, vector.dy * scalar };
}

Vector2D operator*(double scalar, const Vector2D& vector) {
  return vector * scalar;
}

Vector2D operator/(const Vector2D& vector, double scalar) {
  return { vector.dx / scalar, vector.dy / scalar };
}

void circle(vector<Point2D>& positions) {
  double angle = 2.0 * M_PI / positions.size();
  for (int i = 0; i < positions.size(); i++) {
    positions[i].x = cos(i * angle);
    positions[i].y = sin(i * angle);
  }
}

void center_and_scale(unsigned int width, unsigned int height, vector<Point2D>& positions) {
  double x_min = std::numeric_limits<double>::max();
  double x_max = std::numeric_limits<double>::lowest();
  double y_min = std::numeric_limits<double>::max();
  double y_max = std::numeric_limits<double>::lowest();

  for (int i = 0; i < positions.size(); i++) {
    x_min = std::min(x_min, positions[i].x);
    x_max = std::max(x_max, positions[i].x);
    y_min = std::min(y_min, positions[i].y);
    y_max = std::max(y_max, positions[i].y);
  }

  // applying scale factor (0.9: keep some margin) and offset
  double x_scale = width / (x_max - x_min), y_scale = height / (y_max - y_min);
  double scale = 0.9 * std::min(x_scale, y_scale);
  Vector2D center = { x_max + x_min, y_max + y_min };
  Vector2D offset = center / 2.0 * scale;
  for (int i = 0; i < positions.size(); i++)
    positions[i] = (Point2D)((Vector2D) positions[i] * scale - offset);
}

vector<Point2D> fruchterman_reingold(
  const adj_list& g,
  unsigned int width,
  unsigned int height,
  std::vector<double> page_rank,
  unsigned int iters_count,
  double k,
  iter_callback_t iter_cb) {

  vector<Point2D> positions(g.size()); circle(positions);
  FruchtermanReingold fr(g, k);
  for (unsigned int i = 0; i < iters_count; i++) {
    fr(positions, page_rank);
    if (iter_cb) {
      vector<Point2D> scaled_positions = positions;
      center_and_scale(width, height, scaled_positions);
      iter_cb(scaled_positions, i);
    }
  }
  center_and_scale(width, height, positions);
  return positions;
}

} // namespace layout
