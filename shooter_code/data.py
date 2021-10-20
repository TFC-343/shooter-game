from dataclasses import dataclass
import sqlite3 as sql
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    KEYDOWN,
)


@dataclass
class Multiplier:
    factor: float

    def __mul__(self, other):
        return round(self.factor * other)

    def __rmul__(self, other):
        return round(self.factor * other)


class Selector(pygame.sprite.Sprite):
    def __init__(self, top, size, *options):
        super(Selector, self).__init__()

        img = pygame.image.load("shooter_code/images/shooter/shooter90.png")
        img = pygame.transform.scale(img, (40, 40))
        img.set_colorkey(BLACK)
        self.image = img

        self.top = top

        self.size = Multiplier(size)
        self.gap = size * Multiplier(14.423)

        options = list(options)
        for i in range(len(options)):
            options[i] = [options[i][0], top + (self.gap * i), options[i][1]]

        self.options = options

        self.current_item = 0

    def draw(self, surface):
        rect = self.image.get_rect()
        rect.center = (100, self.options[self.current_item][1])
        surface.blit(self.image, rect)
        for i in self.options:
            build_word(i[0], surface, 180, i[1], self.size, 1, 'e')

    def move_up(self):
        if self.options[self.current_item] == self.options[0]:
            pass
        else:
            self.current_item -= 1

    def move_down(self):
        if self.options[self.current_item] == self.options[-1]:
            pass
        else:
            self.current_item += 1

    def execute(self, surface):
        self.options[self.current_item][2](surface)


class letter:
    def __init__(self, name, img, width=5, height=6, above=0, below=0):
        self.name = name
        self.height = height
        self.above = above
        self.width = width
        self.below = below
        self.img = img

    def size(self):
        print(self.height-(self.above + self.below))


@dataclass
class ShooterDatabase:
    shooter_id: str
    name: str
    speed: int
    lasersights: bool
    recharge_speed: list
    u_recharge_speed: int
    penetration: list
    u_penetration: int
    drop_off: list
    u_drop_off: int
    p_lasersights: list
    p_recharge_speed: list
    p_penetration: list
    p_drop_off: list
    owned: bool

    def __str__(self):
        return f"{self.name}"


def build_word(word, surface, x, y, size, gap, anchor='centre'):
    x_, y_ = x, y
    # pygame.draw.line(surface, CYAN, (0, 100), (600, 100))

    total_length = size * gap * (len(word) - 1)
    build = []

    for i in range(len(word)):
        c_letter = letter_dict[word[i]]
        img = c_letter.img
        img = pygame.transform.scale(img, (img.get_width()*size, img.get_height()*size))
        rect = img.get_rect()
        rect.center = (x_ + (rect.width / 2), y_)
        total_length += img.get_width()

        rect.move_ip(0, -c_letter.above * size / 2)
        rect.move_ip(0, c_letter.below * size / 2)

        build.append([img, rect])
        x_ = (x_ + c_letter.width * size) + (gap * size)

    for i in build:
        if anchor == 'w':
            i[1].center = (i[1].center[0] - total_length, i[1].center[1])
        if anchor == 'centre':
            i[1].center = (i[1].center[0] - (total_length / 2), i[1].center[1])
        else:
            pass
        surface.blit(*i)

    return total_length


def do_nothing(*_):
    pass


def get_shooter():
    file = sql.connect("shooter_code/data/data.db")
    cs = file.cursor()
    cs.execute(f"SELECT current_shooter FROM user")
    s = cs.fetchall()[0][0]
    file.close()
    return s


def shooter_from_sql(shooter_id):
    file = sql.connect("shooter_code/data/data.db")
    cs = file.cursor()
    cs.execute(f"SELECT * FROM shooters WHERE shooter_id == '{shooter_id}'")
    fetch = cs.fetchall()[0]
    cs.close()

    return ShooterDatabase(fetch[0], fetch[1], fetch[2], fetch[3],
                           [int(i) for i in fetch[4][1:].split('|')],
                           fetch[5],
                           [int(i) for i in fetch[6][1:].split('|')],
                           fetch[7],
                           [int(i) for i in fetch[8][1:].split('|')],
                           fetch[9],
                           [int(i) for i in fetch[10][1:].split('|')],
                           [int(i) for i in fetch[11][1:].split('|')],
                           [int(i) for i in fetch[12][1:].split('|')],
                           [int(i) for i in fetch[13][1:].split('|')],
                           fetch[14])


def get_settings():
    file = open("shooter_code/data/settings")
    read = file.read()
    file.close()
    settings = {}
    for i in repr(read)[1:-1].split("\\n"):
        t = i.split(":")
        settings[t[0]] = t[1]
    return settings


