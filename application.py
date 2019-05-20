# voeg de huidige structuur toe aan path
import os, sys
directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "classes"))
sys.path.append(os.path.join(directory, "code", "algorithms"))

# importeer de gebruikte structuur
from house import House
from battery import Battery
from brute_force import brute_force
from random_algorithm import random_solution


import sys
import csv
import random
from contextlib import closing

class SmartGrid():
    """
    This is the main Grid class. It contains all necessary attributes and methods to
    solve the unsolvable problem of the Smart Grid.
    """

    def __init__(self, neighbourhood_name):
        """
        Create houses and batteries for the problem.
        """
        self.houses = self.load_houses(f"data/wijk{neighbourhood_name}_huizen.csv")
        self.batteries = self.load_batteries(f"data/wijk{neighbourhood_name}_batterijen.txt")
        self.distances = self.distance()


    def load_houses(self, filename):
        """
        Load houses from filename.
        Return a dictionary of 'id' : House objects.
        """
        # First we parse all the data we need to create the houses with.
        # All parsed lines of data are saved to houses_data.
        houses = {}
        with open(filename, 'r') as infile:
            reader = csv.reader(infile)
            # Skip first row
            next(reader)
            # Set count for houses
            id = 1
            # Iterate over every row in file
            for rows in reader:
                # Put id, x and y position, max output into house object
                x_position = int(rows[0])
                y_position = int(rows[1])
                max_output = float(rows[2])
                house = House(id, x_position, y_position, max_output)
                # Add house to dict with id as key
                houses[id] = house
                id += 1

        return houses


    def load_batteries(self, filename):
        """
        Load batteries from filename.
        Return a dictionairt of 'id': Battery objects.
        """
        # First we parse all the data we need to create the houses with.
        # All parsed lines of data are saved to houses_data.
        batteries = {}
        with open(filename, "r") as infile:
            next(infile)
            id = 1
            for line in infile:
                # Filter chars out of line
                line = line.replace('[', '').replace(']', '').replace(',', '').replace('\t\t', ' ').replace('\t', ' ').replace('\n', '')
                line = line.split(' ')
                # Set values for battery
                x_position = int(line[0])
                y_position = int(line[1])
                capacity = float(line[2])
                # Create battery object and put in dict with id as key
                battery = Battery(id, x_position, y_position, capacity)
                batteries[id] = battery
                id += 1

        return batteries


    def distance(self):
        """
        Create a list with distances from all houses to all batteries.
        """

        x_distance = 0
        y_distance = 0
        distances = []

        # Iterate over every house
        for house in self.houses:
            # Create list of possible distances to batteries
            possibilities = []
            # Iterate over every battery
            for battery in self.batteries:
                # Calculate manhattan distance from house to battery
                x_distance = abs(self.houses[house].xpos - self.batteries[battery].xpos)
                y_distance = abs(self.houses[house].ypos - self.batteries[battery].ypos)
                manhattan_distance = x_distance + y_distance
                # Set battery as key in list of house and add distance
                possibilities.append(manhattan_distance)
            distances.append(possibilities)

        # Return list with all distances
        return distances


    def bound(self):
        """
        Get mininum and maximum bound
        """

        #Get hightest and lowest distance for every house to battery and add up to each other
        maxim = 0
        minim = 0
        for i in range(150):
            maxim += (max(self.distances[i]))
            minim += (min(self.distances[i]))

        print("Minimum bound:", minim)
        print("Maximum bound:", maxim)


    def write_to_csv(self, algorithm, neighbourhood, connections, total_distance, costs_grid, costs_batteries, total_costs):
        """
        Write results to a csv fil
        """
        # Write connections, total distance and costs to a csv file
        with open(f'{algorithm}_grid{neighbourhood}.csv', 'w') as csvFile:
            fields = ['house', 'battery', 'distance', 'max_output_house']
            writer = csv.DictWriter(csvFile, fieldnames=fields)
            writer.writeheader()
            writer.writerows(connections)

            writer = csv.writer(csvFile, delimiter=',')
            writer.writerow(['total distance: ' + str(total_distance), 'costs grid:' + str(costs_grid), 'costs batteries:' + str(costs_batteries), 'total costs:' + str(total_costs), ''])


if __name__ == "__main__":
    # Load data
    neighbourhood = 1
    smartgrid = SmartGrid(neighbourhood)

    # Calculate bounds
    smartgrid.bound()

    # Ask user which algorithm to use
    print(f"Hello! Welcome at the application of team Smartgrid10\n\
        How would you like to try to solve the unsolvable problem of the smartgrid?\n\
        With fixed or moveable batteries?")
    while True:
        answer_1 = str(input("Type A for fixed batteries and B for moveable\n"))
        if answer_1 == 'A' or answer_1 == 'B':
            break
    
    if answer_1 == 'A':
        print(f"Which algoritm would you like to use?\n\
            Type A for a brute force algorithm\n\
            Type B for a random algorithm that will run 10.000 times and saves the best result\n\
            Type C for a greedy algorithm followed by a hillclimber\n\
            Type D for a simulated annealing algorithm on a random solution")

    while True:
        answer_2 = str(input())
        if answer_2 == 'A': 
            distance_connections = brute_force(smartgrid)
            algorithm = "brute_force"
            break
        if answer_2 == 'B': 
            distance_connections = random_solution(smartgrid)
            algorithm = "random"
            break    
        if answer_2 == 'C': 
            distance_connections = random_solution(smartgrid)
            break 
        if answer_2 == 'D': 
            distance_connections = random_solution(smartgrid)
            break 

    total_distance = distance_connections[0]
    connections = distance_connections[1]

    print(f"Total distance: {total_distance}")

    # Calculate total costs
    price_grid = 9
    costs_grid = price_grid * total_distance
    costs_batteries = 5 * 5000
    total_costs = costs_batteries + costs_grid
    print(f"Total costs: {total_costs}")

    # Write results to csv
    smartgrid.write_to_csv(algorithm, neighbourhood, connections, total_distance, costs_grid, costs_batteries, total_costs)
