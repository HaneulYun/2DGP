import game_framework
from pico2d import *

# Boy Run Speed
# fill expressions correctly
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
ROTATE_SPEED_KMPH = 20.0  # Km / Hour
ROTATE_SPEED_MPM = (ROTATE_SPEED_KMPH * 1000.0 / 60.0)
ROTATE_SPEED_MPS = (ROTATE_SPEED_MPM / 60.0)
ROTATE_SPEED_PPS = (ROTATE_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class GhostState:

    @staticmethod
    def enter(boy, event):
        pass

    @staticmethod
    def exit(boy, event):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(int(boy.frame) * 100, 300, 100, 100, boy.x, boy.y)
        else:
            boy.image.clip_draw(int(boy.frame) * 100, 200, 100, 100, boy.x, boy.y)


class Ghost:
    def __init__(self, x, y):
        self.x, self.y = x, y
        # Boy is only once created, so instance image loading is fine
        self.image = load_image('animation_sheet.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.cur_state = GhostState
        self.cur_state.enter(self, None)

    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        pass
