import sys
import math
#e = 2.718281

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
        
    def nearest_distance(self, distances, factories):
        distance = None
        for fact in factories:
            if fact.entityId == self.entityId:
                continue
            try:
                dist = distances[self.entityId][fact.entityId]
            except KeyError:
                dist = distances[fact.entityId][self.entityId]
            if distance is None or dist < distance:
                distance = dist
        return distance
        
    def danger_factor(self, bot):
        enemy_value = bot.factory_puntuation(self,ally=False)
        in_min = out_min = 0
        in_max = bot.max_enemy_puntuation(self)
        out_max = 100
        x = enemy_value
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        
    def calculate_n(self, bot):
        superior = math.log(math.e, bot.assumed_losing_prob)
        prnt(inferior)
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
        self.pond = [1,1,1,1,1]
        self.t = 20
        self.assumed_losing_prob = 0.05
        self.max_dist = max_dist
        self.myfactories = None
        self.enemyfactories = None
        self.neutralfactories = None
       
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
                    self.factories[entity_id]= Factory(entity_id,entity_type,arg_1,arg_2,arg_3)
                if entity_type == "TROOP":
                    self.troops[entity_id] = Troop(entity_id, entity_type, arg_1, arg_2, arg_3,arg_4,arg_5)
            self.myfactories = self.get_myfactories()
            self.enemyfactories = self.get_enemyfactories()
            self.neutralfactories = self.get_neutralfactories()
            self.action()

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
        return  self.pond[0] / ally_dist + self.pond[1] * enemy_dist + self.pond[2] * prod + cybs + self.pond[4] * owner

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
        distance = None
        attacker = None
        for fact in self.myfactories:
            try:
                dist = distances[factory.entityId][fact.entityId]
            except KeyError:
                dist = distances[fact.entityId][factory.entityId]
            if distance is None or dist < distance:
                if fact.numCyborgs > factory.numCyborgs:
                    attacker = fact
                    distance = dist
        return attacker
                    
                    
    def action(self):
        val = None
        factory = None
        for fact in self.neutralfactories + self.enemyfactories:
            calculated_val = self.factory_puntuation(fact)
            if val is None or val < calculated_val:
                val = calculated_val
                factory = fact
        if self.nearest_attacker(factory) is None:
            return "WAIT"
        movement = "MOVE " + str(self.nearest_attacker(factory).entityId) + " " + str(factory.entityId) + " " + str(factory.numCyborgs + 1)
        # if self.movement_puntuation(movement) >= self.movement_puntuation("WAIT"):
        print(movement)
            
                      

# Carga de la infomacion inicial
factory_count = int(input())  # the number of factories
link_count = int(input())  # the number of links between factories
distances = {}
maxd = 0
for i in range(link_count):
    factory_1, factory_2, distance = [int(j) for j in input().split()]
    distances.setdefault(factory_1,{factory_2: distance})
    distances[factory_1][factory_2] = distance
    if distance > maxd:
        maxd = distance
Bot(factory_count, distances, maxd).run()

