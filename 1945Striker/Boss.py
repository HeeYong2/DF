from pico2d import*
import json
import time

data_file = open('data.txt', 'r')
data = json.load(data_file)
data_file.close()


class Boss:
    PIXEL_PER_METER = data['Boss']['PIXEL_PER_METER']          # 10 pixel 30 cm
    RUN_SPEED_KMPH = data['Boss']['RUN_SPEED_KMPH']                  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self):
        self.x = data['Boss']['x']
        self.y = data['Boss']['y']
        self.live_flag = data['Boss']['live_flag']
        self.hp = data['Boss']['hp']
        self.boss_score = data['Boss']['0']
        self.start_time = time.time()
        self.start_udo_shot_time = time.time()
        self.start_multy_shot_time = time.time()

        self.b_wing_w, self.b_wing_h = data['Boss']['b_wing_w'], data['Boss']['b_wing_h']
        self.b_body_w, self.b_body_h = data['Boss']['b_body_w'], data['Boss']['b_body_h']

        if Boss.image == None:
            Boss.image = load_image('Boss.png')


    def update(self, frame_time, missile, score, background):
        self.end_time = time.time()
        if self.end_time - self.start_time >= data['Boss']['boss_respone_time'] and self.live_flag == 0 and self.hp > 0:
            self.create_boss()
            background.bgm.stop()
            background.bgm = load_music('boss_background_sound.mp3')
            background.bgm.set_volume(30)
            background.bgm.repeat_play()


        if self.live_flag == 0:
            return

        elif self.live_flag == 1 and self.hp > 0:
            self.y += Boss.RUN_SPEED_PPS * frame_time

            if self.y >= 550:
                end_udo_shot_time = time.time()
                end_multy_shot_time = time.time()
                self.y = 550
                if end_udo_shot_time - self.start_udo_shot_time > 1:
                    missile.create_boss_udoshot(self.x, self.y)
                    self.start_udo_shot_time = end_udo_shot_time
                elif end_multy_shot_time - self.start_multy_shot_time > 2:
                    missile.create_boss_multyshot(self.x, self.y)
                    missile.create_enemy_multyshot(self.x, self.y - data['Boss']['b_body_h']/2)
                    self.start_multy_shot_time = end_multy_shot_time

        self.destroy_boss()

    def draw(self, frame_time):
        if self.live_flag == 0:
            return
        elif self.live_flag == 1 and self.hp > 0:
            self.image.draw(self.x, self.y)
            #self.draw_bb()

    def create_boss(self):
        if self.live_flag == 0:
            self.x = data['BackGround']['w']/2
            self.y = -data['BackGround']['h']/2
            self.hp = data['Boss']['hp']
            self.live_flag = 1

    def destroy_boss(self):
        if self.live_flag == 0:
            return
        elif self.hp <= 0:
            self.live_flag = 0
            self.hp = 0
            self.boss_score += data['Boss']['score']

    def get_bb(self, num, type):
        if type == data['Boss']['b_wing']:
            return self.x - self.b_wing_w / 2 , self.y - self.b_wing_h / 2, self.x + self.b_wing_w / 2, self.y + self.b_wing_h / 2
        elif type == data['Boss']['b_body']:
            return self.x - self.b_body_w / 2 , self.y - self.b_body_h / 2, self.x + self.b_body_w / 2, self.y + self.b_body_h / 2

    def draw_bb(self):
        draw_rectangle(*self.get_bb(None, data['Boss']['b_wing']))
        draw_rectangle(*self.get_bb(None, data['Boss']['b_body']))