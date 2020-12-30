import pygame
from Level import Level


class LevelManager:
    def __init__(self, levelCount):
        self.Levels = []
        self.inTransition = False
        self.levelTimeMax = 100
        self.levelTime = 0
        self.LevelCount = levelCount
        self.createLevels()

    def update(self):
        if self.levelTime < self.levelTimeMax:
            self.levelTime += 1

    def createLevels(self):
        for i in range(self.LevelCount):
            self.Levels.append(Level(i + 1, i * 10 + 50, i + 1, i + 7))
