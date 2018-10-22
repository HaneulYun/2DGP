import game_framework
from pico2d import *
import title_state
import pause_state_advanced

import game_stage
import game_dragon

windowScale = game_framework.windowScale

name = "MainState"

dragon = None
stage = None
font = None


def enter():
    global dragon, stage
    dragon = game_dragon.Dragon()
    stage = game_stage.Stage('resources\sprites\Rounds\Round A-1.png')
    stage.load('resources\data\Round A-1 data.txt')


def exit():
    global dragon, stage
    del dragon
    del stage


def pause():
    pass


def resume():
    pass


def handle_events():
    global stage
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.change_state(title_state)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
            game_framework.push_state(pause_state_advanced)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_o):
            stage.section = (stage.section - 1) % 6
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            dragon.move_left()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            dragon.move_right()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
            dragon.attack()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_s):
            dragon.jump()
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT) and dragon.moveMotion == game_dragon.MOTION_MOVE and dragon.direction == game_dragon.DIRECTION_LEFT:
            dragon.stop()
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT) and dragon.moveMotion == game_dragon.MOTION_MOVE and dragon.direction == game_dragon.DIRECTION_RIGHT:
            dragon.stop()


def update():
    dragon.update()


def draw():
    clear_canvas()
    stage.draw()
    dragon.draw()
    if game_framework.stack[-1].name == name:
        update_canvas()
