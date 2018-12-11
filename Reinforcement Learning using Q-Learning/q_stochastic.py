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

start = World.start # (0, World.y - 1)
current = start
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
    # policy[1][1] = "#"

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
    # prev_score = score
    (curr_x, curr_y) = current
    # r = 0

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
        # score += goal_reward
        print "**********************  Success score = ", score
    elif current in pit:
        World.restart = True
        # score += pit_reward
        print "**********************  Fail score = ", score

    World.move_bot(current[0], current[1])
    # (act, val) = max_q(s)
    r = move_reward #+ val

    score += r
    # r = score - prev_score
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


def get_state(act):
    global current
    c = current
    act_state = c
    if act == actions[1]:
        act_state = (c[0]-1 if c[0]-1 >= 0 else c[0], c[1])
    elif act == actions[3]:
        act_state = (c[0]+1 if c[0]+1 < World.x else c[0], c[1])
    elif act == actions[0]:
        act_state = (c[0], c[1]-1 if c[1]-1 >= 0 else c[1])
    elif act == actions[2]:
        act_state = (c[0], c[1]+1 if c[1]+1 < World.y else c[1])

    if act_state in walls:
        act_state = c
    return act_state


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
    global alpha, discount, current, score, epsilon, discount, episodes
    iter = 1
    init()

    while iter != -1:
        if World.flag == None:
            quit()
        if World.flag is True:
            continue

        (max_act, max_val) = max_q(current)
        print "***********************************************************"
        print "Current: ", current, max_q(current)

        other_rew = 0
        max_act = random_action(max_act)
        for act in actions:
            if max_act != act:  # and actions[actions.index(max_act) - 2] != act:
                print act
                print get_state(act), max_q(get_state(act))
                other_rew += (0.1 * (max_q(get_state(act)))[1])

        (s, a, reward, s2) = move(random_action(max_act))
        # (s, a, reward, s2) = move((max_act))
        print "Move: ", (s, a, reward, s2)

        (max_act2, max_val2) = max_q(s2)
        print "Next: ", s2, max_q(s2)
        print reward, "+", discount, "* (0.8 *", max_val2, "+", other_rew, "+", 0.1*max_q(s)[1], ")"

        # reward_s2 = reward + discount*(max_val2)
        # reward_s2 = reward + discount*(0.7*max_val2 + other_rew)
        reward_s2 = reward + discount*(0.6*max_val2 + other_rew + 0.1*max_q(s)[1])
        print reward, "+", discount, "*", max_val2
        update_q(s, a, alpha, reward_s2)

        print_q()
        # print_policy()
        print "alpha (learning rate): ", alpha
        # raw_input()     # Manual Control

        iter += 1
        print "Iteration: ", iter

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
