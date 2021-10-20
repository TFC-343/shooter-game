import sqlite3
import sys

import pygame.image
from pygame.locals import (
    KEYDOWN,
    QUIT,
    K_ESCAPE,
    K_RETURN,
    K_UP,
    K_RIGHT,
    K_DOWN,
    K_LEFT,
    MOUSEBUTTONDOWN,
    USEREVENT,
)

from shooter_code.data import *


class ShopSelector:
    def __init__(self, pos, command, direction,  first_image, second_image, surface):
        self.x, self.y = pos
        self.command = command
        self.direction = direction
        self.first_image = first_image
        self.second_image = second_image
        self.surface = surface

        self.selected = False

    def draw(self):
        image_use = self.first_image if not self.selected else self.second_image
        img = pygame.image.load(image_use[0])
        img = pygame.transform.scale(img, (img.get_width()*image_use[1], img.get_height()*image_use[1]))
        rect = img.get_rect()
        rect.center = (self.x, self.y)
        self.surface.blit(img, rect)

    def execute(self):
        self.command()


def get_money():
    file = sql.connect("shooter_code/data/data.db")
    cs = file.cursor()
    cs.execute("SELECT tokens FROM user")
    tokens = cs.fetchall()[0][0]
    file.close()
    return tokens


def draw_shop(surface, box_dict, selected, *boxes):
    for i in list(boxes):
        i.selected = False
    box_dict[selected].selected = True

    for i in boxes:
        i.draw()


def fill_shop_h(surface, pos, image, name, current, next_, price, size):
    x, y = pos

    # img = pygame.image.load(image)
    img = pygame.transform.scale(image, (144*size, 144*size))
    rect = img.get_rect()
    rect.center = (x-(98*size), y-(1*size))
    surface.blit(img, rect)

    pygame.draw.rect(surface, GREEN, (x-(170*size), y-(73*size), 144*size, 144*size), 2)

    build_word(name, surface, x-(3*size), y-(61*size), Multiplier(2.7*size), 1, anchor="left")

    build_word(f"current: {current}", surface, x-(3*size), y-(23*size), Multiplier(2.7*size), 1, anchor="left")
    build_word(f"next: {next_}", surface, x-(3*size), y+(15*size), Multiplier(2.7*size), 1, anchor="left")

    total_length = build_word(f"cost: {price}", surface, x-(3*size), y+(53*size), Multiplier(2.7*size), 1, anchor="left")

    img = pygame.image.load("shooter_code/images/sword2.png")
    img = pygame.transform.scale(img, (img.get_width()*Multiplier(3*size), img.get_height()*Multiplier(3*size)))
    rect = img.get_rect()
    rect.center = (x+(20*size) + total_length, y+(53*size))
    surface.blit(img, rect)


def fill_shop_v(surface, pos, image, name, current, next_, price, size):
    x, y = pos  # 125, 167
    # print(x, y)

    # img = pygame.image.load(image)
    img = pygame.transform.scale(image, (84*size, 84*size))
    rect = img.get_rect()
    rect.center = (x, y-(48*size))
    surface.blit(img, rect)

    pygame.draw.rect(surface, GREEN, (x-(size*42), y-(size*88), 84*size, 84*size), 2)

    text_size = 1.76
    build_word(name, surface, x, y+(size*13), Multiplier(text_size*size), 1)

    build_word(f"current: {current}", surface, x, y+(size*36), Multiplier(text_size*size), 1)
    build_word(f"next: {next_}", surface, x, y+(size*60), Multiplier(text_size*size), 1)

    total_length = build_word(f"cost: {price}", surface, x, y+(size*83), Multiplier(text_size*size), 1)

    img = pygame.image.load("shooter_code/images/sword2.png")
    img = pygame.transform.scale(img, (img.get_width()*Multiplier(text_size*size), img.get_height()*Multiplier(text_size*size)))
    rect = img.get_rect()
    rect.center = (x+(size*15) + int(total_length/2), y+(size*83))
    surface.blit(img, rect)


def update_shop(box_dict, selected, direction):
    direction = {'n': 0, 'e': 1, 's': 2, 'w': 3}[direction]
    if box_dict[selected].direction[direction] is not None:
        selected = box_dict[selected].direction[direction]

    return selected


