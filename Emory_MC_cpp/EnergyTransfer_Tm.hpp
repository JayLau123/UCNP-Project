#pragma once
#include <vector>
#include <tuple>
#include <string>
#include <unordered_map>

class EnergyTransfer {
public:
    virtual double total_probability(double r) const = 0;
    virtual std::pair<int, int> select_path(double r) const = 0;
    virtual void add_state(int ion12, int ion22, double rate) = 0;
};

class UpConversion : public EnergyTransfer {
private:
    int ion2;
    std::vector<std::tuple<int, int, double>> resulting_states;
public:
    UpConversion(int ion2);
    double total_probability(double r) const override;
    std::pair<int, int> select_path(double r) const override;
    void add_state(int ion12, int ion22, double rate) override;
};

class CrossRelaxation : public EnergyTransfer {
private:
    int ion1, ion2;
    std::vector<std::tuple<int, int, double>> resulting_states;
public:
    CrossRelaxation(int ion1, int ion2);
    double total_probability(double r) const override;
    std::pair<int, int> select_path(double r) const override;
    void add_state(int ion12, int ion22, double rate) override;
};

// Helper functions
std::unordered_map<int, UpConversion> up_conversion();
std::unordered_map<int, std::unordered_map<int, CrossRelaxation>> cross_relaxation();