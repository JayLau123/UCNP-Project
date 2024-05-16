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
        'E7E6':0.4092613138830535+15062862.442801291,'E7E5':0.01904121955274265,'E7E4':3.4467583618029134+17.9,'E7E3':93.44157758618482,'E7E2':162.98778196545229,'E7E1':334.1120016219258,'E7E0':2256.2758284193,
        'E8E7': 1.6957653461136708+2323866.221778032,
        'E8E6': 3.067097722867185,
        'E8E5': 0.4645423717222112,
        'E8E4': 94.31318219852967,
        'E8E3': 75.27551752242351,
        'E8E2': 87.11248267553177,
        'E8E1': 918.9196021042433,
        'E8E0': 1090.4059764475894,
        'E9E8': 0.014348135979715888+301337914.1862357,
        'E9E7': 0.4830720928474433,
        'E9E6': 0.09524021206644484,
        'E9E5': 2.251838694215458,
        'E9E4': 16.968045956739193,
        'E9E3': 215.70878030483897,
        'E9E2': 753.5632557882657,
        'E9E1': 94.35534541803662,
        'E9E0': 982.1372000625187,
        'E10E9': 0.04934978765160607+2220499.7286637346,
        'E10E8': 0.15873924027578779,
        'E10E7': 4.364377459681794,
        'E10E6': 12.330696169635486,
        'E10E5': 0.2686649239407923,
        'E10E4': 16.67371622352856,
        'E10E3': 16.464052082910243,
        'E10E2': 213.86053490531287,
        'E10E1': 936.5234192196058,
        'E10E0': 958.440059896806,
        'E11E10': 1.1625839088604317+1548415.6913059584,
        'E11E9': 1.324526425596782,
        'E11E8': 1.8771043878248963,
        'E11E7': 13.996305881174957,
        'E11E6': 17.832523357272812,
        'E11E5': 16.563287024635635,
        'E11E4': 236.19904138444724,
        'E11E3': 94.45944293499487,
        'E11E2': 64.67232480594103,
        'E11E1': 1243.9346549177662,
        'E11E0': 9297.316486123314,
        'E12E11': 0.19649315676566376+44266681.06129336,
        'E12E10': 0.5588032405459346,
        'E12E9': 7.971890540105319,
        'E12E8': 12.76800258479716,
        'E12E7': 99.44086028635165,
        'E12E6': 77.31690533994991,
        'E12E5': 36.12673522485811,
        'E12E4': 508.55789767721313,
        'E12E3': 13.844572642393212,
        'E12E2': 449.589325290292,
        'E12E1': 5387.632532996023,
        'E12E0': 2130.74558349785,
        'E13E12': 0.00022364145399113926+474960799.63932574,
        'E13E11': 0.2638687077691587,
        'E13E10': 4.346372893096346,
        'E13E9': 0.001955763929477078,
        'E13E8': 1.1373348678335395,
        'E13E7': 0.018400121952239102,
        'E13E6': 126.165839780936,
        'E13E5': 0.40391177043368465,
        'E13E4': 30.52735318767222,
        'E13E3': 196.57879852497175,
        'E13E2': 287.00804091501544,
        'E13E1': 42.73483724274275,
        'E13E0': 410.56807941337576,
        'E14E13': 0.0006125522463003234+516581089.11427534,
        'E14E12': 0.016196788996499387,
        'E14E11': 0.11387972107026675,
        'E14E10': 2.350107713527409,
        'E14E9': 8.943247284418822,
        'E14E8': 38.51206896635523,
        'E14E7': 35.04334807995203,
        'E14E6': 64.61437433833866,
        'E14E5': 69.86579523458428,
        'E14E4': 14.340500907451297,
        'E14E3': 1060.9796743420568,
        'E14E2': 2389.063384347622,
        'E14E1': 455.3660616617849,
        'E14E0': 968.7893351629385,
        'E15E14': 0.6754796116197045+4208.0003244398395,
        'E15E13': 0.9969178344353601,
        'E15E12': 0.8791773434076396,
        'E15E11': 3.4348914051758057,
        'E15E10': 109.06244207943858,
        'E15E9': 9.393836406326464,
        'E15E8': 39.6041250381591,
        'E15E7': 38.78927541775605,
        'E15E6': 53.87575686980191,
        'E15E5': 202.93617550796554,
        'E15E4': 160.79258052288716,
        'E15E3': 248.19085435328444,
        'E15E2': 955.0672069535281,
        'E15E1': 1489.4013441938105,
        'E15E0': 353.04203238888493}




