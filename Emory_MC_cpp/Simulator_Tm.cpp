#include "Simulator_Tm.hpp"
#include "Point_Tm.hpp"
#include "Lattice_Tm.hpp"
#include "iostream"
#include "random"

std::unordered_map<int, std::unordered_map<int, CrossRelaxation>> cross_relaxation_map = cross_relaxation();
std::unordered_map<int, UpConversion> up_conversion_map = up_conversion(); 

Simulator::Simulator(Lattice &lattice, const std::unordered_map<std::string, double> &tag)
    : lattice(lattice.deep_copy()), t(0), tag(tag), cross_relaxation(cross_relaxation_map), up_conversion(up_conversion_map) {
    initialize_transitions();
}

void Simulator::step(double steps, bool emission) {
    double time_passed = 0;
    int i = 0;
    while (time_passed < steps) {
        std::string selected_transition = select_transition();
        process_transition(selected_transition, emission);

        std::mt19937 gen(std::random_device{}());
        std::uniform_real_distribution<> dist(0.0, 1.0);
        double random_value = dist(gen);
        double total_rates = std::accumulate(transition_table.begin(), transition_table.end(), 0.0,
                                    [](double sum, const auto &pair) { return sum + pair.second; });
        time_passed += -std::log(random_value) / total_rates;

        // time_passed += -std::log(static_cast<double>(rand()) / RAND_MAX) / 
        //                std::accumulate(transition_table.begin(), transition_table.end(), 0.0,
        //                                [](double sum, const auto &pair) { return sum + pair.second; });
        if (i >= 0) {
            std::cout <<i<< " " << random_value << " "<< total_rates << " "<< time_passed<< " " <<steps<< "\n";
        }
        i++;
        if (i > 10 ) break;
    }
}

void Simulator::initialize_transitions() {
    transition_table.clear();
    transition_to_point.clear();
    for (auto &p : lattice.points) {
        add_decay_transitions(p);
        add_et_transitions(p);
        add_laser_transitions(p);
    }
}

void Simulator::add_decay_transitions(Point &p) {
    std::vector<double> decay = p.get_decay_rates(tag);
    for (size_t k = 0; k < decay.size(); ++k) {
        transition_table["1order_" + p.to_string() + "_" + std::to_string(k)] = decay[k];
        transition_to_point["1order_" + p.to_string() + "_" + std::to_string(k)] = {p, Point(std::make_tuple(0.0, 0.0, 0.0), "Yb", k)};
    }
}

void Simulator::add_et_transitions(Point &p) {
    for (const auto &[p_nei, distance] : lattice.neighbors[p]) {
        auto r = p.react(p_nei, cross_relaxation, up_conversion, tag.at("c0"), distance);
        if (r != 0) {
            transition_table["2order_" + p.to_string() + "_" + p_nei.to_string()] = r;
            transition_to_point["2order_" + p.to_string() + "_" + p_nei.to_string()] = {p, p_nei};
        }
        r = p_nei.react(p, cross_relaxation, up_conversion, tag.at("c0"), distance);
        if (r != 0) {
            transition_table["2order_" + p_nei.to_string() + "_" + p.to_string()] = r;
            transition_to_point["2order_" + p_nei.to_string() + "_" + p.to_string()] = {p_nei, p};
        }
    }
}

void Simulator::add_laser_transitions(Point &p) {
    if (p.type == "Yb" && p.state == 0) {
        transition_table["0order_" + p.to_string() + "_1"] = tag.at("laser");
        transition_to_point["0order_" + p.to_string() + "_1"] = {p, Point(std::make_tuple(0.0, 0.0, 0.0), "Yb", 1)};
    } else if (p.type == "Tm" && p.state == 7) {
        transition_table["0order_" + p.to_string() + "_11"] = tag.at("laser_tm");
        transition_to_point["0order_" + p.to_string() + "_11"] = {p, Point(std::make_tuple(0.0, 0.0, 0.0), "Yb", 11)};
    }
}

std::string Simulator::select_transition() {
    std::vector<std::string> transitions;
    std::vector<double> rates;
    for (const auto &[key, value] : transition_table) {
        transitions.push_back(key);
        rates.push_back(value);
    }

    std::vector<double> probabilities(rates.size());
    double total = std::accumulate(rates.begin(), rates.end(), 0.0);
    std::transform(rates.begin(), rates.end(), probabilities.begin(), [total](double rate) { return rate / total; });

    std::discrete_distribution<int> dist(probabilities.begin(), probabilities.end());
    return transitions[dist(generator)];
}

