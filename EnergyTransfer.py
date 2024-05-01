import numpy as np

def get_constants():
   
   s0=0.00014
   beta = 2*10**-3
   constant = 843091
   E_phonon=450
   threshold = 10**-42
   n=10

   Tm_RME={'E1E0':[0.527, 0.718, 0.228],
         'E2E1':[0.011, 0.48, 0.004],'E2E0':[0.107, 0.231, 0.638],
         'E3E2':[0.089, 0.125, 0.905],'E3E1':[0.129, 0.133, 0.213],'E3E0':[0.249, 0.118, 0.608],
         'E4E3':[0.002, 0.0005, 0.167],'E4E2':[0.629, 0.347, 0],'E4E1':[0.081, 0.344, 0.264],'E4E0':[0, 0.316, 0.841],
         'E5E4':[0.004, 0.075, 0],'E5E3':[0.311, 0.056, 0.044],'E5E2':[0, 0.29, 0.583],'E5E1':[0.287, 0.163, 0.074],'E5E0':[0, 0.0005, 0.258],
         'E6E5':[0.006, 0.0717, 0.0417],'E6E4':[0.0105, 0.0733, 0.3056],'E6E3':[0.0034, 0.0194, 0.0718],'E6E2':[0.0738, 0.0059, 0.5423],'E6E1':[0.1583, 0.0042, 0.3783],'E6E0':[0.0481, 0.0752, 0.0119],
         'E7E6':[0.1905, 0.1722, 0.0009],'E7E5':[0.0647, 0.3055, 0],'E7E4':[0.1607, 0.0680, 0],'E7E3':[0.5631, 0.0935, 0.0225],'E7E2':[0, 0.0011, 0.0185],'E7E1':[0.1240, 0.0116, 0.2266],'E7E0':[0, 0.3079, 0.0926],
         'E8E7':[0.0253, 0, 0],'E8E6':[0, 0.0525, 0],'E8E5':[0.3543, 0, 0],'E8E4':[0, 0, 0],'E8E3':[0, 0.2715, 0],'E8E2':[0, 0, 0],'E8E1':[0, 0.0204, 0],'E8E0':[0, 0, 0.0757],
         'E9E8':[0, 0, 0.0190],'E9E7':[0, 0.0520, 0.8448],'E9E6':[0.2128, 1.2488, 0.6302],'E9E5':[0, 0.0410, 0.3545],'E9E4':[0, 0.0028, 0.0074],'E9E3':[0.0622, 0.5013, 0.3921],'E9E2':[0.0010, 0.0021, 0.0056],'E9E1':[0.0669, 0.3112, 0.0992],'E9E0':[0.0107, 0.0392, 0.0136],
         'E10E9':[0, 0, 0.0011],'E10E8':[0, 0, 0],'E10E7':[0.4444, 0, 0],'E10E6':[0, 0.0050, 0],'E10E5':[0.1370, 0, 0],'E10E4':[0.5714, 0.1964, 0],'E10E3':[0, 0.1074, 0],'E10E2':[0, 0.2857, 0.0893],'E10E1':[0, 0.4055, 0],'E10E0':[0, 0, 0.1239],
         'E11E10':[0.1822, 0, 0],'E11E9':[0, 0.0981, 0.6808],'E11E8':[0.1247, 0, 0],'E11E7':[0.0004, 0.1560, 0],'E11E6':[0.5964, 0.0009, 0.1055],'E11E5':[0.0045, 0.0433, 0],'E11E4':[0.1445, 0.2343, 0],'E11E3':[0.1359, 0.0858, 0.00002],'E11E2':[0, 0.1979, 0.1895],'E11E1':[0.2811, 0.0096, 0.0064],'E11E0':[0, 0.2713, 0.0228]
         }

   Er_RME={ 'E1E0':[0.0195, 0.1173, 1.4316],
         'E2E1':[0.0331, 0.1708, 1.0864],'E2E0':[0.0282, 0.0003, 0.3953],
         'E3E2':[0.0030, 0.0674, 0.1271],'E3E1':[0.0004, 0.0106, 0.7162],'E3E0':[0, 0.1732, 0.0099],
         'E4E3':[0.1279, 0.0059, 0.0281],'E4E2':[0.0704, 0.0112, 1.2839],'E4E1':[0.0101, 0.1533, 0.0714],'E4E0':[0, 0.5354, 0.4619],
         'E5E4':[0, 0.0003, 0.0264],'E5E3':[0, 0.0788, 0.2542],'E5E2':[0, 0.0042, 0.0739],'E5E1':[0, 0, 0.3462],'E5E0':[0, 0, 0.2211],
         'E6E5':[0, 0.1988, 0.0101],'E6E4':[0.3629, 0.0224, 0.0022],'E6E3':[0.2077, 0.0662, 0.2858],'E6E2':[0.0357, 0.1382, 0.0371],'E6E1':[0.0230, 0.0611, 0.0527],'E6E0':[0.7125, 0.4123, 0.0925],
         'E7E6':[0.1229, 0.0153, 0.4017],'E7E5':[0.0001, 0.0058, 0],'E7E4':[0.0121, 0.0342, 0.0151],'E7E3':[0.0163, 0.0954, 0.4277],'E7E2':[0.0035, 0.2648, 0.1515],'E7E1':[0, 0.3371, 0.0001],'E7E0':[0, 0.1468, 0.6266],
         }
   
   for key in list(Tm_RME.keys()):
      parts = key.split('E')
      new_key = f'E{parts[2]}E{parts[1]}'
      if new_key not in Tm_RME:
         Tm_RME[new_key] = Tm_RME[key]
   for key in list(Er_RME.keys()):
      parts = key.split('E')
      new_key = f'E{parts[2]}E{parts[1]}'
      if new_key not in Er_RME:
         Er_RME[new_key] = Er_RME[key]

   Tm_energy = {'E0':153, 'E1': 5828, 'E2': 8396, 'E3':12735, 'E4':14598, 'E5':15180, 'E6': 21352, 'E7':28028, 'E8': 34900, 'E9': 35500, 'E10': 36400, 'E11': 38250}
   Er_energy = {'E0':0, 'E1': 6632, 'E2': 10230, 'E3':12553, 'E4':15306, 'E5':18448, 'E6': 19246, 'E7':20497}
   Yb_energy = {'S0':0, 'S1': 10246}

   Tm_g={'E0':13, 'E1':9, 'E2':11, 'E3':9, 'E4':7, 'E5': 5, 'E6': 9, 'E7': 5, 'E8': 1, 'E9': 13, 'E10': 3, 'E11': 5}
   Er_g = {'E0':16, 'E1':14, 'E2':12, 'E3':10, 'E4': 10, 'E5': 4, 'E6': 12, 'E7': 8}
   Yb_g={'S1':6}

   Tm_Omega={'2':2.04*10**-20, '4':2.01*10**-20, '6':1.44*10**-20}
   Er_Omega={'2':2.11*10**-20, '4':1.37*10**-20, '6':1.22*10**-20}

   return s0, beta, constant, E_phonon, threshold, Tm_RME, Er_RME, Tm_energy, Er_energy, Yb_energy, Tm_g, Er_g, Yb_g, Tm_Omega, Er_Omega, n



