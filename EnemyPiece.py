import pygame
import random
from MovingObject import MovingObject
from CentipedeFeet import CentipedeFeet

red = (255, 0, 0)


class EnemyPiece(MovingObject):
    def __init__(self, x, y, image, angle, directionX, directionY):
        image = pygame.transform.rotate(pygame.image.load("images/centipede/centipede" + image + ".gif"), angle)
        MovingObject.__init__(self, 23, 23, 5, image, x, y)

        self.totalAngle = angle
        self.directionX = directionX
        self.directionY = directionY
        self.curveCounter = 0
        self.feet = CentipedeFeet(self.rect.x, self.rect.y)
        self.feetPosition = random.randint(1, 3)
        self.updateFeetPosition()

    def updateImageWAngle(self, image):
        self.image = pygame.image.load("images/centipede/centipede" + image + ".gif")
        self.image = pygame.transform.rotate(self.image, self.totalAngle % 360)

    def rotateImageWAngle(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)

    def updateFeetPosition(self):
        self.FeetPosition()
        if self.feetPosition < 3:
            self.feetPosition += 1
        else:
            self.feetPosition = 0

    def FeetPosition(self):
        global posX, posY
        if self.feetPosition == 1:
            if self.directionX == 1:
                posX = int(self.rect.x)
            elif self.directionX == -1:
                posX = int(self.rect.x + self.width)
            posY = self.rect.y
        elif self.feetPosition == 2:
            posX = int(self.rect.x + self.width / 2)
            posY = self.rect.y
        elif self.feetPosition == 3:
            if self.directionX == 1:
                posX = int(self.rect.x + self.width)
            elif self.directionX == -1:
                posX = int(self.rect.x)
            posY = self.rect.y
        self.feet.updatePosition(posX, posY)
