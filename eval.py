#!/usr/bin/env python
""" Basic Stable-Baselines3 tester on Gymnasium environments.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Inaki Vazquez"
__email__ = "ivazquez@deusto.es"
__license__ = "GPLv3"

import argparse
import sys

from stable_baselines3 import PPO, DQN, SAC, A2C, DDPG, TD3
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import CheckpointCallback

import gymnasium as gym
import urgym.envs
from urgym.algos import ActionSAC
from stable_baselines3.common.utils import set_random_seed

parser = argparse.ArgumentParser(description='Train an environment with an SB3 algorithm and then render 10 episodes.')
parser.add_argument('-e', '--env', type=str, default="CartPole-v1", help='environment to test (e.g. CartPole-v1)')
parser.add_argument('-a', '--algo', type=str, default='PPO',
					help='algorithm to test from SB3, such as PPO (default), SAC, DQN... using default hyperparameters')
parser.add_argument('-p', '--policy', type=str, required=True, help='policy to load for evaluation')
parser.add_argument('-n', '--nepisodes', type=int, default=10, help='number of episodes to evaluate')

args = parser.parse_args()

str_env = args.env
str_algo = args.algo
algo = getattr(sys.modules[__name__], str_algo) # Obtains the classname based on the string
n_episodes = args.nepisodes
policy_file = args.policy

set_random_seed(42)

env = gym.make(str_env, render_mode='human')
env = Monitor(env)
model = algo.load(policy_file, env)

# Evaluate the agent
total_reward = 0
print(f"Evaluating for {n_episodes} episodes...")

for i in range(n_episodes): # episodes
	print(f"Executing episode {i}... ", end="", flush=True)
	observation,_ = env.reset()
	episode_reward = 0.0
	while True:
		action, _states = model.predict(observation, deterministic=True)
		observation, reward, terminated, truncated, info = env.step(action)
		episode_reward += reward
		if terminated or truncated:
			print(f"reward: {episode_reward:.2f}")
			total_reward += episode_reward
			# observation,_ = env.reset() # Not required, automatic reset
			break
print(f"Mean reward: {total_reward/n_episodes:.2f}")

env.close()

