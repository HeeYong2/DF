__author__ = 'HeeYong'

from pico2d import *
from Gunner import *
import AttackEffect
gunner = None
bullet = None
Effect = None
BulletList = []
class Bullet:
    DIR_RIGHT , DIR_LEFT , DIR_UP , DIR_DOWN , DIR_RUP , DIR_RDOWN , DIR_LUP , DIR_LDOWN = 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8
    BulletUp , BulletDown = 0 , 1
    RightDownImage = None
    LeftDownImage = None
    BulletLeft = None
    Bulletdir = None
    def __init__(self , x , y , GunnerDirection , BulletDirection):
        if self.RightDownImage == None:
            self.RightDownImage = load_image("BasicAttack/BulletLowRight.bmp")
        if self.LeftDownImage == None:
            self.RightDownImage = load_image("BasicAttack/BulletLowLeft.bmp")
        if self.BulletLeft == None:
            self.BulletLeft = load_image("BasicAttack/BulletLeft.png")
        AttackEffect.BasicEffect()
       # BulletInfo = x , y , direction
        #BulletList.append(BulletInfo)
        self.x,self.y = x , y
        self.Direction = GunnerDirection
        self.Bulletspeed = 20
        self.Bulletdir = BulletDirection
        print("총알 생성 완료")
    def update(self):
        global BulletList
        if self.DIR_RIGHT == self.Direction and self.Bulletdir == self.BulletUp:
            self.x += self.Bulletspeed
            self.y += self.Bulletspeed
        elif self. DIR_RIGHT == self.Direction and self.Bulletdir == self.BulletDown:
            self.x += self.Bulletspeed
            self.y -= self.Bulletspeed
        elif self.DIR_LEFT == self.Direction and self.Bulletdir == self.BulletDown:
            self.x -= self.Bulletspeed
            self.y -= self.Bulletspeed
        elif self.DIR_LEFT == self.Direction and self.Bulletdir == self.BulletUp:
            self.x -= self.Bulletspeed
            self.y += self.Bulletspeed
        #for member in BulletList:
        #    member.update()


         #elif self.direction == 1:
           # self.x += 20

    def draw(self):
        global BulletList
        #self.image.clip_draw(self.frame * 80, 0, 80, 80, self.x, self.y)
        if self.DIR_RIGHT == self.Bulletdir:
            self.BulletLeft.draw(self.x + 100 , self.y)
        elif self.DIR_LEFT == self.Bulletdir:
            self.BulletLeft.draw(self.x - 100 , self.y)

        #for member in BulletList:
        #    member.draw()

    def CheckRemove(self):
        pass
