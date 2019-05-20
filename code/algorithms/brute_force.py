from itertools import product

def brute_force(self):
    # Set total distance Grid to 0 and create empty list with connections of houses to batteries
    first = True
    shortest = None
    total_distance = 0
    house = 0
    capacity_reached = False
    shortest_index = None

    # Check possible battery/house combinations
    for distance in product(*self.distances):
        # List of distances of houses
        #print(f"Distances houses to a battery: { list(distance) }")

        # Index of batteries list
        index = tuple(row.index(elem) for row, elem in zip((self.distances), distance))
        list_index = list(index)
        #print(f"Index of batteries: { list_index }")

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
                   # print(f"Shortest index: {shortest_index}")
                    #print(f"Shortest: {shortest}")

    # Write down connections of shortest index
    connections = []
    i = 1
    for row in shortest_index:
        house_to_battery = {'house': i, 'battery': (row + 1),
                    'distance': self.distances[i - 1][row], 'max_output_house': self.houses[i].max_output}
        connections.append(house_to_battery)
        i += 1
        
    total_distance = shortest

    return [total_distance, connections]


