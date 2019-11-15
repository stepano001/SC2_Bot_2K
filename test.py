import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.ids.unit_typeid import UnitTypeId



async def postavnexus(self):
    if self.can_afford(UnitTypeId.NEXUS) and self.already_pending(UnitTypeId.NEXUS) + self.units.filter(lambda structure: structure.type_id == UnitTypeId.NEXUS and structure.is_ready).amount == 0:
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
        for mainBuilding in self.structures(UnitTypeId.NEXUS).ready:
            worker_candidates = self.workers.filter(lambda worker: (worker.is_collecting or worker.is_idle) and worker.tag not in self.unit_tags_received_action)
            if worker_candidates:
                placement_position = self.vespene_geyser.closest_to(mainBuilding)
                jednotka = worker_candidates.closest_to(placement_position)
                self.do(jednotka.build(UnitTypeId.ASSIMILATOR, placement_position))





async def build_pylons(self):
    if self.can_afford(UnitTypeId.PYLON) and ((self.supply_left <= 2) or (self.supply_left <= 2*(len(self.structures(UnitTypeId.NEXUS)) + len(self.structures(UnitTypeId.GATEWAY))))):
        if self.can_afford(UnitTypeId.PYLON) and self.already_pending(UnitTypeId.PYLON) + self.units.filter(lambda structure: structure.type_id == UnitTypeId.PYLON and structure.is_ready).amount == 0:
            map_center = self.game_info.map_center
            position_towards_map_center = self.start_location.towards(map_center, distance=5)
            await self.build(UnitTypeId.PYLON, near=position_towards_map_center, placement_step=1)


async def zealotAndArmy(self):
    for gw in self.structures(UnitTypeId.GATEWAY).ready.idle:
        if self.can_afford(UnitTypeId.DARKTEMPLAR) and len(self.structures(UnitTypeId.DARKSHRINE)) != 0:
            self.do(gw.train(UnitTypeId.DARKTEMPLAR), subtract_cost=True, subtract_supply=True)
        elif self.can_afford(UnitTypeId.ADEPT) and len(self.structures(UnitTypeId.CYBERNETICSCORE)) != 0:
            self.do(gw.train(UnitTypeId.ADEPT), subtract_cost=True, subtract_supply=True)
        elif self.can_afford(UnitTypeId.ZEALOT):
            self.do(gw.train(UnitTypeId.ZEALOT), subtract_cost=True, subtract_supply=True)

async def producing_probes(self):
    if self.supply_workers <= 90:
        for workerBuilding in self.townhalls.idle:
            if self.can_afford(UnitTypeId.PROBE):
                self.do(workerBuilding.train(UnitTypeId.PROBE), subtract_cost=True, subtract_supply=True)

async def build_gateway(self):
    if self.can_afford(UnitTypeId.GATEWAY) and self.already_pending(UnitTypeId.GATEWAY) + self.units.filter(lambda structure: structure.type_id == UnitTypeId.PYLON and structure.is_ready).amount == 0 and (len(self.structures(UnitTypeId.GATEWAY)) < 2+ 3*(len(self.structures(UnitTypeId.NEXUS)) -1) and len(self.structures(UnitTypeId.GATEWAY)) <= 12):
        map_center = self.game_info.map_center
        position_towards_map_center = self.start_location.towards(map_center, distance=5)
        await self.build(UnitTypeId.GATEWAY, near=position_towards_map_center, placement_step=1)

async def ATTACK_FOR_AIUR(self):
    if self.supply_army > 30:
        for z in self.units(UnitTypeId.ZEALOT):
            self.do(z.attack(self.enemy_start_locations[0]))
        for a in self.units(UnitTypeId.ADEPT):
            self.do(a.attack(self.enemy_start_locations[0]))
        for dt in self.units(UnitTypeId.DARKTEMPLAR):
            self.do(dt.attack(self.enemy_start_locations[0]))



async def techUp(self):
    if len(self.structures(UnitTypeId.GATEWAY)) >= 1 and self.can_afford(UnitTypeId.CYBERNETICSCORE) and len(self.structures(UnitTypeId.CYBERNETICSCORE)) < 1:
        map_center = self.game_info.map_center
        position_towards_map_center = self.start_location.towards(map_center, distance=5)
        await self.build(UnitTypeId.CYBERNETICSCORE, near=position_towards_map_center, placement_step=1)

    if len(self.structures(UnitTypeId.CYBERNETICSCORE)) == 1 and self.can_afford(UnitTypeId.TWILIGHTCOUNCIL) and len(self.structures(UnitTypeId.TWILIGHTCOUNCIL)) < 1:
        map_center = self.game_info.map_center
        position_towards_map_center = self.start_location.towards(map_center, distance=5)
        await self.build(UnitTypeId.TWILIGHTCOUNCIL, near=position_towards_map_center, placement_step=1)

    if len(self.structures(UnitTypeId.TWILIGHTCOUNCIL)) == 1 and self.can_afford(UnitTypeId.DARKSHRINE) and len(self.structures(UnitTypeId.DARKSHRINE)) < 1:
        map_center = self.game_info.map_center
        position_towards_map_center = self.start_location.towards(map_center, distance=5)
        await self.build(UnitTypeId.DARKSHRINE, near=position_towards_map_center, placement_step=1)



class Codelat(sc2.BotAI):
    print("Vse funguje zatiiiiim jak ma")


    # 1. vsichni boti sbiraji
    async def on_step(self, iteration: int):
        await self.distribute_workers()
        await producing_probes(self)
        await build_pylons(self)
        await postavnexus(self)
        await build_gateway(self)
        await zealotAndArmy(self)
        await techUp(self)
        if len(self.structures(UnitTypeId.PYLON)) >= 2:
            await postavassimilator(self)
        await ATTACK_FOR_AIUR(self)


nefunkcniKod = """
if len(self.structures(UnitTypeId.PYLON)) >= 4:
    if len(self.townhalls) >= 2:
        #position_towards_map_centerEXPO = self.expansion_locations[1].towards(map_center, distance=5)
        await self.build(UnitTypeId.PYLON, near=self.expansion_locations[1], placement_step=1)
    else:
        #position_towards_map_center = self.townhalls[0].towards(map_center, distance=5)"""
# Game start
run_game(maps.get("Abyssal Reef LE"), [
    Bot(Race.Protoss, Codelat()),
    Computer(Race.Terran, Difficulty.Medium)
], realtime=False)
