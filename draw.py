__author__ = 'Eddie Pantridge'

import pygame as pg
from pygame.locals import *
import util as u

class Trail_Point(pg.sprite.Sprite):
    def __init__(self, c, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([1, 1])
        self.image.fill(c)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def init_draw(states, masses=[1, 1, 1, 1]):
    pg.init()
    screen=pg.display.set_mode((600, 600))
    caption=pg.display.set_caption("Evovling Orbits")

    BG_COLOR = (20, 20, 20)
    pg.draw.rect(screen ,BG_COLOR, Rect(0, 0, 600, 600))
    pg.display.flip()

    clock = pg.time.Clock()

    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    trails = pg.sprite.Group()

    for s in states:
        for event in pg.event.get():
            if event.type == QUIT:
                exit()

        pg.draw.rect(screen, BG_COLOR, Rect(0, 0, 600, 600))
        trails.draw(screen)
        positions = u.pair_list(s[:len(s)/2])

        count = 0
        for pos in positions:
            pos = u.position_mult_scalars(pos, [250])
            draw_pos = [int(pos[0]+300), int(pos[1]+300)]
            pg.draw.circle(screen, (255, 255, 255), draw_pos, 10*masses[count])
            trails.add(Trail_Point(colors[count], draw_pos[0], draw_pos[1]))
            count += 1

        pg.display.flip()
        clock.tick(60)