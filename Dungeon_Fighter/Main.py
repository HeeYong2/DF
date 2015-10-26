import random
import json
import os

from pico2d import *
import FrameWork
import Title
#import Stage1

name = "MainState"

gunner = None
lobby = None
bullet = None
font = None
global Move
Move = False
BulletList = []
class Lobby:
    def __init__(self):
        self.image = load_image('Home.bmp')

    def draw(self):
        self.image.draw(400, 300)

class Gunner:
    image = None #이미지를 배열로 해서 만들면 LEFT RIGHT다 할 수 있지 않을까image[2]이렇게
    STAND1 , RIGHT_SHOT , DOUBLE_SHOT , RIGHT_DOWN_SHOT , WALK , RIGHT_JUMP1 , RIGHT_JUMP\
        , RIGHT_SPEED_SHOT , RIGHT_SLIDING , RIGHT_DAMAGE , RIGHT_POWERGUN\
        ,RIGHTUP_POWERGUN , RIGHT_KICK , RIGHT_WHEEL_SHOT , RIGHT_TURN_SHOT\
        = 15 , 14 , 13 , 12 , 11 , 10 , 9 , 8 , 7 , 6 , 5 , 4 , 3 , 2 , 1
    #생각으로는 그냥 RIGHT_RUN같은거 말고 WALK, RUN이런거로 구분해서 그 안에서 나누는 것으로 하는 것이 나을 수도
    DIR_RIGHT , DIR_LEFT , DIR_UP , DIR_DOWN , DIR_RUP , DIR_RDOWN , DIR_LUP , DIR_LDOWN = 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8

    def handle_stand1(self):
        """
        if self.state == self.STAND1:
            if self.direction == self.DIR_RIGHT:
                self.x = min(800 , self.x + self.speed)
            elif self.direction == self.DIR_LEFT:
                self.x = max(0 , self.x - self.speed)
                """
        pass # fill here

    def handle_walk(self):    #handle_up_walk를 추가하면 될 거 같다. 4방향이 일단 있어야 될거 같다
        #if self.state == self.WALK:
        if self.direction == self.DIR_RIGHT:
            self.x = min(800 , self.x + self.speed)
        elif self.direction == self.DIR_LEFT:
            self.x = max(0 , self.x - self.speed)
        if self.direction == self.DIR_UP:
            self.y = min(600 , self.y + self.speed)
        elif self.direction == self.DIR_DOWN:
            self.y = max(0 , self.y - self.speed)
        pass
    def BulletShoot(self):
        if self.state == self.DOUBLE_SHOT:
            if self.ModuleFrame <= self.frame + 1:
                self.startframe = 0
                self.endframe = 11
                self.state = self.STAND1
                NewBullet = Bullet(self.x , self.y)
                BulletList.append(NewBullet)

        pass
    #fill here
    handle_state = {
        WALK : handle_walk,
        STAND1 : handle_stand1,
        DOUBLE_SHOT : BulletShoot,
        #RIGHT_STAND1 : handle_right,
        #RIGHT_SHOT : handle_shot,
        #RIGHT_DOUBLE_SHOT : handle_double_shot,
    }

    def update(self):
        #if self.x >= 800:
        #    FrameWork.change_state(Stage1)
        self.ModuleFrame = self.endframe - self.startframe
        self.frame = (self.frame + 1) % self.ModuleFrame
        self.FinalFrame = self.frame + self.startframe  #프레임을 시작위치로 이동후 연산
        self.handle_state[self.state](self)
        pass # fill here

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = random.randint(0, 13)
        self.endframe = 11     #프레임 끝 위치가 달라서 끝 프레임을 넣음
        self.startframe = 0    #프레임 시작위치가 달라서 시작 프레임을 넣음
        self.FinalFrame = 0    #마지막 스프라이트는 이것으롣 돌린다
        self.ModuleFrame = 0   #돌려아 하는 스프라이트가 달라서 나눔
        self.state = self.STAND1
        self.direction = self.DIR_RIGHT
        self.speed = 15
        self.FrameSpeed = 0.08
        if Gunner.image == None:
            Gunner.image = load_image('Player/RPlayer.png')
        #Gunner.image[1] = load_image('Player/LPlayer.png')

    def draw(self):
        self.image.clip_draw(self.FinalFrame * 271, self.state * 237, 271, 237, self.x, self.y)
        delay(self.FrameSpeed)

class Bullet:
    def __init__(self , x , y):
        self.image = load_image("BasicAttack/BulletRight.bmp")
        #self.frame = 0
        self.x,self.y = x , y
        self.bulletspeed = 20
        #self.direction = gunner.direction
    def update(self):
         #self.frame = (self.frame + 1) % 5
         #if self.direction == 2:
        self.x += self.bulletspeed
        if self.x < 0 or self.x > 800:
            del BulletList[0]
         #elif self.direction == 1:
           # self.x += 20

    def draw(self):
        #self.image.clip_draw(self.frame * 80, 0, 80, 80, self.x, self.y)
        self.image.draw(self.x + 100 , self.y)



def enter():
    global  gunner , lobby , BulletList
    gunner = Gunner()
    lobby = Lobby()
    BulletList = []
    pass

def exit():
    global gunner , lobby , bullet
    del(gunner)
    del(lobby)
#   del(bullet)
    pass

def pause():
    pass

def resume():
    pass

def handle_events():
    global gunner , bullet , Move
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            FrameWork.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            FrameWork.change_state(Title)
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                gunner.state = gunner.WALK
                gunner.direction = gunner.DIR_RIGHT
                gunner.startframe = 3
                gunner.endframe = 10
            if event.key == SDLK_LEFT:
                gunner.state = gunner.WALK
                gunner.direction = gunner.DIR_LEFT
                gunner.startframe = 3
                gunner.endframe = 10
            if event.key == SDLK_UP:
                gunner.state = gunner.WALK
                gunner.direction = gunner.DIR_UP
                gunner.startframe = 3
                gunner.endframe = 10
            if event.key == SDLK_DOWN:
                gunner.state = gunner.WALK
                gunner.direction = gunner.DIR_DOWN
                gunner.startframe = 3
                gunner.endframe = 10
            if event.key == SDLK_x:                         #총알발사
                gunner.BulletShoot()
                if gunner.state != gunner.DOUBLE_SHOT:
                    gunner.state = gunner.DOUBLE_SHOT
                    gunner.startframe = 2
                    gunner.endframe = 12

        if event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                if gunner.state == gunner.WALK:
                    gunner.state = gunner.STAND1
            if event.key == SDLK_LEFT:
                if gunner.state == gunner.WALK:
                    gunner.state = gunner.STAND1
            if event.key == SDLK_UP:
                if gunner.state == gunner.WALK:
                    gunner.state = gunner.STAND1
            if event.key == SDLK_DOWN:
                if gunner.state == gunner.WALK:
                    gunner.state = gunner.STAND1
def update():
    gunner.update()
    for member in BulletList:
        member.update()
    pass

def draw():
    clear_canvas()
    lobby.draw()
    gunner.draw()
    for member in BulletList:
        member.draw()
    update_canvas()
    pass