import pygame

red = (255, 0, 0)


class Mushroom(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.width = 25
        self.height = 25
        self.live = 3

        self.image = pygame.image.load("images/mushroom/mushroom3.gif")

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def changeImage(self):
        imagePath = "images/mushroom/mushroom" + str(self.live) + ".gif"
        self.image = pygame.image.load(imagePath)