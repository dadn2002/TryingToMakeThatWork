import math
from pathlib import Path

import openpyxl
import pygame

from Itens import *


class DataPlayer:
    def __init__(self, name):
        self.name = name
        self.hp = 0
        self.mp = 0
        self.wpn = []
        self.skl = []
        self.spd = 0
        self.arm = []
        self.totalArmour = 0
        self.inv = []
        self.Pos = []
        self.lvl = 1
        self.maxhpmp = []
        self.dot = []
        self.internalName = 'stragomagus'
        self.sprite = []
        self.missions = []
        self.update()

    def update(self):
        # Data = Path("data/Player Data.xlsx")
        # Dataobj = openpyxl.load_workbook(Data, data_only=True)
        # ObjData = Dataobj.active
        # PlayerDataExcel = []
        # for i in range(12):
        #     PlayerDataExcel.append(ObjData['B' + str(i + 3)].value)
        # Dataobj.save(Data)
        # Name, Hp, Mp, Speed, Wpn1, Wpn2, Helmet, Chest, Leggings, Boots, WorldPosX, WorldPosY, WorldDirection, Inv
        for element in PlayerDataFromExcel:
            if self.name.lower() == element[0].lower():
                self.name = PlayerDataFromExcel[0][0]
                self.hp = PlayerDataFromExcel[0][1]
                self.mp = PlayerDataFromExcel[0][2]
                self.spd = PlayerDataFromExcel[0][3]
                self.wpn = Weapon(PlayerDataFromExcel[0][4])
                for element in PlayerDataFromExcel[0][6]:
                    self.skl.append(Skills(element))
                self.arm = [Armour(PlayerDataFromExcel[0][5]), Armour(PlayerDataFromExcel[0][7]),
                            Armour(PlayerDataFromExcel[0][8]),
                            Armour(PlayerDataFromExcel[0][9]), Armour(PlayerDataFromExcel[0][10])]
                self.totalArmour = 0
                for element in self.arm:
                    self.totalArmour += element.damRed
                self.Pos = [PlayerDataFromExcel[0][11], PlayerDataFromExcel[0][12], PlayerDataFromExcel[0][13]]
                for element in PlayerDataFromExcel[0][14]:
                    self.inv.append(Item(element))
                self.lvl = PlayerDataFromExcel[0][15]
                self.maxhpmp = PlayerDataFromExcel[0][16]
                break
        if self.internalName.lower() == 'stragomagus':
            self.sprite = [199, 5, 16, 24]

    def dotTick(self):
        totalDamage = 0
        for effect in self.dot:
            if effect[0] in ListOfDot:
                totalDamage += effect[2] * (1 + 0.25 * float(int(effect[0][len(effect[0]) - 1])))
                effect[1] -= 1
        for i in range(len(self.dot) - 1, -1, -1):
            if self.dot[i][1] <= 0:
                del self.dot[i]
        return math.floor(totalDamage)

    def info(self):
        return [
            self.name,
            self.hp,
            self.mp,
            self.spd,
            self.wpn,
            self.skl,
            self.arm,
            self.totalArmour,
            self.inv,
            self.Pos,
            self.lvl,
            self.maxhpmp,
        ]

    def removeFromInv(self, item):
        if type(item) is Item:
            item = item.name
        for i in range(len(self.inv)):
            if item == self.inv[i].name:
                del self.inv[i]
                break

    def addToInv(self, name):
        if type(name) is str:
            self.inv.append(Item(name))
        else:
            self.inv.append(name)

    def checkInv(self, name):
        for element in self.inv:
            if name.lower() == element.name:
                return True
        return False


