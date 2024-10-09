#include "Tm_RateCalculation.hpp"
#include "Tm_adjustable_parameter.hpp"
#include <cmath>
#include <unordered_map>
#include <string>
#include <vector>
#include <algorithm>
#include <iostream>

// ED_cal function definition
std::unordered_map<std::string, double> ED_cal(
    const std::unordered_map<std::string, double>& energy_dict, 
    const std::unordered_map<std::string, double>& omega, 
    const std::unordered_map<std::string, std::vector<double>>& RME_square, 
    double n
) {
    std::unordered_map<std::string, double> energy_gaps;
    std::vector<std::string> keys;
    
    // Extract keys
    for (const auto& item : energy_dict) {
        keys.push_back(item.first);
    }

    // Compute energy gaps
    for (size_t i = 0; i < keys.size(); ++i) {
        for (size_t j = i + 1; j < keys.size(); ++j) {
            std::string start_level = keys[j];
            std::string end_level = keys[i];
            std::string start_E = start_level.substr(0, start_level.find('('));
            std::string end_E = end_level.substr(0, end_level.find('('));
            std::string key = start_E + end_E;
            energy_gaps[key] = energy_dict.at(start_level) - energy_dict.at(end_level);
        }
    }

    double n_term = (n * (std::pow(n, 2) + 2) * (std::pow(n, 2) + 2)) / 9;
    double ED_constant = (64 * std::pow(M_PI, 4) * std::pow(4.8e-10, 2)) / (3 * 6.6261e-27);
    std::unordered_map<std::string, double> dic_ED;

    for (const auto& [key, RME_vals] : RME_square) {
        double S = omega.at("2") * RME_vals[0] + omega.at("4") * RME_vals[1] + omega.at("6") * RME_vals[2];
        dic_ED[key] = ED_constant * (std::pow(energy_gaps[key], 3) / 3.0) * n_term * S;
    }

    return dic_ED;
}


std::unordered_map<std::string, double> MD_cal(const std::unordered_map<std::string, double>& energy_dict) {
    // MD selection rule, from Xueyuan Chen

    // Function to extract the symbol part from strings like 'E0(3H6)'
    auto extract_symbol = [](const std::string& energy_str) {
        return energy_str.substr(energy_str.find('(') + 1, energy_str.length() - energy_str.find('(') - 2);
    };

    // Function to compare two symbols according to specified criteria
    auto compare_symbols = [](const std::string& symbol1, const std::string& symbol2) {
        return (symbol1[0] == symbol2[0] &&
                symbol1[1] == symbol2[1] &&
                std::abs(static_cast<int>(symbol1[2]) - static_cast<int>(symbol2[2])) == 1);
    };

    std::vector<std::pair<std::pair<std::string, double>, std::pair<std::string, double>>> pairs;
    std::vector<std::string> keys;
    
    for (const auto& pair : energy_dict) {
        keys.push_back(pair.first);
    }

    for (size_t i = 0; i < keys.size(); ++i) {
        const auto& key1 = keys[i];
        const auto& value1 = energy_dict.at(key1);
        auto symbol1 = extract_symbol(key1);
        
        for (size_t j = i + 1; j < keys.size(); ++j) {
            const auto& key2 = keys[j];
            const auto& value2 = energy_dict.at(key2);
            auto symbol2 = extract_symbol(key2);
            
            if (compare_symbols(symbol1, symbol2)) {
                std::pair<std::string, double> pair1 = {key1, value1};
                std::pair<std::string, double> pair2 = {key2, value2};
                
                if (value1 > value2) {
                    pairs.push_back({pair2, pair1});
                } else {
                    pairs.push_back({pair1, pair2});
                }
            }
        }
    }

    // Calculate the MD rates
    double MD_constant = (4 * (6.626e-27) * pow(3.14, 2) * pow(4.8e-10, 2) * pow(TmAdjustableParameter::n, 3)) / (3 * pow(9.11e-28, 2) * pow(3e10, 2));

    std::unordered_map<char, int> L_QN = { {'S', 0}, {'P', 1}, {'D', 2}, {'F', 3}, {'G', 4}, 
                                  {'H', 5}, {'I', 6}, {'K', 7}, {'L', 8}, {'M', 9}, 
                                  {'N', 10}, {'O', 11}, {'Q', 12}, {'R', 13}, 
                                  {'T', 14}, {'U', 15}, {'V', 16} };

    std::unordered_map<std::string, double> dic_MD;

    for (const auto& pair : pairs) {
        auto end_level = pair.first.first;
        auto start_level = pair.second.first;

        std::string start_E = start_level.substr(0, start_level.find('(')); // E2
        std::string end_E = end_level.substr(0, end_level.find('(')); // E0
        std::string key = start_E + end_E; // E2E0
        
        std::string start_symbol = extract_symbol(start_level); // 3H5
        std::string end_symbol = extract_symbol(end_level); // 3H6

        double start_value = pair.second.second, end_value = pair.first.second, delta_v = start_value - end_value;
        
        double S = (std::stoi(std::string(1, start_symbol[0])) - 1) / 2.0;
        int L = L_QN[start_symbol[1]], J = start_symbol[2] - '0';
        double RME_square, value;
        // J to J+1
        if (end_symbol[2] > start_symbol[2]) {
            RME_square = ((S + L + 1) * (S + L + 1) - (J + 1) * (J + 1)) * 
                                ((J + 1) * (J + 1) - (L - S) * (L - S)) / (4 * (J + 1));
            value = MD_constant * (delta_v * delta_v * delta_v / (2 * J + 1)) * RME_square;
        // J+1 to J
        } else if (end_symbol[2] < start_symbol[2]) {
            RME_square = ((S + L + 1) * (S + L + 1) - J * J) * 
                                (J * J - (L - S) * (L - S)) / (4 * J);
            value = MD_constant * (delta_v * delta_v * delta_v / (2 * J + 1)) * RME_square;
        // J to J
        } else {
            RME_square = (2 * J + 1) / (4 * J * (J + 1));
            value = MD_constant * (delta_v * delta_v * delta_v / (2 * J + 1)) * RME_square;
        }
        dic_MD[key] = value;
    }

    return dic_MD;
}


// MPR_cal function definition
std::unordered_map<std::string, double> MPR_cal(
    const std::unordered_map<std::string, double>& energy_dict, 
    double W0, 
    double alpha, 
    double phonon
) {
    std::unordered_map<std::string, double> energy_gaps;
    std::vector<std::string> keys;
    
    for (const auto& item : energy_dict) {
        keys.push_back(item.first);
    }

    for (size_t i = 1; i < keys.size(); ++i) {
        std::string start_level = keys[i];
        std::string end_level = keys[i - 1];
        std::string start_E = start_level.substr(0, start_level.find('('));
        std::string end_E = end_level.substr(0, end_level.find('('));
        std::string key = start_E + end_E;
        energy_gaps[key] = energy_dict.at(start_level) - energy_dict.at(end_level);
    }

    std::unordered_map<std::string, double> dic_MPR;
    for (const auto& [key, gap] : energy_gaps) {
        dic_MPR[key] = W0 * std::exp(-alpha * (gap - 2 * phonon));
    }

    return dic_MPR;
}