In this assignment, you will be designing a physically-embodied agent (aka a robot) that can
learn and plan.

Grid World

You will be learning and planning on an occupancy grid, a discretized map version of the
simulated world that your robot will later use. Squares on the map should either be marked
as occupied or unoccupied. The robot will try to find a path through the unoccupied
squares from its starting position to a designated goal position.

Design a simple grid layout (about 10x10 in size) with some obstacles. Assume that
4-square connectivity exists (up, down, left, and right); no diagonal moves are allowed. For
this assignment you will have both a deterministic world and a stochastic one. In the
deterministic world, actions taken always occur (moving up always takes the robot up). In
the stochastic world, you should have a transition function that moves the robot; a
reasonable one would be to have an action take the robot where it wants to go with
probability 0.6, 0.1 probability of moving in each of the other directions, and 0.1 probability
of remaining in place. Make sure that the agent can never accidentally wander into
occupied regions.

For debugging purposes, it is useful if you have a visual representation of your world and
the ability to load different map configurations. There are no points for this section of the
assignment but you will need to have this for the subsequent sections. 

A* Planning (5 pts)

For the deterministic version of the world, implement an A* planner. You should be able to
plan from different starting positions to different goal states. For the admissible heuristic
(h(x)), you should use the Euclidean distance metric.

For your writeup include:
• pseudocode of your planner
• f, g, and h values for one example map

Please make sure that you submit pseudocode that corresponds to your implementation
rather than merely referencing standard pseudocode for A* (e.g., from Wikipedia).

Robot Planning Demo (5 pts)

Demonstrate that your robot can follow the path generated by the A* planner using one of
the following simulator options. Single person teams only need to show a demonstration or 
video of their planner correctly navigating two different paths in their own grid world
simulation. Multi- person teams should be able to show that they can follow paths in a
continuous world.
