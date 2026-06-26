import pygame
import random
from config import COLORS

class Particle:
    def __init__(self, x, y, color=None):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, -1)
        self.life = 30
        self.max_life = 30
        self.size = random.randint(2, 5)
        self.color = color or COLORS["particle"]

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2
        self.life -= 1

    def draw(self, surface, offset=(0, 0)):
        alpha = self.life / self.max_life
        size = int(self.size * alpha)
        if size > 0:
            pygame.draw.circle(
                surface, self.color,
                (int(self.x + offset[0]), int(self.y + offset[1])),
                size
            )

    @property
    def alive(self):
        return self.life > 0
