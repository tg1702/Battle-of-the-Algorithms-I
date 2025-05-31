from collections import defaultdict
class Node():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbours = set()

    def add_neighbour(self, neighbour):
        self.neighbours.add(neighbour)



def reconstruct_path(cameFrom, current):
    total_path = [current]

    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.insert(0, current)

    return total_path

def get_neighbours(current, grid):
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    neighbours = []
    rows = len(grid)
    cols = len(grid[0])
    for d in directions:
        r, c = current[0] + d[0], current[1] + d[1]
        if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 1:
            neighbours.append((r, c))
    
    return neighbours

def heuristic(node, goal):
    # Manhattan distance
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def d(a, b):
    return 1

def a_star(start, goal, grid):
    
    openSet = {start}

    cameFrom = {}

    gScore = defaultdict(lambda: float("inf"))
    gScore[start] = 0

    fScore = defaultdict(lambda: float("inf"))
    fScore[start] = heuristic(start, goal)

    while openSet:
        current = min(openSet, key=lambda x: fScore[x])
        
        if current == goal:
            return reconstruct_path(cameFrom, current)

        openSet.remove(current)

        #print(get_neighbours(current, grid))
        for neighbour in get_neighbours(current, grid):

            #print(neighbour)
            tentative_gScore = gScore[current] + d(current, neighbour)

            #print(tentative_gScore, gScore[neighbour])
            if tentative_gScore < gScore[neighbour]:
                cameFrom[neighbour] = current
                gScore[neighbour] = tentative_gScore
                fScore[neighbour] = tentative_gScore + heuristic(neighbour, goal)
                if neighbour not in openSet:
                    openSet.add(neighbour)

    return None  # No path found