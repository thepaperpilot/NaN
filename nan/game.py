import scenebase
import pygame
import components
import processors
import interpolation
import random
import text
import os
import util
import title

def get_player(world):
    player = world.create_entity()
    image = components.Image("playerIdle.png")
    animation = components.Animation("playerSimple.png", splitx=80, framelength=.1)
    carry_image = components.Image("playerCarryIdle.png")
    carry_animation = components.Animation("playerCarrySimple.png", splitx=80, framelength=.1)
    jump = components.Audio("jump.ogg")
    throw = components.Audio("throw")
    world.add_component(player, components.Position(100, 560))
    world.add_component(player, components.Velocity(0, 0))
    world.add_component(player, image)
    world.add_component(player, components.Size(80, 80))
    world.add_component(player, components.Player(image, animation, carry_image, carry_animation, jump, throw))

    return player

class SceneOne(scenebase.SceneBase):
    def __init__(self):
        scenebase.SceneBase.__init__(self)

    def init(self):
        self.font = pygame.font.Font("kenpixel.ttf", 42)
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(100)
        pygame.mixer.music.load('audio/Retro Reggae.ogg')
        pygame.mixer.music.play(-1)

        bg = self.world.create_entity()
        self.world.add_component(bg, components.Position(640, 360))
        self.world.add_component(bg, components.Image("IntroBG.png"))
        self.world.add_component(bg, components.Size(1280, 720))
        self.world.add_component(bg, components.Background())

        player = get_player(self.world)

        sword = self.world.create_entity()
        self.world.add_component(sword, components.Position(300, 560))
        self.world.add_component(sword, components.Velocity(0, 0))
        self.world.add_component(sword, components.Image("sword.png"))
        self.world.add_component(sword, components.Size(80, 80))

        def next_scene():
            self.switch_to_scene(text.TextScene("And thusly the skilled adventurer NaN took out yet another dragon. Dragon killing was no longer a dangerous quest but rather routine cleaning. With the dragon population dwindling NaN had time to help more people with their non life threatening problems.", SceneTwo()))

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
            pygame.mixer.Sound(os.path.join('audio', 'dragon.ogg')).play()

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
        self.world.add_component(dragon, components.Touch(sword, dragon_hit, rect=pygame.Rect(0, -400, -320, 0)))

        def move_up(entity):
            self.world.add_component(entity, components.ChangePosition((640, 640), 1, interpolation.Smooth(), move_down, entity))
        def move_down(entity):
            self.world.add_component(entity, components.ChangePosition((640, 680), 1, interpolation.Smooth(), move_up, entity))

        tutorial = self.world.create_entity()
        image = self.font.render("use arrow keys or WASD to move", False, (32, 255, 128))
        self.world.add_component(tutorial, components.Position(640, 680))
        self.world.add_component(tutorial, components.Image(image=image))
        self.world.add_component(tutorial, components.Size(image.get_width(), image.get_height()))
        move_up(tutorial)

        clouds = []
        for i in [1,2,3,4,5,6]:
            cloud = self.world.create_entity()
            clouds.append(cloud)
            self.world.add_component(cloud, components.Position(random.randrange(100, 1180), random.randrange(75, 200)))
            self.world.add_component(cloud, components.Image("cloud.png", blend=pygame.BLEND_RGBA_MAX))
            self.world.add_component(cloud, components.Size(160, 80))
            self.world.add_component(cloud, components.Background())
            self.world.add_component(cloud, components.Hang())

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
        self.small_font = pygame.font.Font("kenpixel.ttf", 16)
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(100)
        pygame.mixer.music.load('audio/Retro Comedy.ogg')
        pygame.mixer.music.play(-1)

        bg = self.world.create_entity()
        self.world.add_component(bg, components.Position(640, 360))
        self.world.add_component(bg, components.Image("OutsideSceneBG.png"))
        self.world.add_component(bg, components.Size(1280, 720))
        self.world.add_component(bg, components.Background())

        player = get_player(self.world)

        flower = self.world.create_entity()
        self.world.add_component(flower, components.Position(240, 560))
        self.world.add_component(flower, components.Velocity(0, 0))
        self.world.add_component(flower, components.Image("Flower.png"))
        self.world.add_component(flower, components.Flammable(False))
        self.world.add_component(flower, components.Size(80, 80))
        self.world.add_component(flower, components.Audio("light"))

        vase = self.world.create_entity()
        self.world.add_component(vase, components.Position(510, 560))
        self.world.add_component(vase, components.Velocity(0, 0))
        self.world.add_component(vase, components.Image("Vase.png"))
        self.world.add_component(vase, components.Flammable(False))
        self.world.add_component(vase, components.Size(80, 80))
        self.world.add_component(vase, components.Audio("light"))

        guy = self.world.create_entity()
        self.world.add_component(guy, components.Position(340, 560))
        self.world.add_component(guy, components.Velocity(0, 0))
        self.world.add_component(guy, components.Image("NPC2.png"))
        self.world.add_component(guy, components.Flammable(False))
        self.world.add_component(guy, components.Size(80, 80))
        self.world.add_component(guy, components.Audio("grunt"))

        guy2 = self.world.create_entity()
        self.world.add_component(guy2, components.Position(950, 560))
        self.world.add_component(guy2, components.Velocity(0, 0))
        self.world.add_component(guy2, components.Image("NPC1.png"))
        self.world.add_component(guy2, components.Flammable(False))
        self.world.add_component(guy2, components.Size(80, 80))
        self.world.add_component(guy2, components.Audio("grunt"))
        self.world.component_for_entity(guy2, components.Image).image = pygame.transform.flip(self.world.component_for_entity(guy2, components.Image).image, False, False)

        def puzzle_complete():
            complaint = self.world.create_entity()
            self.world.add_component(complaint, components.Position(640, 500))
            self.world.add_component(complaint, components.Image("speech.png"))
            util.drawText(self.world.component_for_entity(complaint, components.Image).image, "You better not have dropped her or anything.", (255, 255, 255), pygame.Rect(30, 20, 246, 134), self.small_font)
            self.world.add_component(complaint, components.Size(307, 173))
            self.world.add_component(complaint, components.ChangePosition((640, 350), 4, interpolation.Smooth(), fade_out))
            self.world.add_component(complaint, components.ChangeAlpha(0, 4, interpolation.Smooth()))
            self.world.add_component(complaint, components.Delay(5, next_scene))

        cat = self.world.create_entity()
        self.world.add_component(cat, components.Position(1100, 170))
        self.world.add_component(cat, components.Hang())
        self.world.add_component(cat, components.Image("Cat.png"))
        self.world.add_component(cat, components.Flammable(False))
        self.world.add_component(cat, components.Size(80, 80))
        self.world.add_component(cat, components.Touch(guy, puzzle_complete))
        self.world.add_component(cat, components.Audio("light"))

        bubble = self.world.create_entity()
        self.world.add_component(bubble, components.Position(200, 100))
        self.world.add_component(bubble, components.Image("speech.png"))
        self.world.add_component(bubble, components.Size(307, 173))
        self.world.add_component(bubble, components.Hang())
        image = self.world.component_for_entity(bubble, components.Image).image
        util.drawText(image, "Oh no! My wonderful cat has found herself stuck in a tree! Won't someone please help me?", (255, 255, 255), pygame.Rect(30, 20, 246, 134), self.small_font)

        def next_scene():
            self.switch_to_scene(text.TextScene("With adventuring work in low demand and the cost of living constantly increasing, NaN was forced to stoop to more and more menial work.", SceneThree()))

        def fade_out():
            for ent, i in self.world.get_component(components.Image):
                self.world.add_component(ent, components.ChangeAlpha(0, 1))
            for ent, a in self.world.get_component(components.Animation):
                self.world.add_component(ent, components.ChangeAlpha(0, 1))

        self.world.add_processor(processors.RenderProcessor())
        self.world.add_processor(processors.InputProcessor(), priority=10)
        self.world.add_processor(processors.PhysicsProcessor(600), priority=5)
        self.world.add_processor(processors.AnimationProcessor(), priority=5)
        self.world.add_processor(processors.PlayerProcessor(player, 95), priority=25)

