#include <cmath>
#include <tuple>
#include <array>

namespace utils{
    // Convert vector to Euclidean space
    std::tuple<double, double, double> to_euclidean(const std::array<double, 3>& vec) {
        double a = vec[0];
        double b = vec[1];
        double c = vec[2];
        
        double x = 0.596 * a + 0.5 * 0.596 * b;
        double y = std::sqrt(3.0) / 2 * 0.596 * b;
        double z = 0.353 * c;
        
        return std::make_tuple(x, y, z);
    }

    // Calculate Euclidean distance
    double e_distance(const std::tuple<double, double, double>& vec) {
        double x = std::get<0>(vec);
        double y = std::get<1>(vec);
        double z = std::get<2>(vec);
        
        return std::sqrt(x * x + y * y + z * z);
    }
}