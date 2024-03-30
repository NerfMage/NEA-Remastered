import rooms


class Node:
    def __init__(self, parent, coords: list, h: int):
        """
        Class to act as Tile proxy in the A* algorithm
        :param parent: The parent node, used to trace the path backwards
        :param coords: The [column, row] of the corresponding Tile
        :param h: The heuristic value, manhattan distance from the destination Tile
        """
        self.parent = parent
        self.coords = coords
        self.h = h

    def get_coords(self) -> list:
        """
        :return: The coordinates of the corresponding Tile as [column, row]
        """
        return [self.coords[0], self.coords[1]]

    def get_tile(self):
        """
        :return: The corresponding Tile
        """
        return rooms.TILES[self.coords[0]][self.coords[1]]

    def get_h(self) -> int:
        """
        :return: The heuristic value, manhattan distance to the end
        """
        return self.h

    def get_parent(self):
        """
        :return: The parent node
        """
        return self.parent


def manhattan(start, end) -> int:
    """
    Function that finds the manhattan distance between two Tiles
    Manhattan distance is horizontal distance + vertical distance
    :param start: First Tile
    :param end: Second Tile
    :return: Distance between Tiles
    """
    dist_x = abs(end.get_center('x') - start.get_center('x'))  # Absolute value ensures outcome is positive
    dist_y = abs(end.get_center('y') - start.get_center('y'))  # Even if dx or dy are negative

    return dist_x + dist_y


def astar(start, end) -> list:
    """
    Function for finding the best path between two Tiles, avoiding obstacles
    Not necessarily fastest as it uses heuristics, but close enough
    :param start: Start Tile
    :param end: Destination Tile
    :return: A list of all the Tiles along the path, in order from end to start as a list of Tiles
    """
    currentNode = Node(None, start.get_map_coords(), 999)
    openList = [currentNode]  # List of all nodes for tiles that have been 'looked at' but not visited
    closedList = []  # List of all coordinates of Tiles that have been visited already

    while currentNode.get_coords() != end.get_map_coords():
        # Moves current node from the openList to the closedList
        openList.remove(currentNode)
        closedList.append(currentNode.get_coords())

        # Checks all Tiles surrounding the current node's Tile
        for tile in rooms.get_surrounding(currentNode.get_tile()):
            if tile.get_map_coords() not in closedList:
                if not any(tile.get_map_coords() == node.get_coords() for node in openList):
                    # Checks if the tile has not already been asigned a node
                    openList.append(Node(currentNode, tile.get_map_coords(), manhattan(end, tile)))

        # Returns the start node if the destination is within the surrounding tiles to avoid bugs
        if len(openList) == 0:
            return [start]

        # Changes currentNode to node from the openList with lowest h value
        currentNode = openList[-1]
        for node in openList:
            if node.get_h() < currentNode.get_h():
                currentNode = node

    # Forms the path by adding all the parents of the nodes
    path = [end]
    while currentNode.get_parent() is not None:
        path.append(rooms.TILES[currentNode.get_parent().get_coords()[0]][currentNode.get_parent().get_coords()[1]])
        currentNode = currentNode.get_parent()

    # Delets all nodes used to save memory
    for _ in openList:
        del _

    return path
