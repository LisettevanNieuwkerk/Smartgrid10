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
    data = data[['Iteration', 'Value']]
    data['Iteration'] = pd.to_numeric(data['Iteration'])
    data['Value'] = pd.to_float(data['Value'])

    return data

def plot_scatter(iteration, value):
    """
    Plots a scatterplot of the inserted data
    """
    # Forms the scatterplot
    plt.scatter(iteration, value)

    # Adds a title and axis names
    plt.title('Value change in iterations', fontweight='bold')
    plt.xlabel('Iterations')
    plt.ylabel('Value')
    plt.ylim(2000, 6000)
    plt.grid(True)
    
    # Actually shows the scatterplot
    plt.show()

def plot_line(iteration, value):
    """
    plots a histogram of the insterted data
    """
    # Forms the histogram
    plt.plot(iteration, value, 'k', iteration, value, 'go')

    # Adds the title and axis names
    plt.title('Value change in iterations', fontweight='bold')
    plt.xlabel('Iterations')
    plt.ylabel('Value')
    plt.ylim(2000, 6000)
    plt.grid(True)

    # Actually shows the histogram
    plt.show


# if __name__ == '__main__':
#     data = load_results('CSV FILE')
#     value = data(data['value'])
#     iterations = data(data['iterations'])
#     plot_scatter(value, iterations)
#     plot_line(value, iterations)