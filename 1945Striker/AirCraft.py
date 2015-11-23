from pico2d import*

class AirCraft:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = [7, 23, 24]

    image = [None] * 3

    LEFT, RIGHT, IDLE, BOMB1, BOMB2 = 0, 1, 2, 3, 4

    def __init__(self):
        self.x, self.y= 275, 20
        self.w = 17
        self.h = 62
        self.frame = [3, 0, 0]
        self.state = self.IDLE
        self.up, self.down, self.left, self.right = False, False, False, False

        if AirCraft.image[0] == None:
            AirCraft.image[0] = load_image('hero_move.png')
        if AirCraft.image[1] == None:
            AirCraft.image[1] = load_image('hero_bomb_1.png')
        if AirCraft.image[2] == None:
            AirCraft.image[2] = load_image('hero_bomb_2.png')

    def update(self, frame_time, missile):
        self.handle_state[self.state](self, frame_time)
        self.handle_updown(frame_time)

    def draw(self, frame_time):
        if self.state == self.BOMB1:
            self.image[1].clip_draw(self.frame[1] * 192, 0, 192, 286, self.x, self.y)
        elif self.state == self.BOMB2:
            self.image[2].clip_draw(self.frame[2] * 192, 0, 192, 286, self.x, self.y)
        else:
            self.image[0].clip_draw(self.frame[0] * 62, 0, 62, 80, self.x, self.y)

        self.draw_bb()

    def handle_left(self, frame_time):
        distance = AirCraft.RUN_SPEED_PPS * frame_time
        self.x -= distance
        self.frame[0] -= 1
        if self.frame[0] <= 0:
            self.frame[0] = 0
        if self.x < 0:
            self.x = 0

    def handle_right(self, frame_time):
        distance = AirCraft.RUN_SPEED_PPS * frame_time
        self.x += distance
        self.frame[0] += 1
        if self.frame[0] >= 6:
            self.frame[0] = 6
        if self.x > 550:
            self.x = 550

    def handle_updown(self, frame_time):
        distance = AirCraft.RUN_SPEED_PPS * frame_time
        if self.up == True:
            self.y += distance
            if self.y > 730:
             self.y = 730
        if self.down == True:
            self.y -= distance
            if self.y < 0:
                self.y = 0

    def handle_idle(self, frame_time):
        self.frame[0] = 3

    def handle_bomb1(self, frame_time):
        self.frame[1] += 1
        if self.frame[1] >= 22:
            self.frame[1] = 22
            self.state = self.BOMB2

    def handle_bomb2(self, frame_time):
        self.frame[2] += 1
        if self.frame[2] >= 23:
            self.frame[2] = 23
            self.state = self.IDLE



    def get_bb(self, num, type):
        return self.x - self.w/2, self.y - self.h/2, self.x + self.w/2, self.y + self.h/2

    def draw_bb(self):
        draw_rectangle(*self.get_bb(0,0))

    def handle_event(self, event, missile, bomb):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_x):
                missile.create_shot(0, self.x, self.y)
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):
                if bomb.get_use_flag() == 0:
                    bomb.create_bomb(self.x, self.y)
                    self.state = self.BOMB1
                    self.frame[1] = 0
                    self.frame[2] = 0
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

