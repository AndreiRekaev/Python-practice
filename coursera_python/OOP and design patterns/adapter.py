class MappingAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def lighten(self, grid):
        dim = (len(grid[0]), len(grid))
        self.adaptee.set_dim(dim)
        lights = []
        obstacles = []
        for i in range(dim[0]):
            for j in range(dim[1]):
                if (grid[j][i] == 1):
                    lights.append((i, j))
                elif (grid[j][i] == -1):
                    obstacles.append((i, j))
        self.adaptee.set_lights(lights)
        self.adaptee.set_obstacles(obstacles)
        return self.adaptee.generate_lights()
