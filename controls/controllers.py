import pygame

from entities.buildings import CoalDrill, EnergyDissipator
from entities.resources import Resource
from gui.pointers import BuildingPlacer
from entities.coordinates import Vector

class Controller:
    def __init__(self, game, gui=None):
        self.game = game
        self.gui = gui

    def process(self, events):
        return


class CharacterController(Controller):
    def process(self, events):
        if self.game.paused:
            return

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            self.game.character.move(Vector(0, -4))
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            self.game.character.move(Vector(0, 4))
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            self.game.character.move(Vector(-4, 0))
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.game.character.move(Vector(4, 0))

        # reuse this for tile selection & highlighting
        # mouse_up_events = [event for event in events if event.type == pygame.MOUSEBUTTONUP]
        # if len(mouse_up_events) > 0:
        #     last = mouse_up_events[-1]
        #     if last.button == 1:
        #         mx, my = last.pos
        #         self.game.tile_grid.remove_tile(mx, my)

        if pygame.mouse.get_pressed() == (1, 0, 0):
            if self.game.construction_mode:
                return

            mpos = pygame.mouse.get_pos()
            tile = self.game.tile_grid.get_tile(mpos)

            if tile and isinstance(tile, Resource):
                self.game.character.mine(tile)


class MainMenuController(Controller):
    def process(self, events):
        if self.game.construction_mode:
            return

        for event in events:
            if event.type == pygame.QUIT:
                self.game.quit = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.paused ^= True
                self.gui.hidden ^= True

            if not self.gui.hidden and event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.game.quit = True


class CharacterInventoryController(Controller):
    def process(self, events):
        if self.game.paused:
            return

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                self.gui.hidden ^= True


class ConstructionController(Controller):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.building_placer = None

    def process(self, events):
        if self.game.paused:
            return

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                self.gui.hidden ^= True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                if self.game.construction_mode:
                    self.disable_construction_mode()
                self.enable_construction_mode(CoalDrill)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if self.game.construction_mode:
                    self.disable_construction_mode()
                self.enable_construction_mode(EnergyDissipator)
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q):
                if self.game.construction_mode:
                    self.disable_construction_mode()

        if pygame.mouse.get_pressed() == (1, 0, 0):
            if not self.game.construction_mode:
                return

            self.construct_building()

    def enable_construction_mode(self, building_type):
        if not building_type.is_affordable(self.game.character.inventory):
            return

        mpos = pygame.mouse.get_pos()
        building = building_type(self.game, Vector(*mpos))

        self.building_placer = BuildingPlacer(game=self.game, building=building)
        self.game.interfaces.append(self.building_placer)
        self.game.construction_mode = True

    def disable_construction_mode(self):
        self.game.interfaces.remove(self.building_placer)
        self.building_placer = None
        self.game.construction_mode = False

    def construct_building(self):
        if not self.game.construction_mode:
            return

        building = self.building_placer.building
        self.game.character.construct(building)
        self.disable_construction_mode()
