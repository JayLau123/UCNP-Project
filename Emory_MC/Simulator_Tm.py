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

    def step(self, steps = 1, emission = False):

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
            tm_upconversions = 0
            tm_crossrelaxations = 0

            tm_excite_7_11s = 0

        transition_table = {}
        transition_to_point = {}
        for p in self.lattice.points:
            decay = p.get_decay_rates(self.tag)
            for k,v in decay.items():
                transition_table[f'1order_{p}_{k}'] = v
                transition_to_point[f'1order_{p}_{k}'] = (p, k)
            
            for p_nei in self.lattice.neighbors[p]:
                r = p.react(nei, self.cross_relaxation, self.up_conversion, self.tag['c0'], distance)
                if r is not None:
                    transition_table[f'2order_{p}_{p_nei}'] = r
                    transition_to_point[f'2order_{p}_{p_nei}'] = (p, p_nei)
            
        for _ in range(steps):

            transitions = np.array(list(transition_table.keys()))
            rates = np.array(list(transition_table.values()))
            probabilities = rates / rates.sum()
            selected_transition = np.random.choice(transitions, p = probabilities)
            if selected_transition[0] == '1': # decay
                p, new_state = transition_to_point[selected_transition] 

                if emission: 

                        if p.state == 3 and new_state == 0:
                            NIR30 += 1

                        if p.state == 6 and new_state == 2:
                            NIR62 += 1

                        if p.state == 7 and new_state == 4:
                            NIR74 += 1

                        if p.state == 7 and new_state == 5:
                            NIR75 += 1

                        if p.state == 8 and new_state == 6:
                            NIR86 += 1

                        if p.state == 9 and new_state == 6:
                            NIR96 += 1

                        if p.state == 6 and new_state == 0:
                            blue60 += 1

                        if p.state == 7 and new_state == 1:
                            blue71 += 1

                        if p.state == 7 and new_state == 2:
                            blue72 += 1

                        if p.state == 8 and new_state == 3:
                            blue83 += 1

                        if p.state == 8 and new_state == 4:
                            blue84 += 1

                        if p.state == 8 and new_state == 5:
                            blue85 += 1

                        if p.state == 9 and new_state == 3:
                            blue93 += 1

                        if p.state == 9 and new_state == 4:
                            blue94 += 1

                        if p.state == 9 and new_state == 5:
                            blue95 += 1

                        if p.state == 10 and new_state == 3:
                            blue10_3 += 1

                        if p.state == 10 and new_state == 4:
                            blue10_4 += 1

                        if p.state == 10 and new_state == 5:
                            blue10_5 += 1

                        if p.state == 11 and new_state == 4:
                            blue11_4 += 1

                        if p.state == 11 and new_state == 5:
                            blue11_5 += 1
                
                p.state = new_state
                ## TODO: modify the transition table
            else: # ET
                pass ## TODO: ET

            ## TODO: update the new state in the point
            ## TODO: modify the transition table
            
            # excited state yb or tm state transition
            for p in self.lattice.excited:
                
                ET_rates = []
                pairs = []

                # p just like an index, self.lattice.neighbors is a dic from ret, we have found all ions' neighbors in advance
                # input the center ion p, we access the center ion's all nearby ions

                neighbors = self.lattice.neighbors[p] # 'neighbors' is a tuple: (neighbor, dist)
                
                for nei, distance in neighbors:
                    pair = p.react(nei, self.cross_relaxation, self.up_conversion, self.tag['c0'], distance)
                    if pair is not None:
                        ET_rates.append(pair)
                        pairs.append((nei, pair))
                        if emission: 

                            if p.state == 3 and new_state == 0:
                                NIR30 += 1

                            if p.state == 6 and new_state == 2:
                                NIR62 += 1

                            if p.state == 7 and new_state == 4:
                                NIR74 += 1

                            if p.state == 7 and new_state == 5:
                                NIR75 += 1

                            if p.state == 8 and new_state == 6:
                                NIR86 += 1

                            if p.state == 9 and new_state == 6:
                                NIR96 += 1

                            if p.state == 6 and new_state == 0:
                                blue60 += 1

                            if p.state == 7 and new_state == 1:
                                blue71 += 1

                            if p.state == 7 and new_state == 2:
                                blue72 += 1

                            if p.state == 8 and new_state == 3:
                                blue83 += 1

                            if p.state == 8 and new_state == 4:
                                blue84 += 1

                            if p.state == 8 and new_state == 5:
                                blue85 += 1

                            if p.state == 9 and new_state == 3:
                                blue93 += 1

                            if p.state == 9 and new_state == 4:
                                blue94 += 1

                            if p.state == 9 and new_state == 5:
                                blue95 += 1

                            if p.state == 10 and new_state == 3:
                                blue10_3 += 1

                            if p.state == 10 and new_state == 4:
                                blue10_4 += 1

                            if p.state == 10 and new_state == 5:
                                blue10_5 += 1

                            if p.state == 11 and new_state == 4:
                                blue11_4 += 1

                            if p.state == 11 and new_state == 5:
                                blue11_5 += 1

                    

                    if np.random.rand() < sum(p_decay_rates) / (sum(ET_rates) + sum(p_decay_rates)):
                        decayed = [i for i in range(p.state)]
                        decay_rates_sum = sum(p_decay_rates)
                        p_decay_rates = [i/decay_rates_sum for i in p_decay_rates]
                        new_state = np.random.choice(decayed, p=p_decay_rates)
                        tm_decay[(p.state, new_state)] = tm_decay.setdefault((p.state, new_state), 0) + 1

                        if emission: 

                            if p.state == 3 and new_state == 0:
                                NIR30 += 1

                            if p.state == 6 and new_state == 2:
                                NIR62 += 1

                            if p.state == 7 and new_state == 4:
                                NIR74 += 1

                            if p.state == 7 and new_state == 5:
                                NIR75 += 1

                            if p.state == 8 and new_state == 6:
                                NIR86 += 1

                            if p.state == 9 and new_state == 6:
                                NIR96 += 1

                            if p.state == 6 and new_state == 0:
                                blue60 += 1

                            if p.state == 7 and new_state == 1:
                                blue71 += 1

                            if p.state == 7 and new_state == 2:
                                blue72 += 1

                            if p.state == 8 and new_state == 3:
                                blue83 += 1

                            if p.state == 8 and new_state == 4:
                                blue84 += 1

                            if p.state == 8 and new_state == 5:
                                blue85 += 1

                            if p.state == 9 and new_state == 3:
                                blue93 += 1

                            if p.state == 9 and new_state == 4:
                                blue94 += 1

                            if p.state == 9 and new_state == 5:
                                blue95 += 1

                            if p.state == 10 and new_state == 3:
                                blue10_3 += 1

                            if p.state == 10 and new_state == 4:
                                blue10_4 += 1

                            if p.state == 10 and new_state == 5:
                                blue10_5 += 1

                            if p.state == 11 and new_state == 4:
                                blue11_4 += 1

                            if p.state == 11 and new_state == 5:
                                blue11_5 += 1
                        
                        pass

                    p.state = new_state

                # no stay, no decay, so ET process
                else:
                    prob_sum = sum(ET_rates)
                    ET_rates = [i/prob_sum for i in ET_rates]
                    nei, rate = random.choices(pairs, ET_rates)[0] # extracts the first item from the chosen pair: the first item of (nei, pair) is nei
                    if p.type == 'Yb' and nei.type == 'Yb':
                        p.state = 0
                        nei.state = 1
                        yb_yb += 1
                    elif p.type == 'Yb' and nei.type != 'Yb':
                        new_state = self.up_conversion[nei.state].select_path(distance)
                        yb_upconversion += 1
                        tm_upconversion[(nei.state, new_state[1])] = tm_upconversion.setdefault((nei.state, new_state[1]), 0) + 1
                        p.state = new_state[0]
                        nei.state = new_state[1]
                    else:
                        new_state = self.cross_relaxation[p.state][nei.state].select_path(distance)
                        tm_crossrelaxation[(p.state, new_state[0], nei.state, new_state[1])] = tm_crossrelaxation.setdefault((p.state, new_state[0], nei.state, new_state[1]), 0) + 1
                        p.state = new_state[0]
                        nei.state = new_state[1]
                
            # laser excites ground state yb to excited yb
            for p in self.lattice.ground_yb: 
                if np.random.rand() < self.dt*self.tag['laser']:
                    p.state = 1
                    yb_excite += 1

