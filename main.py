import pygame
from pygame.locals import (
K_ESCAPE,
K_i,
MOUSEBUTTONDOWN,
MOUSEWHEEL,
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
grey = (50, 0, 176)

#buttons
font = pygame.font.SysFont('Arial Black', 16, False, False)

# screen size
scr_w = 1280
scr_h = 720

#timers for the game
spawntime = 1000
changedirtime = 250
timetodie = 1000

#definitions and classes
def update_keys(self, pressed_keys):
    if pressed_keys[K_ESCAPE]:
       pygame.quit()

def current_milli_time():
    return round(time.time() * 1000)

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
        (x, y) = pygame.mouse.get_pos()
        if x > self.rect.left and x < self.rect.right and y > self.rect.top and y < self.rect.bottom:
            self.current = self.surf2
        else:
            self.current = self.surf






# klasa objektu sprawdzającego czas reakcji
class Target(pygame.sprite.Sprite):
    def __init__(self):
        super(Target, self).__init__()
        self.surf = pygame.Surface((75, 75))
        self.surf = pygame.image.load("tareget.png").convert()
        self.surf.set_colorkey(black)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(scr_w/2 - 300 + 200, scr_w/2 + 150 + 300),
                random.randint(scr_h/2 - 200, scr_h/2 + 200)
            )
        )
        self.speed = random.randint(1, 10)
        self.isAlive = True
        self.Start = current_milli_time()
        self.Next = 0
        self.movedirx = random.randrange(-1, 2, 1)
        self.movediry = random.randrange(-1, 2, 1)
        self.Die = current_milli_time()

    def update(self): #add flag for existing one of targets
        if  current_milli_time() - self.Start > self.Next:
            self.movedirx = random.randrange(-1, 2, 1)
            self.movediry = random.randrange(-1, 2, 1)
            self.Next = random.randint(200, 500)
            self.Start = current_milli_time()

        if current_milli_time() - self.Die > timetodie:
            self.kill()
            self.isAlive = False

        self.rect.move_ip(self.movedirx * self.speed, self.movediry * self.speed)

        if self.rect.right < 0 or self.rect.left < 0:
            self.kill()
            self.isAlive = False
        elif self.rect.bottom < 0 or self.rect.top < 0:
            self.kill()
            self.isAlive = False
        elif self.rect.right > 1250:
            self.kill()
            self.isAlive = False
        elif self.rect.bottom > 660:
            self.kill()
            self.isAlive = False
        elif self.rect.top < 60:
            self.kill()
            self.isAlive = False
        elif self.rect.left < 435:
            self.kill()
            self.isAlive = False

    def checkIfAlive(self):
        if self.isAlive == False:
            addtarget
        #elif self.isAlive == True:




# setting up the screen
screen = pygame.display.set_mode([scr_w, scr_h])
instruction = pygame.image.load("Instruction.png", ).convert()
#
addtarget = pygame.USEREVENT + 1
pygame.time.set_timer(addtarget, spawntime)

#flags
running = True
onealive = True

# targets for the player
target = Target()
all_sprites = pygame.sprite.Group()
all_sprites.add(target)

button = Button('Start 1 ',75, 70)
button3 = Button('Start 2',225, 70)
button2 = Button('Sound',225, 150)
button4 = Button('Hard mode',75, 150)

# main loop
while running:

    # quting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == K_ESCAPE:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            (x, y) = pygame.mouse.get_pos()
            #print(x, y)
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



    clock.tick(60)
    all_sprites.update() #add mouse event to kill and update

    pygame.display.flip()


pygame.quit()
