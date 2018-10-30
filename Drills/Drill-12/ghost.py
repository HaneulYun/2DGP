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
    def enter(ghost, event):
        pass

    @staticmethod
    def exit(ghost, event):
        pass

    @staticmethod
    def do(ghost):
        ghost.rotate += 1
        ghost.x = ghost.cx + ghost.dis * math.cos(ghost.rotate / 180.0 * 3.141592)
        ghost.y = ghost.cy + ghost.dis * math.sin(ghost.rotate / 180.0 * 3.141592)
        ghost.frame = (ghost.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(ghost):
        if ghost.dir == 1:
            ghost.image.clip_draw(int(ghost.frame) * 100, 300, 100, 100, ghost.x, ghost.y)
        else:
            ghost.image.clip_draw(int(ghost.frame) * 100, 200, 100, 100, ghost.x, ghost.y)


class Ghost:
    def __init__(self, x, y, dir):
        self.cx, self.cy = x, y + PIXEL_PER_METER * 3
        self.x, self.y = self.cx, self.cy
        # Boy is only once created, so instance image loading is fine
        self.image = load_image('animation_sheet.png')
        self.dir = dir
        self.velocity = 0
        self.frame = 0
        self.cur_state = GhostState
        self.cur_state.enter(self, None)
        self.rotate = 0
        self.dis = PIXEL_PER_METER * 3

    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        pass
