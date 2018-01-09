#!/usr/bin/env python3

import pygame
import random
import os
import sys
import serial
import math
import re
from sys import platform as _platform

# Set the port communication
try:
    # Set up the port for linux
    if _platform == "linux" or _platform == "linux2":
        port = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.0)

    # Set up the port for macos
    elif _platform == "darwin":
        port = serial.Serial('/dev/tty.usbserial', 115200, timeout=0.0)

    # Set up the port for windows
    elif _platform == "win32" or _platform == "win64":
        port = serial.Serial('COM1', 115200, timeout=0.0)
except:
    print("SORRY! NO SUITABLE PORT WAS FOUND!")
    sys.exit()

# Initialise Pygame
pygame.init()

# Define relevant colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE= (233, 166, 31)
BLUE  = (95, 198, 207)

# Define screen size and set it
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode(SCREEN_SIZE)

# Name the window
pygame.display.set_caption('HASTE SPACE')

# Define initial velocity of Meteors
initial_velocity = 1
d_time = 0.0

# Load sounds
shoot_sound = pygame.mixer.Sound("./assets/Audio/laser.ogg")
target_sound = pygame.mixer.Sound("./assets/Audio/target.ogg")
gameover_sound = pygame.mixer.Sound("./assets/Audio/gameover.ogg")
won_sound = pygame.mixer.Sound("./assets/Audio/won.ogg")

# Load graphics
enemy_imgs = pygame.image.load("./assets/Enemy/0.png").convert()
bullet_img = pygame.image.load("./assets/Enemy/1.png").convert()
star_img   = pygame.image.load("./assets/star.png").convert()

missile_img = pygame.image.load("./assets/missile.png").convert()

meteor_lists = []
for j in range(0,7):
    new_list = []
    meteors_assets = os.listdir("./assets/Meteors/"+str(j))
    for i in range(len(meteors_assets)):
        new_meteor = pygame.image.load("./assets/Meteors/" + str(j) + "/" + meteors_assets[i]).convert()
        new_meteor.set_colorkey(BLACK)
        new_list.append(new_meteor)
    meteor_lists.append(new_list)


title_assets = os.listdir("./assets/Title")
title_assets = sorted(title_assets, key=lambda x: (int(re.sub('\D','',x)),x))
title_imgs = []
for i in range(len(title_assets)):
    new_title = pygame.image.load("./assets/Title/" + title_assets[i]).convert()
    new_title.set_colorkey(BLACK)
    title_imgs.append(new_title)

about_assets = os.listdir("./assets/About")
about_assets = sorted(about_assets, key=lambda x: (int(re.sub('\D','',x)),x))
about_imgs = []
for i in range(len(about_assets)):
    new_about = pygame.image.load("./assets/About/" + about_assets[i]).convert()
    new_about.set_colorkey(BLACK)
    about_imgs.append(new_about)

record_assets = os.listdir("./assets/Record")
record_assets = sorted(record_assets, key=lambda x: (int(re.sub('\D','',x)),x))
record_imgs = []
for i in range(len(record_assets)):
    new_record = pygame.image.load("./assets/Record/" + record_assets[i]).convert()
    new_record.set_colorkey(BLACK)
    record_imgs.append(new_record)


buttons_assets = os.listdir("./assets/Buttons")
buttons_assets = sorted(buttons_assets, key=lambda x: (int(re.sub('\D','',x)),x))
button_imgs = []
for i in range(len(buttons_assets)):
    new_button = pygame.image.load("./assets/Buttons/" + buttons_assets[i]).convert()
    new_button.set_colorkey(BLACK)
    button_imgs.append(new_button)

bg_gameplay = pygame.image.load("./assets/Backdrop/bg_23.jpg").convert()
bg_menu = pygame.image.load("./assets/Backdrop/bg_1.jpg").convert()
bg_version = pygame.image.load("./assets/Backdrop/bg_21.png").convert()
bg_about = pygame.image.load("./assets/Backdrop/bg_5.png").convert()
bg_record = pygame.image.load("./assets/Backdrop/bg_4.png").convert()

