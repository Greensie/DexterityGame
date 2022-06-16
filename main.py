import pygame
from pygame.locals import *
import random


random.seed(None)
pygame.init()
clock = pygame.time.Clock()
# wielkość okna
scr_w = 1280
scr_h = 720
spawntime = 500
changedirtime = 250


# def update(self, pressed_keys):
#    if pressed_keys[K_ESCAPE]:
#        running = False

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
        self.speed = random.randint(1, 5)

    def update(self):
        movedir = random.randint(1,5)
        if movedir == 1:
            self.rect.move_ip(self.speed, self.speed)
            wait
        elif movedir == 2:
            self.rect.move_ip(-self.speed, self.speed)
        elif movedir == 3:
            self.rect.move_ip(self.speed, -self.speed)
        elif movedir == 4:
            self.rect.move_ip(-self.speed, -self.speed)

        print(self.rect)
        if self.rect.right < 0:
            self.kill()
        elif self.rect.right > 1250:
            self.kill()
        elif self.rect.bottom < 0:
            self.kill()
        elif self.rect.bottom > 660:
            self.kill()


screen = pygame.display.set_mode([scr_w, scr_h])
addtarget = pygame.USEREVENT + 1
pygame.time.set_timer(addtarget, spawntime)
running = True

# obiekty do klikania
target = Target()
all_sprites = pygame.sprite.Group()
all_sprites.add(target)

# główna pętla programu
while running:

    # koniec działania programu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == K_ESCAPE:
            running = False

    # wypełnienie tła
    screen.fill((255, 255, 255))

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

    clock.tick(100)
    all_sprites.update()

    pygame.display.flip()


pygame.quit()
