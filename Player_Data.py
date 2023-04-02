from pathlib import Path

import openpyxl
from Itens import *


class DataPlayer:
    def __init__(self, name):
        self.name = 'none'
        self.hp = 0
        self.mp = 0
        self.skl = []
        self.spd = 0
        self.arm = []
        self.totalArmour = 0
        self.inv = []
        self.Pos = []
        self.lvl = 1
        self.maxhpmp = []
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
        self.name = PlayerDataFromExcel[0][0]
        self.hp = PlayerDataFromExcel[0][1]
        self.mp = PlayerDataFromExcel[0][2]
        self.spd = PlayerDataFromExcel[0][3]
        self.skl = Weapon(PlayerDataFromExcel[0][4])
        self.arm = [Armour(PlayerDataFromExcel[0][5]), Armour(PlayerDataFromExcel[0][6]),
                    Armour(PlayerDataFromExcel[0][7]),
                    Armour(PlayerDataFromExcel[0][8]), Armour(PlayerDataFromExcel[0][9])]
        self.totalArmour = 0
        for element in self.arm:
            self.totalArmour += element.damRed
        self.Pos = [PlayerDataFromExcel[0][10], PlayerDataFromExcel[0][11], PlayerDataFromExcel[0][12]]
        for element in PlayerDataFromExcel[0][13]:
            self.inv.append(Item(element))
        self.lvl = PlayerDataFromExcel[0][14]
        self.maxhpmp = PlayerDataFromExcel[0][15]

    def info(self):
        return [
            self.name,
            self.hp,
            self.mp,
            self.spd,
            self.skl,
            self.arm,
            self.totalArmour,
            self.inv,
            self.Pos,
            self.lvl,
            self.maxhpmp,
        ]


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
        # print(self.info())

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
        ]


class Skills:
    def __init__(self, name):
        self.name = name.lower()
        self.dam = 0
        self.ran = 0
        self.typ = ''
        self.elements = ''
        self.tags = []
        self.update()

    def update(self):
        for element in SkillsDataFromExcel:
            if self.name == element[0].lower():
                self.dam = element[1]
                self.ran = element[2]
                self.typ = element[3]
                self.elements = element[4]
                self.tags = element[5]

    def info(self):
        return [self.name, self.dam, self.ran, self.typ, self.elements, self.tags]


PlayerDataFromExcel = [
    # Name, Hp, Mp, Speed, Wpn1, Wpn2, Helmet, Chest, Leggings, Boots, WorldPosX, WorldPosY, WorldDirection, Inv, Lvl, MaxHpMp
    ['Belmont', 80, 0, 3, 'sword', 'Leather Shield', 'Leather Helmet', 'Leather Chest', 'Leather Leggings',
     'Leather Boots', 0, 0, 1, ['tonic1', 'tonic1', 'elixir1'], 1, [100, 10]]
]

EnemyDataFromExcel = [
    # Name, Hp, Mp, Speed, Skls, DamRed, Elements, Xp, Gold, Drop, Region, Weight, AI, SpriteCoord
    # First Skl is always contact damage
    ['goblin', 10, 0, 1, ['contact1', 'punch1'], 0, [], 5, 2, ['tonic'], ['plains'], 5, 'zombie1', [3, 2]],
    ['bandit', 20, 0, 1, ['contact1', 'slash1'], 3, [], 20, 5, ['tonic'], ['plains'], 5, 'zombie1', [102, 2]],
    ['watcher', 10, 0, 1, ['contact0'], -5, [''], 0, 5, ['tonic'], ['plains'], 5, 'watcher1', [201, 2]],
]

SkillsDataFromExcel = [
    # name, dam, range, type, elements, stun, poison, slow, curse
    ['contact1', 10, 1, 'blunt', None, [False, False, False, False]],
    ['contact0', 0, 1, 'blunt', None, [False, False, False, False]],
    ['punch1', 5, 1, ['blunt', 'stun'], None, [False, False, False, False]],
    ['slash1', 10, 1, ['cut'], None, [False, False, False, False]],
]
