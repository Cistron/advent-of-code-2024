from collections import deque
import numpy as np


with open("/Users/michael_baron/dev/advent-of-code/day12/input.txt") as f:
    plot = f.read().strip().split("\n")

# plot = """RRRRIICCFF
# RRRRIICCCF
# VVRRRCCFFF
# VVRCCCJFFF
# VVVVCJJCFE
# VVIVCCJJEE
# VVIIICJJEE
# MIIIIIJJEE
# MIIISIJEEE
# MMMISSJEEE""".split("\n")

plot = [list(row) for row in plot]
plot = np.array(plot)


def get_neighbors(row, col, plot):
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))
    if row < plot.shape[0] - 1:
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col < plot.shape[1] - 1:
        neighbors.append((row, col + 1))
    return neighbors


def dfs(row, col, plot, visited):
    stack = deque([(row, col)])
    letter = plot[row, col]
    region = {(row, col)}
    while stack:
        crow, ccol = stack.pop()
        if (crow, ccol) in visited:
            continue
        visited.add((crow, ccol))
        for nrow, ncol in get_neighbors(crow, ccol, plot):
            if plot[nrow, ncol] == letter and (nrow, ncol) not in visited:
                stack.append((nrow, ncol))
                region.add((nrow, ncol))
    return letter, region


def find_plots(plot):
    visited = set()
    results = []
    for row in range(plot.shape[0]):
        for col in range(plot.shape[1]):
            if (row, col) not in visited:
                letter, region = dfs(row, col, plot, visited)
                results.append((letter, region))
    return results


# number of edges is equivalent to number of corners
def find_corners(region: set[tuple[int]]) -> int:
    # 2x2 corner patterns
    corners = {
        ((False, False), (False, True)),  # top left outside
        ((False, False), (True, False)),  # top right outside
        ((True, False), (False, False)),  # bottom right outside
        ((False, True), (False, False)),  # bottom left outside
        ((True, True), (True, False)),    # top left inside
        ((True, True), (False, True)),    # top right inside
        ((False, True), (True, True)),    # bottom right inside
        ((True, False), (True, True)),    # bottom left inside
    }

    shared_corners = {
        ((True, False), (False, True)),
        ((False, True), (True, False)),
    }

    confirmed_corners = set()
    confirmed_shared_corners = set()

    for row, col in region:
        # 3x3 grid based on region
        grid = np.zeros((3, 3), dtype=bool)
        for drow in range(-1, 2):
            for dcol in range(-1, 2):
                point = (row + drow, col + dcol)
                if point in region:
                    grid[drow + 1, dcol + 1] = True

        for drow in range(2):
            for dcol in range(2):
                two_by_two = tuple(map(tuple, grid[drow : drow + 2, dcol : dcol + 2]))
                if two_by_two in corners:
                    corner_coords = (row + drow - 1, col + dcol - 1)
                    confirmed_corners.add(corner_coords)
                if two_by_two in shared_corners:
                    corner_coords = (row + drow - 1, col + dcol - 1)
                    confirmed_shared_corners.add(corner_coords)

    return len(confirmed_corners) + len(confirmed_shared_corners) * 2


results = find_plots(plot)

cost = 0
for letter, region in results:
    num_corners = find_corners(region)
    cost += num_corners * len(region)

    # for troubleshooting
    # new_grid = np.zeros(plot.shape, dtype=bool)
    # for row, col in region:
    #     new_grid[row, col] = True

    # for r in new_grid:
    #     print("".join(["#" if c else "." for c in r]))

print(cost)
