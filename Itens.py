class Weapon:
    def __init__(self, name, dam=0, ran=0, elements=''):
        RaiseError = True
        self.name = name.lower()
        self.dam = dam
        self.ran = ran
        self.elements = elements

        for element in ListOfWeapons:
            if self.name == element[0].lower():
                self.dam = element[1]
                self.ran = element[2]
                self.elements = element[3]
                RaiseError = False
                break
        if RaiseError:
            self.name = None
        # print(self.name, self.dam, self.ran, self.elements)

    def update(self):
        for element in ListOfWeapons:
            if self.name == element[0].lower():
                self.dam = element[1]
                self.ran = element[2]
                self.elements = element[3]


class Armour:
    def __init__(self, name, damRed=0, Type=''):
        RaiseError = True
        self.name = name.lower()
        self.damRed = damRed
        self.Type = Type

        for element in ListOfArmours:
            if self.name == element[0].lower():
                self.damRed = element[1]
                self.ranType = element[2]
                RaiseError = False
                break
        if RaiseError:
            self.name = None
        # print(self.name, self.dam, self.ran, self.elements)

    def update(self):
        for element in ListOfWeapons:
            if self.name == element[0].lower():
                self.damRed = element[1]
                self.ranType = element[2]


ListOfWeapons = [
    # Name, Dam, Range, Element
    ['fist', 2, 5, 'none'],
    ['stick', 4, 5, 'none'],
    ['sword', 5, 5, 'none'],
    ['stone', 10, 5, 'none'],
]
ListOfArmours = [
    # Name, Dam Red, Type S/H/C/L/B
    ['Leather Shield', 2, 'S'],
    ['Leather Helmet', 2, 'S'],
    ['Leather Chest', 2, 'S'],
    ['Leather Leggings', 2, 'S'],
    ['Leather Boots', 2, 'S'],
]
