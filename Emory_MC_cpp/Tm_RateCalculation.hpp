#ifndef TM_RATECALCULATION_HPP
#define TM_RATECALCULATION_HPP

#include <unordered_map>
#include <string>
#include <vector>

std::unordered_map<std::string, double> ED_cal(
    const std::unordered_map<std::string, double>& energy_dict, 
    const std::unordered_map<std::string, double>& omega, 
    const std::unordered_map<std::string, std::vector<double>>& RME_square, 
    double n
);

std::unordered_map<std::string, double> MD_cal(
    const std::unordered_map<std::string, double>& energy_dict, 
    double n
);

std::unordered_map<std::string, double> MPR_cal(
    const std::unordered_map<std::string, double>& energy_dict, 
    double W0, 
    double alpha, 
    double phonon
);

#endif // TM_RATECALCULATION_HPP