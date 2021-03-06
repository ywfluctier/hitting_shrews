# coding: utf-8
# 1 - Import library
import pygame
import math
import random
from pygame.locals import *

time_teller = pygame.time.get_ticks

# 2 - Initialize the game
pygame.init()
pygame.mixer.init()
width, height = 700, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("打鼩鼬鼱")
positions_s = [(posx, posy) for posy in [150, 280, 410] for posx in [90, 280, 470]]
positions_h = [(posx, posy) for posy in [115, 245, 375] for posx in [110, 300, 490]]
positions_k = [(posx, posy) for posy in [190, 320, 450] for posx in [150, 340, 530]]
audio_k = [False for x in range(9)]
shrew_ques = {x: 0 for x in range(9)}
hammer_on = {x: 0 for x in range(9)}
player_score = 0
delayed_time_on_hit = 250
hold_time_before_hit = 1300
kissing_time = 400
heart_rate = 70

# 3 - Load images
raw_bg = pygame.image.load("resources/images/background.jpg")
raw_hole = pygame.image.load("resources/images/hole.png")
raw_shrew = pygame.image.load("resources/images/shrew.png")
raw_hammer = pygame.image.load("resources/images/hammer.png")
raw_kisses = pygame.image.load("resources/images/kisses.png")
raw_gameover = pygame.image.load("resources/images/gameover.png")
bg = pygame.transform.scale(raw_bg, (width, height))
hole = pygame.transform.scale(raw_hole, (150, 150))
shrew = pygame.transform.scale(raw_shrew, (150, 150))
hammer = pygame.transform.scale(raw_hammer, (100, 100))
kisses = pygame.transform.scale(raw_kisses, (25, 25))
gameover = pygame.transform.scale(raw_gameover, (width, height))

normal_img = pygame.image.load("resources/images/594x600.png")
cute_img = pygame.image.load("resources/images/600x582.png")
shy_img = pygame.image.load("resources/images/600x461.png")
heart_img = pygame.image.load("resources/images/heart.png")
normal = [pygame.transform.scale(normal_img.subsurface((x*594, 0), (594, 600)), (99, 100)) for x in range(2)]
cute = [pygame.transform.scale(cute_img.subsurface((x*600, 0), (600, 582)), (100, 97)) for x in range(5)]
shy = [pygame.transform.scale(shy_img.subsurface((x*600, 0), (600, 461)), (140, 108)) for x in range(6)]
heart = [pygame.transform.scale(heart_img, (x, x)) for x in [30, 36, 42]]

hit = pygame.mixer.Sound("resources/audio/hit.ogg")
hit.set_volume(0.5)
# score presentation
font = pygame.font.Font(None, 44)
survivedtext = font.render(str(player_score), True, (242, 173, 18))
textRect = survivedtext.get_rect()
textRect.topright = [635, 65]

# 4 - keep looping through
while True:
    if heart_rate > 300:
        screen.blit(gameover, (0, 0))
        break
    # 5 - clear the screen before drawing it again
    screen.fill(0)
    screen.blit(bg, (0, 0))
    # 6 - draw the screen elements -- shrew, hammer & hole
    for index in range(9):
        if hammer_on[index]:
            screen.blit(shrew, positions_s[index])
            screen.blit(hammer, positions_h[index])
            if time_teller() - hammer_on[index] > delayed_time_on_hit:
                shrew_ques[index] = hammer_on[index] = 0
        elif shrew_ques[index]:
            screen.blit(shrew, positions_s[index])
            mid = time_teller() - shrew_ques[index]
            if mid > hold_time_before_hit + kissing_time: # vanishing shrew
                shrew_ques[index] = 0
                audio_k[index] = False
            elif mid > hold_time_before_hit: # kissing shrew
                if not audio_k[index]:
                    #hit.play()# play audio
                    audio_k[index] = True
                    heart_rate += 10
                mid -= hold_time_before_hit
                screen.blit(
                    pygame.transform.scale(kisses, (25 + mid / 60, 25 + mid / 60)),
                    (positions_k[index][0], positions_k[index][1]-mid/20))
        else:
            screen.blit(hole, positions_s[index])
    # draw girl
    survivedtext = font.render('{}'.format(heart_rate), True, (255, 0, 0))
    screen.blit(survivedtext, (120, 70))

    time = time_teller()
    if heart_rate < 140:
        screen.blit(normal[time/500 % 2], (180, 30))
        screen.blit(heart[time/650 % 3], (70 - time/650%3*3, 70 - time/650%3*3))
    elif heart_rate < 210:
        screen.blit(cute[time/500 % 5], (180, 30))
        screen.blit(heart[time/330 % 3], (70 - time/330%3*3, 70 - time/330%3*3))
    else:
        screen.blit(shy[time/500 % 3], (170, 25))
        screen.blit(heart[time/100 % 3], (70 - time/100%3*3, 70 - time/100%3*3))

    # generate shrew
    if random.random() < 0.08:
        random_num = random.randint(0, 8)
        if not shrew_ques[random_num]:
            shrew_ques[random_num] = time_teller()


    # 7 - update the screen
    # screen.blit(shrew,positions_s[0])
    #screen.blit(cute, (150,150))

    # 8 - loop through the events
    for event in pygame.event.get():
        # check if the event is the X button
        if event.type == pygame.QUIT:
            # if it is quit the game
            pygame.quit()
            exit(0)
        elif event.type == pygame.KEYDOWN:
            if K_0 < event.key <= K_9:
                mid = event.key - 49
                # if shrew being up & not kissing
                if shrew_ques[mid] and time_teller() - shrew_ques[mid] < hold_time_before_hit:
                    hit.play()
                    player_score += 10
                    shrew_ques[event.key - 49] += delayed_time_on_hit
                    hammer_on[mid] = time_teller()
    # present player's score
    survivedtext = font.render(str(player_score), True, (255, 187, 119))
    screen.blit(survivedtext, textRect)
    pygame.display.flip()
pygame.display.flip()
while True:
    for event in pygame.event.get():
        # check if the event is the X button
        if event.type == pygame.QUIT:
            # if it is quit the game
            pygame.quit()
            exit(0)