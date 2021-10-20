import random
import sqlite3
import sys
import copy

from shooter_code.data import *

import pygame
import pygame.time
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_RETURN,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)


class Player(pygame.sprite.Sprite):
    def __init__(self, new_lives, new_lasersight, new_recharge_time, new_speed):
        super().__init__()

        img1 = pygame.image.load("shooter_code/images/shooter/shooter1.png")
        img1 = pygame.transform.scale(img1, (40, 40))
        img1.set_colorkey(BLACK)
        self.image_green = img1

        img2 = pygame.image.load("shooter_code/images/shooter/shooter2.png")
        img2 = pygame.transform.scale(img2, (40, 40))
        img2.set_colorkey(BLACK)
        self.image_red = img2

        self.rect = self.image_red.get_rect()
        self.rect.center = (300, 750)

        self.speed = new_speed

        self.lives = new_lives
        self.lasersight = new_lasersight
        self.recharge_time = new_recharge_time   # time it takes for the shooter to recharge
        self.recharge = new_recharge_time  # how close the shooter is to being able to shoot again

    def draw(self, surface, type_):
        if self.lasersight:
            pygame.draw.line(surface, 'cyan', self.rect.center, (self.rect.center[0], 0))

        img = self.image_green if type_ == 'green' else self.image_red
        surface.blit(img, self.rect)

    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, new_penetration, new_pen_drop_off):
        super().__init__()

        img = pygame.image.load("shooter_code/images/shooter/bullet1.png")
        img = pygame.transform.scale(img, (25, 25))
        img.set_colorkey(BLACK)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (pos, 715)

        self.speed = 7
        self.penetration = new_penetration
        self.drop_off = new_pen_drop_off

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.rect.move_ip(0, -self.speed)
        if self.rect.bottom < 0:
            self.kill()

    def lower_penetration(self):
        if self.penetration - self.drop_off <= 0:
            self.penetration = 0
        else:
            self.penetration = self.penetration - self.drop_off


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.ani = 1

        self.speed = random.randint(2, 6)

        img = pygame.image.load(f"shooter_code/images/enemies/e{str(self.ani)}.png")
        img = pygame.transform.scale(img, (46, 46))
        img.set_colorkey(BLACK)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(15, SCREEN_WIDTH - 15), -10)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, player_):
        self.rect.move_ip(0, +self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            player_.lives = player_.lives - 1


def animation(surface, animate):
    """i coded this and yet have no idea how it works"""
    for i in animate:
        if i[1] == 4 * 4:
            pass
        else:
            img = pygame.image.load(f"shooter_code/images/enemies/e{str(int(i[1] / 4))}.png")
            img = pygame.transform.scale(img, (46, 46))
            surface.blit(img, (i[0][0] - 23, i[0][1] - 23))
            i[1] = i[1] + 1


def update_scores(score):
    # adds score to tokens
    file = sql.connect("shooter_code/data/data.db")
    cs = file.cursor()
    cs.execute("SELECT tokens FROM user")
    cs.execute(f"UPDATE user SET tokens = {cs.fetchall()[0][0] + score}")

    # updates high score
    cs.execute("SELECT high_score FROM user")
    fetch = cs.fetchall()[0][0]
    cs.execute(f"UPDATE user SET high_score = {fetch if fetch > score else score}")
    file.commit()
    file.close()


def game_over(surface, score, ):

    surface.fill(BACKGROUND_COLOUR)

    # pygame.draw.line(surface, CYAN, (300, 0), (300, 800))  # middle line or calibration

    # game over text and score

    build_word("game over", surface, 300, 250, 5, 1, 'centre')

    img = pygame.image.load("shooter_code/images/sword2.png")
    img = pygame.transform.scale(img, (img.get_width()*5, img.get_height()*5))
    rect = img.get_rect()
    rect.center = (265, 320)
    surface.blit(img, rect)

    build_word(str(score), surface, 315, 320, 5, 1, 'e')

    # pointer
    img = pygame.image.load("shooter_code/images/shooter/shooter90.png")
    img = pygame.transform.scale(img, (40, 40))
    img.set_colorkey(BLACK)
    rect = img.get_rect()
    rect.center = (100, 500)
    surface.blit(img, rect)

    # menu text
    build_word("menu", surface, 300, 500, 8, 1, 'centre')

    pygame.display.update()

    update_scores(score)

    # TODO display high score

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_RETURN:
                    running = False


def health(surface, score, hp):
    """
    displays the health
    surface: pygame surf
    score: amount of kills
    l: lives left
    """

    # if health drops bellow zero run game over screen
    if int(hp) <= 0:

        # displays borken heart
        img = pygame.image.load("shooter_code/images/heart3.png")
        img = pygame.transform.scale(img, (img.get_width()*4, img.get_height()*4))
        rect = img.get_rect()
        rect.center = (570, 65)
        surface.blit(img, rect)

        build_word('0', surface, 540, 65, 6, 1, 'w')

        pygame.display.update()

        pygame.time.delay(1300)  # waits for small amount of time to show death

        game_over(surface, score)

        return False

    img = pygame.image.load("shooter_code/images/heart2.png")
    img = pygame.transform.scale(img, (img.get_width()*4, img.get_height()*4))
    rect = img.get_rect()
    rect.center = (570, 65)
    surface.blit(img, rect)
    build_word(str(hp), surface, 540, 65, 6, 1, 'w')
    return True


def pause_menu(surf, score):
    print("paused")
    saved = copy.copy(surf)

    selec = Selector(250, 4,
                     ["continue", do_nothing],
                     ["back to menu", do_nothing],
                     ["quit", do_nothing])

    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    paused = False
                if event.key == K_DOWN:
                    selec.move_down()
                if event.key == K_UP:
                    selec.move_up()
                if event.key == K_RETURN:
                    if selec.current_item == 0:
                        paused = False
                    if selec.current_item == 1:
                        update_scores(score)  # updates scores
                        return True  # quits out of game loop
                    if selec.current_item == 2:
                        update_scores(score)
                        quit()
                    else:
                        selec.execute(surf)

        surf.blit(saved, (0, 0))  # displays backgorund
        s = pygame.Surface((600, 800), pygame.SRCALPHA)  # makes it darker

        s.fill(pygame.Color(0, 0, 0, 150))
        surf.blit(s, (0, 0))
        build_word("paused", surf, 300, 100, 6, 1)

        selec.draw(surf)

        pygame.display.update()

    print("playing")


def shooter_game(surf, user_shooter: ShooterDatabase):

    pygame.init()

    ADDENEMY = pygame.USEREVENT + 3
    pygame.time.set_timer(ADDENEMY, 2250)

    difficulty = 1
    change_difficulty = pygame.USEREVENT + 4
    pygame.time.set_timer(change_difficulty, 25000)

    recharge_time = user_shooter.recharge_speed[user_shooter.u_recharge_speed]
    speed = user_shooter.speed
    file = sql.connect("shooter_code/data/data.db")
    cs = file.cursor()
    cs.execute("SELECT start_health FROM user")
    user_lives = cs.fetchall()[0][0]
    file.close()

    player = Player(user_lives, user_shooter.lasersights, recharge_time, speed)  # our hero

    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    points = 0

    animate = []

    running = True

    fps = pygame.time.Clock()
    healed = False
    while running:

        ##################################
        #             event              #
        ##################################

        pressed_keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if pause_menu(surf, points):
                        running = False
            elif event.type == QUIT:
                running = False

            if event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)

            if event.type == change_difficulty:
                difficulty += 1
                print(int((1.2 ** (3 - difficulty)) * 10000))
                pygame.time.set_timer(ADDENEMY, int((1.2 ** (4 - difficulty)) * 1000))

        if (pressed_keys[K_UP] or pressed_keys[K_SPACE]) and player.recharge < 0:

            player.recharge = player.recharge_time
            bullet_penetration = user_shooter.penetration[user_shooter.u_penetration]
            penetration_drop_off = user_shooter.drop_off[user_shooter.u_drop_off]

            new_bullet = Bullet(player.rect.center[0], bullet_penetration, penetration_drop_off)
            bullets.add(new_bullet)

        ##################################
        #             update             #
        ##################################

        player.recharge -= 1

        player.update(pressed_keys)
        enemies.update(player)

        bullets.update()

        bullet_hit = pygame.sprite.groupcollide(bullets, enemies, False, False)

        enemy_hit = pygame.sprite.groupcollide(enemies, bullets, True, False)
        for i in enemy_hit:
            points += 1
            animate.append([i.rect.center, 4])

        for i in bullet_hit:
            if random.randint(0, 100) > i.penetration:
                i.kill()
            else:
                i.lower_penetration()

        # if points % 10 == 0 and points > 0 and not healed:
        #     player.lives = player.lives + 1
        #     healed = True
        # elif not (points % 10 == 0):
        #     healed = False

        ##################################
        #             render             #
        ##################################

        surf.fill(BACKGROUND_COLOUR)

        if player.recharge < 0:
            player.draw(surf, 'green')
        else:
            player.draw(surf, 'red')

        for entity in bullets:
            entity.draw(surf)

        for entity in enemies:
            entity.draw(surf)

        img = pygame.image.load("shooter_code/images/sword2.png")
        img = pygame.transform.scale(img, (img.get_width()*4, img.get_height()*4))
        rect = img.get_rect()
        rect.center = (30, 65)
        surf.blit(img, rect)
        build_word(str(points), surf, 60, 65, 6, 1, 'e')

        animation(surf, animate)

        if health(surf, points, player.lives):
            pass
        else:
            running = False

        pygame.display.update()

        fps.tick(FPS)

    return points


if __name__ == '__main__':
    shooter_game(1, True, 70)
