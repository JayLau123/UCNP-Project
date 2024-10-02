#ifndef UTILS_HPP
#define UTILS_HPP

#include <unordered_map>
#include <vector>
#include <string>
#include <random>
#include <cmath>

extern std::unordered_map<std::string, double> Tm_RME;
extern std::unordered_map<std::string, double> Tm_energy;
extern std::unordered_map<std::string, double> Tm_omega;
extern double ET_constant;
extern double threshold;
extern double beta;
extern int n_phonon;
extern double E_phonon;
extern double s0;

class EnergyTransfer {
public:
    virtual double total_probability(double r) = 0;
    virtual std::pair<int, int> select_path(double r) = 0;
    virtual void add_state(int ion12, int ion22, double rate) = 0;
};

class UpConversion : public EnergyTransfer {
public:
    UpConversion(int ion2);
    double total_probability(double r) override;
    std::pair<int, int> select_path(double r) override;
    void add_state(int ion12, int ion22, double rate) override;

private:
    int ion2;
    std::vector<std::tuple<int, int, double>> resulting_states;
};

class CrossRelaxation : public EnergyTransfer {
public:
    CrossRelaxation(int ion1, int ion2);
    double total_probability(double r) override;
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

#endif // UTILS_HPP