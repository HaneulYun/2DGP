import game_framework
from pico2d import *


class Stage:
    def __init__(self):
        self.image = load_image('resources\sprites\Rounds\Round A-1.png')

    def draw(self):
        self.image.clip_draw(320 * 3, 208 * 6, 352, 224,
                             320 * game_framework.windowScale // 2,
                             240 * game_framework.windowScale // 2,
                             320 * game_framework.windowScale,
                             240 * game_framework.windowScale)
        self.image.clip_draw(320 * 0, 208 * 6, 320, 208,
                             320 * game_framework.windowScale // 2,
                             240 * game_framework.windowScale // 2,
                             320 * game_framework.windowScale,
                             240 * game_framework.windowScale)
        self.image.clip_draw(320 * 0, 208 * 5, 320, 208,
                             320 * game_framework.windowScale // 2,
                             208 * game_framework.windowScale // 2,
                             320 * game_framework.windowScale, 208 *
                             game_framework.windowScale)
