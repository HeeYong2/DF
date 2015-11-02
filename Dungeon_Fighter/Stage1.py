import FrameWork
import Main
from pico2d import *
from Gunner import *

__author__ = 'HeeYong'
image = None
gunner = None
stage1 = None
bullet = None
font = None
def enter():
    global image
    image = load_image("Stage1/reshipon0.bmp")
    pass

def exit():
    global image
    del(image)
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            FrameWork.quit()
        else:
            if (event.type , event.key) == (SDL_KEYDOWN , SDLK_ESCAPE):
                FrameWork.quit()
            elif (event.type , event.key) == (SDL_KEYDOWN , SDLK_SPACE):
                FrameWork.change_state(Main)
    pass


def draw():
    clear_canvas()
    image.draw(1600 , 600)
    update_canvas()
    pass

def update():
    pass

def pause():
    pass

def resume():
    pass