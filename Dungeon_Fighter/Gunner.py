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

class Gunner():
    BulletUp , BulletDown = 0 , 1
    BulletDirection = None
    BulletCnt = 0
    ShotMotionCnt = 0
    ShotMotion = False
    imageright = None
    imageleft = None

    RIGHT_STAND1 , RIGHT_SHOT , RIGHT_DOUBLE_SHOT , RIGHT_DOWN_SHOT , RIGHT_WALK , RIGHT_JUMP1 , RIGHT_JUMP\
        , RIGHT_WALK_SHOT , RIGHT_SLIDING , RIGHT_DAMAGE , RIGHT_POWERGUN\
        ,RIGHTUP_POWERGUN , RIGHT_KICK , RIGHT_WHEEL_SHOT , RIGHT_TURN_SHOT , RIGHT_TEMP\
        = 31 , 30 , 29 , 28 , 27 , 26 , 25 , 24 , 23 , 22 , 21 , 20 , 19 , 18 , 17 , 16

    LEFT_STAND1 , LEFT_SHOT , LEFT_DOUBLE_SHOT , LEFT_DOWN_SHOT , LEFT_WALK , LEFT_JUMP1 , LEFT_JUMP\
        , LEFT_WALK_SHOT , LEFT_SLIDING , LEFT_DAMAGE , LEFT_POWERGUN\
        ,LEFTUP_POWERGUN , LEFT_KICK , LEFT_WHEEL_SHOT , LEFT_TURN_SHOT , LEFT_TEMP\
        = 15 , 14 , 13 , 12 , 11 , 10 , 9 , 8 , 7 , 6 , 5 , 4 , 3 , 2 , 1 , 0
    DIR_RIGHT , DIR_LEFT , DIR_UP , DIR_DOWN , DIR_RUP , DIR_RDOWN , DIR_LUP , DIR_LDOWN = 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8

    Upgoing = False
    DownGoing = False
    LeftGoing = False
    RightGoing = False
    LookRight = False
    LookLeft = False
    LookUp = False
    LookDown = False

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.endframe = 12     #프레임 끝 위치가 달라서 끝 프레임을 넣음
        self.startframe = 0    #프레임 시작위치가 달라서 시작 프레임을 넣음
        self.FinalFrame = 0    #마지막 스프라이트는 이것으롣 돌린다
        self.ModuleFrame = 0   #돌려아 하는 스프라이트가 달라서 나눔
        self.state = self.RIGHT_STAND1
        self.direction = self.DIR_RIGHT
        self.speed = 15
        self.FrameSpeed = 0.08
        self.BulletCnt = 0
        if Gunner.imageright == None:
            Gunner.imageright = load_image('Player/Player.png')

    def BulletShoot(self):
        self.BulletCnt += 1
        if self.BulletCnt == 1:
            self.BulletDirection = self.BulletUp
        else:
            self.BulletDirection = self.BulletDown

        if self.BulletCnt == 2:
            self.BulletCnt = 0

        if (self.state == self.RIGHT_SHOT) or (self.state == self.RIGHT_SHOT):
            NewBullet = BulletManager.Bullet(self.x , self.y , self.direction, self.BulletDirection )
            BulletList.append(NewBullet)
            if self.frame > self.endframe - 1:
                self.state = self.LEFT_STAND1

        pass
    #fill here

    def handle_event(self , event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.RightGoing = True
                self.state = self.RIGHT_WALK
                self.direction = self.DIR_RIGHT
                print("오른키 눌림")

            elif event.key == SDLK_LEFT:
                self.LeftGoing = True
                self.state = self.LEFT_WALK
                self.direction = self.DIR_LEFT
                print("왼키 눌림")

            elif event.key == SDLK_UP:
                self.Upgoing = True
                self.state = self.RIGHT_WALK
                self.direction = self.DIR_RIGHT
                print("위키 눌림")

            elif event.key == SDLK_DOWN:
                self.DownGoing = True
                print("아래키 눌림")

            elif event.key == SDLK_x:
                print("x키 누름")

                self.ShotMotionCnt += 1
                if self.ShotMotionCnt < 5:
                    print(self.ShotMotionCnt)
                    self.ShotMotion = True
                    self.startframe = 10
                    self.startframe = 12
                elif self.ShotMotionCnt == 5:
                    self.ShotMotionCnt = 0
                    print(self.ShotMotionCnt)
                    self.startframe = 0
                    self.startframe = 1
                if self.direction == self.DIR_RIGHT:
                    self.state = self.RIGHT_SHOT
                elif self.direction == self.DIR_LEFT:
                    self.state = self.LEFT_SHOT
                self.BulletShoot()
###############################Key UP#######################################
        if event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                self.RightGoing = False
                if self.state == self.RIGHT_WALK:
                    self.state = self.RIGHT_STAND1
            elif event.key == SDLK_LEFT:
                self.LeftGoing = False
                if self.state == self.LEFT_WALK:
                    self.state = self.LEFT_STAND1

            if event.key == SDLK_UP:
                self.UpGoing = False
                if self.state == self.RIGHT_WALK:
                    self.state = self.RIGHT_STAND1

            elif event.key == SDLK_DOWN:
                self.DownGoing = False
                if self.state == self.RIGHT_WALK:
                    self.state = self.RIGHT_STAND1

###############################Key Check#######################################

    def update(self):
        if self.state == self.RIGHT_WALK or self.state == self.LEFT_WALK:
            self.startframe = 3
            self.endframe = 10

        elif self.state == self.RIGHT_STAND1 or self.state == self.LEFT_STAND1:
            self.startframe = 0
            self.endframe = 12

        if self.RightGoing :
            self.x = min(800 , self.x + self.speed)
            print("오른 걷기")
        elif self.LeftGoing:
            self.x = max(0 , self.x - self.speed)
            print("왼 걷기")
        if self.Upgoing == True :
            self.y = min(600 , self.y + self.speed)
            print("윗 걷기")
        elif self.DownGoing == True and self.state == self.RIGHT_WALK:
            self.y = max(0 , self.y - self.speed)
            print("아랫 걷기")

        if self.state == self.RIGHT_SHOT or self.state == self.LEFT_SHOT:
            pass
            # if self.ShotMotion == True:
            #     self.ModuleFrame = self.endframe - self.startframe
            #     self.frame = (self.frame + 1) % 1
            #     self.FinalFrame = self.frame + self.startframe  #프레임을 시작위치로 이동후 연산
            #     print("durl emfdjdha")
            # else:
            #     self.state += 1
            #     self.ModuleFrame = self.endframe - self.startframe
            #     self.frame = (self.frame + 1) % 2
            #     self.FinalFrame = self.frame + self.startframe  #프레임을 시작위치로 이동후 연산
            #     self.ShotMotion = False
            #     print("여기 들어옴")

        else:
            self.ModuleFrame = self.endframe - self.startframe
            self.frame = (self.frame + 1) % self.ModuleFrame
            self.FinalFrame = self.frame + self.startframe  #프레임을 시작위치로 이동후 연산

        for member in BulletList:
            member.update()

        pass # fill here

    def draw(self):
        if self.state == self.RIGHT_SHOT or self.state == self.LEFT_SHOT:
            pass
        else:
            self.imageright.clip_draw(self.FinalFrame * 271, self.state * 237, 271, 237, self.x, self.y)
        delay(self.FrameSpeed)

        for member in BulletList:
            member.draw()

    def CheckStageClear(self):
        return self.x