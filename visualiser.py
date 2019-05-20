"""
This script visualizes the data obtained from the algorithms
"""

import csv
import pandas as pd
import matplotlib.pyplot as plt

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

    return house

def cor_bat(cor_bat):
    """
    Loads the battery coordinates
    """
    # Load the necessary txt data into panda
    battery = pd.read_csv(cor_bat, delimiter= '\s+')

    # Cleans data
    battery = battery[['pos', 'cap']]
    for battery 

    return battery

def load_results2(results_file):
    """
    Loads csv data into pandas
    """
    # Loads the result file from the csv into panda
    result = pd.read_csv(results_file)

    #Cleans the data
    result = result[['house', 'battery', 'distance', 'max_output_house', 'current_capacity_battery']]
    
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
    # plt.xlim(0, 50)
    # plt.ylim(0, 50)
    plt.grid(True, linewidth = 1)

    plt.show()


def load_results(filename):
    """
    Inputs a csv data into panda
    """
    # Load the necessary columns from the csv into panda
    data = pd.read_csv(filename)

    # Cleans the data
    data = data[['Run', 'Total Distance']]
    data['Run'] = pd.to_numeric(data['Run'])
    data['Total Distance'] = pd.to_numeric(data['Total Distance'])


    # data = data[['Run', 'Total Distance', 'Costs Grid', 'Costs Batteries', 'Total Costs']]
    # data['Runs'] = pd.to_numeric(data['Run'])
    # data['Total Distance'] = pd.to_numeric(data['Total Distance'])
    # data['Costs Grid'] = pd.to_numeric(data['Costs Grid'])
    # data['Costs Batteries'] = pd.to_numeric(data['Costs Batteries'])
    # data['Total Costs'] = pd.to_numeric(data['Total Costs'])
    return data

def plot_scatter(runs, costs):
    """
    Plots a scatterplot of the inserted data
    """
    # Forms the scatterplot
    plt.scatter(runs, costs)

    # Adds a title and axis names
    plt.title('Distance change in runs', fontweight='bold')
    plt.xlabel('Run')
    plt.ylabel('Distance')
    plt.ylim(2000, 6000)
    plt.grid(True)
    
    # Actually shows the scatterplot
    plt.show()

def plot_line(runs, distance):
    """
    plots a histogram of the insterted data
    """
    # Forms the histogram
    #plt.plot(runs, distance, 'k', runs, distance, 'go')
    plt.plot(runs, distance)

    # Adds the title and axis names
    plt.title('Distance change in runs', fontweight='bold')
    plt.xlabel('Run')
    plt.ylabel('Distance')
    plt.xlim(0, len(runs))
    plt.ylim(min(distance), max(distance))
    plt.grid(True)

    # Actually shows the histogram
    plt.show()

# def write_to_csv(self, total_distance, costs_grid, costs_batteries, total_costs):
#     """
#     Appends result to an existing csv file
#     """
#     with open('results_random.csv', 'a') as infile:
#         fields = ['Total Distance', 'Costs Grid', 'Costs Batteries', 'Total Costs']
#         writer = csv.DictWriter(infile, fieldnames=fields)
#         writer.writeheader()
# 
#         writer = csv.writer(infile, delimiter=',') 
#         input = [str(total_distance), str(costs_grid), str(costs_batteries), str(total_costs)]
#         writer.writerow(input)

def dict_to_csv(self, total_distance):
    """
    Appends result to an existing csv file
    """
    with open('results_random_distance.csv', 'w', newline='') as infile:
        fields = ['Run', 'Total Distance']
        writer = csv.DictWriter(infile, fieldnames=fields)
        writer.writeheader()

        writer = csv.writer(infile, delimiter=',')
        input = total_distance
        for key, value in input.items():
            writer.writerow([key, value])

if __name__ == '__main__':
    data = load_results('results_random_distance.csv')
    runs = data['Run']
    total_distance = data['Total Distance']
    # plot_line(runs, total_distance)
    house = load_houses('wijk1_huizen.csv')
    result = load_results2('random_randomhouses.csv') 
    battery = cor_bat('wijk1_batterijen.txt')
    show_grid(house, result, battery)

