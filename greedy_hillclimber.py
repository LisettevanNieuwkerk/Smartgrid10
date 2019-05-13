from house import House
from battery import Battery
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
        """Get min and max bound"""
        #Get hightest and lowest distance for every house to battery
        maxim = 0
        minim = 0
        for i in range(150):
            maxim += (max(self.distances[i]))
            minim += (min(self.distances[i]))

        print("MIN:", minim)
        print("MAX:", maxim)


    def greedy(self):
        '''Greedy'''

        #
        house = 1
        sorted_distances = None
        sorted_index = None
        sorted_list = []

        # Iterate over every house and the distances to the batteries
        for distances_house in self.distances:
            # Sort distances and remember index
            sorted_distances = sorted(distances_house)
            sorted_index = sorted(range(len(distances_house)), key=lambda k: distances_house[k])

            # Add connected battery + house to distance
            index = 0
            for distance in sorted_distances:
                battery = sorted_index[index] + 1
                sorted_list.append([distance, battery, house])
                index += 1

            house += 1

        # Get sorted list of all distances
        sorted_list = sorted(sorted_list)

         # Set total distance Grid to 0 and create empty list with connections of houses to batteries
        connections = []
        total_distance = 0
        attached_houses = []

        # Iterate over sorted list
        for i in sorted_list:
            # Check if house already attached to a battery
            house = i[2]
            if house not in attached_houses:
                # Get output house
                max_output = self.houses[house].max_output
                # Check if capacity battery not yet reached
                battery = i[1]
                current_capacity = self.batteries[battery].currentCapacity
                max_capacity = self.batteries[battery].capacity
                if (current_capacity + max_output) <= max_capacity:
                    # Add to capacity, total distance and attached houses
                    self.batteries[battery].currentCapacity += max_output
                    distance = i[0]
                    total_distance += distance
                    attached_houses.append(house)
                    house_to_battery = {'house': house, 'battery': battery,
                    'distance': distance, 'max_output_house': max_output}
                    connections.append(house_to_battery)

        # Check for missing houses
        missing_houses = [value for value in range(1, 150) if value not in attached_houses]
        

        return [total_distance, connections, missing_houses]


    def hillclimber_houses(self, results):
        total_distance = results[0]
        connections = results[1]
        missing_houses = results[2]

        max = 150 - len(missing_houses)

        # Find spot for every missing house
        for house in missing_houses:
            #Find battery with lowest current capacity
            lowest_cap = 1510
            lowest_bat = 0
            for battery in self.batteries:
                if self.batteries[battery].currentCapacity <= lowest_cap:
                    lowest_cap = self.batteries[battery].currentCapacity
                    lowest_bat = battery
            #print(lowest_cap, lowest_bat, 1471.05461869 1)

            # Calculate free space needed in lowest battery to place missing house
            missing_output = self.houses[house].max_output
            space_needed = (lowest_cap + missing_output) - self.batteries[lowest_bat].capacity

            # Iterate over all connections and find connections with lowest_bat
            last_connection1 = max - 1
            space_found = 0
            for connection1 in range(max):
                last_connection2 = max - 1
                if connections[last_connection1]['battery'] == lowest_bat:
                    houseN1 = connections[last_connection1]['house']
                    max_output1 = connections[last_connection1]['max_output_house']
                    battery1 = connections[last_connection1]['battery']

                    # Go over all connections that not with lowest_bat
                    for connection2 in range(max):
                        battery2 = connections[last_connection2]['battery']
                        if battery2 != lowest_bat:
                            houseN2 = connections[last_connection2]['house']
                            max_output2 = connections[last_connection2]['max_output_house']
                            if max_output2 < max_output1:

                                # Check if max capacity not reached with switch
                                new_cap1 = self.batteries[battery1].currentCapacity - max_output1 + max_output2
                                new_cap2 = self.batteries[battery2].currentCapacity - max_output2 + max_output1
                                if new_cap1 <= self.batteries[battery1].capacity or new_cap2 <= self.batteries[battery2].capacity:
                                    # Switch batteries
                                    # Adapt current capacity batteries
                                    self.batteries[battery1].currentCapacity -= max_output1
                                    self.batteries[battery2].currentCapacity -= max_output2

                                    self.batteries[battery1].currentCapacity += max_output2
                                    self.batteries[battery2].currentCapacity += max_output1

                                    # Adapt total distance
                                    distance1 = connections[last_connection1]['distance']
                                    distance2 = connections[last_connection2]['distance']

                                    total_distance -= (distance1 + distance2)

                                    new_distance1 = self.distances[houseN1 - 1][battery2 - 1]
                                    new_distance2 = self.distances[houseN2 - 1][battery1 - 1]

                                    total_distance += (new_distance1 + new_distance2)

                                    #Adapt connections
                                    connections[last_connection1]['battery'] = battery2
                                    connections[last_connection1]['distance'] = new_distance1
                                    connections[last_connection2]['battery'] = battery1
                                    connections[last_connection2]['distance'] = new_distance2

                                    #Calculate space found
                                    space_found += (max_output1 - max_output2)

                                    break

                        last_connection2 -= 1

                    # Check if enough space found for last house
                    if space_found >= space_needed:
                        if (space_found + self.batteries[lowest_bat].currentCapacity) <= self.batteries[lowest_bat].capacity:
                            break

                last_connection1 -= 1

            #Place missing house
            missing_distance = self.distances[house -1][lowest_bat - 1]
            missing_ouput = self.houses[house].max_output
            self.batteries[lowest_bat].currentCapacity += missing_ouput
            total_distance += missing_distance
            connections.append({'house': house, 'battery': lowest_bat,
                    'distance': missing_distance, 'max_output_house': missing_ouput}) 

        return [total_distance, connections]

    def hillclimber_distance(self, results):
        total_distance = results[0]
        connections = results[1]

        for i in range (10):
            # Iterate over all houses and check if possible to connect to closer battery
            max = len(connections) 
            last_connection1 = max - 1 

            for connection1 in range(max):
                last_connection2 = max - 1 
                houseN1 = connections[last_connection1]['house']
                max_output1 = connections[last_connection1]['max_output_house']
                battery1 = connections[last_connection1]['battery']
                distance1 = connections[last_connection1]['distance']
                # Check for connections
                possible_battery = 1
                for distance in self.distances[houseN1 - 1]: 
                    if distance < distance1:
                        # Go over all houses connected to battery that belongs to smaller distance
                        for connection2 in range(max):
                            battery2 = connections[last_connection2]['battery']
                            if battery2 == possible_battery:
                                distance2 = connections[last_connection2]['distance']
                                houseN2 = connections[last_connection2]['house']
                                max_output2 = connections[last_connection2]['max_output_house']

                                # Check if switch would cause improvement
                                new_distance1 = distance
                                new_distance2 = self.distances[houseN2 - 1][battery1 - 1]
                                if (new_distance1 + new_distance2) < (distance1 + distance2): 
                                    # Check if max capacity not reached with switch
                                    new_cap1 = self.batteries[battery1].currentCapacity - max_output1 + max_output2
                                    new_cap2 = self.batteries[battery2].currentCapacity - max_output2 + max_output1
                                    if new_cap1 <= self.batteries[battery1].capacity or new_cap2 <= self.batteries[battery2].capacity:
                                        # Switch batteries
                                        # Adapt current capacity batteries
                                        self.batteries[battery1].currentCapacity -= max_output1
                                        self.batteries[battery2].currentCapacity -= max_output2

                                        self.batteries[battery1].currentCapacity += max_output2
                                        self.batteries[battery2].currentCapacity += max_output1

                                        # Adapt total distance
                                        distance1 = connections[last_connection1]['distance']
                                        distance2 = connections[last_connection2]['distance']

                                        total_distance -= (distance1 + distance2)

                                        new_distance1 = self.distances[houseN1 - 1][battery2 - 1]
                                        new_distance2 = self.distances[houseN2 - 1][battery1 - 1]

                                        total_distance += (new_distance1 + new_distance2)

                                        #Adapt connections
                                        connections[last_connection1]['battery'] = battery2
                                        connections[last_connection1]['distance'] = new_distance1
                                        connections[last_connection2]['battery'] = battery1
                                        connections[last_connection2]['distance'] = new_distance2

                    possible_battery += 1        
                    last_connection2 -= 1
                last_connection1 -= 1    

            print(len(connections))
            print(total_distance)

        return [total_distance, connections]


    def write_to_csv(self, connections, total_distance, costs_grid, costs_batteries, total_costs):
        # Write results to csv file
        with open('results_greedy_algorithm_2_results_grid2.csv', 'w') as csvFile:
            fields = ['house', 'battery', 'distance', 'max_output_house']
            writer = csv.DictWriter(csvFile, fieldnames=fields)
            writer.writeheader()
            writer.writerows(connections)

            writer = csv.writer(csvFile, delimiter=',')
            writer.writerow(['total distance: ' + str(total_distance), 'costs grid:' + str(costs_grid), 'costs batteries:' + str(costs_batteries), 'total costs:' + str(total_costs), ''])


if __name__ == "__main__":
    # Load data
    smartgrid = SmartGrid(3)

    # Calculate bounds
    smartgrid.bound()

    # Get connections from batteries to houses and total distance of cables
    results = smartgrid.greedy()
    results = smartgrid.hillclimber_houses(results)
    results = smartgrid.hillclimber_distance(results)

    #distance_connections = smartgrid.hillclimber(distance_connections)
    total_distance = results[0]
    connections = results[1]


    # Calculate total costs
    price_grid = 9
    costs_grid = price_grid * total_distance
    costs_batteries = 5 * 5000
    total_costs = costs_batteries + costs_grid

    # Write results to csv
    #smartgrid.write_to_csv(connections, total_distance, costs_grid, costs_batteries, total_costs)