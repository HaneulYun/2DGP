from pico2d import *
import game_framework
import game_world

import title_state
import pause_state_advanced

from game_stage import *
from game_dragon import *

windowScale = game_framework.windowScale

name = "MainState"

dragon = None
stage = None
font = None


def enter():
    global dragon, stage
    dragon = Dragon()
    stage = Stage('resources\sprites\Rounds\Round A-1.png')
    stage.load('resources\data\Round A-1 data.txt')
    game_world.add_object(stage, 0)
    game_world.add_object(dragon, 1)


def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    #global stage
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
        else:
            dragon.handle_event(event)
    #    elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
    #        dragon.move_left()
    #    elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
    #        dragon.move_right()
    #    elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
    #        dragon.attack()
    #    elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_s):
    #        dragon.jump()
    #    elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT) and dragon.moveMotion == MOTION_MOVE and dragon.direction == DIRECTION_LEFT:
    #        dragon.stop()
    #    elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT) and dragon.moveMotion == MOTION_MOVE and dragon.direction == DIRECTION_RIGHT:
    #        dragon.stop()


def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    if game_framework.stack[-1].name == name:
        update_canvas()