def upgrade_player(surf):

    def buy_health(money, next_, cost):
        if cost <= money:
            file_ = sql.connect("shooter_code/data/data.db")
            cs_ = file_.cursor()
            cs_.execute(f"UPDATE user SET start_health = {next_}")
            cs_.execute(f"UPDATE user SET tokens = {money-cost}")
            file_.commit()
            file_.close()

    def get_health():
        file = sql.connect("shooter_code/data/data.db")
        cs = file.cursor()
        cs.execute("SELECT start_health FROM user")
        current_health = cs.fetchall()[0][0]
        file.close()
        return current_health

    b1 = ShopSelector((300, 400), do_nothing, ('back', None, None, None),
                      ('shooter_code/images/frames/0-2-w.png', 9), ('shooter_code/images/frames/0-2-g.png', 9),
                      surf)

    back = ShopSelector((100, 67), do_nothing, (None, None, 'b1', None),
                        ("shooter_code/images/frames/back2.png", 4), ("shooter_code/images/frames/back.png", 4),
                        surf)

    box_dict = {'b1': b1, 'back': back}

    selected = 'b1'

    tokens = get_money()
    current_health = get_health()

    update_sql = USEREVENT + 1
    pygame.time.set_timer(update_sql, 1000)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_RETURN:
                    if selected == 'back':
                        running = False
                    if selected == 'b1':
                        buy_health(tokens, current_health + 1, 40*current_health**2)
                if event.key == K_UP:
                    selected = update_shop(box_dict, selected, 'n')
                if event.key == K_RIGHT:
                    selected = update_shop(box_dict, selected, 'e')
                if event.key == K_DOWN:
                    selected = update_shop(box_dict, selected, 's')
                if event.key == K_LEFT:
                    selected = update_shop(box_dict, selected, 'w')
            if event.type == MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
            if event.type == update_sql:
                tokens = get_money()
                current_health = get_health()

        surf.fill(BACKGROUND_COLOUR)

        draw_shop(surf, box_dict, selected, b1, back)

        build_word("back", surf, 100, 67, 3, 1)

        s1 = pygame.Surface((100, 100))
        i = pygame.image.load("shooter_code/images/heart2.png")
        i = pygame.transform.scale(i, (i.get_width()*6, i.get_height()*6))
        r = i.get_rect()
        r.center = (50, 50)
        s1.blit(i, r)

        fill_shop_h(surf, (300, 400), s1, "player health",
                    current_health, current_health + 1, 40 * current_health ** 2, 1)

        build_word(str(tokens), surf, 510, 67, Multiplier(4.8), 1, anchor="w")
        img = pygame.image.load("shooter_code/images/sword2.png")
        img = pygame.transform.scale(img, (img.get_width()*Multiplier(4.2), img.get_height()*Multiplier(4.2)))
        rect = img.get_rect()
        rect.center = (515 + (img.get_width()/2), 67)
        surf.blit(img, rect)

        pygame.display.update()


