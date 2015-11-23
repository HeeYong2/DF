from pico2d import*

class Background:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    def __init__(self):
        self.image = load_image('background2.png')
        self.x = [275] * 3
        self.y = [365, 1095, 1825]

    def draw(self, frame_time):
        self.image.draw(275,365)
        for i in range(0, 3):
            self.image.draw(self.x[i], self.y[i])


    def update(self, frame_time):
        for i in range(0, 3):
            self.y[i] -= frame_time * Background.RUN_SPEED_PPS
            if self.y[i] <= -365:
                self.y[i] = 1825
