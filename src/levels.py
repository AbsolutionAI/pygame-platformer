from entities import Platform, Enemy, Coin
from config import TILE_SIZE, COLORS, WIDTH, HEIGHT

LEVEL_1 = [
    "1111111111111111111111111111",
    "1                          1",
    "1                          1",
    "1     P                   1",
    "1                  EE     1",
    "1      CCC               1",
    "1  111        111         1",
    "1                          1",
    "1          E              1",
    "1        111     CCCC     1",
    "1                     111 1",
    "1  1111                   1",
    "1              11111      1",
    "1                   E     1",
    "1          1111     1111  1",
    "1 1111                    1",
    "1111111111111111111111111111",
]


def load_level(data):
    platforms = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    player_start = (100, 100)

    for y, row in enumerate(data):
        for x, char in enumerate(row):
            px = x * TILE_SIZE
            py = y * TILE_SIZE
            if char == "1":
                platforms.add(Platform(px, py, TILE_SIZE, TILE_SIZE, COLORS["ground"]))
            elif char == "E":
                e = Enemy(px, py, px - 48, px + 48)
                enemies.add(e)
            elif char == "C":
                coins.add(Coin(px + TILE_SIZE // 2, py + TILE_SIZE // 2))
            elif char == "P":
                player_start = (px + TILE_SIZE // 2, py)

    world_width = len(data[0]) * TILE_SIZE
    world_height = len(data) * TILE_SIZE

    return platforms, enemies, coins, player_start, world_width, world_height
