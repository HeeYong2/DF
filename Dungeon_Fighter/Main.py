import random
import json
import os

from pico2d import *
import FrameWork
import Title
import Stage1
from Gunner import *
import BulletManager

#import Stage1

name = "MainState"

gunner = None
lobby = None
bullet = None
font = None

class Lobby:
    def __init__(self):
        self.image = load_image('Home.bmp')

    def draw(self):
        self.image.draw(400, 300)

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
    global gunner , Move
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            FrameWork.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            FrameWork.change_state(Title)
        else:
            gunner.handle_event(event)

def update():
    gunner.update()
    #BulletManager.update()
    pass

def draw():
    clear_canvas()
    lobby.draw()
    gunner.draw()
    #    BulletManager.draw()
    update_canvas()
    pass