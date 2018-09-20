from pico2d import *

KPU_WIDTH, KPU_HEIGHT = 1280, 1024

open_canvas(KPU_WIDTH, KPU_HEIGHT)
kpu_ground = load_image('KPU_GROUND.png')
character = load_image('animation_sheet.png')

def handle_event():
    global running
    global x, y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE)
            running = False
        elif event.type == SDL_MOUSEMOTION:
            x, y = event.x, KPU_HEIGHT - 1 - event.y
    pass

def draw(radian, x, y):
    clear_canvas()
    kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)
    character.rotate_draw(radian, x, y)
    update_canvas()
    delay(0.01)
    pass

def move(x1, y1, x2, y2):
    pass

def input():
    pass


while True:
    draw(0, KPU_WIDTH // 2, KPU_HEIGHT // 2)

close_canvas()