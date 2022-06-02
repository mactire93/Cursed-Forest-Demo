import pygame as pg
from settings import *
import random
import math
from random import randrange, choice
vec = pg.math.Vector2 # uruchamiam element z biblioteki umożliwiającej obliczenie wektora prędkości



class Spritesheet:
    # klasa użytkowa do załadowania obrazów
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
        
    def get_image(self, x, y, width, height):
        # pobierz obraz z arkusza kształtów
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))  # użyte obrazy okazały się zbyt duże i musiałem je wyskalować
        # dodatkowo pojawił się błąd, że nie można użyć liczb niecałkowitych, dlatego użyłem // aby zaokrąglić te liczby
        return image
        
class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False    # domyślny brak ruchu
        self.jumping = False    # domyślny brak skoku
        self.shoting = False
        self.current_frame = 0  # aktualna klatka
        self.last_update = 0    # czas ostatniej aktualizacji
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)   # ustalam pozycję wektora prędkości
        self.vel = vec(0, 0)    # ustalam prędkość
        self.acc = vec(0, 0)    # ustalam przyspieszenie
        self.throw_delay = 750 # czas opóźnienia rzutu
        self.lives = 3
        self.last_throw = pg.time.get_ticks() # czas ostatniego rzutu
        
        self.on_ground = True   # domyślnie na ziemi UWAGA: zmień sobie logikę w self.jumping bo się powtarza
        
    def load_images(self):
        """ animacja ruchu została przedstawiona w def animate() """
        # ustalam listę klatek gdy postać stoi
        self.standing_frames = [self.game.playersheets.get_image(0, 0, 192, 256)]
                                #self.game.playersheets.get_image(0, 512, 192, 256)]
        # przezroczystość tła
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        # ustalam listę klatek w animacji ruchu    
        self.walk_frames_r = [self.game.playersheets.get_image(1152, 512, 192, 256),
                              self.game.playersheets.get_image(1344, 512, 192, 256),
                              self.game.playersheets.get_image(1536, 512, 192, 256)]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            #przezroczystość tła
            frame.set_colorkey(BLACK)
            # odwracam klatki i dodaję do listy walk_frames_l
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        # ustalam listę klatek skoku
        self.jump_frames = [self.game.playersheets.get_image(192, 0, 192, 256)]
        for frame in self.jump_frames:
            frame.set_colorkey(BLACK)
            
        # klatki ataku
        
        self.shot_frames_r = [self.game.playersheets.get_image(192, 768, 192,256)]
        
        self.shot_frames_l = []
        for frame in self.shot_frames_r:
            frame.set_colorkey(BLACK)
            self.shot_frames_l.append(pg.transform.flip(frame, True, False))
            
    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
    """ jeżeli prędkość y będzie mniejsza -3, zrównamy y do -3 """
        
    def jump(self):
        if self.on_ground:  # jeżeli on_ground jest prawdą wykonaj skok i wyłącz on_ground w powietrzu
            self.game.jump_sound.play()
            self.vel.y = -PLAYER_JUMP
            self.jumping = True
            self.on_ground = False
            
    #def throw(self):
        #now = pg.time.get_ticks()
        
        """ problem z utworzeniem pocisku, brakuje y """
        
        #if now - self.last_throw > self.throw_delay:
            #speedx = 10
            #speedy = 0
            #self.last_throw = now
            #bullet1 = Bullet(self.rect.centerx, self.rect.centery, speedx, speedy)
            #bullet.rect.x = self.rect.x
            #bullet.rect.y = self.rect.y
            #game.all_sprites.add(bullet1)
            #game.bullets.add(bullet1)
            
        """ kolejny problem, tym razem brakuje speedy
        może powinienem strzał utworzyć całkiem w klasie Game??"""
        
    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)  # powtarzam przyspieszenie w update, dodaję y na 0.5 jako grawitację
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = - PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        
        
        # dodaję tarcie
        self.acc.x += self.vel.x * PLAYER_FRICTION # przyspieszenie zwiększa się o prędkość pomnożoną przez tarcie
        # równanie ruchu
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:   # gdy prędkość spadnie poniżej 0.1 wyzeruj
            self.vel.x = 0
        #self.pos += self.vel + 0.5 * self.acc # pozycja to suma prędkości i połowy przyspieszenia
        
        # ---- horizontal collision -----
        self.pos.x += self.vel.x + 0.5 * self.acc.x # pozycja wektora to suma prędkości i połowy przyspieszenia, ustalam dla x
        self.rect.centerx = self.pos.x              # uzgadniam pozycję wektora z przyłożeniem centerx prostokąta
        
        # nie pozwól na przejście za ekran (rozwiązanie tymczasowe)
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0
        
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        
        if hits:
            if self.vel.x > 0:
                self.rect.right = hits[0].rect.left
                self.pos.x = self.rect.centerx
                self.vel.x = 0
            elif self.vel.x < 0:
                self.rect.left = hits[0].rect.right
                self.pos.x = self.rect.centerx
                self.vel.x = 0
                
        """Wyjaśnienie: sprite.collide musi dostać odzielną instrukcję dla kolizji wertykalnej i horyznotalnej.
        Dodatkowo przeniosłem kolizje do sprite, dzięki czemu nie wskakuje on już na top platformy przy zderzeniu bocznym"""
        # ---- vertical collision ----        
        self.pos.y += self.vel.y + 0.5 * self.acc.y #pozycja wektora y to suma prędkości i połowy przyspieszenia
        self.rect.centery = self.pos.y  # ustalam przyłożenie wektora i centery prostokąta
        
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        
        if hits:
            if self.vel.y > 0:
                self.rect.bottom = hits[0].rect.top
                self.pos.y = self.rect.centery
                self.vel.y = 0
                self.on_ground = True
                self.jumping = False
            
            elif self.vel.y < 0:
                self.rect.top = hits[0].rect.bottom
                self.pos.y = self.rect.centery
                self.vel.y = 0
               
                
        # kolizja z zombie
        
        """zombie_hits = pg.sprite.spritecollide(self, self.game.zombies, False)
        
        if zombie_hits:
            self.zombie.attack = True"""
        # problem: uderzenie z mobem liczy życia x2, sama mechanika odrzutu mi się podoba
        # jak rozwiązać problem z uderzeniami? Może licznik? 
            
                
    def animate(self):
        now = pg.time.get_ticks() # ustawiam zegar
        
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        # animacja ruchu
        if self.walking:
            # ustawiam zmianę klatek względem różnicy stanu zegara i ostatniej aktualizacji
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                # dzięki modulo z ilości klatek, program zmienia aktualne klatki
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # animacja postaci gdy nie porusza się
        if not self.walking and not self.jumping:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # animacja gdy skacze        
        if self.jumping:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jump_frames)
                bottom = self.rect.bottom
                self.image = self.jump_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if self.shoting:
            if now - self.last_update > 50:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.shot_frames_l)
                bottom = self.rect.bottom
                if self.vel.x >= 0:
                    self.image = self.shot_frames_r[self.current_frame]
                    self.shoting = False
                else:
                    self.image = self.shot_frames_l[self.current_frame]
                    self.shoting = False
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                
        """ nie działa strzelanie"""
                
        
                
            
        
