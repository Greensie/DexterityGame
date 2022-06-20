import pygame
import pylab
from pygame.locals import (
    K_ESCAPE,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
)
import random
import time
import matplotlib
import matplotlib.backends.backend_agg as agg
matplotlib.use("Agg")

random.seed(None)
pygame.init()
clock = pygame.time.Clock()
pygame.mixer.init()
honk = pygame.mixer.Sound("horn.wav")

# colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# buttons
font = pygame.font.SysFont('Arial Black', 16, False, False)

# screen size
scr_w = 1280
scr_h = 720

# timers for the game
spawntime = 1000
timetodie = 1000

number = range(1, 11)
deaths = []
deaths2 = []
start = 1
end = 3

fig = pylab.figure(figsize=[8, 6], dpi=100)
ax = fig.gca()
bx = fig.gca()


# definitions and classes
def update_keys(self, pressed_keys):
    if pressed_keys[K_ESCAPE]:
        pygame.quit()


def current_milli_time():
    return round(time.time() * 1000)


# class for buttons
class Button(pygame.sprite.Sprite):
    def __init__(self, text, x, y):
        super(Button, self).__init__()
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
                random.randint(scr_w / 2 - 300 + 200, scr_w / 2 + 150 + 300),
                random.randint(scr_h / 2 - 200, scr_h / 2 + 200)
            )
        )
        self.speed = random.randint(start, end)
        self.Start = current_milli_time()
        self.Next = 0
        self.movedirx = random.randrange(-1, 2, 1)
        self.movediry = random.randrange(-1, 2, 1)
        self.Die = current_milli_time()
        self.deathtimer = 0

    def update(self):
        if current_milli_time() - self.Start > self.Next:
            self.movedirx = random.randrange(-1, 2, 1)
            self.movediry = random.randrange(-1, 2, 1)
            self.Next = random.randint(200, 500)
            self.Start = current_milli_time()

        if current_milli_time() - self.Die > timetodie:
            self.kill()

        self.rect.move_ip(self.movedirx * self.speed, self.movediry * self.speed)

        if self.rect.right < 0 or self.rect.left < 0 or self.rect.bottom < 0 or self.rect.top < 0:
            self.Die = timetodie
            self.kill()
        elif self.rect.right > 1250 or self.rect.bottom > 660 or self.rect.top < 60 or self.rect.left < 435:
            self.Die = timetodie
            self.kill()

    def kill(self):  # keeping record of time needed to kill target
        super().kill()
        global deaths
        deaths.append(current_milli_time() - self.Die)
        print(deaths, len(deaths))


class SoundTarget(pygame.sprite.Sprite):
    def __init__(self):
        super(SoundTarget, self).__init__()
        honk.play()
        self.StartS = current_milli_time()
        self.DieS = current_milli_time()
        self.NextS = 0

    def update(self):
        if current_milli_time() - self.StartS > self.NextS:
            self.NextS = random.randint(200, 500)
            self.StartS = current_milli_time()

        if current_milli_time() - self.DieS > timetodie:
            self.kill()

    def kill(self):
        super().kill()
        global deaths2
        deaths2.append(current_milli_time() - self.DieS)
        print(deaths2)


# setting up the screen
screen = pygame.display.set_mode([scr_w, scr_h])
instruction = pygame.image.load("Instruction.png", ).convert()

#
addtarget = pygame.USEREVENT + 1
pygame.time.set_timer(addtarget, spawntime)

addsoundtarget = pygame.USEREVENT + 2
pygame.time.set_timer(addsoundtarget, 2*spawntime)

# flags

running = True
onealive = True
clicking = False
game = 0
wasgame = 0

# targets for the player
target = Target()
all_sprites = pygame.sprite.Group()
#all_sprites.add(target)

#soundtarget = SoundTarget()
all_sprites2 = pygame.sprite.Group()
#all_sprites2.add(soundtarget)

# Menu buttons
button = Button('Start 1 ', 75, 70)
button3 = Button('Start 2', 225, 70)
button2 = Button('Sound', 225, 150)
button4 = Button('Hard mode :)', 75, 150)

score = 0

# creating a main menu for the player to start the game when wanted to not in start of application

while running:
    (mx, my) = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                clicking = True
                if (
                        mx < button.rect2.right and mx > button.rect2.left and my > button.rect2.top and my < button.rect2.bottom):
                    game = 1
                    deaths = []
                    deaths2 = []
                elif ( mx < button3.rect2.right and mx > button3.rect2.left and my > button3.rect2.top and my < button3.rect2.bottom):
                    game = 2
                    deaths = []
                    deaths2 = []
                elif (mx < button4.rect2.right and mx > button4.rect2.left and my > button4.rect2.top and my < button4.rect2.bottom):
                    start = 5
                    end = 10

        elif event.type == pygame.QUIT:
            running = False
        elif event.type == MOUSEBUTTONUP:
            clicking = False
        elif event.type == addtarget and game == 1:
            new_target = Target()
            all_sprites.add(new_target)
        elif event.type == addsoundtarget and game == 2:
            new_target = SoundTarget()
            all_sprites2.add(new_target)
        elif event.type == pygame.locals.KEYDOWN and event.key == K_ESCAPE:
            running = False

    # background fill

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

    if game == 1:
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
            if mx < entity.rect.right and mx > entity.rect.left and my > entity.rect.top and my < entity.rect.bottom:
                if clicking == True:
                    entity.kill()
                    wasgame = 1
        if len(deaths) == 10:
            game = 0
        clock.tick(60)
        all_sprites.update()
    if game == 2:
        for entity in all_sprites2:
            if (
                    mx < button2.rect2.right and mx > button2.rect2.left and my > button2.rect2.top and my < button2.rect2.bottom):
                if clicking == True:
                    entity.kill()
                    wasgame = 2
        if len(deaths2) == 10:
            game = 0

    if len(deaths) == 10 or len(deaths2) == 10:
        if wasgame == 1:
            ax = matplotlib.pyplot.plot(number,  deaths)
            canvas = agg.FigureCanvasAgg(fig)
        elif wasgame == 2:
            bx = matplotlib.pyplot.plot(number, deaths2)
            canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        surf = pygame.image.fromstring(raw_data, size, "RGB")
        screen.blit(surf, (440, 60))
        pygame.display.flip()

        clock.tick(60)
        all_sprites2.update()

    pygame.display.flip()

pygame.quit()