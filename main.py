import pygame
from pygame.locals import (
K_ESCAPE,
MOUSEBUTTONDOWN,
MOUSEBUTTONUP,
)
import sys
import random
import time
             
random.seed(None)
pygame.init()
clock = pygame.time.Clock()

#colors
black = (0, 0, 0)
white = (255, 255, 255)

#buttons
font = pygame.font.SysFont('Arial Black', 16, False, False)

# screen size
scr_w = 1280
scr_h = 720

#timers for the game
spawntime = 1000
timetodie = 1000

#definitions and classes
def update_keys(self, pressed_keys):
    if pressed_keys[K_ESCAPE]:
       pygame.quit()

def current_milli_time():
    return round(time.time() * 1000)

#class for buttons
class Button(pygame.sprite.Sprite):
    def __init__(self, text, x, y):
        super(Button, self).__init__()
        #self.surf = pygame.Surface((130, 35)) wielkosc obrazka
        self.surf = pygame.image.load("button1.png").convert()
        self.surf2 = pygame.image.load("button2.png").convert()
        self.text = font.render(text, True, black)
        self.rect = self.surf.get_rect(
            center=(
                x,
                y,
            )
        )
        self.rect2 = self.text.get_rect(
            center=(
                x,
                y,
            )
        )
        self.current = self.surf

    def draw(self, screen):
        screen.blit(self.current, self.rect)
        screen.blit(self.text, self.rect2)

    def update(self):
        (mx, my) = pygame.mouse.get_pos()
        if mx > self.rect.left and mx < self.rect.right and my > self.rect.top and my < self.rect.bottom:
            self.current = self.surf2
        else:
            self.current = self.surf



# class for square targets
class Target(pygame.sprite.Sprite):
    def __init__(self):
        super(Target, self).__init__()
        self.surf = pygame.Surface((75, 75))
        self.surf = pygame.image.load("tareget.png").convert()
        self.rect = self.surf.get_rect(
            center=(
                random.randint(scr_w/2 - 300 + 200, scr_w/2 + 150 + 300),
                random.randint(scr_h/2 - 200, scr_h/2 + 200)
            )
        )
        self.speed = random.randint(1, 2)
        self.Start = current_milli_time()
        self.Next = 0
        self.movedirx = random.randrange(-1, 2, 1)
        self.movediry = random.randrange(-1, 2, 1)
        self.Die = current_milli_time()
        self.deathtimer = 0

    def update(self):
        if  current_milli_time() - self.Start > self.Next:
            self.movedirx = random.randrange(-1, 2, 1)
            self.movediry = random.randrange(-1, 2, 1)
            self.Next = random.randint(200, 500)
            self.Start = current_milli_time()

        if current_milli_time() - self.Die > timetodie:
            self.kill()

        self.rect.move_ip(self.movedirx * self.speed, self.movediry * self.speed)

        if self.rect.right < 0 or self.rect.left < 0:
            self.kill()
        elif self.rect.bottom < 0 or self.rect.top < 0:
            self.kill()
        elif self.rect.right > 1250:
            self.kill()
        elif self.rect.bottom > 660:
            self.kill()
        elif self.rect.top < 60:
            self.kill()
        elif self.rect.left < 435:
            self.kill()

    def deathtimer(self): #keeping record of time needed to kill target
        if current_milli_time() - self.Die > timetodie:
            self.kill()
            self.deathtimer = timetodie
        else:
            self.deathtimer = current_milli_time() - self.Die



# setting up the screen
screen = pygame.display.set_mode([scr_w, scr_h])
instruction = pygame.image.load("Instruction.png", ).convert()

#
addtarget = pygame.USEREVENT + 1
pygame.time.set_timer(addtarget, spawntime)

#flags
mainmenu = True
running = False
onealive = True
clicking = False

# targets for the player
target = Target()
all_sprites = pygame.sprite.Group()
all_sprites.add(target)

#Menu buttons
button = Button('Start 1 ', 75, 70)
button3 = Button('Start 2', 225, 70)
button2 = Button('Sound', 225, 150)
button4 = Button('Stop', 75, 150)

score = 0

# creating a main menu for the player to start the game when wanted to not in start of application

while mainmenu:
    (mx, my) = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if (mx < button.rect2.right and mx > button.rect2.left and my > button.rect2.top and my < button.rect2.bottom):
                    running = True
                    mainmenu = False
        elif event.type == pygame.QUIT:
                mainmenu = False

    screen.fill(white)
    # creating blank surface inside the window
    surf = pygame.Surface((800, 600))
    surf.fill(black)
    rect = surf.get_rect()
    surf_center = (
        (scr_w - surf.get_width()) / 2 + 200,
        (scr_h - surf.get_height()) / 2
    )
    screen.blit(surf, surf_center)
    screen.blit(instruction, (0, 300))
    button.draw(screen)
    button2.draw(screen)
    button3.draw(screen)
    button4.draw(screen)
    button.update()
    button2.update()
    button3.update()
    button4.update()
    pygame.display.flip()


# main loop
while running:

    (mx, my) = pygame.mouse.get_pos()
    #quting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == K_ESCAPE:
            running = False
            pygame.quit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                clicking = True
                if (mx < button3.rect2.right and mx > button3.rect2.left and my > button3.rect2.top and my < button3.rect2.bottom):
                    running = False
                    mainmenu = True
        elif event.type == MOUSEBUTTONUP:
                clicking = False
        elif event.type == addtarget:
            new_target = Target()
            all_sprites.add(new_target)


    # background fill
    screen.fill(white)

    #creating the game surface inside the window
    surf = pygame.Surface((800, 600))
    surf.fill(black)
    rect = surf.get_rect()
    surf_center = (
        (scr_w - surf.get_width()) / 2 + 200,
        (scr_h - surf.get_height()) / 2
    )

    screen.blit(surf, surf_center)
    screen.blit(instruction, (0, 300))
    button.draw(screen)
    button2.draw(screen)
    button3.draw(screen)
    button4.draw(screen)
    button.update()
    button2.update()
    button3.update()
    button4.update()


    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
        if mx < entity.rect.right and mx > entity.rect.left  and my > entity.rect.top  and my < entity.rect.bottom:
            if clicking == True:
                entity.kill()



    clock.tick(60)
    all_sprites.update() #add mouse event to kill and update
    #target.deathtimer()

    pygame.display.flip()

pygame.quit()
