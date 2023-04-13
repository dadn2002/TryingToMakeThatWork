import random


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
