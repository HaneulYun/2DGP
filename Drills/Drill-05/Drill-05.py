from pico2d import *
import math


open_canvas()

grass = load_image('grass.png')
character = load_image('character.png')

 # fill here

def draw(radian, x, y):
    clear_canvas()
    grass.draw(400, 30)
    character.rotate_draw(radian, x, y)
    update_canvas()
    delay(0.01)

def move(x1, y1, x2, y2):
    radian = math.atan2(y2 - y1, x2 - x1)
    distance = math.sqrt((x2 - x1)**2 + (y2-y1)**2)
    while distance > 0:
        draw(radian, x2 - math.cos(radian) * distance, y2 - math.sin(radian) * distance)
        distance -= 1

def idle():
    x1, y1 = 203, 535;
    for x2, y2 in ((132, 243), (535, 470), (477, 203), (715, 136), (316, 225),
                 (510, 92), (692, 518), (682, 336), (712, 349), (203, 535)):
        move(x1, y1, x2, y2)
        x1, y1 = x2, y2

while True:
    idle()

close_canvas()