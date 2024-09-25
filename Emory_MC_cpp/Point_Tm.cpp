#include <tuple>
#include <cmath>
#include <vector>
#include <unordered_map>
#include <string>
#include <memory>
#include <functional>

// Function declarations from the other modules
std::tuple<double, double, double> to_euclidean(const std::array<double, 3>& vec);
double e_distance(const std::tuple<double, double, double>& vec);

// Placeholder for EnergyTransfer_Tm functions and variables
// #include "EnergyTransfer_Tm.hpp"

class Point {
public:
    // Constructors
    Point(const std::array<double, 3>& coor, const std::string& mol = "", int state = 0)
        : p(coor), type(mol), state(state) {}

    // Custom hash function
    std::size_t hash() const {
        return std::hash<std::array<double, 3>>{}(p);
    }

    // Change the state of the Point
    void change_state(int new_state) {
        state = new_state;
    }

    // Convert coordinates to Euclidean space
    std::tuple<double, double, double> to_euclidean() const {
        double a = p[0];
        double b = p[1];
        double c = p[2];
        return std::make_tuple(0.596 * a + 0.5 * 0.596 * b, std::sqrt(3.0) / 2 * 0.596 * b, 0.353 * c);
    }

    // Calculate Euclidean distance to another Point
    double to(const Point& other) const {
        auto vec = std::array<double, 3>{p[0] - other.p[0], p[1] - other.p[1], p[2] - other.p[2]};
        auto evec = to_euclidean(vec);
        return e_distance(evec);
    }

    // Create a deep copy of the current Point
    std::shared_ptr<Point> deep_copy() const {
        return std::make_shared<Point>(p, type, state);
    }

    // Reaction logic based on the Point's type and state
    std::optional<double> react(const Point& other, 
                                const std::unordered_map<int, std::unordered_map<int, double>>& cross_relaxation,
                                const std::unordered_map<int, double>& up_conversion,
                                double yb_yb,
                                double distance) const {
        if (type == "Yb" && state == 1) {
            if (other.type == "Yb") {
                if (other.state == 0) {
                    return yb_yb / std::pow(distance / 1e7, 6);
                }
                return std::nullopt;
            } else {
                return up_conversion.at(other.state);
            }
        } else if (type == "Tm" && other.type == "Tm") {
            return cross_relaxation.at(state).at(other.state);
        }
        return std::nullopt;
    }

    // Retrieve decay rates
    std::vector<double> get_decay_rates(const std::unordered_map<std::string, double>& tag) const {
        std::vector<double> ret;
        for (int i = 0; i < state; ++i) {
            ret.push_back(tag.at("E" + std::to_string(state) + "E" + std::to_string(i)));
        }
        return ret;
    }

    // String representation of the Point
    std::string to_string() const {
        return "(" + std::to_string(p[0]) + ", " + std::to_string(p[1]) + ", " + std::to_string(p[2]) + ") " + type + " " + std::to_string(state);
    }

    // Equality operator
    bool operator==(const Point& other) const {
        return p[0] == other.p[0] && p[1] == other.p[1] && p[2] == other.p[2];
    }

private:
    std::array<double, 3> p;
    std::string type;
    int state;
};

// Hash function specialization for Point to use in unordered_map
namespace std {
    template <>
    struct hash<Point> {
        std::size_t operator()(const Point& point) const {
            return point.hash();
        }
    };
}