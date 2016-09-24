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
        self.font = pygame.font.Font("RobotoMono-Regular.ttf", 42)

        player = self.world.create_entity()
        image = components.Image("playerIdle.png")
        animation = components.Animation("playerSimple.png", splitx=8, framelength=.1)
        carry_image = components.Animation("playerCarryIdle.png", splitx=8, framelength=.1)
        carry_animation = components.Animation("playerCarrySimple.png", splitx=8, framelength=.1)
        self.world.add_component(player, components.Position(100, 100))
        self.world.add_component(player, components.Velocity(0, 0))
        self.world.add_component(player, image)
        self.world.add_component(player, components.Size(64, 64))
        self.world.add_component(player, components.Player(image, animation, carry_image, carry_animation))

        sword = self.world.create_entity()
        self.world.add_component(sword, components.Position(300, 500))
        self.world.add_component(sword, components.Velocity(0, 0))
        self.world.add_component(sword, components.Image("sword.png"))
        self.world.add_component(sword, components.Size(64, 64))

        def move_up(entity):
            self.world.add_component(entity, components.ChangePosition((640, 320), 1, interpolation.Smooth(), move_down, entity))

        def move_down(entity):
            self.world.add_component(entity, components.ChangePosition((640, 360), 1, interpolation.Smooth(), move_up, entity))

        tutorial = self.world.create_entity()
        image = self.font.render("press E to pick up your sword", False, (32, 255, 128))
        self.world.add_component(tutorial, components.Position(640, 360))
        self.world.add_component(tutorial, components.Image(image=image))
        self.world.add_component(tutorial, components.Size(image.get_width(), image.get_height()))
        move_up(tutorial)

        for i in [1,2,3,4,5,6]:
            cloud = self.world.create_entity()
            self.world.add_component(cloud, components.Position(random.randrange(100, 1180), random.randrange(75, 200)))
            #self.world.add_component(cloud, components.Image("cloud.png", blend=pygame.BLEND_RGBA_MAX))
            self.world.add_component(cloud, components.Image("cloud.png"))
            self.world.add_component(cloud, components.Size(192, 96))

        self.world.add_processor(processors.ClickProcessor(), priority=10)
        self.world.add_processor(processors.RenderProcessor())
        self.world.add_processor(processors.OverProcessor(), priority=10)
        self.world.add_processor(processors.VelocityProcessor(), priority=5)
        self.world.add_processor(processors.AnimationProcessor(), priority=5)
        self.world.add_processor(processors.PlayerProcessor(player), priority=25)
