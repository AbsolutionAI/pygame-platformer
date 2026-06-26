import pygame
import sys
from config import *
from entities import Player
from levels import load_level, LEVEL_1
from camera import Camera
from particles import Particle

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 20)
        self.state = "menu"
        self.particles = []
        self.reset()

    def reset(self):
        self.platforms, self.enemies, self.coins, player_start, world_w, world_h = \
            load_level(LEVEL_1)
        self.player = Player(*player_start)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.enemies)
        self.all_sprites.add(self.coins)
        self.camera = Camera(world_w, world_h)
        self.particles.clear()
        self.score = 0

    def run(self):
        while True:
            self.clock.tick(FPS)
            self.handle_events()

            if self.state == "menu":
                self.draw_menu()
            elif self.state == "playing":
                self.update()
                self.draw()
            elif self.state == "game_over":
                self.draw_game_over()

            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if self.state == "menu" and event.key == pygame.K_SPACE:
                    self.state = "playing"
                if self.state == "game_over":
                    if event.key == pygame.K_SPACE:
                        self.reset()
                        self.state = "playing"
                    elif event.key == pygame.K_m:
                        self.reset()
                        self.state = "menu"

    def update(self):
        self.player.update(self.platforms)
        self.enemies.update()
        self.coins.update()
        self.camera.update(self.player)

        for coin in pygame.sprite.spritecollide(self.player, self.coins, True):
            self.score += 10
            for _ in range(8):
                self.particles.append(Particle(coin.rect.centerx, coin.rect.centery))

        for enemy in pygame.sprite.spritecollide(self.player, self.enemies, False):
            if self.player.vel_y > 0 and self.player.rect.bottom <= enemy.rect.centery:
                enemy.kill()
                self.score += 50
                self.player.vel_y = -8
                for _ in range(12):
                    self.particles.append(
                        Particle(enemy.rect.centerx, enemy.rect.centery, COLORS["enemy"])
                    )
            else:
                self.state = "game_over"

        if not self.player.alive():
            self.state = "game_over"

        self.particles = [p for p in self.particles if p.alive]
        for p in self.particles:
            p.update()

    def draw(self):
        self.screen.fill(COLORS["bg"])

        offset = self.camera.rect.topleft

        for platform in self.platforms:
            self.screen.blit(platform.image, self.camera.apply(platform))

        for enemy in self.enemies:
            self.screen.blit(enemy.image, self.camera.apply(enemy))

        for coin in self.coins:
            self.screen.blit(coin.image, self.camera.apply(coin))

        for p in self.particles:
            p.draw(self.screen, offset)

        self.screen.blit(self.player.image, self.camera.apply(self.player))

        score_text = self.font.render(f"Score: {self.score}", True, COLORS["text"])
        self.screen.blit(score_text, (10, 10))

    def draw_menu(self):
        self.screen.fill(COLORS["bg"])
        title = self.font.render("PLATFORMER TEMPLATE", True, COLORS["accent"])
        start = self.font.render("Press SPACE to Play", True, COLORS["text"])
        controls = self.small_font.render(
            "Arrow Keys / WASD to move | Space to jump | Double jump",
            True, COLORS["text"]
        )
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        self.screen.blit(start, (WIDTH // 2 - start.get_width() // 2, HEIGHT // 2))
        self.screen.blit(controls, (WIDTH // 2 - controls.get_width() // 2, HEIGHT // 2 + 40))

    def draw_game_over(self):
        self.screen.fill(COLORS["bg"])
        over = self.font.render("GAME OVER", True, COLORS["accent"])
        score = self.font.render(f"Score: {self.score}", True, COLORS["text"])
        restart = self.small_font.render("Press SPACE to restart | M for menu", True, COLORS["text"])
        self.screen.blit(over, (WIDTH // 2 - over.get_width() // 2, HEIGHT // 3))
        self.screen.blit(score, (WIDTH // 2 - score.get_width() // 2, HEIGHT // 2))
        self.screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + 40))


if __name__ == "__main__":
    Game().run()
