from pico2d import *

KPU_WIDTH, KPU_HEIGHT = 1280, 1024

open_canvas(KPU_WIDTH, KPU_HEIGHT)

kpu_ground = load_image('KPU_GROUND.png')
character = load_image('animation_sheet.png')
cursor = load_image('hand_arrow.png')

def handle_events():
    pass

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
x, y = KPU_WIDTH // 2, KPU_HEIGHT // 2
mouseX, mouseY = x, y
frame = 0

while running:
    pass

close_canvas()