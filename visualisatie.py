"""
This script visualizes the data obtained from the algorithms
"""

import csv
import pandas as pd
import matplotlib.pylot as plt

# def load_houses(filename):
#     """
#     Load csv data into panda
#     """

#     # Load the necessary columns from the csv into panda
#     house = pd.read_csv(filename)

#     # Cleans the data
#     house = house[['x', 'y', 'max.output']]
#     house['x'] = pd.to_numeric(data['x'])
#     house['y'] = pd.to_numeric(data['y'])
#     house['max.output'] = pd.to_float(data['max.output'])


def load_results(filename):
    """
    Inputs a csv data into panda
    """
    # Load the necessary columns from the csv into panda
    data = pd.read_csv(filename)

    # Cleans the data
    data = data[['Run', 'Total Distance', 'Costs Grid', 'Costs Batteries', 'Total Costs']]
    data['Runs'] = pd.to_numeric(data['Run'])
    data['Total Distance'] = pd.to_numeric(data['Total Distance'])
    data['Costs Grid'] = pd.to_numeric(data['Costs Grid'])
    data['Costs Batteries'] = pd.to_numeric(data['Costs Batteries'])
    data['Total Costs'] = pd.to_numeric(data['Total Costs'])

    return data

def plot_scatter(runs, costs):
    """
    Plots a scatterplot of the inserted data
    """
    # Forms the scatterplot
    plt.scatter(runs, costs)

    # Adds a title and axis names
    plt.title('Costs change in runs', fontweight='bold')
    plt.xlabel('Runs')
    plt.ylabel('Costs')
    plt.ylim(2000, 6000)
    plt.grid(True)
    
    # Actually shows the scatterplot
    plt.show()

def plot_line(runs, costs):
    """
    plots a histogram of the insterted data
    """
    # Forms the histogram
    plt.plot(runs, costs, 'k', runs, costs, 'go')

    # Adds the title and axis names
    plt.title('Costs change in runs', fontweight='bold')
    plt.xlabel('Runs')
    plt.ylabel('Costs')
    plt.ylim(2000, 6000)
    plt.grid(True)

    # Actually shows the histogram
    plt.show

def write_to_csv(self, total_distance, costs_grid, costs_batteries, total_costs):
    """
    Appends result to an existing csv file
    """
    with open('results_greedy_csv', 'a') as infile:
        fields = ['Total Distance', 'Costs Grid', 'Costs Batteries', 'Total Costs']
        writer = csv.writer(infile, fieldnames=fields)
        writer.writeheader() 
        input = [str(total_distance), str(costs_grid), str(costs_batteries), str(total_costs)]
        writer.writerow(input)

# if __name__ == '__main__':
#     data = load_results('CSV FILE')
#     value = data(data['Value'])
#     runs = data(data['Runs'])
#     plot_scatter(value, runs)
#     plot_line(value, runs)