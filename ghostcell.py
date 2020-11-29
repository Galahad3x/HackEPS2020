import sys
import math

# Clase Factory encargada de representar las factorias del juego
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

    # Factor de peligro: Probabilidad de que el enemigo robe esta factory
    def danger_factor(self, bot):
        enemy_value = bot.factory_puntuation(self, ally=False)
        in_min = out_min = 0
        in_max = bot.max_enemy_puntuation(self)
        out_max = 100
        x = enemy_value
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    # Calcula n: Calcular los dias aproximador que tardara el enemigo a robar-nos una factory
    def calculate_n(self, bot):
        superior = math.log(math.e, bot.assumed_losing_prob)
        inferior = math.log(math.e, 100 - self.danger_factor(bot))
        prnt(inferior)
        return int(round((superior / inferior) / 100))
'''  
    Clase Troop encargada de representar las tropas del juego 
'''
class Troop:
    def __init__(self, entityId, entityType, owner, leaving, target, numCyborgs, remainingTurns):
        self.entityId = entityId
        self.entityType = entityType
        self.owner = owner
        self.leaving = leaving
        self.target = target
        self.numCyborgs = numCyborgs
        self.remainingTurns = remainingTurns
''' 
    Clase encargada de decidir las las accciones a realizar en el juego   
'''
class Bot:
    def __init__(self, factoryCount, distances, max_dist):
        self.factoryCount = factoryCount
        self.distances = distances
        self.factories = {}
        self.troops = {}
        self.pond = [10, 1, 1, 1,-10] # Ponderaciones para el calculo de las puntuaciones de las factorias
        self.t = 20
        self.assumed_losing_prob = 0.05
        self.max_dist = max_dist
        self.myfactories = None
        self.enemyfactories = None
        self.neutralfactories = None
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

    def get_myfactories(self):
        return [factorie for factorie in self.factories.values() if factorie.owner == 1]

    def get_enemyfactories(self):
        return [factorie for factorie in self.factories.values() if factorie.owner == -1]

    def get_neutralfactories(self):
        return [factorie for factorie in self.factories.values() if factorie.owner == 0]

    def max_enemy_puntuation(self, factory):
        return self.pond[0] + self.pond[1] * self.max_dist + self.pond[2] * 3 + self.pond[4]

    # Calcula la puntuacion la factoria en funcion de la ponderación
    def factory_puntuation(self, factory):
        # De cara el bot
        ally_dist = factory.nearest_distance(self.distances, self.myfactories)
        enemy_dist = factory.nearest_distance(self.distances, self.enemyfactories)
        prod = factory.production
        if factory.numCyborgs != 0:
            cybs = self.pond[3] / factory.numCyborgs
        else:
            cybs = 0
        owner = -factory.owner
        #
        if ally_dist is None or enemy_dist is None:
            return 0
        return self.pond[0] / ally_dist + self.pond[1] * enemy_dist + self.pond[2] * prod + cybs + self.pond[4] * owner

    # Determina la factoria mas cercana valida
    def nearest_attacker(self, factory):
        distance_attacker = None
        attacker = None
        for fact in self.myfactories:
            try:
                dist = self.distances[factory.entityId][fact.entityId]
            except KeyError:
                dist = self.distances[fact.entityId][factory.entityId]
            if distance_attacker is None or dist < distance_attacker:
                if factory.owner == 0:
                    if fact.numCyborgs > factory.numCyborgs:
                        attacker = fact
                        distance_attacker = dist
                elif factory.owner == -1:
                    producedCyborgs = dist * factory.production
                    if fact.numCyborgs > factory.numCyborgs + producedCyborgs:
                        attacker = fact
                        distance_attacker = dist
        return attacker

    # Cualquier de nuestras factories
    def any_attacker(self, factory):
        attacker = []
        for fact in self.myfactories:
            if fact.numCyborgs > factory.numCyborgs:
                attacker.append(fact)
        return attacker

    # Implementación de la utilizacion de las bombas
    def bomb_strategy(self):
        enemyTargetBomb = []
        if self.bombs <= 0:
            return []
        for enemyFactory in self.enemyfactories:
            if enemyFactory.numCyborgs > 5:
                enemyTargetBomb.append(enemyFactory)
                self.bombs -= 1
        return enemyTargetBomb

    # Estrategia del incrementos de produccion de las factorias
    def inc_strategy(self):
        incTarget = []
        for myFactory in self.myfactories:
            if myFactory.production < 3:
                incTarget += ["INC " + str(myFactory.entityId)]
        return incTarget

    # Estratagia
    def neutral_strategy(self):
        movements = []
        myFactories = self.myfactories
        if(len(myFactories)==0):
            return []
        for neutralFactory in self.neutralfactories:
            noTroops = True
            for troop in self.troops.values():
                if troop.target == neutralFactory.entityId:
                    noTroops = False
                    break
            if noTroops and myFactories[0].numCyborgs > 1 :
                movements += ["MOVE " + str(myFactories[0].entityId) + " " + str(neutralFactory.entityId) + " 1"]
                myFactories[0].numCyborgs -= 1
        return movements

    # Estrategia de ayuda a las factorias que van a ser atacadas
    def help_factories_strategy(self):
        movements = []
        for currentFactory in self.myfactories:
            nCyborgs = 0
            for troop in self.troops.values():
                if troop.target == currentFactory.entityId:
                    nCyborgs += 1
            if nCyborgs == 0:
                continue
            for factory in self.myfactories:
                if currentFactory.entityId != factory.entityId and currentFactory.numCyborgs > nCyborgs:
                    movements += ["MOVE " + str(currentFactory.entityId) + " " + str(factory.entityId) + " 1"]
                    currentFactory.numCyborgs -= nCyborgs
        return movements

    # metodo encargado de realizar las acciones indicadas por las diferentes estrategias
    def action(self):
        points = None
        factory = None
        movements = []

       # Busqueda de la factoria con mas puntuacion
        for fact in self.neutralfactories + self.enemyfactories:
            fact_point = self.factory_puntuation(fact)
            if points is None or points < fact_point:
                points = fact_point
                factory = fact

        #Se comprueba si hay una factoria enemiga objetivo, sino la hay se ha ganado
        if factory is None:
            print("WAIT")
            return 0

        #Estrategia de mejora de la produccion
        movements += self.inc_strategy()

        #Se busca la factoria mas cercana a la factoria enemiga objetivo
        attacker = self.nearest_attacker(factory)

        # Si la factoria mas cercana no tienen recursos suficientes se procede a ayudar a las factorias aliadas
        if attacker is None:
            movements += self.help_factories_strategy()
            print(';'.join(movements) if movements != [] else "WAIT")
            return 0
        # En caso contrario se crea una tropa cuyo target es factoria con mas puntuacion
        movements += ["MOVE " + str(attacker.entityId) + " " + str(factory.entityId) + " " + str(factory.numCyborgs + 1)]

        # Se aplica la estrategia de utilizar bombas si es necesario
        enemysTargetBomb = self.bomb_strategy()
        if enemysTargetBomb != []:
            prnt(enemysTargetBomb)
            for enemyTargetBomb in enemysTargetBomb:
                movements += ["BOMB " + str(attacker.entityId) + " " +str(enemyTargetBomb.entityId)]
        print(";".join(movements) if movements != [] else "WAIT")
        return 0

# funcion que realiza prints sobre la salida stderr ya que la salida estandar esta ocupada
def prnt(toprint):
    print(toprint, file=sys.stderr, flush=True)

def main():
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

if __name__ == "__main__":
    main()
