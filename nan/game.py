import scenebase
import math
import pygame
import esper
import components
import processors
import interpolation
import game
import random

class GameScene(scenebase.SceneBase):
    def __init__(self):
        scenebase.SceneBase.__init__(self)

    def init(self):
        player = self.world.create_entity()
        image = components.Image("playerIdle.png")
        animation = components.Animation("playerSimple.png", splitx=8, framelength=.1)
        self.world.add_component(player, components.Position(100, 100))
        self.world.add_component(player, components.Velocity(0, 0))
        self.world.add_component(player, image)
        self.world.add_component(player, components.Size(64, 64))
        self.world.add_component(player, components.Player(image, animation))

        for i in [1,2,3,4,5,6]:
            cloud = self.world.create_entity()
            self.world.add_component(cloud, components.Position(random.randrange(200, 1080), random.randrange(75, 125)))
            #self.world.add_component(cloud, components.Image("cloud.png", blend=pygame.BLEND_RGBA_MAX))
            self.world.add_component(cloud, components.Image("cloud.png"))
            self.world.add_component(cloud, components.Size(192, 96))

        self.world.add_processor(processors.ClickProcessor(), priority=10)
        self.world.add_processor(processors.RenderProcessor())
        self.world.add_processor(processors.OverProcessor(), priority=10)
        self.world.add_processor(processors.VelocityProcessor(), priority=5)
        self.world.add_processor(processors.AnimationProcessor(), priority=5)
        self.world.add_processor(processors.PlayerProcessor(player), priority=25)
