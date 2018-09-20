from pico2d import *
import  math

KPU_WIDTH, KPU_HEIGHT = 1280, 1024

open_canvas(KPU_WIDTH, KPU_HEIGHT)

kpu_ground = load_image('KPU_GROUND.png')
character = load_image('animation_sheet.png')
cursor = load_image('hand_arrow.png')

def handle_events():
    global mouseX, mouseY, targetX, targetY, x, y
    global distance
    global running, moving
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            mouseX, mouseY = event.x, KPU_HEIGHT - 1 - event.y
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            moving = True
            distance = math.sqrt((mouseX - x)**2 + (mouseY-y)**2)
            targetX, targetY = mouseX, mouseY
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
    global x, y, distance, moving
    if moving:
        radian = math.atan2(targetY - y, targetX - x)
        x, y = x + math.cos(radian) * 10, y + math.sin(radian) * 10
        distance = math.sqrt((targetX - x) ** 2 + (targetY - y) ** 2)
        if distance < 4:
            x, y = targetX, targetY
            moving = False
    draw(x, y)

running = True
moving = False
distance = 0.0
x, y = KPU_WIDTH // 2, KPU_HEIGHT // 2
mouseX, mouseY = x, y
targetX, targetY = x, y
frame = 0

while running:
    handle_events()
    move()
    delay(1/60)

close_canvas()