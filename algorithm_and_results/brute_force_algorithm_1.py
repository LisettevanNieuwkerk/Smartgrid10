from house import House
from battery import Battery
import sys
import csv
import random
from itertools import product

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
                xpos = int(rows[0])
                ypos = int(rows[1])
                max_output = float(rows[2])
                house = House(id, xpos, ypos, max_output)
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
                xpos = int(line[0])
                ypos = int(line[1])
                capacity = float(line[2])
                # Create battery object and put in dict with id as key
                battery = Battery(id, xpos, ypos, capacity)
                batteries[id] = battery
                id += 1

        return batteries

    def distance(self):
        """
        Create a dictionaty with distances from all houses to all batteries.
        """

        x_distance = 0
        y_distance = 0
        distances = []

        # Iterate over every house
        for house in self.houses:
            # Put dict of house in dict of distances
            distances.append([])
            # Itirate over every battery
            for battery in self.batteries:
                # Calculate manhattan distance from house to battery
                x_distance = abs(self.houses[house].xpos - self.batteries[battery].xpos)
                y_distance = abs(self.houses[house].ypos - self.batteries[battery].ypos)
                manhattan_distance = x_distance + y_distance
                # Set battery as key in list of house and add distance
                distances[house-1].append(manhattan_distance)

        # Return dict with all distances
        return distances


    def calculate_costs(self):
        # Set total distance Grid to 0 and create empty list with connections of houses to batteries
        first = True
        shortest = None
        total_distance = 0
        house = 0
        capacity_reached = False
        shortest_index = None

        #A = self.distances[0]
        #B = self.distances[1]
        #C = self.distances[2]

        # Check possible battery/house combinations
        for distance in product(*self.distances):
        #for distance in product(A, B, C):
            # List of distances of houses
            #print(f"Distances houses to a battery: { list(distance) }")

            # Index of batteries list
            #index = tuple(row.index(elem) for row, elem in zip((self.distances), distance))
            index = tuple(row.index(elem) for row, elem in zip((self.distances), distance))
            list_index = list(index)
            print(f"Index of batteries: { list_index }")

            # Add capacity to batteries
            # Set capacity all batteries to 0
            for battery in self.batteries:
                self.batteries[battery].currentCapacity = 0

            house = 0
            for i in list_index:
                # If capacity not reached, add tot current capacity and continue
                if self.batteries[i+1].currentCapacity <= self.batteries[i+1].capacity:
                    self.batteries[i+1].currentCapacity += self.houses[house+1].max_output
                    house += 1
                # If battery full; break loop
                else:
                    capacity_reached = True
                    break

            #print(f"Current capacity batteries: {self.batteries[1].currentCapacity, self.batteries[2].currentCapacity, self.batteries[3].currentCapacity, self.batteries[4].currentCapacity, self.batteries[5].currentCapacity}")
            #print(f"Capacity of a battery reached: { capacity_reached }")

            # Check if batteries not full
            if capacity_reached == False:
                # Calculate total distance
                total_distance = sum(distance)
                #print(f"Total distance: {total_distance}")
                # Check if first value
                if first == True:
                    shortest = total_distance
                    first = False
                # If not first value, check if total distance smaller than shortest
                elif first == False:
                    if total_distance < shortest:
                        shortest = total_distance
                        shortest_index = list_index
                        print(f"Shortest index: {shortest_index}")
                        print(f"Shortest: {shortest}")

        print(f"Shortest of all: {shortest}, index: {shortest_index}")

        i = 1
        with open('results_brute_force_algorithm_1.csv', 'w') as csvFile:
            writer = csv.writer(csvFile, delimiter=',')
            writer.writerow(['House', 'Battery', 'Distances'])
            for row in shortest_index:
                writer.writerow([i, (row + 1), self.distances[i - 1][row]])
                i += 1
            writer.writerow(['Shortest of all:' + str(shortest), 'Index: ' +  str(shortest_index)])

if __name__ == "__main__":
    smartgrid = SmartGrid(1)
    smartgrid.calculate_costs()
