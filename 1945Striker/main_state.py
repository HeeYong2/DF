import random
import json
import os

from Missile import*
from Enemy import*
from AirCraft import*
from Background import*
from Bomb import*
from Item import*
from Effect import*
from Boss import*

from pico2d import *

import game_framework
import start_state
import ranking_state


data_file = open('data.txt', 'r')
data = json.load(data_file)
data_file.close()

name = "MainState"

hero = None
missile = None
enemy = None
background = None
font = None
bomb = None
item = None
effect = None
boss = None
score = 0

get_item_sound = None

def enter():
    global hero, missile, enemy, background, font, bomb, item, effect, boss, get_item_sound
    hero = Hero()
    missile = Missile()
    enemy = Enemy()
    background = Background()
    bomb = Bomb()
    item = Item()
    effect = Effect()
    boss = Boss()
    font = load_font('ENCR10B.TTF', 30)

    if get_item_sound == None:
        get_item_sound = load_wav('get_item.wav')
        get_item_sound.set_volume(100)

def exit():
    global hero, missile, enemy, background, font, bomb, item, effect, boss
    del(hero)
    del(missile)
    del(enemy)
    del(background)
    del(font)
    del(bomb)
    del(item)
    del(effect)
    del(boss)

def pause():
    pass
    #print("State [%s] Paused" % self.name)

def resume():
    pass
    #print("State [%s] Resumed" % self.name)

def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            #running = False
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            #running = False
            game_framework.change_state(start_state)
        else:
            hero.handle_event(event, missile, bomb)

