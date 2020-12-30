import pygame

from MovingObject import MovingObject


class CentipedeFeet(MovingObject):
    def __init__(self, x, y):
        image = pygame.image.load("images/centipede/centipedeFeet.gif")
        MovingObject.__init__(self, 3, 25, 0, image, x, y)

    def rotateImageWAngle(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)

    def updatePosition(self, x, y):
        self.rect.x = x
        self.rect.y = y