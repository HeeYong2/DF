from pico2d import*
import random
import time

ITEM_MAX = 10

class Item:
    PIXEL_PER_METER = (10.0 / 0.9)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.95
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION_ITEM = 6
    ITEM_SPEED = 2

    image = None

    def __init__(self):
        self.x = [- 100] * ITEM_MAX
        self.y = [- 100] * ITEM_MAX
        self.frame = [0] * ITEM_MAX
        self.totalframe = [0] * ITEM_MAX
        self.use_flag = [0] * ITEM_MAX
        self.dir_x = [0] * ITEM_MAX
        self.dir_y = [0] * ITEM_MAX
        self.movetime1 = [time.time()] * ITEM_MAX

        if Item.image == None:
            Item.image = load_image('power_item.png')


    def draw(self, frame_time):
        for num in range(ITEM_MAX):
            self.image.clip_draw(self.frame[num] * 40, 0, 40, 26, self.x[num], self.y[num])

        self.draw_bb()

    def update(self, frame_time):
        for num in range(ITEM_MAX):
            if self.use_flag[num] == 0:
                continue

            self.item_move(frame_time, num)

            self.totalframe[num] += Item.FRAMES_PER_ACTION_ITEM * Item.ACTION_PER_TIME * frame_time
            self.frame[num] = int(self.totalframe[num]) % 6


    def create_item(self, x, y):
        for num in range(ITEM_MAX):
            if self.use_flag[num] == 0:
                self.x[num] = x
                self.y[num] = y
                self.use_flag[num] = 1
                return

    def item_move(self, frame_time, num):
        movetime2 = time.time()

        if movetime2 - self.movetime1[num] > 3 or self.x[num] > 550 or self.x[num] < 0 or self.y[num] > 730 or self.y[num] < 0:
            self.dir_x[num] = random.randrange(0, 2)
            self.dir_y[num] = random.randrange(0, 2)
            self.movetime1[num] = movetime2

        if self.use_flag[num] == 1:
            if self.dir_x[num] == 0:
                self.x[num] += Item.RUN_SPEED_PPS * frame_time
            elif self.dir_x[num] == 1:
                self.x[num] -= Item.RUN_SPEED_PPS * frame_time

            if self.dir_y[num] == 0:
                self.y[num] += Item.RUN_SPEED_PPS * frame_time
            elif self.dir_y[num] == 1:
                self.y[num] -= Item.RUN_SPEED_PPS * frame_time



    def get_bb(self, num, type):
        return self.x[num] - 20, self.y[num] - 13, self.x[num] + 20 , self.y[num] + 13

    def draw_bb(self):
        for num in range(ITEM_MAX):
            draw_rectangle(*self.get_bb(num ,0))