import pygame
from enum import IntEnum
from pygame import Rect
from pygine.entities import *
from pygine.input import InputType, pressed
from pygine.maths import Vector2
from pygine.structures import QuadTree
from pygine.transitions import Pinhole, TransitionType
from pygine.utilities import Camera
from random import randint


class SceneType(IntEnum):
    EXAMPLE = 0


class SceneManager:
    def __init__(self):
        self.__reset()

    def get_scene(self, scene_type):
        return self.__all_scenes[int(scene_type)]

    def get_current_scene(self):
        return self.__current_scene

    def __reset(self):
        self.__all_scenes = []
        self.__current_scene = None
        self.__previous_scene = None
        self.__next_scene = None
        self.leave_transition = None
        self.enter_transition = None
        self.start_transition = False

        self.__initialize_scenes()
        self.__set_starting_scene(SceneType.EXAMPLE)

    def __add_scene(self, scene):
        self.__all_scenes.append(scene)
        scene.manager = self

    def __initialize_scenes(self):
        self.__all_scenes = []
        self.__add_scene(Example())

    def __set_starting_scene(self, starting_scene_type):
        assert (len(self.__all_scenes) > 0), \
            "It looks like you never initialized all the scenes! Make sure to setup and call __initialize_scenes()"

        self.__current_scene = self.__all_scenes[int(starting_scene_type)]
        self.__current_scene.relay_player(
            Player(
                Camera.BOUNDS.width / 2 - 3,
                Camera.BOUNDS.height / 2 - 8
            )
        )

    def __setup_transition(self):
        if self.__previous_scene.leave_transition_type == TransitionType.PINHOLE_CLOSE:
            self.leave_transition = Pinhole(TransitionType.PINHOLE_CLOSE)

        if self.__next_scene.enter_transition_type == TransitionType.PINHOLE_OPEN:
            self.enter_transition = Pinhole(TransitionType.PINHOLE_OPEN)

        self.start_transition = True

    def queue_next_scene(self, scene_type):
        self.__previous_scene = self.__current_scene
        self.__next_scene = self.__all_scenes[int(scene_type)]
        self.__setup_transition()

    def __change_scenes(self):
        self.__current_scene = self.__next_scene

    def __update_input(self, delta_time):
        if pressed(InputType.RESET):
            self.__reset()

    def __update_transition(self, delta_time):
        if self.start_transition:
            self.leave_transition.update(delta_time)
            if self.leave_transition.done:
                self.enter_transition.update(delta_time)
                self.__change_scenes()

    def update(self, delta_time):
        assert (self.__current_scene != None), \
            "It looks like you never set a starting scene! Make sure to call __set_starting_scene(starting_scene_type)"

        self.__update_input(delta_time)
        self.__update_transition(delta_time)
        self.__current_scene.update(delta_time)

    def __draw_transitions(self, surface):
        if self.start_transition:
            if self.leave_transition != None and not self.leave_transition.done:
                self.leave_transition.draw(surface)
                if self.leave_transition.done:
                    self.enter_transition.draw(surface)
            else:
                self.enter_transition.draw(surface)

    def draw(self, surface):
        assert (self.__current_scene != None), \
            "It looks like you never set a starting scene! Make sure to call __set_starting_scene(starting_scene_type)"

        self.__current_scene.draw(surface)
        self.__draw_transitions(surface)


