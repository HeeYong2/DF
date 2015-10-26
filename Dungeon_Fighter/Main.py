import random
import json
import os

from pico2d import *
import FrameWork
import Title

name = "MainState"

gunner = None
lobby = None
font = None

#class Bullet:

class Lobby:
    def __init__(self):
        self.image = load_image('Home.bmp')

    def draw(self):
        self.image.draw(400, 300)

class Gunner:
    image = None #이미지를 배열로 해서 만들면 LEFT RIGHT다 할 수 있지 않을까image[2]이렇게
    RIGHT_STAND1 , RIGHT_STAND2 , RIGHT_DOUBLE_SHOT , RIGHT_DOWN_SHOT , RIGHT_WALK , RIGHT_JUMP1 , RIGHT_JUMP\
        , RIGHT_SPEED_SHOT , RIGHT_SLIDING , RIGHT_DAMAGE , RIGHT_POWERGUN\
        ,RIGHTUP_POWERGUN , RIGHT_KICK , RIGHT_WHEEL_SHOT , RIGHT_TURN_SHOT\
        = 15 , 14 , 13 , 12 , 11 , 10 , 9 , 8 , 7 , 6 , 5 , 4 , 3 , 2 , 1
    #생각으로는 그냥 RIGHT_RUN같은거 말고 WALK, RUN이런거로 구분해서 그 안에서 나누는 것으로 하는 것이 나을 수도
    PLAYER_RIGHT , PLAYER_LEFT , PLAYER_UP , PLAYER_DOWN = 0 , 1 , 2 , 3
    """
    def handle_left_run(self):
        self.x -= self.speed
        self.run_frames += 1

        if self.x < 0:
            self.state = self.RIGHT_RUN
            self.x = 0
        if self.run_frames == 100:
            self.state = self.LEFT_STAND
            self.stand_frames = 0

        pass # fill here

    def handle_left_stand(self):
        self.stand_frames += 1
        if self.stand_frames == 50:
            self.state = self.RIGHT_STAND1
            self.run_frames = 0
        pass # fill here


    def handle_right_run(self):
        self.x += self.speed
        self.run_frames += 1

        if self.x > 800:
            self.state = self.LEFT_RUN
            self.x = 800
        if self.run_frames == 100:
            self.state = self.RIGHT_STAND
            self.stand_frames = 0

          pass # fill here
    """

    def handle_right_stand1(self):
        #self.stand_frames += 1
        #if self.stand_frames == 50:
        #self.state = self.RIGHT_WORK
        #self.run_frames = 0
        pass # fill here

    def handle_right_walk(self):    #handle_up_walk를 추가하면 될 거 같다. 4방향이 일단 있어야 될거 같다
        if self.direction == self.PLAYER_RIGHT:
            self.x += self.speed
        elif self.direction == self.PLAYER_UP:
            self.y += self.speed
        elif self.direction == self.PLAYER_DOWN:
            self.y -= self.speed
        elif self.direction == self.PLAYER_LEFT:
            self.x -= self.speed
        pass

    def handle_left(self):
        if self.state == self.PLAYER_LEFT:
            self.x -= self.speed
        pass
    def handle_right(self):
        if self.state == self.RIGHT_WALK:
            self.x += self.speed

        pass
    def handle_up(self):
        pass
    def handle_down(self):
        pass
    #fill here
    handle_state = {
        RIGHT_WALK : handle_right_walk,
        #RIGHT_STAND1 : handle_right_stand1,
        RIGHT_STAND1 : handle_right,
    }

    def update(self):
        self.ModuleFrame = self.endframe - self.startframe
        self.frame = (self.frame + 1) % self.ModuleFrame
        self.FinalFrame = self.frame + self.startframe  #프레임을 시작위치로 이동후 연산
        self.handle_state[self.state](self)
        pass # fill here

    def __init__(self):
        self.x, self.y = random.randint(100, 700), 90
        self.frame = random.randint(0, 13)
        self.endframe = 11     #프레임 끝 위치가 달라서 끝 프레임을 넣음
        self.startframe = 0    #프레임 시작위치가 달라서 시작 프레임을 넣음
        self.FinalFrame = 0    #마지막 스프라이트는 이것으롣 돌린다
        self.ModuleFrame = 0   #돌려아 하는 스프라이트가 달라서 나눔
        self.state = self.RIGHT_STAND1
        self.direction = 0
        self.speed = 15
        Gunner.image = load_image('Player/RPlayer.png')
        #Gunner.image[1] = load_image('Player/LPlayer.png')

    def draw(self):
        self.image.clip_draw(self.FinalFrame * 271, self.state * 237, 271, 237, self.x, self.y)
        delay(0.08)

