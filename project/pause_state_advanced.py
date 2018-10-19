import game_framework
from pico2d import *
import main_state

import main_state

name = "PauseState"
image = None
time = None

def enter():
    global image, time
    image = load_image('pause.png')
    time = 0

def exit():
    global image
    del(image)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
                game_framework.pop_state()

def draw():
    global time
    clear_canvas()
    main_state.draw()
    time = (time + 1) % 300
    if time < 150:
        image.draw(400, 300, 400, 400)
    elif time > 300:
        time = 0
    update_canvas()

def update():
    pass

def pause():
    pass

def resume():
    pass

