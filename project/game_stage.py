import game_framework
from pico2d import *


class Stage:
    def __init__(self, url):
        self.image = load_image(url)
        self.section = 5
        self.map = None

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
        self.image.clip_draw(320 * 0, 208 * self.section, 320, 208,
                             320 * game_framework.windowScale // 2,
                             208 * game_framework.windowScale // 2,
                             320 * game_framework.windowScale, 208 *
                             game_framework.windowScale)

    def load(self, url):
        self.map = []
        f = open(url, 'r')
        lines = f.readlines()
        tmp = [i.split() for i in lines]
        for i in tmp:
            self.map = [[int(j) for j in i]] + self.map
        f.close()
