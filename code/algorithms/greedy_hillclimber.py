
"""
A Greedy algorithm is performed, followed by a algorithm that adds the last missing houses to connections.
At last a hillclimber will be performed to improve the result
"""

import visualiser as vis

def greedy(self):
    """
    Greedy algorithm
    """
    # Set initial calues
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


def add_missing_houses(self, results):
    """
    Add missing houses to list of connection
    """
    # Set values
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


def hillclimber_determined(self, results):
    """
    Deterministic hillclimber to improve result on greedy
    """

    total_distance = results[0]
    connections = results[1]

    # Adds every run with value to a dict
    distances_total = dict()
    key = 1

    print(total_distance)
    for i in range(4):
        # Iterate over all houses and check if possible to connect to closer battery
        max = len(connections)
        last_connection1 = max - 1

        for connection1 in range(max):
            switched = False
            houseN1 = connections[last_connection1]['house']
            max_output1 = connections[last_connection1]['max_output_house']
            battery1 = connections[last_connection1]['battery']
            distance1 = connections[last_connection1]['distance']

            # Adds every distance to a dict with the run number as id
            distances_total[key] = total_distance
            key += 1

            # Check for connections
            possible_battery = 1
            for distance in self.distances[houseN1 - 1]:

                if distance < distance1:

                    last_connection2 = max - 1
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
                            if (new_distance1 + new_distance2) <= (distance1 + distance2):
                                # Check if max capacity not reached with switch
                                new_cap1 = self.batteries[battery1].currentCapacity - max_output1 + max_output2
                                new_cap2 = self.batteries[battery2].currentCapacity - max_output2 + max_output1
                                if new_cap1 <= self.batteries[battery1].capacity and new_cap2 <= self.batteries[battery2].capacity:
                                    # Switch batteries
                                    # Adapt current capacity batteries
                                    self.batteries[battery1].currentCapacity -= max_output1
                                    self.batteries[battery2].currentCapacity -= max_output2

                                    self.batteries[battery1].currentCapacity += max_output2
                                    self.batteries[battery2].currentCapacity += max_output1

                                    # Adapt total distance
                                    total_distance -= (distance1 + distance2)
                                    total_distance += (new_distance1 + new_distance2)



                                    #Adapt connections
                                    connections[last_connection1]['battery'] = battery2
                                    connections[last_connection1]['distance'] = new_distance1
                                    connections[last_connection2]['battery'] = battery1
                                    connections[last_connection2]['distance'] = new_distance2

                                    switched = True
                                    break
                        last_connection2 -= 1
                    if switched == True:
                        break
                possible_battery += 1
            last_connection1 -= 1

        # Saves the dict to a csv
        vis.dict_to_csv(distances_total)

    return [total_distance, connections]