# For handling of sprites - groups
draw_sprites   = pygame.sprite.Group()      # sprites to draw
meteor_sprites = pygame.sprite.Group()      # sprites of meteors
ammo_sprites   = pygame.sprite.Group()      # sprites of missiles
enemy_sprites  = pygame.sprite.Group()      # sprites of shooting enemies
bullet_sprites = pygame.sprite.Group()      # sprites of bullets from enemies
star_sprite    = pygame.sprite.Group()      # sprites of the star


# Classes
class Ship(pygame.sprite.Sprite):
    """ Player sprite """

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("./assets/Ship/ship.png").convert()
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()


class Missile(pygame.sprite.Sprite):
    """ Player bullets sprite """

    def __init__(self):
        super().__init__()

        self.image = missile_img
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 20


class Meteor(pygame.sprite.Sprite):
    """ Meteors sprite """

    def __init__(self, offset):
        super().__init__()
        self.offset = offset
        self.count_ship = 0
        self.anim = 0

        self.sprites = meteor_lists[offset]
        self.image = self.sprites[0]
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()

    def update(self):
        ctr = random.randint(0, 15)
        if ctr in (0, 1, 2):
            self.rect.x += 1
        elif ctr in (3, 4, 5):
            self.rect.y += 2
        elif ctr in (6, 7, 8):
            self.rect.x -= 1
        elif ctr in (9, 10, 11):
            self.rect.y -= 2

        # Handle animation
        if self.anim > 15:
            self.anim = 0
        self.image = self.sprites[int(self.anim)]
        self.anim += 0.08


class Enemy(pygame.sprite.Sprite):
    """ The ship of enemy """

    def __init__(self):
        super().__init__()
        self.t = 0

        self.image = enemy_imgs
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()

    def update(self):
        self.t += 0.05
        self.rect.y = SCREEN_HEIGHT/6 + 100*math.sin(self.t)
        self.rect.x = SCREEN_WIDTH/2 + 100*math.cos(self.t)
        if self.t == 2*math.pi:
            self.t = 0


class Bullet(pygame.sprite.Sprite):
    """ The bullets of enemy """

    def __init__(self):
        super().__init__()

        self.image = bullet_img
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += 10


class Star(pygame.sprite.Sprite):
    """ The flag to be captured as goal of game """

    def __init__(self):
        super().__init__()

        self.image = star_img
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y = SCREEN_HEIGHT/6 
        self.rect.x = SCREEN_WIDTH/2 


# Declaring the various scenes of the game:
#   - VersionScene
#   - MenuScene
#   - GameplayScene
#   - RecordScene
#   - AboutScene


class VersionScene():
    """ Welcoming scene with title and version """

    # VERSION & CONTINUE
    version = "Version 1.0"
    press   = "Press button 2 to continue. . ."

    # Define stamps
    version_font = pygame.font.SysFont('arial', 20, True, True)
    version_text = version_font.render(version, True, ORANGE)

    press_font = pygame.font.SysFont('arial', 20, True, True)
    press_text = press_font.render(press, True, BLUE)
    press_surface = pygame.Surface((500, 20)).convert()
    press_surface.fill(BLACK)
    press_surface.blit(press_text, (0, 0, 10, 10))
    press_surface.set_colorkey(BLACK)

    def __init__(self):
        self.next = self
        self.count_title = [-0.4, 0]
        self.count_press = 0
        self.show_msg = False

    def inputHandler(self, event):
        for direction in str(inputs):
            if direction == '2':
                   self.switch(MenuScene())


    def update(self):
        # Handling animation of title
        if self.count_title[0] >= (len(title_imgs) - 0.4):
            self.show_msg = True
            pass
        else:
            self.count_title[0] += 0.4

        self.count_title[1] += 1
        self.count_press += 1
        if self.count_title[1] == 300:
            self.count_title = [-0.4, 0]


    def render(self):
        screen.blit(bg_version, [0, 0])
        screen.blit(title_imgs[int(self.count_title[0])], [60, SCREEN_HEIGHT/3])
        screen.blit(self.version_text, [6*SCREEN_WIDTH/8, 3*SCREEN_HEIGHT/6])
        if self.show_msg == True:
            self.press_surface.set_alpha(self.count_title[1])
            screen.blit(self.press_surface, [3*SCREEN_WIDTH/9, 5*SCREEN_HEIGHT/6])
            

    def switch(self, nextScene):
            self.next = nextScene


