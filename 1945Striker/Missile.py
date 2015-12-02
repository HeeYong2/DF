from pico2d import*
import json


data_file = open('data.txt', 'r')
data = json.load(data_file)
data_file.close()

MISSILE_MAX = data['Missile']['MISSILE_MAX']

class Missile:
    PIXEL_PER_METER = data['Missile']['PIXEL_PER_METER']         # 10 pixel 30 cm
    RUN_SPEED_KMPH = data['Missile']['RUN_SPEED_KMPH']                      # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = data['Missile']['TIME_PER_ACTION']
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION_H_SHOT = data['Missile']['FRAMES_PER_ACTION_H_SHOT']
    FRAMES_PER_ACTION_E_SHOT = data['Missile']['FRAMES_PER_ACTION_E_SHOT']
    HERO_MISSILE_SPEED = data['Missile']['HERO_MISSILE_SPEED']

    image = [None] * data['Missile']['image_num']
    missile_sound = None

    H_SHOT, H_L_SHOT, H_R_SHOT, E_SHOT, E_L_SHOT, E_R_SHOT, B_UDO_SHOT = 0, 1, 2, 3, 4, 5, 6

    def __init__(self):
        self.x = [data['Missile']['x']] * MISSILE_MAX
        self.y= [data['Missile']['y']] * MISSILE_MAX
        self.frame = [data['Missile']['frame']] * MISSILE_MAX
        self.totalframe = [data['Missile']['totalframe']] * MISSILE_MAX
        self.use_flag = [data['Missile']['use_flag']] * MISSILE_MAX
        self.type = [data['Missile']['type']] * MISSILE_MAX
        self.power = data['Missile']['power']

        self.enemy_missile_w = data['Missile']['enemy_missile_w']
        self.enemy_missile_h = data['Missile']['enemy_missile_h']
        self.hero_missile_w = data['Missile']['hero_missile_w']
        self.hero_missile_h = data['Missile']['hero_missile_h']

        if Missile.image[0] == None:
            Missile.image[0] = load_image('hero_missile1.png')
        if Missile.image[1] == None:
            Missile.image[1] = load_image('hero_missile2.png')
        if Missile.image[2] == None:
            Missile.image[2] = load_image('hero_missile3.png')
        if Missile.image[3] == None:
            Missile.image[3] = load_image('hero_missile4.png')
        if Missile.image[4] == None:
            Missile.image[4] = load_image('enemy_missile1.png')
        if Missile.missile_sound == None:
            Missile.missile_sound = load_wav('missile.wav')
            Missile.missile_sound.set_volume(20)


    def update(self, frame_time, hero):
        for i in range (0, MISSILE_MAX):
            if self.use_flag[i] == 0:
                continue

            if self.type[i] == self.H_SHOT and self.use_flag[i] == 1:                                              #hero middle shot
                self.totalframe[i] += Missile.FRAMES_PER_ACTION_H_SHOT * Missile.ACTION_PER_TIME * frame_time
                self.frame[i] = int(self.totalframe[i]) % 2
                self.y[i] += Missile.RUN_SPEED_PPS * frame_time * Missile.HERO_MISSILE_SPEED
            elif self.type[i] == self.H_L_SHOT and self.use_flag[i] == 1:                                           #hero left shot
                self.totalframe[i] += Missile.FRAMES_PER_ACTION_H_SHOT * Missile.ACTION_PER_TIME * frame_time
                self.frame[i] = int(self.totalframe[i]) % 2
                self.y[i] += Missile.RUN_SPEED_PPS * frame_time * Missile.HERO_MISSILE_SPEED
                self.x[i] -= Missile.RUN_SPEED_PPS * frame_time * Missile.HERO_MISSILE_SPEED / data['Missile']['HERO_X_SPEED']
            elif self.type[i] == self.H_R_SHOT and self.use_flag[i] == 1:                                           #hero right shot
                self.totalframe[i] += Missile.FRAMES_PER_ACTION_H_SHOT * Missile.ACTION_PER_TIME * frame_time
                self.frame[i] = int(self.totalframe[i]) % 2
                self.y[i] += Missile.RUN_SPEED_PPS * frame_time * Missile.HERO_MISSILE_SPEED
                self.x[i] += Missile.RUN_SPEED_PPS * frame_time * Missile.HERO_MISSILE_SPEED / data['Missile']['HERO_X_SPEED']
            elif self.type[i] == self.E_SHOT and self.use_flag[i] == 1:                                             #enemy middle shot
                self.totalframe[i] += Missile.FRAMES_PER_ACTION_E_SHOT * Missile.ACTION_PER_TIME * frame_time
                self.frame[i] = int(self.totalframe[i]) % 3
                self.y[i] -= Missile.RUN_SPEED_PPS * frame_time
            elif self.type[i] == self.E_L_SHOT and self.use_flag[i] == 1:                                             #enemy left shot
                self.totalframe[i] += Missile.FRAMES_PER_ACTION_E_SHOT * Missile.ACTION_PER_TIME * frame_time
                self.frame[i] = int(self.totalframe[i]) % 3
                self.y[i] -= Missile.RUN_SPEED_PPS * frame_time
                self.x[i] -= Missile.RUN_SPEED_PPS * frame_time / data['Missile']['ENEMY_X_SPEED']
            elif self.type[i] == self.E_R_SHOT and self.use_flag[i] == 1:                                             #enemy right shot
                self.totalframe[i] += Missile.FRAMES_PER_ACTION_E_SHOT * Missile.ACTION_PER_TIME * frame_time
                self.frame[i] = int(self.totalframe[i]) % 3
                self.y[i] -= Missile.RUN_SPEED_PPS * frame_time
                self.x[i] += Missile.RUN_SPEED_PPS * frame_time / data['Missile']['ENEMY_X_SPEED']
            elif self.type[i] == self.B_UDO_SHOT and self.use_flag[i] == 1:
                self.totalframe[i] += Missile.FRAMES_PER_ACTION_E_SHOT * Missile.ACTION_PER_TIME * frame_time
                self.frame[i] = int(self.totalframe[i]) % 3
                if hero.x > self.x[i]: self.x[i] += Missile.RUN_SPEED_PPS * frame_time / data['Missile']['UDO_X_SPEED']
                elif hero.x < self.x[i]: self.x[i] -= Missile.RUN_SPEED_PPS * frame_time / data['Missile']['UDO_X_SPEED']
                self.y[i] -= Missile.RUN_SPEED_PPS * frame_time

        self.destroy_missile()

    def draw(self, frame_time):
        for i in range (0, MISSILE_MAX):
            if self.use_flag[i] == 0:
                continue

            for power in range(0, 4):
                if self.type[i] == self.H_SHOT and self.power == power:                                                 #hero h_shot
                    self.image[power].clip_draw(self.frame[i] * data['Missile']['hero_missile_image_w'], 0, data['Missile']['hero_missile_image_w'], data['Missile']['hero_missile_image_h'], self.x[i], self.y[i])
                elif self.type[i] == self.H_L_SHOT and self.power == power:                                         # hero h_l_shot
                    self.image[power - 1].clip_draw(self.frame[i] * data['Missile']['hero_missile_image_w'], 0, data['Missile']['hero_missile_image_w'], data['Missile']['hero_missile_image_h'], self.x[i], self.y[i])
                elif self.type[i] == self.H_R_SHOT and self.power == power:                                              # hero h_r_shot
                    self.image[power - 1].clip_draw(self.frame[i] * data['Missile']['hero_missile_image_w'], 0, data['Missile']['hero_missile_image_w'], data['Missile']['hero_missile_image_h'], self.x[i], self.y[i])

            if self.type[i] == self.E_SHOT or self.type[i] == self.E_L_SHOT or self.type[i] == self.E_R_SHOT or self.type[i] == self.B_UDO_SHOT:
                self.image[4].clip_draw(self.frame[i] * data['Missile']['enemy_missile_image_wh'], 0, data['Missile']['enemy_missile_image_wh'], data['Missile']['enemy_missile_image_wh'], self.x[i], self.y[i])

        #self.draw_bb()

    def create_shot(self, type, xDot , yDot ):
        for i in range (0, MISSILE_MAX):
            if self.use_flag[i] == 0:
                self.use_flag[i] = 1
                self.x[i] = xDot
                self.y[i] = yDot
                self.totalframe[i] = 0
                self.type[i] = type
                break

    def create_enemy_multyshot(self, xDot, yDot):
        for type in range(3, 6):
            self.create_shot(type, xDot, yDot)

    def create_hero_multyshot(self, xDot, yDot):
        for type in range(0, 3):
            self.create_shot(type, xDot, yDot)

    def create_boss_udoshot(self, xDot, yDot):
        self.create_shot(self.B_UDO_SHOT, xDot, yDot)

    def create_boss_multyshot(self, xDot, yDot):
        leftx = xDot - data['Boss']['b_wing1/4']
        rightx = xDot + data['Boss']['b_wing1/4']
        for type in range(3, 6):
            self.create_shot(type, leftx, yDot)
            self.create_shot(type, rightx, yDot)


    def destroy_missile(self):
        for i in range (0, MISSILE_MAX):
            if self.use_flag[i] == 1:
                if self.x[i] > data['BackGround']['right'] or self.x[i] < data['BackGround']['left']:
                    self.use_flag[i] = 0
                if self.y[i] > data['BackGround']['top'] or self.y[i] < data['BackGround']['bottom']:
                    self.use_flag[i] = 0

    def get_bb(self, num, type):
        if type == self.E_SHOT or type == self.E_L_SHOT or type == self.E_R_SHOT or type == self.B_UDO_SHOT:
            return self.x[num] - self.enemy_missile_w/2, self.y[num] - self.enemy_missile_h/2, self.x[num] + self.enemy_missile_w/2, self.y[num] + self.enemy_missile_h/2
        elif type == self.H_SHOT or type == self.H_L_SHOT or type == self.H_R_SHOT:
            return self.x[num] - self.hero_missile_w/2, self.y[num] - self.hero_missile_h/2, self.x[num] + self.hero_missile_w/2, self.y[num] + self.hero_missile_h/2

    def draw_bb(self):
        for num in range(0, MISSILE_MAX):
            if self.use_flag[num] == 0:
                continue

            if self.type[num] == self.E_SHOT or self.type[num] == self.E_L_SHOT or self.type[num] == self.E_R_SHOT or self.type[num] == self.B_UDO_SHOT:
                draw_rectangle(*self.get_bb(num, self.type[num]))
            elif self.type[num] == self.H_SHOT or self.type[num] == self.H_L_SHOT or self.type[num] == self.H_R_SHOT:
                draw_rectangle(*self.get_bb(num, self.type[num]))
