#include "Lattice_Tm.hpp"
#include <algorithm>
#include <iostream>
#include "Point_Tm.hpp"
#include "utils.hpp"

Lattice::Lattice(double yb_conc, double tm_conc, double d, double r, int seed) 
    : yb_conc(yb_conc), tm_conc(tm_conc), d(d), r(r) {
    if (seed != 0) {
        std::srand(seed);
    }
    initialize_points();
    get_neighbors(r);
}

void Lattice::initialize_points() {
    int l_r = static_cast<int>(d / (2 * 0.596));
    int l_z = static_cast<int>(d / (2 * 0.353));
    
    std::vector<Point> na_points;
    for (int i = -l_r; i <= l_r; ++i) {
        for (int j = -l_r; j <= l_r; ++j) {
            for (int k = -l_z; k <= l_z; ++k) {
                na_points.emplace_back(Point({i, j, k}, "Na"));
            }
        }
    }

    std::vector<Point> y_coords;
    for (const auto& na : na_points) {
        y_coords.emplace_back(Point(std::make_tuple(
            std::get<0>(na.p) + 1.0 / 3.0,
            std::get<1>(na.p) + 1.0 / 3.0,
            std::get<2>(na.p) + 1.0 / 2.0
        ), "Y"));
        y_coords.emplace_back(Point(std::make_tuple(
            std::get<0>(na.p) - 1.0 / 3.0,
            std::get<1>(na.p) - 1.0 / 3.0,
            std::get<2>(na.p) + 1.0 / 2.0
        ), "Y"));
    }

    na_points = in_diameter(d, na_points);
    y_coords = in_diameter(d, y_coords);
    
    int n_points = static_cast<int>(y_coords.size() * 3 / 4);
    yb_num = static_cast<int>(yb_conc * n_points);
    tm_num = static_cast<int>(tm_conc * n_points);

    std::vector<std::string> types(na_points.size(), "Na");
    types.resize(na_points.size() + yb_num + tm_num + (n_points - yb_num - tm_num), "Y");
    std::fill(types.begin() + na_points.size(), types.begin() + na_points.size() + yb_num, "Yb");
    std::fill(types.begin() + na_points.size() + yb_num, types.end(), "Tm");

    std::shuffle(types.begin(), types.end());

    for (size_t i = 0; i < y_coords.size(); ++i) {
        y_coords[i].type = types[i];
        if (types[i] == "Yb") {
            y_coords[i].state = std::rand() % 100 < 85 ? 0 : 1;
        } else {
            y_coords[i].state = 0;
        }
    }

    for (const auto& p : y_coords) {
        if (p.type != "Na") {
            y_points.push_back(p);
        } else {
            na_points.push_back(p);
        }
    }
    
    this->na_points = na_points;
    this->y_points = y_points;
    this->points = std::vector<Point>(y_points.begin(), y_points.end());
    this->n_points = static_cast<int>(points.size());
}

void Lattice::get_neighbors(double r) {
    for (size_t i = 0; i < n_points; ++i) {
        std::vector<std::pair<Point, double>> i_nei;
        for (size_t j = 0; j < n_points; ++j) {
            if (i == j) {
                continue;
            }
            double dist = points[i].to(points[j]);
            if (dist <= r) {
                i_nei.emplace_back(points[j], dist);
            }
        }
        neighbors[points[i]] = i_nei;
    }
}

std::vector<Point> Lattice::in_diameter(double d, const std::vector<Point>& points) {
    Point origin({0, 0, 0});
    std::vector<Point> ret;
    for (const auto& point : points) {
        if (point.to(origin) < d / 2) {
            ret.push_back(point);
        }
    }
    return ret;
}

std::pair<std::vector<int>, std::vector<int>> Lattice::collect_stats() {
    std::vector<int> yb_stats(2, 0);
    std::vector<int> tm_stats(8, 0);

    for (const auto& p : points) {
        if (p.type == "Yb") {
            ++yb_stats[p.state];
        } else if (p.type == "Tm") {
            ++tm_stats[p.state];
        }
    }
    
    return {yb_stats, tm_stats};
}

Lattice Lattice::deep_copy() {
    Lattice cp(yb_conc, tm_conc, d, r);
    cp.na_points = na_points;
    cp.y_points.reserve(points.size());
    
    for (const auto& p : points) {
        cp.y_points.push_back(p.deep_copy());
    }

    cp.points = std::vector<Point>(cp.y_points.begin(), cp.y_points.end());
    cp.n_points = n_points;
    cp.get_neighbors(cp.r);

    cp.excited = {};
    cp.ground_yb = {};
    
    for (const auto& p : cp.points) {
        if (p.state != 0) {
            cp.excited.push_back(p);
        }
        if (p.type == "Yb" && p.state == 0) {
            cp.ground_yb.push_back(p);
        }
    }

    return cp;
}