class SceneThree(scenebase.SceneBase):
    def __init__(self):
        scenebase.SceneBase.__init__(self)

    def init(self):
        self.font = pygame.font.Font("kenpixel.ttf", 42)
        self.small_font = pygame.font.Font("kenpixel.ttf", 16)
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(100)
        pygame.mixer.music.load('audio/Retro Polka.ogg')
        pygame.mixer.music.play(-1)

        bg = self.world.create_entity()
        self.world.add_component(bg, components.Position(640, 360))
        self.world.add_component(bg, components.Image("HouseScene2BG.png"))
        self.world.add_component(bg, components.Size(1280, 720))
        self.world.add_component(bg, components.Background())

        player = get_player(self.world)

        floor2 = self.world.create_entity()
        self.world.add_component(floor2, components.Position(400, 390))
        self.world.add_component(floor2, components.Platform())
        self.world.add_component(floor2, components.Image("WoodPlatform2.png"))
        self.world.add_component(floor2, components.Size(480, 40))
        self.world.add_component(floor2, components.Background())

        stair = self.world.create_entity()
        self.world.add_component(stair, components.Position(760, 500))
        self.world.add_component(stair, components.Platform())
        self.world.add_component(stair, components.Image("WoodPlatform1.png"))
        self.world.add_component(stair, components.Size(240, 40))
        self.world.add_component(stair, components.Background())

        bed = self.world.create_entity()
        self.world.add_component(bed, components.Position(260, 330))
        self.world.add_component(bed, components.Velocity(0, 0))
        self.world.add_component(bed, components.Image("Bed.png"))
        self.world.add_component(bed, components.Flammable(False))
        self.world.add_component(bed, components.Size(160, 80))
        self.world.add_component(bed, components.Audio("heavy"))

        bookshelf = self.world.create_entity()
        self.world.add_component(bookshelf, components.Position(420, 290))
        self.world.add_component(bookshelf, components.Velocity(0, 0))
        self.world.add_component(bookshelf, components.Image("Bookshelf.png"))
        self.world.add_component(bookshelf, components.Flammable(False))
        self.world.add_component(bookshelf, components.Size(80, 160))
        self.world.add_component(bookshelf, components.Audio("heavy"))

        chest = self.world.create_entity()
        self.world.add_component(chest, components.Position(540, 330))
        self.world.add_component(chest, components.Velocity(0, 0))
        self.world.add_component(chest, components.Image("chest.png"))
        self.world.add_component(chest, components.Flammable(False))
        self.world.add_component(chest, components.Size(80, 80))
        self.world.add_component(chest, components.Audio("chest"))

        guy = self.world.create_entity()
        self.world.add_component(guy, components.Position(280, 560))
        self.world.add_component(guy, components.Velocity(0, 0))
        self.world.add_component(guy, components.Image("NPC1.png"))
        self.world.add_component(guy, components.Flammable(False))
        self.world.add_component(guy, components.Size(80, 80))
        self.world.add_component(guy, components.Audio("grunt"))

        leftChair = self.world.create_entity()
        self.world.add_component(leftChair, components.Position(430, 560))
        self.world.add_component(leftChair, components.Velocity(0, 0))
        self.world.add_component(leftChair, components.Image("Chair.png"))
        self.world.add_component(leftChair, components.Flammable(False))
        self.world.add_component(leftChair, components.Size(80, 80))
        self.world.add_component(leftChair, components.Audio("light"))

        rightChair = self.world.create_entity()
        self.world.add_component(rightChair, components.Position(610, 560))
        self.world.add_component(rightChair, components.Velocity(0, 0))
        self.world.add_component(rightChair, components.Image("Chair.png"))
        self.world.add_component(rightChair, components.Flammable(False))
        self.world.add_component(rightChair, components.Size(80, 80))
        self.world.add_component(rightChair, components.Audio("light"))
        self.world.component_for_entity(rightChair, components.Image).image = pygame.transform.flip(self.world.component_for_entity(rightChair, components.Image).image, False, False)

        table = self.world.create_entity()
        self.world.add_component(table, components.Position(520, 560))
        self.world.add_component(table, components.Velocity(0, 0))
        self.world.add_component(table, components.Image("Table.png"))
        self.world.add_component(table, components.Flammable(False))
        self.world.add_component(table, components.Size(80, 80))
        self.world.add_component(table, components.Audio("heavy"))

        def puzzle_complete():
            p = self.world.component_for_entity(player, components.Player)
            if p.holding is books:
                p.holding = None
            self.world.delete_entity(books)
            complaint = self.world.create_entity()
            self.world.add_component(complaint, components.Position(640, 500))
            self.world.add_component(complaint, components.Image("speech.png"))
            util.drawText(self.world.component_for_entity(complaint, components.Image).image, "Wow, you got the books dirty. I can't use these anymore.", (255, 255, 255), pygame.Rect(30, 20, 246, 134), self.small_font)
            self.world.add_component(complaint, components.Size(307, 173))
            self.world.add_component(complaint, components.ChangePosition((640, 350), 4, interpolation.Smooth(), fade_out))
            self.world.add_component(complaint, components.ChangeAlpha(0, 4, interpolation.Smooth()))
            self.world.add_component(complaint, components.Delay(5, next_scene))

        books = self.world.create_entity()
        self.world.add_component(books, components.Position(1000, 560))
        self.world.add_component(books, components.Velocity(0, 0))
        self.world.add_component(books, components.Image("PileOfBooks.png"))
        self.world.add_component(books, components.Flammable(False))
        self.world.add_component(books, components.Size(80, 80))
        self.world.add_component(books, components.Touch(bookshelf, puzzle_complete, rect=pygame.Rect(5, 0, -10, 0)))
        self.world.add_component(books, components.Audio("light"))

        lamp = self.world.create_entity()
        self.world.add_component(lamp, components.Position(760, 170))
        self.world.add_component(lamp, components.Image("Chandelier.png"))
        self.world.add_component(lamp, components.Flammable(True))
        self.world.add_component(lamp, components.Size(80, 80))
        self.world.add_component(lamp, components.Hang())
        self.world.add_component(lamp, components.Audio("glass.ogg"))

        bubble = self.world.create_entity()
        self.world.add_component(bubble, components.Position(1000, 100))
        self.world.add_component(bubble, components.Image("speech.png"))
        self.world.add_component(bubble, components.Size(307, 173))
        self.world.add_component(bubble, components.Hang())
        image = self.world.component_for_entity(bubble, components.Image).image
        util.drawText(image, "Ah! NaN, just in time! I need your help putting my books away. They are very important!", (255, 255, 255), pygame.Rect(30, 20, 246, 134), self.small_font)

        def next_scene():
            self.switch_to_scene(text.TextScene("These thankless jobs took their toll on NaN. He put on a friendly face, but inside he was growing weary...", SceneFour()))

        def fade_out():
            for ent, i in self.world.get_component(components.Image):
                self.world.add_component(ent, components.ChangeAlpha(0, 1))
            for ent, a in self.world.get_component(components.Animation):
                self.world.add_component(ent, components.ChangeAlpha(0, 1))

        self.world.add_processor(processors.RenderProcessor())
        self.world.add_processor(processors.InputProcessor(), priority=10)
        self.world.add_processor(processors.PhysicsProcessor(600), priority=5)
        self.world.add_processor(processors.AnimationProcessor(), priority=5)
        self.world.add_processor(processors.PlayerProcessor(player, 85), priority=25)

