import pprint
import sys

import pygame
from pygame.locals import (
    QUIT,
    KEYDOWN,
    K_ESCAPE
)

from shooter_code import game_code
from shooter_code import shop_code
from shooter_code.data import *  # along with pygame


# fps
fps = pygame.time.Clock()


class Pointer(pygame.sprite.Sprite):
    items = [['play', 425], ['shop', 500], ['achievements', 575], ['settings', 650],  ['quit', 725]]

    def __init__(self):
        super().__init__()
        img = pygame.image.load("shooter_code/images/shooter/shooter90.png")
        img = pygame.transform.scale(img, (40, 40))
        img.set_colorkey(BLACK)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (100, 425)
        self.current_item = 0

    def move_up(self):
        if self.items[self.current_item] == self.items[0]:
            pass
        else:
            self.current_item -= 1

    def move_down(self):
        if self.items[self.current_item] == self.items[-1]:
            pass
        else:
            self.current_item += 1

    def execute(self):
        command = self.items[self.current_item][0]
        if command == 'quit':
            pygame.quit()
            sys.exit()
        elif command == 'play':
            kills = game_code.shooter_game(
                user_lives=1,
                user_lasersight=True,
                recharge_time=70,
            )
            print(kills)
        elif command == 'shop':
            shop_code.open_shop()

    def draw(self, surface):
        self.rect.center = (100, self.items[self.current_item][1])
        surface.blit(self.image, self.rect)


# groups
pointers = pygame.sprite.Group()


# player
P1 = Pointer()
pointers.add(P1)

# text size multiplier
SIZE = Multiplier(5.2)


def test(surf):
    being_ran = True
    while being_ran:
        for event in pygame.event.get():
            if event.type == QUIT:
                being_ran = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    being_ran = False
        surf.fill(BLACK)

        build_word("abcdefghijklmnopqrstuvwxyz", surf, 300, 250, 4, 1)
        build_word("0123456789", surf, 300, 300, 4, 1)
        build_word("1a2b4c", surf, 300, 350, 4, 1)
        build_word("26abc", surf, 300, 400, 4, 1)

        pygame.display.update()


def settings(surf):

    def equip_gun(gun):
        file = sql.connect("shooter_code/data/data.db")
        cs = file.cursor()
        if gun[14]:
            cs.execute(f"UPDATE user SET current_shooter = '{gun[0]}'")
        file.commit()
        file.close()

    file = sql.connect("shooter_code/data/data.db")
    cs = file.cursor()
    cs.execute(f"SELECT * FROM shooters")
    fetch = cs.fetchall()
    file.close()

    print(fetch)
    t = []
    for i in fetch:
        t.append([i[1], i[14]])

    selec = Selector(300, 4.2,
                     [fetch[0][1], lambda surf: equip_gun(fetch[0])],
                     [fetch[1][1], lambda surf: equip_gun(fetch[1])],
                     [fetch[2][1], lambda surf: equip_gun(fetch[2])],
                     [fetch[3][1], lambda surf: equip_gun(fetch[3])])


    running = True
    while running:

        ##################################
        #             event              #
        ##################################

        for event in pygame.event.get():  # quits game
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selec.move_down()
                elif event.key == pygame.K_UP:
                    selec.move_up()
                elif event.key == pygame.K_RETURN:
                    if selec.options[selec.current_item][2] == 'quit':
                        running = False
                    else:
                        selec.execute(surf)
                elif event.key == pygame.K_ESCAPE:
                    running = False

        ##################################
        #             update             #
        ##################################

        ()

        ##################################
        #             render             #
        ##################################

        surf.fill(BACKGROUND_COLOUR)

        selec.draw(surf)

        build_word("pick a shooter:", surf, 300, 60, 7, 1, 'centre')
        # pygame.draw.line(surf, CYAN, (300, 0), (300, 800))

        pygame.display.update()
        fps.tick(FPS)


if __name__ == '__main__':
    settings()
