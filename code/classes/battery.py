class Battery(object):
    """
    Representation of a house in SmartGrid
    """

    def __init__(self, id, name, xpos, ypos, capacity, price):
        """
        Initiazes a House
        """
        self.id = id
        self.name = name
        self.xpos = xpos
        self.ypos = ypos
        self.capacity = capacity
        self.price = price
        self.currentCapacity = 0

    def __str__(self):
        return f"BatteryID: {self.id} \n\
        name: {self.name}, x_position: {self.xpos}, y_position: {self.ypos}, capcity: {self.capacity}, price: {self.price}, current_capacity: {self.currentCapacity}"
