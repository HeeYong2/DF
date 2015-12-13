import game_framework
from pico2d import *
import json
import SelectCraft

name = "RankingState"
image = [None] * 2
font = None


def enter():
    global image, font
    image[0] = load_image('gameover.png')
    image[1] = load_image('blackboard.png')


def exit():
    global image
    del(image)

def update(frame_time):
    pass






def draw(frame_time):
    global image
    clear_canvas()
    image[1].draw(275 , 365)
    image[0].draw(275 , 340)



    update_canvas()

def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_r):
                game_framework.change_state(SelectCraft)


def pause(): pass
def resume(): pass




