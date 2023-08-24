import pygame
import sys, os

pygame.init()

window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Gamw")

class Game:
    def __init__(self, x, y):
      self.x = x
      self.y = y
    
    def main(self):
        
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
    
        pygame.display.flip()

game = Game(2, 2)
game.main()

pygame.quit()