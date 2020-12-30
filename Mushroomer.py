import pygame
import random

from MovingObject import MovingObject
from Mushroom import Mushroom


class Mushroomer(MovingObject):
    def __init__(self):
        image = pygame.image.load("images/mushroomer.gif")
        MovingObject.__init__(self, 25, 25, 5, image, 0, 25)

        self.rect.x = random.randint(0, self.screenwidth / 25 - 1) * 25

    def update(self, level):
        self.addMushroom(level)
        self.move()

    def addMushroom(self, level):
        if (not pygame.sprite.spritecollide(self, level.MushroomList, False)) and self.rect.y % 25 == 0:
            check = random.choice([True, False])
            if check:
                mushroom = Mushroom(self.rect.x, self.rect.y)
                level.MushroomList.add(mushroom)
                level.levelSprites.add(mushroom)

    def move(self):
        self.rect.y += self.movePix
