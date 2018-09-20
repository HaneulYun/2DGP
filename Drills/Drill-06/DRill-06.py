from pico2d import *

KPU_WIDTH, KPU_HEIGHT = 1280, 1024

open_canvas(KPU_WIDTH, KPU_HEIGHT)

kpu_ground = load_image('KPU_GROUND.png')
character = load_image('animation_sheet.png')
cursor = load_image('hand_arrow.png')

def handle_events():
    global mouseX, mouseY
    global moving
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            mouseX, mouseY = event.x, KPU_HEIGHT - 1 - event.y
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            moving = True
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

def draw(x, y):
    global frame
    kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)
    character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)
    frame = (frame + 1) % 8
    cursor.draw(mouseX, mouseY)
    update_canvas()

def move():
    pass

running = True
moving = False
x, y = KPU_WIDTH // 2, KPU_HEIGHT // 2
mouseX, mouseY = x, y
frame = 0

while running:
    pass

close_canvas()