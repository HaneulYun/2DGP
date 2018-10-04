from pico2d import *
import  math

KPU_WIDTH, KPU_HEIGHT = 1280, 1024

open_canvas(KPU_WIDTH, KPU_HEIGHT)
kpu_ground = load_image('KPU_GROUND.png')
character = load_image('animation_sheet.png')
cursor = load_image('hand_arrow.png')

def handle_events():
    global mouseX, mouseY, x, y
    global distance, direction
    global running, moving
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            mouseX, mouseY = event.x, KPU_HEIGHT - 1 - event.y
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

def draw(x, y):
    global frame, points, moveNum
    action = (1-moving) * 2
    if(points[moveNum][0] >= x):
        action += direction
    kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)
    character.clip_draw(frame * 100, 100 * action, 100, 100, x, y)
    frame = (frame + 1) % 8
    #cursor.draw(mouseX + cursor.w // 2, mouseY - cursor.h // 2)
    update_canvas()

def set_curve_4_points(p1, p2, p3, p4, ratio):
    global x, y
    t = ratio / 100
    x = ((-t ** 3 + 2 * t ** 2 - t) * p1[0] + (3 * t ** 3 - 5 * t ** 2 + 2) * p2[0] + (
                        -3 * t ** 3 + 4 * t ** 2 + t) * p3[0] + (t ** 3 - t ** 2) * p4[0]) / 2
    y = ((-t ** 3 + 2 * t ** 2 - t) * p1[1] + (3 * t ** 3 - 5 * t ** 2 + 2) * p2[1] + (
                        -3 * t ** 3 + 4 * t ** 2 + t) * p3[1] + (t ** 3 - t ** 2) * p4[1]) / 2

def move():
    global x, y, t, moving
    if moving:
        set_curve_4_points()
        if t > 100:
            moving = False

running = True
moving = False
direction = True
frame = 0
hide_cursor()

import random

x, y = KPU_WIDTH // 2, KPU_HEIGHT // 2
mouseX, mouseY = x, y

size = 10
userPosition = [KPU_WIDTH // 2, KPU_HEIGHT // 2]
points = [(random.randint(0, 1280), random.randint(0, 1024)) for i in range(size)]
moveRatio = 0
moveNum = 1

while running:
    handle_events()
    move()
    draw(x, y)
    delay(1/60)

close_canvas()