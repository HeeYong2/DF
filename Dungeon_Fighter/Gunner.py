__author__ = 'HeeYong'
import random
import json
import os

from pico2d import *

import FrameWork
import BulletManager

gunner = None
bullet = None
BulletList = []

class Gunner:
    imageright = None #이미지를 배열로 해서 만들면 LEFT RIGHT다 할 수 있지 않을까image[2]이렇게
    imageleft = None
    STAND1 , RIGHT_SHOT , DOUBLE_SHOT , RIGHT_DOWN_SHOT , WALK , RIGHT_JUMP1 , RIGHT_JUMP\
        , RIGHT_SPEED_SHOT , RIGHT_SLIDING , RIGHT_DAMAGE , RIGHT_POWERGUN\
        ,RIGHTUP_POWERGUN , RIGHT_KICK , RIGHT_WHEEL_SHOT , RIGHT_TURN_SHOT\
        = 15 , 14 , 13 , 12 , 11 , 10 , 9 , 8 , 7 , 6 , 5 , 4 , 3 , 2 , 1
    #생각으로는 그냥 RIGHT_RUN같은거 말고 WALK, RUN이런거로 구분해서 그 안에서 나누는 것으로 하는 것이 나을 수도
    DIR_RIGHT , DIR_LEFT , DIR_UP , DIR_DOWN , DIR_RUP , DIR_RDOWN , DIR_LUP , DIR_LDOWN = 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8
    Keys = [False , False , False , False]
    def handle_stand1(self):
        pass # fill here

    def handle_walk(self):    #handle_up_walk를 추가하면 될 거 같다. 4방향이 일단 있어야 될거 같다
        #if self.state == self.WALK:
        pass
    def BulletShoot(self):
        if self.state == self.DOUBLE_SHOT:
            if self.ModuleFrame <= self.frame + 1:
                self.startframe = 0
                self.endframe = 11
                self.state = self.STAND1
                NewBullet = BulletManager.Bullet(self.x , self.y , self.direction)
                BulletList.append(NewBullet)

        pass
    #fill here

    def handle_event(self , event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.Keys[0] = True
                self.state = self.WALK
                self.direction = self.DIR_RIGHT

            elif event.key == SDLK_LEFT:
                self.Keys[1] = True
                self.state = self.WALK
                self.direction = self.DIR_LEFT

            elif event.key == SDLK_UP:
                self.Keys[2] = True
                self.state = self.WALK

            elif event.key == SDLK_DOWN:
                self.Keys[3] = True
                self.state = self.WALK

            elif event.key == SDLK_x:
                self.state = self.DOUBLE_SHOT
                gunner.startframe = 2
                gunner.endframe = 12
                gunner.BulletShoot()

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                self.Keys[0] = False
                if self.state == self.WALK:
                    self.state = self.STAND1

            elif event.key == SDLK_LEFT:
                self.Keys[1] = False
                if self.state == self.WALK:
                    self.state = self.STAND1

            elif event.key == SDLK_UP:
                self.Keys[2] = False
                if self.state == self.WALK:
                    self.state = self.STAND1

            elif event.key == SDLK_DOWN:
                self.Keys[3] = False
                if self.state == self.WALK:
                    self.state = self.STAND1

    def update(self):
        if self.state == self.WALK:
            self.startframe = 3
            self.endframe = 10
        elif self.state == self.STAND1:
            gunner.startframe = 0
            gunner.endframe = 11

        if self.Keys[0]:
            self.x = min(800 , self.x + self.speed)
        elif self.Keys[1]:
            self.x = max(0 , self.x - self.speed)
        if self.Keys[2]:
            self.y = min(600 , self.y + self.speed)
        elif self.Keys[3]:
            self.y = max(0 , self.y - self.speed)

        if self.state == self.DOUBLE_SHOT:
             if self.ModuleFrame <= self.frame + 1:
                self.startframe = 0
                self.endframe = 11
                self.state = self.STAND1
                NewBullet = BulletManager.Bullet(self.x , self.y , self.direction)
                BulletList.append(NewBullet)
        self.ModuleFrame = self.endframe - self.startframe
        self.frame = (self.frame + 1) % self.ModuleFrame
        self.FinalFrame = self.frame + self.startframe  #프레임을 시작위치로 이동후 연산

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
        if Gunner.imageright == None:
            Gunner.imageright = load_image('Player/RPlayer.png')
        if Gunner.imageleft == None:
            Gunner.imageleft = load_image('Player/LPlayer.png')

    def draw(self):
        if self.direction == self.DIR_RIGHT:
            self.imageright.clip_draw(self.FinalFrame * 271, self.state * 237, 271, 237, self.x, self.y)
        elif self.direction == self.DIR_LEFT:
            self.imageleft.clip_draw(self.FinalFrame * 271, self.state * 237, 271, 237, self.x, self.y)
        delay(self.FrameSpeed)