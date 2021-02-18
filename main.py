import pygame
import random
from pygame import mixer
from tkinter import *
from tkinter.ttk import *

# Initializing the pygame modules
pygame.init()

# Creating a screen
running = False
homeScreen = Tk()
homeScreen.title('Space Invaders')
homeScreen.geometry('350x200')

style = Style()
style.configure('TButton', font=('Merchant Copy', 15, 'bold'), background='black', borderwidth='4')


def GameLoop(value):
    global running
    running = value  # Game loop Runner
    homeScreen.destroy()


Label(homeScreen, text="Space Invaders", font=('LCD Solid', 15)).pack(side=TOP, pady=10)

btn = Button(homeScreen, text='Start', style='TButton', command=lambda: GameLoop(True))
btn.pack(side=TOP, padx=0, pady=3)

btn2 = Button(homeScreen, text='Quit', command=lambda: GameLoop(False))
btn2.pack(side=TOP, padx=0, pady=3)

homeScreen.mainloop()

screen = None
if running:
    screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("resource\\background.png")

# Background Music
if running:
    mixer.music.load("resource\\background.wav")
    mixer.music.set_volume(0.1)
    mixer.music.play(-1)

# Title and icon
# Icons made by Freepik from www.flaticon.com
icon = pygame.image.load("resource\\Space Invader.png")
pygame.display.set_caption("Space Invader")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("resource\\Space Ship.png")
playerX = 368
playerY = 520
playerX_change = 0
playerY_change = 0
player_speed_change_ALNE = 0  # After loading new enemies

# Score
score = 1
font = pygame.font.Font("freesansbold.ttf", 24)

# Enemy
# Icons made by from www.flaticon.com
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 1
enemyspeedL = 0.08  # Lower Limit
enemyspeedU = 0.15  # Upper Limit


def showScore():
    scoreValue = font.render("Score: " + str(score - 1), True, (255, 255, 255))
    screen.blit(scoreValue, (0, 0))


def loadEnemies():
    for villain in range(no_of_enemies):
        enemyImg.append(pygame.image.load("resource\\Alien_small.png"))
        enemyX.append(random.randrange(0, 736))
        enemyY.append(random.randrange(0, 150))
        enemyX_change.append(0.08)
        enemyY_change.append(0.08)


loadEnemies()

# Bullet
bulletImg = pygame.image.load("resource\\bullet_player.png")
bulletX = 368 + 16
bulletY = 520 + 5
bulletY_change = 0.7
bullet_state = "Ready"


def bullet(x, y):
    screen.blit(bulletImg, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    for enemies in range(no_of_enemies):
        screen.blit(enemyImg[enemies], (x, y))


def fire(x, y):
    screen.blit(bulletImg, (x, y))


def collided(collision_enemyX, collision_enemyY, collision_bulletX, collision_bulletY):
    distanceX = collision_enemyX - collision_bulletX
    distanceY = collision_enemyY - collision_bulletY
    if -48 <= distanceX <= 16 and -48 < distanceY < 0:
        return True
    else:
        return False


# Game Loop
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change = -(0.2 + player_speed_change_ALNE)
            if event.key == pygame.K_d:
                playerX_change = (0.2 + player_speed_change_ALNE)
            if event.key == pygame.K_w:
                playerY_change = -(0.2 + player_speed_change_ALNE)
            if event.key == pygame.K_s:
                playerY_change = (0.2 + player_speed_change_ALNE)
            if event.key == pygame.K_SPACE:
                if bullet_state is "Ready":
                    bullet_state = "Fire"
                    bullet_sound = mixer.Sound("resource\\laser.wav")  # Bullet sound --> "phew phew"
                    bullet_sound.set_volume(0.5)
                    bullet_sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                playerX_change = 0
            if event.key == pygame.K_d:
                playerX_change = 0
            if event.key == pygame.K_w:
                playerY_change = 0
            if event.key == pygame.K_s:
                playerY_change = 0

    playerX += playerX_change
    playerY += playerY_change

    # Player Conditions
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    if playerY <= 300:
        playerY = 300
    elif playerY >= 536:
        playerY = 536

    collision = []
    # Enemy Conditions
    for i in range(no_of_enemies):
        if enemyX[i] <= 0:
            enemyX_change[i] = random.uniform(enemyspeedL, enemyspeedU)
        elif enemyX[i] >= 736:
            enemyX_change[i] = -random.uniform(enemyspeedL, enemyspeedU)
        if enemyY[i] <= 0:
            enemyY_change[i] = random.uniform(enemyspeedL, enemyspeedU)
        elif enemyY[i] >= 150:
            enemyY_change[i] = -random.uniform(enemyspeedL, enemyspeedU)
        enemy(enemyX[i], enemyY[i])
        collision.append(collided(enemyX[i], enemyY[i], bulletX, bulletY))
        enemyX[i] += enemyX_change[i]
        enemyY[i] += enemyY_change[i]
        if collision[i]:  # If the bullet hits the enemy
            mixer.Sound("resource\\explosion.wav").play()  # Explosion sound --> "phys phys"
            bullet_state = "Ready"
            score += 1
            enemyX[i] = random.randrange(0, 736)
            enemyY[i] = random.randrange(0, 150)
            enemyX_change[i] = -enemyX_change[i]
            enemyY_change[i] = -enemyY_change[i]
            if 0 < score <= 10:
                if score % 5 == 1:
                    no_of_enemies += 1
                    loadEnemies()
                    player_speed_change_ALNE += 0.1
                    enemyspeedL += 0.05
                    enemyspeedU += 0.05
                    bulletY_change += 0.175
            elif 10 < score <= 30:
                if score % 10 == 1:
                    no_of_enemies += 1
                    loadEnemies()
                    player_speed_change_ALNE += 0.2
                    enemyspeedL += 0.1
                    enemyspeedU += 0.1
                    bulletY_change += 0.35

    if bullet_state == "Fire":
        fire(playerX + 16, playerY + 5)
        bulletY -= bulletY_change
        if bulletY < 0:
            bullet_state = "Ready"
    else:
        bulletX = playerX + 16
        bulletY = playerY + 5

    bullet(bulletX, bulletY)
    player(playerX, playerY)
    showScore()

    pygame.display.update()

pygame.quit()
