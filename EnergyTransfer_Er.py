import numpy as np
from Er_inf import *
from Er_adjustable_parameter import *

ET_n_term = ((n**2+2) / (3*n) )**4

# double the RME dictionary
for key in list(Er_RME.keys()):
   parts = key.split('E')
   new_key = f'E{parts[2]}E{parts[1]}'
   if new_key not in Er_RME:
      Er_RME[new_key] = Er_RME[key]


# degeneracy of energy level

Er_g= {}
for key in Er_energy.keys():

   key_symbol= key[key.find('(') + 1:-1] # 4I_15_2
   J = int(key_symbol[key_symbol.find('_')+1:-2]) / int(key_symbol[-1])
   g = 2*J+1
   simplified_key = key[0 : key.find('(')]

   Er_g[simplified_key] = g

   # like this
   # Er_g = {'E0':16, 'E1':14, 'E2':12, 'E3':10, 'E4': 10, 'E5': 4, 'E6': 12, 'E7': 8, 'E8': 6, 'E9': 4, 'E10': 10, 'E11': 12, 'E12': 10, 'E13': 16, 'E14': 8, 'E15': 4}   
   

Er_energy_simplified = {}
for key, value in Er_energy.items():

   simplified_key = key[0 : key.find('(')]
   Er_energy_simplified[simplified_key] = value

# like this:
# Er_energy = {'E0':0, 'E1': 6632, 'E2': 10230, 'E3':12553, 'E4':15306, 'E5':18448, 'E6': 19246, 'E7':20497, 'E8':22282, 'E9':22677, 'E10':24475,
#              'E11':26376, 'E12':27319, 'E13':27584, 'E14':27825, 'E15':31414}




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


   ion1_energy = 'S1'
   E_level = Er_energy_simplified
   RME_value = Er_RME
   g_value = Er_g
   Omega_value = Er_omega
   
   ret = {}
   for ion2_energy in Er_energy_simplified:

      ion2_parts = ion2_energy.split('E')
      ion2_initial_state = int(ion2_parts[1])
      ion2_et = UpConversion(ion2_initial_state)

      all_transitions = {}
      delta_E_ion1 = {'S1S0': 10246}
      delta_E_ion2 = {f'{ion2_energy}{level}':  E_level[ion2_energy] -  E_level[level] for level in E_level if level != ion2_energy}
   
      for transition2, energy_diff2 in delta_E_ion2.items():

         ################################################################# important: ET matching condition
         if (energy_diff2 < 0 and abs(10246 + energy_diff2)< n_phonon * E_phonon):
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


         ########################## ET formulation

         my_value = ET_constant*ET_n_term*s0*(S1*S2)*np.exp(-beta*value[0])/(value[3][0]*value[3][1])

         if (my_value > threshold):
            
            donor_transition, acceptor_transition = key.split('-')
            donor_parts = donor_transition.split('S')
            donor_final_state = int(donor_parts[2])
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
      return sum([result1[2]/(r/10**7)**6 for result1 in self.resulting_states])

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


   energy_levels = Er_energy_simplified
   RME_value = Er_RME
   g_value = Er_g # deneracy
   Omega_value = Er_omega

   ret = {}

   for ion1_energy in Er_energy_simplified:
      ion1_ets = {}

      donor_parts = ion1_energy.split('E')
      donor_initial_state=int(donor_parts[1])


      for ion2_energy in Er_energy_simplified:

         acceptor_parts = ion2_energy.split('E')
         acceptor_initial_state=int(acceptor_parts[1])

         ion1_ion2_et = CrossRelaxation(donor_initial_state, acceptor_initial_state)

         all_transitions = {}
         delta_E_ion1 = {f'{ion1_energy}{level}':  energy_levels[ion1_energy] -  energy_levels[level] for level in energy_levels if level != ion1_energy}
         delta_E_ion2 = {f'{ion2_energy}{level}': energy_levels[ion2_energy] - energy_levels[level] for level in energy_levels if level != ion2_energy}

         for transition1, energy_diff1 in delta_E_ion1.items():
            for transition2, energy_diff2 in delta_E_ion2.items():

               ################################################################# important: ET matching condition
               if (energy_diff1 > 0 and energy_diff2 < 0 and abs(energy_diff1+energy_diff2)< n_phonon * E_phonon) or (energy_diff1 < 0 and energy_diff2 > 0 and abs(energy_diff2+energy_diff1)< n_phonon*E_phonon):
                  
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

            ########################## ET formulation
            my_value = ET_constant*ET_n_term*s0*(S1*S2)*np.exp(-beta*value[0])/(value[3][0]*value[3][1])

            if (my_value > threshold):
               
               donor_transition, acceptor_transition = key.split('-')
               donor_parts = donor_transition.split('E')
               donor_final_state = int(donor_parts[2])
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