###########
            for p in [point for point in self.lattice.points if point.type == 'Tm' and point.state == 7]:
                if np.random.rand() < self.dt*self.tag['laser_tm']:
                    p.state = 11
                    tm_excite_7_11 += 1
###########

            
            # update new excited state Yb and Tm, and update new ground state Yb
            self.lattice.excited = [p for p in self.lattice.points if p.state != 0]
            self.lattice.ground_yb = [p for p in self.lattice.points if p.type == 'Yb' and p.state == 0]
            self.t += 1

            if emission:

                NIR30s.append(NIR30)
                NIR62s.append(NIR62)
                NIR74s.append(NIR74)
                NIR75s.append(NIR75)
                NIR86s.append(NIR86)
                NIR96s.append(NIR96)



                blue60s.append(blue60)
                blue71s.append(blue71)
                blue72s.append(blue72)

                blue83s.append(blue83)
                blue84s.append(blue84)
                blue85s.append(blue85)

                blue93s.append(blue93)
                blue94s.append(blue94)
                blue95s.append(blue95)

                blue10_3s.append(blue10_3)
                blue10_4s.append(blue10_4)
                blue10_5s.append(blue10_5)

                blue11_4s.append(blue11_4)
                blue11_5s.append(blue11_5)






                yb_upconversions.append(yb_upconversion)
                yb_ybs.append(yb_yb)
                yb_excites.append(yb_excite)

                tm_decays.append(tm_decay)
                tm_upconversions.append(tm_upconversion)
                tm_crossrelaxations.append(tm_crossrelaxation)

                tm_excite_7_11s.append(tm_excite_7_11)
        

        if emission:
 
            step_data = {}
            yb_state = [len([p for p in self.lattice.points if p.state == i and p.type == 'Yb']) for i in range(2)]
            step_data['yb_state'] = yb_state
            tm_state = [len([p for p in self.lattice.points if p.state == i and p.type == 'Tm']) for i in range(12)]
            step_data['tm_state'] = tm_state

            if steps == 1: 

                step_data['NIR'] = NIR30s[0], NIR62s[0], NIR74s[0], NIR75s[0], NIR86s[0], NIR96s[0]
                step_data['blue'] = blue60s[0], blue71s[0], blue72s[0], blue83s[0], blue84s[0], blue85s[0], blue93s[0], blue94s[0], blue95s[0], blue10_3s[0], blue10_4s[0], blue10_5s[0],blue11_4s[0], blue11_5s[0]


                step_data['yb_upconversions'] = yb_upconversions[0]
                step_data['yb_ybs'] = yb_ybs[0]
                step_data['yb_excites'] = yb_excites[0]


                step_data['tm_decays'] = tm_decays[0]
                step_data['tm_upconversions'] = tm_upconversions[0]
                step_data['tm_crossrelaxations'] = tm_crossrelaxations[0]
                step_data['tm_excite_7_11s'] = tm_excite_7_11s[0]

                return step_data
            
            # else: 

            #     step_data['red'] = red40s
            #     step_data['green'] = green50s, green60s
            #     step_data['yb_upconversions'] = yb_upconversions
            #     step_data['yb_yb'] = yb_ybs
            #     step_data['yb_excites'] = yb_excites
            #     step_data['er_decays'] = er_decays
            #     step_data['er_upconversions'] = er_upconversions
            #     step_data['er_crossrelaxations'] = er_crossrelaxations
            #     return step_data
    
    # def show_state(self):
    #     self.lattice.plot_3d_points_with_plotly()
    
    # def plot_distributions(self):
    #     self.lattice.plot_distributions()

    def simulate(self, t1, t2=None):

        ## At 2500 steps, reach steady state
   
        yb_state_evolution = {i:[] for i in range(0, 2)}
        tm_state_evolution = {i:[] for i in range(0, 12)}
        
        for _ in tqdm(range(t1)):
            r = self.step(emission=True)
            for i in range(2):
                yb_state_evolution[i].append(r['yb_state'][i])
            for i in range(12):
                tm_state_evolution[i].append(r['tm_state'][i])
        if t2 is None:
            return
        c = 0

        # yb_stats = []
        # er_stats = []

        NIRs = []
        NIR30s = []
        NIR62s = []
        NIR74s = []
        NIR75s = []
        NIR86s = []
        NIR96s = []


        blues = []

        blue60s = []
        blue71s = []
        blue72s = []

        blue83s = []
        blue84s = []
        blue85s = []

        blue93s = []
        blue94s = []
        blue95s = []

        blue10_3s = []
        blue10_4s = []
        blue10_5s = []

        blue11_4s = []
        blue11_5s = []




        yb_upconversions = []
        yb_ybs = []
        yb_excites = []
        tm_decays = [] # including MPR and MD
        tm_upconversions = []
        tm_crossrelaxations = []

        tm_excite_7_11s = []

        
        for _ in tqdm(range(t2-t1)):

            r = self.step(emission = True)

            NIRs.append(sum(r['NIR']))

            NIR30s.append(r['NIR'][0])
            NIR62s.append(r['NIR'][1])
            NIR74s.append(r['NIR'][2])
            NIR75s.append(r['NIR'][3])
            NIR86s.append(r['NIR'][4])
            NIR96s.append(r['NIR'][5])



            blues.append(sum(r['blue']))

            blue60s.append(r['blue'][0])
            blue71s.append(r['blue'][1])
            blue72s.append(r['blue'][2])
            blue83s.append(r['blue'][3])
            blue84s.append(r['blue'][4])
            blue85s.append(r['blue'][5])
            blue93s.append(r['blue'][6])
            blue94s.append(r['blue'][7])
            blue95s.append(r['blue'][8])
            blue10_3s.append(r['blue'][9])
            blue10_4s.append(r['blue'][10])
            blue10_5s.append(r['blue'][11])
            blue11_4s.append(r['blue'][12])
            blue11_5s.append(r['blue'][13])




            for i in range(2):
                yb_state_evolution[i].append(r['yb_state'][i])
            for i in range(12):
                tm_state_evolution[i].append(r['tm_state'][i])


            # c+=1
            # if c%100 == 0:
            #     yb_stat, er_stat = self.lattice.collect_stats()
            #     yb_stats.append(yb_stat)
            #     tm_stats.append(tm_stat)
            

            
            yb_upconversions.append(r['yb_upconversions'])
            yb_ybs.append(r['yb_ybs'])
            yb_excites.append(r['yb_excites'])
            tm_decays.append(r['tm_decays'])
            tm_upconversions.append(r['tm_upconversions'])
            tm_crossrelaxations.append(r['tm_crossrelaxations'])
            
            tm_excite_7_11s.append(r['tm_excite_7_11s'])
            
        # self.plot_stats(yb_stats, tm_stats)
        sim_stats = {}
        sim_stats['NIR_microsecond'] = NIRs
        sim_stats['blue_microsecond'] = blues

        sim_stats['NIR30s'] = NIR30s
        sim_stats['NIR62s'] = NIR62s
        sim_stats['NIR74s'] = NIR74s
        sim_stats['NIR75s'] = NIR75s
        sim_stats['NIR86s'] = NIR86s
        sim_stats['NIR96s'] = NIR96s




        sim_stats['blue60s'] = blue60s

        sim_stats['blue71s'] = blue71s
        sim_stats['blue72s'] = blue72s

        sim_stats['blue83s'] = blue83s
        sim_stats['blue84s'] = blue84s
        sim_stats['blue85s'] = blue85s

        sim_stats['blue93s'] = blue83s
        sim_stats['blue94s'] = blue94s
        sim_stats['blue95s'] = blue95s

        sim_stats['blue10_3s'] = blue10_3s
        sim_stats['blue10_4s'] = blue10_4s
        sim_stats['blue10_5s'] = blue10_5s

        sim_stats['blue11_4s'] = blue11_4s
        sim_stats['blue11_5s'] = blue11_5s
       
        
        sim_stats['NIR_avg'] = np.mean(NIRs)
        sim_stats['blue_avg'] = np.mean(blues)
        sim_stats['NIR_blue_ratio'] = np.mean(NIRs)/np.mean(blues)
        sim_stats['NIR_blue_total_avg'] = np.mean(NIRs)+np.mean(blues)

        sim_stats['NIR30_avg'] = np.mean(NIR30s)
        sim_stats['NIR62_avg'] = np.mean(NIR62s)
        sim_stats['NIR74_avg'] = np.mean(NIR74s)
        sim_stats['NIR75_avg'] = np.mean(NIR75s)
        sim_stats['NIR86_avg'] = np.mean(NIR86s)
        sim_stats['NIR96_avg'] = np.mean(NIR96s)


        sim_stats['blue60_avg'] = np.mean(blue60s)

        sim_stats['blue71_avg'] = np.mean(blue71s)
        sim_stats['blue72_avg'] = np.mean(blue72s)

        sim_stats['blue83_avg'] = np.mean(blue83s)
        sim_stats['blue84_avg'] = np.mean(blue84s)
        sim_stats['blue85_avg'] = np.mean(blue85s)

        sim_stats['blue93_avg'] = np.mean(blue93s)
        sim_stats['blue94_avg'] = np.mean(blue94s)
        sim_stats['blue95_avg'] = np.mean(blue95s)

        sim_stats['blue10_3_avg'] = np.mean(blue10_3s)
        sim_stats['blue10_4_avg'] = np.mean(blue10_4s)
        sim_stats['blue10_5_avg'] = np.mean(blue10_5s)

        sim_stats['blue11_4_avg'] = np.mean(blue11_4s)
        sim_stats['blue11_5_avg'] = np.mean(blue11_5s)


        sim_stats['yb_distribution'] = yb_state_evolution
        sim_stats['tm_distribution'] = tm_state_evolution

        # calculate red and green by population * rate
        
        sim_stats['NIR30_avg_pop'] = np.mean(tm_state_evolution[3][t1:]) * self.tag['E3E0']
        sim_stats['NIR62_avg_pop'] = np.mean(tm_state_evolution[6][t1:]) * self.tag['E6E2']
        sim_stats['NIR74_avg_pop'] = np.mean(tm_state_evolution[7][t1:]) * self.tag['E7E4']
        sim_stats['NIR75_avg_pop'] = np.mean(tm_state_evolution[7][t1:]) * self.tag['E7E5']
        sim_stats['NIR86_avg_pop'] = np.mean(tm_state_evolution[8][t1:]) * self.tag['E8E6']
        sim_stats['NIR96_avg_pop'] = np.mean(tm_state_evolution[9][t1:]) * self.tag['E9E6']
        sim_stats['NIR_avg_pop'] = sim_stats['NIR30_avg_pop'] + sim_stats['NIR62_avg_pop'] + sim_stats['NIR74_avg_pop'] + sim_stats['NIR75_avg_pop'] + sim_stats['NIR86_avg_pop'] + sim_stats['NIR96_avg_pop']

        sim_stats['blue60_avg_pop'] = np.mean(tm_state_evolution[6][t1:]) * self.tag['E6E0'] 
        sim_stats['blue71_avg_pop'] = np.mean(tm_state_evolution[7][t1:]) * self.tag['E7E1']
        sim_stats['blue72_avg_pop'] = np.mean(tm_state_evolution[7][t1:]) * self.tag['E7E2']

        sim_stats['blue83_avg_pop'] = np.mean(tm_state_evolution[8][t1:]) * self.tag['E8E3']
        sim_stats['blue84_avg_pop'] = np.mean(tm_state_evolution[8][t1:]) * self.tag['E8E4']
        sim_stats['blue85_avg_pop'] = np.mean(tm_state_evolution[8][t1:]) * self.tag['E8E5']

        sim_stats['blue93_avg_pop'] = np.mean(tm_state_evolution[9][t1:]) * self.tag['E9E3']
        sim_stats['blue94_avg_pop'] = np.mean(tm_state_evolution[9][t1:]) * self.tag['E9E4']
        sim_stats['blue95_avg_pop'] = np.mean(tm_state_evolution[9][t1:]) * self.tag['E9E5']

        sim_stats['blue10_3_avg_pop'] = np.mean(tm_state_evolution[10][t1:]) * self.tag['E10E3']
        sim_stats['blue10_4_avg_pop'] = np.mean(tm_state_evolution[10][t1:]) * self.tag['E10E4']
        sim_stats['blue10_5_avg_pop'] = np.mean(tm_state_evolution[10][t1:]) * self.tag['E10E5']

        sim_stats['blue11_4_avg_pop'] = np.mean(tm_state_evolution[11][t1:]) * self.tag['E11E4']
        sim_stats['blue11_5_avg_pop'] = np.mean(tm_state_evolution[11][t1:]) * self.tag['E11E5']
        
        sim_stats['blue_avg_pop'] = sim_stats['blue60_avg_pop'] + sim_stats['blue71_avg_pop'] + sim_stats['blue72_avg_pop'] + sim_stats['blue83_avg_pop'] + sim_stats['blue84_avg_pop'] + sim_stats['blue85_avg_pop'] + sim_stats['blue93_avg_pop'] + sim_stats['blue94_avg_pop'] + sim_stats['blue95_avg_pop'] + sim_stats['blue10_3_avg_pop']+ sim_stats['blue10_4_avg_pop'] + sim_stats['blue10_5_avg_pop'] + sim_stats['blue11_4_avg_pop'] + sim_stats['blue11_5_avg_pop']
        

        sim_stats['NIR_blue_ratio_pop'] = sim_stats['NIR_avg_pop'] / sim_stats['blue_avg_pop']
        sim_stats['NIR_blue_total_avg_pop'] = sim_stats['NIR_avg_pop'] + sim_stats['blue_avg_pop']
   
        sim_stats['yb_upconversions'] = yb_upconversions
        sim_stats['yb_ybs'] = yb_ybs
        sim_stats['yb_excites'] = yb_excites
        sim_stats['tm_decays'] = tm_decays
        sim_stats['tm_upconversions'] = tm_upconversions
        sim_stats['tm_crossrelaxations'] = tm_crossrelaxations

        sim_stats['tm_excite_7_11s'] = tm_excite_7_11s

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

        

