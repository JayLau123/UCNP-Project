#ifndef POINT_TM_HPP
#define POINT_TM_HPP

#include <tuple>
#include <string>
#include <unordered_map>
#include "utils.hpp"
#include "EnergyTransfer_Tm.hpp"

class Point {
public:
    Point(std::tuple<double, double, double> coor, std::string mol = "", int state = 0);

    size_t hash() const;
    void change_state(int new_state);
    std::tuple<double, double, double> to_euclidean() const;
    double to(const Point& other) const;
    Point deep_copy() const;
    std::pair<double, std::vector<int>> react(const Point& other, 
                                               const std::map<int, CrossRelaxation>& cross_relaxation,
                                               const std::map<int, UpConversion>& up_conversion,
                                               double yb_yb, 
                                               double distance) const;
    std::vector<double> get_decay_rates(const std::map<std::string, double>& tag) const;
    std::string to_string() const;

    bool operator==(const Point& other) const;

private:
    std::tuple<double, double, double> p; // Coordinates
    std::string type; // Molecular type
    int state; // State
};

namespace std {
    template <>
    struct hash<Point> {
        size_t operator()(const Point& point) const {
            return point.hash();
        }
    };
}

#endif // POINT_TM_HPP