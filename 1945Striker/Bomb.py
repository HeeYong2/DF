from pico2d import*
import json


data_file = open('data.txt', 'r')
data = json.load(data_file)
data_file.close()

class Bomb:
    PIXEL_PER_METER = data['Bomb']['PIXEL_PER_METER']          # 10 pixel 30 cm
    RUN_SPEED_KMPH = data['Bomb']['RUN_SPEED_KMPH']                   # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = data['Bomb']['TIME_PER_ACTION']
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION_BOMB = data['Bomb']['FRAMES_PER_ACTION_BOMB']
    HERO_BOMB_SPEED = data['Bomb']['HERO_BOMB_SPEED']

    image = None
    bomb_sound = None

    def __init__(self):
        self.x = data['Bomb']['x']
        self.y = data['Bomb']['y']
        self.frame = data['Bomb']['frame']
        self.totalframe = data['Bomb']['totalframe']
        self.use_flag = data['Bomb']['use_flag']
        self.use_number = data['Bomb']['use_number']
        self.bomb_power = data['Bomb']['power']
        self.check_damage = False

        if Bomb.image == None:
            Bomb.image = load_image('bomb_ani.png')
        if Bomb.bomb_sound == None:
            Bomb.bomb_sound = load_wav('bomb_sound.wav')
            Bomb.bomb_sound.set_volume(60)

    def update(self, frame_time):
        if self.use_flag == 1:
            self.totalframe += Bomb.FRAMES_PER_ACTION_BOMB * Bomb.ACTION_PER_TIME * frame_time
            self.frame = int(self.totalframe)
            if self.frame >= Bomb.FRAMES_PER_ACTION_BOMB - 1:
                self.frame = Bomb.FRAMES_PER_ACTION_BOMB - 1
            self.y += Bomb.RUN_SPEED_PPS * frame_time * Bomb.HERO_BOMB_SPEED

        self.destroy_bomb()

    def draw(self, frame_time):
        if self.use_flag == 0:
            return
        self.image.clip_draw(self.frame * data['Bomb']['bomb_image_w'], 0, data['Bomb']['bomb_image_w'], data['Bomb']['bomb_image_h'], self.x, self.y)
        #self.draw_bb()

    def create_bomb(self, x, y):
        if self.use_flag == 0:
            self.use_flag = 1
            self.totalframe = data['Bomb']['totalframe']
            self.x = x
            self.y = y
            self.use_number -= 1
            self.check_damage = False
            Bomb.bomb_sound.play()

    def destroy_bomb(self):
        if self.use_flag == 1:
            if self.y > data['BackGround']['top'] + data['Bomb']['bomb_image_h'] / 2:
                self.use_flag = 0

    def get_use_flag(self):
        return self.use_flag

    def get_bb(self, num, type):
        return self.x - data['Bomb']['bomb_image_w']/2, self.y - data['Bomb']['bomb_image_h']/2, self.x + data['Bomb']['bomb_image_w']/2 , self.y + data['Bomb']['bomb_image_h']/2

    def draw_bb(self):
        draw_rectangle(*self.get_bb(0,0))