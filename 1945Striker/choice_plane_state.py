import game_framework
from pico2d import*

import main_state


name = "ChoicePlaneState"
image = [None] * 2
choice_sound = None
choice = 0

def enter():
    global image, choice_sound
    if image[0] == None:
        image[0] = load_image('choice_plane1.png')
    if image[1] == None:
        image[1] = load_image('choice_plane2.png')
    if choice_sound == None:
        choice_sound = load_wav('choice_character.wav')
        choice_sound.set_volume(128)

def exit():
    global image
    #del(image[0])



def pause():
    pass

def resume():
    pass

def handle_events(frame_time):
    global choice
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT) or (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
                choice += 1
                choice_sound.play()
                if choice >= 10:
                    choice = 0
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(main_state)

def update(frame_time):
    pass

def draw(frame_time):
    global image, choice
    clear_canvas()
    if choice%2 == 0:
        image[0].draw(275, 365)
    elif choice%2 == 1:
        image[1].draw(275, 365)
    update_canvas()