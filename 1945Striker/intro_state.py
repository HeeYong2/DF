import game_framework
import choice_plane_state
from pico2d import *
import json


data_file = open('data.txt', 'r')
data = json.load(data_file)
data_file.close()


name = "IntroState"
image = None
intro_time = 0.0

def enter():
    global image
    open_canvas(data['BackGround']['w'], data['BackGround']['h'])
    image = load_image('intro.png')


def exit():
    global image
    del(image)
    close_canvas()

def update(frame_time):
    global intro_time

    if (intro_time > data['Public']['intro_time']):
        intro_time = 0
        #game_framework.quit()
        game_framework.push_state(choice_plane_state)
    intro_time += frame_time

def draw(frame_time):
    global image
    clear_canvas()
    image.draw(data['BackGround']['w']/2, data['BackGround']['h']/2)
    update_canvas()

def handle_events(frame_time):
    events = get_events()

def pause(): pass
def resume(): pass




