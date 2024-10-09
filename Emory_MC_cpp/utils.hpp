#ifndef UTILS_HPP
#define UTILS_HPP

#include <tuple>
#include <array>

// Function declarations from utils
namespace utils {
    std::tuple<double, double, double> to_euclidean(const std::tuple<double, double, double>& vec);
    double e_distance(const std::tuple<double, double, double>& vec);
}

#endif // UTILS_HPP