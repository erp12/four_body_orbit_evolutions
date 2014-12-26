__author__ = 'Eddie Pantridge'

import math
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
    STABLE_COLOR = (20, 80, 80)
    pg.draw.rect(screen ,BG_COLOR, Rect(0, 0, 600, 600))
    pg.display.flip()

    clock = pg.time.Clock()
    myfont = pg.font.SysFont("monospace", 15)

    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    trails = pg.sprite.Group()

    frame_count = 0
    for s in states:
        for event in pg.event.get():
            if event.type == QUIT:
                exit()

        pg.draw.rect(screen, BG_COLOR, Rect(0, 0, 600, 600))
        trails.draw(screen)
        positions = u.pair_list(s[:len(s)/2])

        count = 0
        for pos in positions:
            pos = u.position_mult_scalars(pos, [100])
            if math.isnan(pos[0]):
                pos[0] = 0
            if math.isnan(pos[1]):
                pos[1] = 0
            try:
                draw_pos = [int(pos[0]+300), int(pos[1]+300)]
                pg.draw.circle(screen, (255, 255, 255), draw_pos, abs(int(10*masses[count])))
                trails.add(Trail_Point(colors[count], draw_pos[0], draw_pos[1]))
            except OverflowError:
                print "Could not draw frame. OverflowError!"
            count += 1

        label = myfont.render(str(frame_count), 1, (255, 255, 0))
        screen.blit(label, (300, 300))

        pg.display.flip()
        frame_count += 1
        #clock.tick(120)