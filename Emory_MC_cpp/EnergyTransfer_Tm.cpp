#include "utils.hpp"
#include "EnergyTransfer_Tm.hpp"
#include <cmath>
#include <map>
#include <vector>
#include <string>
#include <random>

class EnergyTransfer {
public:
    virtual double total_probability(double r) = 0;
    virtual std::pair<int, int> select_path(double r) = 0;
    virtual void add_state(int ion12, int ion22, double rate) = 0;
};

class UpConversion : public EnergyTransfer {
public:
    UpConversion(int ion2) : ion2(ion2) {}

    double total_probability(double r) override {
        double sum = 0.0;
        for (const auto& result : resulting_states) {
            sum += result[2] / std::pow(r / 1e7, 6);
        }
        return sum;
    }

    std::pair<int, int> select_path(double r) override {
        if (resulting_states.empty()) return {-1, -1};

        std::vector<double> results;
        for (const auto& result : resulting_states) {
            results.push_back(result[2] / std::pow(r, 6));
        }
        
        double sum = std::accumulate(results.begin(), results.end(), 0.0);
        for (auto& prob : results) {
            prob /= sum;
        }

        std::random_device rd;
        std::mt19937 gen(rd());
        std::discrete_distribution<> d(results.begin(), results.end());
        int new_state_index = d(gen);
        
        return {resulting_states[new_state_index][0], resulting_states[new_state_index][1]};
    }

    void add_state(int ion12, int ion22, double rate) override {
        resulting_states.push_back({ion12, ion22, rate});
    }

private:
    int ion2;
    std::vector<std::vector<double>> resulting_states;
};

class CrossRelaxation : public EnergyTransfer {
public:
    CrossRelaxation(int ion2) : ion2(ion2) {}

    double total_probability(double r) override {
        double sum = 0.0;
        for (const auto& result : resulting_states) {
            sum += result[2] / std::pow(r / 1e7, 6);
        }
        return sum;
    }

    std::pair<int, int> select_path(double r) override {
        if (resulting_states.empty()) return {-1, -1};

        std::vector<double> results;
        for (const auto& result : resulting_states) {
            results.push_back(result[2] / std::pow(r, 6));
        }

        double sum = std::accumulate(results.begin(), results.end(), 0.0);
        for (auto& prob : results) {
            prob /= sum;
        }

        std::random_device rd;
        std::mt19937 gen(rd());
        std::discrete_distribution<> d(results.begin(), results.end());
        int new_state_index = d(gen);
        
        return {resulting_states[new_state_index][0], resulting_states[new_state_index][1]};
    }

    void add_state(int ion12, int ion22, double rate) override {
        resulting_states.push_back({ion12, ion22, rate});
    }

private:
    int ion2;
    std::vector<std::vector<double>> resulting_states;
};

std::map<int, UpConversion> up_conversion() {
    std::map<int, UpConversion> ret;
    std::string ion1_energy = "S1";
    auto E_level = Tm_energy_simplified;
    auto RME_value = Tm_RME;
    auto g_value = Tm_g;
    auto Omega_value = Tm_omega;

    for (const auto& [ion2_energy, _] : Tm_energy_simplified) {
        int ion2_initial_state = std::stoi(ion2_energy.substr(1));
        UpConversion ion2_et(ion2_initial_state);
        
        std::map<std::string, double> all_transitions;
        double delta_E_ion1 = 10246;
        
        for (const auto& [level, energy] : E_level) {
            if (level != ion2_energy) {
                double energy_diff2 = energy - E_level[ion2_energy];
                if (energy_diff2 < 0 && std::abs(delta_E_ion1 + energy_diff2) < n_phonon * E_phonon) {
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
            double my_value = ET_constant * ET_n_term * s0 * (S1 * S2) * std::exp(-beta * value[0]) / (value[3][0] * value[3][1]);

            if (my_value > threshold) {
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

std::map<int, CrossRelaxation> cross_relaxation() {
    std::map<int, CrossRelaxation> ret;
    // Similar initialization and logic as up_conversion
    std::string ion1_energy = "S1";
    auto E_level = Tm_energy_simplified;
    auto RME_value = Tm_RME;
    auto g_value = Tm_g;
    auto Omega_value = Tm_omega;

    for (const auto& [ion2_energy, _] : Tm_energy_simplified) {
        int ion2_initial_state = std::stoi(ion2_energy.substr(1));
        CrossRelaxation ion2_et(ion2_initial_state);

        std::map<std::string, double> all_transitions;
        double delta_E_ion1 = 10246;

        for (const auto& [level, energy] : E_level) {
            if (level != ion2_energy) {
                double energy_diff2 = energy - E_level[ion2_energy];
                if (energy_diff2 < 0 && std::abs(delta_E_ion1 + energy_diff2) < n_phonon * E_phonon) {
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
            double my_value = ET_constant * ET_n_term * s0 * (S1 * S2) * std::exp(-beta * value[0]) / (value[3][0] * value[3][1]);

            if (my_value > threshold) {
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