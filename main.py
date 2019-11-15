import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.ids.unit_typeid import UnitTypeId



async def postavnexus(self):


    if self.can_afford(UnitTypeId.NEXUS) and self.already_pending(UnitTypeId.NEXUS) + self.units.filter(
        lambda structure: structure.type_id == UnitTypeId.NEXUS and structure.is_ready).amount == 0:
        worker_candidates = self.workers.filter(lambda worker: (worker.is_collecting or worker.is_idle) and worker.tag not in self.unit_tags_received_action)
        # Worker_candidates can be empty
        if worker_candidates:
            placement_position = await self.get_next_expansion()
            # poslat workera na vylet k nejblizsi expansion
            jednotka = worker_candidates.closest_to(placement_position)
            if placement_position:
                build_worker = jednotka
                self.do(build_worker.build(UnitTypeId.NEXUS, placement_position))

async def producing_probes(self):
    for workerBuilding in self.townhalls.idle:
         if self.can_afford(UnitTypeId.PROBE):
            self.do(workerBuilding.train(UnitTypeId.PROBE), subtract_cost=True, subtract_supply=True)

async def postavassimilator(self):
    if self.can_afford(UnitTypeId.ASSIMILATOR):
        #for mainBuilding in self.structures(UnitTypeId.NEXUS).ready:
            #pozice = await self.find_placement(UnitTypeId.ASSIMILATOR, near=mainBuilding)

        worker_candidates = self.workers.filter(lambda worker: (worker.is_collecting or worker.is_idle) and worker.tag not in self.unit_tags_received_action)
        if worker_candidates:
            placement_position =  await self.find_placement(UnitTypeId.ASSIMILATOR, near=self.start_location)
            print(str(placement_position))
            jednotka = worker_candidates.closest_to(placement_position)
            await self.build(UnitTypeId.ASSIMILATOR, near=placement_position, max_distance=40, placement_step=2)



async def build_pylons(self):
    if self.can_afford(UnitTypeId.PYLON) and ((self.supply_left <= 2) or (self.supply_left <= 2*(len(self.structures(UnitTypeId.NEXUS)) + len(self.structures(UnitTypeId.GATEWAY))))):
        if self.can_afford(UnitTypeId.PYLON) and self.already_pending(UnitTypeId.PYLON) + self.units.filter(lambda structure: structure.type_id == UnitTypeId.PYLON and structure.is_ready).amount == 0:
            map_center = self.game_info.map_center

            position_towards_map_center = self.start_location.towards(map_center, distance=5)
            self.do(self.build(UnitTypeId.PYLON, near=position_towards_map_center, placement_step=1))


async def zealot(self):
    for gw in self.structures(UnitTypeId.GATEWAY).ready.idle:
        if self.can_afford(UnitTypeId.ZEALOT):
            self.do(gw.train(UnitTypeId.ZEALOT), subtract_cost=True, subtract_supply=True)

async def producing_probes(self):
    for workerBuilding in self.townhalls.idle:
        if self.can_afford(UnitTypeId.PROBE):
            self.do(workerBuilding.train(UnitTypeId.PROBE), subtract_cost=True, subtract_supply=True)

async def build_gateway(self):
    if self.can_afford(UnitTypeId.GATEWAY) and self.already_pending(UnitTypeId.GATEWAY) + self.units.filter(lambda structure: structure.type_id == UnitTypeId.PYLON and structure.is_ready).amount == 0 and len(self.structures(UnitTypeId.GATEWAY)) < 2+ 3*(len(self.structures(UnitTypeId.NEXUS)) -1):
        map_center = self.game_info.map_center
        position_towards_map_center = self.start_location.towards(map_center, distance=5)
        await self.build(UnitTypeId.GATEWAY, near=position_towards_map_center, placement_step=1)

async def ATTACK_FOR_AIUR(self):

    if self.units(UnitTypeId.ZEALOT).amount > 10:
        for z in self.units(UnitTypeId.ZEALOT):
            self.do(z.attack(self.enemy_start_locations[0]))

class Codelat(sc2.BotAI):
    print("Vse funguje zatiiiiim jak ma")

    # 1. vsichni boti sbiraji
    async def on_step(self, iteration: int):

        await self.distribute_workers()

        #print(str(await self.find_placement(UnitTypeId.ASSIMILATOR, near=self.start_location)))
        #await postavassimilator(self)
        await producing_probes(self)
        await build_pylons(self)
        await postavnexus(self)
        await build_gateway(self)
        await zealot(self)
        await ATTACK_FOR_AIUR(self)


nefunkcniKod = """
if len(self.structures(UnitTypeId.PYLON)) >= 4:
    if len(self.townhalls) >= 2:
        #position_towards_map_centerEXPO = self.expansion_locations[1].towards(map_center, distance=5)
        await self.build(UnitTypeId.PYLON, near=self.expansion_locations[1], placement_step=1)
    else:
        #position_towards_map_center = self.townhalls[0].towards(map_center, distance=5)"""
# Game start
run_game(maps.get("Acropolis LE"), [
    Bot(Race.Protoss, Codelat()),
    Computer(Race.Terran, Difficulty.Easy)
], realtime=False)