class MenuScene():
    """ Present buttons in menus:
            - Game
            - Record
            - About
            - Quit
    """

    def __init__(self):
        self.next = self
        self.count_ship = 0
        self.count_title = [-0.4, 0]
        self.dir = 1
        self.active_button = 0
        self.one_down = False
        self.one_up   = False
        self.read     = 0

        self.sprite_sheet = pygame.image.load("./assets/Ship/ship_anim.png").convert()
        self.sprites = []
        for i in range(24):
            image = pygame.Surface([250, 250]).convert()
            image.blit(self.sprite_sheet, (0,0), (250*i, 0, 250, 250))
            image.set_colorkey(BLACK)
            self.sprites.append(image)

    def inputHandler(self, inputs):
        for direction in str(inputs):
            if direction == '2':
                if self.active_button == 0:
                   self.switch(GameplayScene())
                if self.active_button == 1:
                   self.switch(RecordScene())
                if self.active_button == 2:
                   self.switch(AboutScene())
                if self.active_button == 3:
                   self.switch(None)
            elif direction == 'D':
               self.one_down = True
            elif direction == 'U':
               self.one_up = True

    def update(self):
        # Handling animation of title
        if self.count_title[0] >= (len(title_imgs) - 0.4):
            pass
        else:
            self.count_title[0] += 0.4

        self.count_title[1] += 1
        if self.count_title[1] == 300:
            self.count_title = [-0.4, 0]

        # Handling animation of ship
        if self.dir == 1:
            self.count_ship += 0.2
        else:
            self.count_ship -= 0.2

        if self.count_ship > 22:
            self.dir = 0
        if self.count_ship < 1:
            self.dir = 1

        # Handling buttons
        self.read += 1
        if self.read == 15:
            if self.one_down:
                self.active_button += 1
            if self.one_up:
                self.active_button -= 1
            self.read = 0

        self.one_down = False
        self.one_up   = False

        if self.active_button >= 4:
            self.active_button = 0
        if self.active_button <= -1:
            self.active_button = 3

    def render(self):
        screen.blit(bg_menu, [0, 0])
        screen.blit(title_imgs[int(self.count_title[0])], [60, 60])
        screen.blit(self.sprites[int(self.count_ship)], [500, 250])
        if self.active_button == 0:
            screen.blit(button_imgs[0], [SCREEN_WIDTH/5, 2*SCREEN_HEIGHT/5])
        else:
            screen.blit(button_imgs[1], [SCREEN_WIDTH/5, 2*SCREEN_HEIGHT/5])
        if self.active_button == 1:
            screen.blit(button_imgs[2], [SCREEN_WIDTH/5, 2*SCREEN_HEIGHT/5+70])
        else:
            screen.blit(button_imgs[3], [SCREEN_WIDTH/5, 2*SCREEN_HEIGHT/5+70])
        if self.active_button == 2:
            screen.blit(button_imgs[4], [SCREEN_WIDTH/5, 2*SCREEN_HEIGHT/5+140])
        else:
            screen.blit(button_imgs[5], [SCREEN_WIDTH/5, 2*SCREEN_HEIGHT/5+140])
        if self.active_button == 3:
            screen.blit(button_imgs[6], [SCREEN_WIDTH/5, 2*SCREEN_HEIGHT/5+210])
        else:
            screen.blit(button_imgs[7], [SCREEN_WIDTH/5, 2*SCREEN_HEIGHT/5+210])


    def switch(self, nextScene):
        self.next = nextScene


