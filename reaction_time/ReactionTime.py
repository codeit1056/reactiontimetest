import pygame
import time
from sys import exit
from random import randint
pygame.init()

WIDTH,HEIGHT = 700,400

window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Reaction Time')
hovering = False
font = pygame.font.Font('assets/start_text.ttf',50)
is_on_press = False
screen_on_time = pygame.time.get_ticks()
clock = pygame.time.Clock()

# Title
title_intro = font.render('Reaction Time Test',False,'White')
title = title_intro.get_rect(center = (335,100))

# Waiting/red screen
wait_screen = pygame.image.load('assets/wait_screen.xcf').convert()
wait = wait_screen.get_rect(topleft = (0,0))
wait_text = font.render('Wait',False,'White')
wait_order = wait_text.get_rect(center = (335,300))

# Sreen which you are supposed to press on - green screen
press_screen = pygame.image.load('assets/press_screen.xcf').convert()
press = press_screen.get_rect(topleft = (0,0))

continue_hover = False
finished = False

while True:
    start_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if not is_on_press:
        # Check if there is mousemotion on the waiting screen and if there is wait a certain amount of time then switch
        # to the pressing screen - green
        if event.type == pygame.MOUSEMOTION and finished == False and pygame.time.get_ticks() > 1250:
            time.sleep(randint(2,5))
            if wait.collidepoint(event.pos):
                is_on_press = True
                when_green = pygame.time.get_ticks()

    else:
        # Show the time passed from when it turns green
        passing_time = start_time - when_green
        window.blit(press_screen,press)
        passing_text = font.render(f'Reaction Time:{passing_time}ms',False,'White')
        passing_time_ms = passing_text.get_rect(center = (350,200))
        window.blit(passing_text,passing_time_ms)
        if event.type == pygame.MOUSEMOTION and finished == False:
            if press.collidepoint(event.pos):
                hovering = True
        
        # If the screen is pressed then switch the screen back to red and show the reaction time
        if event.type == pygame.MOUSEBUTTONDOWN and hovering and finished == False:
            hovering = False
            finished = True
            is_on_press = False
            window.blit(wait_screen,wait)
            window.blit(passing_text,passing_time_ms)
            # Save scores in a file
            with open('scores.txt','a') as scores:
                scores.write(f'{passing_time}\n')
            
    # Only blits to the screen if is_on_press is false and if the game is not finished
    if not is_on_press and finished == False:
        window.blit(wait_screen,wait)
        window.blit(title_intro,title)
        window.blit(wait_text,wait_order)
                    
    pygame.display.update()
    clock.tick(60)