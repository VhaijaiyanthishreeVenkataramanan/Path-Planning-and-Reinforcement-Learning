Q-Learning (10 pts)

Implement an agent that uses Q-learning to learn how to navigate the stochastic version of
this grid world to reach a goal (high reward area). To indicate that a location is a goal, the
agent should receive a high reward (e.g., 100) for reaching that location. The agent should
explore the map in episodes; an episode should end if the agent either reaches the goal or
the episode lasts beyond a fixed length of time (e.g. 150 steps). Episodes can start at
different starting locations. During the learning period, the agent should use an exploration
policy to select its methods; you can use any of the methods we discussed in class
(e.g. greedy, softmax, exploration bonus). Whenever the agent takes an action, it should
update its Q-table, using the Q-learning rule. Try modifying the values of α, γ, and the
number of training episodes to see how it affects the performance.

Once your agent has finished learning, test to make sure that it can reach the goal from
two different locations in the world using the learned Q-table and a max exploration policy
such that the agent always selects the highest valued action for the current state.

Please include the following for your writeup:

• the transition and reward functions used in your world 
• a description of the exploration policy
• description of the Q-learning rule implementation
• a heatmap of the final Q-table (post-learning)
• the learning and training parameters (number of episodes, α, and γ)
• two example action sequences generated using your policy and executed in the stochastic world
