#!/usr/bin/env python3

import pygame
import random
import os
import sys
import serial
import math
import euclid

# Set the port communication
port = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.0)

# Initialise Pygame
pygame.init()

# Define relevant colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE= (233, 166, 31)

# Define screen size and set it
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode(SCREEN_SIZE)

# Define initial velocity of Meteors
initial_velocity = 1
d_time = 0.0

# Define stamps
gameover_font = pygame.font.SysFont('symbola', 55, True, True)
gameover_text = gameover_font.render("Game Over", True, WHITE)

# gameover_text_rect = gameover_text.get_rect()
gameover_text_x = screen.get_width() / 2 - 100 # gameover_text_rect.width / 2
gameover_text_y = screen.get_height() / 2 - 100 # gameover_text_rect.height / 2

# Load sounds
shoot_sound = pygame.mixer.Sound("./assets/Audio/laser.ogg")
target_sound = pygame.mixer.Sound("./assets/Audio/target.ogg")

# Load graphics
meteors_assets = os.listdir("./assets/Meteors")
bg_gameplay = pygame.image.load("./assets/Backdrop/bg_23.jpg").convert()
bg_menu = pygame.image.load("./assets/Backdrop/bg_1.jpg").convert()
title_img = pygame.image.load("./assets/title.png").convert()
title_img.set_colorkey(BLACK)


# Classes
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("./assets/Ship/ship.png").convert()
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()


class Missile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("./assets/missile.png").convert()
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 20


class Meteor(pygame.sprite.Sprite):

    def __init__(self, offset, position, velocity = euclid.Vector2(0,0)):
        super().__init__()
        self.offset = offset
        self.position = position
        self.velocity = velocity

        self.image = pygame.image.load("./assets/Meteors/" + meteors_assets[offset]).convert()
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()

    def set_velocity(self, velocity):
        velocity.y += 1
        self.velocity = velocity

    def update(self):
        self.position += self.velocity * d_time
        self.rect.x, self.rect.y = int(self.position.x), int(self.position.y)



# Declaring the various scenes of the game:
#   - VersionScene
#   - MenuScene
#   - GameplayScene
#   - RecordScene
#   - AboutScene


class VersionScene():
    """ Welcomming scene with title and version """

    def __init__(self):
        self.next = self
        self.counter = 0

    def imputHandler(self, event):
        pass

    def update(self):
        if self.counter < 20:
            screen.fill(BLACK)
        else:
            screen.fill(WHITE)

        switchScene(GameplayScene())

        pass

    def sceneRender(self):
        pass

    def switchScene(self, nextScene):
        if self.counter < 40:
            pass
        else:
            self.next = nextScene
            self.counter = 0


class MenuScene():
    """ Present buttons in menus:
            - Game
            - Record
            - About
            - Quit
    """

    def __init__(self):
        self.next = self
        self.counter = 0
        self.dir = 1

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
               self.switch(GameplayScene())

    def update(self):
        if self.dir == 1:
            self.counter += 0.2
        else:
            self.counter -= 0.2

        if self.counter > 22:
            self.dir = 0
        if self.counter < 1:
            self.dir = 1

    def render(self):
        screen.blit(bg_menu, [0, 0])
        screen.blit(title_img, [60, 60])
        screen.blit(self.sprites[int(self.counter)], [500, 250])

    def switch(self, nextScene):
        self.next = nextScene


