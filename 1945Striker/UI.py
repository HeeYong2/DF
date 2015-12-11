__author__ = 'HeeYong'

from pico2d import *

class StageOneUI:                                               #오른쪽 아래 Credit
    pass


class LifeUI:                                               #오른쪽 아래 Credit
    pass


class PowerUI:                                               #왼쪽 아래 Credit
    PowerBarImage = None
    def __init__(self):
        self.x , self.y = 160 , 40
        self.PowerBarImage = load_image('Power_bar1.png')

    def draw(self , frame_time):
        self.PowerBarImage.draw(self.x , self.y)

    # def update(self , frame_time):
    #     pass

class PushStart:                                            #오른쪽 위 푸쉬 스테이트
    pushimage = None
    pushCnt = 0
    YHeight = 210
    def __init__(self):
        self.x , self.y = 400 , 630
        self.frame = 5
        self.state = 0
        if PushStart.pushimage == None:
            self.pushimage = load_image('Status_Top.png')

    def update(self, frame_time):
        self.pushCnt += 1
        if self.pushCnt < 70 and self.pushCnt >= 0:
            self.YHeight = 210
        if self.pushCnt <= 140 and self.pushCnt >= 70:
            self.YHeight = 110
        if self.pushCnt > 140:
            self.pushCnt = 0


    def draw(self , frame_time):
        self.pushimage.clip_draw(500, self.YHeight, 280, 70, self.x, self.y)

class AnyWay:
    pass