import game_framework
from pico2d import *

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm

# Ghost Rotate Speed
# fill expressions correctly
ROTATE_SPEED_DPS = 720

# Ghost Action Speed
# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

AWAKE_TIME = 2

GHOST_AWAKE, GHOST_AROUND = range(2)


class GhostAwakeState:

    @staticmethod
    def enter(ghost, event):
        ghost.timer = get_time()

    @staticmethod
    def exit(ghost, event):
        pass

    @staticmethod
    def do(ghost):
        t = get_time() - ghost.timer
        if t >= AWAKE_TIME:
            ghost.add_event(GHOST_AROUND)

        t /= AWAKE_TIME
        ghost.x = (1 - t) * (ghost.cx - 25 * ghost.dir) + t * (ghost.cx + ghost.dis * ghost.dir)
        ghost.y = (1 - t) * (ghost.cy - ghost.dis - 25) + t * ghost.cy
        ghost.rotate = (1-t) * 90 * ghost.dir
        ghost.frame = (ghost.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        ghost.image.opacify(0.2 + math.cos(ghost.rotate / 180.0 * 3.141592 / 4) * 0.6)

    @staticmethod
    def draw(ghost):
        if ghost.dir == 1:
            ghost.image.clip_composite_draw(int(ghost.frame) * 100, 300, 100, 100, ghost.rotate / 180 * 3.141592, '',
                                            ghost.x, ghost.y, 100, 100)
        else:
            ghost.image.clip_composite_draw(int(ghost.frame) * 100, 200, 100, 100, ghost.rotate / 180 * 3.141592, '',
                                            ghost.x, ghost.y, 100, 100)


class GhostState:

    @staticmethod
    def enter(ghost, event):
        pass

    @staticmethod
    def exit(ghost, event):
        pass

    @staticmethod
    def do(ghost):
        ghost.rotate += 720 * game_framework.frame_time
        ghost.x = ghost.cx + ghost.dis * math.cos(ghost.rotate / 180.0 * 3.141592) * ghost.dir
        ghost.y = ghost.cy + ghost.dis * math.sin(ghost.rotate / 180.0 * 3.141592)
        ghost.frame = (ghost.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        ghost.image.opacify(0.2 + math.cos(ghost.rotate / 180.0 * 3.141592 / 4) * 0.6)

    @staticmethod
    def draw(ghost):
        if ghost.dir == 1:
            ghost.image.clip_draw(int(ghost.frame) * 100, 300, 100, 100, ghost.x, ghost.y)
        else:
            ghost.image.clip_draw(int(ghost.frame) * 100, 200, 100, 100, ghost.x, ghost.y)


next_state_table = {
    GhostState: {GHOST_AWAKE: GhostState, GHOST_AROUND: GhostState},
    GhostAwakeState: {GHOST_AWAKE: GhostAwakeState, GHOST_AROUND: GhostState}
}


class Ghost:
    def __init__(self, x, y, dir):
        self.cx, self.cy = x, y + PIXEL_PER_METER * 3
        self.x, self.y = self.cx, self.cy
        # Boy is only once created, so instance image loading is fine
        self.image = load_image('animation_sheet.png')
        self.dir = dir
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = GhostAwakeState
        self.cur_state.enter(self, None)
        self.rotate = 0
        self.dis = PIXEL_PER_METER * 3
        self.timer = 0
        self.cur_state.enter(self, 0)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        pass
