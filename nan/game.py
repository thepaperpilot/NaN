import scenebase
import math
import pygame
import esper
import components
import processors
import interpolation
import game

class GameScene(scenebase.SceneBase):
    def __init__(self):
        scenebase.SceneBase.__init__(self)

    def init(self):
        player = self.world.create_entity()
        self.world.add_component(player, components.Position(100, 100))
        self.world.add_component(player, components.Velocity(0, 0))
        self.world.add_component(player, components.Image("player.png"))
        self.world.add_component(player, components.Size(64, 32))
        self.world.add_component(player, components.Player())

        self.world.add_processor(processors.ClickProcessor(), priority=10)
        self.world.add_processor(processors.RenderProcessor())
        self.world.add_processor(processors.OverProcessor(), priority=10)
        self.world.add_processor(processors.VelocityProcessor(), priority=5)
        self.world.add_processor(processors.AnimationProcessor(), priority=5)
        self.world.add_processor(processors.PlayerProcessor(player), priority=25)
