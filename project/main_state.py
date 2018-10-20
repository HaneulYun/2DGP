import game_framework
from pico2d import *
import title_state
import pause_state_advanced

windowScale = game_framework.windowScale

name = "MainState"

boy = None
stage = None
font = None


class Stage:
    def __init__(self):
        self.image = load_image('resources\sprites\Rounds\Misc Backgrounds.png')

    def draw(self):
        self.image.clip_draw(5, 2768 - 223, 320, 208, 320 * game_framework.windowScale // 2, 208 * game_framework.windowScale // 2, 320 * game_framework.windowScale, 208 * game_framework.windowScale)


class Boy:
    def __init__(self):
        self.x, self.y = 0, 90
        self.frame = 0
        self.image = load_image('run_animation.png')
        self.dir = 1

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += self.dir
        if self.x >= 800:
            self.dir = -1
        elif self.x <= 0:
            self.dir = 1

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)


def enter():
    global boy, stage
    boy = Boy()
    stage = Stage()


def exit():
    global boy, stage
    del boy
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
    boy.update()


def draw():
    clear_canvas()
    stage.draw()
    boy.draw()
    if game_framework.stack[-1].name == name:
        update_canvas()
