import sys
import math


# e = 2.718281

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def prnt(toprint):
    print(toprint, file=sys.stderr, flush=True)


class Factory:
    def __init__(self, entityId, entityType, owner, numCyborgs, production):
        self.entityId = entityId
        self.entityType = entityType
        self.owner = owner
        self.numCyborgs = numCyborgs
        self.production = production

    # Calcula la factory mas cercana a esta
    def nearest_distance(self, distances, factories):
        nearer_distance = None
        for fact in factories:
            if fact.entityId == self.entityId:
                continue
            try:
                dist_btw_factories = distances[self.entityId][fact.entityId]
            except KeyError:
                dist_btw_factories = distances[fact.entityId][self.entityId]
            if nearer_distance is None or dist_btw_factories < nearer_distance:
                nearer_distance = dist_btw_factories
        return nearer_distance

    def danger_factor(self, bot):
        enemy_value = bot.factory_puntuation(self, ally=False)
        in_min = out_min = 0
        in_max = bot.max_enemy_puntuation(self)
        out_max = 100
        x = enemy_value
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def calculate_n(self, bot):
        superior = math.log(math.e, bot.assumed_losing_prob)
        inferior = math.log(math.e, 100 - self.danger_factor(bot))
        prnt(inferior)
        return int(round((superior / inferior) / 100))


class Troop:
    def __init__(self, entityId, entityType, owner, leaving, target, numCyborgs, remainingTurns):
        self.entityId = entityId
        self.entityType = entityType
        self.owner = owner
        self.leaving = leaving
        self.target = target
        self.numCyborgs = numCyborgs
        self.remainingTurns = remainingTurns


