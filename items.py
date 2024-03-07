

class Item:
    def __init__(self, value):
        self.value = value


class Gold(Item):
    def __init__(self, value, x, y):
        super().__init__(value)
        self.x = x
        self.y = y

    def get_coords(self):
        return self.x, self.y

    def get_value(self):
        return self.value
