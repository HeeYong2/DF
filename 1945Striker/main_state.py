__author__ = 'HeeYong'

import random
import json
from Missile import*
from Enemy import*
from AirCraft import*
from Background import*
from Bomb import*
from Item import*
from UI import*
from pico2d import *

import game_framework
import SelectCraft

name = "MainState"

aircraft = None
missile = None
enemy = None
background = None
font = None
bomb = None
item = None

def enter():
    global aircraft, missile, enemy, background, font, bomb, item , credit , pushstart ,lifeui , stageoneui , powerbarui
    aircraft = AirCraft()
    missile = Missile()
    enemy = Enemy()
    background = Background()
    bomb = Bomb()
    item = Item()
    credit = Credit()
    pushstart = PushStart()
    lifeui = LifeUI()
    stageoneui = StageOneUI()
    powerbarui = PowerUI()

def exit():
    global aircraft, missile, enemy, background, font, bomb, item , credit , pushstart , stageoneui , lifeui , powerbarui

    del(lifeui)
    del(stageoneui)
    del(pushstart)
    del(credit)
    del(aircraft)
    del(missile)
    del(enemy)
    del(background)
    del(font)
    del(bomb)
    del(item)
    del(powerbarui)

def pause():
    pass

def resume():
    pass

def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(SelectCraft)
        else:
            aircraft.handle_event(event, missile, bomb)

def collide(a, b, a_num , b_num, a_type, b_type):
    left_a, bottom_a, right_a, top_a = a.get_bb(a_num, a_type)
    left_b, bottom_b, right_b, top_b = b.get_bb(b_num, b_type)

    if left_a > right_b:
        return False
    if right_a < left_b:
        return False
    if top_a < bottom_b:
        return False
    if bottom_a > top_b:
        return False

    return True

def update(frame_time):
    global background, aircraft, missile, enemy, bomb, item , pushstart , powerbar

    background.update(frame_time)
    aircraft.update(frame_time, missile)
    missile.update(frame_time)
    enemy.update(frame_time,missile)
    bomb.update(frame_time)
    item.update(frame_time)
    pushstart.update(frame_time)
    #powerbar.update(frame_time)

    for i in range(0, 200):
        if missile.use_flag[i] == 0:
            continue

        if missile.type[i] == 3 or missile.type[i] == 4 or missile.type[i] == 5:
            # if collide(aircraft, missile, 0, i, 0, missile.type[i]):              #플레이어와 에너미사일 충돌
            #     aircraft.x = 300
            #     aircraft.y = 20
            if collide(bomb, missile, 0, i, 0, missile.type[i]):
                missile.use_flag[i] = 0
                missile.x[i] = -500
                missile.y[i] = -500
        elif missile.type[i] == 0 or missile.type[i] == 1 or missile.type[i] == 2:
            for num in range(0, 50):
                if enemy.live_flag[num] == 0:
                    continue

                if collide(enemy, missile, num, i, 0, missile.type[i]):
                    item.create_item(enemy.x[num], enemy.y[num])
                    enemy.x[num] = -300
                    enemy.y[num] = -300
                    enemy.live_flag[num] = 0
                if collide(enemy, missile, num, i, 1, missile.type[i]):
                    item.create_item(enemy.x[num], enemy.y[num])
                    enemy.x[num] = -300
                    enemy.y[num] = -300
                    enemy.live_flag[num] = 0

    for num in range(50):
        if enemy.live_flag[num] == 0:
            continue

        if collide(enemy, bomb, num, 0, 0, 0):
            item.create_item(enemy.x[num], enemy.y[num])
            enemy.x[num] = -300
            enemy.y[num] = -300
            enemy.live_flag[num] = 0
        if collide(enemy, bomb, num, 0, 1, 0):
            item.create_item(enemy.x[num], enemy.y[num])
            enemy.x[num] = -300
            enemy.y[num] = -300
            enemy.live_flag[num] = 0

def draw(frame_time):
    global background, aircraft, missile, enemy, bomb, item ,credit , pushstart , stageoneui , lifeui

    clear_canvas()
    background.draw(frame_time)
    enemy.draw(frame_time)
    item.draw(frame_time)
    aircraft.draw(frame_time)
    missile.draw(frame_time)
    bomb.draw(frame_time)
    credit.draw(frame_time)
    pushstart.draw(frame_time)
    stageoneui.draw(frame_time)
    lifeui.draw(frame_time)
    powerbarui.draw(frame_time)
    update_canvas()