class SceneFour(scenebase.SceneBase):
    count = 0

    def __init__(self):
        scenebase.SceneBase.__init__(self)

    def init(self):
        self.font = pygame.font.Font("kenpixel.ttf", 42)
        self.small_font = pygame.font.Font("kenpixel.ttf", 16)
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(100)
        pygame.mixer.music.load('audio/Retro Beat.ogg')
        pygame.mixer.music.play(-1)

        bg = self.world.create_entity()
        self.world.add_component(bg, components.Position(640, 360))
        self.world.add_component(bg, components.Image("HouseScene3BG.png"))
        self.world.add_component(bg, components.Size(1280, 720))
        self.world.add_component(bg, components.Background())

        player = get_player(self.world)

        floor = self.world.create_entity()
        self.world.add_component(floor, components.Position(640, 560))
        self.world.add_component(floor, components.Size(1280, 100))
        #self.world.add_component(floor, components.Image("box1.png"))

        def spider_tally():
            self.count += 1
            if self.count > 3:
                puzzle_complete()

        spider = self.world.create_entity()
        self.world.add_component(spider, components.Position(200, 320))
        self.world.add_component(spider, components.Hang())
        self.world.add_component(spider, components.Image("Cobweb.png"))
        self.world.add_component(spider, components.Flammable(False))
        self.world.add_component(spider, components.Size(80, 80))
        self.world.add_component(spider, components.Audio("light"))
        self.world.add_component(spider, components.Touch(floor, spider_tally))

        spider2 = self.world.create_entity()
        self.world.add_component(spider2, components.Position(280, 240))
        self.world.add_component(spider2, components.Hang())
        self.world.add_component(spider2, components.Image("Cobweb.png"))
        self.world.add_component(spider2, components.Flammable(False))
        self.world.add_component(spider2, components.Size(80, 80))
        self.world.add_component(spider2, components.Audio("light"))
        self.world.add_component(spider2, components.Touch(floor, spider_tally))

        spider3 = self.world.create_entity()
        self.world.add_component(spider3, components.Position(420, 230))
        self.world.add_component(spider3, components.Hang())
        self.world.add_component(spider3, components.Image("Cobweb.png"))
        self.world.add_component(spider3, components.Flammable(False))
        self.world.add_component(spider3, components.Size(80, 80))
        self.world.add_component(spider3, components.Audio("light"))
        self.world.add_component(spider3, components.Touch(floor, spider_tally))

        spider4 = self.world.create_entity()
        self.world.add_component(spider4, components.Position(440, 400))
        self.world.add_component(spider4, components.Hang())
        self.world.add_component(spider4, components.Image("Cobweb.png"))
        self.world.add_component(spider4, components.Flammable(False))
        self.world.add_component(spider4, components.Size(80, 80))
        self.world.add_component(spider4, components.Audio("light"))
        self.world.add_component(spider4, components.Touch(floor, spider_tally))

        spider5 = self.world.create_entity()
        self.world.add_component(spider5, components.Position(590, 300))
        self.world.add_component(spider5, components.Hang())
        self.world.add_component(spider5, components.Image("Cobweb.png"))
        self.world.add_component(spider5, components.Flammable(False))
        self.world.add_component(spider5, components.Size(80, 80))
        self.world.add_component(spider5, components.Audio("light"))
        self.world.add_component(spider5, components.Touch(floor, spider_tally))

        spider6 = self.world.create_entity()
        self.world.add_component(spider6, components.Position(680, 170))
        self.world.add_component(spider6, components.Hang())
        self.world.add_component(spider6, components.Image("Cobweb.png"))
        self.world.add_component(spider6, components.Flammable(False))
        self.world.add_component(spider6, components.Size(80, 80))
        self.world.add_component(spider6, components.Audio("light"))
        self.world.add_component(spider6, components.Touch(floor, spider_tally))

        spider7 = self.world.create_entity()
        self.world.add_component(spider7, components.Position(760, 390))
        self.world.add_component(spider7, components.Hang())
        self.world.add_component(spider7, components.Image("Cobweb.png"))
        self.world.add_component(spider7, components.Flammable(False))
        self.world.add_component(spider7, components.Size(80, 80))
        self.world.add_component(spider7, components.Audio("light"))
        self.world.add_component(spider7, components.Touch(floor, spider_tally))

        spider8 = self.world.create_entity()
        self.world.add_component(spider8, components.Position(830, 230))
        self.world.add_component(spider8, components.Hang())
        self.world.add_component(spider8, components.Image("Cobweb.png"))
        self.world.add_component(spider8, components.Flammable(False))
        self.world.add_component(spider8, components.Size(80, 80))
        self.world.add_component(spider8, components.Audio("light"))
        self.world.add_component(spider8, components.Touch(floor, spider_tally))

        box = self.world.create_entity()
        self.world.add_component(box, components.Position(520, 560))
        self.world.add_component(box, components.Velocity(0, 0))
        self.world.add_component(box, components.Image("box1.png"))
        self.world.add_component(box, components.Flammable(True))
        self.world.add_component(box, components.Size(80, 80))
        self.world.add_component(box, components.Audio("light"))

        guy = self.world.create_entity()
        self.world.add_component(guy, components.Position(210, 560))
        self.world.add_component(guy, components.Velocity(0, 0))
        self.world.add_component(guy, components.Image("NPC3.png"))
        self.world.add_component(guy, components.Flammable(False))
        self.world.add_component(guy, components.Size(80, 80))
        self.world.add_component(guy, components.Audio("grunt"))

        def puzzle_complete():
            complaint = self.world.create_entity()
            self.world.add_component(complaint, components.Position(640, 500))
            self.world.add_component(complaint, components.Image("speech.png"))
            util.drawText(self.world.component_for_entity(complaint, components.Image).image, "Now get out of my barn!", (255, 255, 255), pygame.Rect(30, 20, 246, 134), self.small_font)
            self.world.add_component(complaint, components.Size(307, 173))
            self.world.add_component(complaint, components.ChangePosition((640, 350), 4, interpolation.Smooth(), fade_out))
            self.world.add_component(complaint, components.ChangeAlpha(0, 4, interpolation.Smooth()))
            self.world.add_component(complaint, components.Delay(5, next_scene))

        cat = self.world.create_entity()
        self.world.add_component(cat, components.Position(1190, 560))
        self.world.add_component(cat, components.Velocity(0,0))
        self.world.add_component(cat, components.Image("Cat.png"))
        self.world.add_component(cat, components.Flammable(False))
        self.world.add_component(cat, components.Size(80, 80))
        self.world.add_component(cat, components.Audio("light"))

        bubble = self.world.create_entity()
        self.world.add_component(bubble, components.Position(1000, 100))
        self.world.add_component(bubble, components.Image("speech.png"))
        self.world.add_component(bubble, components.Size(307, 173))
        self.world.add_component(bubble, components.Hang())
        image = self.world.component_for_entity(bubble, components.Image).image
        util.drawText(image, "My barn is dusty and full of cobwebs. NaN! Come here and do this for me.", (255, 255, 255), pygame.Rect(30, 20, 246, 134), self.small_font)

        def next_scene():
            self.switch_to_scene(text.TextScene("Lack of real adventuring work not only wore on NaN, but it dulled him. His body atrophied as his mind numbed, and he realized he could no longer perform the same feats he'd grown accustomed to.", SceneFive()))

        def fade_out():
            for ent, i in self.world.get_component(components.Image):
                self.world.add_component(ent, components.ChangeAlpha(0, 1))
            for ent, a in self.world.get_component(components.Animation):
                self.world.add_component(ent, components.ChangeAlpha(0, 1))

        self.world.add_processor(processors.RenderProcessor())
        self.world.add_processor(processors.InputProcessor(), priority=10)
        self.world.add_processor(processors.PhysicsProcessor(600), priority=5)
        self.world.add_processor(processors.AnimationProcessor(), priority=5)
        self.world.add_processor(processors.PlayerProcessor(player, 75), priority=25)

