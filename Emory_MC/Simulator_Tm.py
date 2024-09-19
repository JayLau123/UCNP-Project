import numpy as np
import random
from tqdm import tqdm

from EnergyTransfer_Tm import *
from Lattice_Tm import *
from Point_Tm import *

from Tm_inf import *
from Tm_Energy import *
from Tm_EnergyLevelDiagram import *
from Tm_RateCalculation import *

class Simulator():

    def __init__(self, lattice, tag = None, excite_tm = False):

        # get_nerighbors(self, r):
        #    self.neighbors = ret 
        # ret is a dic, key is all ion in self.n_points (3401, Yb+Tm), values are many tuples: (nearby ion, distance< 1 nm) 

        self.lattice = lattice.deep_copy()
        self.t = 0

        if tag is not None:
            self.tag = tag
        else:
            self.tag = tag_default

        self.cross_relaxation = cross_relaxation()
        self.up_conversion = up_conversion()    
        self.excite_tm = excite_tm

    def step(self, steps = 0.003, emission = False):

        if emission:

            NIR30s = 0
            NIR62s = 0
            NIR74s = 0
            NIR75s = 0
            NIR86s = 0
            NIR96s = 0


            blue60s = 0
            blue71s = 0
            blue72s = 0
            blue83s = 0
            blue84s = 0
            blue85s = 0
            blue93s = 0
            blue94s = 0
            blue95s = 0
            blue10_3s = 0
            blue10_4s = 0
            blue10_5s = 0
            blue11_4s = 0
            blue11_5s = 0

            yb_upconversions = 0
            yb_ybs = 0
            yb_excites = 0

            tm_decays = 0
            tm_upconversions = {}
            tm_crossrelaxations = {}

            tm_excite_7_11s = 0

        transition_table = {}
        transition_to_point = {}
        time_passed = 0
        for p in self.lattice.points:
            decay = p.get_decay_rates(self.tag)
            # decay is a list of decay rates. k is new state, v is rate
            for k,v in enumerate(decay):
                transition_table[f'1order_{p}_{k}'] = v
                transition_to_point[f'1order_{p}_{k}'] = (p, k)
            
            # ET process
            for p_nei, distance in self.lattice.neighbors[p]:
                r = p.react(p_nei, self.cross_relaxation, self.up_conversion, self.tag['c0'], distance)
                if r is not None:
                    transition_table[f'2order_{p}_{p_nei}'] = r
                    transition_to_point[f'2order_{p}_{p_nei}'] = (p, p_nei)
            
            # laser excites ground state yb to excited yb
            if p.type == 'Yb' and p.state == 0:
                transition_table[f'0order_{p}_1'] = self.tag['laser']
                transition_to_point[f'0order_{p}_1'] = (p, 1)
            elif p.type == 'Tm' and p.state == 7:
                transition_table[f'0order_{p}_11'] = self.tag['laser_tm']
                transition_to_point[f'0order_{p}_1'] = (p, 11)
            
        with tqdm(total=100) as pbar:
            while (time_passed < steps):

                transitions = np.array(list(transition_table.keys()))
                rates = np.array(list(transition_table.values()))
                probabilities = rates / rates.sum()
                selected_transition = np.random.choice(transitions, p = probabilities)

                if selected_transition[0] == '0': # laser excitation
                    p, new_state = transition_to_point[selected_transition]
                    if p.type == 'Yb':
                        yb_excites += 1
                        del transition_table[f'0order_{p}_{1}']
                        del transition_to_point[f'0order_{p}_{1}']
                    elif p.type == 'Tm':
                        tm_excite_7_11s += 1
                        del transition_table[f'0order_{p}_{11}']
                        del transition_to_point[f'0order_{p}_{11}']

                    for possible_new_state in range(p.state):
                        del transition_table[f'1order_{p}_{possible_new_state}']
                        del transition_to_point[f'1order_{p}_{possible_new_state}']
                    for p_nei, distance in self.lattice.neighbors[p]:
                        r = p.react(p_nei, self.cross_relaxation, self.up_conversion, self.tag['c0'], distance)
                        if r is not None:
                            del transition_table[f'2order_{p}_{p_nei}']
                            del transition_to_point[f'2order_{p}_{p_nei}']
                        r = p_nei.react(p, self.cross_relaxation, self.up_conversion, self.tag['c0'], distance)
                        if r is not None:
                            del transition_table[f'2order_{p_nei}_{p}']
                            del transition_to_point[f'2order_{p_nei}_{p}']

                    p.state = new_state

                    decay = p.get_decay_rates(self.tag)
                    for k,v in enumerate(decay):
                        transition_table[f'1order_{p}_{k}'] = v
                        transition_to_point[f'1order_{p}_{k}'] = (p, k)
                    
                    for p_nei, distance in self.lattice.neighbors[p]:
                        r = p.react(p_nei, self.cross_relaxation, self.up_conversion, self.tag['c0'], distance)
                        if r is not None:
                            transition_table[f'2order_{p}_{p_nei}'] = r
                            transition_to_point[f'2order_{p}_{p_nei}'] = (p, p_nei)
                        r = p_nei.react(p, self.cross_relaxation, self.up_conversion, self.tag['c0'], distance)
                        if r is not None:
                            transition_table[f'2order_{p_nei}_{p}'] = r
                            transition_to_point[f'2order_{p_nei}_{p}'] = (p_nei, p)
                    

                elif selected_transition[0] == '1': # decay
                    p, new_state = transition_to_point[selected_transition] 

                    if emission: 

                            if p.state == 3 and new_state == 0:
                                NIR30s += 1

                            if p.state == 6 and new_state == 2:
                                NIR62s += 1

                            if p.state == 7 and new_state == 4:
                                NIR74s += 1

                            if p.state == 7 and new_state == 5:
                                NIR75s += 1

                            if p.state == 8 and new_state == 6:
                                NIR86s += 1

                            if p.state == 9 and new_state == 6:
                                NIR96s += 1

                            if p.state == 6 and new_state == 0:
                                blue60s += 1

                            if p.state == 7 and new_state == 1:
                                blue71s += 1

                            if p.state == 7 and new_state == 2:
                                blue72s += 1

                            if p.state == 8 and new_state == 3:
                                blue83s += 1

                            if p.state == 8 and new_state == 4:
                                blue84s += 1

                            if p.state == 8 and new_state == 5:
                                blue85s += 1

                            if p.state == 9 and new_state == 3:
                                blue93s += 1

                            if p.state == 9 and new_state == 4:
                                blue94s += 1

                            if p.state == 9 and new_state == 5:
                                blue95s += 1

                            if p.state == 10 and new_state == 3:
                                blue10_3s += 1

                            if p.state == 10 and new_state == 4:
                                blue10_4s += 1

                            if p.state == 10 and new_state == 5:
                                blue10_5s += 1

                            if p.state == 11 and new_state == 4:
                                blue11_4s += 1

                            if p.state == 11 and new_state == 5:
                                blue11_5s += 1
                    
                    for possible_new_state in range(p.state):
                        del transition_table[f'1order_{p}_{possible_new_state}']
                        del transition_to_point[f'1order_{p}_{possible_new_state}']
                        
                    for p_nei, distance in self.lattice.neighbors[p]:
                        r = p.react(p_nei, self.cross_relaxation, self.up_conversion, self.tag['c0'], distance)
                        if r is not None:
                            del transition_table[f'2order_{p}_{p_nei}']
                            del transition_to_point[f'2order_{p}_{p_nei}']
                        r = p_nei.react(p, self.cross_relaxation, self.up_conversion, self.tag['c0'], distance)
                        if r is not None:
                            del transition_table[f'2order_{p_nei}_{p}']
                            del transition_to_point[f'2order_{p_nei}_{p}']
                    
                    if p.type == 'Yb' and p.state == 0:
                        del transition_table[f'0order_{p}_{1}']
                        del transition_to_point[f'0order_{p}_{1}']
                    elif p.type == 'Tm' and p.state == 7:
                        del transition_table[f'0order_{p}_{11}']
                        del transition_to_point[f'0order_{p}_{11}']

                    p.state = new_state
                    
                    decay = p.get_decay_rates(self.tag)
                    for k,v in enumerate(decay):
                        transition_table[f'1order_{p}_{k}'] = v
                        transition_to_point[f'1order_{p}_{k}'] = (p, k)
                    
                    for p_nei, distance in self.lattice.neighbors[p]:
                        r = p.react(p_nei, self.cross_relaxation, self.up_conversion, self.tag['c0'], distance)
                        if r is not None:
                            transition_table[f'2order_{p}_{p_nei}'] = r
                            transition_to_point[f'2order_{p}_{p_nei}'] = (p, p_nei)
                        r = p_nei.react(p, self.cross_relaxation, self.up_conversion, self.tag['c0'], distance)
                        if r is not None:
                            transition_table[f'2order_{p_nei}_{p}'] = r
                            transition_to_point[f'2order_{p_nei}_{p}'] = (p_nei, p)
                    
                    if p.type == 'Yb' and p.state == 0:
                        transition_table[f'0order_{p}_1'] = self.tag['laser']
                        transition_to_point[f'0order_{p}_1'] = (p, 1)
                    elif p.type == 'Tm' and p.state == 7:
                        transition_table[f'0order_{p}_11'] = self.tag['laser_tm']
                        transition_to_point[f'0order_{p}_1'] = (p, 11)

                else: # ET
                    p_donor, p_acceptor = transition_to_point[selected_transition]

                    for possible_new_state in range(p_donor.state):
                        del transition_table[f'1order_{p_donor}_{possible_new_state}']
                        del transition_to_point[f'1order_{p_donor}_{possible_new_state}']
                    for possible_new_state in range(p_acceptor.state):
                        del transition_table[f'1order_{p_acceptor}_{possible_new_state}']
                        del transition_to_point[f'1order_{p_acceptor}_{possible_new_state}']
                    
                    if p_donor.type == 'Yb' and p_donor.state == 0:
                        del transition_table[f'0order_{p_donor}_{1}']
                        del transition_to_point[f'0order_{p_donor}_{1}']
                    elif p_donor.type == 'Tm' and p_donor.state == 7:
                        del transition_table[f'0order_{p_donor}_{11}']
                        del transition_to_point[f'0order_{p_donor}_{11}']
                    if p_acceptor.type == 'Yb' and p_acceptor.state == 0:
                        del transition_table[f'0order_{p_acceptor}_{1}']
                        del transition_to_point[f'0order_{p_acceptor}_{1}']
                    elif p_acceptor.type == 'Tm' and p_acceptor.state == 7:
                        del transition_table[f'0order_{p_acceptor}_{11}']
                        del transition_to_point[f'0order_{p_acceptor}_{11}']
                        
                    for p_nei, distance in self.lattice.neighbors[p_donor]:
                        r = p_donor.react(p_nei, self.cross_relaxation, self.up_conversion, self.tag['c0'], distance)
                        if r is not None:
                            del transition_table[f'2order_{p_donor}_{p_nei}']
                            del transition_to_point[f'2order_{p_donor}_{p_nei}'] 
                        r = p_nei.react(p_donor, self.cross_relaxation, self.up_conversion, self.tag['c0'], distance)
                        if r is not None:
                            del transition_table[f'2order_{p_nei}_{p_donor}']
                            del transition_to_point[f'2order_{p_nei}_{p_donor}'] 
                        
                    for p_nei, distance in self.lattice.neighbors[p_acceptor]:
                        if p_nei == p_donor:
                            continue
                        r = p_acceptor.react(p_nei, self.cross_relaxation, self.up_conversion, self.tag['c0'], distance)
                        if r is not None:
                            del transition_table[f'2order_{p_acceptor}_{p_nei}']
                            del transition_to_point[f'2order_{p_acceptor}_{p_nei}'] 
                        r = p_nei.react(p_acceptor, self.cross_relaxation, self.up_conversion, self.tag['c0'], distance)
                        if r is not None:
                            del transition_table[f'2order_{p_nei}_{p_acceptor}']
                            del transition_to_point[f'2order_{p_nei}_{p_acceptor}'] 
                    

                    if p_donor.type == 'Yb' and p_acceptor.type == 'Yb':
                        p_donor.state = 0
                        p_acceptor.state = 1
                        yb_ybs += 1

                    elif p_donor.type == 'Yb' and p_acceptor.type != 'Yb':
                        new_state = self.up_conversion[p_acceptor.state].select_path(p_donor.to(p_acceptor))
                        if emission:
                            yb_upconversions += 1
                            tm_upconversions[(p_acceptor.state, new_state[1])] = tm_upconversions.setdefault((p_acceptor.state, new_state[1]), 0) + 1
                        p_donor.state = new_state[0]
                        p_acceptor.state = new_state[1]
                    else:
                        new_state = self.cross_relaxation[p_donor.state][p_acceptor.state].select_path(p_donor.to(p_acceptor))
                        if emission:
                            tm_crossrelaxations[(p_donor.state, new_state[0], p_acceptor.state, new_state[1])] = tm_crossrelaxations.setdefault((p_donor.state, new_state[0], p_acceptor.state, new_state[1]), 0) + 1
                        p_donor.state = new_state[0]
                        p_acceptor.state = new_state[1]

                    decay = p_donor.get_decay_rates(self.tag)
                    for k,v in enumerate(decay):
                        transition_table[f'1order_{p_donor}_{k}'] = v
                        transition_to_point[f'1order_{p_donor}_{k}'] = (p_donor, k)
                    
                    for p_nei, distance in self.lattice.neighbors[p_donor]:
                        r = p_donor.react(p_nei, self.cross_relaxation, self.up_conversion, self.tag['c0'], distance)
                        if r is not None:
                            transition_table[f'2order_{p_donor}_{p_nei}'] = r
                            transition_to_point[f'2order_{p_donor}_{p_nei}'] = (p_donor, p_nei)
                        r = p_nei.react(p_donor, self.cross_relaxation, self.up_conversion, self.tag['c0'], distance)
                        if r is not None:
                            transition_table[f'2order_{p_nei}_{p_donor}'] = r
                            transition_to_point[f'2order_{p_nei}_{p_donor}'] = (p_nei, p_donor)

                    if p_donor.type == 'Yb' and p_donor.state == 0:
                        transition_table[f'0order_{p_donor}_1'] = self.tag['laser']
                        transition_to_point[f'0order_{p_donor}_1'] = (p_donor, 1)
                    elif p_donor.type == 'Tm' and p_donor.state == 7:
                        transition_table[f'0order_{p_donor}_11'] = self.tag['laser_tm']
                        transition_to_point[f'0order_{p_donor}_1'] = (p_donor, 11)

                    decay = p_acceptor.get_decay_rates(self.tag)
                    for k,v in enumerate(decay):
                        transition_table[f'1order_{p_acceptor}_{k}'] = v
                        transition_to_point[f'1order_{p_acceptor}_{k}'] = (p_acceptor, k)
                    
                    for p_nei, distance in self.lattice.neighbors[p_acceptor]:
                        if p_nei == p_donor:
                            continue
                        r = p_acceptor.react(p_nei, self.cross_relaxation, self.up_conversion, self.tag['c0'], distance)
                        if r is not None:
                            transition_table[f'2order_{p_acceptor}_{p_nei}'] = r
                            transition_to_point[f'2order_{p_acceptor}_{p_nei}'] = (p_acceptor, p_nei)
                        r = p_nei.react(p_acceptor, self.cross_relaxation, self.up_conversion, self.tag['c0'], distance)
                        if r is not None:
                            transition_table[f'2order_{p_nei}_{p_acceptor}'] = r
                            transition_to_point[f'2order_{p_nei}_{p_acceptor}'] = (p_nei, p_acceptor)

                    if p_acceptor.type == 'Yb' and p_acceptor.state == 0:
                        transition_table[f'0order_{p_acceptor}_1'] = self.tag['laser']
                        transition_to_point[f'0order_{p_acceptor}_1'] = (p_acceptor, 1)
                    elif p_acceptor.type == 'Tm' and p_acceptor.state == 7:
                        transition_table[f'0order_{p_acceptor}_11'] = self.tag['laser_tm']
                        transition_to_point[f'0order_{p_acceptor}_1'] = (p_acceptor, 11)
                    
                time_passed += -np.log(np.random.rand())/rates.sum()
                percent_complete = (time_passed / steps) * 100
                pbar.n = percent_complete
                pbar.last_print_n = percent_complete
                pbar.update(0)

        if emission:
 
            step_data = {}

            step_data['NIR30s'] = NIR30s
            step_data['NIR62s'] = NIR62s
            step_data['NIR74s'] = NIR74s
            step_data['NIR75s'] = NIR75s
            step_data['NIR86s'] = NIR86s
            step_data['NIR96s'] = NIR96s

            step_data['blue60s'] = blue60s
            step_data['blue71s'] = blue71s
            step_data['blue72s'] = blue72s
            step_data['blue83s'] = blue83s
            step_data['blue84s'] = blue84s
            step_data['blue85s'] = blue85s
            step_data['blue93s'] = blue93s
            step_data['blue94s'] = blue94s
            step_data['blue95s'] = blue95s
            step_data['blue10_3s'] = blue10_3s
            step_data['blue10_4s'] = blue10_4s
            step_data['blue10_5s'] = blue10_5s
            step_data['blue11_4s'] = blue11_4s
            step_data['blue11_5s'] = blue11_5s

            step_data['NIR'] = NIR30s, NIR62s, NIR74s, NIR75s, NIR86s, NIR96s
            step_data['blue'] = blue60s, blue71s, blue72s, blue83s, blue84s, blue85s, blue93s, blue94s, blue95s, blue10_3s, blue10_4s, blue10_5s,blue11_4s, blue11_5s


            step_data['yb_upconversions'] = yb_upconversions
            step_data['yb_ybs'] = yb_ybs
            step_data['yb_excites'] = yb_excites

            step_data['tm_decays'] = tm_decays
            step_data['tm_upconversions'] = tm_upconversions
            step_data['tm_crossrelaxations'] = tm_crossrelaxations
            step_data['tm_excite_7_11s'] = tm_excite_7_11s

            return step_data
    
    # def show_state(self):
    #     self.lattice.plot_3d_points_with_plotly()
    
    # def plot_distributions(self):
    #     self.lattice.plot_distributions()

    def simulate(self, t1, t2):

        ## At 2500 steps, reach steady state

        self.step(t1, emission=True)
        sim_stats = self.step(t2-t1)

        return sim_stats
    


