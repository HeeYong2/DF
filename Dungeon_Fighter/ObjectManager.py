__author__ = 'HeeYong'

from Gunner import *
from BulletManager import *
from AttackEffect import *

ObjectList = []

def draw():
    global ObjectList
    for Object in ObjectList:
        Object.draw()

def update():
    global ObjectList
    for Object in ObjectList:
        Object.update()

def AddObject():
    global ObjectList
    #ObjectList.append()