def upgrade_shooter(surf):

    def get_lasersights():
        return shooter_from_sql(get_shooter()).lasersights

    def buy_lasersights():
        if get_money() >= shooter_from_sql(get_shooter()).p_lasersights[0]:
            file = sql.connect("shooter_code/data/data.db")
            cs = file.cursor()
            cs.execute(f"UPDATE shooters SET lasersights = 1 WHERE shooter_id = '{shooter_from_sql(get_shooter()).shooter_id}'")
            cs.execute(f"UPDATE user SET tokens = {get_money()-shooter_from_sql(get_shooter()).p_lasersights[0]}")
            file.commit()
            file.close()

    def buy_recharge():
        if get_money() >= c_shooter.p_recharge_speed[c_shooter.u_recharge_speed]:
            file = sql.connect("shooter_code/data/data.db")
            cs = file.cursor()
            cs.execute(f"UPDATE shooters SET u_recharge_speed = {c_shooter.u_recharge_speed + 1} WHERE shooter_id = '{shooter_from_sql(get_shooter()).shooter_id}'")
            cs.execute(f"UPDATE user SET tokens = {get_money()-c_shooter.p_recharge_speed[c_shooter.u_recharge_speed]}")
            file.commit()
            file.close()

    def buy_pen():
        if get_money() >= c_shooter.p_penetration[c_shooter.u_penetration]:
            file = sql.connect("shooter_code/data/data.db")
            cs = file.cursor()
            cs.execute(f"UPDATE shooters SET u_penetration = {c_shooter.u_penetration + 1} WHERE shooter_id = '{shooter_from_sql(get_shooter()).shooter_id}'")
            cs.execute(f"UPDATE user SET tokens = {get_money()-c_shooter.p_penetration[c_shooter.u_penetration]}")
            file.commit()
            file.close()

    def buy_drop():
        if get_money() >= c_shooter.p_drop_off[c_shooter.u_drop_off]:
            file = sql.connect("shooter_code/data/data.db")
            cs = file.cursor()
            cs.execute(f"UPDATE shooters SET u_drop_off = {c_shooter.u_drop_off + 1} WHERE shooter_id = '{shooter_from_sql(get_shooter()).shooter_id}'")
            cs.execute(f"UPDATE user SET tokens = {get_money()-c_shooter.p_drop_off[c_shooter.u_drop_off]}")
            file.commit()
            file.close()

    s = pygame.Surface((500, 667))
    size = Multiplier(7.506)
    b1 = ShopSelector((125, 167), do_nothing, ('back', 'b2', 'b3', None),
                      ("shooter_code/images/frames/1-4-w.png", size), ("shooter_code/images/frames/1-4-g.png", size), s)
    b2 = ShopSelector((375, 167), do_nothing, ('back', None, 'b4', 'b1'),
                      ("shooter_code/images/frames/1-4-w.png", size), ("shooter_code/images/frames/1-4-g.png", size), s)
    b3 = ShopSelector((125, 500), do_nothing, ('b1', 'b4', None, None),
                      ("shooter_code/images/frames/1-4-w.png", size), ("shooter_code/images/frames/1-4-g.png", size), s)
    b4 = ShopSelector((375, 500), do_nothing, ('b2', None, None, 'b3'),
                  ("shooter_code/images/frames/1-4-w.png", size), ("shooter_code/images/frames/1-4-g.png", size), s)

    back = ShopSelector((100, 67), do_nothing, (None, None, 'b1', None),
                        ("shooter_code/images/frames/back2.png", 4), ("shooter_code/images/frames/back.png", 4),
                        surf)

    box_dict = {'b1': b1, 'b2': b2, 'b3': b3, 'b4': b4, 'back': back}

    selected = 'b1'

    update_sql = USEREVENT + 2
    pygame.time.set_timer(update_sql, 1000)

    c_shooter = shooter_from_sql(get_shooter())

    tokens = get_money()
    laser_stat = c_shooter.lasersights
    laser_price = c_shooter.p_lasersights[0]

    if c_shooter.u_recharge_speed >= len(c_shooter.recharge_speed)-1:
        recharge_stat = False
        recharge_current, recharge_next, recharge_price = [None]*3
    else:
        recharge_stat = True
        recharge_current = c_shooter.recharge_speed[c_shooter.u_recharge_speed]
        recharge_next = c_shooter.recharge_speed[c_shooter.u_recharge_speed+1]
        recharge_price = c_shooter.p_recharge_speed[c_shooter.u_recharge_speed]

    if c_shooter.u_penetration >= len(c_shooter.penetration)-1:
        pen_stat = False
        pen_current, pen_next, pen_price = [None]*3
    else:
        pen_stat = True
        pen_current = c_shooter.penetration[c_shooter.u_penetration]
        pen_next = c_shooter.penetration[c_shooter.u_penetration+1]
        pen_price = c_shooter.p_penetration[c_shooter.u_penetration]

    if c_shooter.u_drop_off >= len(c_shooter.drop_off)-1:
        drop_stat = False
        drop_current, drop_next, drop_price = [None]*3
    else:
        drop_stat = True
        drop_current = c_shooter.drop_off[c_shooter.u_drop_off]
        drop_next = c_shooter.drop_off[c_shooter.u_drop_off+1]
        drop_price = c_shooter.p_drop_off[c_shooter.u_drop_off]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_RETURN:
                    if selected == 'back':
                        running = False
                    if selected == 'b1' and not shooter_from_sql(get_shooter()).lasersights:
                        buy_lasersights()
                    if selected == 'b2' and not (c_shooter.u_recharge_speed >= len(c_shooter.recharge_speed) - 1):
                        buy_recharge()
                    if selected == 'b3' and not (c_shooter.u_penetration >= len(c_shooter.penetration) - 1):
                        buy_pen()
                    if selected == 'b4' and not (c_shooter.u_drop_off >= len(c_shooter.drop_off) - 1):
                        buy_drop()
                if event.key == K_UP:
                    selected = update_shop(box_dict, selected, 'n')
                if event.key == K_RIGHT:
                    selected = update_shop(box_dict, selected, 'e')
                if event.key == K_DOWN:
                    selected = update_shop(box_dict, selected, 's')
                if event.key == K_LEFT:
                    selected = update_shop(box_dict, selected, 'w')
            if event.type == update_sql:
                c_shooter = shooter_from_sql(get_shooter())

                tokens = get_money()

                laser_stat = c_shooter.lasersights
                laser_price = c_shooter.p_lasersights[0]

                if c_shooter.u_recharge_speed >= len(c_shooter.recharge_speed) - 1:
                    recharge_stat = False
                else:
                    recharge_stat = True
                    recharge_current = c_shooter.recharge_speed[c_shooter.u_recharge_speed]
                    recharge_next = c_shooter.recharge_speed[c_shooter.u_recharge_speed + 1]
                    recharge_price = c_shooter.p_recharge_speed[c_shooter.u_recharge_speed]

                if c_shooter.u_penetration >= len(c_shooter.penetration) - 1:
                    pen_stat = False
                else:
                    recharge_stat = True
                    pen_current = c_shooter.penetration[c_shooter.u_penetration]
                    pen_next = c_shooter.penetration[c_shooter.u_penetration + 1]
                    pen_price = c_shooter.p_penetration[c_shooter.u_penetration]

                if c_shooter.u_drop_off >= len(c_shooter.drop_off)-1:
                    drop_stat = False
                    drop_current, drop_next, drop_price = [None]*3
                else:
                    drop_stat = True
                    drop_current = c_shooter.drop_off[c_shooter.u_drop_off]
                    drop_next = c_shooter.drop_off[c_shooter.u_drop_off+1]
                    drop_price = c_shooter.p_drop_off[c_shooter.u_drop_off]

            if event.type == MOUSEBUTTONDOWN:
                pos_x, pos_y = pygame.mouse.get_pos()
                print(pos_x-50, pos_y-133)

        surf.fill(BACKGROUND_COLOUR)
        s.fill(BACKGROUND_COLOUR)

        draw_shop(s, box_dict, selected, b1, b2, b3, b4, back)

        # pygame.draw.line(surf, CYAN, (0, 133), (600, 133))
        # pygame.draw.line(surf, CYAN, (50, 0), (50, 800))
        # pygame.draw.line(surf, CYAN, (550, 0), (550, 800))

        # fill_shop_h(s, (362, 84), "shooter_code/images/shooter/shooter1.png", "bullet penetration", "50", "100", "2000", Multiplier(0.3))

        build_word("back", surf, 100, 67, 3, 1)

        if not laser_stat:
            s1 = pygame.Surface((100, 100))
            i = pygame.transform.scale(pygame.image.load("shooter_code/images/shooter/shooter1.png"), (50, 50))
            r = i.get_rect()
            r.center = (50, 60)
            pygame.draw.line(s1, CYAN, (50, 60), (50, 2))
            s1.blit(i, r)
            fill_shop_v(s, (125, 167), s1, "lasersights", "off", "on", laser_price, 1)
        else:
            build_word("sold out", s, 125, 167, Multiplier(3.7), 1)
        # fill_shop_v(s, (375, 167), "shooter_code/images/shooter/bullet1.png", "faster recharge", 5, 6, 1000, 1)
        # fill_shop_v(s, (125, 500), "shooter_code/images/shooter/bullet1.png", "faster recharge", 5, 6, 1000, 1)

        if recharge_stat:
            # print("here", recharge_current)
            s1 = pygame.Surface((100, 100))
            i = pygame.transform.scale(pygame.image.load("shooter_code/images/engine.png"), (34*Multiplier(2.6), 13*Multiplier(2.6)))
            r = i.get_rect()
            r.center = (50, 50)
            s1.blit(i, r)
            fill_shop_v(s, (375, 167), s1, "recharge rate", str(recharge_current), str(recharge_next), str(recharge_price), 1)
        else:
            build_word("sold out", s, 375, 167, Multiplier(3.7), 1)

        if pen_stat:
            s1 = pygame.Surface((100, 100))
            i = pygame.transform.scale(pygame.image.load("shooter_code/images/enemies/e2.png"), (50, 50))
            r = i.get_rect()
            r.center = (50, 60)
            s1.blit(i, r)
            i = pygame.transform.scale(pygame.image.load("shooter_code/images/shooter/bullet1.png"), (33, 33))
            r = i.get_rect()
            r.center = (50, 40)
            s1.blit(i, r)
            fill_shop_v(s, (125, 500), s1, "penetration", str(pen_current)+'%', str(pen_next)+'%', str(pen_price), 1)
        else:
            build_word("sold out", s, 125, 500, Multiplier(3.7), 1)

        if drop_stat:
            s1 = pygame.Surface((100, 100))
            i = pygame.transform.scale(pygame.image.load("shooter_code/images/shooter/bullet1.png"), (50, 50))
            r = i.get_rect()
            r.center = (50, 50)
            s1.blit(i, r)
            fill_shop_v(s, (375, 500), s1, "pen drop off", str(drop_current), str(drop_next), str(drop_price), 1)
        else:
            build_word("sold out", s, 375, 500, Multiplier(3.7), 1)

        surf.blit(s, (50, 133))

        build_word(str(tokens), surf, 510, 67, Multiplier(4.8), 1, anchor="w")
        img = pygame.image.load("shooter_code/images/sword2.png")
        img = pygame.transform.scale(img, (img.get_width()*Multiplier(4.2), img.get_height()*Multiplier(4.2)))
        rect = img.get_rect()
        rect.center = (515 + (img.get_width()/2), 67)
        surf.blit(img, rect)

        pygame.display.update()


