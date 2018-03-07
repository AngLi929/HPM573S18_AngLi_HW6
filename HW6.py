import numpy as np
import scr.FigureSupport as figureLibrary
from enum import Enum
import scr.SamplePathClass as PathCls
import scr.StatisticalClasses as Stat


class Game(object):
    def __init__(self, id, prob_head):
        self._id = id
        self._rnd = np.random
        self._rnd.seed(id)
        self._probHead = prob_head  # probability of flipping a head
        self._countWins = 0  # number of wins, set to 0 to begin

    def simulate(self, n_of_flips):

        count_tails = 0  # number of consecutive tails so far, set to 0 to begin

        # flip the coin 20 times
        for i in range(n_of_flips):

            # in the case of flipping a heads
            if self._rnd.random_sample() < self._probHead:
                if count_tails >= 2:  # if the series is ..., T, T, H
                    self._countWins += 1  # increase the number of wins by 1
                count_tails = 0  # the tails counter needs to be reset to 0 because a heads was flipped

            # in the case of flipping a tails
            else:
                count_tails += 1  # increase tails count by one

    def get_reward(self):
        # calculate the reward from playing a single game
        return 100*self._countWins - 250


class SetOfGames:
    def __init__(self, prob_head, n_games):
        self._gameRewards = [] # create an empty list where rewards will be stored

        self._sumStat_Rewards = None
        # simulate the games
        for n in range(n_games):
            # create a new game
            game = Game(id=n, prob_head=prob_head)
            # simulate the game with 20 flips
            game.simulate(20)
            # store the reward
            self._gameRewards.append(game.get_reward())
        self._sumStat_Rewards=Stat.SummaryStat('Reward', self._gameRewards)

    def get_ave_reward(self):
        """ returns the average reward from all games"""
        return sum(self._gameRewards) / len(self._gameRewards)

    def get_reward_list(self):
        """ returns all the rewards from all game to later be used for creation of histogram """
        return self._gameRewards


    def get_max(self):
        """ returns maximum reward"""
        return max(self._gameRewards)

    def get_min(self):
        """ returns minimum reward"""
        return min(self._gameRewards)

    def get_probability_loss(self):
        """ returns the probability of a loss """
        count_loss = 0
        for value in self._gameRewards:
            if value < 0:
                count_loss += 1
        return count_loss / len(self._gameRewards)


    def get_reward_CI(self, alpha):
        return self._sumStat_Rewards.get_t_CI(alpha)

    def get_reward_PI(self, alpha):
        return self._sumStat_Rewards.get_PI(alpha)

# Question 1

trial = SetOfGames(prob_head=0.5, n_games=1000)
print("The 95% CI of expected reward is:", trial.get_reward_CI(0.05))

# Question 2

#Interpretation: We are 95% confident that the interval between -31.79 and -20.00 contains the true mean of net rewards

# Question 3
# Casino Owner -- Steady State -- Confidence Interval
A = SetOfGames(prob_head=0.5, n_games=10000)
print("The average expected reward is:", A.get_ave_reward())
print("The 95% CI of expected reward is:", A.get_reward_CI(0.05))
#Interpretation: We are 95% confident that the interval between -26.04 and -22.24 contains the true mean of net rewards

# Gambler -- Transient State -- Projection Interval
B = SetOfGames(prob_head=0.5, n_games=10)
print("The average expected reward is:", B.get_ave_reward())
print("The 95% CI of expected reward is:", B.get_reward_PI(0.05))
#Interpretation: There are 95% percent of probability that next reward of flip will fall between -227.5 to 50.0