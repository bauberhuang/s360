import pygame

#init the system...
pygame.init()
x = 0
y = 0

#display screen(gotta be big lol) 2000x1000 is big enough lol lol lol
Imax_Screen = pygame.display.set_mode((800,600))

#Vibing the captions!!!
pygame.display.set_caption('Nishioi lol')

#Finally Image
image = pygame.image.load('nishioi.jpg')
# imax_sceen.print(image)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                y -= 100
                pygame.display.update()
            elif event.key == pygame.K_DOWN:
                y += 100
                pygame.display.update()
            elif event.key == pygame.K_LEFT:
                x -= 100
                pygame.display.update()
            elif event.key == pygame.K_RIGHT:
                x += 100
                pygame.display.update()
    Imax_Screen.blit(image, (x, y))
    pygame.display.flip()
    pygame.display.update()