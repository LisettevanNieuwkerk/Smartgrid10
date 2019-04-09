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

    def __str__(self):
        return f"{self.xpos} {self.ypos} {self.output}"
        