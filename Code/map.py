from dataclasses import dataclass
import pygame , pytmx , pyscroll
from player import NPC

@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group : pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    npcs :list[NPC]

class MapManager:
    def __init__(self,game,screen,player):
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.game = game
        self.current_map = "world"
        self.register_map("world",portals=[
            Portal(from_world="world",origin_point="enter_house",target_world="house",teleport_point="spawn_house"),
            Portal(from_world="world", origin_point="enter_house2", target_world="house2", teleport_point="spawn_house"),
            Portal(from_world="world", origin_point="enter_world2", target_world="world2", teleport_point="spawn_house"),
        ],npcs=[
            NPC("paul",nb_points=4,dialog =  [
    "Salut Dima, bienvenue dans la brigade forestière !",
    "Merci Sacha, ravi d’être ici.",
    "La forêt est belle mais exigeante. Bonne chance.",
    "Je ferai de mon mieux !",
    "Si besoin, viens me voir au poste de guet.",
    "Compris, je te ferai signe.",
    "Rapports bizarres à l’hôpital nord.",
    "Bizarres ? Quel genre ?",
    "Bruits et lumières la nuit. Reste prudent.",
    "Je ferai attention. Merci !",
    "Bonne chance, Dima !"
]),
        ])
        self.register_map("house",portals=[
            Portal(from_world="house", origin_point="exit_house", target_world="world", teleport_point="enter_house_exit")
        ],npcs=[
            NPC("robin",nb_points=2,dialog=[
    "Dima, un instant…",
    "J’ai reçu des rapports étranges.",
    "Cette ruine est dans notre secteur.",
    "Inspecte l’hôpital chaque semaine.",
    "Ne traîne pas, rapporte tout détail.",
    "Compris ? Mission prioritaire."
]),
        ])
        self.register_map("house2",portals=[
            Portal(from_world="house2", origin_point="exit_house", target_world="world",teleport_point="exit_house2")
        ])
        self.register_map("world2", portals=[
            Portal(from_world="world2", origin_point="exit_house", target_world="world", teleport_point="exit_world2"),
            Portal(from_world="world2", origin_point="enter_house3", target_world="hospital",teleport_point="spawn_house")
        ])
        self.register_map("hospital", portals=[
            Portal(from_world="hospital", origin_point="exit_house", target_world="world2", teleport_point="exit_world3")
        ])
        self.register_map("secret_room")
        self.teleport_player("player")
        self.teleport_npcs()

    def check_npc_collisions(self,dialog_box):
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:
                dialog_box.execute(sprite.dialog)


    def check_collisions(self):
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x,point.y,point.width,point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)

        try:
            lock_zone = self.get_object("lock_zone")
            lock_rect = pygame.Rect(lock_zone.x, lock_zone.y, lock_zone.width, lock_zone.height)

            if self.player.feet.colliderect(lock_rect):
                if not self.game.lockpick_mini.active:
                    self.game.lockpick_mini.map_manager = self
                    self.game.lockpick_mini.start()
        except Exception:
            pass


        for sprite in self.get_group().sprites():

            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 1


            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def teleport_player(self,name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_loaction()

    def register_map(self,name,portals=[],npcs=[]):
        tmx_data = pytmx.util_pygame.load_pygame(f"../Map/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        group.add(self.player)

        for npc in npcs:
            group.add(npc)

        self.maps[name] = Map(name,walls,group,tmx_data,portals,npcs)

    def get_map(self): return self.maps[self.current_map]

    def get_group(self): return self.get_map().group

    def get_walls(self): return self.get_map().walls

    def get_object(self,name): return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_npcs(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs
            for npc in npcs:
               npc.loads_point(map_data.tmx_data)
               npc.teleport_spawn()

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()

        self.game.audio.play_for_map(self.current_map)

        for npc in self.get_map().npcs:
            npc.move()

        self.game.minigame2.update()

        self.game.minigame2.teleport_to_secret_room(self)