class SceneFive(scenebase.SceneBase):
    def __init__(self):
        scenebase.SceneBase.__init__(self)

    def init(self):
        self.font = pygame.font.Font("kenpixel.ttf", 42)
        self.small_font = pygame.font.Font("kenpixel.ttf", 16)
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(100)
        pygame.mixer.music.load('audio/Space Cadet.ogg')
        pygame.mixer.music.play(-1)

        bg = self.world.create_entity()
        self.world.add_component(bg, components.Position(640, 360))
        self.world.add_component(bg, components.Image("HouseSceneBlacksmithBG.png"))
        self.world.add_component(bg, components.Size(1280, 720))
        self.world.add_component(bg, components.Background())

        player = get_player(self.world)

        floor2 = self.world.create_entity()
        self.world.add_component(floor2, components.Position(760, 390))
        self.world.add_component(floor2, components.Platform())
        self.world.add_component(floor2, components.Image("WoodPlatform3.png"))
        self.world.add_component(floor2, components.Size(720, 40))
        self.world.add_component(floor2, components.Background())

        stair = self.world.create_entity()
        self.world.add_component(stair, components.Position(280, 500))
        self.world.add_component(stair, components.Platform())
        self.world.add_component(stair, components.Image("WoodPlatform1.png"))
        self.world.add_component(stair, components.Size(240, 40))
        self.world.add_component(stair, components.Background())

        anvil = self.world.create_entity()
        self.world.add_component(anvil, components.Position(710, 560))
        self.world.add_component(anvil, components.Velocity(0, 0))
        self.world.add_component(anvil, components.Image("Anvil.png"))
        self.world.add_component(anvil, components.Size(80, 80))
        self.world.add_component(anvil, components.Audio("heavy"))

        bed = self.world.create_entity()
        self.world.add_component(bed, components.Position(500, 330))
        self.world.add_component(bed, components.Velocity(0, 0))
        self.world.add_component(bed, components.Image("Bed.png"))
        self.world.add_component(bed, components.Flammable(False))
        self.world.add_component(bed, components.Size(160, 80))
        self.world.add_component(bed, components.Audio("heavy"))

        bookshelf = self.world.create_entity()
        self.world.add_component(bookshelf, components.Position(640, 290))
        self.world.add_component(bookshelf, components.Velocity(0, 0))
        self.world.add_component(bookshelf, components.Image("Bookshelf.png"))
        self.world.add_component(bookshelf, components.Flammable(False))
        self.world.add_component(bookshelf, components.Size(80, 160))
        self.world.add_component(bookshelf, components.Audio("heavy"))

        guy = self.world.create_entity()
        self.world.add_component(guy, components.Position(280, 560))
        self.world.add_component(guy, components.Velocity(0, 0))
        self.world.add_component(guy, components.Image("NPC3.png"))
        self.world.add_component(guy, components.Flammable(False))
        self.world.add_component(guy, components.Size(80, 80))
        self.world.add_component(guy, components.Audio("grunt"))

        leftChair = self.world.create_entity()
        self.world.add_component(leftChair, components.Position(480, 560))
        self.world.add_component(leftChair, components.Velocity(0, 0))
        self.world.add_component(leftChair, components.Image("Chair.png"))
        self.world.add_component(leftChair, components.Flammable(False))
        self.world.add_component(leftChair, components.Size(80, 80))
        self.world.add_component(leftChair, components.Audio("light"))

        topChair = self.world.create_entity()
        self.world.add_component(topChair, components.Position(770, 330))
        self.world.add_component(topChair, components.Velocity(0, 0))
        self.world.add_component(topChair, components.Image("Chair.png"))
        self.world.add_component(topChair, components.Flammable(False))
        self.world.add_component(topChair, components.Size(80, 80))
        self.world.add_component(topChair, components.Audio("light"))

        table = self.world.create_entity()
        self.world.add_component(table, components.Position(570, 560))
        self.world.add_component(table, components.Velocity(0, 0))
        self.world.add_component(table, components.Image("Table.png"))
        self.world.add_component(table, components.Flammable(False))
        self.world.add_component(table, components.Size(80, 80))
        self.world.add_component(table, components.Audio("heavy"))

        vase = self.world.create_entity()

        def puzzle_complete():
            complaint = self.world.create_entity()
            self.world.add_component(complaint, components.Position(640, 500))
            self.world.add_component(complaint, components.Image("speech.png"))
            util.drawText(self.world.component_for_entity(complaint, components.Image).image, "You got a crack in it. Thanks for nothing.", (255, 255, 255), pygame.Rect(30, 20, 246, 134), self.small_font)
            self.world.add_component(complaint, components.Size(307, 173))
            self.world.add_component(complaint, components.ChangePosition((640, 350), 4, interpolation.Smooth(), fade_out))
            self.world.add_component(complaint, components.ChangeAlpha(0, 4, interpolation.Smooth()))
            self.world.add_component(complaint, components.Delay(5, next_scene))

        def open_chest():
            if chest is not None:
                vase = self.world.create_entity()
                p = self.world.component_for_entity(chest, components.Position)
                self.world.delete_entity(chest)
                self.world.add_component(vase, components.Position(p.x, p.y))
                self.world.add_component(vase, components.Size(80, 80))
                self.world.add_component(vase, components.Audio("light"))
                self.world.add_component(vase, components.Image("Vase.png"))
                self.world.add_component(vase, components.Flammable())
                self.world.add_component(vase, components.Touch(guy, puzzle_complete, rect=pygame.Rect(0,0,0,0)))
                if self.world.component_for_entity(player, components.Player).holding == chest:
                    self.world.component_for_entity(player, components.Player).holding = vase
                    i = self.world.component_for_entity(vase, components.Image)
                    s = self.world.component_for_entity(vase, components.Size)
                    i.image = pygame.transform.rotate(i.image, 90)
                    tmp = s.width
                    s.width = s.height
                    s.height = tmp
                else:
                    v = self.world.component_for_entity(chest, components.Velocity)
                    self.world.add_component(vase, components.Velocity(v.x, v.y))
                self.world.component_for_entity(vase, components.Audio).sound.play()

        def open_box1():
            if box is not None:
                n = self.world.create_entity()
                p = self.world.component_for_entity(box, components.Position)
                self.world.delete_entity(box)
                self.world.add_component(n, components.Position(p.x, p.y))
                self.world.add_component(n, components.Size(80, 80))
                self.world.add_component(n, components.Audio("light"))
                self.world.add_component(n, components.Image("Chair.png"))
                self.world.add_component(n, components.Flammable())
                if self.world.component_for_entity(player, components.Player).holding == box:
                    self.world.component_for_entity(player, components.Player).holding = n
                    i = self.world.component_for_entity(n, components.Image)
                    s = self.world.component_for_entity(n, components.Size)
                    i.image = pygame.transform.rotate(i.image, 90)
                    tmp = s.width
                    s.width = s.height
                    s.height = tmp
                else:
                    v = self.world.component_for_entity(box, components.Velocity)
                    self.world.add_component(n, components.Velocity(v.x, v.y))
                self.world.component_for_entity(n, components.Audio).sound.play()

        def open_box2():
            if box2 is not None:
                n = self.world.create_entity()
                p = self.world.component_for_entity(box2, components.Position)
                self.world.delete_entity(box2)
                self.world.add_component(n, components.Position(p.x, p.y))
                self.world.add_component(n, components.Size(80, 80))
                self.world.add_component(n, components.Audio("light"))
                self.world.add_component(n, components.Image("PileOfBooks.png"))
                self.world.add_component(n, components.Flammable())
                if self.world.component_for_entity(player, components.Player).holding == box2:
                    self.world.component_for_entity(player, components.Player).holding = n
                    i = self.world.component_for_entity(n, components.Image)
                    s = self.world.component_for_entity(n, components.Size)
                    i.image = pygame.transform.rotate(i.image, 90)
                    tmp = s.width
                    s.width = s.height
                    s.height = tmp
                else:
                    v = self.world.component_for_entity(box2, components.Velocity)
                    self.world.add_component(n, components.Velocity(v.x, v.y))
                self.world.component_for_entity(n, components.Audio).sound.play()

        chest = self.world.create_entity()
        self.world.add_component(chest, components.Position(1070, 330))
        self.world.add_component(chest, components.Velocity(0, 0))
        self.world.add_component(chest, components.Image("chest.png"))
        self.world.add_component(chest, components.Flammable(False))
        self.world.add_component(chest, components.Size(80, 80))
        self.world.add_component(chest, components.Touch(anvil, open_chest, rect=pygame.Rect(0, 0, 0, 0)))
        self.world.add_component(chest, components.Audio("chest"))

        box = self.world.create_entity()
        self.world.add_component(box, components.Position(860, 330))
        self.world.add_component(box, components.Velocity(0, 0))
        self.world.add_component(box, components.Image("box1.png"))
        self.world.add_component(box, components.Flammable(False))
        self.world.add_component(box, components.Size(80, 80))
        self.world.add_component(box, components.Touch(anvil, open_box1, rect=pygame.Rect(0, 0, 0, 0)))
        self.world.add_component(box, components.Audio("heavy"))

        box2 = self.world.create_entity()
        self.world.add_component(box2, components.Position(950, 330))
        self.world.add_component(box2, components.Velocity(0, 0))
        self.world.add_component(box2, components.Image("box2.png"))
        self.world.add_component(box2, components.Flammable(False))
        self.world.add_component(box2, components.Size(80, 80))
        self.world.add_component(box2, components.Touch(anvil, open_box2, rect=pygame.Rect(0, 0, 0, 0)))
        self.world.add_component(box2, components.Audio("heavy"))

        lamp = self.world.create_entity()
        self.world.add_component(lamp, components.Position(520, 170))
        self.world.add_component(lamp, components.Image("Chandelier.png"))
        self.world.add_component(lamp, components.Flammable(True))
        self.world.add_component(lamp, components.Size(80, 80))
        self.world.add_component(lamp, components.Hang())

        lamp2 = self.world.create_entity()
        self.world.add_component(lamp2, components.Position(1000, 170))
        self.world.add_component(lamp2, components.Image("Chandelier.png"))
        self.world.add_component(lamp2, components.Flammable(True))
        self.world.add_component(lamp2, components.Size(80, 80))
        self.world.add_component(lamp2, components.Hang())

        forge = self.world.create_entity()
        self.world.add_component(forge, components.Position(1040, 520))
        self.world.add_component(anvil, components.Velocity(0, 0))
        self.world.add_component(forge, components.Image("Forge.png"))
        self.world.add_component(forge, components.Flammable(True))
        self.world.add_component(forge, components.Size(80, 160))
        self.world.add_component(anvil, components.Audio("heavy"))

        workbench = self.world.create_entity()
        self.world.add_component(workbench, components.Position(870, 560))
        self.world.add_component(workbench, components.Velocity(0, 0))
        self.world.add_component(workbench, components.Image("Workbench.png"))
        self.world.add_component(workbench, components.Flammable(False))
        self.world.add_component(workbench, components.Size(160, 80))
        self.world.add_component(workbench, components.Audio("heavy"))

        bubble = self.world.create_entity()
        self.world.add_component(bubble, components.Position(200, 100))
        self.world.add_component(bubble, components.Image("speech.png"))
        self.world.add_component(bubble, components.Size(307, 173))
        self.world.add_component(bubble, components.Hang())
        util.drawText(self.world.component_for_entity(bubble, components.Image).image, "Shoot, now where did that vase go? NaN, you touched it last. You need to find it for me!", (255, 255, 255), pygame.Rect(30, 20, 246, 134), self.small_font)

        def next_scene():
            self.switch_to_scene(text.TextScene("NaN was depressed. For the majority of his life he was the strongest, fastest, all around best adventurer in the whole realm. But it was his own effectiveness led to his now pitiful existence.", SceneSix()))

        def fade_out():
            for ent, i in self.world.get_component(components.Image):
                self.world.add_component(ent, components.ChangeAlpha(0, 1))
            for ent, a in self.world.get_component(components.Animation):
                self.world.add_component(ent, components.ChangeAlpha(0, 1))

        self.world.add_processor(processors.RenderProcessor())
        self.world.add_processor(processors.InputProcessor(), priority=10)
        self.world.add_processor(processors.PhysicsProcessor(600), priority=5)
        self.world.add_processor(processors.AnimationProcessor(), priority=5)
        self.world.add_processor(processors.PlayerProcessor(player, 60), priority=25)

