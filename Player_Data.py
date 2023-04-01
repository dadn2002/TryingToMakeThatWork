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
        self.skl = [Weapon(PlayerDataFromExcel[0][4])]
        self.arm = [Armour(PlayerDataFromExcel[0][5]), Armour(PlayerDataFromExcel[0][6]), Armour(PlayerDataFromExcel[0][7]),
                    Armour(PlayerDataFromExcel[0][8]), Armour(PlayerDataFromExcel[0][9])]
        for element in self.arm:
            self.totalArmour += element.damRed
        self.Pos = [[PlayerDataFromExcel[0][10]], [PlayerDataFromExcel[0][11]], [PlayerDataFromExcel[0][12]]]
        self.inv = PlayerDataFromExcel[0][13]

    def info(self):
        return [
            [self.name],
            [self.hp],
            [self.mp],
            [self.skl],
            [self.spd],
            [self.arm],
            [self.inv]
        ]


PlayerDataFromExcel = [
    [
        # Name, Hp, Mp, Speed, Wpn1, Wpn2, Helmet, Chest, Leggings, Boots, WorldPosX, WorldPosY, WorldDirection, Inv
        'debug',
        10,
        0,
        3,
        'sword',
        'Leather Shield',
        'Leather Helmet',
        'Leather Chest',
        'Leather Leggings',
        'Leather Boots',
        0,
        0,
        1,
        [''],
    ]
]
