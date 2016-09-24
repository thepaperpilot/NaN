import pygame
import esper
import title

def run_game(width, height, titletext, fps, starting_scene):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(titletext)
    clock = pygame.time.Clock()

    starting_scene.init()
    active_scene = starting_scene

    font = pygame.font.Font("RobotoMono-Regular.ttf", 24)

    while active_scene is not None:
        dt = clock.tick(fps)

        # event handling
        filtered_events = []
        pressed_keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or \
                              pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True

            if quit_attempt:
                active_scene.terminate()
            else:
                filtered_events.append(event)

        active_scene.world.process(filtered_events, pressed_keys, dt / 1000, screen)

        text = font.render("FPS: " + str(int(1000*1//dt)), True, (0, 128, 0))
        screen.blit(text, (10, 10))

        active_scene = active_scene.next

        pygame.display.flip()

run_game(1280, 720, "NaN", 60, title.TitleScene())
