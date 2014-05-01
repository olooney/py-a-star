import a_star
import math
from PIL import Image
from glob import glob
import os.path

class GridProblem(a_star.Problem):
    """Maps the classic "grid" problem to A*. It uses a greyscale image
    as input and treats any point more than 25% black as unpassable."""

    def __init__(self, filename):
        self.map = Image.open(filename).convert("L")

    def _distance(self, a, b):
        return math.sqrt( (a[0] - b[0])**2 + (a[1] - b[1])**2 )
       
    def heuristic(self, point, goal):
        """classic "distance to goal" heuristic."""
        return self._distance(point, goal)
    
    def neighbor_nodes(self, point):
        """move to any of the 8 adjacent squares, as long as it's not black."""

        candidates = [
            (point[0] + 0, point[1] + 1),
            (point[0] + 1, point[1] + 1),
            (point[0] + 1, point[1] + 0),
            (point[0] + 1, point[1] - 1),
            (point[0] + 0, point[1] - 1),
            (point[0] - 1, point[1] - 1),
            (point[0] - 1, point[1] + 0),
            (point[0] - 1, point[1] + 1),
        ]
        return [ point for point in candidates if self._is_passable(point) ]

    def _is_passable(self, point):
        if point[0] < 0 or point[1] < 0:
            return False
        size = self.map.size
        if point[0] >= size[0] or point[1] >= size[1]:
            return False # out-of-bounds
        if self.map.getpixel(point) < 192: 
            return False # mostly black, a "wall"
        return True

    def distance_between_neighbors(self, point, neighbor):
        return self._distance(point, neighbor)


def save_solution(map_filename, path, solution_filename):
    """draws the solution path in red on top of the image and saves it as a new image."""

    img = Image.open(map_filename).convert("RGB")

    for point in path:
        img.putpixel(point, (255, 0, 0))
        
    img.save(solution_filename)
    return img


def solve(filename, start=(0,0), end=(0,0)):
    """solve one problem and save the solution as an image."""

    input_filename = os.path.join('problems', filename)
    output_filename = os.path.join('solutions', filename)

    problem = GridProblem(input_filename)
    path = a_star.find_path(problem, start, end)
    save_solution(input_filename, path, output_filename)

if __name__ == '__main__':
    # solve the four test mazes
    solve('trivial_map.bmp', start=(0, 0), end=(12, 12))
    solve('small_maze.png', start=(0, 100), end=(106,103))
    solve('curved_maze.png', start=(52, 44), end=(437, 664))
    solve('large_maze.gif', start=(82, 0), end=(430,512))