class GameplayScene():
    """ Where the action takes place  """

    # SCORE
    score = 000

    # Define stamps
    score_font = pygame.font.SysFont('purisa', 25, True, True)
    score_text = score_font.render("Score: " + str(score), True, WHITE)
    gameover_font = pygame.font.SysFont('symbola', 55, True, True)
    gameover_text = gameover_font.render("Game Over", True, WHITE)
    winning_font = pygame.font.SysFont('symbola', 55, True, True)
    winning_text = winning_font.render("YOU WON", True, WHITE)

    # gameover_text_rect = gameover_text.get_rect()
    gameover_text_x = screen.get_width() / 2 - 100 # gameover_text_rect.width / 2
    gameover_text_y = screen.get_height() / 2 - 100 # gameover_text_rect.height / 2

    def __init__(self):
        self.next = self
        self.pause = False
        self.collided = False
        self.won = False
        self.t = 0
        self.no_enemy = False
        self.sound_play = False

        # Instatiating actors
        self.player = Ship()
        self.player.rect.x = SCREEN_WIDTH/2 - 80
        self.player.rect.y = SCREEN_HEIGHT-120
        draw_sprites.add(self.player)

        # Creating meteors
        for i in range(10):
            # new meteor
            meteoroid = Meteor(random.randint(0, 6))
            meteoroid.rect.x = random.randrange(SCREEN_WIDTH  - 100)
            meteoroid.rect.y = random.randrange(SCREEN_HEIGHT - 300) - 350

            # update list of sprites
            draw_sprites.add(meteoroid)
            meteor_sprites.add(meteoroid)

        # Creates enemies
        # update list of sprites
        self.enemy = Enemy()
        draw_sprites.add(self.enemy)
        enemy_sprites.add(self.enemy)

        # Creates star
        self.star = Star()
        draw_sprites.add(self.star)
        star_sprite.add(self.star)
        star_sprite.update()



    def inputHandler(self, inputs):#, self.player, draw_sprites, ammo_sprites):
        # Control Ship with sensor
        for direction in str(inputs):
            if self.pause is False:
                if direction == 'R':
                    self.player.rect.x += 2
                elif direction == 'r':
                    self.player.rect.x += 1
                elif direction == 'L':
                    self.player.rect.x -= 2
                elif direction == 'l':
                    self.player.rect.x -= 1
                elif direction == 'U':
                    self.player.rect.y -= 2
                elif direction == 'u':
                    self.player.rect.y -= 1
                elif direction == 'D':
                    self.player.rect.y += 2
                elif direction == 'd':
                    self.player.rect.y += 1
                elif direction == '1':
                    shoot_sound.play()
                    missile = Missile()
                    missile.rect.x = self.player.rect.x + self.player.rect.size[0]/2
                    missile.rect.y = self.player.rect.y
                    draw_sprites.add(missile)
                    ammo_sprites.add(missile)
                elif direction == '2':
                    self.pause = not self.pause
            elif direction == '2':
                self.pause = not self.pause
            elif direction == '1':
                self.switch(MenuScene())



    def update(self):#, meteor_sprites, ammo_sprites, draw_sprites):
        if self.pause is False:
            # Target down recognition
            for missile in ammo_sprites:
                destroyed_meteor = pygame.sprite.spritecollide(missile, meteor_sprites, True)
                for meteor in destroyed_meteor:
                    target_sound.play()
                    ammo_sprites.remove(missile)
                    draw_sprites.remove(missile)
                    self.score += 1

                destroyed_enemy = pygame.sprite.spritecollide(missile, enemy_sprites, True)
                for enemy in destroyed_enemy:
                    # target_sound.play()
                    ammo_sprites.remove(missile)
                    draw_sprites.remove(missile)
                    self.score += 10
                    self.no_enemy = True
                    
                if missile.rect.y < (-1 * missile.rect.size[1]):
                    ammo_sprites.remove(missile)
                    draw_sprites.remove(missile)

            # update position of missiles
            ammo_sprites.update()
            # Determine edges avoiding scaping of scenario
            if self.player.rect.x > SCREEN_WIDTH - self.player.rect.size[0]:
                self.player.rect.x = SCREEN_WIDTH - self.player.rect.size[0]
            if self.player.rect.x < 0:
                self.player.rect.x = 0
            if self.player.rect.y < 0:
                self.player.rect.y = 0
            if self.player.rect.y > SCREEN_HEIGHT - self.player.rect.size[1]:
                self.player.rect.y = SCREEN_HEIGHT - self.player.rect.size[1]

            # Collision player-meteor recognition
            collision = pygame.sprite.spritecollide(self.player, meteor_sprites, False)
            if len(collision) != 0 and self.won != True:
                self.collided = True

            # Collision player-star recognition
            collision = pygame.sprite.spritecollide(self.player, star_sprite, False)
            if len(collision) != 0 and self.collided != True:
                self.won = True

            for meteors in meteor_sprites:
                if meteors.rect.y > (meteors.rect.size[1] + SCREEN_HEIGHT):
                    meteor_sprites.remove(meteors)
                    draw_sprites.remove(meteors)

                    # new meteor
                    meteoroid = Meteor(random.randint(0, 6))
                    meteoroid.rect.x = random.randrange(SCREEN_WIDTH  - 100)
                    meteoroid.rect.y = random.randrange(SCREEN_HEIGHT - 300) - 350

                    # update list of sprites
                    draw_sprites.add(meteoroid)
                    meteor_sprites.add(meteoroid)


                meteors.rect.y += 1

            for bullet in bullet_sprites:
                collision = pygame.sprite.spritecollide(self.player, bullet_sprites, False)
                if len(collision) != 0 and self.won != True:
                    self.collided = True

                if bullet.rect.y > (bullet.rect.size[1] + SCREEN_HEIGHT):
                    bullet_sprites.remove(bullet)
                    draw_sprites.remove(bullet)

            if self.no_enemy is False:
                self.t += 1
                if self.t == 50:
                    bullet = Bullet()
                    bullet.rect.x = self.enemy.rect.x + self.enemy.rect.size[0]/2
                    bullet.rect.y = self.enemy.rect.y
                    draw_sprites.add(bullet)
                    bullet_sprites.add(bullet)
                    self.t = 0
             
            bullet_sprites.update()
            meteor_sprites.update()
            enemy_sprites.update()

        else:
            pass

    def render(self):
        # Main Scene
        screen.blit(bg_gameplay, [0, 0])

        if self.won and not self.collided:
            if not self.sound_play:
                won_sound.play()
                self.sound_play = True
            screen.blit(self.winning_text, [self.gameover_text_x, self.gameover_text_y])

        draw_sprites.draw(screen)

        score_text = self.score_font.render("Score: " + str(self.score), True, WHITE)
        screen.blit(score_text, [10, 10])

        if self.collided and not self.won:
            if not self.sound_play:
                gameover_sound.play()
                self.sound_play = True
            screen.blit(self.gameover_text, [self.gameover_text_x, self.gameover_text_y])



    def switch(self, nextScene):
        # Delete sprites for transition of scenes
        for sprite in draw_sprites:
            draw_sprites.remove(sprite)
        for sprite in meteor_sprites:
            meteor_sprites.remove(sprite)
        for sprite in enemy_sprites:
            meteor_sprites.remove(sprite)
        for sprite in star_sprite:
            meteor_sprites.remove(sprite)
        for sprite in bullet_sprites:
            meteor_sprites.remove(sprite)

        self.pause = False
        self.collided = False
        self.won = False
        self.t = 0
        self.no_enemy = False
        self.sound_play = False
        self.next = nextScene



