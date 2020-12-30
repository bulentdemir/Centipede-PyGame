import pygame
import random

from Enemy import Enemy
from EnemyPiece import EnemyPiece
from Mushroom import Mushroom
from Mushroomer import Mushroomer
from Spyder import Spyder
from Ghost import Ghost


class Level:
    def __init__(self, levelCode, mushroomCount, enemyCount, enemyPieceCount):
        self.LevelCode = levelCode
        self.EnemyCount = enemyCount
        self.EnemyPieceCount = enemyPieceCount
        self.EnemyPieces = pygame.sprite.Group()
        self.EnemyList = []
        self.MushroomList = pygame.sprite.Group()
        self.levelSprites = pygame.sprite.Group()
        self.SpyderSprites = pygame.sprite.Group()
        self.MushroomerSprites = pygame.sprite.Group()
        self.GhostSprites = pygame.sprite.Group()
        self.EnemyFeetSprites = pygame.sprite.Group()

        self.MushroomCount = mushroomCount

        self.screenwidth = pygame.display.get_surface().get_width()
        self.screenheight = pygame.display.get_surface().get_height()

        self.createEnemy()
        self.createMushrooms()

        self.enemyCounterMax = int(600 / self.LevelCode)
        self.enemyCounter = 0

    def update(self):
        if self.enemyCounter == self.enemyCounterMax:
            self.addMovingObject()
            self.enemyCounter = 0
        elif self.enemyCounter < self.enemyCounterMax:
            self.enemyCounter += 1

    def addMovingObject(self):
        if self.LevelCode == 1:
            selection = 0
        elif self.LevelCode == 2:
            selection = random.randint(0, 1)
        elif self.LevelCode > 2:
            selection = random.randint(0, 2)
        if selection == 0:
            spyder = Spyder()
            self.SpyderSprites.add(spyder)
            self.levelSprites.add(spyder)
        elif selection == 1:
            mushroomer = Mushroomer()
            self.MushroomerSprites.add(mushroomer)
            self.levelSprites.add(mushroomer)
        else:
            ghost = Ghost()
            self.GhostSprites.add(ghost)
            self.levelSprites.add(ghost)

    def createEnemy(self):
        for i in range(self.EnemyCount):
            direction = random.choice([1, -1])
            if 4 - i > 1:
                enemy = Enemy(4 - i, direction, 1)
            else:
                enemy = Enemy(2, direction, 1)
            self.EnemyList.append(enemy)

            for j in range(self.EnemyPieceCount):
                if direction == -1:
                    if j == 0:
                        self.EnemyList[i].pieces.append(EnemyPiece(self.screenwidth + (j - 1) * 25, (i + 2) * 25, "Head", 0, direction, 1))

                    else:
                        self.EnemyList[i].pieces.append(EnemyPiece(self.screenwidth + (j - 1) * 25, (i + 2) * 25, "Tail", 0, direction, 1))
                elif direction == 1:
                    if j == 0:
                        self.EnemyList[i].pieces.append(EnemyPiece((-j) * 25, (i + 2) * 25, "Head", 180, direction, 1))
                    else:
                        self.EnemyList[i].pieces.append(EnemyPiece((-j) * 25, (i + 2) * 25, "Tail", 180, direction, 1))
                self.EnemyFeetSprites.add(self.EnemyList[i].pieces[-1].feet)
                self.levelSprites.add(self.EnemyList[i].pieces[-1].feet)
            self.EnemyPieces.add(enemy.pieces)
            self.levelSprites.add(enemy.pieces)

    def createMushrooms(self):
        for i in range(self.MushroomCount):
            mushroomWidth = random.randint(1, int(self.screenwidth / 25) - 2)
            mushroomHeight = random.randint(1, int(self.screenheight / 25) - 2)
            mushroomPosX = mushroomWidth * 25
            mushroomPosY = mushroomHeight * 25
            if not (mushroomPosX == 400 and mushroomPosY == 500):
                mushroom = Mushroom(mushroomPosX, mushroomPosY)
                self.MushroomList.add(mushroom)
                self.levelSprites.add(mushroom)