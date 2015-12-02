from pico2d import*
import random
import time

data_file = open('data.txt', 'r')
data = json.load(data_file)
data_file.close()

ENEMY_MAX = data['Enemy']['ENEMY_MAX']

class Enemy:
    PIXEL_PER_METER = data['Enemy']['PIXEL_PER_METER']           # 10 pixel 30 cm
    RUN_SPEED_KMPH = data['Enemy']['RUN_SPEED_KMPH']                   # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = data['Enemy']['TIME_PER_ACTION']
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = data['Enemy']['FRAMES_PER_ACTION']

    image = [None] * 3
    death_sound = None

    E1_WING, E1_BODY = data['Enemy']['E1_WING'], data['Enemy']['E1_BODY']
    E2_WING, E2_BODY = data['Enemy']['E2_WING'], data['Enemy']['E2_BODY']
    E3_WING, E3_BODY = data['Enemy']['E3_WING'], data['Enemy']['E3_BODY']
    E2_ONE, E1_THREE = data['Enemy']['E2_ONE'], data['Enemy']['E1_THREE']

    def __init__(self):
        self.start_respone_time_E1_ONE = time.time()
        self.start_respone_time_E1_THREE = time.time()
        self.start_respone_time_E3_TWO = time.time()
        self.x, self.y = [data['Enemy']['x']] * ENEMY_MAX, [data['Enemy']['y']] * ENEMY_MAX
        self.live_flag = [data['Enemy']['live_flag']] * ENEMY_MAX
        self.hp = [data['Enemy']['hp']] * ENEMY_MAX
        self.enemy_score = data['Enemy']['0']
        self.start_shot_time = [time.time()] * ENEMY_MAX
        self.end_shot_time = [time.time()] * ENEMY_MAX
        self.end_shot_time2 = [time.time()] * ENEMY_MAX
        self.type = [data['Enemy']['type']] * ENEMY_MAX
        self.pattern_type = [data['Enemy']['pattern_type']] * ENEMY_MAX
        self.dir = [None] * ENEMY_MAX

        self.e1_wing_w , self.e1_wing_h = data['Enemy']['e1_wing_w'], data['Enemy']['e1_wing_h']
        self.e1_body_w, self.e1_body_h = data['Enemy']['e1_body_w'], data['Enemy']['e1_body_h']
        self.e2_wing_w, self.e2_wing_h = data['Enemy']['e2_wing_w'], data['Enemy']['e2_wing_h']
        self.e2_body_w, self.e2_body_h = data['Enemy']['e2_body_w'], data['Enemy']['e2_body_h']
        self.e3_wing_w, self.e3_wing_h = data['Enemy']['e3_wing_w'], data['Enemy']['e3_wing_h']
        self.e3_body_w, self.e3_body_h = data['Enemy']['e3_body_w'], data['Enemy']['e3_body_h']

        if Enemy.image[0] == None:
            Enemy.image[0] = load_image('enemy_1.png')
        if Enemy.image[1] == None:
            Enemy.image[1] = load_image('enemy_2.png')
        if Enemy.image[2] == None:
            Enemy.image[2] = load_image('enemy_3.png')
        if Enemy.death_sound == None:
            Enemy.death_sound = load_wav('death.wav')
            Enemy.death_sound.set_volume(30)

    def update(self, frame_time, missile, effect, item):
        self.end_respone_time = time.time()

        #print("start_respone_time : %d  end_respone_time : %d" %(self.start_respone_time, self.end_respone_time))
        for i in range (0, ENEMY_MAX):
            if self.live_flag[i] == 1 and self.hp[i] > 0:
                #print("start_shot_time : %d  end_shot_time : %d i = %d" %(self.start_shot_time[i], self.end_shot_time[i], i))
                self.end_shot_time[i] = time.time()
                self.end_shot_time2[i] = time.time()

                #enemy speed
                if self.type[i] == data['Enemy']['e1_type']:
                    self.y[i] -= Enemy.RUN_SPEED_PPS * frame_time * data['Enemy']['e1_speed']
                if self.type[i] == data['Enemy']['e2_type']:
                    self.y[i] -= Enemy.RUN_SPEED_PPS * frame_time * data['Enemy']['e2_speed']
                if self.type[i] == data['Enemy']['e3_type']:
                    self.y[i] -= Enemy.RUN_SPEED_PPS * frame_time * data['Enemy']['e3_speed']
                    if self.dir[i] == data['Enemy']['dir_left']:
                        self.x[i] -= Enemy.RUN_SPEED_PPS * frame_time / data['Enemy']['e3_speed']
                    elif self.dir[i] == data['Enemy']['dir_right']:
                        self.x[i] += Enemy.RUN_SPEED_PPS * frame_time / data['Enemy']['e3_speed']
                #enemy missile create
                if self.end_shot_time[i] - self.start_shot_time[i] >= data['Enemy']['missile_respone_time1']:   #1 second
                    if self.pattern_type[i] == self.E2_ONE:
                        missile.create_shot(3,self.x[i], self.y[i])
                        self.start_shot_time[i] = time.time()
                if self.end_shot_time2[i] - self.start_shot_time[i] >= data['Enemy']['missile_respone_time2']: #3 second
                    if self.pattern_type[i] == self.E1_THREE:
                        missile.create_enemy_multyshot(self.x[i], self.y[i])
                        self.start_shot_time[i] = time.time()

            #enemy create
            if self.end_respone_time - self.start_respone_time_E1_ONE >= data['Enemy']['E2_ONE_respone_time']:  #7 second
                self.create_enemy(data['Enemy']['e2_type'])
                self.start_respone_time_E1_ONE = self.end_respone_time
            if self.end_respone_time - self.start_respone_time_E1_THREE >= data['Enemy']['E1_THREE_respone_time']:   #5 second
                self.create_enemy_three(data['Enemy']['e1_type'])
                self.start_respone_time_E1_THREE = self.end_respone_time
            if self.end_respone_time - self.start_respone_time_E3_TWO >= data['Enemy']['E3_TWO_respone_time']: #3 second
                dir_random = random.randint(data['Enemy']['dir_right'],data['Enemy']['dir_left'])
                self.create_diagonal_enemy(data['Enemy']['e3_type'], dir_random)
                self.start_respone_time_E3_TWO = self.end_respone_time

        self.destroy_enemy(effect, item, missile)


    def draw(self, frame_time):
        for i in range (0, ENEMY_MAX):
            if self.live_flag[i] == 0:
                continue
            elif self.hp[i] > 0 :
                if self.type[i] == data['Enemy']['e1_type']:
                    self.image[0].rotate_draw(3.1, self.x[i], self.y[i])
                elif self.type[i] == data['Enemy']['e2_type']:
                    self.image[1].rotate_draw(3.1, self.x[i], self.y[i])
                elif self.type[i] == data['Enemy']['e3_type']:
                    self.image[2].rotate_draw(3.1, self.x[i], self.y[i])
        #self.image.clip_draw(0, 0, 88, 64, self.x, self.y)
        #self.draw_bb()

    def create_enemy(self, type):
            for i in range (0, ENEMY_MAX):
                if self.live_flag[i] == 0:
                    self.live_flag[i] = 1
                    self.x[i] = random.randint(data['Enemy']['respone_interval'], data['BackGround']['w'] - data['Enemy']['respone_interval'])
                    self.y[i] = data['BackGround']['h']
                    self.hp[i] = data['Enemy']['hp']
                    self.pattern_type[i] = self.E2_ONE
                    self.type[i] = type
                    self.start_shot_time[i] = time.time()
                    self.end_shot_time[i] = time.time()
                    self.dir[i] = None
                    break

    def create_diagonal_enemy(self, type, dir):
        for num in range(2):
            for i in range(0, ENEMY_MAX):
                if self.live_flag[i] == 0:
                    self.live_flag[i] = 1
                    if dir == data['Enemy']['dir_left']:
                        self.x[i] = random.randint(data['BackGround']['w']/2, data['BackGround']['w'] - data['Enemy']['respone_interval'])
                    elif dir == data['Enemy']['dir_right']:
                        self.x[i] = random.randint(data['Enemy']['respone_interval'], data['BackGround']['w']/2 )
                    self.y[i] = data['BackGround']['h']+ (data['Enemy']['e3_body_h'] * num)
                    self.hp[i] = data['Enemy']['hp']
                    self.pattern_type[i] = self.E2_ONE
                    self.type[i] = type
                    self.dir[i] = dir
                    self.start_shot_time[i] = time.time()
                    self.end_shot_time[i] = time.time()
                    break

    def create_enemy_three(self, type):
        respone_space = random.randint(data['Enemy']['respone_interval'], data['BackGround']['w'] - data['Enemy']['threeplane_w'])
        for num in range(3):
            for i in range (0, ENEMY_MAX):
                if self.live_flag[i] == 0:
                    self.live_flag[i] = 1
                    self.x[i] = data['Enemy']['plane_w'] * num + respone_space
                    self.y[i] = data['BackGround']['h']
                    self.hp[i] = data['Enemy']['hp']
                    self.pattern_type[i] = self.E1_THREE
                    self.type[i] = type
                    self.dir[i] = None
                    break

    def destroy_enemy(self, effect, item, missile):
        for i in range (0, ENEMY_MAX):
            if self.live_flag[i] == 0:
                continue
            if self.y[i] < data['BackGround']['bottom'] or self.x[i] > data['BackGround']['right'] or self.x[i] < data['BackGround']['left']:
                self.pattern_type[i] = data['Enemy']['pattern_type']
                self.live_flag[i] = data['Enemy']['live_flag']

            if self.hp[i] <= 0:
                self.pattern_type[i] = data['Enemy']['pattern_type']
                self.live_flag[i] = data['Enemy']['live_flag']
                effect.create_effect(1, self.x[i], self.y[i])
                self.enemy_score += data['Enemy']['score']
                if self.type[i] == data['Enemy']['e2_type']:
                    if missile.power < 3:
                        item.create_item(self.x[i], self.y[i])
                self.death_sound.play()


    def get_bb(self, num, type):
        if type == self.E1_WING:
            return self.x[num] - self.e1_wing_w/2, self.y[num] - self.e1_wing_h/2, self.x[num] + self.e1_wing_w/2, self.y[num] + self.e1_wing_h/2
        elif type == self.E1_BODY:
            return self.x[num] - self.e1_body_w/2, self.y[num] - self.e1_body_h/2, self.x[num] + self.e1_body_w/2, self.y[num] + self.e1_body_h/2
        elif type == self.E2_WING:
            return self.x[num] - self.e2_wing_w/2, self.y[num] - self.e2_wing_h/2, self.x[num] + self.e2_wing_w/2, self.y[num] + self.e2_wing_h/2
        elif type == self.E2_BODY:
            return self.x[num] - self.e2_body_w/2, self.y[num] - self.e2_body_h/2, self.x[num] + self.e2_body_w/2, self.y[num] + self.e2_body_h/2
        elif type == self.E3_WING:
            return self.x[num] - self.e3_wing_w/2, self.y[num] - self.e3_wing_h/2, self.x[num] + self.e3_wing_w/2, self.y[num] + self.e3_wing_h/2
        elif type == self.E3_BODY:
            return self.x[num] - self.e3_body_w/2, self.y[num] - self.e3_body_h/2, self.x[num] + self.e3_body_w/2, self.y[num] + self.e3_body_h/2

    def draw_bb(self):
        for num in range(0, ENEMY_MAX):
            if self.live_flag[num] == 0:
                continue
            if self.type[num] == data['Enemy']['e1_type']:
                draw_rectangle(*self.get_bb(num, self.E1_WING))
                draw_rectangle(*self.get_bb(num, self.E1_BODY))
            elif self.type[num] == data['Enemy']['e2_type']:
                draw_rectangle(*self.get_bb(num, self.E2_WING))
                draw_rectangle(*self.get_bb(num, self.E2_BODY))
            elif self.type[num] == data['Enemy']['e3_type']:
                draw_rectangle(*self.get_bb(num, self.E3_WING))
                draw_rectangle(*self.get_bb(num, self.E3_BODY))

