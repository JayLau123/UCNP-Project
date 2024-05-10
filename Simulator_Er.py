import numpy as np
import random

from EnergyTransfer_Er import *
from Lattice_Er import *
from Point_Er import *

from tqdm import tqdm


tag_default={'c0':9.836062e-40, # Yb-Yb resonant energy transfer
        'Ws': 827,
        'E1E0':88.12753083306136+39,
        'E2E1':13.728308752002313+8.3+4077.51425913661,'E2E0':105.00663885847584,
        'E3E2':0.6904748414556272+1.7+353536.78966928925,'E3E1':40.06626483314129,'E3E0':107.07825106403719,
        'E4E3':1.4142534182563467+78491.28131241069,'E4E2':49.124834957391506,'E4E1':45.114305779338295,'E4E0':1009.6221517188111,
        'E5E4':0.5491077883920105+20115.437448364588,'E5E3':46.481404188403104,'E5E2':28.889483458690968,'E5E1':378.15231194559027,'E5E0':919.1044353717751,
        'E6E5':0.02617036285192619+73532852.08885323,'E6E4':8.841624545216064,'E6E3':47.60084543949401,'E6E2':41.09061870168263,'E6E1':71.35702052573745,'E6E0':2812.803587953125,
        'E7E6':0.4092613138830535+15062862.442801291,'E7E5':0.01904121955274265,'E7E4':3.4467583618029134+17.9,'E7E3':93.44157758618482,'E7E2':162.98778196545229,'E7E1':334.1120016219258,'E7E0':2256.2758284193}

