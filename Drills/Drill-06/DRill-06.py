from pico2d import *
import math

KPU_WIDTH, KPU_HEIGHT = 1280, 1024

open_canvas(KPU_WIDTH, KPU_HEIGHT)
kpu_ground = load_image('KPU_GROUND.png')
character = load_image('animation_sheet.png')
cursor = load_image('hand_arrow.png')

def handle_event():
    global running
    global x, y
    global mouseX, mouseY
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            running = False
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            mouseX, mouseY = event.x, KPU_HEIGHT - 1 - event.y
            return True

def draw(radian, x, y):
    global frame
    clear_canvas()
    kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)
    character.clip_draw(frame*100, 100*1, 100, 100, x, y)
    update_canvas()
    frame = (frame + 1) % 8
    delay(0.02)
    pass

def move(x1, y1, x2, y2):
    global x, y
    radian = math.atan2(y2 - y1, x2 - x1)
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    while distance > 0 :
        draw(radian, x2 - math.cos(radian) * distance, y2 - math.sin(radian) * distance)
        distance -= 1
        if handle_event():
            x, y = x2 - math.cos(radian) * distance, y2 - math.sin(radian) * distance
            move(x, y, mouseX, mouseY)
            return 0
    x, y = x2 - math.cos(radian) * distance, y2 - math.sin(radian) * distance

def idle_with_mouse():
    if handle_event():
        move(x, y, mouseX, mouseY)

running = True

mouseX, mouseY = KPU_WIDTH // 2, KPU_HEIGHT // 2
x, y = mouseX, mouseY
frame = 0

while running:
    idle_with_mouse()

close_canvas()