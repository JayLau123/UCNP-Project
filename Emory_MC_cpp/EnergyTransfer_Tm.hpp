#ifndef ENERGYTRANSFER_TM_HPP
#define ENERGYTRANSFER_TM_HPP

#include "Tm_inf.hpp"
#include "Tm_adjustable_parameter.hpp"
#include <unordered_map>
#include <vector>
#include <string>
#include <random>
#include <cmath>

class EnergyTransfer {
public:
    virtual double total_probability(double r) const = 0;
    virtual std::pair<int, int> select_path(double r) = 0;
    virtual void add_state(int ion12, int ion22, double rate) = 0;
};

class UpConversion : public EnergyTransfer {
public:
    UpConversion();
    UpConversion(int ion2);
    UpConversion(const UpConversion& other);
    double total_probability(double r) const override;
    std::pair<int, int> select_path(double r) override;
    void add_state(int ion12, int ion22, double rate) override;

private:
    int ion2;
    std::vector<std::tuple<int, int, double>> resulting_states;
};

class CrossRelaxation : public EnergyTransfer {
public:
    CrossRelaxation();
    CrossRelaxation(int ion1, int ion2);
    CrossRelaxation(const CrossRelaxation& other);
    double total_probability(double r) const override;
    std::pair<int, int> select_path(double r) override;
    void add_state(int ion12, int ion22, double rate) override;

private:
    int ion1;
    int ion2;
    std::vector<std::tuple<int, int, double>> resulting_states;
};

// Function declarations
std::unordered_map<int, UpConversion> up_conversion();
std::unordered_map<int, std::unordered_map<int, CrossRelaxation>> cross_relaxation();

#endif // ENERGYTRANSFER_TM_HPP