import pygame

time = pygame.time.get_ticks
pygame.init()
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
rheart = pygame.image.load('resources/images/heart.png')
heart = pygame.transform.scale(rheart, (50, 50))

mm = pygame.sprite.Sprite()
counter = 0.0
while True:
    screen.fill(0)
    counter += 1
    if counter < 800:
        heart = pygame.transform.scale(rheart, (40 + int(counter) / 80, 40 + int(counter) / 80))
        ro_heart = pygame.transform.rotate(heart, counter * 0.05)
        lastx, lasty = 250-counter/200, \
                       250 -counter*counter/40000
        screen.blit(ro_heart, (lastx - ro_heart.get_rect().width/2,
                               lasty- ro_heart.get_rect().height/2))
    elif counter < 1600:
        delta = counter - 800
        heart = pygame.transform.scale(rheart,(50+int(delta)/80,50+int(delta)/80))
        ro_heart = pygame.transform.rotate(heart, 80 - counter * 0.05)
        screen.blit(ro_heart, (lastx - ro_heart.get_rect().width / 2 + delta/200,
                               lasty - ro_heart.get_rect().height / 2-delta*delta/40000))
    else:
        counter = 0
        print time()
    # if time() < 800:
    #     degree += 1
    #     bak_degree = degree
    #     ro_heart = pygame.transform.rotate(heart, degree * 0.05)
    #     lastx, lasty = 250-degree/125, \
    #                    250 -degree*degree/125/125
    #     screen.blit(ro_heart, (lastx - ro_heart.get_rect().width/2,
    #                            lasty- ro_heart.get_rect().height/2))
    #
    #
    # elif time() < 1600:
    #     degree += 1
    #     ro_heart = pygame.transform.rotate(heart, bak_degree * 0.1 - degree * 0.05 )
    #     screen.blit(ro_heart, (lastx - ro_heart.get_rect().width / 2 + (degree-bak_degree)/300,
    #                            lasty - ro_heart.get_rect().height / 2 - ((degree-bak_degree)/300)**2))

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print counter,time()
            pygame.quit()
            exit(0)
