#include "utils.hpp"
#include "EnergyTransfer_Tm.hpp"
#include "Tm_inf.hpp"
#include "Tm_adjustable_parameter.hpp"
#include <cmath>
#include <unordered_map>
#include <vector>
#include <string>
#include <random>

static double ET_n_term;
static std::unordered_map<std::string, double> Tm_energy_simplified;
static std::unordered_map<std::string, int> Tm_g;

void initialize_data(int n, const std::unordered_map<std::string, double>& Tm_energy) {
    ET_n_term = std::pow(((n * n + 2) / (3.0 * n)), 4);

    for (const auto& key_value : Tm_RME) {
        // TODO: 这个iteration可能出问题，因为我modify了Tm_RME
        std::string key = key_value.first;
        auto parts = key.find('E');
        std::string new_key = "E" + key.substr(parts + 2, 1) + "E" + key.substr(parts + 1, 1);
        if (Tm_RME.find(new_key) == Tm_RME.end()) {
            Tm_RME[new_key] = key_value.second;
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

UpConversion::UpConversion(int ion2) : ion2(ion2) {}

double UpConversion::total_probability(double r) {
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



CrossRelaxation::CrossRelaxation(int ion1, int ion2) : ion1(ion1), ion2(ion2) {}

double CrossRelaxation::total_probability(double r) {
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
    auto E_level = Tm_energy_simplified;
    auto RME_value = Tm_RME;
    auto g_value = Tm_g;
    auto Omega_value = Tm_omega;

    for (const auto& [ion2_energy, _] : Tm_energy_simplified) {
        int ion2_initial_state = std::stoi(ion2_energy.substr(1));
        UpConversion ion2_et(ion2_initial_state);
        
        std::unordered_map<std::string, double> all_transitions;
        double delta_E_ion1 = 10246;
        
        for (const auto& [level, energy] : E_level) {
            if (level != ion2_energy) {
                double energy_diff2 = energy - E_level[ion2_energy];
                if (energy_diff2 < 0 && std::abs(delta_E_ion1 + energy_diff2) < TmAdjustableParameter::n_phonon * TmAdjustableParameter::E_phonon) {
                    double Delta_E = std::abs(delta_E_ion1 + energy_diff2);
                    all_transitions["S1S0-" + level] = Delta_E;
                }
            }
        }

        for (const auto& [key, value] : all_transitions) {
            auto parts = key.substr(0, key.find('-'));
            auto second_part = key.substr(key.find('-') + 1);
            auto second_values = RME_value[second_part];
            all_transitions[key] = {value, 2e-20, second_values};
            auto new_key = "E" + second_part.substr(second_part.find('E') + 1);
            all_transitions[key].push_back({Yb_g[ion1_energy], g_value[new_key]});
        }

        for (const auto& [key, value] : all_transitions) {
            double S1 = value[1];
            double S2 = Omega_value["2"] * value[2][0] + Omega_value["4"] * value[2][1] + Omega_value["6"] * value[2][2];
            double my_value = TmAdjustableParameter::ET_constant * ET_n_term * TmAdjustableParameter::s0 * (S1 * S2) * std::exp(-TmAdjustableParameter::beta * value[0]) / (value[3][0] * value[3][1]);

            if (my_value > Tm_adjustable_parameter::threshold) {
                auto donor_transition = key.substr(0, key.find('-'));
                auto acceptor_transition = key.substr(key.find('-') + 1);
                int donor_final_state = std::stoi(donor_transition.substr(donor_transition.find('S') + 1));
                int acceptor_final_state = std::stoi(acceptor_transition.substr(acceptor_transition.find('E') + 1));

                ion2_et.add_state(donor_final_state, acceptor_final_state, my_value);
            }
        }
        
        ret[ion2_initial_state] = ion2_et;
    }

    return ret;
}

std::unordered_map<int, CrossRelaxation> cross_relaxation() {
    std::unordered_map<int, CrossRelaxation> ret;
    std::string ion1_energy = "S1";
    auto E_level = Tm_energy_simplified;
    auto RME_value = Tm_RME;
    auto g_value = Tm_g;
    auto Omega_value = Tm_omega;

    for (const auto& [ion2_energy, _] : Tm_energy_simplified) {
        int ion2_initial_state = std::stoi(ion2_energy.substr(1));
        CrossRelaxation ion2_et(ion2_initial_state);

        std::unordered_map<std::string, double> all_transitions;
        double delta_E_ion1 = 10246;

        for (const auto& [level, energy] : E_level) {
            if (level != ion2_energy) {
                double energy_diff2 = energy - E_level[ion2_energy];
                if (energy_diff2 < 0 && std::abs(delta_E_ion1 + energy_diff2) < TmAdjustableParameter::n_phonon * TmAdjustableParameter::E_phonon) {
                    double Delta_E = std::abs(delta_E_ion1 + energy_diff2);
                    all_transitions["S1S0-" + level] = Delta_E;
                }
            }
        }

        for (const auto& [key, value] : all_transitions) {
            auto parts = key.substr(0, key.find('-'));
            auto second_part = key.substr(key.find('-') + 1);
            auto second_values = RME_value[second_part];
            all_transitions[key] = {value, 2e-20, second_values};
            auto new_key = "E" + second_part.substr(second_part.find('E') + 1);
            all_transitions[key].push_back({Yb_g[ion1_energy], g_value[new_key]});
        }

        for (const auto& [key, value] : all_transitions) {
            double S1 = value[1];
            double S2 = Omega_value["2"] * value[2][0] + Omega_value["4"] * value[2][1] + Omega_value["6"] * value[2][2];
            double my_value = TmAdjustableParameter::ET_constant * ET_n_term * TmAdjustableParameter::s0 * (S1 * S2) * std::exp(-TmAdjustableParameter::beta * value[0]) / (value[3][0] * value[3][1]);

            if (my_value > TmAdjustableParameter::threshold) {
                auto donor_transition = key.substr(0, key.find('-'));
                auto acceptor_transition = key.substr(key.find('-') + 1);
                int donor_final_state = std::stoi(donor_transition.substr(donor_transition.find('S') + 1));
                int acceptor_final_state = std::stoi(acceptor_transition.substr(acceptor_transition.find('E') + 1));

                ion2_et.add_state(donor_final_state, acceptor_final_state, my_value);
            }
        }

        ret[ion2_initial_state] = ion2_et;
    }

    return ret;
}