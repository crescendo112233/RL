import numpy as np
import random
from data_structure import p_tree


class cache:
    def __init__(self):
        self.state = None
        self.achieved_goal = None  # ?
        self.observation = None
        self.done = False
        self.step_count = 0
        self.episod_reward = 0
        self.reward = 0
        self.bias = 0.001
        self.tree = p_tree.p_tree()

    def reset(self):
        self.tree.randomly_init_branch()
        self.tree.randomly_add_video(5000)
        self.state = np.array(self.tree.get_state(), dtype=float)
        request_column = np.log(self.bias + self.state[:, 3])
        self.state[:, 3] = request_column
        self.episod_reward = 0
        self.reward = 0
        print(self.state)

    def step(self, action, observation=None):  # action = ["top_tag_index", "sub_tag_index", "0/1"]
        self.step_count += 1
        if observation is None:
            self.observation = self.get_observation()
        else:
            self.observation = observation


    def get_observation(self): # simulate real request frequency
        observation = [0, 0, "BV1234567891"]
        return observation


c = cache()
c.reset()