class Scene(object):
    VIEWPORT_BUFFER = 32

    def __init__(self):
        self.camera = Camera()
        self.camera_location = Vector2(0, 0)
        self.bounds = Rect(0, 0, Camera.BOUNDS.width, Camera.BOUNDS.height)
        self.camera_viewport = Rectangle(
            -Scene.VIEWPORT_BUFFER, -Scene.VIEWPORT_BUFFER,
            Camera.BOUNDS.width + Scene.VIEWPORT_BUFFER * 2,
            Camera.BOUNDS.height + Scene.VIEWPORT_BUFFER * 2,
            Color.RED,
            2
        )
        self.entities = []  
        self.sprites = []      
        self.shapes = []
        self.triggers = []
        self.entity_quad_tree = QuadTree(self.bounds, 4)
        self.sprite_quad_tree = QuadTree(self.bounds, 4)        
        self.shape_quad_tree = QuadTree(self.bounds, 4)
        self.query_result = None
        self.leave_transition_type = TransitionType.PINHOLE_CLOSE
        self.enter_transition_type = TransitionType.PINHOLE_OPEN
        self.manager = None
        self.player = None
    
    def set_scene_bounds(self, bounds):
        self.bounds = bounds
        self.sprite_quad_tree = QuadTree(self.bounds, 4)
        self.entity_quad_tree = QuadTree(self.bounds, 4)
        self.shape_quad_tree = QuadTree(self.bounds, 4)

    def relay_player(self, player):
        self.player = player
        self.entities.append(self.player)

    def relay_entity(self, entity):
        self.entities.append(entity)
        # We can potentially add aditional logic for certain entites. For example, if the entity is a NPC then spawn it at (x, y)

    def _reset(self):
        raise NotImplementedError(
            "A class that inherits Scene did not implement the reset() method")

    def _create_triggers(self):
        raise NotImplementedError(
            "A class that inherits Scene did not implement the create_triggers() method")

    def __update_spatial_indexing(self):
        if self.sprite_quad_tree == None:     
            for i in range(len(self.sprites)):
                self.sprite_quad_tree.insert(self.sprites[i])
        
        if self.shape_quad_tree == None:          
            for i in range(len(self.shapes)):
                self.shape_quad_tree.insert(self.shapes[i])
    
        self.entity_quad_tree.clear()        
        for i in range(len(self.entities)):
            self.entity_quad_tree.insert(self.entities[i])          

    def __update_entities(self, delta_time):
        for i in range(len(self.entities)-1, -1, -1):
            self.entities[i].update(
                delta_time, self.entities, self.entity_quad_tree)
        self.entities.sort(key=lambda e: e.y + e.height)

    def __update_triggers(self, delta_time):
        for t in self.triggers:
            t.update(delta_time, self.entities, self.manager)

    def __update_camera(self):
        self.camera_location = Vector2(
            self.player.x + self.player.width / 2 - self.camera.BOUNDS.width / 2,
            self.player.y + self.player.height / 2 - self.camera.BOUNDS.height / 2
        )
        self.camera.update(self.camera_location, self.bounds)
        self.camera_viewport.set_location(
            self.camera.get_viewport_top_left().x - Scene.VIEWPORT_BUFFER,
            self.camera.get_viewport_top_left().y - Scene.VIEWPORT_BUFFER)

    def update(self, delta_time):
        self.__update_spatial_indexing()
        self.__update_entities(delta_time)
        self.__update_triggers(delta_time)
        self.__update_camera()

    def draw(self, surface):
        if globals.debugging:
            self.entity_quad_tree.draw(surface)

            for t in self.triggers:
                t.draw(surface, CameraType.DYNAMIC)

        self.query_result = self.shape_quad_tree.query(self.camera_viewport.bounds)
        for s in self.shapes:
            s.draw(surface, CameraType.DYNAMIC)

        self.query_result = self.sprite_quad_tree.query(self.camera_viewport.bounds)            
        for s in self.sprites:
            s.draw(surface, CameraType.DYNAMIC)

        self.query_result = self.entity_quad_tree.query(self.camera_viewport.bounds)
        for e in self.query_result:
            e.draw(surface)    


class Example(Scene):
    def __init__(self):
        super(Example, self).__init__()
        self._reset()
        self._create_triggers()

    def _reset(self):
        self.set_scene_bounds(Rect(0, 0, Camera.BOUNDS.width * 2, Camera.BOUNDS.height))
        self.entities = []

        for i in range(0, 32):
            self.entities.append(Block(
                randint(16, self.bounds.width - 16), randint(16, self.bounds.height - 16)))

    def _create_triggers(self):
        self.triggers = []
