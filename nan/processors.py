import pygame
import esper
import components
import math

class RenderProcessor(esper.Processor):
    def __init__(self):
        esper.Processor.__init__(self)

    def process(self, filtered_events, pressed_keys, dt, screen):
        screen.fill((0, 0, 0))
        for ent, (i, p, s) in self.world.get_components(components.Image, components.Position, components.Size):
            if s.scale is 1:
                screen.blit(i.image, (p.x - s.width // 2, p.y - s.height // 2))
            else:
                image = pygame.transform.scale(i.image, (int(s.width * s.scale), int(s.height * s.scale)))
                screen.blit(image, (p.x - s.width * s.scale // 2, p.y - s.height * s.scale // 2))
        for ent, (c, p) in self.world.get_components(components.Circle, components.Position):
            pygame.draw.circle(screen, c.color, (int(p.x), int(p.y)), c.radius, c.width)
        for ent, (r, p) in self.world.get_components(components.Rect, components.Position):
            pygame.draw.rect(screen, c.color, r.rect)

class ClickProcessor(esper.Processor):
    def __init__(self):
        esper.Processor.__init__(self)

    def process(self, filtered_events, pressed_keys, dt, screen):
        for event in filtered_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for ent, (s, p, c) in self.world.get_components(components.Size, components.Position, components.Click):
                    if p.x - s.width // 2 <= x and p.x + s.width // 2 >= x and p.y - s.height // 2 <= y and p.y + s.height // 2 >= y:
                        c.run()

class OverProcessor(esper.Processor):
    def __init__(self):
        esper.Processor.__init__(self)

    def process(self, filtered_events, pressed_keys, dt, screen):
        for event in filtered_events:
            if event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                for ent, (s, p, o) in self.world.get_components(components.Size, components.Position, components.Over):
                    if p.x - s.width // 2 <= x and p.x + s.width // 2 >= x and p.y - s.height // 2 <= y and p.y + s.height // 2 >= y:
                        if not o.active:
                            o.enterf(ent)
                            o.active = True
                    elif o.active:
                        o.exitf(ent)
                        o.active = False

class PlayerProcessor(esper.Processor):
    def __init__(self, player):
        esper.Processor.__init__(self)
        self.player = player

    def process(self, filtered_events, pressed_keys, dt, screen):
        for event in filtered_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.world.component_for_entity(self.player, components.Velocity).x = -100
                elif event.key == pygame.K_RIGHT:
                    self.world.component_for_entity(self.player, components.Velocity).x = 100
                elif event.key == pygame.K_UP:
                    self.world.component_for_entity(self.player, components.Velocity).y = -100
                elif event.key == pygame.K_DOWN:
                    self.world.component_for_entity(self.player, components.Velocity).y = 100
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    self.world.component_for_entity(self.player, components.Velocity).x = 0
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    self.world.component_for_entity(self.player, components.Velocity).y = 0

class VelocityProcessor(esper.Processor):
    def __init__(self):
        esper.Processor.__init__(self)

    def process(self, filtered_events, pressed_keys, dt, screen):
        for ent, (p, v) in self.world.get_components(components.Position, components.Velocity):
            v.y = min(v.y + 9.81*10*dt, 53*10) # terminal velocity

            p.x = max(min(p.x + v.x * dt, 1280), 0)
            p.y = min(p.y + v.y * dt, 600)

class AnimationProcessor(esper.Processor):
    def __init__(self):
        esper.Processor.__init__(self)

    def process(self, filtered_events, pressed_keys, dt, screen):
        to_remove = []
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
                    c.chain(*c.args)
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
                    c.chain(*c.args)
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
                    c.chain(*c.args)
            else:
                x,y = c.target
                ox, oy = c.original
                x = x * c.interp.apply(c.current / c.time) + ox * (1 - c.interp.apply(c.current / c.time))
                y = y * c.interp.apply(c.current / c.time) + oy * (1 - c.interp.apply(c.current / c.time))

            v.x = x
            v.y = y

        # Alpha Animation
        for ent, (i, a) in self.world.get_components(components.Image, components.ChangeAlpha):
            if not a.current:
                a.current = dt
                a.original = a.start
            else:
                a.current += dt

            if a.current >= a.time:
                alpha = a.target
                to_remove.append((ent, components.ChangeAlpha))
                if a.chain:
                    a.chain(*a.args)
            else:
                alpha = a.target * a.interp.apply(a.current / a.time) + a.original * (1 - a.interp.apply(a.current / a.time))

            i.image.set_alpha(alpha * 255)

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
                    c.chain(*c.args)

        # Delay Animation
        for ent, d in self.world.get_component(components.Delay):
            d.time -= dt
            if d.time <= 0:
                to_remove.append((ent, components.Delay))
                if d.chain:
                    d.chain(*d.args)

        # Remove Components
        for (ent, comp) in to_remove:
            self.world.remove_component(ent, comp)
