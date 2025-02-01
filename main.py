import sys
import numpy as np
import gymnasium
import HSREnv
from HSREnv.envs.hsr import HSR

if __name__ == "__main__":
    #env = gymnasium.make("HSREnv-v1")

    game = HSR()
    while True:
        game.view("human")

    