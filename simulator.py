import numpy as np
import random

from EnergyTransfer import *
from lattice import *
from point import *

from tqdm import tqdm

tag_default={'c0':9.836062e-40, # Yb-Yb resonant energy transfer
        'Ws':0,
        'W10':88.12753083306136,
        'W21':13.728308752002313,'W20':105.00663885847584,
        'W32':0.6904748414556272,'W31':40.06626483314129,'W30':107.07825106403719,
        'W43':1.4142534182563467,'W42':49.124834957391506,'W41':45.114305779338295,'W40':1009.6221517188111,
        'W54':0.5491077883920105,'W53':46.481404188403104,'W52':28.889483458690968,'W51':378.15231194559027,'W50':919.1044353717751,
        'W65':0.02617036285192619,'W64':8.841624545216064,'W63':47.60084543949401,'W62':41.09061870168263,'W61':71.35702052573745,'W60':2812.803587953125,
        'W76':0.4092613138830535,'W75':0.01904121955274265,'W74':3.4467583618029134,'W73':93.44157758618482,'W72':162.98778196545229,'W71':334.1120016219258,'W70':2256.2758284193,
        'laser': 1000}


class Simulator():

    def __init__(self, lattice, tag = None, dt = 10**(-6)):

        self.lattice = lattice.deep_copy()
        self.t = 0
        self.dt = dt

        if tag is not None:
            self.tag = tag
        else:
            self.tag = tag_default

        self.cross_relaxation = cross_relaxation()
        self.up_conversion = up_conversion()        

    def step(self, steps = 1, emission = False):

        if emission:
            nir40s = []
            green50s = []
            green60s = []
            yb_upconversions = []
            yb_ybs = []
            yb_excites = []
            er_decays = []
            er_upconversions = []
            er_crossrelaxations = []

        for _ in range(steps):

            if emission:
                nir40 = 0
                green50 = 0
                green60 = 0
                yb_upconversion = 0
                yb_yb = 0
                yb_excite = 0
                er_decay = {} # including MPR and MD
                er_upconversion = {}
                er_crossrelaxation = {}

            np.random.shuffle(self.lattice.excited)

            # excited state yb or tm state transition
            for p in self.lattice.excited:
                rates = []
                pair_rates = []
                neighbors = self.lattice.neighbors[p]
                
                for nei, distance in neighbors:
                    pair = p.react(nei, self.cross_relaxation, self.up_conversion, self.tag['c0'], distance)
                    if pair is not None:
                        rates.append(pair)
                        pair_rates.append((nei, pair))
                
                p_decay_rates = p.get_decay_rates(self.tag)
                # print(rates)
                no_reaction_prob = 1-self.dt*(sum(rates) + sum(p_decay_rates))

                # stay in current state
                if np.random.rand() < no_reaction_prob:
                    continue 

                # decay
                if np.random.rand() < sum(p_decay_rates) / (sum(rates) + sum(p_decay_rates)):
                    decayed = [i for i in range(p.state)]
                    decay_rates_sum = sum(p_decay_rates)
                    p_decay_rates = [i/decay_rates_sum for i in p_decay_rates]
                    new_state = np.random.choice(decayed, p=p_decay_rates)
                    er_decay[(p.state, new_state)] = er_decay.setdefault((p.state, new_state), 0) + 1
                    if emission: 
                        if p.state == 4 and new_state == 0:
                            nir40 += 1
                        if p.state == 5 and new_state == 0:
                            green50 += 1
                        if p.state == 6 and new_state == 0:
                            green60 += 1
                    p.state = new_state

                # etu
                else:
                    prob_sum = sum(rates)
                    rates = [i/prob_sum for i in rates]
                    nei, rate = random.choices(pair_rates, rates)[0]
                    if p.type == 'Yb' and nei.type == 'Yb':
                        p.state = 0
                        nei.state = 1
                        yb_yb += 1
                    elif p.type == 'Yb' and nei.type != 'Yb':
                        new_state = self.up_conversion[nei.state].select_path(distance)
                        yb_upconversion += 1
                        er_upconversion[(nei.state, new_state[1])] = er_upconversion.setdefault((nei.state, new_state[1]), 0) + 1
                        p.state = new_state[0]
                        nei.state = new_state[1]
                    else:
                        new_state = self.cross_relaxation[p.state][nei.state].select_path(distance)
                        er_crossrelaxation[(p.state, new_state[0], nei.state, new_state[1])] = er_crossrelaxation.setdefault((p.state, new_state[0], nei.state, new_state[1]), 0) + 1
                        p.state = new_state[0]
                        nei.state = new_state[1]
                
            # laser excites ground state yb to excited yb
            for p in self.lattice.ground_yb: 
                if np.random.rand() < self.dt*self.tag['laser']:
                    p.state = 1
                    yb_excite += 1
            
            # update new excited state Yb and Tm, and update new ground state Yb
            self.lattice.excited = [p for p in self.lattice.points if p.state != 0]
            self.lattice.ground_yb = [p for p in self.lattice.points if p.type == 'Yb' and p.state == 0]
            self.t += 1

            if emission:
                nir40s.append(nir40)
                green50s.append(green50)
                green60s.append(green60)
                yb_upconversions.append(yb_upconversion)
                yb_ybs.append(yb_yb)
                yb_excites.append(yb_excite)
                er_decays.append(er_decay)
                er_upconversions.append(er_upconversion)
                er_crossrelaxations.append(er_crossrelaxation)
        
        if emission:
            # print(nir40s, green50s, green60s)
            step_data = {}
            yb_state = [len([p for p in self.lattice.points if p.state == i and p.type == 'Yb']) for i in range(2)]
            step_data['yb_state'] = yb_state
            tm_state = [len([p for p in self.lattice.points if p.state == i and p.type == 'Er']) for i in range(8)]
            step_data['tm_state'] = tm_state

            if steps == 1: 

                step_data['nir'] = nir40s[0]
                step_data['green'] = green50s[0], green60s[0]
                step_data['yb_upconversions'] = yb_upconversions[0]
                step_data['yb_ybs'] = yb_ybs[0]
                step_data['yb_excites'] = yb_excites[0]
                step_data['er_decays'] = er_decays[0]
                step_data['er_upconversions'] = er_upconversions[0]
                step_data['er_crossrelaxations'] = er_crossrelaxations[0]
                return step_data
            
            # else: 

            #     step_data['nir'] = nir40s
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
        tm_state_evolution = {i:[] for i in range(0, 8)}
        
        for _ in tqdm(range(t1)):
            r = self.step(emission=True)
            for i in range(2):
                yb_state_evolution[i].append(r['yb_state'][i])
            for i in range(8):
                tm_state_evolution[i].append(r['tm_state'][i])
        if t2 is None:
            return
        c = 0
        yb_stats = []
        tm_stats = []
        nirs = []
        greens = []
        nir40s = []
        green50s = []
        green60s = []

        yb_upconversions = []
        yb_ybs = []
        yb_excites = []
        er_decays = [] # including MPR and MD
        er_upconversions = []
        er_crossrelaxations = []
        
        for _ in tqdm(range(t2-t1)):
            r = self.step(emission = True)
            nirs.append(r['nir'])
            # print(r['nir'], r['green'], greens)
            greens.append(sum(r['green']))
            nir40s.append(r['nir']) # [0]
            green50s.append(r['green'][0])
            green60s.append(r['green'][1])
            for i in range(2):
                yb_state_evolution[i].append(r['yb_state'][i])
            for i in range(8):
                tm_state_evolution[i].append(r['tm_state'][i])
            c+=1
            if c%100 == 0:
                yb_stat, tm_stat = self.lattice.collect_stats()
                yb_stats.append(yb_stat)
                tm_stats.append(tm_stat)
            
            
            yb_upconversions.append(r['yb_upconversions'])
            yb_ybs.append(r['yb_ybs'])
            yb_excites.append(r['yb_excites'])
            er_decays.append(r['er_decays'])
            er_upconversions.append(r['er_upconversions'])
            er_crossrelaxations.append(r['er_crossrelaxations'])
            
        # self.plot_stats(yb_stats, tm_stats)
        sim_stats = {}
        sim_stats['nir_microsecond'] = nirs
        sim_stats['blue_microsecond'] = greens
        sim_stats['nir40s'] = nir40s
        sim_stats['green50s'] = green50s
        sim_stats['green60s'] = green60s
        sim_stats['nir_avg'] = np.mean(nirs)
        sim_stats['green_avg'] = np.mean(greens)
        sim_stats['yb_distribution'] = yb_state_evolution
        sim_stats['tm_distribution'] = tm_state_evolution

        sim_stats['yb_upconversions'] = yb_upconversions
        sim_stats['yb_ybs'] = yb_ybs
        sim_stats['yb_excites'] = yb_excites
        sim_stats['er_decays'] = er_decays
        sim_stats['er_upconversions'] = er_upconversions
        sim_stats['er_crossrelaxations'] = er_crossrelaxations
        return sim_stats
    
    def plot_stats(self, yb_stats, tm_stats):

        plt.figure(figsize=(15, 5))

        # 1 row, 3 columns, 1st plot
        plt.subplot(1, 3, 1)

        bars = plt.bar(['Yb', 'Er', 'Y'], [self.lattice.yb_num, self.lattice.tm_num, self.lattice.n_points-self.lattice.yb_num-self.lattice.tm_num], color=['blue', 'pink', 'green'], width=0.4)
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
        tm_avg = []
        for i in range(len(tm_stats[0])):
            tm_avg.append(np.mean([j[i] for j in tm_stats]))
        plt.subplot(1, 3, 3)
        bars = plt.bar([0,1,2,3,4,5,6,7], tm_avg, color='pink', width=0.4)
        plt.ylabel('Count',fontsize=18)
        plt.title('Value distribution for emitters',fontsize=18)
        plt.xticks([0, 1, 2, 3, 4, 5, 6, 7], ['G', '1st', '2nd', '3rd', '4th', '5th', '6th', '7th'],fontsize=16)
        for i, bar in enumerate(bars):
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 5, round(tm_avg[i],1), ha='center', va='bottom')

        plt.tight_layout()
        plt.show()




        

