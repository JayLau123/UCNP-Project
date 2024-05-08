import numpy as np
import random

from EnergyTransfer import *
from Lattice_Tm import *
from Point_Tm import *

from tqdm import tqdm


# Tm
tag_default={'c0':9.836062e-40, # Yb-Yb resonant energy transfer
            'Ws': 827,
            'E1E0': 125.48935641249709+2.8398261386622337,
            'E2E1': 3.318715560788497+149977.8404029679,
            'E2E0': 176.99746253145912+50.01921044404302,
            'E3E2': 34.206376660350635+7.407650126658919+304.82652110247335,
            'E3E1': 66.54090079350377,
            'E3E0': 778.6223334161804,
            'E4E3': 0.4924196808876664+1768677.8208097615,
            'E4E2': 146.53082969740504,
            'E4E1': 258.72754779151234+58.98152867828142,
            'E4E0': 1725.685918453449,
            'E5E4': 0.013601242611778256+0.017876416530239997+156605871.04362732,
            'E5E3': 5.142484506889417,
            'E5E2': 192.81631278900016,
            'E5E1': 362.10251583753916,
            'E5E0': 548.8209590762159,
            'E6E5': 12.27244074045102+0.4986967075676975,
            'E6E4': 45.243463132798716,
            'E6E3': 23.045067137896037,
            'E6E2': 494.8335554945873,
            'E6E1': 790.6119449426245,
            'E6E0': 612.1894036274351,
            'E7E6': 95.08404006966971+0.085455699785309,
            'E7E5': 686.9558866118873,
            'E7E4': 488.5169554820362,
            'E7E3': 2125.9773631820567,
            'E7E2': 94.77917251652532,
            'E7E1': 2862.4113298030165,
            'E7E0': 7073.7489463917145,
            'E8E7': 36.360391540658185+0.043034327471444415,
            'E8E6': 569.6516174960112,
            'E8E5': 12032.350149796916,
            'E8E4': 0.0,
            'E8E3': 12900.2316312164,
            'E8E2': 0.0,
            'E8E1': 2187.1540079844326,
            'E8E0': 9927.473226890408,
            'E9E8': 0.0009868585361115672+147044060.55781594,
            'E9E7': 92.02566943051052,
            'E9E6': 1821.4670182763978,
            'E9E5': 830.6733816463998,
            'E9E4': 24.831884624739615,
            'E9E3': 3347.4442413228044,
            'E9E2': 47.629920257740245,
            'E9E1': 3947.2568763835907,
            'E9E0': 886.4651309513591,
            'E10E9': 0.0008355835105102547+51456267.57176652,
            'E10E8': 0.0+0.2550375,
            'E10E7': 384.94530942879226,
            'E10E6': 24.780471461156164,
            'E10E5': 1932.3866509383674,
            'E10E4': 11701.39579382536,
            'E10E3': 2070.270151288934,
            'E10E2': 11169.388410903926,
            'E10E1': 16852.549991893735,
            'E10E0': 6148.3298289008,
            'E11E10': 1.0217676091109+1851011.5502068659,
            'E11E9': 10.632357583847941,
            'E11E8': 4.152306926420422,
            'E11E7': 145.78586549966536,
            'E11E6': 2870.8263210603573,
            'E11E5': 512.9026534772217,
            'E11E4': 4398.79486047782,
            'E11E3': 3243.3217145047865,
            'E11E2': 7747.609950763437,
            'E11E1': 8907.227766388574,
            'E11E0': 13879.298417790638}




