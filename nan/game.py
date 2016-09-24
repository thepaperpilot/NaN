import scenebase
import pygame
import components
import processors
import interpolation
import random
import text

class SceneOne(scenebase.SceneBase):
    def __init__(self):
        scenebase.SceneBase.__init__(self)

    def init(self):
        self.font = pygame.font.Font("kenpixel.ttf", 42)

        bg = self.world.create_entity()
        self.world.add_component(bg, components.Position(640, 360))
        self.world.add_component(bg, components.Image("IntroBG.png"))
        self.world.add_component(bg, components.Size(1280, 720))
        self.world.add_component(bg, components.Background())

        player = self.world.create_entity()
        image = components.Image("playerIdle.png")
        animation = components.Animation("playerSimple.png", splitx=80, framelength=.1)
        carry_image = components.Image("playerCarryIdle.png")
        carry_animation = components.Animation("playerCarrySimple.png", splitx=80, framelength=.1)
        self.world.add_component(player, components.Position(100, 100))
        self.world.add_component(player, components.Velocity(0, 0))
        self.world.add_component(player, image)
        self.world.add_component(player, components.Size(80, 80))
        self.world.add_component(player, components.Player(image, animation, carry_image, carry_animation))

        sword = self.world.create_entity()
        self.world.add_component(sword, components.Position(300, 500))
        self.world.add_component(sword, components.Velocity(0, 0))
        self.world.add_component(sword, components.Image("sword.png"))
        self.world.add_component(sword, components.Size(80, 80))

        def next_scene():
            self.switch_to_scene(text.TextScene("And thusly NaN took out yet another dragon. But eventually there were no more dragons to kill, but there remained bills to pay. NaN began to take on side jobs...", SceneTwo()))

        def dragon_hit():
            self.world.component_for_entity(dragon, components.Animation).frame = 1
            damage = self.world.create_entity()
            image = self.font.render("999,999,999,999,999,999", False, (255, 128, 0))
            self.world.add_component(damage, components.Position(960, 320))
            self.world.add_component(damage, components.Image(image=image))
            self.world.add_component(damage, components.Size(image.get_width(), image.get_height()))
            self.world.add_component(damage, components.ChangePosition((960, 260), 2, interpolation.Smooth(), fade_out))
            self.world.add_component(damage, components.ChangeAlpha(0, 2))
            self.world.add_component(damage, components.Delay(3, next_scene))

        def fade_out():
            for ent, i in self.world.get_component(components.Image):
                self.world.add_component(ent, components.ChangeAlpha(0, 1))
            for ent, a in self.world.get_component(components.Animation):
                self.world.add_component(ent, components.ChangeAlpha(0, 1))

        dragon = self.world.create_entity()
        self.world.add_component(dragon, components.Position(1000, 500))
        self.world.add_component(dragon, components.Velocity(0, 0))
        self.world.add_component(dragon, components.Animation("dragon.png", splitx=640, frame=0))
        self.world.add_component(dragon, components.Size(640, 640))
        self.world.add_component(dragon, components.Touch(sword, dragon_hit, rect=pygame.Rect(320, 0, -320, 0)))

        def move_up(entity):
            self.world.add_component(entity, components.ChangePosition((640, 640), 1, interpolation.Smooth(), move_down, entity))
        def move_down(entity):
            self.world.add_component(entity, components.ChangePosition((640, 680), 1, interpolation.Smooth(), move_up, entity))

        tutorial = self.world.create_entity()
        image = self.font.render("press E to pick up your sword", False, (32, 255, 128))
        self.world.add_component(tutorial, components.Position(640, 680))
        self.world.add_component(tutorial, components.Image(image=image))
        self.world.add_component(tutorial, components.Size(image.get_width(), image.get_height()))
        move_up(tutorial)

        clouds = []
        for i in [1,2,3,4,5,6]:
            cloud = self.world.create_entity()
            clouds.append(cloud)
            self.world.add_component(cloud, components.Position(random.randrange(100, 1180), random.randrange(75, 200)))
            #self.world.add_component(cloud, components.Image("cloud.png", blend=pygame.BLEND_RGBA_MAX))
            self.world.add_component(cloud, components.Image("cloud.png"))
            self.world.add_component(cloud, components.Size(160, 80))
            self.world.add_component(cloud, components.Background())

        self.world.add_processor(processors.RenderProcessor())
        self.world.add_processor(processors.InputProcessor(), priority=10)
        self.world.add_processor(processors.PhysicsProcessor(600), priority=5)
        self.world.add_processor(processors.AnimationProcessor(), priority=5)
        self.world.add_processor(processors.PlayerProcessor(player, 100), priority=25)
        self.world.add_processor(processors.Scene1Processor(player, tutorial, self.font), priority=20)

