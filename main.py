import pygame
from pygame.locals import (
K_ESCAPE,
K_i,
)
from pygame.locals import (
MOUSEBUTTONDOWN,
MOUSEWHEEL,
)
import random

random.seed(None)
pygame.init()
clock = pygame.time.Clock()
# screen size
scr_w = 1280
scr_h = 720

#timers for the game
spawntime = 500
changedirtime = 250


#definitions and classes
def update_keys(self, pressed_keys):
    if pressed_keys[K_ESCAPE]:
       pygame.quit()


# klasa objektu sprawdzającego czas reakcji
class Target(pygame.sprite.Sprite):
    def __init__(self):
        super(Target, self).__init__()
        self.surf = pygame.Surface((75, 75))
        self.surf.fill((127, 255, 0))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(scr_w/2 - 20 + 200, scr_w/2 + 150 + 200),
                random.randint(scr_h/2 - 20, scr_h/2 + 100)
            )
        )
        self.speed = random.randint(1, 2)

    def update(self): #add flag for existing one of targets
        movedir = random.randint(1, 5)
        if movedir == 1:
            self.rect.move_ip(self.speed, self.speed)
        elif movedir == 2:
            self.rect.move_ip(-self.speed, self.speed)
        elif movedir == 3:
            self.rect.move_ip(self.speed, -self.speed)
        elif movedir == 4:
            self.rect.move_ip(-self.speed, -self.speed)

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

# setting up the screen
screen = pygame.display.set_mode([scr_w, scr_h])

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
    screen.fill((255, 255, 255))

    #creating the game surface inside the window
    surf = pygame.Surface((800, 600))
    surf.fill((0, 0, 0))
    rect = surf.get_rect()
    surf_center = (
        (scr_w - surf.get_width()) / 2 + 200,
        (scr_h - surf.get_height()) / 2
    )

    screen.blit(surf, surf_center)

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    #add spawning another targets after first one disappears


    clock.tick(30)
    all_sprites.update() #add mouse event to kill and update

    pygame.display.flip()


pygame.quit()
