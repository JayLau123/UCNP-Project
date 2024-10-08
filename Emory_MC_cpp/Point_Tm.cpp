#include "Point_Tm.hpp"
#include "utils.hpp"
#include <cmath>
#include <sstream>
#include <iomanip>

Point::Point() : p{0.0, 0.0, 0.0}, type("Default"), state(0) {}

Point::Point(std::tuple<double, double, double> coor, std::string mol, int state)
    : p(coor), type(mol), state(state) {}

size_t Point::hash() const {
    return std::hash<double>()(std::get<0>(p)) ^ std::hash<double>()(std::get<1>(p)) ^ std::hash<double>()(std::get<2>(p));
}

void Point::change_state(int new_state) {
    state = new_state;
}

std::tuple<double, double, double> Point::to_euclidean() const {
    double a = std::get<0>(p);
    double b = std::get<1>(p);
    double c = std::get<2>(p);
    return std::make_tuple(0.596 * a + 0.5 * 0.596 * b, 
                           std::sqrt(3) / 2 * 0.596 * b, 
                           0.353 * c);
}

double Point::to(const Point& other) const {
    auto p1 = p;
    auto p2 = other.p;
    auto vec = std::make_tuple(std::get<0>(p1) - std::get<0>(p2), 
                                std::get<1>(p1) - std::get<1>(p2), 
                                std::get<2>(p1) - std::get<2>(p2));
    auto evec = utils::to_euclidean(vec);
    return utils::e_distance(evec);
}

Point Point::deep_copy() const {
    return Point(p, type, state);
}

std::pair<double, std::vector<int>> Point::react(const Point& other, 
                                                 const std::unordered_map<int, CrossRelaxation>& cross_relaxation,
                                                 const std::unordered_map<int, std::unordered_map<int, UpConversion>>& up_conversion,
                                                 double yb_yb, 
                                                 double distance) const {
    if (type == "Yb" && state == 1) {
        if (other.type == "Yb") {
            if (other.state == 0) {
                return {yb_yb / std::pow(distance / 1e7, 6), {}};
            }
            return {0.0, {}};
        } else {
            return {up_conversion.at(other.state).total_probability(distance), {}};
        }
    } else if (type == "Tm" && other.type == "Tm") {
        return {cross_relaxation.at(state).at(other.state).total_probability(distance), {}};
    }
    return {0.0, {}};
}

std::vector<double> Point::get_decay_rates(const std::unordered_map<std::string, double>& tag) const {
    std::vector<double> ret;
    for (int i = 0; i < state; ++i) {
        ret.push_back(tag.at("E" + std::to_string(state) + "E" + std::to_string(i)));
    }
    return ret;
}

std::string Point::to_string() const {
    std::ostringstream oss;
    oss << std::fixed << std::setprecision(2)
        << "(" << std::get<0>(p) << ", " 
        << std::get<1>(p) << ", " 
        << std::get<2>(p) << ") " 
        << type << " " 
        << state;
    return oss.str();
}

bool Point::operator==(const Point& other) const {
    return p == other.p;
}