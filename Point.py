import pygame

white = (255, 255, 255)

pygame.init()
font = pygame.font.Font("font/AtariClassic-gry3.ttf", 15)


class Point:
    def __init__(self, point, pos, color):
        self.font = font.render(point, True, color)
        self.pos = pos

        self.counter = 0
        self.counterMax = 30

    def update(self):
        self.counter += 1
        self.pos.y -= 1