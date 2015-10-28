import FrameWork
import Title
from pico2d import *

name = "StartState"
logo_time = 0.0
LogoCnt = 0
def enter():
    global Loading
    open_canvas()
    Loading = []
    for iImage in range(0 , 20):
        Loading.append(load_image("Loading/%d.bmp" % iImage))
    pass

def exit():
    global Loading
    del(Loading)
    close_canvas()
    pass

def update():
    if(LogoCnt == 20):
        delay(1)
        FrameWork.push_state(Title)
    pass

def draw():
    global Loading , LogoCnt
    clear_canvas()
    if(LogoCnt < 20):
        delay(0.05)
        LogoCnt += 1

    for i in range(0 ,LogoCnt):
        Loading[i].draw(400 , 300)
    update_canvas()
    pass

def handle_events():
    events = get_events()
    pass

def pause(): pass

def resume(): pass