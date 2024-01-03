from heapq import heappush, heappop

file = open(".\\2023\\input\\17_sample.txt").readlines()
grid = [list(int(y) for y in list(x.strip())) for x in file]


def add(queue, heat_loss: int, row: int, col: int, dr: int, dc: int, steps: int = 1):
    new_row = row + dr
    new_col = col + dc

    if not (0 <= new_row < len(grid) and 0 <= new_col < len(grid[new_row])):
        return

    heappush(
        queue,
        (
            heat_loss + grid[new_row][new_col],
            new_row,
            new_col,
            dr,
            dc,
            steps,
        ),
    )


visited = set()
priority_queue = [(0, 0, 0, 0, 0, 0)]

while priority_queue:
    heat_loss, row, col, dr, dc, steps = heappop(priority_queue)

    if row == len(grid) - 1 and col == len(grid[row]) - 1:
    # if row == 0 and col == 8:
        print(heat_loss)
        break

    if (row, col, dr, dc, steps) in visited:
        continue

    visited.add((row, col, dr, dc, steps))

    for new_dr, new_dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if (new_dr, new_dc) == (-dr, -dc):
            continue # don't move backwards
        elif (new_dr, new_dc) == (dr, dc) and (dr, dc) != (0, 0):
            if (new_dr, new_dc) == (dr, dc) and steps == 3:
                continue # stop exploring
            else:
                new_steps = steps + 1 # if we move in the same direction, add a step to the counter
        else:
            new_steps = 1 # we are moving in a different direction, reset the step counter
        add(priority_queue, heat_loss, row, col, new_dr, new_dc, new_steps)