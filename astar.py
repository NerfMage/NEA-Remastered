import rooms


class Node:
    def __init__(self, parent, coords, h):
        self.parent = parent
        self.coords = coords
        self.h = h

    def get_coords(self):
        return self.coords

    def get_tile(self):
        return rooms.TILES[self.coords[0]][self.coords[1]]

    def get_h(self):
        return self.h

    def get_parent(self):
        return self.parent


def manhattan(start, end) -> int:
    dist_x = abs(end.get_center()[0] - start.get_center()[0])
    dist_y = abs(end.get_center()[1] - start.get_center()[1])

    return dist_x + dist_y


def astar(start, end) -> list:
    currentNode = Node(None, [start.get_column(), start.get_row()], 999)
    openList = [currentNode]
    closedList = []

    while currentNode.get_coords() != [end.get_column(), end.get_row()]:
        openList.remove(currentNode)
        closedList.append(currentNode.get_coords())

        for tile in rooms.get_surrounding(rooms.TILES[currentNode.get_coords()[0]][currentNode.get_coords()[1]]):
            if tile.get_coords() not in closedList and not tile.return_occupied():
                if tile not in openList:
                    openList.append(Node(currentNode, [tile.get_column(), tile.get_row()], manhattan(tile, end)))

        if len(openList) == 0:
            return [start]

        currentNode = openList[-1]
        for node in openList:
            if node.get_h() < currentNode.get_h():
                currentNode = node

    path = []

    while currentNode.get_parent() is not None:
        path.append(rooms.TILES[currentNode.get_parent().get_coords()[0]][currentNode.get_parent().get_coords()[1]])
        currentNode = currentNode.get_parent()

    for node in closedList:
        del node

    for node in openList:
        del node

    return path
