import numpy as np
import math as math
import World
import threading
import time
import random

# grid = [[0, 0, 0, 0],
#         [0, -99, 0, 0],
#         [0, 0, 0, 0],
#         [0, 0, 0, 0]]
grid = World.grid
actions = World.actions #   ["up", "left", "down", "right"]
policy_sign = ["^", "<", "v", ">"]
states = []

# start = World.start # (0, World.y - 1)
current = World.start
walls = World.walls
goal = World.goal   #   (World.specials[1][0], World.specials[1][1])
pit = World.pit #   [(World.specials[0][0], World.specials[0][1])]
print "Goal: ", goal
print "Pit: ", pit
print "Walls: ", walls

Q = {}
discount = World.discount
alpha = 1
score = 1
move_reward = -0.04
goal_reward = 1
pit_reward = -1
move_pass = 0.8
move_fail = 0.1
move_action = [-1, 0, 1]
epsilon = 0.1
episodes = 10000
steps = 300


def init():
    for i in range(World.x):
        for j in range(World.y):
            if (i, j) in walls:        # Obstacle
                continue
            states.append((i, j))


    for state in states:
        temp = {}
        for action in actions:
            if state == goal:
                temp[action] = goal_reward
            elif state in pit:
                temp[action] = pit_reward
            else:
                temp[action] = 0.1
                World.set_color(state, action, temp[action])
        Q[state] = temp


def print_q():
    for state in states:
        if state == goal:
            print "Goal ", state, " : ", Q[state]
        elif state in pit:
            print "Pit ", state, " : ", Q[state]
        else:
            print state, " : ", Q[state]


def print_policy():
    global grid
    policy = [[" " for col in grid[0]] for row in grid]

    for s in Q:
        (a, b) = s
        (act, val) = max_q(s)
        if s == goal:
            policy[a][b] = str(goal_reward)
            grid[a][b] = goal_reward
        elif s == pit:
            policy[a][b] = str(pit_reward)
            grid[a][b] = pit_reward
        else:
            policy[a][b] = policy_sign[actions.index(act)]
            grid[a][b] = format(val, '.2f')
    print np.array(grid)
    print np.array(policy)


def move(action):
    global current, score
    s = current
    (curr_x, curr_y) = current

    if action == actions[1]:
        current = (curr_x-1 if curr_x-1 >= 0 else curr_x, curr_y)
    elif action == actions[3]:
        current = (curr_x+1 if curr_x+1 < World.x else curr_x, curr_y)
    elif action == actions[0]:
        current = (curr_x, curr_y-1 if curr_y-1 >= 0 else curr_y)
    elif action == actions[2]:
        current = (curr_x, curr_y+1 if curr_y+1 < World.y else curr_y)

    #   check for goal or pit
    if current in walls:
        current = s
    elif current == goal:
        World.restart = True
        print "**********************  Success score = ", score
    elif current in pit:
        World.restart = True
        print "**********************  Fail score = ", score

    World.move_bot(current[0], current[1])
    r = move_reward

    score += r
    s2 = current
    return s, action, r, s2


def max_q(state):
    q_val = None
    act = None
    for a, q in Q[state].items():
        if q_val is None or q > q_val:
            q_val = q
            act = a
    return act, q_val


def update_q(s, a, alpha, new_q):
    Q[s][a] *= (1 - alpha)
    Q[s][a] += (alpha * new_q)
    World.set_color(s, a, Q[s][a])
    print Q[s][a]


def soft_max(state, tou):
    (a, v) = max_q(state)
    exp_q = math.exp(v/tou)

    sum_exp_q = 0
    for (act, val) in Q[state].items():
        sum_exp_q += math.exp(val/tou)

    soft_value = (exp_q / sum_exp_q)
    return soft_value


def random_action(act):
    random.seed(a=None)
    r = random.random()
    other_actions = []
    for a in actions:
        if a !=act:
            other_actions.append(a)
    print other_actions
    if r >= 1 - epsilon:
        r2 = random.randint(0, 2)
        print "Random action:", other_actions[r2]
        return other_actions[r2]

    else:
        print "Optimum action"
        return act


def q_learn():
    global alpha, discount, current, score, epsilon, episodes
    iter = 1
    init()

    while iter != episodes:
        if World.flag is None:
            quit()
        if World.flag is True:
            continue

        (max_act, max_val) = max_q(current)
        print "***********************************************************"
        print "Current: ", current, max_q(current)

        (s, a, reward, s2) = move(random_action(max_act))
        print "Move: ", (s, a, reward, s2)

        (max_act2, max_val2) = max_q(s2)
        print "Next: ", s2, max_q(s2)
        print reward, "+", discount, "*", max_val2
        update_q(s, a, alpha, reward + discount*max_val2)

        print_q()
        # print_policy()
        print "alpha (learning rate): ", alpha
        # raw_input()

        iter += 1
        print "Iteration: ", iter
        print "Epsilon: ", epsilon

        if World.restart is True:
            current = World.start
            World.move_bot(current[0], current[1])
            World.restart = False
            World.restart_game()
            alpha = pow(iter, -0.1)
            score = 1

        time.sleep((World.w1.get() + 0.1)/ 100)
        epsilon = World.w2.get()
        # epsilon = soft_max(current, iter)
        discount = World.discount
        print "Epsilon: ", epsilon


t = threading.Thread(target=q_learn)
t.daemon = True
t.start()
World.begin()
