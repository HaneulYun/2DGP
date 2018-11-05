import game_framework
from pico2d import *

import main_state

MOTION_TYPE = 0
MOTION_FRAME = 1

MOTION_IDLE = (4, 2, 0)
MOTION_MOVE = (3, 6)

MOTION_JUMP = (2, 4)
MOTION_DROP = (1, 4)

MOTION_DIED = (0, 9)

TILE_PER_METER = (1 / 1)  # 1 tile 1 m
MOVE_SPEED_MPS = 4

# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

SLEEP_TIME = 10

LEFT_DOWN, LEFT_UP, RIGHT_DOWN, RIGHT_UP, SLEEP_TIMER, JUMP, ATTACK = range(7)

key_event_table = {
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYDOWN, SDLK_s): JUMP,
    (SDL_KEYDOWN, SDLK_a): ATTACK
}


class IdleState:
    @staticmethod
    def enter(dragon, event):
        global TIME_PER_ACTION, ACTION_PER_TIME, FRAMES_PER_ACTION
        TIME_PER_ACTION = 0.5
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = MOTION_IDLE[MOTION_FRAME]

        if event == RIGHT_DOWN:
            dragon.velocity += MOVE_SPEED_MPS
        elif event == LEFT_DOWN:
            dragon.velocity -= MOVE_SPEED_MPS
        elif event == RIGHT_UP:
            dragon.velocity -= MOVE_SPEED_MPS
        elif event == LEFT_UP:
            dragon.velocity += MOVE_SPEED_MPS

        if dragon.velocity < 0:
            dragon.dir = -1
        elif dragon.velocity > 0:
            dragon.dir = 1

        dragon.timer = get_time()

    @staticmethod
    def exit(dragon, event):
        pass
        #if event == SPACE:
        #    dragon.fire_ball()

    @staticmethod
    def do(dragon):
        dragon.frame = (dragon.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) %\
                       FRAMES_PER_ACTION
        #if get_time() - dragon.timer >= SLEEP_TIME:
        #    dragon.add_event(SLEEP_TIMER)

    @staticmethod
    def draw(dragon):
        if dragon.dir == 1:
            h = ''
        else:
            h = 'h'
        dragon.image.clip_composite_draw(int(dragon.frame) * 25, MOTION_IDLE[MOTION_TYPE] * 25, 25, 25, 0, h,
                                         dragon.x * 8 * game_framework.windowScale,
                                         (dragon.y * 8 + 14.5) * game_framework.windowScale,
                                         25 * game_framework.windowScale, 25 * game_framework.windowScale)


class MoveState:
    @staticmethod
    def enter(dragon, event):
        global TIME_PER_ACTION, ACTION_PER_TIME, FRAMES_PER_ACTION
        TIME_PER_ACTION = 0.5
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = MOTION_MOVE[MOTION_FRAME]

        if event == LEFT_DOWN:
            dragon.velocity -= MOVE_SPEED_MPS
        elif event == RIGHT_DOWN:
            dragon.velocity += MOVE_SPEED_MPS
        elif event == LEFT_UP:
            dragon.velocity += MOVE_SPEED_MPS
        elif event == RIGHT_UP:
            dragon.velocity -= MOVE_SPEED_MPS

        if dragon.velocity < 0:
            dragon.dir = -1
        elif dragon.velocity > 0:
            dragon.dir = 1

    @staticmethod
    def exit(dragon, event):
        pass
        #if event == SPACE:
        #    dragon.fire_ball()

    @staticmethod
    def do(dragon):
        dragon.frame = (dragon.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) %\
                       FRAMES_PER_ACTION

        if not main_state.stage.map[int(dragon.y)][int(dragon.x)]:
            if dragon.velocity < 0 :
                if not main_state.stage.map[int(dragon.y)][int(dragon.x - 1.5)]:
                    dragon.x += dragon.velocity * game_framework.frame_time
            elif dragon.velocity > 1:
                if not main_state.stage.map[int(dragon.y)][int(dragon.x + 1.5)]:
                    dragon.x += dragon.velocity * game_framework.frame_time

    @staticmethod
    def draw(dragon):
        if dragon.dir == 1:
            h = ''
        else:
            h = 'h'
        dragon.image.clip_composite_draw(int(dragon.frame) * 25, MOTION_MOVE[MOTION_TYPE] * 25, 25, 25, 0, h,
                                         dragon.x * 8 * game_framework.windowScale,
                                         (dragon.y * 8 + 14.5) * game_framework.windowScale,
                                         25 * game_framework.windowScale, 25 * game_framework.windowScale)


