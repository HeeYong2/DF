from pico2d import*
import random
import time

ENEMY_MAX = 50

class Enemy:
    PIXEL_PER_METER = (10.0 / 0.8)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    image = None

    E1_WING, E1_BODY = 0, 1
    E1_ONE, E1_THREE = 0, 1

    def __init__(self):
        self.start_respone_time_E1_ONE = time.time()
        self.start_respone_time_E1_THREE = time.time()
        self.x, self.y = [900] * ENEMY_MAX, [900] * ENEMY_MAX
        self.live_flag = [0] * ENEMY_MAX
        self.start_shot_time = [time.time()] * ENEMY_MAX
        self.end_shot_time = [time.time()] * ENEMY_MAX
        self.type = None
        self.patter_type = [0] * ENEMY_MAX

        self.e1_wing_w , self.e1_wing_h = 80, 14
        self.e1_body_w, self.e1_body_h = 16, 62

        if Enemy.image == None:
            Enemy.image = load_image('Stage/Monster/enemy_1.png')

    def update(self, frame_time, missile):
        self.end_respone_time = time.time()
        #print("start_respone_time : %d  end_respone_time : %d" %(self.start_respone_time, self.end_respone_time))
        for i in range (0, ENEMY_MAX):

            if self.live_flag[i] == 1:
                #print("start_shot_time : %d  end_shot_time : %d i = %d" %(self.start_shot_time[i], self.end_shot_time[i], i))
                self.y[i] -= Enemy.RUN_SPEED_PPS * frame_time
                self.end_shot_time[i] = time.time()
                if self.end_shot_time[i] - self.start_shot_time[i] >=3:
                    if self.patter_type[i] == self.E1_ONE:
                        missile.create_shot(3,self.x[i], self.y[i])
                    elif self.patter_type[i] == self.E1_THREE:
                        missile.create_enemy_multyshot(self.x[i], self.y[i])
                    self.start_shot_time[i] = time.time()

            if self.end_respone_time - self.start_respone_time_E1_ONE >= 3:
                self.create_enemy()
                self.start_respone_time_E1_ONE = self.end_respone_time

            if self.end_respone_time - self.start_respone_time_E1_THREE >= 5:
                self.create_enemy_three()
                self.start_respone_time_E1_THREE = self.end_respone_time

    def draw(self, frame_time):
        for i in range (0, ENEMY_MAX):
            self.image.rotate_draw(3.1, self.x[i], self.y[i])
        #self.image.clip_draw(0, 0, 88, 64, self.x, self.y)
        self.draw_bb()

    def create_enemy(self):
        for i in range (0, ENEMY_MAX):
            if self.live_flag[i] == 0:
                self.live_flag[i] = 1
                self.x[i] = random.randint(50, 500)
                self.y[i] = 730
                self.patter_type[i] = self.E1_ONE
                break

    def create_enemy_three(self):
        for num in range(3):
            for i in range (0, ENEMY_MAX):
                if self.live_flag[i] == 0:
                    self.live_flag[i] = 1
                    self.x[i] = 80*num + 20
                    self.y[i] = 730
                    self.patter_type[i] = self.E1_THREE
                    break

    def get_bb(self, num, type):
        if type == self.E1_WING:
            return self.x[num] - self.e1_wing_w/2, self.y[num] - self.e1_wing_h/2, self.x[num] + self.e1_wing_w/2, self.y[num] + self.e1_wing_h/2
        elif type == self.E1_BODY:
            return self.x[num] - self.e1_body_w/2, self.y[num] - self.e1_body_h/2, self.x[num] + self.e1_body_w/2, self.y[num] + self.e1_body_h/2

    def draw_bb(self):
        for num in range(0, ENEMY_MAX):
            draw_rectangle(*self.get_bb(num, self.E1_WING))
            draw_rectangle(*self.get_bb(num, self.E1_BODY))
