from house import House
from battery import Battery

class Inventory(object):
    """
    Representation of the inventory of a neighbourhood.
    """
        
    def __init__(self):
        self.houses = dict()
        self.batteries = dict()

    def add_house(self, house):
        self.houses[house.id] = house

    def add_battery(self, battery):
        self.batteries[battery.id] = battery
    

