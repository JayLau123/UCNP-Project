
#include <iostream>
#include <unordered_map>
#include <vector>
#include <iostream>

#include "Tm_inf.hpp"
#include "Tm_RateCalculation.hpp"
#include "Tm_adjustable_parameter.hpp"
#include "utils.hpp"
#include "Point_Tm.hpp"
#include "Lattice_Tm.hpp"
#include "EnergyTransfer_Tm.hpp"
#include "Simulator_Tm.hpp"

int main() {
    // Manually input for Yb
    std::unordered_map<std::string, double> tag_Yb = {
        {"c0", 7e-39},  // Yb-Yb resonant energy transfer
        {"Ws", 834}     // Yb ED+MD
    };
    

    // Calculating tags for Tm
    auto tag_Tm_ED = ED_cal(Tm_energy, Tm_omega, Tm_RME, TmAdjustableParameter::n);
    auto tag_Tm_MD = MD_cal(Tm_energy);
    auto tag_Tm_mpr = MPR_cal(Tm_energy, TmAdjustableParameter::W0, TmAdjustableParameter::alpha, TmAdjustableParameter::E_phonon);
    auto tag_default = tag_Tm_ED;

    // Add Yb parameters to tag_default
    for (const auto& key_value : tag_Yb) {
        tag_default[key_value.first] = key_value.second;
    }

    // Combine MD+ED
    for (const auto& key_value : tag_Tm_MD) {
        tag_default[key_value.first] += key_value.second;
    }

    // Combine MD+ED+MPR
    for (const auto& key_value : tag_Tm_mpr) {
        tag_default[key_value.first] += key_value.second;
    }

    std::unordered_map<int, std::unordered_map<int, CrossRelaxation>> cross_relaxation_map = cross_relaxation();
    for (const auto& entry : cross_relaxation_map) {
        for (const auto& entry1 : entry.second) {
            int key = entry1.first;
            const CrossRelaxation& cross = entry1.second;
            std::cout << "Key: " << entry.first<<" "<<key << ", Total Probability: " << cross.total_probability(1) << std::endl;
        }
    }

    return 0;

    std::cout << "done with tag"<< '\n';

    // Parameters for the simulation 
    // std::vector<double> Tm_conc = {0.15};
    // std::vector<double> power_density = {10000};
    // double t1 = 3000 * 1e-6;
    // double t2 = 5000 * 1e-6;

    // for (const auto& c : Tm_conc) {
    //     for (const auto& p : power_density) {
    //         std::cout << "Running simulation for Tm concentration " << c << ", power density " << p << std::endl;

    //         // sigma from MC paper, SI
    //         tag_default["laser"] = 0.058 * p;
    //         tag_default["laser_tm"] = 0.0084 * p;

    //         // Create Lattice and Simulator objects
    //         Lattice my_lattice(1 - c, c, TmAdjustableParameter::d, TmAdjustableParameter::r0);
    //         Simulator my_simulator(my_lattice, tag_default);

    //         // Run simulation
    //         my_simulator.simulate(t1, t2);

    //         // Process the result (if needed)
    //     }
    // }

    // std::cout << "\nAll progress has been finished." << std::endl;

    return 0;
}
