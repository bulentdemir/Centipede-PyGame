import pygame
import random

from MovingObject import MovingObject
from Mushroom import Mushroom


class Ghost(MovingObject):
    def __init__(self):
        image = pygame.image.load("images/ghost/ghost1.gif")
        #x = self.screenwidth - 25
        #y = random.randint(0, self.screenheight / (25 * 2) - 1) * 25
        MovingObject.__init__(self, 25, 25, 5, image, 0, 0)

        self.rect.x = self.screenwidth - 25
        self.rect.y = random.randint(0, self.screenheight / (25 * 2) - 1) * 25

        self.imageCode = 1

        self.directionX = -1

    def update(self, level):
        self.changeImage()
        self.addMushroom(level)
        self.move()

    def changeImage(self):
        if self.imageCode == 1:
            self.image = pygame.image.load("images/ghost/ghost2.gif")
            self.imageCode = 2
        elif self.imageCode == 2:
            self.image = pygame.image.load("images/ghost/ghost1.gif")
            self.imageCode = 1

    def addMushroom(self, level):
        if (not pygame.sprite.spritecollide(self, level.MushroomList, False)) and self.rect.x % 25 == 0:
            check = random.choice([True, False])
            if check:
                mushroom = Mushroom(self.rect.x, self.rect.y)
                level.MushroomList.add(mushroom)
                level.levelSprites.add(mushroom)

    def move(self):
        self.rect.x += self.movePix * self.directionX
