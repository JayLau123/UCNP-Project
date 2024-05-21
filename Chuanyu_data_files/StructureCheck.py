# use pickle module to save the results as a pickle file and reload them later
# The / character cannot be used in file names because it is reserved as a directory separator, replace / with underscores _ or using another safe delimiter.


import os
import pickle

class PickleSaver:
    def __init__(self, data):
        self.data = data

    def load_all_data(self):
        data = self.data
        KEY1 = []
        KEY2 = []

        for key1 in data:
            KEY1.append(key1)
        print(f'\nAll percentages = {KEY1}')

        for value1 in data.values():
            for key2 in value1:
                KEY2.append(key2)
            break  # To avoid repetition, break after the first complete iteration
        print(f'\nFor each percentage, all power densities = {KEY2}')

        unique_third_keys = set()
        print('\nFor each combination of Percentage+Power density, the accessible data:')
        for value1 in data.values():
            for value2 in value1.values():
                for key3, value3 in value2.items():
                    if key3 not in unique_third_keys:
                        unique_third_keys.add(key3)
                        print(f'key3 = {key3}, value3 = {value3}')