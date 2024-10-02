import numpy as np
from EnergyTransfer_Tm import *
from Lattice_Tm import *
from Point_Tm import *
from Tm_inf import *

class Simulator():

    def __init__(self, lattice, tag):
        
        self.lattice = lattice.deep_copy()
        self.t = 0
        self.tag = tag
        self.cross_relaxation = cross_relaxation()
        self.up_conversion = up_conversion()  

    def step(self, steps=0.003):
        transition_table, transition_to_point = self.initialize_transitions()
        time_passed = 0
        
        while time_passed < steps:
            selected_transition = self.select_transition(transition_table)
            self.process_transition(selected_transition, transition_table, transition_to_point)  
            time_passed += -np.log(np.random.rand())/sum(transition_table.values())

    def initialize_transitions(self):
        transition_table = {}
        transition_to_point = {}
        for p in self.lattice.points:
            self.add_decay_transitions(p, transition_table, transition_to_point)
            self.add_et_transitions(p, transition_table, transition_to_point)
            self.add_laser_transitions(p, transition_table, transition_to_point)
        return transition_table, transition_to_point
    
    def add_decay_transitions(self, p, transition_table, transition_to_point):
        decay = p.get_decay_rates(self.tag)
        for k, v in enumerate(decay):
            transition_table[f'1order_{p}_{k}'] = v
            transition_to_point[f'1order_{p}_{k}'] = (p, k)
    
    def add_et_transitions(self, p, transition_table, transition_to_point):
        for p_nei, distance in self.lattice.neighbors[p]:
            r = p.react(p_nei, self.cross_relaxation, self.up_conversion, self.tag['c0'], distance)
            if r is not None:
                transition_table[f'2order_{p}_{p_nei}'] = r
                transition_to_point[f'2order_{p}_{p_nei}'] = (p, p_nei)
            r = p_nei.react(p, self.cross_relaxation, self.up_conversion, self.tag['c0'], distance)
            if r is not None:
                transition_table[f'2order_{p_nei}_{p}'] = r
                transition_to_point[f'2order_{p_nei}_{p}'] = (p_nei, p)
        
    def add_laser_transitions(self, p, transition_table, transition_to_point):
        if p.type == 'Yb' and p.state == 0:
            transition_table[f'0order_{p}_1'] = self.tag['laser']
            transition_to_point[f'0order_{p}_1'] = (p, 1)
        elif p.type == 'Tm' and p.state == 7:
            transition_table[f'0order_{p}_11'] = self.tag['laser_tm']
            transition_to_point[f'0order_{p}_11'] = (p, 11)

    def select_transition(self, transition_table):
        transitions = np.array(list(transition_table.keys()))
        rates = np.array(list(transition_table.values()))
        probabilities = rates / rates.sum()
        return np.random.choice(transitions, p=probabilities)
    
    def process_transition(self, selected_transition, transition_table, transition_to_point):
        if selected_transition.startswith('0'):
            self.process_laser_excitation(selected_transition, transition_table, transition_to_point)
        elif selected_transition.startswith('1'):
            self.process_decay(selected_transition, transition_table, transition_to_point)
        else:
            self.process_et(selected_transition, transition_table, transition_to_point)
    
    def process_laser_excitation(self, selected_transition, transition_table, transition_to_point):
        p, new_state = transition_to_point[selected_transition]
        self.remove_old_transitions(p, transition_table, transition_to_point)
        p.state = new_state
        self.update_after_transition(p, transition_table, transition_to_point)
    
    def process_decay(self, selected_transition, transition_table, transition_to_point):
        p, new_state = transition_to_point[selected_transition]
        self.remove_old_transitions(p, transition_table, transition_to_point)
        p.state = new_state
        self.update_after_transition(p, transition_table, transition_to_point)
    
    def process_et(self, selected_transition, transition_table, transition_to_point):
        p_donor, p_acceptor = transition_to_point[selected_transition]
        self.remove_old_transitions(p_donor, transition_table, transition_to_point)
        self.remove_old_transitions(p_acceptor, transition_table, transition_to_point)
        self.handle_energy_transfer(p_donor, p_acceptor, transition_table, transition_to_point)
        self.update_after_transition(p_donor, transition_table, transition_to_point)
        self.update_after_transition(p_acceptor, transition_table, transition_to_point)
        
    
    def update_after_transition(self, p, transition_table, transition_to_point):
        self.add_decay_transitions(p, transition_table, transition_to_point)
        self.add_et_transitions(p, transition_table, transition_to_point)
        self.add_laser_transitions(p, transition_table, transition_to_point)
    
    def remove_old_transitions(self, p, transition_table, transition_to_point):
        for possible_new_state in range(p.state):
            del transition_table[f'1order_{p}_{possible_new_state}']
            del transition_to_point[f'1order_{p}_{possible_new_state}']

        for p_nei, _ in self.lattice.neighbors[p]:
            if f'2order_{p}_{p_nei}' in transition_table:
                del transition_table[f'2order_{p}_{p_nei}']
                del transition_to_point[f'2order_{p}_{p_nei}']
            if f'2order_{p_nei}_{p}' in transition_table:
                del transition_table[f'2order_{p_nei}_{p}']
                del transition_to_point[f'2order_{p_nei}_{p}']
        
        if p.type == 'Yb' and p.state == 0:
            del transition_table[f'0order_{p}_{1}']
            del transition_to_point[f'0order_{p}_{1}']
        if p.type == 'Tm' and p.state == 7:
            del transition_table[f'0order_{p}_{11}']
            del transition_to_point[f'0order_{p}_{11}']

    def handle_energy_transfer(self, p_donor, p_acceptor, transition_table, transition_to_point):
        if p_donor.type == 'Yb' and p_acceptor.type == 'Yb':
            p_donor.state = 0
            p_acceptor.state = 1
        elif p_donor.type == 'Yb' and p_acceptor.type != 'Yb': 
            # upconversion
            new_state = self.up_conversion[p_acceptor.state].select_path(p_donor.to(p_acceptor))
            p_donor.state = new_state[0]
            p_acceptor.state = new_state[1]
        else:
            # cross relaxation
            new_state = self.cross_relaxation[p_donor.state][p_acceptor.state].select_path(p_donor.to(p_acceptor))
            p_donor.state = new_state[0]
            p_acceptor.state = new_state[1]

    def simulate(self, t1, t2):

        self.step(t1)
        sim_stats = self.step(t2-t1)

        return sim_stats
