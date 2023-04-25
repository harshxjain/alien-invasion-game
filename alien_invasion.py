import sys
import pygame

from settings import Settings
from ship import Ship

class AlienInvasion:
    '''Overall class to manage game assets and behavior'''

    def __init__(self):
        '''Initialize the game and create game resources'''
        
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("ALIEN INVASION")

        self.ship = Ship(self)


    def run_game(self):
        '''Start the main loop of the game'''
        
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()
            

    def _check_events(self):
        '''Respond to key presses and mouse movements'''
        
        # Check if the player has closed the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)


    def _check_keydown_events(self, event):
        '''Check for key presses'''

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q: # Pressing 'Q' exits the game
            sys.exit()


    def _check_keyup_events(self, event):
        '''Check for key releases'''

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


    def _update_screen(self):
        '''Update images on screen and flip to the new screen'''
        
        # Redraw the screen during each pass throught the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
            
        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game intance and run the game
    ai = AlienInvasion()
    ai.run_game()