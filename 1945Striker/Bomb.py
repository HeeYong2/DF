from pico2d import*

class Bomb:
    PIXEL_PER_METER = (10.0 / 0.2)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.95
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION_BOMB = 8
    HERO_BOMB_SPEED = 2

    image = None

    def __init__(self):
        self.x = -100
        self.y = -100
        self.frame = 0
        self.totalframe = 0
        self.use_flag = 0

        if Bomb.image == None:
            Bomb.image = load_image('Stage/Bomb/bomb_ani.png')

    def update(self, frame_time):
        if self.use_flag == 1:
            self.totalframe += Bomb.FRAMES_PER_ACTION_BOMB * Bomb.ACTION_PER_TIME * frame_time
            self.frame = int(self.totalframe)
            if self.frame >= 7:
                self.frame = 7
            self.y += Bomb.RUN_SPEED_PPS * frame_time * Bomb.HERO_BOMB_SPEED

        self.destroy_bomb()

    def draw(self, frame_time):
        self.image.clip_draw(self.frame * 192, 0, 192, 272, self.x, self.y)
        self.draw_bb()

    def create_bomb(self, x, y):
        if self.use_flag == 0:
            self.use_flag = 1
            self.totalframe = 0
            self.x = x
            self.y = y

    def destroy_bomb(self):
        if self.use_flag == 1:
            if self.y > 1000:
                self.use_flag = 0

    def get_use_flag(self):
        return self.use_flag

    def get_bb(self, num, type):
        return self.x - 96, self.y - 136, self.x + 96 , self.y + 96

    def draw_bb(self):
        draw_rectangle(*self.get_bb(0,0))