class EnergyTransfer():
   def total_probability(self, r):
      pass

   def select_path(self, r):
      pass

   def add_state(self, ion12, ion22, rate):
      pass




class UpConversion(EnergyTransfer):
   def __init__ (self, ion2):
      self.ion2 = ion2
      self.resulting_states = []

   def total_probability(self, r): # TODO: 要不要在这里乘以10**（-6）
      return sum([result1[2]/(r/10**7)**6 for result1 in self.resulting_states])

   def select_path(self, r):
      if len(self.resulting_states) == 0 :
         return None
      
      results = [result1[2]/r**6 for result1 in self.resulting_states]
      results = [prob / sum(results) for prob in results]

      new_state = np.random.choice([i for i in range(len(self.resulting_states))], p=results)
      return self.resulting_states[new_state][0:2]
   
   def add_state(self, ion12, ion22, rate):
      self.resulting_states.append((ion12, ion22, rate))



def up_conversion():

   s0, beta, constant, E_phonon, threshold, Tm_RME, Er_RME, Tm_energy, Er_energy, Yb_energy, Tm_g, Er_g, Yb_g, Tm_Omega, Er_Omega, n = get_constants()

   ion1_energy = 'S1'
   E_level = Er_energy
   RME_value = Er_RME
   g_value = Er_g
   Omega_value = Er_Omega
   
   ret = {}
   for ion2_energy in Er_energy:
      ion2_et = UpConversion(int(ion2_energy[1:]))

      all_transitions = {}
      delta_E_ion1 = {'S1S0': 10246}
      delta_E_ion2 = {f'{ion2_energy}{level}':  E_level[ion2_energy] -  E_level[level] for level in E_level if level != ion2_energy}
   
      for transition2, energy_diff2 in delta_E_ion2.items():

         ################################################################# important: ET matching condition
         if (energy_diff2 < 0 and abs(10246 + energy_diff2)< n*E_phonon):
            Delta_E = abs(10246 + energy_diff2)
            key = f'S1S0-{transition2}'
            all_transitions[key] = Delta_E
         
      for ET_key in all_transitions:
            first_part, second_part = ET_key.split('-')
            second_values = RME_value[second_part]
            all_transitions[ET_key] = [all_transitions[ET_key], 2*10**-20, second_values]
            parts = second_part.split('E')
            new_key = f'E{parts[1]}'
            all_transitions[ET_key].append([Yb_g[ion1_energy], g_value[new_key]])
      

      for key, value in all_transitions.items():

         S1 = value[1]
         S2 = Omega_value['2']*value[2][0]+Omega_value['4']*value[2][1]+Omega_value['6']*value[2][2]

         my_value = constant*s0*(S1*S2)*np.exp(-beta*value[0])/(value[3][0]*value[3][1])

         if (my_value > threshold):
            
            donor_transition, acceptor_transition = key.split('-')
            donor_parts = donor_transition.split('E')
            donor_final_state = int(donor_parts[1])
            acceptor_parts = acceptor_transition.split('E')
            acceptor_final_state = int(acceptor_parts[2])

            ion2_et.add_state(donor_final_state, acceptor_final_state, my_value)
            # ion2_et.add_state(0, int(key[-1]), my_value)

      

      ret[int(ion2_energy[1:])] = ion2_et

      
   return ret



