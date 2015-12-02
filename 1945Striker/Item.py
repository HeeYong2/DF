from pico2d import*
import random
import time
import json


data_file = open('data.txt', 'r')
data = json.load(data_file)
data_file.close()

ITEM_MAX = data['Item']['ITEM_MAX']

class Item:
    PIXEL_PER_METER = data['Item']['PIXEL_PER_METER']           # 10 pixel 30 cm
    RUN_SPEED_KMPH = data['Item']['RUN_SPEED_KMPH']                   # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = data['Item']['TIME_PER_ACTION']
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION_ITEM = data['Item']['FRAMES_PER_ACTION_ITEM']
    ITEM_SPEED = data['Item']['ITEM_SPEED']

    image = None

    def __init__(self):
        self.x = [data['Item']['x']] * ITEM_MAX
        self.y = [data['Item']['y']] * ITEM_MAX
        self.frame = [data['Item']['frame']] * ITEM_MAX
        self.totalframe = [data['Item']['totalframe']] * ITEM_MAX
        self.use_flag = [data['Item']['use_flag']] * ITEM_MAX
        self.dir_x = [data['Item']['dir_x']] * ITEM_MAX
        self.dir_y = [data['Item']['dir_y']] * ITEM_MAX
        self.movetime1 = [time.time()] * ITEM_MAX

        if Item.image == None:
            Item.image = load_image('power_item.png')


    def draw(self, frame_time):
        for num in range(ITEM_MAX):
            if self.use_flag[num] == 0:
                continue
            self.image.clip_draw(self.frame[num] * data['Item']['item_image_w'], 0, data['Item']['item_image_w'], data['Item']['item_image_h'], self.x[num], self.y[num])

            #self.draw_bb(num)

    def update(self, frame_time):
        for num in range(ITEM_MAX):
            if self.use_flag[num] == 0:
                continue

            self.item_move(frame_time, num)

            self.totalframe[num] += Item.FRAMES_PER_ACTION_ITEM * Item.ACTION_PER_TIME * frame_time
            self.frame[num] = int(self.totalframe[num]) % Item.FRAMES_PER_ACTION_ITEM


    def create_item(self, x, y):
        for num in range(ITEM_MAX):
            if self.use_flag[num] == 0:
                self.x[num] = x
                self.y[num] = y
                self.use_flag[num] = 1
                return

    def item_move(self, frame_time, num):
        movetime2 = time.time()

        if movetime2 - self.movetime1[num] > data['Item']['item_move_time'] or self.x[num] >= data['BackGround']['right'] or self.x[num] <= data['BackGround']['left'] or self.y[num] >= data['BackGround']['top'] or self.y[num] <= data['BackGround']['bottom']:
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
        return self.x[num] - data['Item']['item_image_w']/2, self.y[num] - data['Item']['item_image_h']/2, self.x[num] + data['Item']['item_image_w']/2 , self.y[num] + data['Item']['item_image_h']/2

    def draw_bb(self, num):
        draw_rectangle(*self.get_bb(num ,0))