import pygame
import esper
import components
import math
import util

# TODO clean up, abstract, w/e
class RenderProcessor(esper.Processor):
    def __init__(self):
        esper.Processor.__init__(self)

    def render(self, ent, p, s, dt, screen):
        if self.world.has_component(ent, components.Image):
            i = self.world.component_for_entity(ent, components.Image)
            image = pygame.transform.scale(i.image, (int(s.width * s.scale), int(s.height * s.scale)))
            self.render_image(image, p, s, i.alpha, i.blend, screen)
        elif self.world.has_component(ent, components.Animation):
            a = self.world.component_for_entity(ent, components.Animation)
            a.time += dt
            frame = (a.time // a.framelength) % a.maxframes
            if a.framelength == -1:
                frame = a.frame
            rect = pygame.Rect(frame * a.splitx, 0, a.splitx, a.image.get_height())
            image = pygame.transform.scale(a.image.subsurface(rect), (int(s.width * s.scale), int(s.height * s.scale)))
            self.render_image(image, p, s, a.alpha, a.blend, screen)

    def render_image(self, image, p, s, alpha, blend, screen):
        if alpha == 255:
            screen.blit(image, (p.x - s.width * s.scale // 2, p.y - s.height * s.scale // 2), special_flags=blend)
        else:
            util.blit_alpha(screen, image, (p.x - s.width * s.scale // 2, p.y - s.height * s.scale // 2), alpha, blend)

    def process(self, filtered_events, pressed_keys, dt, screen):
        screen.fill((0, 64, 0))
        for ent, (b, p, s) in self.world.get_components(components.Background, components.Position, components.Size):
            self.render(ent, p, s, dt, screen)

        for ent, (a, p, s) in self.world.get_components(components.Animation, components.Position, components.Size):
            if self.world.has_component(ent, components.Player) or self.world.has_component(ent, components.Background):
                continue
            self.render(ent, p, s, dt, screen)

        for ent, (i, p, s) in self.world.get_components(components.Image, components.Position, components.Size):
            if self.world.has_component(ent, components.Player) or self.world.has_component(ent, components.Background):
                continue
            self.render(ent, p, s, dt, screen)

        for ent, (c, p) in self.world.get_components(components.Circle, components.Position):
            pygame.draw.circle(screen, c.color, (int(p.x), int(p.y)), c.radius, c.width)

        for ent, r in self.world.get_component(components.Rect):
            pygame.draw.rect(screen, r.color, r.rect)

        for ent, (pl, p, s) in self.world.get_components(components.Player, components.Position, components.Size):
            self.render(ent, p, s, dt, screen)

class InputProcessor(esper.Processor):
    def __init__(self):
        esper.Processor.__init__(self)

    def process(self, filtered_events, pressed_keys, dt, screen):
        for event in filtered_events:
            if event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                x *= 1280 / pygame.display.get_surface().get_width()
                y *= 720 / pygame.display.get_surface().get_height()
                for ent, (s, p, o) in self.world.get_components(components.Size, components.Position, components.Over):
                    if p.x - s.width * s.scale // 2 <= x and p.x + s.width * s.scale // 2 >= x and p.y - s.height * s.scale / 2 <= y and p.y + s.height * s.scale // 2 >= y:
                        if not o.active:
                            o.enterf(ent)
                            o.active = True
                    elif o.active:
                        o.exitf(ent)
                        o.active = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x *= 1280 / pygame.display.get_surface().get_width()
                y *= 720 / pygame.display.get_surface().get_height()
                for ent, (s, p, c) in self.world.get_components(components.Size, components.Position, components.Click):
                    if p.x - s.width * s.scale // 2 <= x and p.x + s.width * s.scale // 2 >= x and p.y - s.height // 2 <= y and p.y + s.height // 2 >= y:
                        c.run()

class PlayerProcessor(esper.Processor):
    left_down = False
    right_down = False

    def __init__(self, player, vitality):
        esper.Processor.__init__(self)
        self.player = player
        self.vitality = vitality

    def process(self, filtered_events, pressed_keys, dt, screen):
        v = self.world.component_for_entity(self.player, components.Velocity)
        p = self.world.component_for_entity(self.player, components.Player)
        s = self.world.component_for_entity(self.player, components.Size)
        pos = self.world.component_for_entity(self.player, components.Position)
        for event in filtered_events:
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and not self.left_down:
                    v.x -= 3 * self.vitality
                    self.left_down = True
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and not self.right_down:
                    v.x += 3 * self.vitality
                    self.right_down = True
                elif (event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE) and v.y == 0:
                    v.y -= 6 * self.vitality
                elif event.key == pygame.K_e:
                    if p.holding:
                        if self.world.has_component(self.player, components.Image):
                            self.world.remove_component(self.player, components.Image)
                            self.world.add_component(self.player, p.image)
                        elif self.world.has_component(self.player, components.Animation):
                            self.world.remove_component(self.player, components.Animation)
                            self.world.add_component(self.player, p.animation)
                        i = self.world.component_for_entity(p.holding, components.Image)
                        i.image = pygame.transform.rotate(i.image, -90)
                        self.world.add_component(p.holding, components.Velocity(0,0))
                        p.holding = None
                    else:
                        rect = pygame.Rect(pos.x, pos.y - s.height * s.scale / 2, s.width * s.scale * (1 if p.facing_right else -1), s.height * s.scale)
                        rect.normalize()
                        for ent, (p2, i) in self.world.get_components(components.Position, components.Image):
                            if self.world.has_component(ent, components.Player):
                                continue
                            if rect.collidepoint(p2.x, p2.y):
                                p.holding = ent
                                if self.world.has_component(self.player, components.Image):
                                    self.world.remove_component(self.player, components.Image)
                                    self.world.add_component(self.player, p.carry_image)
                                elif self.world.has_component(self.player, components.Animation):
                                    self.world.remove_component(self.player, components.Animation)
                                    self.world.add_component(self.player, p.carry_animation)
                                i.image = pygame.transform.rotate(i.image, 90)
                                self.world.remove_component(ent, components.Velocity)
            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.left_down:
                    v.x += 3 * self.vitality
                    self.left_down = False
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.right_down:
                    v.x -= 3 * self.vitality
                    self.right_down = False

            elif event.type == pygame.MOUSEBUTTONDOWN and p.holding:
                if self.world.has_component(self.player, components.Image):
                    self.world.remove_component(self.player, components.Image)
                    self.world.add_component(self.player, p.image)
                elif self.world.has_component(self.player, components.Animation):
                    self.world.remove_component(self.player, components.Animation)
                    self.world.add_component(self.player, p.animation)
                i = self.world.component_for_entity(p.holding, components.Image)
                i.image = pygame.transform.rotate(i.image, -90)
                x = event.pos[1] * 1280 / pygame.display.get_surface().get_width()
                y = event.pos[0] * 720 / pygame.display.get_surface().get_height()
                angle = math.atan2(x - pos.y, y - pos.x) % (2 * math.pi)
                self.world.add_component(p.holding, components.Velocity(math.cos(angle)*16 * self.vitality, math.sin(angle)*12 * self.vitality))
                self.world.add_component(p.holding, components.RotationalVelocity(320))
                p.holding = None

            if v.x == 0 and self.world.has_component(self.player, components.Animation):
                self.world.remove_component(self.player, components.Animation)
                if p.holding:
                    self.world.add_component(self.player, p.carry_image)
                else:
                    self.world.add_component(self.player, p.image)
            elif v.x != 0 and self.world.has_component(self.player, components.Image):
                self.world.remove_component(self.player, components.Image)
                if p.holding:
                    self.world.add_component(self.player, p.carry_animation)
                else:
                    self.world.add_component(self.player, p.animation)

            if (p.facing_right and v.x < 0) or (not p.facing_right and v.x > 0):
                p.facing_right = not p.facing_right
                p.image.image = pygame.transform.flip(p.image.image, True, False)
                p.animation.image = pygame.transform.flip(p.animation.image, True, False)
                p.carry_image.image = pygame.transform.flip(p.carry_image.image, True, False)
                p.carry_animation.image = pygame.transform.flip(p.carry_animation.image, True, False)

        if p.holding:
            p3 = self.world.component_for_entity(p.holding, components.Position)
            p3.x = pos.x
            p3.y = pos.y - s.height

class PhysicsProcessor(esper.Processor):
    def __init__(self, ground=-1):
        esper.Processor.__init__(self)
        self.ground = ground

    def process(self, filtered_events, pressed_keys, dt, screen):
        for ent, (p, s, v) in self.world.get_components(components.Position, components.Size, components.Velocity):
            v.y = min(v.y + 9.81*100*dt, 53*100) # terminal velocity
            if not self.world.has_component(ent, components.Player):
                v.x *= .98

            p.x = max(min(p.x + v.x * dt, 1280), 0)
            if self.ground != -1:
                p.y = min(p.y + v.y * dt, self.ground - s.height * s.scale / 2)

                if p.y >= self.ground - s.height * s.scale / 2 and v.y > 0:
                    v.y = 0

                if p.y >= self.ground - s.height * s.scale / 2 and self.world.has_component(ent, components.RotationalVelocity):
                    r = self.world.component_for_entity(ent, components.RotationalVelocity)
                    i = self.world.component_for_entity(ent, components.Image)
                    i.image = r.image
                    s.scale = r.scale
                    self.world.remove_component(ent, components.RotationalVelocity)
            else:
                p.y -= v.y * dt

        for ent, (t, p, s)  in self.world.get_components(components.Touch, components.Position, components.Size):
            rect = pygame.Rect(p.x - s.width / 2 + t.rect.x, p.y - s.height / 2 + t.rect.y, s.width + t.rect.width, s.height + t.rect.height)
            tp = self.world.component_for_entity(t.target, components.Position)
            ts = self.world.component_for_entity(t.target, components.Size)
            if rect.colliderect(pygame.Rect(tp.x, tp.y, ts.width, ts.height)):
                if not t.active:
                    t.touch()
                    if t.multi:
                        t.active = True
                    else:
                        self.world.remove_component(ent, components.Touch)
            else:
                t.active = False

        #Platform Physics
        for platEnt, (c, box, pf) in self.world.get_components(components.Position, components.Size, components.Platform):
            for ent, (p, s, v) in self.world.get_components(components.Position, components.Size, components.Velocity):
                if not self.world.has_component(ent, components.Platform):
                    if c.x - box.width/2 < p.x < c.x + box.width/2 and c.y + box.height/2 < p.y < c.y - box.height/2 :
                        if c.x - 20 < p.x < c.x + 20 and c.y + 20 < p.y < c.y - 20 :
                            p.y = min(c.y - box.height, p.y)
                            v.y = min(0, v.y)

class AnimationProcessor(esper.Processor):
    def __init__(self):
        esper.Processor.__init__(self)

    def process(self, filtered_events, pressed_keys, dt, screen):
        to_remove = []
        to_run = []
        # Position Animation
        for ent, (p, c) in self.world.get_components(components.Position, components.ChangePosition):
            if c.current is None:
                c.current = dt
                c.original = (p.x, p.y)
            else:
                c.current += dt

            if c.current >= c.time:
                x,y = c.target
                to_remove.append((ent, components.ChangePosition))
                if c.chain:
                    to_run.append((c.chain, c.args))
            else:
                x,y = c.target
                ox, oy = c.original
                x = x * c.interp.apply(c.current / c.time) + ox * (1 - c.interp.apply(c.current / c.time))
                y = y * c.interp.apply(c.current / c.time) + oy * (1 - c.interp.apply(c.current / c.time))

            p.x = x
            p.y = y

        # Size Animation
        for ent, (s, c) in self.world.get_components(components.Size, components.ChangeSize):
            if not c.current:
                c.current = dt
                c.original = s.scale
            else:
                c.current += dt

            if c.current >= c.time:
                scale = c.target
                to_remove.append((ent, components.ChangeSize))
                if c.chain:
                    to_run.append((c.chain, c.args))
            else:
                scale = c.target * c.interp.apply(c.current / c.time) + c.original * (1 - c.interp.apply(c.current / c.time))

            s.scale = scale

        # Velocity Animation
        for ent, (v, c) in self.world.get_components(components.Velocity, components.ChangeVelocity):
            if not c.current:
                c.current = dt
                c.original = (v.x,v.y)
            else:
                c.current += dt

            if c.current >= c.time:
                x,y = c.target
                to_remove.append((ent, components.ChangeVelocity))
                if c.chain:
                    to_run.append((c.chain, c.args))
            else:
                x,y = c.target
                ox, oy = c.original
                x = x * c.interp.apply(c.current / c.time) + ox * (1 - c.interp.apply(c.current / c.time))
                y = y * c.interp.apply(c.current / c.time) + oy * (1 - c.interp.apply(c.current / c.time))

            v.x = x
            v.y = y

        # Alpha Animation
        for ent, a in self.world.get_component(components.ChangeAlpha):
            if not a.current:
                a.current = dt
                if self.world.has_component(ent, components.Image):
                    a.original = self.world.component_for_entity(ent, components.Image).alpha / 255
                elif self.world.has_component(ent, components.Animation):
                    a.original = self.world.component_for_entity(ent, components.Animation).alpha / 255
            else:
                a.current += dt

            if a.current >= a.time:
                alpha = a.target
                to_remove.append((ent, components.ChangeAlpha))
                if a.chain:
                    to_run.append((a.chain, a.args))
            else:
                alpha = a.target * a.interp.apply(a.current / a.time) + a.original * (1 - a.interp.apply(a.current / a.time))

            if self.world.has_component(ent, components.Image):
                self.world.component_for_entity(ent, components.Image).alpha = alpha * 255
            elif self.world.has_component(ent, components.Animation):
                self.world.component_for_entity(ent, components.Animation).alpha = alpha * 255

        # Circle Animation
        for ent, (v, c) in self.world.get_components(components.Velocity, components.CircleAnimation):
            c.current += dt
            oldy = v.y
            v.x = math.cos(math.pi * 2 * c.current / c.time) * c.radius / c.time
            v.y = math.sin(math.pi * 2 * c.current / c.time) * c.radius / c.time
            if abs((math.pi * 2 * c.current / c.time) % (2 * math.pi) - c.stopangle % (2 * math.pi)) < .1:
                if not c.loop:
                    to_remove.append((ent, components.Velocity))
                    to_remove.append((ent, components.CircleAnimation))
                if c.chain:
                    to_run.append((c.chain, c.args))

        # Rotational Velocity
        for ent, (i, r, s) in self.world.get_components(components.Image, components.RotationalVelocity, components.Size):
            if not r.image:
                r.image = i.image
                r.scale = s.scale
            width = i.image.get_width()
            r.angle += dt * r.speed
            i.image = pygame.transform.rotate(r.image, r.angle)
            s.scale *= i.image.get_width() / width

        # Delay Animation
        for ent, d in self.world.get_component(components.Delay):
            d.time -= dt
            if d.time <= 0:
                to_remove.append((ent, components.Delay))
                if d.chain:
                    to_run.append((d.chain, d.args))

        # Remove Components
        for (ent, comp) in to_remove:
            self.world.remove_component(ent, comp)

        for (chain, args) in to_run:
            chain(*args)

class TitleProcessor(esper.Processor):
    x = 0
    y = 0

    def __init__(self, title):
        esper.Processor.__init__(self)
        self.title = title

    def process(self, filtered_events, pressed_keys, dt, screen):
        for event in filtered_events:
            if event.type == pygame.MOUSEMOTION:
                p = self.world.component_for_entity(self.title, components.Position)
                if self.x == 0:
                    self.x = p.x
                    self.y = p.y
                mousex, mousey = pygame.mouse.get_pos()
                mousex *= 1280 / pygame.display.get_surface().get_width()
                mousey *= 720 / pygame.display.get_surface().get_height()
                p.x = self.x + (self.x - mousex) / 10
                p.y = self.y + (self.y - mousey) / 10

class TextProcessor(esper.Processor):
    def __init__(self, callback):
        esper.Processor.__init__(self)
        self.callback = callback

    def process(self, filtered_events, pressed_keys, dt, screen):
        for event in filtered_events:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.callback()


class Scene1Processor(esper.Processor):
    def __init__(self, player, tutorial, font):
        esper.Processor.__init__(self)
        self.player = player
        self.tutorial = tutorial
        self.font = font

    def process(self, filtered_events, pressed_keys, dt, screen):
        p = self.world.component_for_entity(self.player, components.Position)
        if p.x > 900:
            p.x = 900

        for event in filtered_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    image = self.font.render("aim your mouse and click to throw", False, (32, 255, 128))
                    self.world.component_for_entity(self.tutorial, components.Image).image = image
                    imgs = self.world.component_for_entity(self.tutorial, components.Size)
                    imgs.width = image.get_width()
                    imgs.height = image.get_height()

class Scene2Processor(esper.Processor):
    def __init__(self, player):
        esper.Processor.__init__(self)
        self.player = player

    def process(self, filtered_events, pressed_keys, dt, screen):
        pass
