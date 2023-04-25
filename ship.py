import pygame

class Ship:
    '''A class to manage the ship'''

    def __init__(self, ai_game):
        '''Initialize the ship and set it's starting position'''

        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Movement flag
        self.moving_right = False
        self.moving_left = False

        # Store a decimal value for the ship's x coordinate
        self.x = float(self.rect.x)

    def update(self):
        '''Update ship's position based on the movement flag'''

        # Update ship's x value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        elif self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed

        # Update ship's rect x
        self.rect.x = self.x

    def blitme(self):
        '''Draw the ship at its current position'''
        self.screen.blit(self.image, self.rect)