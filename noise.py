
import random
import math

def smooth(inp):
    newgrid = [[0 for x in inp[0]] for y in inp]
    for i in range(len(inp)):
        for j in range(len(inp[0])):
            neighbours = [inp[i][j]]
            orthogonal = 0.5
            diagonal = 0.5/math.sqrt(2)
            weight = [1]
            try:
                neighbours.append(orthogonal * inp[i-1][j])
                weight.append(orthogonal)
            except:
                pass
            try:
                neighbours.append(orthogonal * inp[i+1][j])
                weight.append(orthogonal)
            except:
                pass
            try:
                neighbours.append(orthogonal * inp[i][j-1])
                weight.append(orthogonal)
            except:
                pass
            try:
                neighbours.append(orthogonal * inp[i][j+1])
                weight.append(orthogonal)
            except:
                pass
            try:
                neighbours.append(diagonal * inp[i-1][j-1])
                weight.append(diagonal)
            except:
                pass
            try:
                neighbours.append(diagonal * inp[i+1][j+1])
                weight.append(diagonal)
            except:
                pass
            try:
                neighbours.append(diagonal * inp[i-1][j+1])
                weight.append(diagonal)
            except:
                pass
            try:
                neighbours.append(diagonal * inp[i+1][j-1])
                weight.append(diagonal)
            except:
                pass
            newgrid[i][j] = sum(neighbours) / sum(weight)
    return newgrid

def disp(inp):
    s = ""
    for line in inp:
        s += " ".join(map(str, line)) + "\n"
    print(s)


def grid_max(grid):
    maximum = 0
    for line in grid:
        for x in line:
            maximum = max(maximum, x)
    return maximum

def map_noise_to_ids(grid, ids):
    # partition [0,max] into equally sized intervals, one interval for each id in ids.
    maxm = grid_max(grid)
    #disp(grid)
    print(maxm)
    num_intervals = len(ids)
    interval_size = maxm / num_intervals
    interval_borders = [interval_size * (1+x) for x in range(num_intervals)]
    def get_index(x, borders):
        for i,b in enumerate(borders):
            if x <= b:
                return i
        return len(borders)-1
    newgrid = [[0 for x in grid[0]] for y in grid]
    for i, line in enumerate(grid):
        for j, elem in enumerate(line):
            newgrid[i][j] = ids[get_index(elem, interval_borders)]
    return newgrid

def smooth_noise(width, height, iterations):
    grid = [[random.expovariate(0.1) for x in range(width)] for y in range(height)]
    #plt.imshow(grid)
    #plt.show()
    for i in range(iterations):
        grid = smooth(grid)
        #plt.imshow(grid)
        #plt.show()
    return grid

