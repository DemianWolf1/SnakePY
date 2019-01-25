import pygame


class Borders:
    def createlist(self, width=640, height=480, size=10):
        """ in - (self)
Creates a list of borderss Rect objects.
out - list"""
        bounds = []
        bounds.append(pygame.Rect((0, height - size), (width, size))) # down bound
        bounds.append(pygame.Rect((0, 0), (width, size))) # upper bound
        bounds.append(pygame.Rect((0, 0), (size, height))) # left bound
        bounds.append(pygame.Rect((width-size, 0), (size, height))) # right bound
        return bounds

if __name__ == "__main__":
    import sys
    pygame.init()
    scr = pygame.display.set_mode((640, 480))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        scr.fill((0,0,0))
        for i in Borders().createlist(width=640, height=480, size=10):
            pygame.draw.rect(scr, (100, 100, 255), i)
        pygame.display.flip()
