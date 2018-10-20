import game_framework
from pico2d import *

MOTION_TYPE = 0
MOTION_FRAME = 1

MOTION_STOP = (4, 2)
MOTION_MOVE = (3, 6)
MOTION_JUMP = (2, 4)
MOTION_DROP = (1, 4)
MOTION_DIED = (0, 9)

DIRECTION_LEFT = 0
DIRECTION_RIGHT = 1


class Dragon:
    def __init__(self):
        self.x, self.y = 3.5, 1
        self.motionState = MOTION_STOP
        self.isAttack = False
        self.direction = DIRECTION_RIGHT
        self.frameCycle = 0
        self.frame = 0
        self.speed = 0.02
        self.image = load_image('resources\sprites\Characters\Dragon.png')

    def update(self):
        self.frameCycle = (self.frameCycle + 1) % 50
        if 0 == self.frameCycle:
            self.frame = (self.frame + 1) % self.motionState[MOTION_FRAME]
        if MOTION_MOVE == self.motionState:
            if DIRECTION_LEFT == self.direction:
                self.x = self.x - self.speed
            elif DIRECTION_RIGHT == self.direction:
                self.x = self.x + self.speed
        elif MOTION_JUMP == self.motionState:
            self.y = self.y + self.speed
            if MOTION_JUMP[MOTION_FRAME] - 1 == self.frame and 50 - 1 == self.frameCycle:
                self.drop()
        elif MOTION_DROP == self.motionState:
            self.y = self.y - self.speed
            if MOTION_DROP[MOTION_FRAME] - 1 == self.frame and 50 - 1 == self.frameCycle:
                self.stop()

    def draw(self):
        if DIRECTION_LEFT == self.direction:
            flip = 'h'
        else:
            flip = ''
        self.image.clip_composite_draw(self.frame * 25, self.motionState[MOTION_TYPE] * 25, 25, 25, 0, flip,
                                       self.x * 8 * game_framework.windowScale,
                                       (self.y * 8 + 12.5) * game_framework.windowScale,
                                       25 * game_framework.windowScale,
                                       25 * game_framework.windowScale)

    def move_left(self):
        if MOTION_JUMP != self.motionState or MOTION_DROP != self.motionState:
            self.motionState = MOTION_MOVE
            self.direction = DIRECTION_LEFT

    def move_right(self):
        if MOTION_JUMP != self.motionState or MOTION_DROP != self.motionState:
            self.motionState = MOTION_MOVE
            self.direction = DIRECTION_RIGHT

    def jump(self):
        if MOTION_JUMP != self.motionState or MOTION_DROP != self.motionState:
            self.motionState = MOTION_JUMP
            self.frame = 0

    def drop(self):
        self.motionState = MOTION_DROP
        self.frame = 0

    def attack(self):
        pass

    def stop(self):
        self.motionState = MOTION_STOP
        self.frame = 0
