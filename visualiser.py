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

def load_results_bounds(filename):
    """
    Inputs a csv data into panda
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
    # Loads the different datasets
    runs = data[data.columns[0]]
    distance = data[data.columns[1]]

    runs1 = data1[data1.columns[0]]
    distance1 = data1[data1.columns[1]]

     # Forms the histogram
    plt.plot(runs, distance, label="Random")
    plt.plot(runs1, distance1, color = 'orange', label="Greedy-Hillclimber")

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
    plt.legend(loc='top right')

    # Adds the title and axis names
    # TO DO: Add axis names based on column header/ Seperate title for different Algorithm
    plt.title(f"{algorithm}", fontweight='bold')
    plt.xlabel('Iterations')
    plt.ylabel('Total Distance')
    plt.xlim(0, len(runs))
    plt.ylim((min(distance) - 10), max(distance))

    # Shows Grid
    plt.grid(True)

    # Actually shows the histogram
    plt.show()

def plot_comparison(data, data1, data2, algorithm):
    """
    Plots a comparison of the seperate neighbourhoods
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
    plt.legend(loc='top right')

    # Plots the legend
    plt.legend(loc='top right')

    # Adds the title and axis names
    plt.title(f"{algorithm} Algorithm", fontweight='bold')
    plt.xlabel('Iterations')
    plt.ylabel('Total Distance')

    # Actually shows the histogram
    plt.show()

def dict_to_csv(total_distance, algorithm, neighbourhood):
    """
    Appends result to an csv file
    """
    with open('results_' + algorithm + neighbourhood + '_distance.csv', 'w', newline='') as infile:
        fields = ['Run', 'Total Distance']
        writer = csv.DictWriter(infile, fieldnames=fields)
        writer.writeheader()

        writer = csv.writer(infile, delimiter=',')
        input = total_distance
        for key, value in input.items():
            writer.writerow([key, value])