class CrossRelaxation(EnergyTransfer):
   def __init__ (self, ion1, ion2):
      self.ion1 = ion1
      self.ion2 = ion2
      self.resulting_states = []

   def total_probability(self, r):
      return sum([result1[2]/r**6 for result1 in self.resulting_states])

   def select_path(self, r):
      if len(self.resulting_states) == 0 :
         return None
      
      results = [result1[2]/(r/10**7)**6 for result1 in self.resulting_states]
      results = [prob / sum(results) for prob in results]
      # print(self.resulting_states, total_prob, results)
      new_state = np.random.choice([i for i in range(len(self.resulting_states))], p=results)
      return self.resulting_states[new_state][0:2]
   
   def add_state(self, ion12, ion22, rate):
      self.resulting_states.append((ion12, ion22, rate))



def cross_relaxation():

   s0, beta, constant, E_phonon, threshold, Tm_RME, Er_RME, Tm_energy, Er_energy, Yb_energy, Tm_g, Er_g, Yb_g, Tm_Omega, Er_Omega, n = get_constants()

   energy_levels = Er_energy
   RME_value = Er_RME
   g_value = Er_g # deneracy
   Omega_value = Er_Omega

   ret = {}

   for ion1_energy in Er_energy:
      ion1_ets = {}
      for ion2_energy in Er_energy:
         ion1_ion2_et = CrossRelaxation(int(ion1_energy[1]), int(ion2_energy[1]))

         all_transitions = {}
         delta_E_ion1 = {f'{ion1_energy}{level}':  energy_levels[ion1_energy] -  energy_levels[level] for level in energy_levels if level != ion1_energy}
         delta_E_ion2 = {f'{ion2_energy}{level}': energy_levels[ion2_energy] - energy_levels[level] for level in energy_levels if level != ion2_energy}

         for transition1, energy_diff1 in delta_E_ion1.items():
            for transition2, energy_diff2 in delta_E_ion2.items():

               ################################################################# important: ET matching condition
               if (energy_diff1 > 0 and energy_diff2 < 0 and abs(energy_diff1+energy_diff2)< n*E_phonon) or (energy_diff1 < 0 and energy_diff2 > 0 and abs(energy_diff2+energy_diff1)< n*E_phonon):
                  
                  Delta_E = abs(energy_diff1 + energy_diff2)
                  key=f'{transition1}-{transition2}'
                  all_transitions[key]=Delta_E

         for ET_key in all_transitions:
            first_part, second_part = ET_key.split('-')
            
            # Oscillator strength: S (Emory)
            first_values = RME_value.get(first_part, [])
            second_values = RME_value.get(second_part, [])

            if first_values and second_values:

                  all_transitions[ET_key] = [all_transitions[ET_key], first_values, second_values]

            parts = first_part.split('E')
            new_key1 = f'E{parts[1]}'

            parts = second_part.split('E')
            new_key2 = f'E{parts[1]}'

            # append degeneracy of initial level of donor and acceptor
            all_transitions[ET_key].append([g_value[new_key1], g_value[new_key2]])

         for key, value in all_transitions.items():
            S1 = Omega_value['2']*value[1][0]+Omega_value['4']*value[1][1]+Omega_value['6']*value[1][2]
            S2 = Omega_value['2']*value[2][0]+Omega_value['4']*value[2][1]+Omega_value['6']*value[2][2]

            my_value = constant*s0*(S1*S2)*np.exp(-beta*value[0])/(value[3][0]*value[3][1])

            if (my_value > threshold):
               
               donor_transition, acceptor_transition = key.split('-')
               donor_parts = donor_transition.split('E')
               donor_final_state = int(donor_parts[1])
               acceptor_parts = acceptor_transition.split('E')
               acceptor_final_state = int(acceptor_parts[2])

               ion1_ion2_et.add_state(donor_final_state, acceptor_final_state, my_value)
               # ion1_ion2_et.add_state(int(key[3]), int(key[-1]), my_value)

         parts_ion2 = ion2_energy.split('E')
         ion2_initial_state = int(parts_ion2[1])
         ion1_ets[ion2_initial_state] = ion1_ion2_et
         # ion1_ets[int(ion2_energy[1])] = ion1_ion2_et


      parts_ion1 = ion1_energy.split('E')
      ion1_initial_state = int(parts_ion1[1])
      ret[ion1_initial_state] = ion1_ets
      #ret[int(ion1_energy[1])] = ion1_ets

      
   return ret

