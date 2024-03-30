

class Item:
    def __init__(self, value):
        """
        Class for all acquirable items in the game
        Includes droppable and non-droppable
        :param value: The value of the item, in gold
        """
        self.value = value

    def get_value(self) -> int:
        """
        :return: The value of the item
        """
        return self.value


class Gold(Item):
    def __init__(self, value, x, y):
        """
        Class for droppable gold item
        :param value: The value of the gold
        :param x: x-coord
        :param y: y-coord
        """
        super().__init__(value)
        self.x = x
        self.y = y

    def get_coords(self) -> tuple[int, int]:
        """
        :return: The coordinates of the gold
        """
        return self.x, self.y
