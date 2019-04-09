from house import House
from battery import Battery
import sys
import csv

class SmartGrid():
    """
    This is the main Grid class. It contains all necessary attributes and methods to
    solve the unsolvable problem of the Smart Grid.
    """

    def __init__(self, neighbourhood_name):
        """
        Create houses and batteries for the problem.
        """
        self.houses = self.load_houses(f"wijk{neighbourhood_name}_huizen.csv")
        self.batteries = self.load_batteries(f"wijk{neighbourhood_name}_batterijen.txt")
        # self.inventory = Inventory()

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

    def play(self):
        # Print dictionary of bateries
        #for i in self.batteries:
        #    print(self.batteries[i])

        # Print dictionary of houses
        #for i in self.houses:
        #    print(self.houses[i])

        xdist = 0
        ydist = 0
        kabels = {}
        # Iterate over every house
        for keyh in self.houses:
            # Put house in dict
            house = f"house_{keyh}"
            kabels[house] = {}
            # Itirate over every battery
            for keyb in self.batteries:
                # Calculate manhattan distance from house to battery
                xdist = abs(self.houses[keyh].xpos - self.batteries[keyb].xpos)
                ydist = abs(self.houses[keyh].ypos - self.batteries[keyb].ypos)
                manhattandist = xdist + ydist
                # Set battery as key in list of house and add distance
                battery = f"battery_{keyb}"
                kabels[house][battery] = manhattandist
        # Dict with possible distances
        print(kabels)


if __name__ == "__main__":
    smartgrid = SmartGrid(1)
    smartgrid.play()
