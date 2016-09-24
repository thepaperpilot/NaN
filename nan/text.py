import scenebase
import pygame
import components
import processors
import interpolation
import util

class TextScene(scenebase.SceneBase):
    def __init__(self, text, scene):
        scenebase.SceneBase.__init__(self)
        self.text = text
        self.scene = scene

    def init(self):
        self.font = pygame.font.Font("RobotoMono-Regular.ttf", 42)

        text = self.world.create_entity()
        image = pygame.Surface([1280,720], pygame.SRCALPHA, 32).convert_alpha()
        util.drawText(image, self.text, (255, 255, 255), pygame.Rect(100, 100, 1080, 520), self.font)
        self.world.add_component(text, components.Position(640, 320))
        self.world.add_component(text, components.Image(image=image))
        self.world.add_component(text, components.Size(image.get_width(), image.get_height()))
        self.world.add_component(text, components.ChangePosition((640, 420), .5))
        self.world.add_component(text, components.ChangeAlpha(1, 1))

        def fade_out(entity):
            self.world.add_component(entity, components.ChangeAlpha(0, 1, interpolation.Circle(), fade_in, entity))

        def fade_in(entity):
            self.world.add_component(entity, components.ChangeAlpha(1, 1, interpolation.Circle(), fade_out, entity))

        continue_text = self.world.create_entity()
        image = self.font.render("press any button to continue", False, (32, 128, 255))
        self.world.add_component(continue_text, components.Position(640, 640))
        self.world.add_component(continue_text, components.Image(image=image))
        self.world.add_component(continue_text, components.Size(image.get_width(), image.get_height()))
        fade_in(continue_text)

        def fade_scene():
            for ent in [text, continue_text]:
                if self.world.has_component(ent, components.ChangeAlpha):
                    self.world.remove_component(ent, components.ChangeAlpha)
                self.world.add_component(ent, components.ChangeAlpha(0, .5))

            self.world.add_component(text, components.Delay(.5, next_scene))

        def next_scene():
            self.switch_to_scene(self.scene)

        self.world.add_processor(processors.RenderProcessor())
        self.world.add_processor(processors.AnimationProcessor(), priority=5)
        self.world.add_processor(processors.TextProcessor(fade_scene), priority=10)
