from pico2d import*
import json


data_file = open('data.txt', 'r')
data = json.load(data_file)
data_file.close()

EFFECT_MAX = data['Effect']['EFFECT_MAX']

class Effect:
    TIME_PER_ACTION = data['Effect']['TIME_PER_ACTION']
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION_HIT = data['Effect']['FRAMES_PER_ACTION_HIT']
    FRAMES_PER_ACTION_DEATH = data['Effect']['FRAMES_PER_ACTION_DEATH']

    image = [None] * 2

    def __init__(self):
        self.x = [data['Effect']['x']] * EFFECT_MAX
        self.y = [data['Effect']['y']] * EFFECT_MAX
        self.frame = [data['Effect']['frame']] * EFFECT_MAX
        self.totalframe = [data['Effect']['totalframe']] * EFFECT_MAX
        self.use_flag = [data['Effect']['use_flag']] * EFFECT_MAX
        self.type = [data['Effect']['type']] * EFFECT_MAX

        if Effect.image[0] == None:
            Effect.image[0] = load_image('effect_hit.png')
        if Effect.image[1] == None:
            Effect.image[1] = load_image('effect_death.png')


    def update(self, frame_time):
        for i in range(EFFECT_MAX):
            if self.use_flag[i] == 0:
                continue

            if self.type[i] == 0:
                self.totalframe[i] += Effect.ACTION_PER_TIME * Effect.FRAMES_PER_ACTION_HIT * frame_time
                self.frame[i] = int(self.totalframe[i])
                if self.totalframe[i] >= Effect.FRAMES_PER_ACTION_HIT:
                    self.totalframe[i] = Effect.FRAMES_PER_ACTION_HIT
                    self.destroy_effect(i)

            elif self.type[i] == 1:
                self.totalframe[i] += Effect.ACTION_PER_TIME * Effect.FRAMES_PER_ACTION_DEATH * frame_time
                self.frame[i] = int(self.totalframe[i])
                if self.totalframe[i] >= Effect.FRAMES_PER_ACTION_DEATH:
                    self.totalframe[i] = Effect.FRAMES_PER_ACTION_DEATH
                    self.destroy_effect(i)



    def draw(self, frame_time):
        for i in range(EFFECT_MAX):
            if self.use_flag[i] == 0:
                continue

            if self.type[i] == 0:
                self.image[0].clip_draw(self.frame[i] * data['Effect']['effect_hit_image_w'], 0, data['Effect']['effect_hit_image_w'], data['Effect']['effect_hit_image_h'], self.x[i], self.y[i])  #17
            elif self.type[i] == 1:
                self.image[1].clip_draw(self.frame[i] * data['Effect']['effect_death_image_wh'], 0, data['Effect']['effect_death_image_wh'], data['Effect']['effect_death_image_wh'], self.x[i], self.y[i])  #15


    def create_effect(self, type, xDot, yDot):
        for i in range(EFFECT_MAX):
            if self.use_flag[i] == 0:
                self.x[i] = xDot
                if type == 0:
                    self.y[i] = yDot + data['Effect']['effect_hit_range']
                elif type == 1:
                    self.y[i] = yDot
                self.type[i] = type
                self.use_flag[i] = 1
                self.totalframe[i] = data['Effect']['totalframe']
                self.frame[i] = data['Effect']['frame']
                return

    def destroy_effect(self, i):
        if self.use_flag[i] == 1:
            self.x[i] = data['Effect']['x']
            self.y[i] = data['Effect']['y']
            self.type[i] = data['Effect']['type']
            self.use_flag[i] = data['Effect']['use_flag']
