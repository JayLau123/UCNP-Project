# use pickle module to save the results as a pickle file and reload them later
# The / character cannot be used in file names because it is reserved as a directory separator, replace / with underscores _ or using another safe delimiter.


import pickle
from datetime import datetime
import os
import plotly.graph_objects as go
import nbformat as nbf


class PickleSaver:

    def __init__(self, base_name='Mydata', folder='Chuanyu_data_files'):
     
        self.base_name = base_name
        self.folder = folder


        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    def save_data(self, data):
      

        current_date = datetime.now().strftime('%m_%d_%Y')
        base_filename = f'{self.base_name}_{current_date}'
        
        index = 1
        filename = os.path.join(self.folder, f'{base_filename}_{index}.pkl')
        while os.path.exists(filename):
            index += 1
            filename = os.path.join(self.folder, f'{base_filename}_{index}.pkl')


        with open(filename, 'wb') as f:
            pickle.dump(data, f)

        print(f"Data has been successfully saved to '{filename}'")
        print()


    def load_all_data(self):
        
        if not os.path.exists(self.folder):
            print(f"Folder '{self.folder}' does not exist.")
            return {}

        files = [f for f in os.listdir(self.folder) if f.endswith('.pkl')]
        all_data = {}

        for file in sorted(files):
            filepath = os.path.join(self.folder, file)
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
                all_data[file] = data

        print(f'Filename = {file}')

        KEY1=[]
        KEY2=[]

        for key1, value1 in data.items():
            KEY1.append(key1)
        print(f'\nAll percentages = {KEY1}')

        for key1, value1 in data.items():
            for key2, value2 in value1.items():
                KEY2.append(key2)
            break
        print(f'\nFor each percentage, all power densities = {KEY2}')

        # use a set to keep track of unique third keys
        unique_third_keys = set()

        print('\nFor each combination of Percentage+Power density, the accessible data: ')
        print()
        for key1, value1 in data.items():
            for key2, value2 in value1.items():
                for key3 in value2.keys():
                    if key3 not in unique_third_keys:
                        unique_third_keys.add(key3)
                        print(f'key3 = {key3}, value3 = {value2[key3]}')
