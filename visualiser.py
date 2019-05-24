"""
This script visualizes the data obtained from the algorithms
"""

import csv
import pandas as pd
import matplotlib.pyplot as plt
from house import House
from battery import Battery

import os
import sys

directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "classes"))
sys.path.append(os.path.join(directory, "code", "algorithms"))
sys.path.append(os.path.join(directory, "results", "Fixed_batteries"))
sys.path.append(os.path.join(directory, "data"))

def load_results_bounds(filename):
    """
    Inputs a csv data into panda. Used for the visualisation of the scatterplot
    in the presentation.
    """
    # Load the necessary columns from the csv into panda
    data = pd.read_csv(filename)

    # Cleans the data
    data = data[['Minimum', 'Total_distance']]
    data['Minimum'] = pd.to_numeric(data['Minimum'])
    data['Total_distance'] = pd.to_numeric(data['Total_distance'])
    print(data)
    return data

def plot_scatter(data):
    """
    Plots a scatterplot of the inserted data. Used for the visualisation of the scatterplot
    in the presentation.
    """
    minimum = data[data.columns[0]]
    distance = data[data.columns[1]]

    # Forms the scatterplot
    plt.scatter(minimum, distance)

    # Adds a title and axis names
    plt.title('Minimum vs Total distance', fontweight='bold', fontsize='large')
    plt.xlabel('Minimun Bound', fontsize='large')
    plt.gca().invert_xaxis()
    plt.ylabel('Total Distance', fontsize='large')
    plt.grid(True)

    # Actually shows the scatterplot
    plt.show()

def plot_comparison_GHR(data, data1):
    """
    Definition used for comperison of Hillclimber versus Simulated Annealing from Random.
    Function used for graphs in presentation.
    """
    # Loads the different datasets
    runs = data[data.columns[0]]
    distance = data[data.columns[1]]

    runs1 = data1[data1.columns[0]]
    distance1 = data1[data1.columns[1]]

     # Forms the histogram
    plt.plot(runs, distance, label="Simulated Annealing")
    plt.plot(runs1, distance1, color = 'orange', label="Hillclimber")

def load_results_runs(filename):
    """
    Inputs a csv data from the iterations or runs into panda
    """
    # Load the necessary columns from the csv into panda
    data = pd.read_csv(filename)

    # Cleans the data
    data = data[['Run', 'Total Distance']]
    data['Run'] = pd.to_numeric(data['Run'])
    data['Total Distance'] = pd.to_numeric(data['Total Distance'])

    return data    

def plot_line(data, algorithm):
    """
    plots a histogram of the insterted data
    """
    runs = data[data.columns[0]]
    distance = data[data.columns[1]]

    # Forms the histogram
    plt.plot(runs, distance)
    plt.legend(loc='upper right')

    # Adds the title and axis names
    if algorithm == "random":
        plt.title('Random Algorithm')
        plt.xlabel('Runs')
        plt.ylabel('Total Distance')

    if algorithm == "greedy_hillclimber":
        plt.title('Greedy Hillclimber Algorithm')
        plt.xlabel('Iterations')
        plt.ylabel('Total Distance')

    if algorithm == "simulated_annealing":
        plt.title('Simulated Annealing')
        plt.xlabel('Iterations')
        plt.ylabel('Total Distance')
    
    if algorithm == "hillclimber":
        plt.title('Hillclimber on a random solution')
        plt.xlabel('Iterations')
        plt.ylabel('Total Distance')

    plt.xlim(0, len(runs))
    plt.ylim((min(distance) - 10), (max(distance) + 10))

    # Shows Grid
    plt.grid(True)

    # Actually shows the histogram
    plt.show()

def plot_comparison(data, data1, data2, algorithm):
    """
    Plots a comparison of the seperate neighbourhoods.
    Used for graphs in the presentation.
    """
    # Loads the different datasets
    runs = data[data.columns[0]]
    distance = data[data.columns[1]]

    runs1 = data1[data1.columns[0]]
    distance1 = data1[data1.columns[1]]

    runs2 = data2[data2.columns[0]]
    distance2 = data2[data2.columns[1]]

    # Forms the histogram
    plt.plot(runs, distance, label="Wijk 1")
    plt.plot(runs1, distance1, color = 'orange', label="Wijk 2")
    plt.plot(runs2, distance2, color = 'red', label="Wijk 3")
    plt.legend(loc='upper right')

    # Plots the legend
    plt.legend(loc='upper right')

    # Adds the title and axis names
    plt.title(f"{algorithm} Algorithm", fontweight='bold')
    plt.xlabel('Iterations')
    plt.ylabel('Total Distance')

    # Actually shows the histogram
    plt.show()

def dict_to_csv(total_distance, algorithm):
    """
    Appends result to an csv file
    """
    # Creates or overwrites new csv from dict
    with open(f'results/visualisatie/results_{algorithm}_distance.csv', 'w', newline='') as infile:
        fields = ['Run', 'Total Distance']
        writer = csv.DictWriter(infile, fieldnames=fields)
        writer.writeheader()

        writer = csv.writer(infile, delimiter=',')
        input = total_distance
        for key, value in input.items():
            writer.writerow([key, value])

