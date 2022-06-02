# ustawienia gry
TITLE = "Cursed Forest - Demo"
WIDTH = 1024
HEIGHT = 728
FPS = 60
FONT_NAME = 'times new roman'  # arial, verdana, times new roman, palatino, garamond, comic sans ms
HS_FILE = "highscore.txt"
PLAYER_SPRITESHEET = "playersheet.png"
ZOMBIE_SPRITESHEET = "zombiesheet.png"


# ustawienia gracza
PLAYER_FRICTION = -0.12
PLAYER_ACC = 0.5
PLAYER_JUMP = 20
PLAYER_GRAV = 0.8
MOB_GRAV = 0.8

# lista platform

GROUND_LIST =[(0, HEIGHT - 40),
              (50, HEIGHT - 40),
              (100, HEIGHT - 40),
              (150, HEIGHT - 40),
              (200, HEIGHT - 40),
              (250, HEIGHT - 40),
              (300, HEIGHT - 40),
              (350, HEIGHT - 40),
              (400, HEIGHT - 40)]

PLATFORM_LIST = [(300, 478),
                (400, 278),
                (600, 378),
                (800, 200),
                (1000, 290),
                (1200, 378),
                (1400, 200),
                (3600, 478),# trzeci land
                (3920, 478),
                (4240, 478),
                (4700, 538),# czwarty land
                (5070, 478),
                (5390, 478),
                (5710, 478),
                (6180, 478),# piąty land
                (6500, 478),
                (6820, 478)]

# x + 46, y - 40                
COIN_LIST =[(346, 438),
            (446, 238),
            (646, 338),
            (846, 160),
            (1046, 250),
            (1246, 338),
            (1446, 160),
            (3646, 438),# trzeci
            (3966, 438),
            (4286, 438),
            (4746, 498),# czwarty
            (5436, 438),
            (5756, 438),
            (5116, 438),
            (6226, 438),# piąty
            (6546, 438),
            (6866, 438)]
            
ZOMBIE_LIST = [(1200, HEIGHT - 168),
               (384, HEIGHT - 168),
               (2880, HEIGHT - 168),
               (3904, HEIGHT - 168),
               (4024, HEIGHT - 168),
               (6464, HEIGHT - 168),
               (6528, HEIGHT - 168),
               (7680, HEIGHT - 168),
               (7800, HEIGHT - 168),
               (8890, HEIGHT - 336),
               (9010, HEIGHT - 336)]


# zdefiniowane kolory

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
