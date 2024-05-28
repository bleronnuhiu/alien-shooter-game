import pygame
from pygame import sprite, transform, image, key, event, display, font, mixer
from random import randint
from pygame.locals import *

pygame.init()

# Initialize and play background music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

# Fonts and labels
font.init()
font1 = font.SysFont(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.SysFont(None, 36)

score = 0  # Variable to track the player's score (number of ships hit)
goal = 10
lost = 0  # Variable to track the number of missed ships
max_lost = 3

# Parent class for other sprites
class GameSprite(sprite.Sprite):
    # Class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Call the class constructor (Sprite)
        sprite.Sprite.__init__(self)

        # Load and scale the sprite image
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed  # Set the sprite's speed

        # Set the sprite's position
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # Method to draw the sprite on the window
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Main player class
class Player(GameSprite):
    # Method to control player movement with keyboard arrows
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

# Enemy sprite class
class Enemy(GameSprite):
    # Method to update enemy position
    def update(self):
        self.rect.y += self.speed
        global lost
        # Reset enemy position if it goes beyond the screen
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

# Bullet sprite class
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

# Create the game window
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

# Create player sprite instance
ship = Player("rocket.png", 5, win_height - 100, 80, 100, 10)

# Create enemy sprites
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

# Create a group for bullets
bullets = sprite.Group()

# Game over flag
finish = False

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Main game loop
game = True  # Flag to keep the game running
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

    if not finish:
        window.blit(background, (0, 0))  # Refresh the background

        # Display the score and number of missed ships
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        # Update player, enemy, and bullet sprites
        ship.update()
        monsters.update()
        bullets.update()

        # Redraw sprites
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        # Check for collisions
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        # Check for losing condition
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        # Check for winning condition
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

    display.update()
    clock.tick(60)  # Limit the frame rate to 60 FPS

pygame.quit()

'''
Key Changes:
Fixed fire method: Changed self.centerx to self.rect.centerx and corrected the call to bullet.add() to bullets.add().
Added bullets group: Ensured the bullets are updated and drawn correctly on the screen by creating and managing the bullets sprite group.
Collision handling: Added collision detection and scoring logic for when bullets hit the enemies.
Game loop updates: Updated the main game loop to handle bullet updates and rendering properly.
'''
