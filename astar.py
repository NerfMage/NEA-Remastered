import rooms


class Node:
    def __init__(self, parent, coords, h):
        self.parent = parent
        self.coords = coords
        self.h = h

    def get_coords(self):
        return [self.coords[0], self.coords[1]]

    def get_tile(self):
        return rooms.TILES[self.coords[0]][self.coords[1]]

    def get_h(self):
        return self.h

    def get_parent(self):
        return self.parent


def manhattan(start, end) -> int:
    dist_x = abs(end.get_center('x') - start.get_center('x'))
    dist_y = abs(end.get_center('y') - start.get_center('y'))

    return dist_x + dist_y


def astar(start, end) -> list:
    currentNode = Node(None, start.get_map_coords(), 999)
    openList = [currentNode]
    closedList = []

    while currentNode.get_coords() != end.get_map_coords():
        openList.remove(currentNode)
        closedList.append(currentNode.get_coords())

        for tile in rooms.get_surrounding(currentNode.get_tile()):
            if tile.get_map_coords() not in closedList:
                if not any(tile.get_map_coords() == node.get_coords() for node in openList):
                    # Checks if the tile hasnota lreadybeen asigned a node
                    openList.append(Node(currentNode, tile.get_map_coords(), manhattan(end, tile)))

        if len(openList) == 0:
            return [start]

        currentNode = openList[-1]
        for node in openList:
            if node.get_h() < currentNode.get_h():
                currentNode = node

    path = [end]
    while currentNode.get_parent() is not None:
        path.append(rooms.TILES[currentNode.get_parent().get_coords()[0]][currentNode.get_parent().get_coords()[1]])
        currentNode = currentNode.get_parent()

    for _ in closedList:
        del _

    for _ in openList:
        del _

    return path