def enter():
    global  gunner , lobby
    gunner = Gunner()
    lobby = Lobby()
    pass

def exit():
    global gunner , lobby
    del(gunner)
    del(lobby)
    pass

def pause():
    pass

def resume():
    pass

def handle_events():
    global gunner
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            FrameWork.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            FrameWork.change_state(Title)
        elif event.type == SDL_KEYDOWN:                                #키를 눌렀을 때
            if event.key == SDLK_RIGHT:
                if gunner.state != gunner.RIGHT_WALK:
                    gunner.direction = gunner.PLAYER_RIGHT
                    gunner.state = gunner.RIGHT_WALK
                    gunner.endframe = 10
                    gunner.startframe = 3
            elif event.key == SDLK_UP:
                if gunner.state != gunner.RIGHT_WALK:
                    gunner.direction = gunner.PLAYER_UP
                    gunner.state = gunner.RIGHT_WALK
                    gunner.endframe = 10
                    gunner.startframe = 3
            elif event.key == SDLK_DOWN:
                if gunner.state != gunner.RIGHT_WALK:
                    gunner.direction = gunner.PLAYER_DOWN
                    gunner.state = gunner.RIGHT_WALK
                    gunner.endframe = 10
                    gunner.startframe = 3
            elif event.key == SDLK_LEFT:
                if gunner.state != gunner.RIGHT_WALK:
                    gunner.direction = gunner.PLAYER_LEFT
                    gunner.state = gunner.RIGHT_WALK
                    gunner.endframe = 10
                    gunner.startframe = 3
            elif event.key == SDLK_x:
                if gunner.state != gunner.RIGHT_WALK:
                    gunner.direction = gunner.PLAYER_LEFT
                    gunner.state = gunner.RIGHT_WALK
                    gunner.endframe = 23
                    gunner.startframe = 27
        elif event.type == SDL_KEYUP:                       #Key를 떼었을 때
                if event.key == SDLK_RIGHT:
                    if gunner.state != gunner.RIGHT_STAND1:
                        gunner.state = gunner.RIGHT_STAND1
                        gunner.endframe = 11
                        gunner.startframe = 0
                elif event.key == SDLK_UP:
                    if gunner.state != gunner.RIGHT_STAND1:
                        gunner.state = gunner.RIGHT_STAND1
                        gunner.endframe = 11
                        gunner.startframe = 0
                elif event.key == SDLK_DOWN:
                    if gunner.state != gunner.RIGHT_STAND1:
                        gunner.state = gunner.RIGHT_STAND1
                        gunner.endframe = 11
                        gunner.startframe = 0
                elif event.key == SDLK_LEFT:
                    if gunner.state != gunner.RIGHT_STAND1:
                        gunner.state = gunner.RIGHT_STAND1
                        gunner.endframe = 11
                        gunner.startframe = 0
        """
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if gunner.state == gunner.LEFT_RUN:
                gunner.state = gunner.RIGHT_RUN
            elif gunner.state == gunner.RIGHT_RUN:
                gunner.state = gunner.LEFT_RUN
            elif gunner.state == gunner.RIGHT_STAND:
                gunner.state = gunner.RIGHT_RUN
            elif gunner.state == gunner.LEFT_STAND:
                gunner.state = gunner.LEFT_RUN
                """
    pass

def update():
    gunner.update()
    pass

def draw():
    clear_canvas()
    lobby.draw()
    gunner.draw()
    update_canvas()
    pass