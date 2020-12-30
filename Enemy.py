import pygame

from MovingObject import MovingObject


class Enemy():
    def __init__(self, velocity, directionX, directionY):
        self.pieces = []
        self.width = 25
        self.height = 25

        self.movePix = 5

        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        self.directionX = directionX
        self.directionY = directionY

        self.counter = 0
        self.velocity = velocity

    def update(self, mushrooms):
        self.swapPieces()
        self.checkPieceZero(mushrooms)

    def checkPieceZero(self, mushrooms):
        if 0 < self.pieces[0].curveCounter < 5:
            self.curve(0)
            self.pieces[0].curveCounter += 1
        else:
            self.pieces[0].curveCounter = 0
            newX = self.pieces[0].rect.x + self.pieces[0].directionX * self.width
            if (not (newX > self.screenwidth - self.width / 2 or newX < -5)) and (not (pygame.sprite.spritecollide(self.pieces[0], mushrooms, False))):
                self.pieces[0].curveCounter = 0
                self.pieces[0].rect.x += self.pieces[0].directionX * self.movePix
            elif pygame.sprite.spritecollide(self.pieces[0], mushrooms, False):
                self.curve(0)
                self.pieces[0].curveCounter += 1
            elif newX > self.screenwidth - self.width / 2 or newX < 0:
                self.curve(0)
                self.pieces[0].curveCounter += 1
        if self.counter == 3:
            self.pieces[0].updateFeetPosition()
            self.counter = 0
        else:
            self.counter += 1
            self.pieces[0].FeetPosition()

    def swapPieces(self):
        for i in range(1, len(self.pieces)):
            if 0 < self.pieces[-i].curveCounter < 5:
                self.curve(-i)
                self.pieces[-i].curveCounter += 1
            else:
                if self.pieces[-(i + 1)].curveCounter == 5:
                    self.pieces[-(i + 1)].curveCounter = 0
                    self.pieces[-i].curveCounter = 0
                    self.curve(-i)
                    self.pieces[-i].curveCounter += 1
                else:
                    self.pieces[-i].curveCounter = 0
                    self.pieces[-i].rect.x += self.pieces[-i].directionX * self.movePix
            if self.counter == 3:
                self.pieces[-i].updateFeetPosition()
            else:
                self.pieces[-i].FeetPosition()

    def curve(self, i):
        newY = self.pieces[i].rect.y + self.pieces[i].directionY * self.height
        if newY <= 25 or newY >= self.screenheight:
            self.pieces[i].directionY *= -1
        self.pieces[i].rect.x += self.pieces[i].directionX * self.movePix
        self.pieces[i].rect.y += self.pieces[i].directionY * self.movePix
        if self.pieces[i].curveCounter == 2:
            self.pieces[i].directionX *= -1
            self.rotateEnemyPiece(i)
        if self.pieces[i].curveCounter == 4:
            self.rotateEnemyPiece(i)

    def rotateEnemyPiece(self, i):
        if self.pieces[i].directionY == 1:
            if self.pieces[i].directionX == 1:
                self.pieces[i].rotateImageWAngle(270)
                self.pieces[i].totalAngle += 270
            elif self.pieces[i].directionX == -1:
                self.pieces[i].rotateImageWAngle(90)
                self.pieces[i].totalAngle += 90
        elif self.pieces[i].directionY == -1:
            if self.pieces[i].directionX == 1:
                self.pieces[i].rotateImageWAngle(90)
                self.pieces[i].totalAngle += 90
            elif self.pieces[i].directionX == -1:
                self.pieces[i].rotateImageWAngle(270)
                self.pieces[i].totalAngle += 270