class SceneSix(scenebase.SceneBase):
    def __init__(self):
        scenebase.SceneBase.__init__(self)

    def init(self):
        self.font = pygame.font.Font("kenpixel.ttf", 42)
        self.small_font = pygame.font.Font("kenpixel.ttf", 16)
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(100)
        pygame.mixer.music.load('audio/Space Cadet.ogg')
        pygame.mixer.music.play(-1)

        bg = self.world.create_entity()
        self.world.add_component(bg, components.Position(640, 360))
        self.world.add_component(bg, components.Image("HouseScene1BG.png"))
        self.world.add_component(bg, components.Size(1280, 720))
        self.world.add_component(bg, components.Background())

        player = get_player(self.world)

        floor2 = self.world.create_entity()
        self.world.add_component(floor2, components.Position(520, 390))
        self.world.add_component(floor2, components.Platform())
        self.world.add_component(floor2, components.Image("WoodPlatform3.png"))
        self.world.add_component(floor2, components.Size(720, 40))
        self.world.add_component(floor2, components.Background())

        stair = self.world.create_entity()
        self.world.add_component(stair, components.Position(1000, 500))
        self.world.add_component(stair, components.Platform())
        self.world.add_component(stair, components.Image("WoodPlatformHalf.png"))
        self.world.add_component(stair, components.Size(120, 40))
        self.world.add_component(stair, components.Background())

        step1 = self.world.create_entity()
        self.world.add_component(step1, components.Position(920, 440))
        self.world.add_component(step1, components.Platform())
        self.world.add_component(step1, components.Image("WoodPlatformThird.png"))
        self.world.add_component(step1, components.Size(80, 40))
        self.world.add_component(step1, components.Background())

        step2 = self.world.create_entity()
        self.world.add_component(step2, components.Position(1080, 560))
        self.world.add_component(step2, components.Platform())
        self.world.add_component(step2, components.Image("WoodPlatformThird.png"))
        self.world.add_component(step2, components.Size(80, 40))
        self.world.add_component(step2, components.Background())

        bed = self.world.create_entity()
        self.world.add_component(bed, components.Position(520, 330))
        self.world.add_component(bed, components.Velocity(0, 0))
        self.world.add_component(bed, components.Image("Bed.png"))
        self.world.add_component(bed, components.Flammable(False))
        self.world.add_component(bed, components.Size(160, 80))
        self.world.add_component(bed, components.Audio("heavy"))

        bed2 = self.world.create_entity()
        self.world.add_component(bed2, components.Position(760, 330))
        self.world.add_component(bed2, components.Velocity(0, 0))
        self.world.add_component(bed2, components.Image("Bed.png"))
        self.world.add_component(bed2, components.Flammable(False))
        self.world.add_component(bed2, components.Size(160, 80))
        self.world.add_component(bed2, components.Audio("heavy"))

        bed3 = self.world.create_entity()
        self.world.add_component(bed3, components.Position(280, 560))
        self.world.add_component(bed3, components.Velocity(0, 0))
        self.world.add_component(bed3, components.Image("Bed.png"))
        self.world.add_component(bed3, components.Flammable(False))
        self.world.add_component(bed3, components.Size(160, 80))
        self.world.add_component(bed3, components.Audio("heavy"))
        self.world.component_for_entity(bed3, components.Image).image = pygame.transform.flip(self.world.component_for_entity(bed3, components.Image).image, False, False)

        bed4 = self.world.create_entity()
        self.world.add_component(bed4, components.Position(520, 560))
        self.world.add_component(bed4, components.Velocity(0, 0))
        self.world.add_component(bed4, components.Image("Bed.png"))
        self.world.add_component(bed4, components.Flammable(False))
        self.world.add_component(bed4, components.Size(160, 80))
        self.world.add_component(bed4, components.Audio("heavy"))
        self.world.component_for_entity(bed4, components.Image).image = pygame.transform.flip(self.world.component_for_entity(bed4, components.Image).image, False, False)

        guy = self.world.create_entity()
        self.world.add_component(guy, components.Position(1000, 460))
        self.world.add_component(guy, components.Velocity(0, 0))
        self.world.add_component(guy, components.Image("NPC2.png"))
        self.world.add_component(guy, components.Flammable(False))
        self.world.add_component(guy, components.Size(80, 80))
        self.world.add_component(guy, components.Audio("grunt"))

        table = self.world.create_entity()
        self.world.add_component(table, components.Position(280, 330))
        self.world.add_component(table, components.Velocity(0, 0))
        self.world.add_component(table, components.Image("TableBig.png"))
        self.world.add_component(table, components.Flammable(False))
        self.world.add_component(table, components.Size(160, 80))
        self.world.add_component(table, components.Audio("heavy"))

        def puzzle_complete():
            complaint = self.world.create_entity()
            self.world.add_component(complaint, components.Position(640, 500))
            self.world.add_component(complaint, components.ChangeAlpha(0, 4, interpolation.Smooth()))
            self.world.add_component(complaint, components.Image("speech.png"))
            self.world.add_component(bubble, components.Size(307, 173))
            if(self.world.component_for_entity(mug, components.Flammable).lit):
                for ent, p in self.world.get_component(components.Player):
                    if p.holding is mug:
                        p.holding = None
                self.world.delete_entity(mug)
                util.drawText(self.world.component_for_entity(complaint, components.Image).image, "Way to take your time.", (255, 255, 255), pygame.Rect(30, 20, 246, 134), self.small_font)
                self.world.add_component(complaint, components.ChangePosition((640, 350), 4, interpolation.Smooth(), fade_out))
                self.world.add_component(complaint, components.Delay(5, next_scene))
            else:
                util.drawText(self.world.component_for_entity(complaint, components.Image).image, "It's cold! Heat it up for me.", (255, 255, 255), pygame.Rect(30, 20, 246, 134), self.small_font)

        mug = self.world.create_entity()
        self.world.add_component(mug, components.Position(250, 160))
        self.world.add_component(mug, components.Hang())
        self.world.add_component(mug, components.Image("Mug.png"))
        self.world.add_component(mug, components.Flammable(False))
        self.world.add_component(mug, components.Size(80, 80))
        self.world.add_component(mug, components.Touch(guy, puzzle_complete, True))
        self.world.add_component(mug, components.Audio("light"))

        lamp = self.world.create_entity()
        self.world.add_component(lamp, components.Position(520, 160))
        self.world.add_component(lamp, components.Image("Chandelier.png"))
        self.world.add_component(lamp, components.Flammable(True))
        self.world.add_component(lamp, components.Size(80, 80))
        self.world.add_component(lamp, components.Hang())

        lamp2 = self.world.create_entity()
        self.world.add_component(lamp2, components.Position(760, 160))
        self.world.add_component(lamp2, components.Image("Chandelier.png"))
        self.world.add_component(lamp2, components.Flammable(True))
        self.world.add_component(lamp2, components.Size(80, 80))
        self.world.add_component(lamp2, components.Hang())

        fireplace = self.world.create_entity()
        self.world.add_component(fireplace, components.Position(760, 520))
        self.world.add_component(fireplace, components.Image("Fireplace.png"))
        self.world.add_component(fireplace, components.Flammable(True))
        self.world.add_component(fireplace, components.Size(160, 160))
        self.world.add_component(fireplace, components.Velocity(0, 0))

        shelf = self.world.create_entity()
        self.world.add_component(shelf, components.Position(250, 210))
        self.world.add_component(shelf, components.Image("shelf.png"))
        self.world.add_component(shelf, components.Size(80, 20))

        bubble = self.world.create_entity()
        self.world.add_component(bubble, components.Position(1000, 100))
        self.world.add_component(bubble, components.Image("speech.png"))
        self.world.add_component(bubble, components.Size(307, 173))
        self.world.add_component(bubble, components.Hang())
        image = self.world.component_for_entity(bubble, components.Image).image
        util.drawText(image, "About time you got here, NaN. I need my coffee stat! It's probably been sitting there for hours!", (255, 255, 255), pygame.Rect(30, 20, 246, 134), self.small_font)

        def next_scene():
            #self.switch_to_scene(text.TextScene("NaN was unsure how much longer he could go on like this. He still wanted to help people, but was filled with thoughts of inadequacy and self doubt.", SceneSeven()))
            self.switch_to_scene(text.TextScene("Eventually he'd had enough. There was no way he could go back to adventuring, but he similarly could not stop here. He began a new journey, leaving his town without a single goodbye. Thanks for playing.", title.TitleScene()))

        def fade_out():
            for ent, i in self.world.get_component(components.Image):
                self.world.add_component(ent, components.ChangeAlpha(0, 1))
            for ent, a in self.world.get_component(components.Animation):
                self.world.add_component(ent, components.ChangeAlpha(0, 1))

        self.world.add_processor(processors.RenderProcessor())
        self.world.add_processor(processors.InputProcessor(), priority=10)
        self.world.add_processor(processors.PhysicsProcessor(600), priority=5)
        self.world.add_processor(processors.AnimationProcessor(), priority=5)
        self.world.add_processor(processors.PlayerProcessor(player, 40), priority=25)
