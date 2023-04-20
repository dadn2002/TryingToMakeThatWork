import random
from Itens import *


def zoneSpawn(mapName, tier):
    plains = [
        # Enemy average, Enemy Names + SpawnRate,
        [[1, 3], [['wolf', 70], ['hornet', 10], ['rabbit', 14], ['rat', 5], ['bandit', 1]]],  # 0
        [[1, 3], [['wolf', 60], ['hornet', 15], ['rabbit', 15], ['rat', 5], ['bandit', 5]]],  # 1
        [[2, 4], [['wolf', 50], ['hornet', 20], ['rabbit', 15], ['rat', 5], ['bandit', 10]]],  # 2
        [[3, 5], [['wolf', 60], ['hornet', 25], ['rabbit', 0], ['rat', 0], ['bandit', 15]]],  # 3
        [240, 0],  # Coordinate of background sprite
    ]
    tempSpawn = []
    nameOdd = []
    totalOdd = []
    background = []
    if mapName == 'plains':
        tempSpawn = plains[tier]
        background = plains[4]
    for enemySpawnRate in tempSpawn[1]:
        nameOdd.append(enemySpawnRate[0])
        totalOdd.append(enemySpawnRate[1])
    tempEnemies = random.choices(nameOdd, weights=totalOdd, k=random.randint(tempSpawn[0][0], tempSpawn[0][1]))
    return [tempEnemies, background]


def zoneChestLoot(mapName, tier):
    DomaCastle = [
        [[1, 3], [['tonic1', 200], ['ether1', 10], ['elixir1', 1]]],  # 0
        [[2, 5], [['tonic1', 200], ['ether1', 10], ['elixir1', 1]]],  # 1
        [[3, 5], [['tonic1', 200], ['ether1', 10], ['elixir1', 1]]],  # 2
        [[3, 5], [['tonic1', 200], ['tonic2', 20], ['ether1', 10], ['elixir1', 1]]],  # 3
    ]
    tempChestLoot = []
    nameOdd = []
    totalOdd = []
    if mapName.lower() == 'DomaCastle'.lower():
        tempChestLoot = DomaCastle[tier]
    for dropSpawnHeight in tempChestLoot[1]:
        nameOdd.append(dropSpawnHeight[0])
        totalOdd.append(dropSpawnHeight[1])
    tempDrop = random.choices(nameOdd, weights=totalOdd, k=random.randint(tempChestLoot[0][0], tempChestLoot[0][1]))
    finalDrop = []
    for item in tempDrop:
        finalDrop.append(Item(item))
    return finalDrop


def zoneMission(mission):
    description = ''     # Description of what we need to do
    missionMapName = []  # Collection of Maps Names
    creatureToKill = []  # Collection of Creatures + Maps Names in which it will spawn
    itemToCollect = []   # Collection of Itens + Maps Names in which it apper in lootTable
    npcToTalk = []       # Collection of Npcs Names + Maps Names in which it will spawn
    if mission.lower() == 'DomaCastle1'.lower():
        description = 'Kill rogue guards'
        missionMapName = ['DomaCastleForest1']
        creatureToKill = []
        itemToCollect = []
        npcToTalk = []

    return [description, missionMapName, creatureToKill, itemToCollect, npcToTalk]