def open_shop(surf):
    size = Multiplier(7.506)
    b1 = ShopSelector((50 + int(500/4), 133 + int(667/4)), do_nothing, ('b4', 'b2', 'b3', None),
                      ('shooter_code/images/frames/1-4-w.png', size), ('shooter_code/images/frames/1-4-g.png', size),
                      surf)
    b2 = ShopSelector((int(500/2) + 50 + int(500/4), 133 + int(667/4)), lambda: upgrade_shooter(surf), ('b4', None, 'b3', 'b1'),
                      ('shooter_code/images/frames/1-4-w.png', size), ('shooter_code/images/frames/1-4-g.png', size),
                      surf)
    b3 = ShopSelector((50 + int(500/2), int(667/2) + 133 + int(667/4)), lambda: upgrade_player(surf), ('b1', None, None, None),
                      ('shooter_code/images/frames/0-2-w.png', size), ('shooter_code/images/frames/0-2-g.png', size),
                      surf)
    b4 = ShopSelector((100, 67), do_nothing, (None, None, 'b1', None),
                      ("shooter_code/images/frames/back2.png", 4), ("shooter_code/images/frames/back.png", 4),
                      surf)

    box_dict = {'b1': b1, 'b2': b2, 'b3': b3, 'b4': b4}

    selected = 'b1'

    update_sql = USEREVENT + 5
    pygame.time.set_timer(update_sql, 1000)
    tokens = get_money()

    running = True
    while running:

        ##################################
        #             event              #
        ##################################

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == update_sql:
                tokens = get_money()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_RETURN:
                    if selected == 'b4':
                        running = False
                    else:
                        box_dict[selected].execute()
                if event.key == K_UP:
                    selected = update_shop(box_dict, selected, 'n')
                if event.key == K_RIGHT:
                    selected = update_shop(box_dict, selected, 'e')
                if event.key == K_DOWN:
                    selected = update_shop(box_dict, selected, 's')
                if event.key == K_LEFT:
                    selected = update_shop(box_dict, selected, 'w')

        ##################################
        #             update             #
        ##################################

        ##################################
        #             render             #
        ##################################

        surf.fill(BACKGROUND_COLOUR)

        # pygame.draw.line(surf, CYAN, (0, 133), (600, 133))
        # pygame.draw.line(surf, CYAN, (50, 0), (50, 800))
        # pygame.draw.line(surf, CYAN, (550, 0), (550, 800))

        draw_shop(surf, box_dict, selected, b1, b2, b3, b4)
        build_word("shooters", surf, 50 + int(500/4), 133 + int(667/4), 3, 1)

        build_word("shooter", surf, int(500/2) + 50 + int(500/4), 133 + int(667/4) - 20, 3, 1)
        build_word("upgrades", surf, int(500/2) + 50 + int(500/4), 133 + int(667/4) + 20, 3, 1)

        build_word("player", surf, 50 + int(500/2), int(667/2) + 133 + int(667/4) - 33, 5, 1)
        build_word("upgrades", surf, 50 + int(500/2), int(667/2) + 133 + int(667/4) + 33, 5, 1)

        build_word("back", surf, 100, 67, 3, 1)

        build_word(str(tokens), surf, 510, 67, Multiplier(4.8), 1, anchor="w")
        img = pygame.image.load("shooter_code/images/sword2.png")
        img = pygame.transform.scale(img, (img.get_width()*Multiplier(4.2), img.get_height()*Multiplier(4.2)))
        rect = img.get_rect()
        rect.center = (515 + (img.get_width()/2), 67)
        surf.blit(img, rect)

        pygame.display.update()


if __name__ == '__main__':
    open_shop()
