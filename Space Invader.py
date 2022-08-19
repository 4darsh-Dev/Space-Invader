import pygame
import random
import math
from pygame import mixer

pygame.init()

# initialize the window of the game 
screen = pygame.display.set_mode((800, 600))

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 490
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY  = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 6

for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.5)
    enemyY_change.append(40)

# Background Image
backgroundImg = pygame.image.load("space_background.jpg")
mixer.music.load("background.mp3")
mixer.music.play(-1)
volume = 0.125
mixer.music.set_volume(volume)


# Background Sound



# bullet
bulletImg = pygame.image.load("bullet_light_color.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

# Score
score_val = 0
score_font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x, y):
    score = score_font.render("Score : " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("Game Over", True, (225, 225, 225))
    screen.blit(over_text, (200, 250))

def write_score(score):
    with open('hiscore.txt','w') as f:
        f.write(str(score))



def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet1(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x-5, y+10))


def fire_bullet2(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+45, y+10))

def isCollison(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(((enemyX - bulletX)**2) + ((enemyY - bulletY)**2))

    if distance < 32 :
        return True
    else:
        return False
    


# Game Loop

running = True
while(running):

    # Background color in (R,G,B)format:
    screen.fill((76, 156, 185))

    screen.blit(backgroundImg, (0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #if keystroke is pressed whether it is left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1.7
            if event.key == pygame.K_RIGHT:
                playerX_change = 1.7
            if event.key == pygame.K_UP:
                if bullet_state is "ready":
                    # bullet sound
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bullet_sound.set_volume(volume)
                    # Gets the x coordinate of spaceship and saves it to the bulletX
                    bulletX = playerX
                    fire_bullet1(bulletX, bulletY)
                    fire_bullet2(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT : 
                playerX_change = 0
        
        
            
    # for preventing player bouncing off out of the window when it hits the boundary
    playerX += playerX_change

    if playerX <= 0:
            playerX = 0
    elif playerX >= 736 :
            playerX  = 736

    # Enemy movement
    
    # for enemy spaceship bouce off saving and handling
    for i in range(number_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break 
        
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.9
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.9
            enemyY[i] += enemyY_change[i]

        # Collison
        collison = isCollison(enemyX[i], enemyY[i], bulletX, bulletY)
        if collison:
            # explosion sound 
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            explosion_sound.set_volume(0.04)
               
            bulletY = 480
            bullet_state = "ready"
            score_val += 50
            
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
        
    if bullet_state is "fire":
        fire_bullet1(bulletX, bulletY)
        fire_bullet2(bulletX, bulletY)
        bulletY -= bulletY_change

    

    player(playerX, playerY)
    show_score(textX, textY)
    write_score(int(score_val))
    pygame.display.update()