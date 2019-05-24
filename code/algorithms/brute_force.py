from itertools import product

def brute_force(self):
"""
This is a brute force algorithm, created in the beginning of the project.
It takes very long for it to generate an answer (but we've tested it on a smaller replicated grid & it worked! (unfortunately these results are lost atm)).
We haven't used it in our further research,
but we left in in the repository, as it was a part of our 'exploration' :)!
"""

    # Set total distance Grid to 0 and create empty list with connections of houses to batteries
    first = True
    shortest = None
    total_distance = 0
    house = 0
    capacity_reached = False
    shortest_index = None

    # Check possible battery/house combinations
    for distance in product(*self.distances):

        # Index of batteries list
        index = tuple(row.index(elem) for row, elem in zip((self.distances), distance))
        list_index = list(index)

        # Add capacity to batteries and set capacity to 0
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

        # Check if batteries are not full yet
        if capacity_reached == False:
            # Calculate total distance
            total_distance = sum(distance)

            # Check if it is the first value
            if first == True:
                shortest = total_distance
                first = False

            # If not first value, check if total distance smaller than shortest distance
            elif first == False:
                if total_distance < shortest:
                    shortest = total_distance
                    shortest_index = list_index

    # Write down connections of shortest index
    connections = []
    i = 1
    for row in shortest_index:
        house_to_battery = {'house': i, 'battery': (row + 1),
                    'distance': self.distances[i - 1][row], 'max_output_house': self.houses[i].max_output}
        connections.append(house_to_battery)
        i += 1

    # Save the shortest generated distance as total distance    
    total_distance = shortest

    return [total_distance, connections]
