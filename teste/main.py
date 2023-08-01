import pygame,sys,scripts.scenes

flags = pygame.OPENGL
screen = pygame.display.set_mode((1280,720),vsync=True)
pygame.display.set_caption("UmbrellaBoy")
clock = pygame.time.Clock()

demo = scripts.scenes.Demo(screen)


while True:
    screen.fill((47,83,163))

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    demo.update()

    clock.tick(60)
    pygame.display.flip()