class SceneTwo(scenebase.SceneBase):
    def __init__(self):
        scenebase.SceneBase.__init__(self)

    def init(self):
        self.font = pygame.font.Font("kenpixel.ttf", 42)

        bg = self.world.create_entity()
        self.world.add_component(bg, components.Position(640, 360))
        self.world.add_component(bg, components.Image("HouseScene1BG.png"))
        self.world.add_component(bg, components.Size(1280, 720))
        self.world.add_component(bg, components.Background())

        player = self.world.create_entity()
        image = components.Image("playerIdle.png")
        animation = components.Animation("playerSimple.png", splitx=80, framelength=.1)
        carry_image = components.Image("playerCarryIdle.png")
        carry_animation = components.Animation("playerCarrySimple.png", splitx=80, framelength=.1)
        self.world.add_component(player, components.Position(100, 100))
        self.world.add_component(player, components.Velocity(0, 0))
        self.world.add_component(player, image)
        self.world.add_component(player, components.Size(80, 80))
        self.world.add_component(player, components.Player(image, animation, carry_image, carry_animation))

        sword = self.world.create_entity()
        self.world.add_component(sword, components.Position(300, 500))
        self.world.add_component(sword, components.Velocity(0, 0))
        self.world.add_component(sword, components.Image("sword.png"))
        self.world.add_component(sword, components.Size(80, 80))

        floor2 = self.world.create_entity()
        self.world.add_component(floor2, components.Position(520, 380))
        self.world.add_component(floor2, components.Platform())
        self.world.add_component(floor2, components.Image("WoodPlatform3.png"))
        self.world.add_component(floor2, components.Size(720, 40))
        self.world.add_component(floor2, components.Background())

        stair = self.world.create_entity()
        self.world.add_component(stair, components.Position(1000, 500))
        self.world.add_component(stair, components.Platform())
        self.world.add_component(stair, components.Image("WoodPlatform1.png"))
        self.world.add_component(stair, components.Size(240, 40))
        self.world.add_component(stair, components.Background())


        def next_scene():
            self.switch_to_scene(text.TextScene("And thusly NaN took out yet another dragon. But eventually there were no more dragons to kill, but there remained bills to pay. NaN began to take on side jobs...", SceneOne()))

        def dragon_hit():
            self.world.component_for_entity(dragon, components.Animation).frame = 1
            damage = self.world.create_entity()
            image = self.font.render("999,999,999,999,999,999", False, (255, 128, 0))
            self.world.add_component(damage, components.Position(960, 320))
            self.world.add_component(damage, components.Image(image=image))
            self.world.add_component(damage, components.Size(image.get_width(), image.get_height()))
            self.world.add_component(damage, components.ChangePosition((960, 260), 2, interpolation.Smooth(), fade_out))
            self.world.add_component(damage, components.ChangeAlpha(0, 2))
            self.world.add_component(damage, components.Delay(3, next_scene))

        def fade_out():
            for ent, i in self.world.get_component(components.Image):
                self.world.add_component(ent, components.ChangeAlpha(0, 1))
            for ent, a in self.world.get_component(components.Animation):
                self.world.add_component(ent, components.ChangeAlpha(0, 1))

        dragon = self.world.create_entity()
        self.world.add_component(dragon, components.Position(1000, 500))
        self.world.add_component(dragon, components.Velocity(0, 0))
        self.world.add_component(dragon, components.Animation("dragon.png", splitx=640, frame=0))
        self.world.add_component(dragon, components.Size(640, 640))
        self.world.add_component(dragon, components.Touch(sword, dragon_hit, rect=pygame.Rect(320, 0, -320, 0)))

        self.world.add_processor(processors.RenderProcessor())
        self.world.add_processor(processors.InputProcessor(), priority=10)
        self.world.add_processor(processors.PhysicsProcessor(600), priority=5)
        self.world.add_processor(processors.AnimationProcessor(), priority=5)
        self.world.add_processor(processors.PlayerProcessor(player, 80), priority=25)
        self.world.add_processor(processors.Scene2Processor(player), priority=30)
