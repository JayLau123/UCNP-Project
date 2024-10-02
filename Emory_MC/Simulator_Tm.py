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
        self.initialize_transitions()

    def step(self, steps=0.003):
        time_passed = 0

        with tqdm(total=100) as pbar:
            while time_passed < steps:
                selected_transition = self.select_transition()
                self.process_transition(selected_transition)  
                time_passed += -np.log(np.random.rand())/sum(self.transition_table.values())
                
                percent_complete = time_passed/steps * 100
                pbar.n = percent_complete
                pbar.last_print_n = percent_complete
                pbar.update(0)
    
    def initialize_transitions(self):
        self.transition_table = {}
        self.transition_to_point = {}
        for p in self.lattice.points:
            self.add_decay_transitions(p)
            self.add_et_transitions(p)
            self.add_laser_transitions(p) 
    
    def add_decay_transitions(self, p):
        decay = p.get_decay_rates(self.tag)
        for k, v in enumerate(decay):
            self.transition_table[f'1order_{p}_{k}'] = v
            self.transition_to_point[f'1order_{p}_{k}'] = (p, k)
    
    def add_et_transitions(self, p):
        for p_nei, distance in self.lattice.neighbors[p]:
            r = p.react(p_nei, self.cross_relaxation, self.up_conversion, self.tag['c0'], distance)
            if r is not None:
                self.transition_table[f'2order_{p}_{p_nei}'] = r
                self.transition_to_point[f'2order_{p}_{p_nei}'] = (p, p_nei)
            r = p_nei.react(p, self.cross_relaxation, self.up_conversion, self.tag['c0'], distance)
            if r is not None:
                self.transition_table[f'2order_{p_nei}_{p}'] = r
                self.transition_to_point[f'2order_{p_nei}_{p}'] = (p_nei, p)
        
    def add_laser_transitions(self, p):
        if p.type == 'Yb' and p.state == 0:
            self.transition_table[f'0order_{p}_1'] = self.tag['laser']
            self.transition_to_point[f'0order_{p}_1'] = (p, 1)
        elif p.type == 'Tm' and p.state == 7:
            self.transition_table[f'0order_{p}_11'] = self.tag['laser_tm']
            self.transition_to_point[f'0order_{p}_11'] = (p, 11)

    def select_transition(self):
        transitions = np.array(list(self.transition_table.keys()))
        rates = np.array(list(self.transition_table.values()))
        probabilities = rates / rates.sum()
        return np.random.choice(transitions, p=probabilities)
    
    def process_transition(self, selected_transition):
        if selected_transition.startswith('0'):
            self.process_laser_excitation(selected_transition)
        elif selected_transition.startswith('1'):
            self.process_decay(selected_transition)
        else:
            self.process_et(selected_transition)
    
    def process_laser_excitation(self, selected_transition):
        p, new_state = self.transition_to_point[selected_transition]
        self.remove_old_transitions(p)
        p.state = new_state
        self.update_after_transition(p)
    
    def process_decay(self, selected_transition):
        p, new_state = self.transition_to_point[selected_transition]
        self.remove_old_transitions(p)
        p.state = new_state
        self.update_after_transition(p)
    
    def process_et(self, selected_transition):
        p_donor, p_acceptor = self.transition_to_point[selected_transition]
        self.remove_old_transitions(p_donor)
        self.remove_old_transitions(p_acceptor)
        self.handle_energy_transfer(p_donor, p_acceptor)
        self.update_after_transition(p_donor)
        self.update_after_transition(p_acceptor)
        
    
    def update_after_transition(self, p):
        self.add_decay_transitions(p)
        self.add_et_transitions(p)
        self.add_laser_transitions(p)
    
    def remove_old_transitions(self, p):
        for possible_new_state in range(p.state):
            del self.transition_table[f'1order_{p}_{possible_new_state}']
            del self.transition_to_point[f'1order_{p}_{possible_new_state}']

        for p_nei, _ in self.lattice.neighbors[p]:
            if f'2order_{p}_{p_nei}' in self.transition_table:
                del self.transition_table[f'2order_{p}_{p_nei}']
                del self.transition_to_point[f'2order_{p}_{p_nei}']
            if f'2order_{p_nei}_{p}' in self.transition_table:
                del self.transition_table[f'2order_{p_nei}_{p}']
                del self.transition_to_point[f'2order_{p_nei}_{p}']
        
        if p.type == 'Yb' and p.state == 0:
            del self.transition_table[f'0order_{p}_{1}']
            del self.transition_to_point[f'0order_{p}_{1}']
        if p.type == 'Tm' and p.state == 7:
            del self.transition_table[f'0order_{p}_{11}']
            del self.transition_to_point[f'0order_{p}_{11}']

    def handle_energy_transfer(self, p_donor, p_acceptor):
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