class SleepState:
    @staticmethod
    def enter(dragon, event):
        dragon.frame = 0

    @staticmethod
    def exit(dragon, event):
        pass

    @staticmethod
    def do(dragon):
        dragon.frame = (dragon.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(dragon):
        if dragon.dir == 1:
            #dragon.image.clip_composite_draw(int(dragon.frame) * 100, 300, 100, 100, 3.141592 / 2,
            #                              '', dragon.x - 25, dragon.y - 25, 100, 100)
            dragon.image.clip_composite_draw(dragon.frame * 25, 0 * 25, 25, 25, 0, '',
                                             dragon.x * 8 * game_framework.windowScale,
                                             (dragon.y * 8 + 14.5) * game_framework.windowScale,
                                             25 * game_framework.windowScale,
                                             25 * game_framework.windowScale)
        else:
            #dragon.image.clip_composite_draw(int(dragon.frame) * 100, 200, 100, 100, -3.141592 / 2,
            #                              '', dragon.x + 25, dragon.y - 25, 100, 100)
            dragon.image.clip_composite_draw(dragon.frame * 25, 0 * 25, 25, 25, 0, '',
                                             dragon.x * 8 * game_framework.windowScale,
                                             (dragon.y * 8 + 14.5) * game_framework.windowScale,
                                             25 * game_framework.windowScale,
                                             25 * game_framework.windowScale)


next_state_table = {
    IdleState: {LEFT_DOWN: MoveState, LEFT_UP: MoveState, RIGHT_DOWN: MoveState, RIGHT_UP: MoveState,
                SLEEP_TIMER: SleepState, JUMP : IdleState, ATTACK : IdleState },
    MoveState: {LEFT_DOWN: IdleState, LEFT_UP: IdleState, RIGHT_DOWN: IdleState, RIGHT_UP: IdleState,
                JUMP: IdleState, ATTACK: IdleState},
    SleepState: {LEFT_DOWN: MoveState, LEFT_UP: MoveState, RIGHT_DOWN: MoveState, RIGHT_UP: MoveState,
                 JUMP: IdleState, ATTACK: IdleState},
}


class Dragon:
    def __init__(self):
        self.x, self.y = 3.5, 1
        self.image = load_image('resources\sprites\Characters\Dragon.png')
        # self.moveMotion = MOTION_STOP
        # self.direction = DIRECTION_RIGHT
        # self.jumpMotion = None
        # self.attackMotion = False
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

        # self.jumping = 0.0

        # self.frameCycle = 0
        # self.speed = 0.04

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

        #if self.moveMotion == MOTION_MOVE:
        #    if self.direction == DIRECTION_LEFT and not main_state.stage.map[int(self.y)][int(self.x)]\
        #            and not main_state.stage.map[int(self.y)][int(self.x - 1.5)]:
        #        self.x = self.x - self.speed
        #    elif self.direction == DIRECTION_RIGHT and not main_state.stage.map[int(self.y)][int(self.x)]\
        #            and not main_state.stage.map[int(self.y)][int(self.x + 1.5)]:
        #        self.x = self.x + self.speed
        #if self.jumpMotion == MOTION_JUMP:
        #    self.y = self.y + self.speed
        #    self.jumping += self.speed
        #    if self.jumping > 5.5:
        #        self.drop()
        #elif self.jumpMotion == MOTION_DROP:
        #    self.y = self.y - self.speed
        #    if main_state.stage.map[int(self.y)][int(self.x)]:
        #        self.y = int(self.y+1)
        #        self.jumpMotion = None
        #        self.stop()
        #elif not main_state.stage.map[int(self.y - 1)][int(self.x)]:
        #    self.drop()

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)