void Simulator::process_transition(const std::string &selected_transition, bool emission) {
    if (selected_transition.substr(0, 1) == "0") {
        process_laser_excitation(selected_transition);
    } else if (selected_transition.substr(0, 1) == "1") {
        process_decay(selected_transition, emission);
    } else {
        process_et(selected_transition);
    }
}

void Simulator::process_laser_excitation(const std::string &selected_transition) {
    auto [p, new_state] = transition_to_point[selected_transition];
    remove_old_transitions(p);
    p.state = new_state.state;
    update_after_transition(p);
}

void Simulator::process_decay(const std::string &selected_transition, bool emission) {
    auto [p, new_state] = transition_to_point[selected_transition];
    if (emission) {
        if (p.state == 3 && new_state.state == 0) nir++;
        else if (p.state == 6 && new_state.state == 2) nir++;
        else if (p.state == 7 && new_state.state == 4) nir++;
        else if (p.state == 7 && new_state.state == 5) nir++;
        else if (p.state == 8 && new_state.state == 6) nir++;
        else if (p.state == 9 && new_state.state == 6) nir++;

        else if (p.state == 6 && new_state.state == 0) blue++;
        else if (p.state == 7 && new_state.state == 1) blue++;
        else if (p.state == 7 && new_state.state == 2) blue++;
        else if (p.state == 8 && new_state.state == 3) blue++;
        else if (p.state == 8 && new_state.state == 4) blue++;
        else if (p.state == 8 && new_state.state == 5) blue++;
        else if (p.state == 9 && new_state.state == 3) blue++;
        else if (p.state == 9 && new_state.state == 4) blue++;
        else if (p.state == 9 && new_state.state == 5) blue++;
        else if (p.state == 10 && new_state.state == 3) blue++;
        else if (p.state == 10 && new_state.state == 4) blue++;
        else if (p.state == 10 && new_state.state == 5) blue++;
        else if (p.state == 11 && new_state.state == 4) blue++;
        else if (p.state == 11 && new_state.state == 5) blue++;
    }
    remove_old_transitions(p);
    p.state = new_state.state;
    update_after_transition(p);
}

void Simulator::process_et(const std::string &selected_transition) {
    auto [p_donor, p_acceptor] = transition_to_point[selected_transition];
    remove_old_transitions(p_donor);
    remove_old_transitions(p_acceptor);
    handle_energy_transfer(p_donor, p_acceptor);
    update_after_transition(p_donor);
    update_after_transition(p_acceptor);
}

void Simulator::update_after_transition(Point &p) {
    add_decay_transitions(p);
    add_et_transitions(p);
    add_laser_transitions(p);
}

void Simulator::remove_old_transitions(Point &p) {
    for (int possible_new_state = 0; possible_new_state < p.state; ++possible_new_state) {
        transition_table.erase("1order_" + p.to_string() + "_" + std::to_string(possible_new_state));
        transition_to_point.erase("1order_" + p.to_string() + "_" + std::to_string(possible_new_state));
    }

    for (const auto &[p_nei, _] : lattice.neighbors[p]) {
        transition_table.erase("2order_" + p.to_string() + "_" + p_nei.to_string());
        transition_to_point.erase("2order_" + p.to_string() + "_" + p_nei.to_string());
        transition_table.erase("2order_" + p_nei.to_string() + "_" + p.to_string());
        transition_to_point.erase("2order_" + p_nei.to_string() + "_" + p.to_string());
    }

    if (p.type == "Yb" && p.state == 0) {
        transition_table.erase("0order_" + p.to_string() + "_1");
        transition_to_point.erase("0order_" + p.to_string() + "_1");
    }
    if (p.type == "Tm" && p.state == 7) {
        transition_table.erase("0order_" + p.to_string() + "_11");
        transition_to_point.erase("0order_" + p.to_string() + "_11");
    }
}

void Simulator::handle_energy_transfer(Point &p_donor, Point &p_acceptor) {
    if (p_donor.type == "Yb" && p_acceptor.type == "Yb") {
        p_donor.state = 0;
        p_acceptor.state = 1;
    } else if (p_donor.type == "Yb" && p_acceptor.type != "Yb") {
        // upconversion
        auto new_state = up_conversion[p_acceptor.state].select_path(p_donor.to(p_acceptor));
        p_donor.state = new_state.first;
        p_acceptor.state = new_state.second;
    } else {
        // cross relaxation
        auto new_state = cross_relaxation[p_donor.state][p_acceptor.state].select_path(p_donor.to(p_acceptor));
        p_donor.state = new_state.first;
        p_acceptor.state = new_state.second;
    }
}

std::pair<int, int> Simulator::simulate(double t1, double t2) {
    step(t1, false);
    step(t2 - t1, true);
    return {nir, blue}; 
}
