class Weapon:
    def __init__(self, name, dam=0, ran=0, elements=''):
        RaiseError = True
        self.name = name.lower()
        self.dam = dam
        self.ran = ran
        self.elements = elements
        self.update()
        # print(self.name, self.dam, self.ran, self.elements)

    def update(self):
        for element in ListOfWeapons:
            if self.name == element[0].lower():
                self.dam = int(element[1])
                self.ran = int(element[2])
                self.elements = element[3]

    def info(self):
        return [
            self.name,
            self.dam,
            self.ran,
            self.elements,
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


ListOfWeapons = [
    # Name, Dam, Range, Element
    ['fist', 2, 5, 'none'],
    ['stick', 4, 5, 'none'],
    ['sword', 5, 5, 'none'],
    ['stone', 10, 5, 'none'],
]
ListOfArmours = [
    # Name, Dam Red, Type S/H/C/L/B
    ['Leather Shield', 1, 'S'],
    ['Leather Helmet', 1, 'S'],
    ['Leather Chest', 1, 'S'],
    ['Leather Leggings', 1, 'S'],
    ['Leather Boots', 1, 'S'],
]