class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.plat_img
        self.image.set_colorkey(BLACK)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        #self.image = pg.transform.scale(self.image, (75, 40))
        self.rect.x = x
        self.rect.y = y
        
class Ground(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.ground_img
        self.image.set_colorkey(BLACK) # dla czarnego tła
        self.image.set_colorkey(WHITE) # dla białego tła
        self.rect = self.image.get_rect()
        #self.image = pg.transform.scale(self.image, (75, 40))
        self.rect.x = x
        self.rect.y = y
        
class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.coin_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
       
class Zombie(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.attack = False
        self.move_update = 0
        self.animation_update = 0
        self.load_img()
        self.image = self.game.zombiesheets.get_image(0, 0, 192, 256)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 3
        self.vx = 2
        self.dx = 1
        self.vy = 0 # prędkość oś y
        self.dy = 0.5 # przyspieszenie oś y
        
        self.current_frame = 0
        
    def load_img(self):
        
        self.walk_frames_r = [self.game.zombiesheets.get_image(0, 1024, 192, 256),
                              self.game.zombiesheets.get_image(192, 1024, 192, 256),
                              self.game.zombiesheets.get_image(384, 1024, 192, 256),
                              self.game.zombiesheets.get_image(576, 1024, 192, 256),
                              self.game.zombiesheets.get_image(768, 1024, 192, 256),
                              self.game.zombiesheets.get_image(960, 1024, 192, 256),
                              self.game.zombiesheets.get_image(1152, 1024, 192, 256),
                              self.game.zombiesheets.get_image(1344, 1024, 192, 256)]
        
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        
        self.attack_frames_r = [self.game.zombiesheets.get_image(0, 768, 192, 256),
                              self.game.zombiesheets.get_image(192, 768, 192,256),
                              self.game.zombiesheets.get_image(384, 768, 192, 256)]
        
        self.attack_frames_l = []
        for frame in self.attack_frames_r:
            frame.set_colorkey(BLACK)
            self.attack_frames_l.append(pg.transform.flip(frame, True, False))
        
    def update(self):
        self.move_towards_player()
        now = pg.time.get_ticks()
        animation_timer = pg.time.get_ticks()
        self.rect.x += self.vx
        self.vx = self.dx
        self.vy += self.dy # grawitacja
        self.rect.y += self.vy
        
        if now - self.move_update > 3000:
            self.move_update = now
            self.dx *= -1
                    
        if animation_timer - self.animation_update > 300:
            
            self.animation_update = animation_timer
            self.current_frame = (self.current_frame + 1) %len(self.walk_frames_l)
            x = self.rect.x
            y = self.rect.y
            if self.dx > 0:
                self.image = self.walk_frames_r[self.current_frame]
                
            else:
                self.image = self.walk_frames_l[self.current_frame]
                
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.rect.x += self.vx
        
            
        if self.attack:
            if animation_timer - self.animation_update > 100:
                self.animation_update = animation_timer
                self.current_frame = (self.current_frame + 1) %len(self.attack_frames_l)
                x = self.rect.x
                y = self.rect.y
                if self.dx > 0:
                    self.image = self.attack_frames_r[self.current_frame]
                    self.attack = False
                else:
                    self.image = self.attack_frames_l[self.current_frame]
                    self.attack = False
            
            
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        
        if hits:
            self.vy > 0
            self.rect.bottom = hits[0].rect.top
            self.vy = 0
            
    def move_towards_player(self):
        now = pg.time.get_ticks()
        animation_timer = pg.time.get_ticks()
        
        if self.game.player.rect.x - self.rect.x <= 300 and self.game.player.rect.x - self.rect.x > 0:
            try:
                dx, dy = self.game.player.rect.x - self.rect.x, self.game.player.rect.y - self.rect.y
                dist = math.hypot(dx, dy)
                dx, dy = dx / dist, dy / dist
                self.rect.x += dx * self.speed
                self.rect.y += dy * self.speed
            except ZeroDivisionError:
                return
            if animation_timer - self.animation_update > 300:
            
                self.animation_update = animation_timer
                self.current_frame = (self.current_frame + 1) %len(self.walk_frames_l)
                x = self.rect.x
                y = self.rect.y
                if dx > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.rect.x += self.vx
            
        if self.game.player.rect.x - self.rect.x >= -300 and self.game.player.rect.x - self.rect.x <= 0:
            try:
                dx, dy = self.game.player.rect.x - self.rect.x, self.game.player.rect.y - self.rect.y
                dist = math.hypot(dx, dy)
                dx, dy = dx / dist, dy / dist
                self.rect.x += dx * self.speed
                self.rect.y += dy * self.speed
            except ZeroDivisionError:
                return
            if animation_timer - self.animation_update > 300:
            
                self.animation_update = animation_timer
                self.current_frame = (self.current_frame + 1) %len(self.walk_frames_l)
                x = self.rect.x
                y = self.rect.y
                if dx > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.rect.x += self.vx
            
        """punktem odniesienia jest gracz"""
        
        
                
           
class Bullet(pg.sprite.Sprite):
    def __init__(self, game, player):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.player = player
        self.image = self.game.bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.speed = 15
        self.distance = 0
        self.gravity = 2
        self.dt = 0.04
        self.vy = 0
        if self.player.vel.x > 0:
            self.speed = self.speed
        elif self.player.vel.x < 0:
            self.speed = - self.speed
        
        
    def update(self):
        self.distance += self.speed
        self.rect.x += self.speed
        self.vy = self.vy + self.gravity * self.dt
        self.rect.y = self.rect.y + self.vy + self.dt
        
        hits = pg.sprite.spritecollide(self, self.game.zombies, True)
        
        if hits:
            self.game.score += 20
            self.game.throw_hit_sound.play()
            self.kill() # po uderzeniu w moba tracimy pocisk
            
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        
        if hits:
            self.kill()
        
        