class RecordScene():
    """ Best score record """

    def __init__(self):
        self.next = self
        self.count_record = [-0.4, 0]

    def inputHandler(self, event):
        for direction in str(inputs):
            if direction == '2':
                   self.switch(MenuScene())

    def update(self):
        # Handling animation of title
        if self.count_record[0] >= (len(record_imgs) - 0.4):
            pass
        else:
            self.count_record[0] += 0.3

        self.count_record[1] += 1
        if self.count_record[1] == 300:
            self.count_record = [-0.4, 0]

    def render(self):
        screen.blit(bg_record, [0, 0])
        screen.blit(record_imgs[int(self.count_record[0])], [SCREEN_WIDTH/5, 60])

    def switch(self, nextScene):
        self.next = nextScene


class AboutScene():
    """ Authorship and credits and how to play"""

#    how_font       = pygame.font.SysFont('purisa', 45, True, True)
    credits_font   = pygame.font.SysFont('purisa', 15, True, True)
    copyright_font = pygame.font.SysFont('arial', 15, True, True)
    body_font      = pygame.font.SysFont('arial', 30, True, True)

#    how_text       = how_font.render("How to Play: ", True, WHITE)
    body1_text      = body_font.render("Button1: Shoot", True, ORANGE)
    body2_text      = body_font.render("Button2: Pause", True, ORANGE)
    body3_text      = body_font.render("Button1->2: Menu", True, ORANGE)
    credits_text   = credits_font.render("Some images and sprites were found at https://opengameart.org/ ", True, WHITE)
    copyright_text = copyright_font.render("\u00a9 2018 Junaid Kahn - Kelve Henrique - Sebastian Dichler", True, BLUE)

    def __init__(self):
        self.next = self
        self.count_about = [-0.4, 0]

    def inputHandler(self, event):
        for direction in str(inputs):
            if direction == '2':
                   self.switch(MenuScene())

    def update(self):
        # Handling animation of title
        if self.count_about[0] >= (len(about_imgs) - 0.4):
            pass
        else:
            self.count_about[0] += 0.3

        self.count_about[1] += 1
        if self.count_about[1] == 300:
            self.count_about = [-0.4, 0]

    def render(self):
        screen.blit(bg_about, [0, 0])
        screen.blit(about_imgs[int(self.count_about[0])], [SCREEN_WIDTH/4, 60])
