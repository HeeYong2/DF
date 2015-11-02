__author__ = 'HeeYong'

from pico2d import *
from Gunner import *
from BulletManager import *
gunner = None
bullet = None
effect = None

class BasicEffect:
    image = None
    DIR_RIGHT , DIR_LEFT , DIR_UP , DIR_DOWN , DIR_RUP , DIR_RDOWN , DIR_LUP , DIR_LDOWN = 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8
    def __init__(self):
        print("Init성공")
        self.x , self.y = 400 , 300
        self.frame = 0
        self.direction = self.DIR_RIGHT
        if BasicEffect.image == None:
            self.image = load_image("BasicAttack/BulletBasicLeft.bmp")
            print("Load성공")

    def update(self):
        self.frame = (self.frame + 1) % 5
        print(self.frame)
        print("업데이트 성공")

    def draw(self):
        self.image_clip_draw(self.frame * 80 , 0 , 80 , 35 , self.x , self.y)
        print("렌더 성공")