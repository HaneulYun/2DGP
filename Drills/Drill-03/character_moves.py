from pico2d import *
import math

open_canvas()

grass = load_image('grass.png')
character = load_image('character.png')

# fill here
PI = 3.141592

width = 800
height = 600

cx = 400
cy = 315
radius = 30 + 200

pivotTerm = 35
speed = 300
rSpeed = 0.4

x = 400
y = 85
direction = 0
radian = 0

moveType = True

while True :
    clear_canvas_now()
    grass.draw_now(400, 30)

    if moveType :
        if direction == 0 :
            x += speed / 60
            if x >= width - pivotTerm :
                x = width - pivotTerm
                direction = 1
                radian = 0.5
        elif direction == 1 :
            y += speed / 60
            if y >= height - pivotTerm :
                y = height - pivotTerm
                direction = 2
                radian = 1.0
        elif direction == 2 :
            x -= speed / 60
            if x <= pivotTerm :
                x = pivotTerm
                direction = 3
                radian = 1.5
        elif direction == 3 :
            y -= speed / 60
            if y <= 50 + pivotTerm :
                y = 50 + pivotTerm
                direction = 4
                radian = 2.0
        elif direction == 4 :
            x += speed / 60
            if x >= width / 2 :
                x = width / 2
                direction = 0
                moveType = False
                radian = 0
    else :
        radian += rSpeed / 60
        x = cx + math.cos(PI * (radian - 0.5)) * radius
        y = cy + math.sin(PI * (radian - 0.5)) * radius
        if radian > 2.0 :
            x = width / 2
            y = 85
            direction = 0
            moveType = True
            radian = 0

    character.rotate_draw(PI * radian, x, y)
    character.draw_now(-100, -100)
    delay(1 / 60)

close_canvas()
