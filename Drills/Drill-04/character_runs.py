from pico2d import *
open_canvas()
grass = load_image('grass.png')
character = load_image('animation_sheet.png')

x = 0
wPivotTerm = 25

# 여기를 채우세요.
x = 0
direction = True
frame = 0
while x < 800 :
    clear_canvas()
    grass.draw(400, 30)
    character.clip_draw(frame * 100, direction * 100, 100, 100, x, 90)
    if direction :
        x += 10
        if x > get_canvas_width() - wPivotTerm :
            x = get_canvas_width() - wPivotTerm
            direction = False
    else :
        x -= 10
        if x < wPivotTerm :
            x = wPivotTerm
            direction = True
    update_canvas()
    frame = (frame + 1) % 8
    delay(0.05)
    get_events()

close_canvas()