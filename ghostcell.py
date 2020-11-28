import sys
import math

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
        
class Troop:
    def __init__(self, entityId, entityType, owner, leaving, target, nCyborgs, remainingTurns):
        self.entityId = entityId
        self.entityType = entityType
        self.owner = owner
        self.leaving = leaving
        self.target = target
        self.nCyborgs = nCyborgs
        self.remainingTurns = remainingTurns

class Bot:
    def __init__(self, factoryCount, distances):
        self.factoryCount = factory_count
        self.distances = distances
        self.factories = {}
        self.troops = {}
       
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
            self.action(None)

    def get_myfactories(self):
        return [factorie for factorie in self.factories.values() if factorie.owner == 1]

    def get_enemyfactories(self):
        return [factorie for factorie in self.factories.values() if factorie.owner == -1]

    def get_neutralfactories(self):
        return [factorie for factorie in self.factories.values() if factorie.owner == 0]

    def factory_puntuation(self, factory):
        return 0

    def action(self, factory_puntuation):
        print('WAIT')
                      

# Carga de la infomacion inicial
factory_count = int(input())  # the number of factories
link_count = int(input())  # the number of links between factories
distances = {}
for i in range(link_count):
    factory_1, factory_2, distance = [int(j) for j in input().split()]
    distances.setdefault(factory_1,{factory_2: distance})
    distances[factory_1][factory_2] = distance
Bot(factory_count, distances).run()

