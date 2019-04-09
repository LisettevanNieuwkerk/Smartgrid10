class House(object):
    """
    Representation of a house in SmartGrid
    """

    def __init__(self, id, xpos, ypos, max_output):
        """
        Initiazes a House
        """
        self.id = id
        self.xpos = xpos
        self.ypos = ypos
        self.max_output = max_output

    # def distance_battery(self):
    #     find closest distance to a battery

    def __str__(self):
        return f"HouseId {self.id} (xpos: {self.xpos}, ypos: {self.ypos}, max_output: {self.max_output})"
