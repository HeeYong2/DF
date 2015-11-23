import game_framework
import SelectCraft
from pico2d import *

name = "IntroState"
image = None
intro_time = 0.0

def enter():
    global image
    open_canvas(550, 730)
    image = load_image('intro.png')


def exit():
    global image
    del(image)
    close_canvas()

def update(frame_time):
    global intro_time

    if (intro_time > 2.0):
        intro_time = 0
        #game_framework.quit()
        game_framework.push_state(SelectCraft)
    intro_time += frame_time

def draw(frame_time):
    global image
    clear_canvas()
    image.draw(275, 365)
    update_canvas()

def handle_events(frame_time):
    events = get_events()

def pause(): pass
def resume(): pass




