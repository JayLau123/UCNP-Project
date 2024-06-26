import numpy as np
import random
from tqdm import tqdm

from EnergyTransfer_Er import *
from Lattice_Er import *
from Point_Er import *

from Er_inf import *
from Er_Energy import *
from Er_EnergyLevelDiagram import *
from Er_RateCalculation import *


# us as time step

class Simulator():

    def __init__(self, lattice, find_Er_ED_transition, tag = None, dt = 10**(-6), excite_er = False):

        # get_nerighbors(self, r):
        #    self.neighbors = ret 
        # ret is a dic, key is all ion in self.n_points (3401, Yb+Er), values are many tuples: (nearby ion, distance< 1 nm) 

        self.lattice = lattice.deep_copy()
        self.t = 0
        self.dt = dt
        self.selected_Er_ED_transition = find_Er_ED_transition

        if tag is not None:
            self.tag = tag
        else:
            self.tag = tag_default

        self.cross_relaxation = cross_relaxation()
        self.up_conversion = up_conversion()        
        self.excite_er = excite_er


    def step(self, steps = 1, emission = False):

        if emission:


            whole_lists1 = []

            for key1, value in self.selected_Er_ED_transition.items():
                for key2 in value.keys():
                    name1 = key2[key2.find('E')+1 : key2.find('(')]
                    key2_new = key2[key2.find('(')+1:]
                    name2 = key2_new[key2_new.find(')')+2 : key2_new.find('(')]
                    list_name=f'{key1}_{name1}_{name2}s'

                    whole_dic = {}
                    whole_dic[list_name] = []
                    whole_lists1.append(whole_dic)

                    # [{'green_30_14s': []},
                    #  {'green_26_8s': []},
                    #  {'green_23_6s': []},
                    #  {'green_11_1s': []},
                    #  {'green_29_12s': []},
                    #  {'green_35_28s': []}]

            # red40s = []
            # red71s = []
            # red81s = []
            # red91s = []
            # red10_2s = []
            # red11_2s = []
            # red11_3s = []
            # red12_3s = []
            # red13_3s = []
            # red14_3s = []
            # red15_4s = []
            # green50s = []
            # green60s = []
            # green10_1s = []
            # green11_1s = []
            # green12_2s = []
            # green13_2s = []
            # green14_2s = []
            # green15_3s = []



            yb_upconversions = []
            yb_ybs = []
            yb_excites = []
            er_decays = []
            er_upconversions = []
            er_crossrelaxations = []

            er_excite_0_2s = []
            er_excite_2_7s = []
            er_excite_9_16s = []
            er_excite_10_20s = []
            er_excite_15_25s = []
            er_excite_17_28s = []
            er_excite_18_28s = []
            er_excite_33_36s = []
            er_excite_34_36s = []



        for _ in range(steps):

            if emission:
                

                whole_lists2 = []

                for key1, value in self.selected_Er_ED_transition.items():
                    for key2 in value.keys():
                        name1 = key2[key2.find('E')+1 : key2.find('(')]
                        key2_new = key2[key2.find('(')+1:]
                        name2 = key2_new[key2_new.find(')')+2 : key2_new.find('(')]
                        list_name=f'{key1}_{name1}_{name2}'

                        whole_dic = {}
                        whole_dic[list_name] = 0
                        whole_lists2.append(whole_dic)

                        # [{'green_30_14': 0},
                        #  {'green_26_8': 0},
                        #  {'green_23_6': 0},
                        #  {'green_11_1': 0},
                        #  ...]


                # red40 = 0
                # red71 = 0
                # red81 = 0
                # red91 = 0
                # red10_2 = 0
                # red11_2 = 0
                # red11_3 = 0
                # red12_3 = 0
                # red13_3 = 0
                # red14_3 = 0
                # red15_4 = 0
                # green50 = 0
                # green60 = 0
                # green10_1 = 0
                # green11_1 = 0
                # green12_2 = 0
                # green13_2 = 0
                # green14_2 = 0
                # green15_3 = 0


                yb_upconversion = 0
                yb_yb = 0
                yb_excite = 0


                er_excite_0_2 = 0
                er_excite_2_7 = 0
                er_excite_9_16 = 0
                er_excite_10_20 = 0
                er_excite_15_25 = 0
                er_excite_17_28 = 0
                er_excite_18_28 = 0
                er_excite_33_36 = 0
                er_excite_34_36 = 0


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

                        for i in whole_lists2:
                            for key, value in i.items():
                                number_start = int(key.split('_')[1])
                                number_end = int(key.split('_')[2])

                                if p.state == number_start and new_state == number_end:

                                    value +=1
                            

                        # if p.state == 4 and new_state == 0:
                        #     red40 += 1
                        # if p.state == 7 and new_state == 1:
                        #     red71 += 1
                        # if p.state == 8 and new_state == 1:
                        #     red81 += 1
                        # if p.state == 9 and new_state == 1:
                        #     red91 += 1
                        # if p.state == 10 and new_state == 2:
                        #     red10_2 += 1
                        # if p.state == 11 and new_state == 2:
                        #     red11_2 += 1
                        # if p.state == 11 and new_state == 3:
                        #     red11_3 += 1
                        # if p.state == 12 and new_state == 3:
                        #     red12_3 += 1
                        # if p.state == 13 and new_state == 3:
                        #     red13_3 += 1
                        # if p.state == 14 and new_state == 3:
                        #     red14_3 += 1
                        # if p.state == 15 and new_state == 4:
                        #     red15_4 += 1
                        # if p.state == 5 and new_state == 0:
                        #     green50 += 1
                        # if p.state == 6 and new_state == 0:
                        #     green60 += 1
                        # if p.state == 10 and new_state == 1:
                        #     green10_1 += 1
                        # if p.state == 11 and new_state == 1:
                        #     green11_1 += 1
                        # if p.state == 12 and new_state == 2:
                        #     green12_2 += 1
                        # if p.state == 13 and new_state == 2:
                        #     green13_2 += 1
                        # if p.state == 14 and new_state == 2:
                        #     green14_2 += 1
                        # if p.state == 15 and new_state == 3:
                        #     green15_3 += 1


                    p.state = new_state

                ######################## # no stay, no decay, so ET process

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
            
            

            for p in [point for point in self.lattice.points if point.type == 'Er' and point.state == 0]:
                if np.random.rand() < self.dt*self.tag['laser_er']:
                    p.state = 2
                    er_excite_0_2 += 1

            for p in [point for point in self.lattice.points if point.type == 'Er' and point.state == 2]:
                if np.random.rand() < self.dt*self.tag['laser_er']:
                    p.state = 7
                    er_excite_2_7 += 1

            for p in [point for point in self.lattice.points if point.type == 'Er' and point.state == 9]:
                if np.random.rand() < self.dt*self.tag['laser_er']:
                    p.state = 16
                    er_excite_9_16 += 1

            for p in [point for point in self.lattice.points if point.type == 'Er' and point.state == 10]:
                if np.random.rand() < self.dt*self.tag['laser_er']:
                    p.state = 20
                    er_excite_10_20 += 1

            for p in [point for point in self.lattice.points if point.type == 'Er' and point.state == 15]:
                if np.random.rand() < self.dt*self.tag['laser_er']:
                    p.state = 25
                    er_excite_15_25 += 1

            for p in [point for point in self.lattice.points if point.type == 'Er' and point.state == 17]:
                if np.random.rand() < self.dt*self.tag['laser_er']:
                    p.state = 28
                    er_excite_17_28 += 1

            for p in [point for point in self.lattice.points if point.type == 'Er' and point.state == 18]:
                if np.random.rand() < self.dt*self.tag['laser_er']:
                    p.state = 28
                    er_excite_18_28 += 1

            for p in [point for point in self.lattice.points if point.type == 'Er' and point.state == 33]:
                if np.random.rand() < self.dt*self.tag['laser_er']:
                    p.state = 36
                    er_excite_33_36 += 1

            for p in [point for point in self.lattice.points if point.type == 'Er' and point.state == 34]:
                if np.random.rand() < self.dt*self.tag['laser_er']:
                    p.state = 36
                    er_excite_34_36 += 1


            
            # update new excited state Yb and Er, and update new ground state Yb
            self.lattice.excited = [p for p in self.lattice.points if p.state != 0]
            self.lattice.ground_yb = [p for p in self.lattice.points if p.type == 'Yb' and p.state == 0]
            self.t += 1

            if emission:


                for i, j in zip(whole_lists1, whole_lists2):
                    for key, value in j.items():
                        i[f'{key}s'].append(value)


                # red40s.append(red40)
                # red71s.append(red71)
                # red81s.append(red81)
                # red91s.append(red91)
                # red10_2s.append(red10_2)
                # red11_2s.append(red11_2)
                # red11_3s.append(red11_3)
                # red12_3s.append(red12_3)
                # red13_3s.append(red13_3)
                # red14_3s.append(red14_3)
                # red15_4s.append(red15_4)
                # green50s.append(green50)
                # green60s.append(green60)
                # green10_1s.append(green10_1)
                # green11_1s.append(green11_1)
                # green12_2s.append(green12_2)
                # green13_2s.append(green13_2)
                # green14_2s.append(green14_2)
                # green15_3s.append(green15_3)

    


                yb_upconversions.append(yb_upconversion)
                yb_ybs.append(yb_yb)
                yb_excites.append(yb_excite)
                er_decays.append(er_decay)
                er_upconversions.append(er_upconversion)
                er_crossrelaxations.append(er_crossrelaxation)


                er_excite_0_2s.append(er_excite_0_2)
                er_excite_2_7s.append(er_excite_2_7)
                er_excite_9_16s.append(er_excite_9_16)
                er_excite_10_20s.append(er_excite_10_20)
                er_excite_15_25s.append(er_excite_15_25)
                er_excite_17_28s.append(er_excite_17_28)
                er_excite_18_28s.append(er_excite_18_28)
                er_excite_33_36s.append(er_excite_33_36)
                er_excite_34_36s.append(er_excite_34_36)



        
        if emission:


            step_data = {}
            yb_state = [len([p for p in self.lattice.points if p.state == i and p.type == 'Yb']) for i in range(2)]
            step_data['yb_state'] = yb_state
            er_state = [len([p for p in self.lattice.points if p.state == i and p.type == 'Er']) for i in range(38)]
            step_data['er_state'] = er_state

            if steps == 1: 

               

                step_data_emission = {}
                # Loop through each dictionary in the list
                for i in whole_lists1:
                    for key, value in i.items():
                        color_name = key.split('_')[0]

                        if color_name not in step_data_emission:
                            step_data_emission[color_name] = []

                        step_data_emission[color_name].append(value[0])
                        # {'green': [0, 1, 2, 3], 'red': [4, 5, 6, 7]}

                # step_data['red'] = red40s[0], red71s[0], red81s[0], red91s[0], red10_2s[0], red11_2s[0], red11_3s[0], red12_3s[0], red13_3s[0], red14_3s[0], red15_4s[0] 
                # step_data['green'] = green50s[0], green60s[0], green10_1s[0], green11_1s[0], green12_2s[0], green13_2s[0], green14_2s[0], green15_3s[0]

        

                for i in whole_lists1:
                    for key, value in i.items():
                        step_data[key]=value[0]


                

                step_data['yb_upconversions'] = yb_upconversions[0]
                step_data['yb_ybs'] = yb_ybs[0]
                step_data['yb_excites'] = yb_excites[0]
                step_data['er_decays'] = er_decays[0]
                step_data['er_upconversions'] = er_upconversions[0]
                step_data['er_crossrelaxations'] = er_crossrelaxations[0]

                step_data['er_excite_0_2s'] = er_excite_0_2s[0]
                step_data['er_excite_2_7s'] = er_excite_2_7s[0]
                step_data['er_excite_9_16s'] = er_excite_9_16s[0]
                step_data['er_excite_10_20s'] = er_excite_10_20s[0]
                step_data['er_excite_15_25s'] = er_excite_15_25s[0]
                step_data['er_excite_17_28s'] = er_excite_17_28s[0]
                step_data['er_excite_18_28s'] = er_excite_18_28s[0]
                step_data['er_excite_33_36s'] = er_excite_33_36s[0]
                step_data['er_excite_34_36s'] = er_excite_34_36s[0]





                return step_data, step_data_emission
            
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

        ## after t1 steps, reach steady state
   
        yb_state_evolution = {i:[] for i in range(0, 2)}
        er_state_evolution = {i:[] for i in range(0, 38)}
        
        for _ in tqdm(range(t1)):

            r, r_emission = self.step(emission=True)

            for i in range(2):
                yb_state_evolution[i].append(r['yb_state'][i])
            for i in range(38):
                er_state_evolution[i].append(r['er_state'][i])

        if t2 is None:
            return

        # yb_stats = []
        # er_stats = []

        whole_lists1 = []

        for key1, value in self.selected_Er_ED_transition.items():
            for key2 in value.keys():
                name1 = key2[key2.find('E')+1 : key2.find('(')]
                key2_new = key2[key2.find('(')+1:]
                name2 = key2_new[key2_new.find(')')+2 : key2_new.find('(')]
                list_name=f'{key1}_{name1}_{name2}s'

                whole_dic = {}
                whole_dic[list_name] = []
                whole_lists1.append(whole_dic)

        # red40s = []
        # red71s = []
        # red81s = []
        # red91s = []
        # red10_2s = []
        # red11_2s = []
        # red11_3s = []
        # red12_3s = []
        # red13_3s = []
        # red14_3s = []
        # red15_4s = []
        # green50s = []
        # green60s = []
        # green10_1s = []
        # green11_1s = []
        # green12_2s = [] 
        # green13_2s = []
        # green14_2s = []
        # green15_3s = []


        whole_lists1_tot = []
        # reds = []
        # greens = []


        yb_upconversions = []
        yb_ybs = []
        yb_excites = []
        er_decays = [] # including MPR and MD
        er_upconversions = []
        er_crossrelaxations = []


        er_excite_0_2s = []
        er_excite_2_7s = []
        er_excite_9_16s = []
        er_excite_10_20s = []
        er_excite_15_25s = []
        er_excite_17_28s = []
        er_excite_18_28s = []
        er_excite_33_36s = []
        er_excite_34_36s = []
        
        for _ in tqdm(range(t2-t1)):

            r, r_emission = self.step(emission = True)

            for i in whole_lists1:
                for key, value in i.items():
                    value.append(r[key])

            # red40s.append(r['red'][0])
            # red71s.append(r['red'][1])
            # red81s.append(r['red'][2])
            # red91s.append(r['red'][3])
            # red10_2s.append(r['red'][4])
            # red11_2s.append(r['red'][5])
            # red11_3s.append(r['red'][6])
            # red12_3s.append(r['red'][7])
            # red13_3s.append(r['red'][8])
            # red14_3s.append(r['red'][9])
            # red15_4s.append(r['red'][10])
            # green50s.append(r['green'][0])
            # green60s.append(r['green'][1])
            # green10_1s.append(r['green'][2])
            # green11_1s.append(r['green'][3])
            # green12_2s.append(r['green'][4])
            # green13_2s.append(r['green'][5])
            # green14_2s.append(r['green'][6])
            # green15_3s.append(r['green'][7])

           
            for key, value in r_emission.items():
                whole_dic = {}
                whole_dic[key] = []
                whole_dic[key].append(sum(value))
                whole_lists1_tot.append(whole_dic)

            # reds.append(sum(r['red']))
            # greens.append(sum(r['green']))



            for i in range(2):
                yb_state_evolution[i].append(r['yb_state'][i])
            for i in range(38):
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

            er_excite_0_2s.append(r['er_excite_0_2s'])
            er_excite_2_7s.append(r['er_excite_2_7s'])
            er_excite_9_16s.append(r['er_excite_9_16s'])
            er_excite_10_20s.append(r['er_excite_10_20s'])
            er_excite_15_25s.append(r['er_excite_15_25s'])
            er_excite_17_28s.append(r['er_excite_17_28s'])
            er_excite_18_28s.append(r['er_excite_18_28s'])
            er_excite_33_36s.append(r['er_excite_33_36s'])
            er_excite_34_36s.append(r['er_excite_34_36s'])


            
        # self.plot_stats(yb_stats, er_stats)
        sim_stats = {}
        # sim_stats['red_microsecond'] = reds
        # sim_stats['green_microsecond'] = greens

        for i in whole_lists1:

            for key, value in i.items():

                sim_stats[key] = value

                # sim_stats['red40s'] = red40s
                # sim_stats['red71s'] = red71s
                # sim_stats['red81s'] = red81s
                # sim_stats['red91s'] = red91s
                # sim_stats['red10_2s'] = red10_2s
                # sim_stats['red11_2s'] = red11_2s
                # sim_stats['red11_3s'] = red11_3s
                # sim_stats['red12_3s'] = red12_3s
                # sim_stats['red13_3s'] = red13_3s
                # sim_stats['red14_3s'] = red14_3s
                # sim_stats['red15_4s'] = red15_4s       
                # sim_stats['green50s'] = green50s
                # sim_stats['green60s'] = green60s
                # sim_stats['green10_1s'] = green10_1s
                # sim_stats['green11_1s'] = green11_1s
                # sim_stats['green12_2s'] = green12_2s
                # sim_stats['green13_2s'] = green13_2s
                # sim_stats['green14_2s'] = green14_2s
                # sim_stats['green15_3s'] = green15_3s

                

                # pps (ms to s)
                sim_stats[f'{key}_avg'] = np.mean(value)*10**6

                # sim_stats['red40_avg'] = np.mean(red40s)
                # sim_stats['red71_avg'] = np.mean(red71s)
                # sim_stats['red81_avg'] = np.mean(red81s)
                # sim_stats['red91_avg'] = np.mean(red91s)
                # sim_stats['red10_2_avg'] = np.mean(red10_2s)
                # sim_stats['red11_2_avg'] = np.mean(red11_2s)
                # sim_stats['red11_3_avg'] = np.mean(red11_3s)
                # sim_stats['red12_3_avg'] = np.mean(red12_3s)
                # sim_stats['red13_3_avg'] = np.mean(red13_3s)
                # sim_stats['red14_3_avg'] = np.mean(red14_3s)
                # sim_stats['red15_4_avg'] = np.mean(red15_4s)
                
                # sim_stats['green50_avg'] = np.mean(green50s)
                # sim_stats['green60_avg'] = np.mean(green60s)
                # sim_stats['green10_1_avg'] = np.mean(green10_1s)
                # sim_stats['green11_1_avg'] = np.mean(green11_1s)
                # sim_stats['green12_2_avg'] = np.mean(green12_2s)
                # sim_stats['green13_2_avg'] = np.mean(green13_2s)
                # sim_stats['green14_2_avg'] = np.mean(green14_2s)
                # sim_stats['green15_3_avg'] = np.mean(green15_3s)


        for i in whole_lists1_tot:
            
            for key, value in i.items():

                sim_stats[f'{key}_microsecond'] = value
                # sim_stats['red_microsecond'] = reds
                # sim_stats['green_microsecond'] = greens

                sim_stats[f'{key}_avg'] = np.mean(value)*10**6
                # sim_stats['red_avg'] = np.mean(reds)
                # sim_stats['green_avg'] = np.mean(greens)


    

        r_key_list = list(r_emission.keys())
        sim_stats[f'{r_key_list[0]}_{r_key_list[1]}_ratio'] = np.mean(r_emission[r_key_list[0]]) / np.mean(r_emission[r_key_list[1]])
        sim_stats[f'{r_key_list[0]}_{r_key_list[1]}_total_avg'] = ( np.mean(r_emission[r_key_list[0]]) + np.mean(r_emission[r_key_list[1]]) )*10**6
        # sim_stats['red_green_ratio'] = np.mean(reds)/np.mean(greens)
        # sim_stats['red_green_total_avg'] = np.mean(reds)+np.mean(greens)

        sim_stats['yb_distribution'] = yb_state_evolution
        sim_stats['er_distribution'] = er_state_evolution

        color_totals = {}
        for i in whole_lists1:
            for key in i.keys():

                number_start = int(key[:-1].split('_')[1])
                number_end = int(key[:-1].split('_')[2])

                sim_stats[f'{key}_avg_pop'] = np.mean(er_state_evolution[number_start][t1:]) * self.tag[f'E{number_start}E{number_end}']


                # # calculate red and green by population * rate
                
                # sim_stats['red40_avg_pop'] = np.mean(er_state_evolution[4][t1:]) * self.tag['E4E0']
                # sim_stats['red71_avg_pop'] = np.mean(er_state_evolution[7][t1:]) * self.tag['E7E1']
                # sim_stats['red81_avg_pop'] = np.mean(er_state_evolution[8][t1:]) * self.tag['E8E1']
                # sim_stats['red91_avg_pop'] = np.mean(er_state_evolution[9][t1:]) * self.tag['E9E1']
                # sim_stats['red10_2_avg_pop'] = np.mean(er_state_evolution[10][t1:]) * self.tag['E10E2']
                # sim_stats['red11_2_avg_pop'] = np.mean(er_state_evolution[11][t1:]) * self.tag['E11E2']
                # sim_stats['red11_3_avg_pop'] = np.mean(er_state_evolution[11][t1:]) * self.tag['E11E3']
                # sim_stats['red12_3_avg_pop'] = np.mean(er_state_evolution[12][t1:]) * self.tag['E12E3']
                # sim_stats['red13_3_avg_pop'] = np.mean(er_state_evolution[13][t1:]) * self.tag['E13E3']
                # sim_stats['red14_3_avg_pop'] = np.mean(er_state_evolution[14][t1:]) * self.tag['E14E3']
                # sim_stats['red15_4_avg_pop'] = np.mean(er_state_evolution[15][t1:]) * self.tag['E15E4']

                # sim_stats['green50_avg_pop'] = np.mean(er_state_evolution[5][t1:]) * self.tag['E5E0']
                # sim_stats['green60_avg_pop'] = np.mean(er_state_evolution[6][t1:]) * self.tag['E6E0']
                # sim_stats['green10_1_avg_pop'] = np.mean(er_state_evolution[10][t1:]) * self.tag['E10E1']
                # sim_stats['green11_1_avg_pop'] = np.mean(er_state_evolution[11][t1:]) * self.tag['E11E1']
                # sim_stats['green12_2_avg_pop'] = np.mean(er_state_evolution[12][t1:]) * self.tag['E12E2']
                # sim_stats['green13_2_avg_pop'] = np.mean(er_state_evolution[13][t1:]) * self.tag['E13E2']
                # sim_stats['green14_2_avg_pop'] = np.mean(er_state_evolution[14][t1:]) * self.tag['E14E2']
                # sim_stats['green15_3_avg_pop'] = np.mean(er_state_evolution[15][t1:]) * self.tag['E15E3']



                color_name = key.split('_')[0]
                # If the color name isn't in the color_totals, initialize it

                if color_name not in color_totals:
                    color_totals[color_name] = 0

                color_totals[color_name] += sim_stats[f'{key}_avg_pop']

        # Updating sim_stats with the aggregated values
        sim_stats.update({f"{color}_avg_pop": total for color, total in color_totals.items()})
        # sim_stats['red_avg_pop'] = sim_stats['red40_avg_pop'] + sim_stats['red71_avg_pop'] + sim_stats['red81_avg_pop'] + sim_stats['red91_avg_pop'] + sim_stats['red10_2_avg_pop'] + sim_stats['red11_2_avg_pop'] + sim_stats['red11_3_avg_pop'] + sim_stats['red12_3_avg_pop'] + sim_stats['red13_3_avg_pop'] + sim_stats['red14_3_avg_pop'] + sim_stats['red15_4_avg_pop']
        # sim_stats['green_avg_pop'] = sim_stats['green50_avg_pop'] + sim_stats['green60_avg_pop'] + sim_stats['green10_1_avg_pop'] + sim_stats['green11_1_avg_pop'] + sim_stats['green12_2_avg_pop'] + sim_stats['green13_2_avg_pop'] + sim_stats['green14_2_avg_pop'] + sim_stats['green15_3_avg_pop']
    

        color_totals_key_list = list(color_totals.keys())
        sim_stats[f'{color_totals_key_list[0]}_{color_totals_key_list[1]}_ratio_pop'] = color_totals[color_totals_key_list[0]] / color_totals[color_totals_key_list[1]]
        sim_stats[f'{color_totals_key_list[0]}_{color_totals_key_list[1]}_total_avg_pop'] = color_totals[color_totals_key_list[0]] + color_totals[color_totals_key_list[1]]
        # sim_stats['red_green_ratio_pop'] = sim_stats['red_avg_pop'] / sim_stats['green_avg_pop']
        # sim_stats['red_green_total_avg_pop'] = sim_stats['red_avg_pop'] + sim_stats['green_avg_pop']

        

        sim_stats['yb_upconversions'] = yb_upconversions
        sim_stats['yb_ybs'] = yb_ybs
        sim_stats['yb_excites'] = yb_excites
        sim_stats['er_decays'] = er_decays
        sim_stats['er_upconversions'] = er_upconversions
        sim_stats['er_crossrelaxations'] = er_crossrelaxations

        sim_stats['er_excite_0_2s'] = er_excite_0_2s
        sim_stats['er_excite_2_7s'] = er_excite_2_7s
        sim_stats['er_excite_9_16s'] = er_excite_9_16s
        sim_stats['er_excite_10_20s'] = er_excite_10_20s
        sim_stats['er_excite_15_25s'] = er_excite_15_25s
        sim_stats['er_excite_17_28s'] = er_excite_17_28s
        sim_stats['er_excite_18_28s'] = er_excite_18_28s
        sim_stats['er_excite_33_36s'] = er_excite_33_36s
        sim_stats['er_excite_34_36s'] = er_excite_34_36s        

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

        

