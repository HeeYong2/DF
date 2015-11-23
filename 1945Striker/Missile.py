from pico2d import*

SHOT_MAX = 200

class Missile:
    PIXEL_PER_METER = (10.0 / 0.2)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION_H_SHOT = 2
    FRAMES_PER_ACTION_E_SHOT = 3
    HERO_MISSILE_SPEED = 5

    image = [None] * 2

    H_SHOT, H_L_SHOT, H_R_SHOT, E_SHOT, E_L_SHOT, E_R_SHOT = 0, 1, 2, 3, 4, 5

    def __init__(self):
        self.frame = [0] * SHOT_MAX
        self.totalframe = [0.0] * SHOT_MAX
        self.x = [0] * SHOT_MAX
        self.y= [0] * SHOT_MAX
        self.use_flag = [0] * SHOT_MAX
        self.type = [0] * SHOT_MAX

        self.enemy_missile_w = 14
        self.enemy_missile_h = 14
        self.hero_missile_w = 6
        self.hero_missile_h = 42

        if Missile.image[0] == None:
            Missile.image[0] = load_image('Stage/Bullet/Player_Bullet.png')
        if Missile.image[1] == None:
            Missile.image[1] = load_image('enemy_missile1.png')

    def update(self, frame_time):
        for i in range (0, SHOT_MAX):
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
                self.x[i] -= Missile.RUN_SPEED_PPS * frame_time * Missile.HERO_MISSILE_SPEED / 2
            elif self.type[i] == self.H_R_SHOT and self.use_flag[i] == 1:                                           #hero right shot
                self.totalframe[i] += Missile.FRAMES_PER_ACTION_H_SHOT * Missile.ACTION_PER_TIME * frame_time
                self.frame[i] = int(self.totalframe[i]) % 2
                self.y[i] += Missile.RUN_SPEED_PPS * frame_time * Missile.HERO_MISSILE_SPEED
                self.x[i] += Missile.RUN_SPEED_PPS * frame_time * Missile.HERO_MISSILE_SPEED / 2
            elif self.type[i] == self.E_SHOT and self.use_flag[i] == 1:                                             #enemy middle shot
                self.totalframe[i] += Missile.FRAMES_PER_ACTION_E_SHOT * Missile.ACTION_PER_TIME * frame_time
                self.frame[i] = int(self.totalframe[i]) % 3
                self.y[i] -= Missile.RUN_SPEED_PPS * frame_time
            elif self.type[i] == self.E_L_SHOT and self.use_flag[i] == 1:                                             #enemy left shot
                self.totalframe[i] += Missile.FRAMES_PER_ACTION_E_SHOT * Missile.ACTION_PER_TIME * frame_time
                self.frame[i] = int(self.totalframe[i]) % 3
                self.y[i] -= Missile.RUN_SPEED_PPS * frame_time
                self.x[i] -= Missile.RUN_SPEED_PPS * frame_time / 2
            elif self.type[i] == self.E_R_SHOT and self.use_flag[i] == 1:                                             #enemy right shot
                self.totalframe[i] += Missile.FRAMES_PER_ACTION_E_SHOT * Missile.ACTION_PER_TIME * frame_time
                self.frame[i] = int(self.totalframe[i]) % 3
                self.y[i] -= Missile.RUN_SPEED_PPS * frame_time
                self.x[i] += Missile.RUN_SPEED_PPS * frame_time / 2

        self.destroy_missile()

    def draw(self, frame_time):
        for i in range (0, SHOT_MAX):
            if self.type[i] == self.H_SHOT:
                self.image[0].clip_draw(self.frame[i] * 32, 0, 32, 96, self.x[i], self.y[i])
            elif self.type[i] == self.E_SHOT or self.type[i] == self.E_L_SHOT or self.type[i] == self.E_R_SHOT:
                self.image[1].clip_draw(self.frame[i] * 16, 0, 16, 16, self.x[i], self.y[i])
        self.draw_bb()

    def create_shot(self, type, xDot , yDot ):
        for i in range (0, SHOT_MAX):
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


    def destroy_missile(self):
        for i in range (0, SHOT_MAX):
            if self.use_flag[i] == 1:
                if self.x[i] > 650 or self.x[i] < -100:
                    self.use_flag[i] = 0
                if self.y[i] > 830 or self.y[i] < -100:
                    self.use_flag[i] = 0

    def get_bb(self, num, type):
        if type == self.E_SHOT or type == self.E_L_SHOT or type == self.E_R_SHOT:
            return self.x[num] - self.enemy_missile_w/2, self.y[num] - self.enemy_missile_h/2, self.x[num] + self.enemy_missile_w/2, self.y[num] + self.enemy_missile_h/2
        elif type == self.H_SHOT:
            return self.x[num] - self.hero_missile_w/2, self.y[num] - self.hero_missile_h/2, self.x[num] + self.hero_missile_w/2, self.y[num] + self.hero_missile_h/2

    def draw_bb(self):
        for num in range(0, SHOT_MAX):
            if self.type[num] == self.E_SHOT or self.type[num] == self.E_L_SHOT or self.type[num] == self.E_R_SHOT:
                draw_rectangle(*self.get_bb(num, self.type[num]))
            elif self.type[num] == self.H_SHOT:
                draw_rectangle(*self.get_bb(num, self.type[num]))
