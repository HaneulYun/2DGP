import game_framework
from pico2d import *

from game_bubble import Bubble

import main_state
import game_world

MOTION_TYPE = 0
MOTION_FRAME = 1

MOTION_IDLE = (4, 2)
MOTION_MOVE = (3, 6)
MOTION_SLEEP = (5, 3)

MOTION_JUMP = (2, 4)
MOTION_DROP = (1, 4)

MOTION_DIED = (0, 9)

TILE_PER_METER = (1 / 1)  # 1 tile 1 m
MOVE_SPEED_MPS = 10.0

# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8
TYPE_OF_ACTION = 0

SLEEP_TIME = 3

LEFT_DOWN, LEFT_UP, RIGHT_DOWN, RIGHT_UP, SLEEP_TIMER, JUMP, DROP, ATTACK = range(8)

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
        global TIME_PER_ACTION, ACTION_PER_TIME
        TIME_PER_ACTION = 0.75
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        dragon.cur_frame_per_action = MOTION_IDLE[MOTION_FRAME]

        if event == RIGHT_DOWN:
            dragon.velocity += MOVE_SPEED_MPS
        elif event == LEFT_DOWN:
            dragon.velocity -= MOVE_SPEED_MPS
        elif event == RIGHT_UP:
            dragon.velocity -= MOVE_SPEED_MPS
        elif event == LEFT_UP:
            dragon.velocity += MOVE_SPEED_MPS
        elif event == JUMP:
            dragon.rest_jump_volume = 5.5
            dragon.cur_frame_per_action = MOTION_JUMP[MOTION_FRAME]

        if dragon.velocity < 0:
            dragon.dir = -1
        elif dragon.velocity > 0:
            dragon.dir = 1
        dragon.frame = 0
        dragon.timer = get_time()

    @staticmethod
    def exit(dragon, event):
        if event == ATTACK:
            dragon.fire_bubble()
            dragon.attack = 1

    @staticmethod
    def do(dragon):
        dragon.frame = (dragon.frame + dragon.cur_frame_per_action * ACTION_PER_TIME * game_framework.frame_time) % \
                       dragon.cur_frame_per_action
        if dragon.rest_jump_volume > 0:
            dragon.y += MOVE_SPEED_MPS * game_framework.frame_time
            dragon.rest_jump_volume -= MOVE_SPEED_MPS * game_framework.frame_time
            if dragon.rest_jump_volume < 0:
                dragon.y += dragon.rest_jump_volume
                dragon.rest_jump_volume = 0
                dragon.cur_frame_per_action = MOTION_DROP[MOTION_FRAME]
                dragon.frame = 0
        elif not main_state.stage.map[int(dragon.y + 0.99 - 1)][int(dragon.x)]:
            dragon.y -= MOVE_SPEED_MPS * game_framework.frame_time
            if main_state.stage.map[int(dragon.y)][int(dragon.x)]:
                dragon.y = int(dragon.y + 1)
                dragon.cur_frame_per_action = MOTION_IDLE[MOTION_FRAME]
                dragon.frame = 0
        elif get_time() - dragon.timer >= SLEEP_TIME:
            dragon.add_event(SLEEP_TIMER)

    @staticmethod
    def draw(dragon):
        if dragon.dir == 1:
            h = ''
        else:
            h = 'h'

        if dragon.rest_jump_volume > 0:
            action_type = MOTION_JUMP[MOTION_TYPE]
        elif not main_state.stage.map[int(dragon.y + 0.99 - 1)][int(dragon.x)]:
            action_type = MOTION_DROP[MOTION_TYPE]
        else:
            action_type = MOTION_IDLE[MOTION_TYPE]
        dragon.image.clip_composite_draw(int(dragon.frame) * 25, action_type * 25, 25, 25, 0, h,
                                         dragon.x * 8 * game_framework.windowScale,
                                         (dragon.y * 8 + 14.5) * game_framework.windowScale,
                                         25 * game_framework.windowScale, 25 * game_framework.windowScale)


