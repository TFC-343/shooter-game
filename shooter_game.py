#! /usr/bin/env python3.9
import pprint
import sys

from shooter_code.data import *
import pygame
from pygame.locals import (
    QUIT,
    KEYDOWN
)

from shooter_code import game_code
from shooter_code import shop_code

__doc__ = """shooter game 2!"""
__author__ = "TFC343"
__version__ = "2.0.0"
__build__ = "29"


pygame.init()

# fps
fps = pygame.time.Clock()

# create surface
surf = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
surf.fill(BACKGROUND_COLOUR)
# pygame.mouse.set_visible(False)

pygame.display.set_caption('Shooter game')
pygame.display.set_icon(pygame.transform.scale(pygame.image.load(r"shooter_code/icons/icon3.png"), (32, 32)))


class Shooter(pygame.sprite.Sprite):
    def __init__(self):
        super(Shooter, self).__init__()

        img = pygame.image.load("shooter_code/images/shooter/shooter1.png")
        img = pygame.transform.scale(img, (30, 30))
        img.set_colorkey(BLACK)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (300, 310)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


def start_game(surf):
    game_code.shooter_game(surf, shooter_from_sql(get_shooter()))


# groups
pointers = pygame.sprite.Group()

# selection
selec = Selector(425, 7,
                 ['play', lambda surf: start_game(surf)],
                 ['shop', lambda surf: shop_code.open_shop(surf)],
                 ['quit', quit])

# shooter
shooter = Shooter()

# text size multiplier
SIZE = Multiplier(5.2)


def game_loop():
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
                    selec.execute(surf)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        ##################################
        #             update             #
        ##################################

        ()

        ##################################
        #             render             #
        ##################################

        surf.fill(BACKGROUND_COLOUR)


        build_word("shooter game", surf, 300, 60, 5, 1, 'centre')
        # pygame.draw.line(surf, CYAN, (300, 0), (300, 800))

        selec.draw(surf)

        pygame.display.update()
        fps.tick(FPS)


if __name__ == '__main__':
    game_loop()
