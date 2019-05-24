import math
import decimal
import random
import visualiser as vis

def simulated_annealing (self, results):
    """
    This is the algorithm for simulated annealing
    """
    total_distance = results[0]
    connections = results[1]
    print(f"Start: {total_distance}")

    best_result = total_distance
    best_connections = connections

    # Cool Schema values
    T = 150.0
    T_min = 0.00001
    alpha = 0.9
    j = 0
    distances_total = dict()
    key = 1

    #While temperature is not zero
    while T > T_min:
        i = 1
        while i <= 1000:

            # Adds the distance to a dict with the number of succesful run as its key
            distances_total[key] = total_distance
            key += 1
            new_distance = None
            # Find neighbouring solution
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

                            new_distance1 = self.distances[houseN1 - 1][battery2 - 1]
                            new_distance2 = self.distances[houseN2 - 1][battery1 - 1]

                            new_distance = total_distance - old_distance1 - old_distance2
                            new_distance = new_distance + new_distance1 + new_distance2

            # Check if it is a acceptable solution
            delta = total_distance - new_distance
            r = random.random()
            if delta >= 0 or (math.exp(delta / T)) > r:
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
            # print(total_distance)
            if best_result >= total_distance:
                best_result = total_distance
                best_connections = connections

            i += 1
            j += 1
        T *= alpha

    # Saves the dict to a csv
    vis.dict_to_csv(distances_total)

    return [total_distance, connections]
