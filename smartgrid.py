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

    def __init__(self, neighbourhood_name, fixed):
        """
        Create houses and batteries for the problem.
        """
        self.houses = self.load_houses(f"data/wijk{neighbourhood_name}_huizen.csv")
        self.batteries = self.load_batteries(f"data/wijk{neighbourhood_name}_batterijen_lowestbound.txt", fixed)
        self.distances = self.distance()
        self.coordinates = []

    def kmeans_function(self):

        batterie_locations = []

        for house in self.houses:
            house_location = []
            house_location.append(self.houses[house].xpos)
            house_location.append(self.houses[house].ypos)
            batterie_locations.append(house_location)

        x = random.randint(1,10000)
        cluster = KMeans(n_clusters=5, random_state=x)
        cluster.fit(batterie_locations)
        positions = cluster.cluster_centers_
        positions = np.around(np.abs(positions)).astype(int)
        print(positions)
        # print(positions)
        # print(batterie_locations)
        # print(positions)
        # test = locatiechecker()

        return positions

    def locatiechecker(self):
        davidmok_leg = True
        print(davidmok_leg)
        for house in self.houses:
            for batterij in self.batteries:
                if (self.houses[house].xpos == self.batteries[batterij].xpos and self.houses[house].ypos == self.batteries[batterij].ypos):
                    davidmok_leg = False
                    print("BATJE:", batterij, "OSSO:", house)

        print(davidmok_leg)
        return davidmok_leg

    def load_batteries_differentbatts(self, filename):
        """
        Load batteries from filename.
        Return a dictionairt of 'id': Battery objects.
        """
        # First we parse all the data we need to create the houses with.
        # All parsed lines of data are saved to houses_data.
        batteries = {}
        used_capacity = 0


        with open(filename, "r") as infile:
            battery_type = infile.readlines()
            # print(types[1], types[2], types[3])

            for i in range(3):
                battery_type[i] = battery_type[i].replace('[', '').replace(']', '').replace(',', '').replace('\t\t', ' ').replace('\t', ' ').replace('\n', '')
                battery_type[i] = battery_type[i].split('  ')
                # print(battery_type)

            id = 1
            while True:
                x = random.randint(1,3)
                x = x - 1
                # Set values for battery
                x_position = random.randint(1,50)
                y_position = random.randint(1,50)
                capacity = battery_type[x][1]
                price = battery_type[x][2]
                # Create battery object and put in dict with id as key
                battery = Battery(id, x_position, y_position, capacity)
                batteries[id] = battery
                id += 1
                used_capacity += int(battery_type[x][2])
                print(battery)
                # print(used_capacity)
                if used_capacity >= 7700:
                    break

        return batteries

    def load_batteries1(self, filename, fixed):
        """
        Load batteries from filename.
        Return a dictionairt of 'id': Battery objects.
        """
        # First we parse all the data we need to create the houses with.
        # All parsed lines of data are saved to houses_data.
        batteries = {}

        self.coordinates = self.kmeans_function()
        # print("TEST!!", self.coordinates)

        with open(filename, "r") as infile:
            next(infile)
            id = 1
            for line in infile:
                # Filter chars out of line
                line = line.replace('[', '').replace(']', '').replace(',', '').replace('\t\t', ' ').replace('\t', ' ').replace('\n', '')
                line = line.split(' ')
                # Set values for battery
                x_position = self.coordinates[id-1][0]
                y_position = self.coordinates[id-1][1]
                capacity = float(line[2])
                price = 0
                # Create battery object and put in dict with id as key
                battery = Battery(id, x_position, y_position, capacity)
                batteries[id] = battery
                id += 1
                # print(battery)


        return batteries

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


    def load_batteries(self, filename, fixed):
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
                # if fixed == True:
                x_position = int(line[0])
                y_position = int(line[1])
                # elif fixed == False:
                #     x_position = random.randint(1,50)
                #     y_position = random.randint(1,50)

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



        # print("Minimum bound:", minim)
        # print("Maximum bound:", maxim)

        return minim

    def write_to_csv(self, position_batteries, algorithm, neighbourhood, connections, total_distance, costs_grid, costs_batteries, total_costs):
        """
        Write results to a csv fil
        """
        # Write connections, total distance and costs to a csv file
        with open(f'results/{position_batteries}/{algorithm}_grid{neighbourhood}.csv', 'w', newline='') as csvFile:
            fields = ['house', 'battery', 'distance', 'max_output_house']
            writer = csv.DictWriter(csvFile, fieldnames=fields)
            writer.writeheader()
            writer.writerows(connections)

            writer = csv.writer(csvFile, delimiter=',')
            writer.writerow(['total distance: ' + str(total_distance), 'costs grid:' + str(costs_grid), 'costs batteries:' + str(costs_batteries), 'total costs:' + str(total_costs)])
