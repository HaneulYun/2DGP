import game_framework
import pico2d

import main_state


game_framework.windowScale = 4
windowScale = game_framework.windowScale

# fill here
pico2d.open_canvas(320 * windowScale, 240 * windowScale)
game_framework.run(main_state)
pico2d.close_canvas()