class Bot:
    def __init__(self, factoryCount, distances, max_dist):
        self.factoryCount = factory_count
        self.distances = distances
        self.factories = {}
        self.troops = {}
        self.pond = [5, 0.8, 0, 0,0] # Ponderaciones para el calculo de las puntuaciones de las factorias
        self.t = 20
        self.assumed_losing_prob = 0.05
        self.max_dist = max_dist
        self.myfactories = None
        self.enemyfactories = None
        self.neutralfactories = None
        self.turn = 0
        self.bombs = 2
    # Arranque del bot
    def run(self):
        while True:
            entity_count = int(input())  # the number of entities (e.g. factories and troops)
            for i in range(entity_count):
                inputs = input().split()
                entity_id = int(inputs[0])
                entity_type = inputs[1]
                arg_1 = int(inputs[2])
                arg_2 = int(inputs[3])
                arg_3 = int(inputs[4])
                arg_4 = int(inputs[5])
                arg_5 = int(inputs[6])
                if entity_type == "FACTORY":
                    self.factories[entity_id] = Factory(entity_id, entity_type, arg_1, arg_2, arg_3)
                if entity_type == "TROOP":
                    self.troops[entity_id] = Troop(entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5)
            self.myfactories = self.get_myfactories()
            self.enemyfactories = self.get_enemyfactories()
            self.neutralfactories = self.get_neutralfactories()
            self.action()
            self.turn += 1

    def get_myfactories(self):
        return [factorie for factorie in self.factories.values() if factorie.owner == 1]

    def get_enemyfactories(self):
        return [factorie for factorie in self.factories.values() if factorie.owner == -1]

    def get_neutralfactories(self):
        return [factorie for factorie in self.factories.values() if factorie.owner == 0]

    def max_enemy_puntuation(self, factory):
        return self.pond[0] + self.pond[1] * self.max_dist + self.pond[2] * 3 + self.pond[4]

    def factory_puntuation(self, factory, ally=True):
        if ally:
            ally_dist = factory.nearest_distance(self.distances, self.myfactories)
            enemy_dist = factory.nearest_distance(self.distances, self.enemyfactories)
            prod = factory.production
            if factory.numCyborgs != 0:
                cybs = self.pond[3] / factory.numCyborgs
            else:
                cybs = 0
            owner = -factory.owner
        else:
            ally_dist = factory.nearest_distance(self.distances, self.enemyfactories)
            enemy_dist = factory.nearest_distance(self.distances, self.myfactories)
            prod = factory.production
            if factory.numCyborgs != 0:
                cybs = self.pond[3] / factory.numCyborgs
            else:
                cybs = 0
            owner = factory.owner

        if ally_dist is None or enemy_dist is None:
            return 0
        return self.pond[0] / ally_dist + self.pond[1] * enemy_dist + self.pond[2] * prod + cybs + self.pond[4] * owner


    def nearest_attacker(self, factory):
        distance_attcker = None

    def movement_puntuation(self, movement):
        movs = movement.split(" ")
        if movs[0] == "MOVE":
            suma_numCyborgs = sum([fact.numCyborgs for fact in self.myfactories])
            numCyborgs = suma_numCyborgs - self.factories[int(movs[2])].numCyborgs
            for fact in self.myfactories:
                if fact.entityId != int(movs[2]):
                    numCyborgs += max(fact.calculate_n(self), self.t) * fact.production
                else:
                    try:
                        dist = distances[int(movs[2])][int(movs[1])]
                    except KeyError:
                        dist = distances[int(movs[1])][int(movs[2])]
                    numCyborgs += (max(fact.calculate_n(self), self.t) - dist) * fact.production
        elif movs[0] == "WAIT":
            numCyborgs = sum([fact.numCyborgs for fact in self.myfactories])
            for fact in self.myfactories:
                numCyborgs += max(fact.calculate_n(self), self.t) * fact.production
        return numCyborgs

    def nearest_attacker(self, factory):
        distance_attacker = None
        attacker = None
        for fact in self.myfactories:
            try:
                dist = distances[factory.entityId][fact.entityId]
            except KeyError:
                dist = distances[fact.entityId][factory.entityId]
            if distance_attacker is None or dist < distance_attacker:
                if fact.numCyborgs > factory.numCyborgs:
                    attacker = fact
                    distance_attacker = dist
        return attacker

    def any_attacker(self, factory):
        attacker = []
        for fact in self.myfactories:
            if fact.numCyborgs > factory.numCyborgs:
                attacker.append(fact)
        return attacker
    '''
    def action(self):
        points = None
        factory = None
        if self.turn == 0:
            myFirstFactory = self.myfactories[0]
            firstEnemyFactory = self.enemyfactories[0]
            moviment = "BOMB " + str(myFirstFactory.entityId) + " " + str(firstEnemyFactory.entityId)
            print(moviment)
            return 0
        elif self.turn == 1:
            firstEnemyTroop = None
            for troope in self.troops.values():
                if troope.owner == -1:
                    firstEnemyTroop = troope
                    break
            myFirstFactory = self.myfactories[0]
            moviment = "BOMB " + str(myFirstFactory.entityId) + " " + str(firstEnemyTroop.target)
            print(moviment)
            return moviment
        for fact in self.neutralfactories + self.enemyfactories:
            fact_point = self.factory_puntuation(fact)
            if points is None or points < fact_point:
                points = fact_point
                factory = fact
        if factory is None:
            for p in self.myfactories:
                if p.production < 3:
                    movement += ";INC " + str(p.entityId)
            #print("WAIT")
        attacker = self.nearest_attacker(factory)
        if attacker is None:
            print("WAIT")
            return 0
        movement = "MOVE " + str(attacker.entityId) + " " + str(factory.entityId) + " " + str(factory.numCyborgs + 1)

        #if attacker.production < 3:
            #movement += ";INC " + str(attacker.entityId)
        print(movement)
    '''
    def bomb_strategy(self):
        enemyTargetBomb = []
        if self.bombs <= 0:
            return []
        for enemyFactory in self.enemyfactories:
            if enemyFactory.numCyborgs > 20:
                enemyTargetBomb.append(enemyFactory)
        return enemyTargetBomb

    def action(self):
        points = None
        factory = None
        for fact in self.neutralfactories + self.enemyfactories:
            fact_point = self.factory_puntuation(fact)
            if points is None or points < fact_point:
                points = fact_point
                factory = fact
        if factory is None:
            moviment = ""
            for p in self.myfactories:
                if p.production < 3:
                    moviment += ";INC " + str(p.entityId)
            print(moviment if moviment!='' else 'WAIT')
            return 0
        attacker = self.nearest_attacker(factory)
        if attacker is None:
            print("WAIT")
            return 0
        movement = "MOVE " + str(attacker.entityId) + " " + str(factory.entityId) + " " + str(factory.numCyborgs + 1)
        enemysTargetBomb = self.bomb_strategy()
        if enemysTargetBomb != []:
            prnt(enemysTargetBomb)
            for enemyTargetBomb in enemysTargetBomb:
                movement += ";BOMB " + str(attacker.entityId) + " " +str(enemyTargetBomb.entityId)
                self.bombs -= 1
        print(movement)


    def movement_puntuation(self, movement):
        movs = movement.split(" ")
        if movs[0] == "MOVE":
            suma_numCyborgs = sum([fact.numCyborgs for fact in self.myfactories])
            numCyborgs = suma_numCyborgs - self.factories[int(movs[2])].numCyborgs
            for fact in self.myfactories:
                if fact.entityId != int(movs[2]):
                    numCyborgs += max(fact.calculate_n(self), self.t) * fact.production
                else:
                    try:
                        dist = distances[int(movs[2])][int(movs[1])]
                    except KeyError:
                        dist = distances[int(movs[1])][int(movs[2])]
                    numCyborgs += (max(fact.calculate_n(self), self.t) - dist) * fact.production
        elif movs[0] == "WAIT":
            numCyborgs = sum([fact.numCyborgs for fact in self.myfactories])
            for fact in self.myfactories:
                numCyborgs += max(fact.calculate_n(self), self.t) * fact.production
        return numCyborgs


# Carga de la infomacion inicial
factory_count = int(input())  # the number of factories
link_count = int(input())  # the number of links between factories
distances = {}
maxd = 0
for i in range(link_count):
    factory_1, factory_2, distance = [int(j) for j in input().split()]
    distances.setdefault(factory_1, {factory_2: distance})
    distances[factory_1][factory_2] = distance
    if distance > maxd:
        maxd = distance
Bot(factory_count, distances, maxd).run()
