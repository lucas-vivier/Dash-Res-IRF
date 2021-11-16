import pandas as pd
import os, sys
import json


from utils import reverse_nested_dict

sys.path.append(os.path.dirname(__file__))

folder_data = os.path.join(os.path.dirname(__file__), 'data', 'scenarios')
folder_assets = os.path.join(os.path.dirname(__file__), 'assets')


with open(os.path.join(folder_assets, 'colors.json')) as f:
    colors_attributes = json.load(f)


scenarios = [f for f in os.listdir(folder_data) if f not in ['log.txt', '.DS_Store', 'img']]
folders = {scenario: os.path.join(folder_data, scenario) for scenario in scenarios}

detailed = {
    scenario.replace('_', ' '): pd.read_csv(os.path.join(folders[scenario], 'detailed.csv'), index_col=[0]).T for
    scenario in
    scenarios}
detailed = reverse_nested_dict(detailed)
detailed = {key: pd.DataFrame(item) for key, item in detailed.items()}


stock = {
    scenario.replace('_', ' '): pd.read_csv(os.path.join(folders[scenario], 'stock.csv'), index_col=[0, 1, 2, 3, 4, 5])
    for scenario in scenarios}


scenarios = [scenario.replace('_', ' ') for scenario in scenarios]

order = {
    'Energy performance': ['G', 'F', 'E', 'D', 'C', 'B', 'A', 'BBC', 'BEPOS'],
    'Housing type': ['Single-family', 'Multi-family'],
    'Occupancy status': ['Homeowners', 'Landlords', 'Social-housing'],
    'Income class': ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10'],
    'Income class owner': ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10'],
    'Heating energy': ['Power', 'Natural gas', 'Oil fuel', 'Wood fuel']
}

color_policies = {
    'Cee taxes (euro)': 'lightcoral',
    'Carbon tax (euro)': 'black',
    'Cee subsidy (euro)': 'lightcoral',
    'Eptz subsidy (euro)': 'darkolivegreen',
    'Reduced tax (euro)': 'green',
    'Cite (euro)': 'red'
}

subsidies = {subsidy: detailed[subsidy] for subsidy in color_policies.keys()}
subsidies = reverse_nested_dict(subsidies)
subsidies = {key: pd.DataFrame(item) for key, item in subsidies.items()}


scenarios_table = pd.read_csv(os.path.join(folder_assets, 'scenario.csv'), index_col=None, header=[0]).dropna()
