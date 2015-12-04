import game_framework
from pico2d import *
import json
import SelectCraft

name = "RankingState"
image = None
font = None
data_file = open('data.txt', 'r')
data = json.load(data_file)
data_file.close()

def enter():
    global image, font
    image = load_image('blackboard.png')
    font = load_font('ENCR10B.TTF', 30)


def exit():
    global image
    del(image)

def update(frame_time):
    pass

def get_key(item):
    return item['score']

def draw_ranking():
    with open('score.txt','r') as f:
        score_list = json.load(f)
    score_list.sort(key=get_key, reverse=True)
    top_10 = score_list[:10]
    font.draw(data['BackGround']['w']/2 - 90, 600, '[Ranking]', (255,255,255))
    font.draw(10,30, '[ReGame: PRESS R]', (255,255,255))
    for i, record in enumerate(top_10):
        font.draw(100, 550 - i * 40, '#%2d    (Score : %d)' % (i+1, record['score']), (255,255,255))


def draw(frame_time):
    global image
    clear_canvas()
    image.draw(data['BackGround']['w']/2, data['BackGround']['h']/2)

    draw_ranking()

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