class Simulator():

    def __init__(self, lattice, tag = None, dt = 10**(-6), excite_er = False):

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
        self.excite_er = excite_er




    def step(self, steps = 1, emission = False):

        if emission:

            red40s = []
            red71s = []
            red81s = []
            red91s = []
            red10_2s = []
            red11_2s = []
            red11_3s = []
            red12_3s = []
            red13_3s = []
            red14_3s = []
            red15_4s = []


            green50s = []
            green60s = []
            green10_1s = []
            green11_1s = []
            green12_2s = []
            green13_2s = []
            green14_2s = []
            green15_3s = []



            yb_upconversions = []
            yb_ybs = []
            yb_excites = []
            er_decays = []
            er_upconversions = []
            er_crossrelaxations = []

            # consider the Er excitation from laser: E0 to E2, E2 to E7
            er_excite_02s = []
            er_excite_27s = []

        for _ in range(steps):

            if emission:

                red40 = 0
                red71 = 0
                red81 = 0
                red91 = 0
                red10_2 = 0
                red11_2 = 0
                red11_3 = 0
                red12_3 = 0
                red13_3 = 0
                red14_3 = 0
                red15_4 = 0


                green50 = 0
                green60 = 0
                green10_1 = 0
                green11_1 = 0
                green12_2 = 0
                green13_2 = 0
                green14_2 = 0
                green15_3 = 0

                yb_upconversion = 0
                yb_yb = 0
                yb_excite = 0

                er_excite_02 = 0
                er_excite_27 = 0

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

                        if p.state == 7 and new_state == 1:
                            red71 += 1

                        if p.state == 8 and new_state == 1:
                            red81 += 1

                        if p.state == 9 and new_state == 1:
                            red91 += 1

                        if p.state == 10 and new_state == 2:
                            red10_2 += 1

                        if p.state == 11 and new_state == 2:
                            red11_2 += 1

                        if p.state == 11 and new_state == 3:
                            red11_3 += 1

                        if p.state == 12 and new_state == 3:
                            red12_3 += 1

                        if p.state == 13 and new_state == 3:
                            red13_3 += 1

                        if p.state == 14 and new_state == 3:
                            red14_3 += 1

                        if p.state == 15 and new_state == 4:
                            red15_4 += 1




                        if p.state == 5 and new_state == 0:
                            green50 += 1
                        if p.state == 6 and new_state == 0:
                            green60 += 1

                        if p.state == 10 and new_state == 1:
                            green10_1 += 1

                        if p.state == 11 and new_state == 1:
                            green11_1 += 1

                        if p.state == 12 and new_state == 2:
                            green12_2 += 1

                        if p.state == 13 and new_state == 2:
                            green13_2 += 1
                        
                        if p.state == 14 and new_state == 2:
                            green14_2 += 1
                        
                        if p.state == 15 and new_state == 3:
                            green15_3 += 1


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
            
            # 
            for p in [point for point in self.lattice.points if point.type == 'Er' and point.state == 2]:
                if np.random.rand() < self.dt*self.tag['laser_er']:
                    p.state = 7
                    er_excite_27 += 1

            for p in [point for point in self.lattice.points if point.type == 'Er' and point.state == 0]:
                if np.random.rand() < self.dt*self.tag['laser_er']:
                    p.state = 2
                    er_excite_02 += 1
            
            # update new excited state Yb and Er, and update new ground state Yb
            self.lattice.excited = [p for p in self.lattice.points if p.state != 0]
            self.lattice.ground_yb = [p for p in self.lattice.points if p.type == 'Yb' and p.state == 0]
            self.t += 1

            if emission:


                red40s.append(red40)
                red71s.append(red71)
                red81s.append(red81)
                red91s.append(red91)
                red10_2s.append(red10_2)
                red11_2s.append(red11_2)
                red11_3s.append(red11_3)
                red12_3s.append(red12_3)
                red13_3s.append(red13_3)
                red14_3s.append(red14_3)
                red15_4s.append(red15_4)


                green50s.append(green50)
                green60s.append(green60)
                green10_1s.append(green10_1)
                green11_1s.append(green11_1)
                green12_2s.append(green12_2)
                green13_2s.append(green13_2)
                green14_2s.append(green14_2)
                green15_3s.append(green15_3)

    



                yb_upconversions.append(yb_upconversion)
                yb_ybs.append(yb_yb)
                yb_excites.append(yb_excite)
                er_decays.append(er_decay)
                er_upconversions.append(er_upconversion)
                er_crossrelaxations.append(er_crossrelaxation)

                er_excite_27s.append(er_excite_27)
                er_excite_02s.append(er_excite_02)
        
        if emission:
 
            step_data = {}
            yb_state = [len([p for p in self.lattice.points if p.state == i and p.type == 'Yb']) for i in range(2)]
            step_data['yb_state'] = yb_state
            er_state = [len([p for p in self.lattice.points if p.state == i and p.type == 'Er']) for i in range(16)]
            step_data['er_state'] = er_state

            if steps == 1: 


                step_data['red'] = red40s[0], red71s[0], red81s[0], red91s[0], red10_2s[0], red11_2s[0], red11_3s[0], red12_3s[0], red13_3s[0], red14_3s[0], red15_4s[0] 
                step_data['green'] = green50s[0], green60s[0], green10_1s[0], green11_1s[0], green12_2s[0], green13_2s[0], green14_2s[0], green15_3s[0]


                step_data['yb_upconversions'] = yb_upconversions[0]
                step_data['yb_ybs'] = yb_ybs[0]
                step_data['yb_excites'] = yb_excites[0]
                step_data['er_decays'] = er_decays[0]
                step_data['er_upconversions'] = er_upconversions[0]
                step_data['er_crossrelaxations'] = er_crossrelaxations[0]

                step_data['er_excite_02s'] = er_excite_02s[0]
                step_data['er_excite_27s'] = er_excite_27s[0]

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
        er_state_evolution = {i:[] for i in range(0, 16)}
        
        for _ in tqdm(range(t1)):
            r = self.step(emission=True)
            for i in range(2):
                yb_state_evolution[i].append(r['yb_state'][i])
            for i in range(16):
                er_state_evolution[i].append(r['er_state'][i])
        if t2 is None:
            return
        c = 0

        # yb_stats = []
        # er_stats = []

        reds = []

        red40s = []
        red71s = []
        red81s = []
        red91s = []
        red10_2s = []
        red11_2s = []
        red11_3s = []
        red12_3s = []
        red13_3s = []
        red14_3s = []
        red15_4s = []


        greens = []
        
        green50s = []
        green60s = []
        green10_1s = []
        green11_1s = []
        green12_2s = [] 
        green13_2s = []
        green14_2s = []
        green15_3s = []


        yb_upconversions = []
        yb_ybs = []
        yb_excites = []
        er_decays = [] # including MPR and MD
        er_upconversions = []
        er_crossrelaxations = []

        er_excite_02s = []
        er_excite_27s = []
        
        for _ in tqdm(range(t2-t1)):

            r = self.step(emission = True)

            reds.append(sum(r['red']))

            red40s.append(r['red'][0])
            red71s.append(r['red'][1])
            red81s.append(r['red'][2])
            red91s.append(r['red'][3])
            red10_2s.append(r['red'][4])
            red11_2s.append(r['red'][5])
            red11_3s.append(r['red'][6])
            red12_3s.append(r['red'][7])
            red13_3s.append(r['red'][8])
            red14_3s.append(r['red'][9])
            red15_4s.append(r['red'][10])
                

            greens.append(sum(r['green']))

            green50s.append(r['green'][0])
            green60s.append(r['green'][1])
            green10_1s.append(r['green'][2])
            green11_1s.append(r['green'][3])
            green12_2s.append(r['green'][4])
            green13_2s.append(r['green'][5])
            green14_2s.append(r['green'][6])
            green15_3s.append(r['green'][7])




            for i in range(2):
                yb_state_evolution[i].append(r['yb_state'][i])
            for i in range(16):
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
            er_excite_02s.append(r['er_excite_02s'])
            er_excite_27s.append(r['er_excite_27s'])
            
        # self.plot_stats(yb_stats, er_stats)
        sim_stats = {}
        sim_stats['red_microsecond'] = reds
        sim_stats['green_microsecond'] = greens


        sim_stats['red40s'] = red40s
        sim_stats['red71s'] = red71s
        sim_stats['red81s'] = red81s
        sim_stats['red91s'] = red91s
        sim_stats['red10_2s'] = red10_2s
        sim_stats['red11_2s'] = red11_2s
        sim_stats['red11_3s'] = red11_3s
        sim_stats['red12_3s'] = red12_3s
        sim_stats['red13_3s'] = red13_3s
        sim_stats['red14_3s'] = red14_3s
        sim_stats['red15_4s'] = red15_4s
 

        
        sim_stats['green50s'] = green50s
        sim_stats['green60s'] = green60s
        sim_stats['green10_1s'] = green10_1s
        sim_stats['green11_1s'] = green11_1s
        sim_stats['green12_2s'] = green12_2s
        sim_stats['green13_2s'] = green13_2s
        sim_stats['green14_2s'] = green14_2s
        sim_stats['green15_3s'] = green15_3s


        sim_stats['red_avg'] = np.mean(reds)

        sim_stats['red40_avg'] = np.mean(red40s)
        sim_stats['red71_avg'] = np.mean(red71s)
        sim_stats['red81_avg'] = np.mean(red81s)
        sim_stats['red91_avg'] = np.mean(red91s)
        sim_stats['red10_2_avg'] = np.mean(red10_2s)
        sim_stats['red11_2_avg'] = np.mean(red11_2s)
        sim_stats['red11_3_avg'] = np.mean(red11_3s)
        sim_stats['red12_3_avg'] = np.mean(red12_3s)
        sim_stats['red13_3_avg'] = np.mean(red13_3s)
        sim_stats['red14_3_avg'] = np.mean(red14_3s)
        sim_stats['red15_4_avg'] = np.mean(red15_4s)

        sim_stats['green_avg'] = np.mean(greens)

        sim_stats['green50_avg'] = np.mean(green50s)
        sim_stats['green60_avg'] = np.mean(green60s)
        sim_stats['green10_1_avg'] = np.mean(green10_1s)
        sim_stats['green11_1_avg'] = np.mean(green11_1s)
        sim_stats['green12_2_avg'] = np.mean(green12_2s)
        sim_stats['green13_2_avg'] = np.mean(green13_2s)
        sim_stats['green14_2_avg'] = np.mean(green14_2s)
        sim_stats['green15_3_avg'] = np.mean(green15_3s)



        sim_stats['red_green_ratio'] = np.mean(reds)/np.mean(greens)
        sim_stats['red_green_total_avg'] = np.mean(reds)+np.mean(greens)


        sim_stats['yb_distribution'] = yb_state_evolution
        sim_stats['er_distribution'] = er_state_evolution

        # calculate red and green by population * rate
        
        sim_stats['red40_avg_pop'] = np.mean(er_state_evolution[4][t1:]) * self.tag['E4E0']
        sim_stats['red71_avg_pop'] = np.mean(er_state_evolution[7][t1:]) * self.tag['E7E1']
        sim_stats['red81_avg_pop'] = np.mean(er_state_evolution[8][t1:]) * self.tag['E8E1']
        sim_stats['red91_avg_pop'] = np.mean(er_state_evolution[9][t1:]) * self.tag['E9E1']
        sim_stats['red10_2_avg_pop'] = np.mean(er_state_evolution[10][t1:]) * self.tag['E10E2']
        sim_stats['red11_2_avg_pop'] = np.mean(er_state_evolution[11][t1:]) * self.tag['E11E2']
        sim_stats['red11_3_avg_pop'] = np.mean(er_state_evolution[11][t1:]) * self.tag['E11E3']
        sim_stats['red12_3_avg_pop'] = np.mean(er_state_evolution[12][t1:]) * self.tag['E12E3']
        sim_stats['red13_3_avg_pop'] = np.mean(er_state_evolution[13][t1:]) * self.tag['E13E3']
        sim_stats['red14_3_avg_pop'] = np.mean(er_state_evolution[14][t1:]) * self.tag['E14E3']
        sim_stats['red15_4_avg_pop'] = np.mean(er_state_evolution[15][t1:]) * self.tag['E15E4']

        sim_stats['red_avg_pop'] = sim_stats['red40_avg_pop'] + sim_stats['red71_avg_pop'] + sim_stats['red81_avg_pop'] + sim_stats['red91_avg_pop'] + sim_stats['red10_2_avg_pop'] + sim_stats['red11_2_avg_pop'] + sim_stats['red11_3_avg_pop'] + sim_stats['red12_3_avg_pop'] + sim_stats['red13_3_avg_pop'] + sim_stats['red14_3_avg_pop'] + sim_stats['red15_4_avg_pop']




        sim_stats['green50_avg_pop'] = np.mean(er_state_evolution[5][t1:]) * self.tag['E5E0']
        sim_stats['green60_avg_pop'] = np.mean(er_state_evolution[6][t1:]) * self.tag['E6E0']
        sim_stats['green10_1_avg_pop'] = np.mean(er_state_evolution[10][t1:]) * self.tag['E10E1']
        sim_stats['green11_1_avg_pop'] = np.mean(er_state_evolution[11][t1:]) * self.tag['E11E1']
        sim_stats['green12_2_avg_pop'] = np.mean(er_state_evolution[12][t1:]) * self.tag['E12E2']
        sim_stats['green13_2_avg_pop'] = np.mean(er_state_evolution[13][t1:]) * self.tag['E13E2']
        sim_stats['green14_2_avg_pop'] = np.mean(er_state_evolution[14][t1:]) * self.tag['E14E2']
        sim_stats['green15_3_avg_pop'] = np.mean(er_state_evolution[15][t1:]) * self.tag['E15E3']

        sim_stats['green_avg_pop'] = sim_stats['green50_avg_pop'] + sim_stats['green60_avg_pop'] + sim_stats['green10_1_avg_pop'] + sim_stats['green11_1_avg_pop'] + sim_stats['green12_2_avg_pop'] + sim_stats['green13_2_avg_pop'] + sim_stats['green14_2_avg_pop'] + sim_stats['green15_3_avg_pop']
    

        sim_stats['red_green_ratio_pop'] = sim_stats['red_avg_pop'] / sim_stats['green_avg_pop']
        sim_stats['red_green_total_avg_pop'] = sim_stats['red_avg_pop'] + sim_stats['green_avg_pop']


        sim_stats['yb_upconversions'] = yb_upconversions
        sim_stats['yb_ybs'] = yb_ybs
        sim_stats['yb_excites'] = yb_excites
        sim_stats['er_decays'] = er_decays
        sim_stats['er_upconversions'] = er_upconversions
        sim_stats['er_crossrelaxations'] = er_crossrelaxations
        sim_stats['er_excite_02s'] = er_excite_02s
        sim_stats['er_excite_27s'] = er_excite_27s

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

        

