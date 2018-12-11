import sys
import World
import threading
import time
import numpy as np
import math

grid = World.grid

(x, y) = (World.y, World.x)
walls = World.walls
start = (World.player[1], World.player[0])
cost = 1
goal = (World.goal[1], World.goal[0])

h_grid = [[0 for row in range(y)] for col in range(x)]
print "length:", len(h_grid)
print "Size of grid: ", x, "x", y

delta = [[1, 0],
         [-1, 0],
         [0, 1],
         [0, -1]]
fgh = ["f", "g", "h"]
p = 0.1
D = 1

states = []
fgh_dict = {}


def init_fgh():
    for i in range(World.x):
        for j in range(World.y):
            if (i, j) in walls:        # Obstacle
                continue
            states.append((i, j))


    for state in states:
        temp = {}
        for var in fgh:
                temp[var] = 0
        fgh_dict[state] = temp

init_fgh()


def heuristic(node):
    dx = abs(node[0] - goal[0])
    dy = abs(node[1] - goal[1])
    if World.eu_or_mh == 'Manhattan':
        return D * (dx + dy)
    else:
        return D * (dx*dx + dy*dy)

def init_h():
    global goal, h_grid, x, y, p
    open_list = []
    closed_list = []
    neighbors = []
    open_list.append(goal)
    closed_list.append(goal)

    while True:
        for curr in open_list:
            for i in range(len(delta)):
                x2 = curr[0] + delta[i][0]
                y2 = curr[1] + delta[i][1]

                if 0 <= x2 < x and 0 <= y2 < y:
                    if (x2, y2) not in closed_list:     # and (x2, y2) not in open_list:
                        closed_list.append((x2, y2))
                        neighbors.append((x2, y2))

        for m, n in neighbors:
            h_grid[m][n] = heuristic((m,n))

        open_list = neighbors
        neighbors = []
        if len(closed_list) == x*y:
            break

print "\nGrid Map: \n", np.array(grid)


def search():
    global x, y, p, states, fgh_dict
    cost_grid = [[-1 for row in range(y)] for col in range(x)]
    open = []
    open.append((0, 0, start[0], start[1]))
    closed = []
    closed.append(start)
    expanded_grid = [[-1 for row in range(y)] for col in range(x)]
    expanded_grid_states = []
    action_grid = [[-1 for row in range(y)] for col in range(x)]
    expand_count = 0
    g = 0

    #   Calculation of f, g and h for each state
    while True:
        if World.flag is True:
                continue
        init_h()
        if len(open) == 0:
            World.noPath()
            print "No Path exists!"
            sys.exit()
        else:
            open.sort()
            open.reverse()
            temp = open.pop()
            # print "Picked: ", temp
            # print "Open List: ", open
            # print "Closed List: ", closed
            (f, g, tx, ty) = (temp[0], temp[1], temp[2], temp[3])

            expanded_grid[tx][ty] = expand_count
            expand_count += 1
            expanded_grid_states.append((ty, tx))
            # World.showExpand(expanded_grid_states)
            # time.sleep((World.w1.get() + 0.1)/ 100)

            if (tx, ty) == goal:
                print "Goal Found!!"
                break

            for i in range(len(delta)):
                dx = tx + delta[i][0]
                dy = ty + delta[i][1]
                # print (dx, dy)

                if 0 <= dx < x and 0 <= dy < y:
                    if (dx, dy) not in closed and (dy, dx) not in walls:     # and (x2, y2) not in open_list:
                        g2 = g + cost

                        dx1 = tx - goal[0]
                        dy1 = ty - goal[1]
                        dx2 = start[0] - goal[0]
                        dy2 = start[1] - goal[1]
                        cross = abs(dx1*dy2 - dx2*dy1)
                        h2 = h_grid[dx][dy]
                        #   Pick one of the below two Tie breaker policy
                        # h2 = h2 + cross*0.1
                        h2 *= (1 + p)

                        f2 = g2 + h2
                        open.append((f2, g2, dx, dy))
                        closed.append((dx, dy))
                        cost_grid[dx][dy] = g2
                        action_grid[dx][dy] = i
                        fgh_dict[(dy, dx)] = {'f':f2, 'g':g2, 'h':h2}

    print "action: \n", np.array(action_grid)

    #   Back tracing the shortest path from goal
    g1 = goal[0]
    g2 = goal[1]
    policy = []
    policy.append((g2, g1))
    while g1 != start[0] or g2 != start[1] :
        x2 = g1 - delta[action_grid[g1][g2]][0]
        y2 = g2 - delta[action_grid[g1][g2]][1]
        policy.append((y2, x2))
        g1 = x2
        g2 = y2


    World.showExpand(expanded_grid_states, fgh_dict)

    World.move()
    policy.reverse()
    for p in policy:
        World.move_bot(p[0], p[1])
        time.sleep((World.w1.get() + 0.1)/ 100)

    # print "\nOpened map: \n", np.array(grid)
    print "\nHeuristic (h): \n", np.array(h_grid)
    print "\nExpanded grid: \n", np.array(expanded_grid)
    print "\nCost (g): \n", np.array(cost_grid)
    print "\nExplored Coordinates: ", expanded_grid_states
    print "Path Coordinates: ", policy


t = threading.Thread(target=search)
t.daemon = True
t.start()
World.begin()
