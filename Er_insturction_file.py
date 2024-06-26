import os
import nbformat as nbf
from datetime import datetime

def create_instruction_notebook(guide_folder='Chuanyu_data_files', structure_check_file='StructureCheck.py', saturation_plot_file='SaturationCurves.py', optimal_percentage_file='OptimalPercentage.py', population_evolution_file='PopulationEvolution.py'):
    """
    Create a Jupyter Notebook with instructions and code to load data and generate plots.
    
    Parameters:
    - guide_folder (str): Folder where the guide notebook will be saved.
    - saturation_plot_file (str): Path to the Python file containing the SaturationPlot class.
    - optimal_percentage_file (str): Path to the Python file containing the SinglePowerDensityPlot class.
    - population_evolution_file (str): Path to the Python file containing the PopulationEvolutionPlot class.
    """
    # Ensure the guide folder exists
    if not os.path.exists(guide_folder):
        os.makedirs(guide_folder)

    # Generate a unique filename for the notebook
    current_date = datetime.now().strftime('%m_%d_%Y')
    base_filename = f'Guide_{current_date}'
    index = 1
    notebook_path = os.path.join(guide_folder, f'{base_filename}_{index}.ipynb')
    while os.path.exists(notebook_path):
        index += 1
        notebook_path = os.path.join(guide_folder, f'{base_filename}_{index}.ipynb')

    # Ask for instructions to include in the notebook
    instructions = input("Please provide instructions for this dataset: ")

    # Create a new notebook object
    nb = nbf.v4.new_notebook()

    # Add a markdown cell with the provided instructions
    nb.cells.append(nbf.v4.new_markdown_cell(f"# Guide for Dataset - {current_date}_{index}\n\n{instructions}"))

    # Add a code cell for data loading
    nb.cells.append(nbf.v4.new_code_cell(f"""\
import pickle
import os
from datetime import datetime
import plotly.graph_objects as go
import nbformat as nbf
                            


# Load the data

filepath = f'myC_{current_date}_{index}.pkl'
with open(filepath, 'rb') as f:
    data = pickle.load(f)

print("data loaded successfully")

"""))


    # New cell to be added with the comment and data processing
    data_processing_cell = """

# check the percentages and power density

percentages = sorted(data.keys())
power_densities = sorted({k for subdict in data.values() for k in subdict.keys()})
print('Percentages:', percentages)
print('Power Densities:', sorted(power_densities))

    """

    # New cell to be added with the comment and data processing
    data_structure_cell = """

KEY1 = []
KEY2 = []

for key1 in data:
    KEY1.append(key1)
print(f'All percentages = {KEY1}')

for value1 in data.values():
    for key2 in value1:
        KEY2.append(key2)
    break 
print(f'For each percentage, all power densities = {KEY2}')

unique_third_keys = set()
print('For each combination of Percentage+Power density, the accessible data:')
for value1 in data.values():
    for value2 in value1.values():
        for key3, value3 in value2.items():
            if key3 not in unique_third_keys:
                unique_third_keys.add(key3)
                print(f'key3 = {key3}, value3 = {value3}')

    """

    # Append the new processing cell to the notebook
    nb.cells.append(nbf.v4.new_code_cell(data_processing_cell))

    # Append the new processing cell to the notebook
    nb.cells.append(nbf.v4.new_code_cell(data_structure_cell))



    

# Importing and using the SaturationPlot class, SinglePowerDensityPlot class, PopulationEvolutionPlot class
    nb.cells.append(nbf.v4.new_code_cell(f"""\
# Import the SaturationPlot class from the SaturationCurves module
from {os.path.splitext(saturation_plot_file)[0]} import SaturationPlot

# Generate the saturation curves plot
plot = SaturationPlot(data)
plot.generate_plot(output_file='saturation_plot.html')
"""))

    # add 
    nb.cells.append(nbf.v4.new_code_cell(f"""\
# Import the SinglePowerDensityPlot class from the OptimalPercentage module
from {os.path.splitext(optimal_percentage_file)[0]} import SinglePowerDensityPlot


# Provide a list of available power densities
available_power_densities = sorted({{k for subdict in data.values() for k in subdict.keys()}})
print(f'Available power densities: {{available_power_densities}}')

# Prompt the user to select a power density
selected_power_density = float(input(f'Input a power density from the above options: '))

# Generate the single power density plot
single_plot = SinglePowerDensityPlot(data, selected_power_density)
single_plot.generate_plot(output_file='single_power_density_plot.html')
"""))

    # add 
    nb.cells.append(nbf.v4.new_code_cell(f"""\
# Import the PopulationEvolutionPlot class from the PopulationEvolution module
from {os.path.splitext(population_evolution_file)[0]} import PopulationEvolutionPlot

# Provide a list of available percentages

available_percentages = sorted(data.keys())
print(f'Available percentages: {{available_percentages}}')
# Prompt the user to select a percentage
percentage = float(input(f'Input a percentage from the above options: '))

available_power_densities = sorted({{k for k in data[percentage].keys()}})
print(f'Available power densities for percentage {{percentage}}: {{available_power_densities}}')
# Prompt the user to select a power density
power_density = float(input(f'Input a power density from the above options: '))


# Generate the population evolution plot
pop_plot = PopulationEvolutionPlot(data, percentage, power_density)
pop_plot.generate_plot(output_file='population_evolution_plot.html')
"""))

    # Write the notebook to the file
    with open(notebook_path, 'w') as f:
        nbf.write(nb, f)

    print(f"Instruction notebook has been successfully saved to '{notebook_path}'")
    print()


    
