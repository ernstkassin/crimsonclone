# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 8:23:51 2022

@author: Ernst
"""
import pygame
import random
import numpy as np
import time 
#import requests
#import matplotlib.pyplot as plt

import os

#import gc
#os.chdir(r'C:\Users\Ernst\Documents\projects\games\crimsonclone\assets')

# Get the path to the script's directory (works on GitHub and locally)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define assets directory relative to the script
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# dont bother asking permissions for sound files when initializing pygame
pygame.mixer.quit()
# intialize pygame
pygame.init()
print("Initializing game...")  # Debugging initialization

#init dictionary of words
font = pygame.font.SysFont('cambria', 33)


               

try: 
    dictionary = np.genfromtxt(os.path.join(ASSETS_DIR, 'crimsonwords.txt'), delimiter='\n', dtype='str')
    print(f"Loaded {len(dictionary)} words.")  # Debug
except Exception as e:
    print(f"Error loading dictionary: {e}")  # Debug
#dictionary = np.genfromtxt('words.txt',delimiter='\n',dtype='str')


#dictionary = np.loadtxt('woods.txt',delimiter='\n',dtype='str')
#dictionary = np.concatenate(np.char.split(dictionary, sep=' '))

high_score = int(np.loadtxt(os.path.join(ASSETS_DIR, 'high_score.txt')))
# init screen
screen = pygame.display.set_mode((1200,900))
# title and icon
pygame.display.set_caption("Space Invaders")
print("Screen initialized.")  # Debug
#icon = pygame.image.load('spaceship.png')
#pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load(os.path.join(ASSETS_DIR, 'player.png'))
playerX = 600
playerY = 800
playerX_change = 0
user_text = ''
#kill_count = 0


# enemy
#enemyImg = []
#enemyX = []
#enemyY = []
#enemyX_change = []
#enemyWord = []
#num_enemies = 4

wpm_arr,accuracy_arr = [],[]

num_enemies = 4

enemyImg = [pygame.image.load(os.path.join(ASSETS_DIR, 'monster.png')) for _ in range(num_enemies)]
enemyX = [random.randint(0, 1100) for _ in range(num_enemies)]
enemyY = [random.randint(0, 50) for _ in range(num_enemies)]
enemyWord = [random.choice(dictionary) for _ in range(num_enemies)]  # Safe word selection

#enemyY_change = 0.05 * (1.1) ** 5  # Ensuring this is initialized only once
enemyY_change = 0.25 * (1.1) ** 5 
# bullet
bulletImg = pygame.image.load(os.path.join(ASSETS_DIR, 'bullet.png'))
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 8*5
bullet_state = "ready"

end_text = ""
score = 0

def player(x,y):
    screen.blit(playerImg,(x,y))
    

def score_(x,y,score,user_text):
    s_score = font.render("score: "+str(score),True,(0,0,0))
    s_text = font.render(str(''.join(user_text)),True,(0,0,0))
    s_high_score = font.render("high_score: " + str(high_score),True,(0,0,0))
  #  s_text1 = font.render("Score",True,(0,0,0))
  #  s_text2 = font.render("High score",True(0,0,0))
  #  screen.blit(s_text1,(x-10,y))
    screen.blit(s_score,(x,y))
    screen.blit(s_high_score,(x+930,y))
    screen.blit(s_text,(x+600,y+700))
    
def enemy(x,y,i):
    text = font.render(enemyWord[i], True, (0,0,255))
    screen.blit(enemyImg[i],(x,y))
    screen.blit(text,(x,y+30))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x,y))
    
def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = np.sqrt((enemyX-bulletX)**2+(enemyY-bulletY)**2)
    return (distance < 27)



# game loop
    

start_time = time.time()
wpm = 0
attempts,accuracy = 1,1
while 1:
    screen.fill((0,128,128))
    #user_text = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT: ## defined in pygame.locals
            pygame.quit()
 #           sys.exit()
        if event.type == pygame.KEYDOWN:

           
           if event.key == pygame.K_RETURN:
               attempts += 1
               word = ''.join(user_text)
               if word in enemyWord:
                   i = enemyWord.index(word)
                   playerX = enemyX[i]
                   bulletX = playerX
                   fire_bullet(bulletX,bulletY)
                   if np.mod(score,10) == 0:
                       enemyY_change *= 1.10
                       stop_time = time.time()
                       time10word = stop_time - start_time
                       wpm = 600/time10word
                       start_time = time.time()
                       wpm_arr.append(wpm)
                       accuracy_arr.append(accuracy*100)
                       print("wpm: ",wpm,"accuracy: ",accuracy)
               elif word == "reset":
                    # enemy
                    enemyImg = []
                    enemyX = []
                    enemyY = []
                    enemyX_change = []
                    enemyWord = []
                    num_enemies = 5

                    for i in range(num_enemies):
                        enemyImg.append(pygame.image.load(os.path.join(ASSETS_DIR, 'monster.png')))
                        enemyWord.append(dictionary[np.random.randint(len(dictionary))])
                        enemyX.append(random.randint(0,1100))
                        enemyY.append(random.randint(-100,0))
    #enemyX_change.append(0.5)
                        enemyY_change = 0.25*(1.1)**5
                    score = 0
                    attempts = 1
                    end_text = ""
                    start_time = time.time()
                    wpm_arr,accuracy_arr = [],[]
              # elif word == "plot":
              #     plt.figure(0)
              #     xvec = np.linspace(0,len(wpm_arr),len(wpm_arr))
              #     plt.plot(xvec[1:],wpm_arr[1:],label = 'wpm')
              #     plt.plot(xvec[1:],accuracy_arr[1:],label = 'accuracy')
              #     plt.legend()
              #     plt.show()
                

               user_text = []
           elif event.key == pygame.K_BACKSPACE:
               user_text = user_text[:-1]
           else:
               user_text += event.unicode
        
    for i in range(num_enemies):
        if enemyY[i] > 777:
            for j in range(num_enemies):
                enemyY[j] = 2000
                end_text = "YOU LOSE!"
            if score > high_score:
                with open('high_score.txt', 'w') as f:
                        f.write(str(score))
            break
                
            print("Score:",score)
        enemyY[i] += enemyY_change
            
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            bullet_state = "ready"
            bulletY = 800
            enemyX[i] = random.randint(0,768)
            enemyY[i] = random.randint(0,10)
            enemyWord[i] = dictionary[np.random.randint(len(dictionary))]
            while len(np.unique(enemyWord)) < num_enemies:
                enemyWord[i] = dictionary[np.random.randint(len(dictionary))]
            score += 1
            accuracy = (score+1)/attempts
        enemy(enemyX[i],enemyY[i],i)
    
    if bulletY <= -300:
        bulletY = 800
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    
    player(playerX,playerY)
    score_(20,20,score,user_text)
    #score_(20,40,high_score,[]#)
    
    
    s_lose = font.render(end_text,True,(0,0,0))
    screen.blit(s_lose,(500,400))


    #wpm = score * 60 / (time.time() - start_time)
    s_wpm = font.render("wpm:" + str(round(wpm)),True,(0,0,0))
    if score > 10:
        screen.blit(s_wpm,(1050,50))
    
    s_accuracy = font.render("accuracy:" + str(round(accuracy*100,1)),True,(0,0,0))
    screen.blit(s_accuracy,(950,80))
    
    pygame.display.update()
    


