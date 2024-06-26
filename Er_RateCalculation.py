
print('Successfully import:') 
print()
print('ED_cal(energy_dict, omega, RME_square, n)') 
print('MD_cal(energy_dict, n)') 
print('MPR_cal(energy_dict, W0, alpha, phonon)')
print()



def ED_cal(energy_dict, omega, RME_square, n):

    keys = list(energy_dict.keys())
    energy_gaps = {}

    for i in range(len(keys)):
        for j in range(i+1, len(keys)):

            
            start_level = keys[j]
            end_level = keys[i]

            start_symbol= start_level[start_level.find('(') + 1:-1] # 3F4
            
            J = int(start_symbol[start_symbol.find('_')+1:-2]) / int(start_symbol[-1])

            start_E = start_level[0 : start_level.find('(')] # E1
            end_E = end_level[0 : end_level.find('(')] # E0
            key =  start_E + end_E # E1E0
            energy_gaps[key] = (energy_dict[start_level] - energy_dict[end_level], J)


    n_term = (n*(n**2+2)**2)/9

    ED_constant = (64*3.14**4*(4.8*10**-10)**2)/(3*6.6261*10**-27)

    dic_ED={}

    for key in RME_square:

        S=omega['2']*RME_square[key][0]+omega['4']*RME_square[key][1]+omega['6']*RME_square[key][2]
        dic_ED[key] = ED_constant * (energy_gaps[key][0]**3 / (2*energy_gaps[key][1]+1) ) * n_term * S

    return dic_ED



def MD_cal(energy_dict, n):

    """Find and print pairs of energy levels from energy_dict based on specific symbol criteria."""

    def extract_symbol(energy_str):
        """Extracts the symbol part from strings like 'E0(3H6)'."""
        return energy_str[energy_str.find('(') + 1:-1]

    def compare_symbols(symbol1, symbol2):
        """Compare two symbols according to specified criteria."""

        number1 = int(symbol1[symbol1.find('_')+1:-2])
        number2 = int(symbol2[symbol2.find('_')+1:-2])


        return (symbol1[0] == symbol2[0] and 
                symbol1[1] == symbol2[1] and 
                abs( number1 - number2 ) == 2)

    pairs = []
    keys = list(energy_dict.keys())

    for i in range(len(keys)):

        key1, value1 = keys[i], energy_dict[keys[i]]

        symbol1 = extract_symbol(key1)

        for j in range(i + 1, len(keys)):

            key2, value2 = keys[j], energy_dict[keys[j]]

            symbol2 = extract_symbol(key2)

            if compare_symbols(symbol1, symbol2):
                
                pair = sorted([(key1, value1), (key2, value2)], key=lambda x: x[1])
                pairs.append(pair)
    

    # print(pairs)
    # calculate the MD rates
    
    MD_constant = (4*(6.626*10**-27)*(3.14**2)*(4.8*10**-10)**2*(n**3)) / (3*(9.11*10**-28)**2*(3*10**10)**2)

    L_QN = {'S':0, 'P':1, 'D':2, 'F':3, 'G':4, 'H':5, 'I':6, 'K':7, 'L':8, 'M':9, 'N':10, 'O':11, 'Q':12, 'R':13, 'T': 14, 'U': 15, 'V': 16}

    dic_MD = {}
    
    for i in pairs:

        end_level = i[0][0]
        start_level = i[1][0]

        start_E = start_level[0 : start_level.find('(')] # E1
        end_E = end_level[0 : end_level.find('(')] # E0
        key =  start_E + end_E # E1E0


        
        start_symbol= start_level[start_level.find('(') + 1:-1] # 4I_13_2
        end_symbol= end_level[end_level.find('(') + 1:-1] # 4I_15_2

        start_value = i[1][1]
        end_value = i[0][1]
        delta_v = start_value - end_value

        number1 = int(end_symbol[end_symbol.find('_')+1:-2])
        number2 = int(start_symbol[start_symbol.find('_')+1:-2])

        # J to J+1
        if number1 > number2: 

            # print('J to J+1')

            S =  (int(start_symbol[0])-1)/2
            L =  L_QN[start_symbol[1]]
            J = int(start_symbol[start_symbol.find('_')+1:-2]) / int(start_symbol[-1])

            RME_square = ( (S + L +1)**2 - (J + 1)**2 ) * ( (J + 1)**2 - (L - S)**2 )  / (4 * (J + 1 ))
            value = MD_constant * ( delta_v**3 / (2*J+1) ) * RME_square
            dic_MD[key] = value

        # J+1 to J
        elif number1 < number2:

            # print('J+1 to J')

            S =  (int(start_symbol[0])-1)/2
            L =  L_QN[start_symbol[1]]
            J = int(start_symbol[start_symbol.find('_')+1:-2]) / int(start_symbol[-1])

            RME_square = ( (S + L +1)**2 - ( J )**2 ) * ( ( J )**2 - (L - S)**2 )  / ( 4*J )
            value = MD_constant * ( delta_v**3 / (2*J+1) ) * RME_square
            dic_MD[key] = value

        # J to J
        else:


            S =  (int(start_symbol[0])-1)/2
            L =  L_QN[start_symbol[1]]
            J = int(start_symbol[start_symbol.find('_')+1:-2]) / int(start_symbol[-1])
            
            RME_square = (2*J+1)  / ( 4*J*(J+1) )
            
            value = MD_constant * ( delta_v**3 / (2*J+1) ) * RME_square
            
            dic_MD[key] = value


    return dic_MD


# MPR calculation

import numpy as np

def MPR_cal(energy_dict, W0, alpha, E_phonon):

    # # zero-phonon relaxation rate
    # W0=2*10**7

    # # MPR rate constant
    # alpha=3.5*10**-3

    # # phonon energy
    # phonon=450

    keys = list(energy_dict.keys())
    energy_gaps = {}

    for i in range(1, len(keys)):
            
        start_level = keys[i]
        end_level = keys[i-1]

        start_E = start_level[0 : start_level.find('(')] # E1
        end_E = end_level[0 : end_level.find('(')] # E0
        key =  start_E + end_E # E1E0
        energy_gaps[key] = energy_dict[start_level] - energy_dict[end_level]

    dic_MPR={}

    for key in energy_gaps:

        mpr = W0 * np.exp(-alpha * (energy_gaps[key] - 2*E_phonon))
        dic_MPR[key] = mpr

    return dic_MPR