class MoveState:
    @staticmethod
    def enter(dragon, event):
        global TIME_PER_ACTION, ACTION_PER_TIME
        TIME_PER_ACTION = 0.5
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        dragon.cur_frame_per_action = MOTION_MOVE[MOTION_FRAME]

        if event == LEFT_DOWN:
            dragon.velocity -= MOVE_SPEED_MPS
        elif event == RIGHT_DOWN:
            dragon.velocity += MOVE_SPEED_MPS
        elif event == LEFT_UP:
            dragon.velocity += MOVE_SPEED_MPS
        elif event == RIGHT_UP:
            dragon.velocity -= MOVE_SPEED_MPS
        elif event == JUMP:
            dragon.rest_jump_volume = 5.5
            dragon.cur_frame_per_action = MOTION_JUMP[MOTION_FRAME]

        if dragon.velocity < 0:
            dragon.dir = -1
        elif dragon.velocity > 0:
            dragon.dir = 1

        dragon.frame = 0

    @staticmethod
    def exit(dragon, event):
        if event == ATTACK:
            dragon.fire_bubble()

    @staticmethod
    def do(dragon):
        dragon.frame = (dragon.frame + dragon.cur_frame_per_action * ACTION_PER_TIME * game_framework.frame_time) % \
                       dragon.cur_frame_per_action

        if not main_state.stage.map[int(dragon.y)][int(dragon.x)]:
            if dragon.velocity < 0:
                if not main_state.stage.map[int(dragon.y)][int(dragon.x - 1.5)]:
                    dragon.x += dragon.velocity * game_framework.frame_time
            elif dragon.velocity > 1:
                if not main_state.stage.map[int(dragon.y)][int(dragon.x + 1.5)]:
                    dragon.x += dragon.velocity * game_framework.frame_time

        if dragon.rest_jump_volume > 0:
            dragon.y += MOVE_SPEED_MPS * game_framework.frame_time
            dragon.rest_jump_volume -= MOVE_SPEED_MPS * game_framework.frame_time
            if dragon.rest_jump_volume < 0:
                dragon.y += dragon.rest_jump_volume
                dragon.rest_jump_volume = 0
                dragon.cur_frame_per_action = MOTION_DROP[MOTION_FRAME]
                dragon.frame = 0
        elif not main_state.stage.map[int(dragon.y + 0.99 - 1)][int(dragon.x)]:
            dragon.y -= MOVE_SPEED_MPS * game_framework.frame_time
            if main_state.stage.map[int(dragon.y)][int(dragon.x)]:
                dragon.y = int(dragon.y + 1)
                dragon.cur_frame_per_action = MOTION_MOVE[MOTION_FRAME]
                dragon.frame = 0

    @staticmethod
    def draw(dragon):
        if dragon.dir == 1:
            h = ''
        else:
            h = 'h'

        if dragon.rest_jump_volume > 0:
            action_type = MOTION_JUMP[MOTION_TYPE]
        elif not main_state.stage.map[int(dragon.y + 0.99 - 1)][int(dragon.x)]:
            action_type = MOTION_DROP[MOTION_TYPE]
        else:
            action_type = MOTION_MOVE[MOTION_TYPE]
        dragon.image.clip_composite_draw(int(dragon.frame) * 25, action_type * 25, 25, 25, 0, h,
                                         dragon.x * 8 * game_framework.windowScale,
                                         (dragon.y * 8 + 14.5) * game_framework.windowScale,
                                         25 * game_framework.windowScale, 25 * game_framework.windowScale)


class SleepState:
    @staticmethod
    def enter(dragon, event):
        global TIME_PER_ACTION, ACTION_PER_TIME
        TIME_PER_ACTION = 1
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        dragon.cur_frame_per_action = MOTION_SLEEP[MOTION_FRAME]

        dragon.frame = 0

    @staticmethod
    def exit(dragon, event):
        pass

    @staticmethod
    def do(dragon):
        dragon.frame = (dragon.frame + dragon.cur_frame_per_action * ACTION_PER_TIME * game_framework.frame_time) % \
                       dragon.cur_frame_per_action

    @staticmethod
    def draw(dragon):
        if dragon.dir == 1:
            h = ''
        else:
            h = 'h'
        dragon.image.clip_composite_draw(int(dragon.frame) * 30, MOTION_SLEEP[MOTION_TYPE] * 25, 30, 25, 0, h,
                                         dragon.x * 8 * game_framework.windowScale,
                                         (dragon.y * 8 + 14.5) * game_framework.windowScale,
                                         25 * game_framework.windowScale, 25 * game_framework.windowScale)


next_state_table = {
    IdleState: {LEFT_DOWN: MoveState, LEFT_UP: MoveState, RIGHT_DOWN: MoveState, RIGHT_UP: MoveState,
                SLEEP_TIMER: SleepState, JUMP: IdleState, ATTACK: IdleState },
    MoveState: {LEFT_DOWN: IdleState, LEFT_UP: IdleState, RIGHT_DOWN: IdleState, RIGHT_UP: IdleState,
                JUMP: MoveState, ATTACK: MoveState},
    SleepState: {LEFT_DOWN: MoveState, LEFT_UP: MoveState, RIGHT_DOWN: MoveState, RIGHT_UP: MoveState,
                 JUMP: IdleState, ATTACK: IdleState},
}


class Dragon:
    def __init__(self):
        self.x, self.y = 3.5, 1
        self.image = load_image('resources\sprites\Characters\Dragon.png')
        # self.moveMotion = MOTION_STOP
        # self.jumpMotion = None
        # self.attackMotion = False
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.attack = 0
        self.rest_jump_volume = 0
        self.cur_frame_per_action = 0
        self.cur_state.enter(self, None)

    def fire_bubble(self):
        bubble = Bubble(self.x, self.y, self.dir*3)
        game_world.add_object(bubble, 1)

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
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)