def check_collision(a, b, a_num , b_num, a_type, b_type):
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
    global background, hero, missile, enemy, bomb, item, effect, boss, score

    background.update(frame_time)
    hero.update(frame_time, missile)
    missile.update(frame_time, hero)
    enemy.update(frame_time,missile, effect, item)
    bomb.update(frame_time)
    item.update(frame_time)
    effect.update(frame_time)
    boss.update(frame_time, missile, score, background)


    for i in range(0, data['Missile']['MISSILE_MAX']):
        if missile.use_flag[i] == 0:
            continue

        if missile.type[i] == 3 or missile.type[i] == 4 or missile.type[i] == 5 or missile.type[i] == 6:                        # hero to enemymissile
            if check_collision(hero, missile, None, i, None, missile.type[i]):
                effect.create_effect(1, hero.x, hero.y)
                missile.use_flag[i] = data['Missile']['use_flag']
            if check_collision(bomb, missile, None, i, None, missile.type[i]) and bomb.use_flag == 1:         #bomb to enemymissile
                missile.use_flag[i] = data['Missile']['use_flag']
        elif missile.type[i] == 0 or missile.type[i] == 1 or missile.type[i] == 2:                      #enemy to heromissile
            for e_num in range(0, data['Enemy']['ENEMY_MAX']):
                if enemy.live_flag[e_num] == 0:
                    continue

                if check_collision(enemy, missile, e_num, i, data['Enemy']['E1_WING'], missile.type[i]):   #enemywing
                    effect.create_effect(0, missile.x[i], missile.y[i])
                    enemy.hp[e_num] -= missile.power + 1
                    missile.use_flag[i] = data['Missile']['use_flag']
                if check_collision(enemy, missile, e_num, i, data['Enemy']['E1_BODY'], missile.type[i]):   #enemybody
                    effect.create_effect(0, missile.x[i], missile.y[i])
                    enemy.hp[e_num] -= missile.power + 1
                    missile.use_flag[i] = data['Missile']['use_flag']
                if check_collision(enemy, missile, e_num, i, data['Enemy']['E2_WING'], missile.type[i]):   #enemywing
                    effect.create_effect(0, missile.x[i], missile.y[i])
                    enemy.hp[e_num] -= missile.power + 1
                    missile.use_flag[i] = data['Missile']['use_flag']
                if check_collision(enemy, missile, e_num, i, data['Enemy']['E2_BODY'], missile.type[i]):   #enemybody
                    effect.create_effect(0, missile.x[i], missile.y[i])
                    enemy.hp[e_num] -= missile.power + 1
                    missile.use_flag[i] = data['Missile']['use_flag']
                if check_collision(enemy, missile, e_num, i, data['Enemy']['E3_WING'], missile.type[i]):   #enemywing
                    effect.create_effect(0, missile.x[i], missile.y[i])
                    enemy.hp[e_num] -= missile.power + 1
                    missile.use_flag[i] = data['Missile']['use_flag']
                if check_collision(enemy, missile, e_num, i, data['Enemy']['E3_BODY'], missile.type[i]):   #enemybody
                    effect.create_effect(0, missile.x[i], missile.y[i])
                    enemy.hp[e_num] -= missile.power + 1
                    missile.use_flag[i] = data['Missile']['use_flag']


            if boss.live_flag == 1 and boss.y >= 550 and boss.hp > 0:                                                         #heromissile to boss
                if check_collision(boss, missile, None, i, data['Boss']['b_wing'], missile.type[i]):
                        effect.create_effect(0, missile.x[i], missile.y[i])
                        boss.hp -= missile.power + 1
                        missile.use_flag[i] = data['Missile']['use_flag']
                if check_collision(boss, missile, None, i, data['Boss']['b_body'], missile.type[i]):
                        effect.create_effect(0, missile.x[i], missile.y[i])
                        boss.hp -= missile.power + 1
                        missile.use_flag[i] = data['Missile']['use_flag']

    if boss.live_flag == 1 and boss.y >= 550 and boss.hp > 0 and bomb.check_damage == False:
        if check_collision(boss, bomb, None, None, data['Boss']['b_wing'], None):     #herobomb to boss
            boss.hp -= bomb.bomb_power
            bomb.check_damage = True
        if check_collision(boss, bomb, None, None, data['Boss']['b_body'], None):     #herobomb to boss
            boss.hp -= bomb.bomb_power
            bomb.check_damage = True


    for e_num in range(data['Enemy']['ENEMY_MAX']):                   #enemy to herobomb
        if enemy.live_flag[e_num] == 0 or bomb.use_flag == 0:
            continue

        if check_collision(enemy, bomb, e_num, None, 0, None):
            enemy.hp[e_num] -= bomb.bomb_power
        if check_collision(enemy, bomb, e_num, None, 1, None):
            enemy.hp[e_num] -= bomb.bomb_power


    for i_num in range(data['Item']['ITEM_MAX']):                 #hero to item
        if item.use_flag[i_num] == 0:
            continue

        if check_collision(hero, item, None, i_num, None, None):
            item.use_flag[i_num] = 0
            item.x[i_num] = data['Item']['x']
            item.y[i_num] = data['Item']['y']
            missile.power += 1
            if missile.power >= 3:
                missile.power = 3
            get_item_sound.play()

    get_score()

    if boss.live_flag == 0 and boss.hp <= 0:
        record_score()
        game_framework.change_state(ranking_state)
        return

def get_score():
    global background, hero, missile, enemy, bomb, item, effect, font, score

    score = enemy.enemy_score + boss.boss_score

def draw(frame_time):
    global background, hero, missile, enemy, bomb, item, effect, font, score

    clear_canvas()
    background.draw(frame_time)
    enemy.draw(frame_time)
    boss.draw(frame_time)
    item.draw(frame_time)
    hero.draw(frame_time)
    missile.draw(frame_time)
    bomb.draw(frame_time)
    effect.draw(frame_time)

    font.draw(10, 700, '[Score : %d]' %(score), (255,255,255))
    font.draw(350, 30, '[Bomb : %d]' %(bomb.use_number), (255,255,255))

    update_canvas()


def record_score():
    global background, hero, missile, enemy, bomb, item, effect, boss, score
    score_list = []

    if os.path.exists('score.txt'):
        with open('score.txt','r') as f:
            score_list = json.load(f)

    score = {"score": score}

    score_list.append(score)

    #print(json.dumps(score_list))

    with open('score.txt', 'w') as f:
        json.dump(score_list, f)