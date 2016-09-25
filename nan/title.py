import scenebase
import pygame
import components
import processors
import text
import game
import math

class TitleScene(scenebase.SceneBase):
    def __init__(self):
        scenebase.SceneBase.__init__(self)

    def init(self):
        self.font = pygame.font.Font("kenpixel.ttf", 72)
        self.titlefont = pygame.font.Font("kenpixel.ttf", 144)

        def start_game():
            for ent, (p, i) in self.world.get_components(components.Position, components.Image):
                self.world.add_component(ent, components.ChangePosition((p.x, p.y + 100), .25))
                self.world.add_component(ent, components.ChangeAlpha(0, .25))
            def change_scene():
                self.switch_to_scene(text.TextScene("This is the story of an adventurer named NaN, known across the land for his unwavering enthusiasm for helping anyone with anything. His abilities were known far and wide, and indeed our story even begins with him defeating a dragon with ease...", game.SceneOne()))
            next_scene = self.world.create_entity()
            self.world.add_component(next_scene, components.Delay(.5, change_scene))

        def scene_select():
            self.switch_to_scene(SceneSelect())

        def quit_game():
            self.terminate()

        def highlight(entity):
            t = self.world.component_for_entity(entity, components.Text)
            image = t.font.render("> " + t.text + " <", False, (0, 128, 128))
            self.world.component_for_entity(entity, components.Image).image = image
            size = self.world.component_for_entity(entity, components.Size)
            size.width = image.get_width()
            size.height = image.get_height()

        def lowlight(entity):
            t = self.world.component_for_entity(entity, components.Text)
            image = t.font.render(t.text, False, t.color)
            self.world.component_for_entity(entity, components.Image).image = image
            size = self.world.component_for_entity(entity, components.Size)
            size.width = image.get_width()
            size.height = image.get_height()

        start = self.world.create_entity()
        image = self.font.render("start", False, (0, 128, 0))
        self.world.add_component(start, components.Position(640, 440))
        self.world.add_component(start, components.Text("start", self.font))
        self.world.add_component(start, components.Image(image=image))
        self.world.add_component(start, components.Size(image.get_width(), image.get_height(), .75))
        self.world.add_component(start, components.Click(start_game))
        self.world.add_component(start, components.Over(highlight, lowlight))
        self.world.add_component(start, components.Audio("click"))

        scene = self.world.create_entity()
        image = self.font.render("scene select", False, (0, 128, 0))
        self.world.add_component(scene, components.Position(640, 540))
        self.world.add_component(scene, components.Text("scene select", self.font))
        self.world.add_component(scene, components.Image(image=image))
        self.world.add_component(scene, components.Size(image.get_width(), image.get_height(), .75))
        self.world.add_component(scene, components.Click(scene_select))
        self.world.add_component(scene, components.Over(highlight, lowlight))
        self.world.add_component(scene, components.Audio("click"))

        quitbutton = self.world.create_entity()
        image = self.font.render("quit", False, (0, 128, 0))
        self.world.add_component(quitbutton, components.Position(640, 640))
        self.world.add_component(quitbutton, components.Text("quit", self.font))
        self.world.add_component(quitbutton, components.Image(image=image))
        self.world.add_component(quitbutton, components.Size(image.get_width(), image.get_height(), .75))
        self.world.add_component(quitbutton, components.Click(quit_game))
        self.world.add_component(quitbutton, components.Over(highlight, lowlight))
        self.world.add_component(quitbutton, components.Audio("click"))

        title = self.world.create_entity()
        image = self.titlefont.render("NaN", False, (0, 128, 0))
        self.world.add_component(title, components.Position(640, 240))
        self.world.add_component(title, components.Image(image=image))
        self.world.add_component(title, components.Size(image.get_width(), image.get_height()))

        self.world.add_processor(processors.RenderProcessor())
        self.world.add_processor(processors.InputProcessor(), priority=10)
        self.world.add_processor(processors.PhysicsProcessor(), priority=5)
        self.world.add_processor(processors.AnimationProcessor(), priority=5)

