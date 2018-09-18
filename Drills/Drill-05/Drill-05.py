from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('character.png')

 # fill here

def draw(x, y):
    clear_canvas()
    grass.draw(400, 30)
    character.draw(x, y)
    update_canvas()
    delay(0.01)
    pass

def move(x1, y1, x2, y2):
    pass

def idle():
    pass

while True:
    idle()

close_canvas()

