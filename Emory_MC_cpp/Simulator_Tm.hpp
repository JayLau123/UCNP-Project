#ifndef SIMULATOR_HPP
#define SIMULATOR_HPP

#include <unordered_map>
#include <vector>
#include <string>
#include <random>
#include <cmath>
#include "Point_Tm.hpp"
#include "Lattice_Tm.hpp"
#include "EnergyTransfer_Tm.hpp"

class Simulator {
public:
    Simulator(Lattice &lattice, const std::unordered_map<std::string, double> &tag);
    void step(double steps = 0.003);
    void simulate(double t1, double t2);

private:
    void initialize_transitions();
    void add_decay_transitions(Point &p);
    void add_et_transitions(Point &p);
    void add_laser_transitions(Point &p);
    std::string select_transition();
    void process_transition(const std::string &selected_transition);
    void process_laser_excitation(const std::string &selected_transition);
    void process_decay(const std::string &selected_transition);
    void process_et(const std::string &selected_transition);
    void update_after_transition(Point &p);
    void remove_old_transitions(Point &p);
    void handle_energy_transfer(Point &p_donor, Point &p_acceptor);

    Lattice lattice;
    double t;
    std::unordered_map<std::string, double> tag;
    std::unordered_map<int, std::unordered_map<int, CrossRelaxation>> cross_relaxation;
    std::unordered_map<int, UpConversion> up_conversion;
    std::unordered_map<std::string, double> transition_table;
    std::unordered_map<std::string, std::pair<Point, Point>> transition_to_point;
    std::default_random_engine generator;
};

#endif // SIMULATOR_HPP