# letters
path = "shooter_code/images/text/letters/"
chr_a = letter('a', pygame.image.load(path+'a.png'), 5, 6)
chr_b = letter('b', pygame.image.load(path+'b.png'), 5, 9, 3)
chr_c = letter('c', pygame.image.load(path+'c.png'))
chr_d = letter('d', pygame.image.load(path+'d.png'), 5, 9, 3)
chr_e = letter('e', pygame.image.load(path+'e.png'))
chr_f = letter('f', pygame.image.load(path+'f.png'), 3, 9, 3)
chr_g = letter('g', pygame.image.load(path+'g.png'), 5, 8, 0, 2)
chr_h = letter('h', pygame.image.load(path+'h.png'), 5, 9, 3)
chr_i = letter('i', pygame.image.load(path+'i.png'), 1, 8, 2)
chr_j = letter('j', pygame.image.load(path+'j.png'), 2, 10, 2, 2)
chr_k = letter('k', pygame.image.load(path+'k.png'), 5, 9, 3)
chr_l = letter('l', pygame.image.load(path+'l.png'), 1, 9, 3)
chr_m = letter('m', pygame.image.load(path+'m.png'), 7, 6)
chr_n = letter('n', pygame.image.load(path+'n.png'))
chr_o = letter('o', pygame.image.load(path+'o.png'))
chr_p = letter('p', pygame.image.load(path+'p.png'), 5, 9, 0, 3)
chr_q = letter('q', pygame.image.load(path+'q.png'), 5, 9, 0, 3)
chr_r = letter('r', pygame.image.load(path+'r.png'), 3, 6)
chr_s = letter('s', pygame.image.load(path+'s.png'), 4, 6)
chr_t = letter('t', pygame.image.load(path+'t.png'), 3, 9, 3)
chr_u = letter('u', pygame.image.load(path+'u.png'))
chr_v = letter('v', pygame.image.load(path+'v.png'))
chr_w = letter('w', pygame.image.load(path+'w.png'), 7, 6)
chr_x = letter('x', pygame.image.load(path+'x.png'))
chr_y = letter('y', pygame.image.load(path+'y.png'), 5, 8, 0, 2)
chr_z = letter('z', pygame.image.load(path+'z.png'), 4, 6,)
chr_space = letter(' ', pygame.image.load(path+"SPACE.png"))
chr_zero = letter('0', pygame.image.load(path+'0.png'), 4, 7, 1)
chr_one = letter('1', pygame.image.load(path+'1.png'), 3, 7, 1)
chr_two = letter('2', pygame.image.load(path+'2.png'), 4, 7, 1)
chr_three = letter('3', pygame.image.load(path+'3.png'), 4, 7, 1)
chr_four = letter('4', pygame.image.load(path+'4.png'), 5, 7, 1)
chr_five = letter('5', pygame.image.load(path+'5.png'), 4, 7, 1)
chr_six = letter('6', pygame.image.load(path+'6.png'), 4, 7, 1)
chr_seven = letter('7', pygame.image.load(path+'7.png'), 4, 7, 1)
chr_eight = letter('8', pygame.image.load(path+'8.png'), 4, 7, 1)
chr_nine = letter('9', pygame.image.load(path+'9.png'), 4, 7, 1)
chr_colon = letter(':', pygame.image.load(path+'colon.png'), 1)
chr_percent = letter('%', pygame.image.load(path+'percent.png'))

letter_dict = {
    'a': chr_a,
    'b': chr_b,
    'c': chr_c,
    'd': chr_d,
    'e': chr_e,
    'f': chr_f,
    'g': chr_g,
    'h': chr_h,
    'i': chr_i,
    'j': chr_j,
    'k': chr_k,
    'l': chr_l,
    'm': chr_m,
    'n': chr_n,
    'o': chr_o,
    'p': chr_p,
    'q': chr_q,
    'r': chr_r,
    's': chr_s,
    't': chr_t,
    'u': chr_u,
    'v': chr_v,
    'w': chr_w,
    'x': chr_x,
    'y': chr_y,
    'z': chr_z,
    ' ': chr_space,
    '0': chr_zero,
    '1': chr_one,
    '2': chr_two,
    '3': chr_three,
    '4': chr_four,
    '5': chr_five,
    '6': chr_six,
    '7': chr_seven,
    '8': chr_eight,
    '9': chr_nine,
    ':': chr_colon,
    '%': chr_percent,
}


# screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800


# colours
BLACK = pygame.Color(0, 0, 0)

RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)

YELLOW = pygame.Color(255, 255, 0)
MAGENTA = pygame.Color(255, 0, 255)
CYAN = pygame.Color(0, 255, 255)

WHITE = pygame.Color(255, 255, 255)


BACKGROUND_COLOUR = BLACK


# fps
FPS = 60


if __name__ == '__main__':
    print(get_upgrades(shooter_dict))
