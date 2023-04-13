class Weapon:
    def __init__(self, name, dam=0, ran=0, elements=''):
        RaiseError = True
        self.name = name.lower()
        self.dam = dam
        self.ran = ran
        self.tags = elements
        self.update()
        # print(self.name, self.dam, self.ran, self.elements)

    def update(self):
        for element in ListOfWeapons:
            if self.name == element[0].lower():
                self.dam = int(element[1])
                self.ran = int(element[2])
                self.tags = element[3]

    def info(self):
        return [
            self.name,
            self.dam,
            self.ran,
            self.tags,
        ]


class Armour:
    def __init__(self, name, damRed=0, Type=''):
        RaiseError = True
        self.name = name.lower()
        self.damRed = damRed
        self.Type = Type

        for element in ListOfArmours:
            if self.name == element[0].lower():
                self.damRed = element[1]
                self.Type = element[2]
                RaiseError = False
                break
        if RaiseError:
            self.name = None
        # print(self.name, self.dam, self.ran, self.elements)

    def update(self):
        for element in ListOfWeapons:
            if self.name == element[0].lower():
                self.damRed = element[1]
                self.Type = element[2]

    def info(self):
        return [
            self.name,
            self.damRed,
            self.Type,
        ]


class Item:
    def __init__(self, name):
        self.name = name.lower()
        self.price = 0
        self.tags = []
        self.update()

    def update(self):
        for element in ListOfItens:
            if self.name == element[0].lower():
                self.price = element[1]
                if len(element) > 2:
                    for i in range(2, len(element)):
                        self.tags.append(element[i])
                else:
                    self.tags.append(element[2])

    def info(self):
        return [self.name, self.price, self.tags]


def isConsumable(name):
    consumable = ['hp', 'mp']
    for element in Item(name).tags:
        if element[0] in consumable:
            return True
    return False


ListOfWeapons = [
    # Name, Dam, Range, Tags (Elements, projectile, are, etc)
    ['fist', 2, 1, ['phy']],
    ['stick', 4, 1, ['phy']],
    ['sword', 999, 2, ['phy']],
    ['stone', 10, 1, ['phy']],
    ['staff', 5, 2, ['mag']],
]
ListOfArmours = [
    # Name, Dam Red, Type S/H/C/L/B
    ['Leather Shield', 1, 'S'],
    ['Leather Helmet', 1, 'S'],
    ['Leather Chest', 1, 'S'],
    ['Leather Leggings', 1, 'S'],
    ['Leather Boots', 1, 'S'],
]
ListOfItens = [
    # Name, price, Tags: ['hp', value], ['mp', value], ['keytype', tier],
    ['tonic1', 5, ['hp', 20]],
    ['tonic2', 50, ['hp', 100]],
    ['ether1', 5, ['mp', 10]],
    ['elixir1', 40, ['hp', 50], ['mp', 20]],
    ['key', 5, ['undead', 1]],
]
