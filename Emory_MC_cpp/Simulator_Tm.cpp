#include "Simulator.h"
#include "Lattice.h"
#include "Point.h"

Simulator::Simulator(const Lattice &lattice, const std::unordered_map<std::string, double> &tag)
    : lattice(lattice.deep_copy()), t(0), tag(tag) {}

void Simulator::step(double steps) {
    std::unordered_map<std::string, double> transition_table;
    std::unordered_map<std::string, std::pair<Point*, int>> transition_to_point;
    initialize_transitions(transition_table, transition_to_point);

    double time_passed = 0;

    while (time_passed < steps) {
        std::string selected_transition = select_transition(transition_table);
        process_transition(selected_transition, transition_table, transition_to_point);
        time_passed += -log((double)rand() / RAND_MAX) / transition_table[selected_transition];
    }
}

void Simulator::initialize_transitions(std::unordered_map<std::string, double> &transition_table, std::unordered_map<std::string, std::pair<Point*, int>> &transition_to_point) {
    for (Point &p : lattice.points) {
        add_decay_transitions(p, transition_table, transition_to_point);
        add_et_transitions(p, transition_table, transition_to_point);
        add_laser_transitions(p, transition_table, transition_to_point);
    }
}

void Simulator::add_decay_transitions(Point &p, std::unordered_map<std::string, double> &transition_table, std::unordered_map<std::string, std::pair<Point*, int>> &transition_to_point) {
    std::vector<double> decay = p.get_decay_rates(tag);
    for (size_t k = 0; k < decay.size(); ++k) {
        transition_table["1order_" + std::to_string(reinterpret_cast<intptr_t>(&p)) + "_" + std::to_string(k)] = decay[k];
        transition_to_point["1order_" + std::to_string(reinterpret_cast<intptr_t>(&p)) + "_" + std::to_string(k)] = std::make_pair(&p, k);
    }
}

void Simulator::add_et_transitions(Point &p, std::unordered_map<std::string, double> &transition_table, std::unordered_map<std::string, std::pair<Point*, int>> &transition_to_point) {
    for (auto &[p_nei, distance] : lattice.neighbors[p]) {
        double r = p.react(p_nei, cross_relaxation, up_conversion, tag.at("c0"), distance);
        if (r > 0) {
            transition_table["2order_" + std::to_string(reinterpret_cast<intptr_t>(&p)) + "_" + std::to_string(reinterpret_cast<intptr_t>(&p_nei))] = r;
            transition_to_point["2order_" + std::to_string(reinterpret_cast<intptr_t>(&p)) + "_" + std::to_string(reinterpret_cast<intptr_t>(&p_nei))] = std::make_pair(&p, reinterpret_cast<intptr_t>(&p_nei));
        }
    }
}

void Simulator::add_laser_transitions(Point &p, std::unordered_map<std::string, double> &transition_table, std::unordered_map<std::string, std::pair<Point*, int>> &transition_to_point) {
    if (p.type == "Yb" && p.state == 0) {
        transition_table["0order_" + std::to_string(reinterpret_cast<intptr_t>(&p)) + "_1"] = tag.at("laser");
        transition_to_point["0order_" + std::to_string(reinterpret_cast<intptr_t>(&p)) + "_1"] = std::make_pair(&p, 1);
    } else if (p.type == "Tm" && p.state == 7) {
        transition_table["0order_" + std::to_string(reinterpret_cast<intptr_t>(&p)) + "_11"] = tag.at("laser_tm");
        transition_to_point["0order_" + std::to_string(reinterpret_cast<intptr_t>(&p)) + "_11"] = std::make_pair(&p, 11);
    }
}

std::string Simulator::select_transition(const std::unordered_map<std::string, double> &transition_table) {
    double total_rate = 0;
    for (const auto &entry : transition_table) total_rate += entry.second;

    double r = ((double)rand() / RAND_MAX) * total_rate;
    double sum = 0;

    for (const auto &entry : transition_table) {
        sum += entry.second;
        if (sum >= r) return entry.first;
    }

    return "";
}

void Simulator::process_transition(const std::string &selected_transition, std::unordered_map<std::string, double> &transition_table, std::unordered_map<std::string, std::pair<Point*, int>> &transition_to_point) {
    if (selected_transition[0] == '0') {
        process_laser_excitation(selected_transition, transition_table, transition_to_point);
    } else if (selected_transition[0] == '1') {
        process_decay(selected_transition, transition_table, transition_to_point);
    } else {
        process_et(selected_transition, transition_table, transition_to_point);
    }
}

void Simulator::process_laser_excitation(const std::string &selected_transition, std::unordered_map<std::string, double> &transition_table, std::unordered_map<std::string, std::pair<Point*, int>> &transition_to_point) {
    auto [p, new_state] = transition_to_point[selected_transition];
    remove_old_transitions(*p, transition_table, transition_to_point);
    p->state = new_state;
    update_after_transition(*p, transition_table, transition_to_point);
}

void Simulator::process_decay(const std::string &selected_transition, std::unordered_map<std::string, double> &transition_table, std::unordered_map<std::string, std::pair<Point*, int>> &transition_to_point) {
    auto [p, new_state] = transition_to_point[selected_transition];
    remove_old_transitions(*p, transition_table, transition_to_point);
    p->state = new_state;
    update_after_transition(*p, transition_table, transition_to_point);
}

void Simulator::process_et(const std::string &selected_transition, std::unordered_map<std::string, double> &transition_table, std::unordered_map<std::string, std::pair<Point*, int>> &transition_to_point) {
    auto [p_donor, p_acceptor_ptr] = transition_to_point[selected_transition];
    Point &p_acceptor = *reinterpret_cast<Point*>(p_acceptor_ptr);

    handle_energy_transfer(*p_donor, p_acceptor, transition_table, transition_to_point);
}

void Simulator::update_after_transition(Point &p, std::unordered_map<std::string, double> &transition_table, std::unordered_map<std::string, std::pair<Point*, int>> &transition_to_point) {
    add_decay_transitions(p, transition_table, transition_to_point);
    add_et_transitions(p, transition_table, transition_to_point);
    add_laser_transitions(p, transition_table, transition_to_point);
}

void Simulator::remove_old_transitions(Point &p, std::unordered_map<std::string, double> &transition_table, std::unordered_map<std::string, std::pair<Point*, int>> &transition_to_point) {
    for (auto it = transition_table.begin(); it != transition_table.end();) {
        if (it->first.find(std::to_string(reinterpret_cast<intptr_t>(&p))) != std::string::npos) {
            transition_to_point.erase(it->first);
            it = transition_table.erase(it);
        } else {
            ++it;
        }
    }
}

void Simulator::handle_energy_transfer(Point &p_donor, Point &p_acceptor, std::unordered_map<std::string, double> &transition_table, std::unordered_map<std::string, std::pair<Point*, int>> &transition_to_point) {
    if (p_donor.type == "Yb" && p_acceptor.type == "Tm") {
        remove_old_transitions(p_donor, transition_table, transition_to_point);
        remove_old_transitions(p_acceptor, transition_table, transition_to_point);

        p_donor.state -= 1;
        p_acceptor.state += 1;

        update_after_transition(p_donor, transition_table, transition_to_point);
        update_after_transition(p_acceptor, transition_table, transition_to_point);
    }
}

void Simulator::simulate(double t1, double t2) {
    while (t < t2) {
        step();
        t += 0.003;
    }
}

