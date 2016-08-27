#!/usr/bin/env python
# -*- coding: utf-8 -*-

# EXTRA CREDIT:
#
# Create a program that will play the Greed Game.
# Rules for the game are in GREED_RULES.TXT.
#
# You already have a DiceSet class and score function you can use.
# Write a player class and a Game class to complete the project.  This
# is a free form assignment, so approach it however you desire.

from runner.koan import *
from about_dice_project import DiceSet
from about_scoring_project import score


class AboutExtraCredit(Koan):
    # Write tests here. If you need extra test classes add them to the
    # test suite in runner/path_to_enlightenment.py
    def test_extra_credit_task(self):
        pass

    class Player(object):
    def __init__(self, name):
        self.name = name
        self.dice = DiceSet()

    def __str__(self):
        return self.name

    def roll(self, numDice):
        self.dice.roll(numDice)
        return score(self.dice.values), self.dice.values

    class Game(object):
        def __init__(self, players):
            self.players = players
            self.goal = 1500
            self.numDice = 5
            self.scores = dict((p, 0) for p in players)

        def play(self):
            if len(self.players) < 2:
                print 'need more than 2 players to play'
                return
            isFinalRound, endGame = False, False
            while True:
                for player in self.players:
                    if endGame:
                        break
                    print "%s's turn" % player, '-' * 40
                    s, vals = player.roll(self.numDice)
                    if s == 0:
                        print "%s rolled 0 score, next player's turn" % player
                        continue
                    else:
                        print '%s rolled %s, got %d' % (player, vals, s)
                        c = self.count_unscoring_dice(vals)
                        while raw_input('continue to roll? (y|n)').lower()[0] == 'y':
                            c = self.numDice if c == 0 else c
                            newS, newVals = player.roll(c)
                            print '%s rolled %s, got %d' % (player, newVals, newS)
                            if newS == 0:
                                print "%s rolled 0 score, next player's turn" % player
                                s = 0
                                break
                            else:
                                s += newS
                                c = self.count_unscoring_dice(newVals)
                    if s >= 300:
                        self.scores[player] += s
                    print '%s got %d for this turn, total %d' % (player, s, self.scores[player])
                    if self.scores[player] >= self.goal:
                        print 'Final round', '=' * 50
                        isFinalRound = True
                if endGame:
                    self.print_scores()
                    break
                if isFinalRound:
                    endGame = True

        def count_unscoring_dice(self, vals):
            cnts = 0
            for us in [2, 3, 4, 6]:
                c = vals.count(us)
                cnts += c if c < 3 else 0
            return cnts

        def enter_final(self):
            return any(s >= self.goal for s in self.scores.itervalues())

        def print_scores(self):
            print 'final scores', '+' * 50
            for p, s in self.scores.iteritems():
                print p, s
