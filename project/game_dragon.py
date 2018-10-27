import game_framework
from pico2d import *

import main_state

MOTION_TYPE = 0
MOTION_FRAME = 1

MOTION_STOP = (4, 2, 0)
MOTION_MOVE = (3, 6)

MOTION_JUMP = (2, 4)
MOTION_DROP = (1, 4)

MOTION_DIED = (0, 9)

DIRECTION_LEFT = -1
DIRECTION_RIGHT = 1


class Dragon:
    def __init__(self):
        self.x, self.y = 3.5, 1
        self.moveMotion = MOTION_STOP
        self.direction = DIRECTION_RIGHT
        self.jumpMotion = None
        self.attackMotion = False

        self.jumping = 0.0

        self.frameCycle = 0
        self.frame = 0
        self.speed = 0.04
        self.image = load_image('resources\sprites\Characters\Dragon.png')

    def update(self):
        self.frameCycle = (self.frameCycle + 1) % 50
        if 0 == self.frameCycle:
            if self.jumpMotion is None:
                self.frame = (self.frame + 1) % self.moveMotion[MOTION_FRAME]
            else:
                self.frame = (self.frame + 1) % self.jumpMotion[MOTION_FRAME]

        if self.moveMotion == MOTION_MOVE:
            if self.direction == DIRECTION_LEFT and not main_state.stage.map[int(self.y)][int(self.x)]\
                    and not main_state.stage.map[int(self.y)][int(self.x - 1.5)]:
                self.x = self.x - self.speed
            elif self.direction == DIRECTION_RIGHT and not main_state.stage.map[int(self.y)][int(self.x)]\
                    and not main_state.stage.map[int(self.y)][int(self.x + 1.5)]:
                self.x = self.x + self.speed
        if self.jumpMotion == MOTION_JUMP:
            self.y = self.y + self.speed
            self.jumping += self.speed
            if self.jumping > 5.5:
                self.drop()
        elif self.jumpMotion == MOTION_DROP:
            self.y = self.y - self.speed
            if main_state.stage.map[int(self.y)][int(self.x)]:
                self.y = int(self.y+1)
                self.jumpMotion = None
                self.stop()
        elif not main_state.stage.map[int(self.y - 1)][int(self.x)]:
            self.drop()

    def draw(self):
        if self.direction == DIRECTION_LEFT:
            flip = 'h'
        else:
            flip = ''

        if self.jumpMotion is None:
            motion_type = self.moveMotion[MOTION_TYPE]
        else:
            motion_type = self.jumpMotion[MOTION_TYPE]
        self.image.clip_composite_draw(self.frame * 25, motion_type * 25, 25, 25, 0, flip,
                                       self.x * 8 * game_framework.windowScale,
                                       (self.y * 8 + 14.5) * game_framework.windowScale,
                                       25 * game_framework.windowScale,
                                       25 * game_framework.windowScale)

    def move_left(self):
        self.moveMotion = MOTION_MOVE
        self.direction = DIRECTION_LEFT

    def move_right(self):
        self.moveMotion = MOTION_MOVE
        self.direction = DIRECTION_RIGHT

    def jump(self):
        if self.jumpMotion is None:
            self.jumping = 0.0
            self.jumpMotion = MOTION_JUMP
            self.frame = 0

    def drop(self):
        self.jumpMotion = MOTION_DROP
        self.frame = 0

    def attack(self):
        pass

    def stop(self):
        self.moveMotion = MOTION_STOP
        self.frame = 0