class DataEnemy:
    def __init__(self, name):  # Name, Hp, Mp, Speed, Skls, DamRed, Elements, Xp, Gold, Drop, Region, Weight, AI
        self.name = name.lower()
        self.hp = 0
        self.mp = 0
        self.spd = 0
        self.skl = []
        self.damRed = 0
        self.elements = []
        self.xp = 0
        self.gold = 0
        self.drop = []
        self.region = []
        self.weight = 0
        self.ai = ''
        self.sprite = []
        self.box = []
        self.dot = []
        self.update()

    def update(self):
        for element in EnemyDataFromExcel:
            if self.name == element[0].lower():
                self.name = element[0].lower()
                self.hp = element[1]
                self.mp = element[2]
                self.spd = element[3]
                for skill in element[4]:
                    self.skl.append(Skills(str(skill)))
                self.damRed = element[5]
                self.elements = element[6]
                self.xp = element[7]
                self.gold = element[8]
                self.drop = element[9]
                self.region = element[10]
                self.weight = element[11]
                self.ai = element[12]
                self.sprite = element[13]
                self.box = element[14]
                break
        # print(self.info())

    def dotTick(self):
        totalDamage = 0
        for effect in self.dot:
            if effect[0] in ListOfDot:
                testResistence = False
                effectLevel = int(effect[0][len(effect[0]) - 1])
                for element in self.elements:
                    if element[0][0:len(element[0]) - 1] == effect[0][0:len(effect[0]) - 1]:
                        resistenceLevel = int(element[0][len(element[0]) - 1])
                        totalDamage += effect[2] * (1 + 0.25 * float(effectLevel - resistenceLevel))
                        testResistence = True
                        break
                if testResistence is False:
                    totalDamage += effect[2] * (1 + 0.25 * float(effectLevel))
                effect[1] -= 1
        for i in range(len(self.dot) - 1, -1, -1):
            if self.dot[i][1] <= 0:
                del self.dot[i]
        return math.floor(totalDamage)

    def info(self):
        return [
            self.name,
            self.hp,
            self.mp,
            self.spd,
            self.skl,
            self.damRed,
            self.elements,
            self.xp,
            self.gold,
            self.drop,
            self.region,
            self.weight,
            self.ai,
            self.sprite,
            self.box,
            self.dot
        ]


class DataNpc:
    def __init__(self, name, profession='', inventory='', map=''):
        self.name = name
        self.profession = profession
        self.holdPosition = []
        self.hasHitBox = False
        self.textBox = []
        self.inv = inventory
        self.map = map
        self.sprite = []
        self.update()

    def update(self):
        if self.map.lower() == 'domacastle':
            if self.name.lower() == 'guard':
                self.sprite = [698, 5, 16, 24]
            if self.name.lower() == 'king':
                self.sprite = [552, 548, 16, 24]
                self.textBox = [['Mission', 'DomaCastle1']]
                self.holdPosition = [4872, 128, 'down']
                self.hasHitBox = True

    def info(self):
        return [
            self.name,
            self.profession,
            self.holdPosition,
            self.hasHitBox,
            self.textBox,
            self.inv,
            self.map,
            self.sprite,
        ]


class Skills:
    def __init__(self, name):
        self.name = name.lower()
        self.dam = 0
        self.are = []
        self.ran = 0
        self.typ = ''
        self.tags = []
        self.update()

    def update(self):
        for element in SkillsDataFromExcel:
            if self.name == element[0].lower():
                self.dam = element[1]
                self.are = element[2]
                self.ran = element[3]
                self.typ = element[4]
                self.tags = element[5]
                break

    def runSound(self):
        if self.typ == 'blunt':
            pygame.mixer.Sound.play(pygame.mixer.Sound("ost/2eswordslashlong.mp3"))
        elif self.typ == 'fire':
            pygame.mixer.Sound.play(pygame.mixer.Sound("ost/16fire1.mp3"))
        elif self.typ == 'fire3':
            pygame.mixer.Sound.play(pygame.mixer.Sound("ost/19fire3.mp3"))

    def info(self):
        return [self.name, self.dam, self.are, self.ran, self.typ, self.tags]


PlayerDataFromExcel = [
    # Name, Hp, Mp, Speed, Wpn1, Wpn2, Skills, ,Helmet, Chest, Leggings, Boots, WorldPosX, WorldPosY, WorldDirection, Inv, Lvl, MaxHpMp
    ['Belmont', 100, 10, 3, 'staff', 'Leather Shield', ['bite1', 'fire1', 'fire3'], 'Leather Helmet', 'Leather Chest',
     'Leather Leggings',
     'Leather Boots', 0, 0, 1, ['tonic1', 'tonic1', 'elixir1', 'key', 'key', 'key', 'key'], 1, [100, 10]]
]

