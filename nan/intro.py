import scenebase
import pygame
import components
import processors
import interpolation
import util

class IntroScene(scenebase.SceneBase):
    def __init__(self):
        scenebase.SceneBase.__init__(self)

    def init(self):
        self.font = pygame.font.Font("RobotoMono-Regular.ttf", 42)

        intro = self.world.create_entity()
        image = pygame.Surface((1280, 720))
        util.drawText(image, "This is the story of an adventurer named NaN, known across the land for his unwavering enthusiasm for helping anyone with anything. 3 years ago he even protected his hometown from a vicious wandering dragon...", (255, 255, 255), pygame.Rect(100, 100, 1080, 520), self.font)
        self.world.add_component(intro, components.Position(640, 320))
        self.world.add_component(intro, components.Image(image=image))
        self.world.add_component(intro, components.Size(image.get_width(), image.get_height()))
        self.world.add_component(intro, components.ChangePosition((640, 420), .5))
        self.world.add_component(intro, components.ChangeAlpha(0, 1, 1))

        def fade_out(entity):
            self.world.add_component(entity, components.ChangeAlpha(1, 0, 1, interpolation.Circle(), fade_in, entity))

        def fade_in(entity):
            self.world.add_component(entity, components.ChangeAlpha(0, 1, 1, interpolation.Circle(), fade_out, entity))

        continue_text = self.world.create_entity()
        image = self.font.render("press any button to continue", False, (32, 128, 255))
        self.world.add_component(continue_text, components.Position(640, 640))
        self.world.add_component(continue_text, components.Image(image=image))
        self.world.add_component(continue_text, components.Size(image.get_width(), image.get_height()))
        fade_in(continue_text)

        self.world.add_processor(processors.RenderProcessor())
        self.world.add_processor(processors.AnimationProcessor(), priority=5)
        self.world.add_processor(processors.IntroProcessor(self), priority=10)
