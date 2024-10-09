#include "utils.hpp"
#include "EnergyTransfer_Tm.hpp"
#include "Tm_inf.hpp"
#include "Tm_adjustable_parameter.hpp"
#include <cmath>
#include <unordered_map>
#include <vector>
#include <string>
#include <iostream>
#include <random>

static double ET_n_term;
static std::unordered_map<std::string, double> Tm_energy_simplified;
static std::unordered_map<std::string, int> Tm_g;
std::unordered_map<std::string, std::vector<double>> Tm_RME_tmp;

void initialize_data() {
    ET_n_term = std::pow(((TmAdjustableParameter::n * TmAdjustableParameter::n + 2) / (3.0 * TmAdjustableParameter::n)), 4);
    
    Tm_RME_tmp.clear();
    Tm_g.clear();
    Tm_energy_simplified.clear();
    Tm_RME_tmp = Tm_RME; 

    for (const auto& key_value : Tm_RME) {
        std::string key = key_value.first;
        auto firstE = key.find('E');
        auto secondE = key.find('E', firstE+1);
        std::string new_key = key.substr(secondE) + key.substr(firstE, secondE-firstE);
        if (Tm_RME.find(new_key) == Tm_RME.end()) {
            Tm_RME_tmp[new_key] = key_value.second;
        }
    }

    for (const auto& kv : Tm_energy) {
        std::string key = kv.first;
        auto pos = key.find('(');
        std::string simplified_key = key.substr(0, pos);
        double J = std::stod(key.substr(pos + 3, 1)) / 2;
        Tm_g[simplified_key] = 2 * J + 1;
        Tm_energy_simplified[simplified_key] = kv.second;
    }
}

UpConversion::UpConversion() : ion2(0) {} 

UpConversion::UpConversion(int ion2) : ion2(ion2) {}

UpConversion::UpConversion(const UpConversion& other) : ion2(other.ion2) {}

double UpConversion::total_probability(double r) const {
    double sum = 0.0;
    for (const auto& result : resulting_states) {
        sum += std::get<2>(result) / std::pow(r / 1e7, 6);
    }
    return sum;
}

std::pair<int, int> UpConversion::select_path(double r) {
    if (resulting_states.empty()) {
        return {-1, -1};
    }

    std::vector<double> results;
    for (const auto& result : resulting_states) {
        results.push_back(std::get<2>(result) / std::pow(r, 6));
    }
    
    double sum = std::accumulate(results.begin(), results.end(), 0.0);
    for (auto& prob : results) {
        prob /= sum;
    }

    std::random_device rd;
    std::mt19937 gen(rd());
    std::discrete_distribution<> d(results.begin(), results.end());
    int new_state_index = d(gen);

    return {std::get<0>(resulting_states[new_state_index]), std::get<1>(resulting_states[new_state_index])};
}

void UpConversion::add_state(int ion12, int ion22, double rate) {
    resulting_states.push_back({ion12, ion22, rate});
}


CrossRelaxation::CrossRelaxation() : ion1(0), ion2(0) {} 

CrossRelaxation::CrossRelaxation(int ion1, int ion2) : ion1(ion1), ion2(ion2) {}

CrossRelaxation::CrossRelaxation(const CrossRelaxation& other) : ion1(other.ion1), ion2(other.ion2) {}

double CrossRelaxation::total_probability(double r) const {
    double sum = 0.0;
    for (const auto& result : resulting_states) {
        sum += std::get<2>(result) / std::pow(r / 1e7, 6);
    }
    return sum;
}

std::pair<int, int> CrossRelaxation::select_path(double r) {
    if (resulting_states.empty()) return {-1, -1};

    std::vector<double> results;
    for (const auto& result : resulting_states) {
        results.push_back(std::get<2>(result) / std::pow(r, 6));
    }

    double sum = std::accumulate(results.begin(), results.end(), 0.0);
    for (auto& prob : results) {
        prob /= sum;
    }

    std::random_device rd;
    std::mt19937 gen(rd());
    std::discrete_distribution<> d(results.begin(), results.end());
    int new_state_index = d(gen);
    
    return {std::get<0>(resulting_states[new_state_index]), std::get<1>(resulting_states[new_state_index])};
}

void CrossRelaxation::add_state(int ion12, int ion22, double rate) {
    resulting_states.push_back({ion12, ion22, rate});
}