EnemyDataFromExcel = [
    # Name, Hp, Mp, Speed, Skls, DamRedPhy, Elements, Xp, Gold, Drop, Region, Weight, AI, SpriteCoord, Rect
    # First Skl is always contact damage
    ['bandit', 50, 0, 1, ['slash1', 'pull1'], 0, [], 5, 2, [['tonic1', 0.3]], ['plains'], 5, 'zombie1', [13, 14],
     [32, 48]],
    ['wolf', 40, 0, 1, ['bite1', 'roar1'], 0, [], 5, 2, [['tonic1', 0.5]], ['plains'], 5, 'zombie1', [54, 12],
     [49, 48]],
    ['mammoth', 100, 0, 1, ['stomp1', 'dash1'], 5, [['fire1']], 5, 2,
     [['tonic1', 1], ['tonic1', 1], ['tonic1', 0.5], ['tonic1', 0.5]], ['plains'], 5, 'zombie1', [105, 14], [63, 48]],
    ['rat', 5, 0, 2, ['bite1'], -5, [], 5, 2, [['tonic1', 0.1]], ['plains'], 5, 'zombie1', [175, 30], [32, 32]],
    ['toxic cloud', 30, 0, 1, ['poison1'], 0, [], 5, 2, [['ether1', 0.5], ['ether1', 0.5]], ['plains'], 5, 'zombie1',
     [213, 31], [32, 31]],
    ['engineer', 50, 0, 2, ['punch1'], 0, [], 2, 2, [['tonic1', 0.2]], ['plains'], 5, 'zombie1', [251, 30],
     [24, 32]],
    ['rabbit', 15, 0, 2, ['bite1'], 0, [], 0, 2, [['tonic1', 0.1]], ['plains'], 5, 'zombie1', [280, 30],
     [32, 32]],
    ['hornet', 5, 0, 1, ['sting1'], 0, [], 5, 2, [['tonic1', 0.1]], ['plains'], 5, 'zombie1', [482, 31],
     [32, 31]],
    ['wolf', 15, 0, 1, ['bite1', 'roar1'], 0, [], 5, 2, [['tonic1', 0.5]], ['plains'], 5, 'zombie1', [54, 12],
     [49, 48]],
    ['wolf', 15, 0, 1, ['bite1', 'roar1'], 0, [], 5, 2, [['tonic1', 0.5]], ['plains'], 5, 'zombie1', [54, 12],
     [49, 48]],
]

SkillsDataFromExcel = [
    # name, dam, area, range, type, tags
    ['slash1', 10, ['single', 1], 4, 'blunt', [['phy'], ['cut'], ['value', 100]]],
    ['punch1', 8, ['single', 1], 4, 'blunt', [['phy'], ['value', 80]]],
    ['bite1', 8, ['single', 1], 4, 'blunt', [['phy'], ['cut'], ['bleed1', 3, 1], ['value', 100]]],
    ['sting1', 5, ['single', 1], 4, 'blunt', [['phy'], ['cut'], ['poison1', 3, 1], ['value', 100]]],
    ['roar1', 0, ['are', 3], -1, 'buff', [['buff'], ['dam1', 2, 1], ['value', 20]]],
    ['stomp1', 20, ['single', 1], 2, 'blunt', [['phy'], ['stun1', 1, 0], ['value', 10]]],
    ['pull1', 5, ['single', 1], 4, 'blunt', [['phy'], ['pull1', -1], ['value', 10]]],
    ['dash1', 30, ['single', 1], 4, 'blunt', [['phy'], ['push1', -1], ['value', 80]]],
    ['poison1', 5, ['area', 3], 3, 'poison', [['poison1', 3, 1], ['mpcost', 2], ['value', 50]]],
    ['fire1', 5, ['area', 3], 3, 'fire', [['fire1', 3, 1], ['mpcost', 2], ['value', 80]]],
    ['fire2', 50, ['area', 3], 3, 'fire2', [['fire2', 3, 5], ['mpcost', 5], ['value', 50]]],
    ['fire3', 100, ['area', 5], 4, 'fire3', [['fire3', 3, 10], ['mpcost', 10], ['heavy', -1], ['value', 10]]],
]

ListOfDot = [
    # ['name', duration, base damage]
    'fire1',
    'fire2',
    'fire3',
    'bleed1',
    'poison1',
    'stun1'
]
