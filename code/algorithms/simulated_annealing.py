from house import House
from battery import Battery
import sys
import csv
import random
from contextlib import closing
import math
import decimal


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
        Create a list with distances from all houses to all batteries.
        """

        x_distance = 0
        y_distance = 0
        distances = []

        # Iterate over every house
        for house in self.houses:
            # Put dict of house in dict of distances
            possibilities = []
            # Itirate over every battery
            for battery in self.batteries:
                # Calculate manhattan distance from house to battery
                x_distance = abs(self.houses[house].xpos - self.batteries[battery].xpos)
                y_distance = abs(self.houses[house].ypos - self.batteries[battery].ypos)
                manhattan_distance = x_distance + y_distance
                # Set battery as key in list of house and add distance
                possibilities.append(manhattan_distance)
            distances.append(possibilities)

        # Return dict with all distances
        return distances

    def bound(self):
        #for i in self.distances:
        maxim = 0
        minim = 0
        for i in range(150):
            maxim += (max(self.distances[i]))
            minim += (min(self.distances[i]))

        print("MIN:", minim)
        print("MAX:", maxim)


    def random(self):
        highest_score = 0
        first_attempt = True
        best_connections = None

        # Run multiple times
        for j in range(100):
            # Set total distance Grid to 0 and create empty list with connections of houses to batteries
            total_distance = 0
            connections = []

            # Empty capacity
            for battery in self.batteries:
                self.batteries[battery].currentCapacity = 0

            # Iterate over all houses and get max output
            for i in range(150):
                house = i + 1
                max_output = self.houses[house].max_output
                picked_batteries = []

                while True:
                    # Pick random battery
                    battery = random.randint(1,5)
                    index_battery = battery - 1

                    # Check if already chosen and add to picked list
                    if battery not in picked_batteries:
                        picked_batteries.append(battery)

                        max_capacity = self.batteries[battery].capacity
                        current_capacity = self.batteries[battery ].currentCapacity
                        possible_capacity = current_capacity + max_output

                        # Check if max capacity not yet reached
                        if possible_capacity <= max_capacity:
                            # Check distance from house to battery and add to total distances
                            distances_house = self.distances[i]
                            distance = distances_house[index_battery]
                            total_distance += distance
                            # Add output to current capacity
                            self.batteries[battery].currentCapacity += max_output
                            house_to_battery = {'house': house, 'battery': battery, 'distance': distance, 'max_output_house': max_output}
                            connections.append(house_to_battery)
                            break

                        # Check if al 5 batteries tried
                        if (len(picked_batteries) == 5):
                            break

            # Only save results when all houses connected
            if len(connections) == 150:
                if first_attempt == True:
                    highest_score = total_distance
                    best_connections = connections
                    first_attempt = False
                else:
                    if total_distance < highest_score:
                        highest_score = total_distance
                        best_connections = connections

        return [highest_score, best_connections]


    def neighbor (self, total_distance, connections):
        new_distance = None

        # Find neigboring solution
        while new_distance == None:
            # Pick random connection
            connection1 = random.randint(0,149)
            connection2 = random.randint(0,149)
            # Check if not same connection
            if connection1 != connection2:
                # Check if not same battery
                battery1 = connections[connection1]['battery']
                battery2 = connections[connection2]['battery']
                if battery1 != battery2:

                    # Check if switch would be possible:
                    max_output1 = connections[connection1]['max_output_house']
                    max_output2 = connections[connection2]['max_output_house']  
                    new_cap1 = self.batteries[battery1].currentCapacity - max_output1 + max_output2
                    new_cap2 = self.batteries[battery2].currentCapacity - max_output2 + max_output1
                    if new_cap1 <= self.batteries[battery1].capacity and new_cap2 <= self.batteries[battery2].capacity:
                        # Calculate new distance
                        houseN1 = connections[connection1]['house']
                        houseN2 = connections[connection2]['house']

                        old_distance1 = connections[connection1]['distance']
                        old_distance2 = connections[connection2]['distance']
                        print(f"totalOld {total_distance}")
                        print(f"old {old_distance1} {old_distance2}")    

                        new_distance1 = self.distances[houseN1 - 1][battery2 - 1]
                        new_distance2 = self.distances[houseN2 - 1][battery1 - 1]
                        print(f"new {new_distance1} {new_distance2}")  

                        new_distance = total_distance - old_distance1 - old_distance2
                        new_distance = new_distance + new_distance1 + new_distance2
                        print(f"totalNew {new_distance}")

                        # Switch batteries
                        # Adapt current capacity batteries
                        self.batteries[battery1].currentCapacity -= max_output1
                        self.batteries[battery2].currentCapacity -= max_output2
                        self.batteries[battery1].currentCapacity += max_output2
                        self.batteries[battery2].currentCapacity += max_output1


                        #Adapt connections
                        connections[connection1]['battery'] = battery2
                        connections[connection1]['distance'] = new_distance1
                        connections[connection2]['battery'] = battery1
                        connections[connection2]['distance'] = new_distance2                          

        
        return new_distance, connections  

    def anneal_distance (self, results):

        total_distance = results[0]
        connections = results[1]

        print(f"first = {total_distance}")

        best_result = total_distance
        best_connections = connections
        counter = 0

        T = 1.5
        T_min = 0.0001
        alpha = 0.99
        #While temperature is not zero
        while T > T_min:

            i = 1
            while i <= 100:
                # Pick random connection
                connection1 = random.randint(0,149)
                connection2 = random.randint(0,149)
                # Check if not same connection
                if connection1 != connection2:
                    # Check if not same battery
                    battery1 = connections[connection1]['battery']
                    battery2 = connections[connection2]['battery']
                    if battery1 != battery2:
                        # Check if switch would be possible:
                        max_output1 = connections[connection1]['max_output_house']
                        max_output2 = connections[connection2]['max_output_house']  
                        new_cap1 = self.batteries[battery1].currentCapacity - max_output1 + max_output2
                        new_cap2 = self.batteries[battery2].currentCapacity - max_output2 + max_output1
                        if new_cap1 <= self.batteries[battery1].capacity and new_cap2 <= self.batteries[battery2].capacity:
                            # Calculate new distance
                            houseN1 = connections[connection1]['house']
                            houseN2 = connections[connection2]['house']

                            old_distance1 = connections[connection1]['distance']
                            old_distance2 = connections[connection2]['distance']   

                            new_distance1 = self.distances[houseN1 - 1][battery2 - 1]
                            new_distance2 = self.distances[houseN2 - 1][battery1 - 1]

                            new_distance = total_distance - old_distance1 - old_distance2
                            new_distance = new_distance + new_distance1 + new_distance2
                            
                            if new_distance <= total_distance:
                                total_distance = new_distance

                                # Switch batteries
                                # Adapt current capacity batteries
                                self.batteries[battery1].currentCapacity -= max_output1
                                self.batteries[battery2].currentCapacity -= max_output2
                                self.batteries[battery1].currentCapacity += max_output2
                                self.batteries[battery2].currentCapacity += max_output1


                                #Adapt connections
                                connections[connection1]['battery'] = battery2
                                connections[connection1]['distance'] = new_distance1
                                connections[connection2]['battery'] = battery1
                                connections[connection2]['distance'] = new_distance2

                
                            else:
                                delta = total_distance - new_distance                   
                                ap = math.exp(delta / T)
                                r = random.random()
                                if ap >= r:
                                    total_distance = new_distance
                                    # Switch batteries
                                    # Adapt current capacity batteries
                                    self.batteries[battery1].currentCapacity -= max_output1
                                    self.batteries[battery2].currentCapacity -= max_output2
                                    self.batteries[battery1].currentCapacity += max_output2
                                    self.batteries[battery2].currentCapacity += max_output1


                                    #Adapt connections
                                    connections[connection1]['battery'] = battery2
                                    connections[connection1]['distance'] = new_distance1
                                    connections[connection2]['battery'] = battery1
                                    connections[connection2]['distance'] = new_distance2

                            if best_result >= total_distance:
                                best_result = total_distance
                                best_connections = connections 

                i += 1 
            T *= alpha

        print(f"results {total_distance}")
        print(f"results {best_result}")               
        
    

        # test
        '''houses_list = []
        print(len(connections))
        print(total_distance)  
        for battery in self.batteries:
            print(self.batteries[battery].currentCapacity)   
        for connection in connections:    
            houses_list.append(connection['house'])  
      
        missing_houses = [value for value in range(1, 150) if value not in houses_list]   
        print(missing_houses)'''


        return [total_distance, connections]


    def write_to_csv(self, connections, total_distance, costs_grid, costs_batteries, total_costs):
        # Write results to csv file
        with open('results_random_algorithm_1.csv', 'w') as csvFile:
            fields = ['house', 'battery', 'distance', 'max_output_house', \
                 'current_capacity_battery']
            writer = csv.DictWriter(csvFile, fieldnames=fields)
            writer.writeheader()
            writer.writerows(connections)

            writer = csv.writer(csvFile, delimiter=',')
            writer.writerow(['total distance: ' + str(total_distance), \
                 'costs grid:' + str(costs_grid), 'costs batteries:' + \
                     str(costs_batteries), 'total costs:' + str(total_costs), ''])


if __name__ == "__main__":
    # Load data
    smartgrid = SmartGrid(3)

    # Calculate bounds
    smartgrid.bound()

    # Get connections from batteries to houses and total distance of cables
    results = smartgrid.random()
    results = smartgrid.anneal_distance(results)
    total_distance = results[0]
    connections = results[1]

    # Calculate total costs
    price_grid = 9
    costs_grid = price_grid * total_distance
    costs_batteries = 5 * 5000
    total_costs = costs_batteries + costs_grid

    # Write results to csv
    #smartgrid.write_to_csv(connections, total_distance, costs_grid, costs_batteries, total_costs)
