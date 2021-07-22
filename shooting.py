import pygame
import random
import time
import tkinter as tk

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(r"images/shooter/shooter1.png").convert()
        self.surf = pygame.transform.scale(self.surf, (40, 40))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

        self.surf2 = pygame.image.load(r"images/shooter/shooter2.png").convert()
        self.surf2 = pygame.transform.scale(self.surf2, (40, 40))
        self.surf2.set_colorkey((255, 255, 255), RLEACCEL)

        self.rect = self.surf.get_rect(center=(300, 750))

    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.ani = 1
        self.surf = pygame.image.load(f"images/enemies/e{str(self.ani)}.png").convert()
        self.surf = pygame.transform.scale(self.surf, (46, 46))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(random.randint(15, SCREEN_WIDTH - 15), -10))
        # self.rect = self.surf.get_rect(center=(200, 20))
        self.speed = random.randint(1, 4)

    def update(self, l):
        self.rect.move_ip(0, +self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            l.append(1)


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super(Bullet, self).__init__()
        self.surf = pygame.image.load(r"images/shooter/bullet1.png").convert()
        self.surf = pygame.transform.scale(self.surf, (25, 25))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(player.rect.center[0], 715))
        self.speed = 5

    def update(self):
        self.rect.move_ip(0, -self.speed)
        if self.rect.bottom < 0:
            self.kill()


def number(type, posx, posy, size, dis, iList=None, iNumber=None):
    if iList is not None:
        pass
    else:
        iList = list(iNumber)
        if len(iList) == 1:
            iList = ['0'] + iList


    iList = [[i, [3, 5, size]] for i in iList]
    if type == 'sword':

        iList = [['sword2', [11, 10, int(size/2)]]] + iList

    elif type == 'heart':
        iList = iList + [['heart2', [11, 10, 4]]]

    elif type == 'bheart':
        iList = iList + [['heart3', [13, 10, 4]]]

    for i in range(0, len(iList)):
        name = f'images/{iList[i][0]}.png'
        img = pygame.image.load(name)
        img = pygame.transform.scale(img, (iList[i][1][0] * iList[i][1][2], iList[i][1][1] * iList[i][1][2]))
        length = 0
        for x in range(0, i):
            length = length + iList[x][1][0] * iList[x][1][2] + dis
        main.blit(img, (posx + length, posy))



def animation(animate):
    for i in animate:
        if i[1] == 4 * 4:
            pass
        else:
            img = pygame.image.load(f"images/enemies/e{str(int(i[1] / 4))}.png")
            img = pygame.transform.scale(img, (46, 46))
            main.blit(img, (i[0][0] - 23, i[0][1] - 23))
            i[1] = i[1] + 1


def health(main, w, l):
    size = 8
    try:
        sc = str(100 - l)
    except ZeroDivisionError:
        sc = '100'

    if int(sc) <= 0:
        sc = ['0', '0']
        number('bheart', 490, 50, size, 5, iList=sc)
        pygame.display.flip()
        pygame.time.delay(1300)

        main.fill((0, 0, 0))
        img = pygame.image.load("images/text/str/game over.png")
        img = pygame.transform.scale(img, (6*39, 6*5))
        main.blit(img, (300-int((39*6)/2), 250))
        number('sword', 259, 300, 6, 5, iNumber=str(w))
        pygame.display.flip()
        pygame.time.delay(1200)

        def return_name():
            name.append(ent.get())
            get_name.destroy()

        name = []

        get_name = tk.Tk()
        lbl = tk.Label(get_name, text="enter your name")
        ent = tk.Entry(get_name)
        btn = tk.Button(get_name, text="Submit", command=return_name)
        
        lbl.pack(pady=10)
        ent.pack(pady=10, padx=15)
        btn.pack(pady=10)
        tk.mainloop()

        try:
            file = open('highscores/HS', 'a')
            file.write(f"\n({name[0]}, {w})")
            file.close()
        except:
            pass

        option = 0
        HSpage = True
        while HSpage:
            pressed_keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        HSpage = False
                elif event.type == QUIT:
                    HSpage = False

                if pressed_keys[K_LEFT]:
                    option -= 1
                    if option == -1:
                        option = 2
                    print(option)

                elif pressed_keys[K_RIGHT]:
                    option += 1
                    if option == 3:
                        option = 0
                    print(option)

            main.fill((0, 0, 0))




        quit()

        # quit()

    number('heart', 490, 50, size, 5, iNumber=sc)


def kills(w):
    size = 8
    number('sword', 10, 50, size, 5, iNumber=str(w))


pygame.init()

main = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter game')
pygame.display.set_icon(pygame.transform.scale(pygame.image.load(r"icons/icon3.png"), (32, 32)))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 2250)


difficulty = 1
DIFFICULTY = pygame.USEREVENT + 2
pygame.time.set_timer(DIFFICULTY, 25000)
# pygame.time.set_timer(DIFFICULTY, 250)

t2r = 70

recharge = t2r

player = Player()

bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
# all_sprites.add(player)

# clock = pygame.time.Clock()

w = 0
l = [1 for i in range(0, 99)]

animate = []

running = True

healed = False
while running:
    recharge -= 1
    # print(pygame.time.get_ticks())
    pygame.time.delay(10)
    pressed_keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

        if event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        if event.type == DIFFICULTY:
            difficulty += 1
            print(int((1.2**(3-difficulty))*10000))
            pygame.time.set_timer(ADDENEMY, int((1.2**(4-difficulty))*1000))

        if pressed_keys[K_UP] and recharge < 0:
            recharge = t2r
            # print("shooty shoot")
            new_bullet = Bullet()
            bullets.add(new_bullet)
            all_sprites.add(new_bullet)

    player.update(pressed_keys)
    enemies.update(l)

    bullets.update()

    main.fill((0, 0, 0))

    if recharge < 0:
        main.blit(player.surf, player.rect)
    else:
        main.blit(player.surf2, player.rect)

    for entity in all_sprites:
        main.blit(entity.surf, entity.rect)

    x = pygame.sprite.groupcollide(enemies, bullets, dokilla=True, dokillb=True)
    for i in x:
        w += 1
        # print(i.rect.center)
        animate.append([i.rect.center, 4])

    # print(w, len(l))

    if w % 10 == 0 and w > 0 and not (healed):
        l.pop()
        healed = True
    elif not (w % 10 == 0):
        healed = False

    kills(w)
    health(main, w, len(l))
    animation(animate)

    pygame.display.flip()

    # clock.tick(50)
