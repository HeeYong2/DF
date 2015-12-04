from pico2d import*
import json



data_file = open('data.txt', 'r')
data = json.load(data_file)
data_file.close()

class Hero:
    PIXEL_PER_METER = data['Hero']['PIXEL_PER_METER']             # 10 pixel 30 cm
    RUN_SPEED_KMPH = data['Hero']['RUN_SPEED_KMPH']                   # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = data['Hero']['TIME_PER_ACTION']
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = [data['Hero']['FRAMES_PER_ACTION_HERO'], data['Hero']['FRAMES_PER_ACTION_BOMB1'], data['Hero']['FRAMES_PER_ACTION_BOMB2']]

    image = [None] * data['Hero']['image_num']

    LEFT, RIGHT, IDLE, BOMB1, BOMB2 = data['Hero']['StateLeft'], data['Hero']['StateRight'], data['Hero']['StateIdle'], data['Hero']['StateBomb1'], data['Hero']['StateBomb2']

    def __init__(self):
        self.x, self.y= data['Hero']['x'], data['Hero']['y']
        self.w = data['Hero']['w']
        self.h = data['Hero']['h']
        self.totalframe = [data['Hero']['totalframe1'] , data['Hero']['totalframe2'], data['Hero']['totalframe3']]
        self.frame = [data['Hero']['totalframe1'] , data['Hero']['totalframe2'], data['Hero']['totalframe3']]
        self.state = self.IDLE
        self.up, self.down, self.left, self.right = data['Hero']['up'], data['Hero']['down'], data['Hero']['left'], data['Hero']['right']

        if Hero.image[0] == None:
            Hero.image[0] = load_image('hero_move.png')
        if Hero.image[1] == None:
            Hero.image[1] = load_image('hero_bomb_1.png')
        if Hero.image[2] == None:
            Hero.image[2] = load_image('hero_bomb_2.png')

    def update(self, frame_time, missile):
        self.handle_state[self.state](self, frame_time)
        self.handle_updown(frame_time)

    def draw(self, frame_time):
        if self.state == self.BOMB1:
            self.image[1].clip_draw(self.frame[1] * data['Hero']['image1_w'], 0, data['Hero']['image1_w'], data['Hero']['image1_h'], self.x, self.y)
        elif self.state == self.BOMB2:
            self.image[2].clip_draw(self.frame[2] * data['Hero']['image2_w'], 0, data['Hero']['image2_w'], data['Hero']['image2_h'], self.x, self.y)
        else:
            self.image[0].clip_draw(self.frame[0] * data['Hero']['image0_w'], 0, data['Hero']['image0_w'], data['Hero']['image0_h'], self.x, self.y)

        #self.draw_bb()

    def handle_left(self, frame_time):
        distance = Hero.RUN_SPEED_PPS * frame_time
        self.x -= distance
        self.totalframe[0] -= Hero.FRAMES_PER_ACTION[0] * Hero.ACTION_PER_TIME * frame_time
        self.frame[0] = int(self.totalframe[0])
        if self.totalframe[0] <= 0:
            self.totalframe[0] = 0
        if self.x < data['BackGround']['left']:
            self.x = data['BackGround']['left']

    def handle_right(self, frame_time):
        distance = Hero.RUN_SPEED_PPS * frame_time
        self.x += distance
        self.totalframe[0] += Hero.FRAMES_PER_ACTION[0] * Hero.ACTION_PER_TIME * frame_time
        self.frame[0] = int(self.totalframe[0])
        if self.totalframe[0] >= Hero.FRAMES_PER_ACTION[0] - 1:
            self.totalframe[0] = Hero.FRAMES_PER_ACTION[0] - 1
        if self.x > data['BackGround']['right']:
            self.x = data['BackGround']['right']

    def handle_updown(self, frame_time):
        distance = Hero.RUN_SPEED_PPS * frame_time
        if self.up == True:
            self.y += distance
            if self.y > data['BackGround']['top']:
             self.y = data['BackGround']['top']
        if self.down == True:
            self.y -= distance
            if self.y < data['BackGround']['bottom']:
                self.y = data['BackGround']['bottom']

    def handle_idle(self, frame_time):
        self.frame[0] = data['Hero']['totalframe1']
        self.totalframe[0] = data['Hero']['totalframe1']

    def handle_bomb1(self, frame_time):
        self.totalframe[1] += Hero.FRAMES_PER_ACTION[1] * Hero.ACTION_PER_TIME * frame_time
        self.frame[1] = int(self.totalframe[1])
        if self.frame[1] >= Hero.FRAMES_PER_ACTION[1] - 1:
            self.frame[1] = Hero.FRAMES_PER_ACTION[1] - 1
            self.state = self.BOMB2

    def handle_bomb2(self, frame_time):
        self.totalframe[2] += Hero.FRAMES_PER_ACTION[2] * Hero.ACTION_PER_TIME * frame_time
        self.frame[2] = int(self.totalframe[2])
        if self.frame[2] >= Hero.FRAMES_PER_ACTION[2] - 1:
            self.frame[2] = Hero.FRAMES_PER_ACTION[2] - 1
            self.state = self.IDLE



    def get_bb(self, num, type):
        return self.x - self.w/2, self.y - self.h/2, self.x + self.w/2, self.y + self.h/2

    def draw_bb(self):
        draw_rectangle(*self.get_bb(0,0))

    def handle_event(self, event, missile, bomb):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_x):     #hero missile  = space
            if missile.power == 0:
                missile.create_shot(0, self.x, self.y)
                missile.missile_sound.play()
            elif missile.power == 1:
                missile.create_hero_multyshot(self.x, self.y)
                missile.missile_sound.play()
                missile.missile_sound.play()
            elif missile.power == 2:
                missile.create_hero_multyshot(self.x, self.y)
                missile.missile_sound.play()
                missile.missile_sound.play()
            elif missile.power == 3:
                missile.create_hero_multyshot(self.x, self.y)
                missile.missile_sound.play()
                missile.missile_sound.play()
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):     #hero bomb     = b
                if bomb.get_use_flag() == 0 and bomb.use_number > 0:
                    bomb.create_bomb(self.x, self.y)
                    self.state = self.BOMB1
                    self.totalframe[1] = data['Hero']['totalframe2']
                    self.totalframe[2] = data['Hero']['totalframe3']
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state in (self.RIGHT, self.IDLE, self.LEFT):
                self.state = self.LEFT
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state in (self.LEFT, self.IDLE, self.RIGHT):
                self.state = self.RIGHT
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            self.up = True
            self.down = False
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            self.up = False
            self.down = True
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state in (self.LEFT,):
                self.state = self.IDLE
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state in (self.RIGHT,):
                self.state = self.IDLE
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_UP):
            self.up = False
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
            self.down = False

    handle_state = {
                LEFT : handle_left,
                RIGHT : handle_right,
                IDLE : handle_idle,
                BOMB1 : handle_bomb1,
                BOMB2 : handle_bomb2
    }

