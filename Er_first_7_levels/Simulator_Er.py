import numpy as np
import random

from EnergyTransfer_Er import *
from Lattice_Er import *
from Point_Er import *

from tqdm import tqdm


# tag_default={'c0':9.836062e-40, # Yb-Yb resonant energy transfer
#         'Ws': 827,
#         'E1E0':88.12753083306136+39,
#         'E2E1':13.728308752002313+8.3+4077.51425913661,'E2E0':105.00663885847584,
#         'E3E2':0.6904748414556272+1.7+353536.78966928925,'E3E1':40.06626483314129,'E3E0':107.07825106403719,
#         'E4E3':1.4142534182563467+78491.28131241069,'E4E2':49.124834957391506,'E4E1':45.114305779338295,'E4E0':1009.6221517188111,
#         'E5E4':0.5491077883920105+20115.437448364588,'E5E3':46.481404188403104,'E5E2':28.889483458690968,'E5E1':378.15231194559027,'E5E0':919.1044353717751,
#         'E6E5':0.02617036285192619+73532852.08885323,'E6E4':8.841624545216064,'E6E3':47.60084543949401,'E6E2':41.09061870168263,'E6E1':71.35702052573745,'E6E0':2812.803587953125,
#         'E7E6':0.4092613138830535+15062862.442801291,'E7E5':0.01904121955274265,'E7E4':3.4467583618029134+17.9,'E7E3':93.44157758618482,'E7E2':162.98778196545229,'E7E1':334.1120016219258,'E7E0':2256.2758284193}


