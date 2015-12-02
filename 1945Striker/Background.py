from pico2d import*
import json

data_file = open('data.txt', 'r')
data = json.load(data_file)
data_file.close()

class Background:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    def __init__(self):
        self.image = load_image('background2.png')
        self.x = [data['BackGround']['w']/2] * 3
        self.y = [365, 1095, 1825]
        self.bgm = load_music('background_sound.mp3')
        self.bgm.set_volume(30)
        self.bgm.repeat_play()


    def draw(self, frame_time):
        self.image.draw(data['BackGround']['w']/2 ,data['BackGround']['h']/2)
        for i in range(0, 3):
            self.image.draw(self.x[i], self.y[i])


    def update(self, frame_time):
        for i in range(0, 3):
            self.y[i] -= frame_time * Background.RUN_SPEED_PPS * data['BackGround']['background_speed']
            if self.y[i] <= -data['BackGround']['h']/2:
                self.y[i] = 1825
