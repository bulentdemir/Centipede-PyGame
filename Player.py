import pygame
from MovingObject import MovingObject

pygame.mixer.init()

from Bullet import Bullet


class Player(MovingObject):

    def __init__(self):
        image = pygame.image.load("images/player/player1.gif")
        MovingObject.__init__(self, 25, 25, 5, image, 0, 0)
        self.imageCode = 1

        self.live = 5
        self.point = 0
        self.level = 1

        self.rect.x = self.screenwidth / 2
        self.rect.y = self.screenheight - 100

        self.counterMax = 9
        self.counter = self.counterMax

        self.rebornCounterMax = 150
        self.rebornCounter = 0

        self.fireSound = pygame.mixer.Sound("sounds/fire.ogg")
        self.activeStuff = pygame.mixer.Sound("sounds/activeStuff.ogg")
        self.mushroomSound = pygame.mixer.Sound("sounds/mushroom.ogg")
        self.liveReduce = pygame.mixer.Sound("sounds/liveReduce.ogg")
        self.levelPassing = pygame.mixer.Sound("sounds/levelPassing.ogg")

        self.isReborn = True

    def reborn(self):
        if self.rebornCounter < self.rebornCounterMax:
            self.rebornCounter += 1
            if self.rebornCounter % 15 == 0:
                if self.imageCode == 1:
                    self.image = pygame.image.load("images/player/player2.gif")
                    self.imageCode = 2
                elif self.imageCode == 2:
                    self.image = pygame.image.load("images/player/player1.gif")
                    self.imageCode = 1
        elif self.rebornCounter == self.rebornCounterMax:
            self.image = pygame.image.load("images/player/player1.gif")
            self.imageCode = 1
            self.isReborn = False

    def handle_event(self, event, bullets, allSprites, mushrooms):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if self.rect.y < self.screenheight - self.height:
                    self.moveOnY(1, mushrooms)
            elif event.key == pygame.K_UP:
                if self.rect.y > self.screenheight / 2:
                    self.moveOnY(-1, mushrooms)
            elif event.key == pygame.K_LEFT:
                if self.rect.x > 0:
                    self.moveOnX(-1, mushrooms)
            elif event.key == pygame.K_RIGHT:
                if self.rect.x < self.screenwidth - self.width:
                    self.moveOnX(1, mushrooms)
            elif event.key == pygame.K_SPACE:
                if self.counter == self.counterMax:
                    self.createBullet(bullets, allSprites)
        if self.counter != self.counterMax:
            self.counter += 1

    def moveOnY(self, direction, mushrooms):
        self.rect.y += direction * self.movePix
        if pygame.sprite.spritecollide(self, mushrooms, False):
            self.rect.y = self.rect.y - direction * self.movePix

    def moveOnX(self, direction, mushrooms):
        self.rect.x += direction * self.movePix
        if pygame.sprite.spritecollide(self, mushrooms, False):
            self.rect.x -= direction * self.movePix

    def createBullet(self, bullets, allSprites):
        self.fireSound.play()
        bullet = Bullet(self.rect.x + (self.image.get_width() / 2), self.rect.y)
        bullets.add(bullet)
        allSprites.add(bullet)
        self.counter = 0

    def resetPosition(self):
        self.rect.x = self.screenwidth / 2
        self.rect.y = self.screenheight - 100