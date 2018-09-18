from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('character.png')

# fill here
def move_from_center_to_right():
    x, y = 800 // 2, 90
    while x < 800 - 25:
        clear_canvas_now()
        grass.draw_now(400, 30)
        character.draw_now(x, y)
        x += 2
        delay(0.01)

def move_up():
    x, y = 800 - 25, 90
    while y < 600 - 50:
        clear_canvas_now()
        grass.draw_now(400, 30)
        character.draw_now(x, y)
        y += 2
        delay(0.01)

def move_left():
    x, y = 800 - 25, 550
    while x > 25:
        clear_canvas_now()
        grass.draw_now(400, 30)
        character.draw_now(x, y)
        x -= 2
        delay(0.01)

def move_down():
    x, y = 25, 550
    while y > 90:
        clear_canvas_now()
        grass.draw_now(400, 30)
        character.draw_now(x, y)
        y -= 2
        delay(0.01)

def move_from_left_to_center():
    x, y = 25, 90
    while x < 800 // 2:
        clear_canvas_now()
        grass.draw_now(400, 30)
        character.draw_now(x, y)
        x += 2
        delay(0.01)

def make_rectangle():
    move_from_center_to_right()
    move_up()
    move_left()
    move_down()
    move_from_left_to_center()

def make_circle():
    cx, cy, r = 800 // 2, 600 // 2, (600-180) // 2
    degree = -90
    while degree < 270:
        clear_canvas_now()
        grass.draw_now(400, 30)
        character.draw_now(cx, cy)
        degree -= 2
        delay(0.01)

while True:
    make_rectangle();
    make_circle();
    
close_canvas()