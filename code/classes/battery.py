class Battery(object):
    """
    Representation of a house in SmartGrid
    """

    def __init__(self, id, xpos, ypos, capacity):
        """
        Initiazes a House
        """
        self.id = id
        self.xpos = xpos
        self.ypos = ypos
        self.capacity = capacity
        self.currentCapacity = 0

    def __str__(self):
        return f"BatteryId {self.id} (xpos: {self.xpos}, ypos: {self.ypos}, capcity: {self.capacity}, current_capacity: {self.currentCapacity})"
