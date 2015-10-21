import random
import json
import os

from pico2d import *
import FrameWork
import Title

name = "MainState"

gunner = None
grass = None
font = None

#class Bullet:

class Grass:
    def __init__(self):
        self.image = load_image('Home.bmp')

    def draw(self):
        self.image.draw(400, 300)

class Gunner:
    image = None
    RIGHT_STAND1 , RIGHT_STAND2 , RIGHT_DOUBLE_SHOT , RIGHT_DOWN_SHOT , RIGHT_JUMP1 , RIGHT_JUMP\
        ,RIGHT_WORK , RIGHT_SPEED_SHOT , RIGHT_SLIDING , RIGHT_DAMAGE , RIGHT_POWERGUN\
        ,RIGHTUP_POWERGUN , RIGHT_KICK , RIGHT_WHEEL_SHOT , RIGHT_TURN_SHOT\
        = 14 , 13 , 12 , 11 , 10 , 9 , 8 , 7 , 6 , 5 , 4 , 3 , 2 , 1 , 0

    def handle_left_run(self):
        self.x -= self.speed
        self.run_frames += 1
        """
        if self.x < 0:
            self.state = self.RIGHT_RUN
            self.x = 0
        if self.run_frames == 100:
            self.state = self.LEFT_STAND
            self.stand_frames = 0
            """
        pass # fill here

    def handle_left_stand(self):
        self.stand_frames += 1
        if self.stand_frames == 50:
            self.state = self.RIGHT_STAND1
            self.run_frames = 0
        pass # fill here

    """
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
        self.stand_frames += 1
        if self.stand_frames == 50:
            self.state = self.RIGHT_WORK
            self.run_frames = 0
        pass # fill here

    def handle_right_walk(self):
        self.stand_frames += 1
        if self.stand_frames == 50:
            self.state = self.RIGHT_WORK
            self.run_frames = 0
        pass
    #fill here
    handle_state = {
        #LEFT_RUN : handle_left_run,
        #RIGHT_RUN : handle_right_run,
        #LEFT_STAND : handle_left_stand,
        RIGHT_WORK : handle_right_walk,
        RIGHT_STAND1 : handle_right_stand1,
    }

    def update(self):
        self.frame = (self.frame + 1) % self.endframe
        self.FinalFrame = self.frame + self.startframe  #프레임을 시작위치로 이동후 연산
        self.handle_state[self.state](self)
        pass # fill here

    def __init__(self):
        self.x, self.y = random.randint(100, 700), 90
        self.frame = random.randint(0, 7)
        self.run_frames = 0
        self.stand_frames = 0
        self.endframe = 13;     #프레임 끝 위치가 달라서 끝 프레임을 넣음
        self.startframe = 0;    #프레임 시작위치가 달라서 시작 프레임을 넣음
        self.FinalFrame = 0;    #마지막 스프라이트는 이것으롣 돌린다
        self.state = self.RIGHT_STAND1
        self.speed = 0.5
        if Gunner.image == None:
            Gunner.image = load_image('Player/RPlayer.bmp')
            #Gunner.image = load_image('Player/LPlayer.bmp')

    def draw(self):
        self.image.clip_draw(self.FinalFrame * 271, self.state * 237, 271, 237, self.x, self.y)
        delay(0.1)

def enter():
    global  gunner , grass
    gunner = Gunner()
    grass = Grass()
    pass

def exit():
    global gunner , grass
    del(gunner)
    del(grass)
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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            gunner.state == gunner.RIGHT_WORK
            gunner.endframe = 12
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            gunner.state == gunner.RIGHT_STAND1
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
    grass.draw()
    gunner.draw()
    update_canvas()
    pass