import pygame
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((28, 32))
        self.image.fill(COLORS["player"])
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.vel_x = 0
        self.vel_y = 0
        self.jumps_left = MAX_JUMPS
        self.on_ground = False
        self.score = 0
        self.facing = 1

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED
            self.facing = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = PLAYER_SPEED
            self.facing = 1
        if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]:
            self.jump()

        self.vel_y += GRAVITY
        if self.vel_y > 15:
            self.vel_y = 15

        self.rect.x += self.vel_x
        self.collide_horizontal(platforms)

        self.rect.y += self.vel_y
        self.on_ground = False
        self.collide_vertical(platforms)

        if self.rect.y > GAME_OVER_FALL:
            self.kill()

    def jump(self):
        if self.jumps_left > 0:
            force = JUMP_FORCE if self.jumps_left == MAX_JUMPS else DOUBLE_JUMP_FORCE
            self.vel_y = force
            self.jumps_left -= 1

    def collide_horizontal(self, platforms):
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel_x > 0:
                    self.rect.right = p.rect.left
                elif self.vel_x < 0:
                    self.rect.left = p.rect.right

    def collide_vertical(self, platforms):
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel_y > 0:
                    self.rect.bottom = p.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                    self.jumps_left = MAX_JUMPS
                elif self.vel_y < 0:
                    self.rect.top = p.rect.bottom
                    self.vel_y = 0


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color=None):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(color or COLORS["platform"])
        self.rect = self.image.get_rect(topleft=(x, y))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, patrol_left, patrol_right):
        super().__init__()
        self.image = pygame.Surface((28, 28))
        self.image.fill(COLORS["enemy"])
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = 2
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right
        self.dir = 1

    def update(self):
        self.rect.x += self.speed * self.dir
        if self.rect.x <= self.patrol_left:
            self.dir = 1
        elif self.rect.x >= self.patrol_right:
            self.dir = -1


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        self.image.fill(COLORS["coin"])
        self.rect = self.image.get_rect(center=(x, y))
        self.bob_offset = 0

    def update(self):
        self.bob_offset = (self.bob_offset + 0.05) % (2 * 3.14159)
        self.rect.y += pygame.math.Vector2(0, pygame.math.sin(self.bob_offset)).y * 0.3
