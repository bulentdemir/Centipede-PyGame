import pygame

class MovingObject(pygame.sprite.Sprite):
    def __init__(self, width, height, movePix, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height

        self.movePix = movePix

        self.image = image

        self.rect = self.image.get_rect()

        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        self.rect.x = x
        self.rect.y = y