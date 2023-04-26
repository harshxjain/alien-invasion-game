import sys
import pygame
from time import sleep

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien


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

        # Create an instance to store game statistics
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()


    def run_game(self):
        '''Start the main loop of the game'''

        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                
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
        elif event.key == pygame.K_q:  # Pressing 'Q' exits the game
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self, event):
        '''Check for key releases'''

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


    def _fire_bullet(self):
        '''Create a new bullet rect and add it to the bullets group'''

        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        '''Update the position of bullets and get rids of old bullets'''
        self.bullets.update()

        # Remove bullets that are off screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            # print(len(self.bullets))

        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        '''Respond to alien-bullet collisions'''
        
        # Check for any bullet that have hit aliens
        # If so, get rid of the bullet and alien
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()


    def _ship_hit(self):
        '''Respond to ship being hit by an alien'''

        if self.stats.ships_left > 0:
            # Decrement ships_left
            self.stats.ships_left -= 1
            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False


    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)


    def _create_fleet(self):
        '''Create a fleet of alien'''

        # Create an alien and find the number of aliens in a row
        # Spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # Determine the number of aliens that can fit in one row
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows that can fit the screen
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - \
            (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)

        # Create the first row of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                # Create an alien and place it in the row
                self._create_alien(alien_number, row_number)


    def _check_fleet_edges(self):
        '''Respond appropriately if an alien has reached the edge'''

        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
            

    def _check_aliens_bottom(self):
        '''Check if any aliens have hit bottom of the screen'''
        
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this as the same as when the ship got hit
                self._ship_hit()
                break


    def _change_fleet_direction(self):
        '''Drop the entire fleet and change the fleet direction'''

        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _update_aliens(self):
        '''Check if the fleet is at the edge, and update the position of all aliens in the fleet'''

        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()


    def _update_screen(self):
        '''Update images on screen and flip to the new screen'''

        # Redraw the screen during each pass throught the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets:
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game intance and run the game
    ai = AlienInvasion()
    ai.run_game()
