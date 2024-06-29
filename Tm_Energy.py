print('Successfully import: ')
print()
print('sorted_wavelength(energy_dict)')
print('find_ED_transition(energy_dict)') 
print('find_MD_transition(energy_dict)')
print()

import numpy as np


def sorted_wavelength(energy_dict):
    keys = list(energy_dict.keys())
    energy_gaps = {}
    for i in range(len(keys)):
        for j in range(i+1, len(keys)):
            key_gap = f"{keys[j]}{keys[i]}"
            energy_gaps[key_gap] = energy_dict[keys[j]] - energy_dict[keys[i]]

    wavelength={}

    for key, value in energy_gaps.items():
        wavelength[key]=round((10**7)/value)

    sorted_wavelength = dict(sorted(wavelength.items(), key=lambda item: item[1]))

    return sorted_wavelength


def find_ED_transition(energy_dict):
    keys = list(energy_dict.keys())
    energy_gaps = {}
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            key_gap = f"{keys[j]}{keys[i]}"
            energy_gaps[key_gap] = energy_dict[keys[j]] - energy_dict[keys[i]]

    wavelength = {}
    for key, value in energy_gaps.items():
        wavelength[key] = round((10**7) / value)  # Convert energy gaps to wavelengths

    sorted_wavelength = dict(sorted(wavelength.items(), key=lambda item: item[1]))

    num_colors = int(input("How many types of colors are you interested in? "))
    color_transitions = {}

    for i in range(1, num_colors + 1):
        color_name = input(f"Enter the name for type-{i} color (e.g., blue, red, green, etc ): ")
        lower_bound = float(input(f"Enter the lower bound for type-{i} color (nm): "))
        upper_bound = float(input(f"Enter the upper bound for type-{i} color (nm): "))

        # Filter transitions within the specified range
        filtered_transitions = {k: v for k, v in sorted_wavelength.items() if lower_bound < v < upper_bound}
        
        # Organize transitions under the selected color
        color_transitions[color_name] = filtered_transitions
        
        # Print details about the filtered transitions
        print(f"\nFor {color_name} ({lower_bound} nm to {upper_bound} nm):")
        print(f"Number of selected transitions: {len(filtered_transitions)}")

        # for transition, wavelength in filtered_transitions.items():
        #     print(f"{transition}: {wavelength} nm")

    return color_transitions


def find_MD_transition(energy_dict):
    """Find and print pairs of energy levels from energy_dict based on specific symbol criteria."""

    def extract_symbol(energy_str):
        """Extracts the symbol part from strings like 'E0(3H6)'."""
        return energy_str[energy_str.find('(') + 1:-1]

    def compare_symbols(symbol1, symbol2):
        """Compare two symbols according to specified criteria."""
        return (symbol1[0] == symbol2[0] and 
                symbol1[1] == symbol2[1] and 
                abs(int(symbol1[2]) - int(symbol2[2])) == 1)

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
    
    return pairs


