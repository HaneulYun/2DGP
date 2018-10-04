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

frame_gap = 0

def draw(x, y):
    global frame, points, moveNum, frame_gap, check, points
    action = (1-moving) * 2
    if(points[moveNum-1][0] >= x):
        action += direction
    kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)
    for checking in range(10):
        if check[checking]:
            character.clip_draw(0, 100 * 0, 100, 100, points[checking-1][0], points[checking-1][1])
    character.clip_draw(frame * 100, 100 * action, 100, 100, x, y)
    frame_gap = (frame_gap + 1) % 3
    if frame_gap == 0:
        frame = (frame + 1) % 8
    cursor.draw(mouseX + cursor.w // 2, mouseY - cursor.h // 2)
    update_canvas()

def set_curve_4_points(p1, p2, p3, p4):
    global x, y, moveRatio, moveNum, check
    t = moveRatio / 150
    x = ((-t ** 3 + 2 * t ** 2 - t) * p1[0] + (3 * t ** 3 - 5 * t ** 2 + 2) * p2[0] + (
                        -3 * t ** 3 + 4 * t ** 2 + t) * p3[0] + (t ** 3 - t ** 2) * p4[0]) / 2
    y = ((-t ** 3 + 2 * t ** 2 - t) * p1[1] + (3 * t ** 3 - 5 * t ** 2 + 2) * p2[1] + (
                        -3 * t ** 3 + 4 * t ** 2 + t) * p3[1] + (t ** 3 - t ** 2) * p4[1]) / 2
    moveRatio += 1
    if moveRatio > 150:
        moveRatio = 0
        check[moveNum] = True
        moveNum = (moveNum+1) % 10

def move():
    global x, y, moving, points, moveNum, moveRatio
    if moving:
        set_curve_4_points(points[moveNum-3], points[moveNum-2], points[moveNum-1], points[moveNum])

running = True
moving = True
direction = True
frame = 0
hide_cursor()

import random

x, y = KPU_WIDTH // 2, KPU_HEIGHT // 2
mouseX, mouseY = x, y

size = 10
userPosition = [KPU_WIDTH // 2, KPU_HEIGHT // 2]
points = [(random.randint(0, 1280), random.randint(0, 1024)) for i in range(size)]
check = [False for i in range (size)]
moveRatio = 0
moveNum = 1

while running:
    handle_events()
    move()
    draw(x, y)
    delay(1/60)

close_canvas()