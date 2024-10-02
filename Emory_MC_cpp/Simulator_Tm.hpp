#ifndef SIMULATOR_HPP
#define SIMULATOR_HPP

#include <vector>
#include <map>
#include <string>
#include <random>
#include <iostream>
#include "Lattice.hpp"
#include "Point.hpp"

class Simulator {
public:
    Simulator(Lattice lattice, std::map<std::string, double> tag, bool excite_tm = false);
    void step(double steps = 0.003, bool emission = false);

private:
    Lattice lattice;
    double t;
    std::map<std::string, double> tag;
    std::map<std::string, double> cross_relaxation;
    std::map<std::string, double> up_conversion;
    bool excite_tm;

    // Emission counters
    int NIR30s, NIR62s, NIR74s, NIR75s, NIR86s, NIR96s;
    int blue60s, blue71s, blue72s, blue83s, blue84s, blue85s, blue93s, blue94s, blue95s, blue10_3s, blue10_4s, blue10_5s, blue11_4s, blue11_5s;
    int yb_upconversions, yb_ybs, yb_excites, tm_decays;
    std::map<std::string, int> tm_upconversions;
    std::map<std::string, int> tm_crossrelaxations;
    int tm_excite_7_11s;

    void initializeEmissionCounters();
    void updateTransitionTable(std::map<std::string, double>& transition_table, std::map<std::string, std::pair<Point*, int>>& transition_to_point);
    void handleLaserExcitation(const std::string& selected_transition, std::map<std::string, double>& transition_table, std::map<std::string, std::pair<Point*, int>>& transition_to_point);
    void handleDecay(const std::string& selected_transition, std::map<std::string, double>& transition_table, std::map<std::string, std::pair<Point*, int>>& transition_to_point);
    void handleEnergyTransfer(const std::string& selected_transition, std::map<std::string, double>& transition_table, std::map<std::string, std::pair<Point*, int>>& transition_to_point);
};