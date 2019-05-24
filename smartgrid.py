# voeg de huidige structuur toe aan path
import os, sys
directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "classes"))

from sklearn.cluster import KMeans
from house import House
from battery import Battery
import sys
import csv
import random
import numpy as np


class SmartGrid():
    """
    This is the main Grid class. It contains all necessary attributes and methods to
    solve the unsolvable problem of the Smart Grid.
    """

    def __init__(self, neighbourhood, fixed, algorithm, different):
        """
        Create houses and batteries for the problem.
        """
        battery_file = None

        self.houses = self.load_houses(f"data/wijk{neighbourhood}_huizen.csv")

        if different == False:
            battery_file = f"data/wijk{neighbourhood}_batterijen.txt"
        elif different == True:
            battery_file = f"data/newbatteries.txt"

        self.batteries = self.load_batteries(battery_file, fixed, algorithm, different)
        self.distances = self.distance()


    def load_batteries(self, filename, fixed, algorithm, different):
        """
        Load batteries from filename.
        Return a dictionairy of 'id': Battery objects.
        """
        # First we parse all the data we need to create the houses with.
        # All parsed lines of data are saved to houses_data.
        coordinates = []
        count = 0

        batteries = {}
        different_batteries = []
        with open(filename, "r") as infile:
            next(infile)
            for line in infile:
                # Filter chars out of line
                line = line.replace('[', '').replace(']', '').replace(',', '').replace('\t\t', ' ').replace('\t', ' ').replace('\n', '')
                line = line.split(' ')

                different_batteries.append(line)

        # Load in regular batteries
        if different == False:
            for different_battery in different_batteries:
                # Set values for battery
                id = count + 1
                name = 'Normal'
                capacity = float(different_battery[2])
                price = 5000
                if fixed == True:
                    x_position = int(different_battery[0])
                    y_position = int(different_battery[1])
                    coordinates.append([x_position, y_position])
                # Create battery object and put in dict with id as key
                battery = Battery(id, name, capacity, price)
                batteries[id] = battery
                count += 1

        # Load in different batteries
        elif different == True:
            total_capacity_houses = 7700
            used_capacity = 0
            while True:
                x = random.randint(0,2)
                different_battery = different_batteries[x]
                # Set values for battery
                id = count + 1
                name = different_battery[0]
                capacity = float(different_battery[1])
                price = int(different_battery[2])

                # Create battery object and put in dict with id as key
                battery = Battery(id,  name, capacity, price)
                batteries[id] = battery
                count += 1

                used_capacity += float(different_battery[1])
                # print(used_capacity)
                if used_capacity >= total_capacity_houses:
                    break

        # If batteries moveable, define coordinates
        if fixed == False:
            coordinates = self.define_coordinates(algorithm, id)

        # Add coordinates
        count = 0
        for battery in batteries:
            batteries[battery].xpos = coordinates[count][0]
            batteries[battery].ypos = coordinates[count][1]
            count += 1

        return batteries


    def define_coordinates(self, algorithm, id):
        """
        Define new coordinates of battery
        """
        coordinates = None
        # Define coordinates according to K-Means clustering
        if algorithm == "cluster_position":
            while True:
                coordinates = self.kmeans_function(id)
                # Check if coordinates are possible
                free_space = self.location_checker(coordinates)
                if free_space == True:
                    break

        # Define coordinates random
        if algorithm == "random_position":
            while True:
                coordinates = []
                for i in range(id):
                    x_position = random.randint(1,50)
                    y_position = random.randint(1,50)
                    coordinates.append([x_position, y_position])
                # Check if coordinates are possible
                free_space = self.location_checker(coordinates)
                if free_space == True:
                    break

        return coordinates


    def kmeans_function(self, id):
        """
        K-Means clustering function that finds the middle of clusters
        """
        # Puts all coordinates of houses in a list
        battery_locations = []
        for house in self.houses:
          house_location = []
          house_location.append(self.houses[house].xpos)
          house_location.append(self.houses[house].ypos)
          battery_locations.append(house_location)

        # Tries to find the middels of the clusters with K-means clustering
        x = random.randint(1,10000)
        cluster = KMeans(n_clusters=id, random_state=x)
        cluster.fit(battery_locations)
        coordinates = cluster.cluster_centers_
        coordinates = np.around(np.abs(coordinates)).astype(int)

        return coordinates


    def location_checker(self, coordinates):
        """
        Checks if a house is not placed on the position of the battery
        """
        free_space = True
        # Iterate over all houses
        for house in self.houses:
            # Checks if one of the batteries on the same coordinates as a
            for location in coordinates:
                if location[0] == self.houses[house].xpos and location[1] == self.houses[house].ypos:
                    free_space = False
                    return free_space

        return free_space


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

        return minim, maxim


    def write_to_csv(self, position_batteries, type, pos, algorithm, neighbourhood, connections, total_distance, costs_grid, costs_batteries, total_costs):
        """
        Write results to a csv file
        """
        # Write connections, total distance and costs to a csv file
        with open(f'results/{position_batteries}/{type}_{pos}_{algorithm}_grid{neighbourhood}.csv', 'w', newline='') as csvFile:
            fields = ['house', 'battery', 'distance', 'max_output_house']
            writer = csv.DictWriter(csvFile, fieldnames=fields)
            writer.writeheader()
            writer.writerows(connections)

            writer = csv.writer(csvFile, delimiter=',')
            writer.writerow(['total distance: ' + str(total_distance), 'costs grid:' + str(costs_grid), 'costs batteries:' + str(costs_batteries), 'total costs:' + str(total_costs)])
