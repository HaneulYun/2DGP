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
        self.image = load_image('resources\sprites\Rounds\Misc Backgrounds.png')

    def draw(self):
        self.image.clip_draw(5, 2768 - 223, 320, 208, 320 * game_framework.windowScale // 2, 208 * game_framework.windowScale // 2, 320 * game_framework.windowScale, 208 * game_framework.windowScale)


MOTION_STOP = 4
MOTION_MOVE = 3
MOTION_JUMP = 2
MOTION_DROP = 1
MOTION_DIED = 0

DIRECTION_LEFT = 0
DIRECTION_RIGHT = 1


class Dragon:
    def __init__(self):
        self.x, self.y = 100, 90
        self.motionState = MOTION_STOP
        self.isAttack = False
        self.dir = DIRECTION_RIGHT
        self.frameCycle = 0
        self.frame = 0
        self.image = load_image('resources\sprites\Characters\Dragon.png')

    def update(self):
        self.frameCycle = (self.frameCycle + 1) % 100
        if 0 == self.frameCycle:
            self.frame = (self.frame + 1) % 2
        # self.x += self.dir
        if self.x >= 800:
            self.dir = -1
        elif self.x <= 0:
            self.dir = 1

    def draw(self):
        self.image.clip_draw(self.frame * 25, self.motionState * 25, 25, 25, self.x, self.y, 25 * game_framework.windowScale, 25 * game_framework.windowScale)

    def move_left(self):
        pass

    def move_right(self):
        pass

    def jump(self):
        pass

    def attack(self):
        pass


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


def update():
    dragon.update()


def draw():
    clear_canvas()
    stage.draw()
    dragon.draw()
    if game_framework.stack[-1].name == name:
        update_canvas()
