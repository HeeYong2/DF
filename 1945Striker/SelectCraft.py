import game_framework

from pico2d import*

import main_state

name = "SelectCraft"
image = None
select = 0

def enter():
    global image
    image = load_image('Stage/logo/choice_plane2.png')

def exit():
    global image
    del(image)

def pause():
    pass

def resume():
    pass

def handle_events(frame_time):
    global select
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(main_state)

def update(frame_time):
    pass

def draw(frame_time):
    global image, select
    clear_canvas()
    image.draw(274, 365)
    update_canvas()