'''
    def plot_stats(self, yb_stats, er_stats):

        plt.figure(figsize=(15, 5))

        # 1 row, 3 columns, 1st plot
        plt.subplot(1, 3, 1)

        bars = plt.bar(['Yb', 'Er', 'Y'], [self.lattice.yb_num, self.lattice.er_num, self.lattice.n_points-self.lattice.yb_num-self.lattice.er_num], color=['blue', 'pink', 'green'], width=0.4)
        plt.ylabel('Count',fontsize=18)
        plt.title('Distribution of three types',fontsize=18)
        plt.xticks(['Yb', 'Er', 'Y'], ['Sensitizers', 'Emitters', 'Others'],fontsize=16)
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 5, yval, ha='center', va='bottom')

        # Plotting value distribution for type A using histogram
        # 1 row, 3 columns, 2nd plot
        yb_avg = []
        for i in range(len(yb_stats[0])):
            yb_avg.append(np.mean([j[i] for j in yb_stats]))
        plt.subplot(1, 3, 2)
        bars = plt.bar([0,1], yb_avg, color='blue', width=0.4)
        plt.ylabel('Count',fontsize=18)
        plt.title('Value distribution for sensitizers',fontsize=18)
        plt.xticks([0, 1], ['0(Ground state)', '1(Excited state)'],fontsize=16)
        for i, bar in enumerate(bars):
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 5, round(yb_avg[i],1), ha='center', va='bottom')

        # Plotting value distribution for type B using histogram
        # 1 row, 3 columns, 3rd plot
        er_avg = []
        for i in range(len(er_stats[0])):
            er_avg.append(np.mean([j[i] for j in er_stats]))
        plt.subplot(1, 3, 3)
        bars = plt.bar([0,1,2,3,4,5,6,7], er_avg, color='pink', width=0.4)
        plt.ylabel('Count',fontsize=18)
        plt.title('Value distribution for emitters',fontsize=18)
        plt.xticks([0, 1, 2, 3, 4, 5, 6, 7], ['G', '1st', '2nd', '3rd', '4th', '5th', '6th', '7th'],fontsize=16)
        for i, bar in enumerate(bars):
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 5, round(er_avg[i],1), ha='center', va='bottom')

        plt.tight_layout()
        plt.show()
'''

        