class Simulator_tm():

    def __init__(self, lattice, tag = None, dt = 10**(-6)):

        ################################### self.lattice has all methods and attributes form Latttice class
        # get_nerighbors(self, r):
        #    self.neighbors = ret 
        # ret is a dic, key is all ion in self.n_points (3401, Yb+Tm or Yb+Er), values are many tuples: (nearby ion, distance< 1 nm) 
        # 

        self.lattice = lattice.deep_copy() 
        self.t = 0
        self.dt = dt

        if tag is not None:
            self.tag = tag
        else:
            self.tag = tag_default

        self.cross_relaxation = cross_relaxation_Tm()
        self.up_conversion = up_conversion_Tm()        

    def step(self, steps = 1, emission = False):

        if emission:

            NIR30s = []
            NIR62s = []
            NIR75s = []

            blue60s = []
            blue71s = []
            blue83s = []
            blue10_4s = []
            blue10_5s = []



            yb_upconversions = []
            yb_ybs = []
            yb_excites = []

            tm_decays = []
            tm_upconversions = []
            tm_crossrelaxations = []

        for _ in range(steps):

            if emission:

                # red40 = 0
                # green50 = 0
                # green60 = 0

                NIR30 = 0
                NIR62 = 0
                NIR75 = 0

                blue60 = 0
                blue71 = 0
                blue83 = 0
                blue10_4 = 0
                blue10_5 = 0

                yb_upconversion = 0
                yb_yb = 0
                yb_excite = 0

                tm_decay = {} # including MPR and MD
                tm_upconversion = {}
                tm_crossrelaxation = {}

            np.random.shuffle(self.lattice.excited)

            # excited state yb/tm/er state transition
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
                # print(rates)
                no_reaction_prob = 1-self.dt*(sum(ET_rates) + sum(p_decay_rates))

                # stay in current state v.s. change
                if np.random.rand() < no_reaction_prob:
                    continue  # skip the current iteration and continue with the next one

                # decay v.s. ET process
                # if decay, then decide which pathway to go

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

                        if p.state == 7 and new_state == 5:
                            NIR75 += 1


                        if p.state == 6 and new_state == 0:
                            blue60 += 1

                        if p.state == 7 and new_state == 1:
                            blue71 += 1

                        if p.state == 8 and new_state == 3:
                            blue83 += 1

                        if p.state == 10 and new_state == 4:
                            blue10_4 += 1

                        if p.state == 10 and new_state == 5:
                            green10_5 += 1


                    p.state = new_state

                # no stay, no decay, so ET process
                else:
                    prob_sum = sum(ET_rates)
                    ET_rates = [i/prob_sum for i in ET_rates]
                
                    nei, _ = random.choices(pairs, ET_rates)[0] # extracts the first item from the chosen pair: the first item of (nei, pair) is nei ################

                    if p.type == 'Yb' and nei.type == 'Yb':
                        p.state = 0
                        nei.state = 1
                        yb_yb += 1

                    elif p.type == 'Yb' and nei.type != 'Yb':

                        new_state = self.up_conversion[nei.state].select_path(distance)
                        tm_upconversion[(nei.state, new_state[1])] = tm_upconversion.setdefault((nei.state, new_state[1]), 0) + 1
                        p.state = new_state[0]
                        nei.state = new_state[1]
                        yb_upconversion += 1

                    else:
                        new_state = self.cross_relaxation[p.state][nei.state].select_path(distance)
                        tm_crossrelaxation[(p.state, new_state[0], nei.state, new_state[1])] = tm_crossrelaxation.setdefault((p.state, new_state[0], nei.state, new_state[1]), 0) + 1
                        p.state = new_state[0]
                        nei.state = new_state[1]
                



            # laser excites ground state yb to excited yb
            for p in self.lattice.ground_Yb: 
                if np.random.rand() < self.dt*self.tag['laser']:
                    p.state = 1
                    yb_excite += 1
            

            # update new excited state Yb and Tm, and update new ground state Yb
            self.lattice.excited = [p for p in self.lattice.points if p.state != 0]
            self.lattice.ground_Yb = [p for p in self.lattice.points if p.type == 'Yb' and p.state == 0]
            self.t += 1

            if emission:

                NIR30s.append(NIR30)
                NIR62s.append(NIR62)
                NIR75s.append(NIR75)
                blue60s.append(blue60)
                blue71s.append(blue71)
                blue83s.append(blue83)
                blue10_4s.append(blue10_4)
                blue10_5s.append(blue10_5)
    



                yb_upconversions.append(yb_upconversion)
                yb_ybs.append(yb_yb)
                yb_excites.append(yb_excite)

                tm_decays.append(tm_decay)
                tm_upconversions.append(tm_upconversion)
                tm_crossrelaxations.append(tm_crossrelaxation)



        if emission:
 
            step_data = {}
            yb_state = [len([p for p in self.lattice.points if p.state == i and p.type == 'Yb']) for i in range(2)]
            step_data['yb_state'] = yb_state
            tm_state = [len([p for p in self.lattice.points if p.state == i and p.type == 'Tm']) for i in range(12)]
            step_data['tm_state'] = tm_state

            if steps == 1: 


                # NIR30s.append(NIR30)
                # NIR62s.append(NIR62)
                # NIR75s.append(NIR75)
                # blue60s.append(blue60)
                # blue71s.append(blue71)
                # blue83s.append(blue83)
                # blue10_4s.append(blue10_4)
                # blue10_5s.append(blue10_5)

                step_data['NIR'] = NIR30s[0], NIR62s[0], NIR75s[0]
                step_data['blue'] = blue60s[0], blue71s[0], blue83s[0], blue10_4s[0], blue10_5s[0]


                step_data['yb_upconversions'] = yb_upconversions[0]
                step_data['yb_ybs'] = yb_ybs[0]
                step_data['yb_excites'] = yb_excites[0]


                step_data['tm_decays'] = tm_decays[0]
                step_data['tm_upconversions'] = tm_upconversions[0]
                step_data['tm_crossrelaxations'] = tm_crossrelaxations[0]
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

        ## At 2000 steps, reach steady state
   
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
        
        # c = 0



        NIRs = []
        NIR30s = []
        NIR62s = []
        NIR75s = []

        blues = []
        blue60s = []
        blue71s = []
        blue83s = []
        blue10_4s = []
        blue10_5s = []


        yb_upconversions = []
        yb_ybs = []
        yb_excites = []
        tm_decays = [] # including MPR and MD
        tm_upconversions = []
        tm_crossrelaxations = []
        
        for _ in tqdm(range(t2-t1)):

            r = self.step(emission = True)

            NIRs.append(sum(r['NIR']))

            NIR30s.append(r['NIR'][0])
            NIR62s.append(r['NIR'][1])
            NIR75s.append(r['NIR'][2])

            blues.append(sum(r['blue']))

            blue60s.append(r['blue'][0])
            blue71s.append(r['blue'][1])
            blue83s.append(r['blue'][2])
            blue10_4s.append(r['blue'][3])
            blue10_5s.append(r['blue'][4])


            for i in range(2):
                yb_state_evolution[i].append(r['yb_state'][i])
            for i in range(12):
                tm_state_evolution[i].append(r['tm_state'][i])


            # c+=1
            # if c%100 == 0:
            #     yb_stat, tm_stat = self.lattice.collect_stats()
            #     yb_stats.append(yb_stat)
            #     tm_stats.append(tm_stat)
            

            
            yb_upconversions.append(r['yb_upconversions'])
            yb_ybs.append(r['yb_ybs'])
            yb_excites.append(r['yb_excites'])
            tm_decays.append(r['tm_decays'])
            tm_upconversions.append(r['tm_upconversions'])
            tm_crossrelaxations.append(r['tm_crossrelaxations'])
            


        # self.plot_stats(yb_stats, tm_stats)
        sim_stats = {}
        sim_stats['NIR_microsecond'] = NIRs
        sim_stats['blue_microsecond'] = blues

        sim_stats['NIR30s'] = NIR30s
        sim_stats['NIR62s'] = NIR62s
        sim_stats['NIR75s'] = NIR75s

        sim_stats['blue60s'] = blue60s
        sim_stats['blue71s'] = blue71s
        sim_stats['blue83s'] = blue83s
        sim_stats['blue10_4s'] = blue10_4s
        sim_stats['blue10_5s'] = blue10_5s
       
        
        sim_stats['NIR_avg'] = np.mean(NIRs)
        sim_stats['blue_avg'] = np.mean(blues)
        sim_stats['NIR_blue_ratio'] = np.mean(NIRs)/np.mean(blues)
        sim_stats['NIR_blue_total_avg'] = np.mean(NIRs)+np.mean(blues)

        sim_stats['NIR30_avg'] = np.mean(NIR30s)
        sim_stats['NIR62_avg'] = np.mean(NIR62s)
        sim_stats['NIR75_avg'] = np.mean(NIR75s)

        sim_stats['blue60_avg'] = np.mean(blue60s)
        sim_stats['blue71_avg'] = np.mean(blue71s)
        sim_stats['blue83_avg'] = np.mean(blue83s)
        sim_stats['blue10_4_avg'] = np.mean(blue10_4s)
        sim_stats['blue10_5_avg'] = np.mean(blue10_5s)

        sim_stats['yb_distribution'] = yb_state_evolution
        sim_stats['tm_distribution'] = tm_state_evolution

        # calculate red and green by population * rate
        sim_stats['NIR_avg_pop'] = np.mean(tm_state_evolution[3][t1:]) * self.tag['E3E0'] + np.mean(tm_state_evolution[6][t1:]) * self.tag['E6E2'] + np.mean(tm_state_evolution[7][t1:]) * self.tag['E7E5']
        sim_stats['NIR30_avg_pop'] = np.mean(tm_state_evolution[3][t1:]) * self.tag['E3E0']
        sim_stats['NIR62_avg_pop'] = np.mean(tm_state_evolution[6][t1:]) * self.tag['E6E2']
        sim_stats['NIR75_avg_pop'] = np.mean(tm_state_evolution[7][t1:]) * self.tag['E7E5']

        sim_stats['blue_avg_pop'] = np.mean(tm_state_evolution[6][t1:]) * self.tag['E6E0'] + np.mean(tm_state_evolution[7][t1:]) * self.tag['E7E1'] + np.mean(tm_state_evolution[8][t1:]) * self.tag['E8E3']+ np.mean(tm_state_evolution[10][t1:]) * self.tag['E10E4']+ np.mean(tm_state_evolution[10][t1:]) * self.tag['E10E5']
        sim_stats['blue60_avg_pop'] = np.mean(tm_state_evolution[6][t1:]) * self.tag['E6E0'] 
        sim_stats['blue71_avg_pop'] = np.mean(tm_state_evolution[7][t1:]) * self.tag['E7E1'] 
        sim_stats['blue83_avg_pop'] = np.mean(tm_state_evolution[8][t1:]) * self.tag['E8E3']
        sim_stats['blue10_4_avg_pop'] = np.mean(tm_state_evolution[10][t1:]) * self.tag['E10E4']
        sim_stats['blue10_5_avg_pop'] = np.mean(tm_state_evolution[10][t1:]) * self.tag['E10E5']


        sim_stats['NIR_blue_ratio_pop'] = sim_stats['NIR_avg_pop'] / sim_stats['blue_avg_pop']
        sim_stats['NIR_blue_total_avg_pop'] = sim_stats['NIR_avg_pop'] + sim_stats['blue_avg_pop']
   
        sim_stats['yb_upconversions'] = yb_upconversions
        sim_stats['yb_ybs'] = yb_ybs
        sim_stats['yb_excites'] = yb_excites
        sim_stats['tm_decays'] = tm_decays
        sim_stats['tm_upconversions'] = tm_upconversions
        sim_stats['tm_crossrelaxations'] = tm_crossrelaxations

        return sim_stats
    

    


'''
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
'''

        

