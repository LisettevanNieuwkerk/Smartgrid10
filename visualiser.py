"""
This script visualizes the data obtained from the algorithms
"""

import csv
import pandas as pd
import matplotlib.pyplot as plt
from house import House
from battery import Battery

import os, sys
directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "classes"))
sys.path.append(os.path.join(directory, "code", "algorithms"))
sys.path.append(os.path.join(directory, "results", "Fixed_batteries"))
sys.path.append(os.path.join(directory, "data"))

def load_houses(cor_file):
    """
    Load csv data into pandas
    """
    # Load the necessary columns from the csv into panda
    house = pd.read_csv(cor_file)

    # Cleans the data --> need to change x_value to x
    house = house[['x', 'y', 'max. output']]
    house['x'] = pd.to_numeric(house['x'])
    house['y'] = pd.to_numeric(house['y'])
    house['max. output'] = pd.to_numeric(house['max. output'])

    # house =
    # house = pd.DataFrame.from_dict(cor_file, orient='index')


    print(house)
    return house

def cor_bat(battery):
    """
    Loads the battery coordinates
    """
    # Load the necessary txt data into panda
    battery = pd.read_csv(cor_bat, sep= '\s+', header=['x_pos', 'y_pos', 'cap'])
    # battery = battery[['pos', 'cap']]
    print(battery)
    # print(battery['pos']).str.replace(']','').values.tolist())
    # Cleans data

    battery = pd.DataFrame(battery['pos'].str.replace(']','').values.tolist(), columns=['x_pos', 'y_pos'])

    print(battery)
    return battery

def load_results(results_file):
    """
    Loads csv data into pandas
    """
    # Loads the result file from the csv into panda
    result = pd.read_csv(results_file)

    #Cleans the data
    result = result[['house', 'battery', 'distance', 'max_output_house']]

    # Drops the last line which states the totals
    result = result.drop(result.index[150])
    result['house'] = pd.to_numeric(result['house'])
    result['battery'] = pd.to_numeric(result['battery'])
    result['distance'] = pd.to_numeric(result['distance'])

    return result

def show_grid(house, result, battery):
    """
    Creates a grid from the results and the houses
    """
    # Loads the two dataframes
    house = house
    result = result
    battery = battery

    # Forms scatterplot from the coordinates
    plt.plot(house['x'], house['y'])
    plt.scatter(house['x'], house['y'])
    plt.scatter(battery['pos'])

    # Adds a title and axis names
    plt.title('Position from the houses', fontweight='bold')
    plt.grid(True, linewidth = 1)

    plt.show()

def load_results_runs(filename):
    """
    Inputs a csv data into panda
    """
    # Load the necessary columns from the csv into panda
    data = pd.read_csv(filename)

    # Cleans the data
    data = data[['Run', 'Total Distance']]
    data['Run'] = pd.to_numeric(data['Run'])
    data['Total Distance'] = pd.to_numeric(data['Total Distance'])

    return data

def load_results_bounds(filename):
    """
    Inputs a csv data into panda
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
    Plots a scatterplot of the inserted data
    """
    minimum = data[data.columns[0]]
    distance = data[data.columns[1]]

    # print(minimum)
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

    # To use in main
    bounds = vis.load_results_bounds('bounds_test.csv')
    vis.plot_scatter(bounds)

def plot_line(data):
    """
    plots a histogram of the insterted data
    """
    runs = data[data.columns[0]]
    distance = data[data.columns[1]]

    # Forms the histogram
    plt.plot(runs, distance)

    # Adds the title and axis names
    # TO DO: Add axis names based on column header
    plt.title('Distance change in runs', fontweight='bold')
    plt.xlabel('Run')
    plt.ylabel('Distance')
    plt.xlim(0, len(runs))
    plt.ylim((min(distance) - 10), max(distance))
    plt.grid(True)

    # plt.hlines(y=(min(distance)), xmin=0, xmax=(max(runs)), color='r')

    # TO DO: Show Tick as minimum

    # Actually shows the histogram
    plt.show()

def dict_to_csv(total_distance):
    """
    Appends result to an csv file
    """
    with open('results_random_distance.csv', 'w', newline='') as infile:
        fields = ['Run', 'Total Distance']
        writer = csv.DictWriter(infile, fieldnames=fields)
        writer.writeheader()

        writer = csv.writer(infile, delimiter=',')
        input = total_distance
        for key, value in input.items():
            writer.writerow([key, value])

# if __name__ == '__main__':
#     data = load_results_runs('results_random_distance.csv')
#     runs = data['Run']
#     total_distance = data['Total Distance']
#     plot_line(runs, total_distance)
#     # house = load_houses('data/wijk1_huizen.csv')
#     # result = load_results('results/Fixed_batteries/random_grid1.csv')
#     # battery = cor_bat('data/wijk1_batterijen.txt')
#     # show_grid(house, result, battery)