std::unordered_map<int, UpConversion> up_conversion() {
    std::unordered_map<int, UpConversion> ret;
    std::string ion1_energy = "S1";
    initialize_data();
    auto& E_level = Tm_energy_simplified;
    auto& RME_value = Tm_RME_tmp;
    auto& g_value = Tm_g;
    auto& Omega_value = Tm_omega;

    for (const auto& [ion2_energy, _] : Tm_energy_simplified) {
        auto pos = ion2_energy.find('E');
        int ion2_initial_state = std::stoi(ion2_energy.substr(pos + 1));
        UpConversion ion2_et(ion2_initial_state);
                
        for (const auto& [level, energy] : E_level) {
            if (level != ion2_energy) {
                double energy_diff2 = E_level[ion2_energy] - energy;
                if (energy_diff2 < 0 && std::abs(10246 + energy_diff2) < TmAdjustableParameter::n_phonon * TmAdjustableParameter::E_phonon) {
                    double Delta_E = std::abs(10246 + energy_diff2);
                    auto second_part = ion2_energy+level;
                    auto second_values = RME_value.at(ion2_energy+level);
                    auto new_key = level;

                    double S1 = 2e-20;
                    double S2 = Omega_value.at("2") * second_values[0] + Omega_value.at("4") * second_values[1] + Omega_value.at("6") * second_values[2];
                    double my_value = TmAdjustableParameter::ET_constant * ET_n_term * TmAdjustableParameter::s0 * (S1 * S2) * std::exp(-TmAdjustableParameter::beta * Delta_E) / (Yb_g.at(ion1_energy) * g_value.at(new_key));
                    if (my_value > TmAdjustableParameter::threshold) {
                        int donor_final_state = 0;
                        int acceptor_final_state = std::stoi(level.substr(level.find('E') + 1));

                        ion2_et.add_state(donor_final_state, acceptor_final_state, my_value);
                    }
                }
            }
        }
        
        ret[ion2_initial_state] = ion2_et;
    }

    return ret;
}


std::unordered_map<int, std::unordered_map<int, CrossRelaxation>> cross_relaxation() {
    std::unordered_map<int, std::unordered_map<int, CrossRelaxation>> ret;
    initialize_data();
    auto& E_level = Tm_energy_simplified;
    auto& RME_value = Tm_RME_tmp;
    auto& g_value = Tm_g;
    auto& Omega_value = Tm_omega;
    
    for (const auto& ion1_energy : Tm_energy_simplified) {
        std::unordered_map<int, CrossRelaxation> ion1_ets;
        auto pos = ion1_energy.first.find('E');
        int donor_initial_state = std::stoi(ion1_energy.first.substr(pos + 1));
        
        for (const auto& ion2_energy : Tm_energy_simplified) {

            pos = ion2_energy.first.find('E');
            int acceptor_initial_state = std::stoi(ion2_energy.first.substr(pos + 1));

            CrossRelaxation ion1_ion2_et(donor_initial_state, acceptor_initial_state);

            std::unordered_map<std::string, double> all_transitions;
            for (const auto& level : Tm_energy_simplified) {
                if (level.first != ion1_energy.first) {
                    double energy_diff1 = Tm_energy_simplified.at(ion1_energy.first) - level.second;
                    std::string transition1 = ion1_energy.first + level.first;
                    
                    for (const auto& level2 : Tm_energy_simplified) {
                        if (level2.first != ion2_energy.first) {
                            double energy_diff2 = Tm_energy_simplified.at(ion2_energy.first) - level2.second;
                            std::string transition2 = ion2_energy.first + level2.first;

                            if ((energy_diff1 > 0 && energy_diff2 < 0 && std::abs(energy_diff1 + energy_diff2) < TmAdjustableParameter::n_phonon * TmAdjustableParameter::E_phonon) ||
                                (energy_diff1 < 0 && energy_diff2 > 0 && std::abs(energy_diff2 + energy_diff1) < TmAdjustableParameter::n_phonon * TmAdjustableParameter::E_phonon)) {
                                all_transitions[transition1 + "-" + transition2] = std::abs(energy_diff1 + energy_diff2);

                                const auto& first_values = RME_value.at(transition1);
                                const auto& second_values = RME_value.at(transition2);

                                if (!first_values.empty() && !second_values.empty()) {
                                    double S1 = Tm_omega.at("2") * first_values[0] + Tm_omega.at("4") * first_values[1] + Tm_omega.at("6") * first_values[2];
                                    double S2 = Tm_omega.at("2") * second_values[0] + Tm_omega.at("4") * second_values[1] + Tm_omega.at("6") * second_values[2];
                                    double my_value = TmAdjustableParameter::ET_constant * ET_n_term * TmAdjustableParameter::s0 * (S1 * S2) 
                                                      * std::exp(-TmAdjustableParameter::beta * abs(energy_diff1 + energy_diff2)) / (g_value.at(level.first) * g_value.at(level2.first));

                                    if (my_value > TmAdjustableParameter::threshold){
                                        int donor_final_state = std::stoi(transition1.substr(transition1.find('E') + 1));
                                        int acceptor_final_state = std::stoi(transition2.substr(transition2.find('E') + 1));
                                        ion1_ion2_et.add_state(donor_final_state, acceptor_final_state, my_value);
                                    }
                                }
                            }
                        }
                    }
                }
            }

            ion1_ets[acceptor_initial_state] = ion1_ion2_et;
        }

        ret[donor_initial_state] = ion1_ets;
    }

    return ret;
}