class Battery(object):
    """
    Representation of a battery in SmartGrid
    """

    def __init__(self, id, name, capacity, price):
        """
        Initiazes a Battery
        """
        self.id = id
        self.name = name
        self.price = price
        self.capacity = capacity
        self.currentCapacity = 0
        self.xpos = None
        self.ypos = None


    def __str__(self):
        return f"Battery: {self.id}\nName: {self.name}, x_position: {self.xpos},y_position: {self.ypos}, capcity: {self.capacity}, price: {self.price}, current_capacity: {self.currentCapacity}"