class GameplayScene():
    """ Where the action takes place  """
    score = 000
    score_font = pygame.font.SysFont('purisa', 25, True, True)
    score_text = score_font.render("Score: " + str(score), True, WHITE)

    def __init__(self):
        self.next = self
        self.collided = False

    def inputHandler(self, inputs):#, player, draw_sprites, ammo_sprites):
        # Control Ship with sensor
        for direction in str(inputs):
            if direction == 'R':
                player.rect.x += 2
            elif direction == 'r':
                player.rect.x += 1
            elif direction == 'L':
                player.rect.x -= 2
            elif direction == 'l':
                player.rect.x -= 1
            elif direction == 'U':
                player.rect.y -= 2
            elif direction == 'u':
                player.rect.y -= 1
            elif direction == 'D':
                player.rect.y += 2
            elif direction == 'd':
                player.rect.y += 1
            elif direction == '1':
                shoot_sound.play()
                missile = Missile()
                missile.rect.x = player.rect.x + player.rect.size[0]/2
                missile.rect.y = player.rect.y
                draw_sprites.add(missile)
                ammo_sprites.add(missile)
            elif direction == '2':
                self.switch(MenuScene())


    def update(self):#, meteor_sprites, ammo_sprites, draw_sprites):
        # Target down recognition
        for missile in ammo_sprites:
            destroyed_meteor = pygame.sprite.spritecollide(missile, meteor_sprites, True)
            for meteor in destroyed_meteor:
                # target_sound.play()
                ammo_sprites.remove(missile)
                draw_sprites.remove(missile)
                self.score += 1

            if missile.rect.y < (-1 * missile.rect.size[1]):
                ammo_sprites.remove(missile)
                draw_sprites.remove(missile)

        # update position of missiles
        ammo_sprites.update()
        # Determine edges avoiding scaping of scenario
        if player.rect.x > SCREEN_WIDTH - player.rect.size[0]:
            player.rect.x = SCREEN_WIDTH - player.rect.size[0]
        if player.rect.x < 0:
            player.rect.x = 0
        if player.rect.y < 0:
            player.rect.y = 0
        if player.rect.y > SCREEN_HEIGHT - player.rect.size[1]:
            player.rect.y = SCREEN_HEIGHT - player.rect.size[1]

        self.collided = False
        # Collision recognition
        collision = pygame.sprite.spritecollide(player, meteor_sprites, False)
        if len(collision) != 0:
           self.collided = True
           # is_running = False

    def render(self):
        # Main Scene
        screen.blit(bg_gameplay, [0, 0])
        if self.collided:
            screen.blit(gameover_text, [gameover_text_x, gameover_text_y])

        score_text = self.score_font.render("Score: " + str(self.score), True, WHITE)
        screen.blit(score_text, [10, 10])
        draw_sprites.draw(screen)


    def switch(self, nextScene):
        self.next = nextScene


class RecordScene():
    """ Best score record """

    def __init__(self):
        self.next = self

    def imputHandler(self, event):
        pass

    def update(self):
        pass

    def sceneRender(self):
        pass

    def switchScene(self, nextScene):
        self.next = nextScene


class AboutScene():
    """ Authorship and credits """

    def __init__(self):
        self.next = self

    def imputHandler(self, event):
        pass

    def update(self):
        pass

    def sceneRender(self):
        pass

    def switchScene(self, nextScene):
        self.next = nextScene


def get_velocity():
    angle = random.uniform(0, math.pi*2)
    x_axis = math.sin(angle)
    y_axis = math.cos(angle)
    vector = euclid.Vector2(x_axis, y_axis)
    vector.normalize()
    vector *= initial_velocity
    return vector

# Handling of sprites
draw_sprites = pygame.sprite.Group()        # sprites to draw
meteor_sprites = pygame.sprite.Group()      # sprites of meteors
ammo_sprites = pygame.sprite.Group()        # sprites of missiles

# Instatiating actors
player = Ship()
player.rect.x = SCREEN_WIDTH/2 - 80
player.rect.y = SCREEN_HEIGHT-120
draw_sprites.add(player)

for i in range(10):
    # set random velocity
    velocity = get_velocity()

    # set random position
    x = random.randrange(SCREEN_WIDTH  - 100)
    y = random.randrange(SCREEN_HEIGHT - 300)

    # new meteor
    meteoroid = Meteor(i, euclid.Vector2(x, y), velocity )
    meteoroid.update()

    # update list of sprites
    draw_sprites.add(meteoroid)
    meteor_sprites.add(meteoroid)


# Get the Clock object
clock = pygame.time.Clock()

# Name the window
pygame.display.set_caption('Haste Space')

# Variables
fps = 60                         # Frames per Second
active_scene = MenuScene()#GameplayScene()    # state of game


dir_tick = 0.0

while active_scene != None:
    # Limit the framerate
    d_time_ms = clock.tick(fps)

    # Adjusting Meteors on the screen
    d_time = d_time_ms / 8
    dir_tick += d_time

    if dir_tick > 1.0:
        dir_tick = 0
        new_velocity = get_velocity()
        one_random = random.randrange(10)
        for met in meteor_sprites:
            if met.offset == one_random:
                met.set_velocity(new_velocity)
                met.update()
                break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active_scene = None

    # Read port for coord.
    inputs = port.read(10)

    # flush buffer from port
    port.reset_input_buffer()

    # Correspondent scene handling
    active_scene.inputHandler(inputs)
    active_scene.update()
    active_scene.render()
    active_scene = active_scene.next

    # Update screen
    pygame.display.flip()


# Quit game
pygame.quit()
sys.exit()
