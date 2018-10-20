import game_framework
from pico2d import *
import title_state
import pause_state_advanced

windowScale = game_framework.windowScale

name = "MainState"

dragon = None
stage = None
font = None


class Stage:
    def __init__(self):
        self.image = load_image('resources\sprites\Rounds\Round A-1.png')

    def draw(self):
        self.image.clip_draw(320 * 3, 208 * 6, 352, 224, 320 * game_framework.windowScale // 2, 240 * game_framework.windowScale // 2, 320 * game_framework.windowScale, 240 * game_framework.windowScale)
        self.image.clip_draw(320 * 0, 208 * 6, 320, 208, 320 * game_framework.windowScale // 2, 240 * game_framework.windowScale // 2, 320 * game_framework.windowScale, 240 * game_framework.windowScale)
        self.image.clip_draw(320 * 0, 208 * 5, 320, 208, 320 * game_framework.windowScale // 2, 208 * game_framework.windowScale // 2, 320 * game_framework.windowScale, 208 * game_framework.windowScale)


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
        self.x, self.y = 100, 90
        self.motionState = MOTION_STOP
        self.isAttack = False
        self.direction = DIRECTION_RIGHT
        self.frameCycle = 0
        self.frame = 0
        self.image = load_image('resources\sprites\Characters\Dragon.png')

    def update(self):
        self.frameCycle = (self.frameCycle + 1) % 50
        if 0 == self.frameCycle:
            self.frame = (self.frame + 1) % self.motionState[MOTION_FRAME]
        if MOTION_MOVE == self.motionState:
            if DIRECTION_LEFT == self.direction:
                self.x = self.x - 1
            elif DIRECTION_RIGHT == self.direction:
                self.x = self.x + 1
        elif MOTION_JUMP == self.motionState:
            self.y = self.y + 1
            if MOTION_JUMP[MOTION_FRAME] - 1 == self.frame and 50 - 1 == self.frameCycle:
                self.drop()
        elif MOTION_DROP == self.motionState:
            self.y = self.y - 1
            if MOTION_DROP[MOTION_FRAME] - 1 == self.frame and 50 - 1 == self.frameCycle:
                self.stop()

    def draw(self):
        self.image.clip_draw(self.frame * 25, self.motionState[MOTION_TYPE] * 25, 25, 25, self.x, self.y, 25 * game_framework.windowScale, 25 * game_framework.windowScale)

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


def enter():
    global dragon, stage
    dragon = Dragon()
    stage = Stage()


def exit():
    global dragon, stage
    del dragon
    del stage


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.change_state(title_state)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
            game_framework.push_state(pause_state_advanced)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            dragon.move_left()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            dragon.move_right()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
            dragon.attack()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_s):
            dragon.jump()
        elif event.type == SDL_KEYUP and (event.key == SDLK_LEFT or event.key == SDLK_RIGHT):
            dragon.stop()


def update():
    dragon.update()


def draw():
    clear_canvas()
    stage.draw()
    dragon.draw()
    if game_framework.stack[-1].name == name:
        update_canvas()
