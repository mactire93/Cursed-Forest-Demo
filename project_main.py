# Cursed Forest - gra platformowa

# Sound and Music:
# Art from Kenney.nl
# Jump sound from https://opengameart.org/users/ignasd
# Jump sound from https://opengameart.org/users/qubodup
# Attack sound from https://opengameart.org/content/37-hitspunches
# Swish sound from https://opengameart.org/users/artisticdude
# Zombie sound from https://opengameart.org/users/artisticdude
# Die sound from https://opengameart.org/users/haeldb
# Coin sound from https://opengameart.org/users/lordtomorrow
# Rock Bullet img by https://opengameart.org/users/phaelax
# Theme music by https://opengameart.org/users/haeldb
# Death theme by https://opengameart.org/content/bleeding-out
# Dark Forest Theme by https://opengameart.org/users/cynicmusic

import pygame as pg # teraz pygame będziemy nazywać pg
import random
from settings import *
from sprites import *
from os import path
import time

class Game:
    def __init__(self):
        # inicjalizacja okna gry itd
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True # zmienna odnosi się całego programu
        self.font_name = pg.font.match_font(FONT_NAME) # ustalam nazwę czcionek
        self.load_data()
        
    def load_data(self):
        # załadowuję wyniki
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
                
        # załaduj szablony gracza
        self.playersheets = Spritesheet(path.join(img_dir, PLAYER_SPRITESHEET))
        # załaduj szablon zombie
        self.zombiesheets = Spritesheet(path.join(img_dir, ZOMBIE_SPRITESHEET))
        # załaduj obrazy ziemi i platform
        self.plat_img = pg.image.load(path.join(img_dir, 'forest_pack_05.png')).convert()
        self.ground_img = pg.image.load(path.join(img_dir, 'forest_pack_13.png')).convert()
        # załaduj obraz monet
        self.coin_img = pg.image.load(path.join(img_dir, 'coin_gold.png')).convert()
        # załaduj pociski
        self.bullet_img = pg.image.load(path.join(img_dir, 'rock_bullet.png')).convert()
        # załaduj obraz tła
        self.background = pg.image.load(path.join(img_dir, 'bg_forest.png')).convert()
        self.background_rect = self.background.get_rect()

        
        # załaduj dźwięki
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'slightscream-11.ogg'))
        self.coin_sound = pg.mixer.Sound(path.join(self.snd_dir, 'coinsplash.ogg'))
        self.death_sound = pg.mixer.Sound(path.join(self.snd_dir,'3yell1.ogg'))
        self.zombie_attack_sound = pg.mixer.Sound(path.join(self.snd_dir, 'zombie-attack1.ogg'))
        self.claw_hit_sound = pg.mixer.Sound(path.join(self.snd_dir, 'clawsnd01.ogg'))
        self.swish_sound = pg.mixer.Sound(path.join(self.snd_dir, 'swish-7.ogg'))
        self.throw_hit_sound = pg.mixer.Sound(path.join(self.snd_dir, 'hit33.ogg'))
        
        
    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()    # dodaję grupę wszystkich sprite's
        self.platforms = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.zombies = pg.sprite.Group()
        self.player = Player(self)  # dodaję gracza
        self.all_sprites.add(self.player)   # dodaję gracza do grupy sprite's
        # dodaję platformy
        for plat in PLATFORM_LIST:
            p = Platform(self, *plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
            
        # generator ziemi(rozwiązanie tymczasowe)  
        i = 0
        x = 0
        while i < 35:
            ground = Ground(self, x, HEIGHT - 40)
            self.all_sprites.add(ground)
            self.platforms.add(ground)
            i += 1
            x += 64 #ustalone względem szerokości obrazu
            
        i = 0
        x = x + 320
        while i < 10:
            ground = Ground(self, x, HEIGHT - 40)
            self.all_sprites.add(ground)
            self.platforms.add(ground)
            i += 1
            x += 64 #ustalone względem szerokości obrazu
            
        i = 0
        x = x + 320
        while i < 15:
            ground = Ground(self, x, HEIGHT - 40)
            self.all_sprites.add(ground)
            self.platforms.add(ground)
            i += 1
            x += 64 #ustalone względem szerokości obrazu

        i = 0
        x = x + 1600
        while i < 15:
            ground = Ground(self, x, HEIGHT - 40)
            self.all_sprites.add(ground)
            self.platforms.add(ground)
            i += 1
            x += 64 #ustalone względem szerokości obrazu
        i = 0    
        x = x + 320
        while i < 15:
            ground = Ground(self, x, HEIGHT - 40)
            self.all_sprites.add(ground)
            self.platforms.add(ground)
            i += 1
            x += 64 #ustalone względem szerokości obrazu
        
        i = 0
        x = x - 640
        while i < 10:
            ground = Ground(self, x, HEIGHT - 104)
            self.all_sprites.add(ground)
            self.platforms.add(ground)
            i += 1
            x += 64 #ustalone względem szerokości obrazu
        
        i = 0
        x = x - 320
        while i < 5:
            ground = Ground(self, x, HEIGHT - 168)
            self.all_sprites.add(ground)
            self.platforms.add(ground)
            i += 1
            x += 64 #ustalone względem szerokości obrazu
            
        i = 0
        x = x + 320
        while i < 15:
            ground = Ground(self, x, HEIGHT - 40)
            self.all_sprites.add(ground)
            self.platforms.add(ground)
            i += 1
            x += 64 #ustalone względem szerokości obrazu
        
        i = 0
        x = x - 960
        while i < 10:
            ground = Ground(self, x, HEIGHT - 104)
            self.all_sprites.add(ground)
            self.platforms.add(ground)
            i += 1
            x += 64 #ustalone względem szerokości obrazu
            
        i = 0
        x = x - 640
        while i < 5:
            ground = Ground(self, x, HEIGHT - 168)
            self.all_sprites.add(ground)
            self.platforms.add(ground)
            i += 1
            x += 64 #ustalone względem szerokości obrazu
        
        
            
        
            
        # dodaję monety
        for coin in COIN_LIST:
            c = Coin(self, *coin)
            self.all_sprites.add(c)
            self.coins.add(c)
        # dodaję zombie
        for zombie in ZOMBIE_LIST:
            z = Zombie(self, *zombie)
            self.all_sprites.add(z)
            self.zombies.add(z)
        
            
        # dodaję muzykę w tle
        pg.mixer.music.load(path.join(self.snd_dir, 'GameMusic_ForestTheme_24.mp3'))
        
        self.run()  # odpalan pętlę gry
    
    def run(self):
        # tutaj będzie pętla gry
        
        pg.mixer.music.play(loops = -1) # nieskończona pętla
        
        self.playing = True # tworzę pętlę gry (odnosi się pętli gry)
        while self.playing:
            self.clock.tick(FPS)
            self.events()   # uruchamiam zdarzenia
            self.update()   # uruchamiam aktualizacje pętli
            self.draw()     # rysuję obiekty
            
        pg.mixer.music.fadeout(500)
            
    def update(self):
        # tutaj aktualizuje się pętla gry
        self.all_sprites.update()
        
        # obsługa kolizji

        # kolizja z coinami
        
        coin_hits = pg.sprite.spritecollide(self.player, self.coins, True)
        if coin_hits:
            self.coin_sound.play()
            self.score += 10
            
        # kolizja gracz - zombie
        
        #for z in self.zombies:
            #if self.player.rect.x - z.rect.x <= abs(200):
                #z.move_towards_player()
                
        """nad tym jeszcze muszę popracować"""
        
        zombie_hits = pg.sprite.spritecollide(self.player, self.zombies, False)
        for zombie in zombie_hits:
            if self.player.vel.x > 0 and zombie.vx < 0:
                zombie.attack = True
                self.claw_hit_sound.play()
                self.player.vel.x -= 20
                self.player.vel.y -= 20
                self.player.lives -= 1
                self.zombie_attack_sound.play()
            if self.player.vel.x < 0 and zombie.vx > 0:
                zombie.attack = True
                self.claw_hit_sound.play()
                self.player.vel.x += 20
                self.player.vel.y -= 20
                self.player.lives -= 1
                self.zombie_attack_sound.play()
            if self.player.vel.x == 0 and zombie.vx < 0:
                zombie.attack = True
                self.claw_hit_sound.play()
                self.player.vel.x -= 20
                self.player.vel.y -= 20
                self.player.lives -= 1
                self.zombie_attack_sound.play()
            if self.player.vel.x == 0 and zombie.vx > 0:
                zombie.attack = True
                self.claw_hit_sound.play()
                self.player.vel.x += 20
                self.player.vel.y -= 20
                self.player.lives -= 1
                self.zombie_attack_sound.play()
                
        # jeśli obiekt przekroczy połowę ekranu
        if self.player.rect.right >= WIDTH / 2: # jeśli gracz przekroczy 1/2 ekranu
            self.player.pos.x -= abs(self.player.vel.x)
            #self.background_rect.rect.x -= abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.right -= abs(self.player.vel.x)   # od prawej kraw. plat. odejmiemy prędkość gracza
            
            for coin in self.coins:
                coin.rect.right -= abs(self.player.vel.x)
                    
            for zombie in self.zombies:
                zombie.rect.right -=abs(self.player.vel.x)

               
                    
        # gracz umiera w wyniku upadku
        if self.player.rect.bottom > HEIGHT:
            self.death_sound.play()
            self.playing = False
        # gracz umiera gdy straci życie
        if self.player.lives == 0:
            self.death_sound.play()
            time.sleep(1)
            self.playing = False
            
        
                    
        
    def events(self):
        # pętla gry - obsługa zdarzeń
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
                    
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()
                    
            if event.type == pg.KEYUP:
                if event.key == pg.K_s:
                    self.player.shoting = True
                    now = pg.time.get_ticks()
                    if now - self.player.last_throw > self.player.throw_delay:
                        self.player.last_throw = now
                        bullet = Bullet(self, self.player)
                        bullet.rect.x = self.player.rect.centerx
                        bullet.rect.y = self.player.rect.centery
                        self.all_sprites.add(bullet)
                        self.bullets.add(bullet)
                        self.swish_sound.play()
                        
        
    def draw(self):
        #Pętla gry - rysowanie obiektów
        self.screen.fill(BLUE) # tło ekranu
        self.screen.blit(self.background, self.background_rect)
        self.all_sprites.draw(self.screen)  # rysuję wszystkie obiekty
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        self.draw_text(str(self.player.lives), 22, WHITE, WIDTH / 3, 15)
        pg.display.flip()   # rzutuję obiekty na ekran
        
    def show_start_screen(self):
        # wyświetl ekran startowy
        pg.mixer.music.load(path.join(self.snd_dir, 'ratsrats_0.ogg'))
        pg.mixer.music.play(loops = -1) # nieskończona pętla do muzyki powyżej
        self.screen.fill(BLACK)
        self.draw_text("CURSED FOREST - DEMO", 48, RED, WIDTH / 2, HEIGHT / 4)
        self.draw_text("NACIŚNIJ PRZYCISK ABY ZAGRAĆ", 22, RED, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("NAJLEPSZY WYNIK: " + str(self.highscore), 22, RED, WIDTH / 2, 15)

        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500) # po zakończeniu działania, wycisz muzykę
        
    def show_go_screen(self):
        # wyświetl ekran game over
        if not self.running:
            return
        pg.mixer.music.load(path.join(self.snd_dir, 'bleeding_out2.ogg'))
        pg.mixer.music.play(loops = -1) # nieskończona pętla do muzyki 
        self.screen.fill(BLACK)
        self.draw_text("KONIEC GRY!", 48, RED, WIDTH / 2, HEIGHT / 4)
        self.draw_text("TWÓJ WYNIK: " + str(self.score), 22, RED, WIDTH / 2, HEIGHT / 2 + 80)
        self.draw_text("NACIŚNIJ PRZYCISK ABY ZAGRAĆ PONOWNIE", 22, RED, WIDTH / 2, HEIGHT * 3 / 4)
        
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NOWY REKORD!", 22, RED, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("NAJLEPSZY WYNIK: " + str(self.highscore), 22, RED, WIDTH / 2, HEIGHT / 2 + 40)
            
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)
            
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False
                    
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
            
        
    
g = Game()      # uruchomienie obiektu klasy Game
g.show_start_screen()   # uruchamiam ekran startowy
while g.running:    # dopóki zmienna g działa, wyświetla new oraz show_go_screen()
    g.new()     # uruchamiam nową grę
    g.show_go_screen()      # uruchamiam ekran game over
    
pg.quit()
