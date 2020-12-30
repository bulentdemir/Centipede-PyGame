import pygame
from MovingObject import MovingObject

white = (255, 255, 255)


class Bullet(MovingObject):
    def __init__(self, rectX, rectY):
        image = pygame.Surface([2, 15])
        MovingObject.__init__(self, 2, 15, 10, image, rectX, rectY)
        self.image.fill(white)

    def update(self):
        self.move()

    def move(self):
        if self.rect.y >= 0:
            self.rect.y -= self.movePix
