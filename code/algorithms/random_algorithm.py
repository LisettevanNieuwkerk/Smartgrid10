import random
import visualiser as vis


def random_solution(self, count):
    """
    Random algorithm > assigns all houses to a random battery & tries other battery when the battery is already full.
    """
    # initialize the values
    highest_score = 0
    first_attempt = True
    best_connections = None
    distances_total = dict()
    key = 1

    # Run multiple times
    for j in range(10000):

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
                battery = random.randint(1, count)
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

            # Adds the distance to a dict with the number of succesful run as its key
            distances_total[key] = total_distance
            key += 1

            if first_attempt == True:
                highest_score = total_distance
                best_connections = connections
                first_attempt = False
            else:
                if total_distance < highest_score:
                    highest_score = total_distance
                    best_connections = connections

    # Saves the dict to a csv
    algorithm = "random"
    vis.dict_to_csv(distances_total, algorithm)

    return [highest_score, best_connections]