#        screen.blit(title_imgs[int(self.count_title[0])], [60, 60])
#        screen.blit(self.how_text,       [SCREEN_WIDTH/3, SCREEN_HEIGHT/6 + 100])
        screen.blit(self.body1_text,     [SCREEN_WIDTH/4, SCREEN_HEIGHT/6 + 150])
        screen.blit(self.body2_text,     [SCREEN_WIDTH/4, SCREEN_HEIGHT/6 + 200])
        screen.blit(self.body3_text,     [SCREEN_WIDTH/4, SCREEN_HEIGHT/6 + 250])
        screen.blit(self.credits_text,   [SCREEN_WIDTH/7, SCREEN_HEIGHT - 100])
        screen.blit(self.copyright_text, [SCREEN_WIDTH/4, SCREEN_HEIGHT - 50])

    def switch(self, nextScene):
        self.next = nextScene


# Get the Clock object
clock = pygame.time.Clock()


# Variables
fps = 60                            # Frames per Second
active_scene = VersionScene()       # state of game


dir_tick = 0.0

while active_scene != None:
    # Limit the framerate
    d_time_ms = clock.tick(fps)

    # Adjusting Meteors on the screen
    d_time = d_time_ms / 8
    dir_tick += d_time

    # Read port for coord.
    inputs = port.read(10)

    # flush buffer from port
    port.reset_input_buffer()

    # Correspondent scene handling
    active_scene.inputHandler(inputs)
    active_scene.update()
    active_scene.render()
    active_scene = active_scene.next

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active_scene = None

    # Update screen
    pygame.display.flip()


# Quit game
pygame.quit()
sys.exit()