class Simulator():

    def __init__(self, lattice, tag = None, dt = 10**(-6)):

        # get_nerighbors(self, r):
        #    self.neighbors = ret 
        # ret is a dic, key is all ion in self.n_points (3401, Yb+Er), values are many tuples: (nearby ion, distance< 1 nm) 

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
            red40s = []
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
                red40 = 0
                green50 = 0
                green60 = 0
                yb_upconversion = 0
                yb_yb = 0
                yb_excite = 0
                er_decay = {} # including MPR and MD
                er_upconversion = {}
                er_crossrelaxation = {}

            np.random.shuffle(self.lattice.excited)

            # excited state yb or er state transition
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
                
                p_decay_rates = p.get_decay_rates(self.tag)
                
                no_reaction_prob = 1-self.dt*(sum(ET_rates) + sum(p_decay_rates))

                # stay in current state v.s. change
                if np.random.rand() < no_reaction_prob:
                    continue # skip the current iteration and continue with the next one

                
                # decay v.s. ET process
                # if decay, then decide which pathway to go

                if np.random.rand() < sum(p_decay_rates) / (sum(ET_rates) + sum(p_decay_rates)):
                    decayed = [i for i in range(p.state)]
                    decay_rates_sum = sum(p_decay_rates)
                    p_decay_rates = [i/decay_rates_sum for i in p_decay_rates]
                    new_state = np.random.choice(decayed, p=p_decay_rates)
                    er_decay[(p.state, new_state)] = er_decay.setdefault((p.state, new_state), 0) + 1
                    if emission: 
                        if p.state == 4 and new_state == 0:
                            red40 += 1
                        if p.state == 5 and new_state == 0:
                            green50 += 1
                        if p.state == 6 and new_state == 0:
                            green60 += 1
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
            
            # update new excited state Yb and Er, and update new ground state Yb
            self.lattice.excited = [p for p in self.lattice.points if p.state != 0]
            self.lattice.ground_yb = [p for p in self.lattice.points if p.type == 'Yb' and p.state == 0]
            self.t += 1

            if emission:
                red40s.append(red40)
                green50s.append(green50)
                green60s.append(green60)
                yb_upconversions.append(yb_upconversion)
                yb_ybs.append(yb_yb)
                yb_excites.append(yb_excite)
                er_decays.append(er_decay)
                er_upconversions.append(er_upconversion)
                er_crossrelaxations.append(er_crossrelaxation)
        
        if emission:
 
            step_data = {}
            yb_state = [len([p for p in self.lattice.points if p.state == i and p.type == 'Yb']) for i in range(2)]
            step_data['yb_state'] = yb_state
            er_state = [len([p for p in self.lattice.points if p.state == i and p.type == 'Er']) for i in range(8)]
            step_data['er_state'] = er_state

            if steps == 1: 

                step_data['red'] = red40s[0]
                step_data['green'] = green50s[0], green60s[0]
                step_data['yb_upconversions'] = yb_upconversions[0]
                step_data['yb_ybs'] = yb_ybs[0]
                step_data['yb_excites'] = yb_excites[0]
                step_data['er_decays'] = er_decays[0]
                step_data['er_upconversions'] = er_upconversions[0]
                step_data['er_crossrelaxations'] = er_crossrelaxations[0]
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
        er_state_evolution = {i:[] for i in range(0, 8)}
        
        for _ in tqdm(range(t1)):
            r = self.step(emission=True)
            for i in range(2):
                yb_state_evolution[i].append(r['yb_state'][i])
            for i in range(8):
                er_state_evolution[i].append(r['er_state'][i])
        if t2 is None:
            return
        c = 0

        # yb_stats = []
        # er_stats = []

        reds = []
        greens = []
        red40s = []
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

            reds.append(r['red'])

            greens.append(sum(r['green']))
            red40s.append(r['red'])
            green50s.append(r['green'][0])
            green60s.append(r['green'][1])
            for i in range(2):
                yb_state_evolution[i].append(r['yb_state'][i])
            for i in range(8):
                er_state_evolution[i].append(r['er_state'][i])


            # c+=1
            # if c%100 == 0:
            #     yb_stat, er_stat = self.lattice.collect_stats()
            #     yb_stats.append(yb_stat)
            #     er_stats.append(er_stat)
            

            
            yb_upconversions.append(r['yb_upconversions'])
            yb_ybs.append(r['yb_ybs'])
            yb_excites.append(r['yb_excites'])
            er_decays.append(r['er_decays'])
            er_upconversions.append(r['er_upconversions'])
            er_crossrelaxations.append(r['er_crossrelaxations'])
            
        # self.plot_stats(yb_stats, er_stats)
        sim_stats = {}
        sim_stats['red_microsecond'] = reds
        sim_stats['green_microsecond'] = greens

        sim_stats['red40s'] = red40s
        sim_stats['green50s'] = green50s
        sim_stats['green60s'] = green60s
        
        sim_stats['red_avg'] = np.mean(reds)
        sim_stats['green_avg'] = np.mean(greens)
        sim_stats['red_green_ratio'] = np.mean(reds)/np.mean(greens)
        sim_stats['red_green_total_avg'] = np.mean(reds)+np.mean(greens)
        sim_stats['green50_avg'] = np.mean(green50s)
        sim_stats['green60_avg'] = np.mean(green60s)


        sim_stats['yb_distribution'] = yb_state_evolution
        sim_stats['er_distribution'] = er_state_evolution

        # calculate red and green by population * rate
        sim_stats['red_avg_pop'] = np.mean(er_state_evolution[4][t1:]) * self.tag['E4E0']
        sim_stats['green_avg_pop'] = np.mean(er_state_evolution[6][t1:]) * self.tag['E6E0'] + np.mean(er_state_evolution[5][t1:]) * self.tag['E5E0'] 

        sim_stats['red_green_ratio_pop'] = sim_stats['red_avg_pop'] / sim_stats['green_avg_pop']

        sim_stats['red_green_total_avg_pop'] = np.mean(er_state_evolution[4][t1:]) * self.tag['E4E0'] + np.mean(er_state_evolution[6][t1:]) * self.tag['E6E0'] + np.mean(er_state_evolution[5][t1:]) * self.tag['E5E0'] 
        sim_stats['green50_avg_pop'] = np.mean(er_state_evolution[5][t1:]) * self.tag['E5E0']
        sim_stats['green60_avg_pop'] = np.mean(er_state_evolution[6][t1:]) * self.tag['E6E0']



        sim_stats['yb_upconversions'] = yb_upconversions
        sim_stats['yb_ybs'] = yb_ybs
        sim_stats['yb_excites'] = yb_excites
        sim_stats['er_decays'] = er_decays
        sim_stats['er_upconversions'] = er_upconversions
        sim_stats['er_crossrelaxations'] = er_crossrelaxations

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

        

