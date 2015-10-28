__author__ = 'HeeYong'

from pico2d import *

gunner = None
bullet = None

BulletList = []

class Bullet:
    DIR_RIGHT , DIR_LEFT , DIR_UP , DIR_DOWN , DIR_RUP , DIR_RDOWN , DIR_LUP , DIR_LDOWN = 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8
    def __init__(self , x , y , direction):
        self.image = load_image("BasicAttack/BulletLeft.png")
        #self.frame = 0
        self.x,self.y = x , y
        self.direction = direction
        self.bulletspeed = 20
        #self.direction = gunner.direction
    def update(self):
        if self.DIR_RIGHT == self.direction:
            self.x += self.bulletspeed
        elif self.DIR_LEFT == self.direction:
            self.x -= self.bulletspeed
        if (self.x < 0 or self.x > 800)\
                or self.y > 600 or self.y < 0:
            del BulletList[0]
         #elif self.direction == 1:
           # self.x += 20

    def draw(self):
        #self.image.clip_draw(self.frame * 80, 0, 80, 80, self.x, self.y)
        if self.DIR_RIGHT == self.direction:
            self.image.draw(self.x + 100 , self.y)
        elif self.DIR_LEFT == self.direction:
            self.image.draw(self.x - 100 , self.y)