class SceneSelect(scenebase.SceneBase):
    def __init__(self):
        scenebase.SceneBase.__init__(self)

    def init(self):
        self.font = pygame.font.Font("kenpixel.ttf", 72)

        def go_back():
            self.switch_to_scene(TitleScene())

        def open_scene(scene):
            self.switch_to_scene(scene)

        def highlight(entity):
            t = self.world.component_for_entity(entity, components.Text)
            image = t.font.render("> " + t.text + " <", False, (0, 128, 128))
            self.world.component_for_entity(entity, components.Image).image = image
            size = self.world.component_for_entity(entity, components.Size)
            size.width = image.get_width()
            size.height = image.get_height()

        def lowlight(entity):
            t = self.world.component_for_entity(entity, components.Text)
            image = t.font.render(t.text, False, t.color)
            self.world.component_for_entity(entity, components.Image).image = image
            size = self.world.component_for_entity(entity, components.Size)
            size.width = image.get_width()

        back = self.world.create_entity()
        image = self.font.render("back", False, (0, 128, 0))
        self.world.add_component(back, components.Position(640, 360))
        self.world.add_component(back, components.Text("back", self.font))
        self.world.add_component(back, components.Image(image=image))
        self.world.add_component(back, components.Size(image.get_width(), image.get_height(), .75))
        self.world.add_component(back, components.Reactive())
        self.world.add_component(back, components.Click(go_back))
        self.world.add_component(back, components.Over(highlight, lowlight))
        self.world.add_component(back, components.Audio("click"))

        scene1 = self.world.create_entity()
        self.world.add_component(scene1, components.Position(300, 100))
        self.world.add_component(scene1, components.Platform())
        self.world.add_component(scene1, components.Image("IntroBG.png"))
        self.world.add_component(scene1, components.Size(320, 180))
        self.world.add_component(scene1, components.Reactive())
        self.world.add_component(scene1, components.Click(open_scene, game.SceneOne()))

        label1 = self.world.create_entity()
        image = self.font.render("1", False, (0, 128, 0))
        self.world.add_component(label1, components.Position(300, 170))
        self.world.add_component(label1, components.Image(image=image))
        self.world.add_component(label1, components.Size(image.get_width(), image.get_height()))
        self.world.add_component(label1, components.Reactive())

        scene2 = self.world.create_entity()
        self.world.add_component(scene2, components.Position(980, 100))
        self.world.add_component(scene2, components.Platform())
        self.world.add_component(scene2, components.Image("HouseScene2BG.png"))
        self.world.add_component(scene2, components.Size(320, 180))
        self.world.add_component(scene2, components.Reactive())
        self.world.add_component(scene2, components.Click(open_scene, game.SceneTwo()))

        label2 = self.world.create_entity()
        image = self.font.render("2", False, (0, 128, 0))
        self.world.add_component(label2, components.Position(980, 170))
        self.world.add_component(label2, components.Image(image=image))
        self.world.add_component(label2, components.Size(image.get_width(), image.get_height()))
        self.world.add_component(label2, components.Reactive())

        scene3 = self.world.create_entity()
        self.world.add_component(scene3, components.Position(300, 350))
        self.world.add_component(scene3, components.Platform())
        self.world.add_component(scene3, components.Image("HouseSceneBlacksmithBG.png"))
        self.world.add_component(scene3, components.Size(320, 180))
        self.world.add_component(scene3, components.Reactive())
        self.world.add_component(scene3, components.Click(open_scene, game.SceneThree()))

        label3 = self.world.create_entity()
        image = self.font.render("3", False, (0, 128, 0))
        self.world.add_component(label3, components.Position(300, 420))
        self.world.add_component(label3, components.Image(image=image))
        self.world.add_component(label3, components.Size(image.get_width(), image.get_height()))
        self.world.add_component(label3, components.Reactive())

        scene4 = self.world.create_entity()
        self.world.add_component(scene4, components.Position(980, 350))
        self.world.add_component(scene4, components.Platform())
        self.world.add_component(scene4, components.Image("HouseScene1BG.png"))
        self.world.add_component(scene4, components.Size(320, 180))
        self.world.add_component(scene4, components.Reactive())
        self.world.add_component(scene4, components.Click(open_scene, game.SceneFour()))

        label4 = self.world.create_entity()
        image = self.font.render("4", False, (0, 128, 0))
        self.world.add_component(label4, components.Position(980, 420))
        self.world.add_component(label4, components.Image(image=image))
        self.world.add_component(label4, components.Size(image.get_width(), image.get_height()))
        self.world.add_component(label4, components.Reactive())


        for ent, (i, p, s, r) in self.world.get_components(components.Image, components.Position, components.Size, components.Reactive):
            if r.x == 0:
                r.x = p.x
                r.y = p.y
            mousex, mousey = pygame.mouse.get_pos()
            mousex *= 1280 / pygame.display.get_surface().get_width()
            mousey *= 720 / pygame.display.get_surface().get_height()
            p.x = r.x + (r.x - mousex) / 10
            p.y = r.y + (r.y - mousey) / 10
            s.scale = 100 / min(400, max(100, math.sqrt((r.x - mousex) ** 2 + (r.y - mousey) ** 2)))

        self.world.add_processor(processors.RenderProcessor())
        self.world.add_processor(processors.InputProcessor(), priority=10)
        self.world.add_processor(processors.PhysicsProcessor(), priority=5)
        self.world.add_processor(processors.AnimationProcessor(), priority=5)