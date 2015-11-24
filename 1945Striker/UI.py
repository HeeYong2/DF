__author__ = 'HeeYong'

from pico2d import *

class Credit:                                               #오른쪽 아래 Credit
    def __init__(self):
        self.x , self.y = 440 , 53
        self.image = load_image('Stage/UI/Credit.png')

    def draw(self , frame_time):
        self.image.draw(self.x , self.y)

class StageOneUI:                                               #오른쪽 아래 Credit
    StageOneImage = None
    def __init__(self):
        self.x , self.y = 150 , 610
        self.StageOneImage = load_image('Stage/UI/Status_Top.png')

    def draw(self , frame_time):
        self.StageOneImage.clip_draw(200, 195, 280, 70, self.x, self.y)

class LifeUI:                                               #오른쪽 아래 Credit
    LifeImage = None
    def __init__(self):
        self.x , self.y = 80 , 630
        self.LifeImage = load_image('Stage/UI/Status_Top.png')

    def draw(self , frame_time):
        self.LifeImage.clip_draw(0, 195, 96, 100, self.x, self.y)

class PowerUI:                                               #왼쪽 아래 Credit
    PowerBarImage = None
    def __init__(self):
        self.x , self.y = 160 , 60
        self.PowerBarImage = load_image('Stage/UI/Power_bar1.png')

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
            self.pushimage = load_image('Stage/UI/Status_Top.png')

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