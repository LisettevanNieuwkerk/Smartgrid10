from house import House
from battery import Battery
from neighbourhood import Neighbourhood
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
        # self.houses = self.load_houses(f"wijk{neighbourhood_name}_huizen.csv")
        self.batteries = self.load_batteries(f"wijk{neighbourhood_name}_batterijen.txt")
        # self.inventory = Inventory()        

    def load_houses(self, filename):
        """
        Load houses from filename. 
        Return a dictionary of 'id' : House objects.
        """
        # First we parse all the data we need to create the houses with.
        # All parsed lines of data are saved to houses_data.
        houses = dict()
        with open(filename, 'r') as infile:
            reader = csv.reader(infile)
            next(reader)
            id = 0
            for rows in reader:
                xpos = int(rows[0])
                ypos = int(rows[1])
                max_output = float(rows[2])
                id += 1
                house = House(id, xpos, ypos, max_output)
                houses[id] = house

     
    def load_batteries(self, filename):
        """
        Load batteries from filename.
        Return a dictionairt of 'id': Battery objects.
        """
        # First we parse all the data we need to create the houses with.
        # All parsed lines of data are saved to houses_data.  
        batteries = dict()
        with open(filename, "r") as infile:
            next(infile)
            id = 0
            for rows in infile:
                pos = rows[0]
                capacity = rows[1]
                print(pos)
                print(capacity)
                
                # id += 1
                # battery = Battery(id, xpos, ypos, capacity)
                # batteries[id] = battery 



SmartGrid(1)