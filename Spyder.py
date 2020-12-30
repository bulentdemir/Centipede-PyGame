import pygame
import random

from MovingObject import MovingObject


class Spyder(MovingObject):
    def __init__(self):
        image = pygame.image.load("images/spyder/spyder1.gif")
        MovingObject.__init__(self, 25, 25, 2, image, 0, 0)

        self.imageNo = 1

        self.rect.x = random.randrange(0, int(self.screenwidth / 25), int(self.screenwidth / 25) - 1) * 25
        self.rect.y = random.randint(1, int(self.screenheight / 25) - 1) * 25

        self.directionX = 1
        self.directionY = 1

        self.counterMax = 4
        self.counter = self.counterMax

    def update(self, mushroomList):
        self.updateMove(mushroomList)
        self.updateImage()
        self.counter += 1

    def updateMove(self, mushroomList):
            self.changeDirection(mushroomList)
            self.rect.x += self.movePix * self.directionX
            self.rect.y += self.movePix * self.directionY

    def changeDirection(self, mushroomList):
        newX = self.rect.x + self.movePix * self.directionX
        newY = self.rect.y + self.movePix * self.directionY
        notInScreen = newX > self.screenwidth - self.width or newX < 0 or newY > self.screenheight - self.height or newY < self.height or (
                    self.directionY == -1 and newY < self.screenheight / 2)
        if notInScreen:
            if self.rect.x > self.screenwidth - 25 or self.rect.x < 0:
                self.directionX *= -1
            elif self.rect.y > self.screenheight - 25 or self.rect.y < 25:
                self.directionY *= -1
            elif self.directionY == -1 and self.rect.y < self.screenheight / 2:
                self.directionY *= -1
        else:
            self.rect.x += self.movePix * self.directionX
            if pygame.sprite.spritecollide(self, mushroomList, True):
                self.rect.x -= self.movePix * self.directionX
                self.directionX *= -1
            else:
                self.rect.y += self.movePix * self.directionY
                if pygame.sprite.spritecollide(self, mushroomList, True):
                    self.rect.y -= self.movePix * self.directionY
                    self.directionY *= -1

    def updateImage(self):
        if self.counter == self.counterMax:
            if self.imageNo == 1:
                self.image = pygame.image.load("images/spyder/spyder2.gif")
                self.imageNo = 2
                self.counter = 0
            elif self.imageNo == 2:
                self.image = pygame.image.load("images/spyder/spyder1.gif")
                self.imageNo = 1
                self.counter =0
