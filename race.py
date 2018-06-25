

import pygame
import time
import random
 
pygame.init()

#############
crash_sound = pygame.mixer.Sound("crash.ogg")
#############
 
display_width = 800
display_height = 600

CAR_POSITION_X = (display_width * 0.45)
CAR_POSITION_Y = (display_height * 0.75)
 
black = (0,0,0)
charcoal = (100,100,100)
white = (255,255,255)

red = (200,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)
 
block_color = (210,105,30)
 
car_width = 73
 
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()
 
carImg = pygame.image.load('car.png')
gameIcon = pygame.image.load('car.png')

pygame.display.set_icon(gameIcon)

pause = False
#crash = True
 
def boxes_dodged(count):
    font = pygame.font.SysFont("comicsansms", 25)
    text = font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text,(0,0))
 
def boxes(boxx, boxy, boxw, boxh, color):
    pygame.draw.rect(gameDisplay, color, [boxx, boxy, boxw, boxh])
 
def car(x,y):
    gameDisplay.blit(carImg,(x,y))
 
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
 
 
def crash():
    ####################################
    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()
    ####################################
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("You Crashed", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        

        button("Play Again",150,450,100,50,green,bright_green,game_loop)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15) # The program will never run at more than 15 frames per second

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
    

def quitgame():
    pygame.quit()
    quit()

def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False
    

def paused():
    ############
    pygame.mixer.music.pause()
    #############
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # TODO: Add ability to press p again to unpause
        button("Continue",150,450,100,50,green,bright_green,unpause)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)   


def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(charcoal)
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects("MIB Racing!", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("GO!",150,450,100,50,green,bright_green,game_loop)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)
        
        
    
    

    
def game_loop():
    global pause
    ############
    pygame.mixer.music.load('test.ogg')
    pygame.mixer.music.play(-1)
    ############
    x = CAR_POSITION_X
    y = CAR_POSITION_Y
 
    x_change = 0
 
    
    box_startx = random.randrange(0, display_width)
    box_starty = -600
    box_speed = 4
    # starting size of block
    box_width = 100
    box_height = 100
 
    boxCount = 1 # TODO: Multiple blocks option
 
    dodged = 0
 
    gameExit = False
 
    while not gameExit:
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -20
                    
                if event.key == pygame.K_RIGHT:
                    x_change = 20
                if event.key == pygame.K_p:
                    pause = True
                    paused()
                    

                    
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
 
        x += x_change
        gameDisplay.fill(charcoal)
 
        boxes(box_startx, box_starty, box_width, box_height, block_color)
 
 
        
        box_starty += box_speed
        car(x,y)
        boxes_dodged(dodged)
 
        if x > display_width - car_width or x < 0:
            crash()
 
        if box_starty > display_height:
            box_starty = 0 - box_height
            # x starting point of box -- random ensures boxes fall from different places along the screen
            box_startx = random.randrange(0,display_width)
            dodged += 1
            # Speed of oncoming traffic(e.g. blocks) gradually
            box_speed += 1
            # UNCOMMENT THIS IF you want: The more blocks you dodge, the bigger the blocks become
            # box_width += (dodged * 1.2)
 
        if y < box_starty+box_height:
            print('y crossover')
 
            if x > box_startx and x < box_startx + box_width or x+car_width > box_startx and x + car_width < box_startx+box_width:
                print('x crossover')
                # Basically if the boxes coordinates == the cars, then crash is called
                crash()
        
        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()