class Simulator():

    def __init__(self, lattice, tag=None, dt=10**(-6), excite_er=False):

        # get_nerighbors(self, r):
        #    self.neighbors = ret 
        # ret is a dic, key is all ion in self.n_points (3401, Yb+Er), values are many tuples: (nearby ion, distance< 1 nm) 


        self.lattice = lattice.deep_copy()
        self.t = 0
        self.dt = dt
        self.tag = tag if tag is not None else tag_default
        self.cross_relaxation = cross_relaxation()
        self.up_conversion = up_conversion()
        self.back_transfer = back_transfer()
        self.excite_er = excite_er

    def step(self, steps=1, emission=False):
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
            er_backtransfers = []

            # consider the Er excitation from laser: E0 to E2, E2 to E7
            er_excite_02s = []
            er_excite_27s = []

        for _ in range(steps):
            if emission:
                red40 = 0
                green50 = 0
                green60 = 0
                yb_upconversion = 0
                er_backtransfer = 0
                yb_yb = 0
                yb_excite = 0

                er_excite_02 = 0
                er_excite_27 = 0

                
                er_decay = {} # including MPR and MD
                er_upconversion = {}
                er_crossrelaxation = {}
                er_backtransfer = {}

            np.random.shuffle(self.lattice.excited)

            for p in self.lattice.excited:

                ET_rates = []
                pairs = []

                # p just like an index, self.lattice.neighbors is a dic from ret, we have found all ions' neighbors in advance
                # input the center ion p, we access the center ion's all nearby ions

                # find unchanged probability: no any changes with any neighbors

                neighbors = self.lattice.neighbors[p] # 'neighbors' is a tuple: (neighbor, dist) nei+distance

                for nei, distance in neighbors:
                    pair = p.react(nei, self.cross_relaxation, self.up_conversion, self.back_transfer, self.tag['c0'], distance)
                    if pair is not None:
                        ET_rates.append(pair)
                        pairs.append((nei, pair))


                p_decay_rates = p.get_decay_rates(self.tag)
                no_reaction_prob = 1 - self.dt * (sum(ET_rates) + sum(p_decay_rates))

                # stay in current state v.s. change
                # if np.random.rand() < no_reaction_prob:
                #     continue # skip the current iteration and continue with the next one

                r1 = np.random.uniform(0,1)

                if r1 < no_reaction_prob:
                    continue # skip the current iteration and continue with the next one

                r2 = np.random.uniform(0,1)

                # decay v.s. ET process, # if decay, then decide which pathway to go

                if r2 < sum(p_decay_rates) / (sum(ET_rates) + sum(p_decay_rates)):
                    decayed = [i for i in range(p.state)]
                    p_decay_rates = [rate / sum(p_decay_rates) for rate in p_decay_rates]
                    new_state = np.random.choice(decayed, p=p_decay_rates) #######################################
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
                    ET_rates = [rate / sum(ET_rates) for rate in ET_rates]

                    # firstly, select which neighbor to interact
                    # extracts the first item from the chosen pair: the first item of (nei, pair) is nei, while nei from self.lattice.neighbors is a tuple: (self.points[j], dist)
                    nei, dist = random.choices(pairs, ET_rates)[0]  #######################################

                    if p.type == 'Yb' and nei.type == 'Yb':
                        if nei.state == 0:
                            p.state = 0
                            nei.state = 1
                            yb_yb += 1

                   # if the neighbor is Er, then decide which pathway to go with the neighbor Er, 
                   # we don't care the nei.state, since we have found all possible pathways of all Er states in upconversion function
                   # we only use the nei.state as an index, to find the pre-calculated choice, given the distance

                    elif p.type == 'Yb' and nei.type != 'Yb':
                        new_state = self.up_conversion[nei.state].select_path(distance)
                        p.state = new_state[0]
                        nei.state = new_state[1]
                        yb_upconversion += 1
                        er_upconversion[(nei.state, new_state[1])] = er_upconversion.setdefault((nei.state, new_state[1]), 0) + 1

                    elif p.type != 'Yb' and nei.type == 'Yb':
                        new_state = self.back_transfer[p.state].select_path(distance)
                        
                        nei.state = new_state[0]
                        p.state = new_state[1]

                        er_backtransfer[(p.state, new_state[0])] = er_backtransfer.setdefault((p.state, new_state[0]), 0) + 1
                        er_backtransfer +=1

                    else:
                        new_state = self.cross_relaxation[p.state][nei.state].select_path(distance)
                        er_crossrelaxation[(p.state, new_state[0], nei.state, new_state[1])] = er_crossrelaxation.setdefault((p.state, new_state[0], nei.state, new_state[1]), 0) + 1
                            
                        p.state = new_state[0]
                        nei.state = new_state[1]
                        
                       
            for p in self.lattice.ground_yb:
                if np.random.rand() < self.dt * self.tag['laser']:
                    p.state = 1
                    yb_excite += 1

            for p in [point for point in self.lattice.points if point.type == 'Er' and point.state == 2]:
                if np.random.rand() < self.dt * self.tag['laser_er']:
                    p.state = 7
                    er_excite_27 += 1
            for p in [point for point in self.lattice.points if point.type == 'Er' and point.state == 0]:
                if np.random.rand() < self.dt * self.tag['laser_er']:
                    p.state = 2
                    er_excite_02 += 1

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
                er_backtransfers.append(er_backtransfer)
                er_excite_27s.append(er_excite_27)
                er_excite_02s.append(er_excite_02)

        if emission:
            step_data = {}
            yb_state = [len([p for p in self.lattice.points if p.state == i and p.type == 'Yb']) for i in range(2)]
            step_data['yb_state'] = yb_state
            er_state = [len([p for p in self.lattice.points if p.state == i and p.type == 'Er']) for i in range(8)]
            step_data['er_state'] = er_state

            if steps == 1:
                step_data['red'] = red40s[0]
                step_data['green'] = (green50s[0], green60s[0])
                step_data['yb_upconversions'] = yb_upconversions[0]
                step_data['yb_ybs'] = yb_ybs[0]
                step_data['yb_excites'] = yb_excites[0]
                step_data['er_decays'] = er_decays[0]
                step_data['er_upconversions'] = er_upconversions[0]
                step_data['er_crossrelaxations'] = er_crossrelaxations[0]
                step_data['er_backtransfers'] = er_backtransfers[0]
                step_data['er_excite_02s'] = er_excite_02s[0]
                step_data['er_excite_27s'] = er_excite_27s[0]

                return step_data


    def simulate(self, t1, t2=None):
        """
        Simulate the energy transfer processes in the system over a period of time.

        Parameters:
        t1 (int): The number of steps to simulate for reaching steady state.
        t2 (int, optional): The total number of steps to simulate, including after reaching steady state.

        Returns:
        dict: A dictionary containing the simulation statistics.
        """

        ## At 2500 steps, reach steady state

        yb_state_evolution = {i: [] for i in range(0, 2)}
        er_state_evolution = {i: [] for i in range(0, 8)}

        for _ in tqdm(range(t1)):
            r = self.step(emission=True)
            for i in range(2):
                yb_state_evolution[i].append(r['yb_state'][i])
            for i in range(8):
                er_state_evolution[i].append(r['er_state'][i])

        if t2 is None:
            return {
                'yb_distribution': yb_state_evolution,
                'er_distribution': er_state_evolution
            }

        reds, greens, red40s, green50s, green60s = [], [], [], [], []
        yb_upconversions, yb_ybs, yb_excites = [], [], []
        er_decays, er_upconversions, er_crossrelaxations, er_backtransfers = [], [], [], []
        er_excite_02s, er_excite_27s = [], []

        for _ in tqdm(range(t2 - t1)):
            
            r = self.step(emission=True)

            reds.append(r['red'])
            greens.append(sum(r['green']))
            red40s.append(r['red'])
            green50s.append(r['green'][0])
            green60s.append(r['green'][1])

            for i in range(2):
                yb_state_evolution[i].append(r['yb_state'][i])
            for i in range(8):
                er_state_evolution[i].append(r['er_state'][i])

            yb_upconversions.append(r['yb_upconversions'])
            yb_ybs.append(r['yb_ybs'])
            yb_excites.append(r['yb_excites'])
            er_decays.append(r['er_decays'])
            er_upconversions.append(r['er_upconversions'])
            er_crossrelaxations.append(r['er_crossrelaxations'])
            er_backtransfers.append(r['er_backtransfers'])
            er_excite_02s.append(r['er_excite_02s'])
            er_excite_27s.append(r['er_excite_27s'])

        sim_stats = {
            'red_microsecond': reds,
            'green_microsecond': greens,
            'red40s': red40s,
            'green50s': green50s,
            'green60s': green60s,
            'red_avg': np.mean(reds)*10**6,
            'green_avg': np.mean(greens)*10**6,
            'green50_avg': np.mean(green50s)*10**6,
            'green60_avg': np.mean(green60s)*10**6,

            'green_red_ratio': (np.mean(greens)*10**6)/(np.mean(reds)*10**6),
            'red_green_total_avg': np.mean(reds)*10**6 + np.mean(greens)*10**6,

            'yb_distribution': yb_state_evolution,
            'er_distribution': er_state_evolution,
            
            'red_avg_pop': np.mean(er_state_evolution[4][t1:]) * self.tag['E4E0'],
            'green_avg_pop': (np.mean(er_state_evolution[6][t1:]) * self.tag['E6E0']
                            + np.mean(er_state_evolution[5][t1:]) * self.tag['E5E0']),
            'green50_avg_pop': np.mean(er_state_evolution[5][t1:]) * self.tag['E5E0'],
            'green60_avg_pop': np.mean(er_state_evolution[6][t1:]) * self.tag['E6E0'],
            'red_green_ratio_pop': (np.mean(er_state_evolution[4][t1:]) * self.tag['E4E0']
                                    / (np.mean(er_state_evolution[6][t1:]) * self.tag['E6E0']
                                    + np.mean(er_state_evolution[5][t1:]) * self.tag['E5E0'])),
            'red_green_total_avg_pop': (np.mean(er_state_evolution[4][t1:]) * self.tag['E4E0']
                                        + np.mean(er_state_evolution[6][t1:]) * self.tag['E6E0']
                                        + np.mean(er_state_evolution[5][t1:]) * self.tag['E5E0']),
            'yb_upconversions': yb_upconversions,
            'yb_ybs': yb_ybs,
            'yb_excites': yb_excites,
            'er_decays': er_decays,
            'er_upconversions': er_upconversions,
            'er_crossrelaxations': er_crossrelaxations,
            'er_backtransfers': er_backtransfers,
            'er_excite_02s': er_excite_02s,
            'er_excite_27s': er_excite_27s
        }

        return sim_stats