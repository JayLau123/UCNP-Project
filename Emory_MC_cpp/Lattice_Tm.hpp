#ifndef LATTICE_TM_HPP
#define LATTICE_TM_HPP

#include <vector>
#include <random>
#include <unordered_map>
#include "Point_Tm.hpp"
#include "utils.hpp"

class Lattice {
public:
    std::vector<Point> points;
    std::unordered_map<Point, std::vector<std::pair<Point, double>>> neighbors;
    
    Lattice(double yb_conc, double tm_conc, double d, double r, int seed = 0);
    void get_neighbors(double r);
    std::vector<Point> in_diameter(double d, const std::vector<Point>& points);
    std::pair<std::vector<int>, std::vector<int>> collect_stats();
    Lattice deep_copy();

private:
    double yb_conc;
    double tm_conc;
    int yb_num;
    int tm_num;
    double d;
    double r;
    std::vector<Point> na_points;
    std::vector<Point> y_points;
    int n_points;
    std::vector<Point> excited;
    std::vector<Point> ground_yb;

    void initialize_points();
};

#endif // LATTICE_TM_HPP