#!/usr/bin/env python3

import pygame
import random
import os
import sys
import serial
import math
import euclid

# Initialise Pygame
pygame.init()

# Define relevant colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define screen size and set it
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode(SCREEN_SIZE)

# Define initial velocity of Meteors
initial_velocity = 1
d_time = 0.0

# Define stamps
score = 000
score_font = pygame.font.SysFont('purisa', 25, True, True)
score_text = score_font.render("Score: " + str(score), True, WHITE)

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
bg_img = pygame.image.load("./assets/bg.jpg").convert()
# ship_img = pygame.image.load("./assets/Sprites/Ships/spaceShips_008.png").convert()
# ship_img.set_colorkey(BLACK)
# meteor_img = pygame.image.load("./assets/Sprites/Meteors/spaceMeteors_001.png").convert()


# Classes
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("./assets/ship.png").convert()
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()


class Missile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("./assets/fire.png").convert()
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
    
        

def get_velocity():
    angle = random.uniform(0, math.pi*2)
    x_axis = math.sin(angle) 
    y_axis = math.cos(angle)
    vector = euclid.Vector2(x_axis, y_axis)
    vector.normalize()
    vector *= initial_velocity
    return vector

# Handling of sprites
draw_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
ammo_sprites = pygame.sprite.Group()

# Instatiating actors
player = Ship()
player.rect.x = SCREEN_WIDTH/2 - 80
player.rect.y = SCREEN_HEIGHT-120
draw_sprites.add(player)

for i in range(10):
    # set random velocity
    velocity = get_velocity()

    # set random position
    x = random.randrange(SCREEN_WIDTH)
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
fps = 60             # Frames per Second
is_running = True    # state of game

# Set the port communication
port = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.0)

collided = False
dir_tick = 0.0
while is_running:
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
            is_running = False

    # Read port for coord.
    rcv = port.read(10)
    
    # Control Ship with sensor
    for direction in str(rcv):
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
            print('Second Button pressed!')

    # Target down recognition
    for missile in ammo_sprites:
        destroyed_meteor = pygame.sprite.spritecollide(missile, meteor_sprites, True)
        for meteor in destroyed_meteor:
            # target_sound.play()
            ammo_sprites.remove(missile)
            draw_sprites.remove(missile)
            score += 1

        if missile.rect.y < (-1 * missile.rect.size[1]):
            ammo_sprites.remove(missile)
            draw_sprites.remove(missile)

    # update position of missiles
    ammo_sprites.update()

    # flush buffer from port
    port.reset_input_buffer()

    # Determine edges avoiding scaping of scenario
    if player.rect.x > SCREEN_WIDTH - player.rect.size[0]:
        player.rect.x = SCREEN_WIDTH - player.rect.size[0]
    if player.rect.x < 0:
        player.rect.x = 0
    if player.rect.y < 0:
        player.rect.y = 0
    if player.rect.y > SCREEN_HEIGHT - player.rect.size[1]:
        player.rect.y = SCREEN_HEIGHT - player.rect.size[1]

           
    # Collision recognition
    collision = pygame.sprite.spritecollide(player, meteor_sprites, False)
    if len(collision) != 0:
       collided = True
       # is_running = False


    # Main Scene
    screen.blit(bg_img, [0, 0])
    if collided:
        screen.blit(gameover_text, [gameover_text_x, gameover_text_y])

    score_text = score_font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, [10, 10]) 
    draw_sprites.draw(screen)

    # Update screen
    pygame.display.flip()


# Quit game
pygame.quit()
sys.exit()
