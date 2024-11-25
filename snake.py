import pygame
import random
from utils import SCREEN_WIDTH, SCREEN_HEIGHT

class Snake(pygame.sprite.Sprite):
    OFF_SCREEN_LEFT = -80
    OFF_SCREEN_RIGHT = SCREEN_WIDTH
    NORMAL_RESPAWN_TIMER = 5000  # Normal respawn time
    FAST_RESPAWN_TIMER = 3000     # Faster respawn time after 100 points
    NORMAL_SPEED = 2            # Normal speed
    FAST_SPEED = 4              # Faster speed after 100 points
    NORMAL_SIZE = 1.0           # Normal size multiplier
    BIGGER_SIZE = 1.5           # Bigger size multiplier after 100 points
    ANIMATION_CYCLE_LENGTH = 5000
    DIRECTION_LEFT = -1
    DIRECTION_RIGHT = 1
    BOTTOM_POSITION_Y_RANGE = (SCREEN_HEIGHT - 80, SCREEN_HEIGHT - 60)

    def __init__(self, allsprites, images):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = self.images["spr_snake_1"]
        self.rect = self.image.get_rect()
        allsprites.add(self)

        # Initialize attributes
        self.size_multiplier = Snake.NORMAL_SIZE  # Initialize size_multiplier here
        self.respawn_timer = Snake.NORMAL_RESPAWN_TIMER  # Normal respawn time
        self.timer = -self.respawn_timer  # This will allow the snake to appear after a delay
        self.snake_animator = 0
        self.speed = Snake.NORMAL_SPEED  # Initialize speed
        self.direction = random.choice([Snake.DIRECTION_LEFT, Snake.DIRECTION_RIGHT])  # Random initial direction
        self.reset_position()

    def update(self):
        if not self.is_in_game_world():
            self.timer += 1

        self.snake_animator = (self.snake_animator + 1) % Snake.ANIMATION_CYCLE_LENGTH
        self.update_animation()

        if self.timer >= 0 and self.timer < self.respawn_timer:
            self.move()

        if (self.direction == Snake.DIRECTION_LEFT and self.rect.right < Snake.OFF_SCREEN_LEFT) or \
           (self.direction == Snake.DIRECTION_RIGHT and self.rect.left > Snake.OFF_SCREEN_RIGHT):
            self.reset_position()

    def move(self):
        """Move the snake in the current direction with the current speed."""
        self.rect.x += self.speed * self.direction

    def reset_position(self):
        """Reset snake position and resize based on current size multiplier."""
        if self.direction == Snake.DIRECTION_LEFT:
            self.rect.x = Snake.OFF_SCREEN_RIGHT
        else:
            self.rect.x = Snake.OFF_SCREEN_LEFT - self.rect.width
            
        # Adjust the spawn range after resizing
        self.rect.y = random.randint(SCREEN_HEIGHT - 100, SCREEN_HEIGHT - 80)  # Higher spawn range after resize
        
        self.timer = 0  # Reset timer when the snake respawns

        # Resize the snake based on the size multiplier
        self.rect.width = int(self.rect.width * self.size_multiplier)
        self.rect.height = int(self.rect.height * self.size_multiplier)

        # Ensure the snake stays within the screen bounds after resizing
        if self.rect.x < 0:  # Avoid going off-screen left
            self.rect.x = 0
        if self.rect.x + self.rect.width > SCREEN_WIDTH:  # Avoid going off-screen right
            self.rect.x = SCREEN_WIDTH - self.rect.width

        # Reset the image to match the new size
        self.image = pygame.transform.scale(self.images["spr_snake_1"], (self.rect.width, self.rect.height))


    def update_animation(self):
        frame = (self.snake_animator // 5) % 4 + 1
        if self.direction == Snake.DIRECTION_LEFT:
            self.image = self.images[f"spr_snake_{frame}"]
        else:
            self.image = pygame.transform.flip(self.images[f"spr_snake_{frame}"], True, False)

    def is_in_game_world(self):
        return self.rect.right > Snake.OFF_SCREEN_LEFT and self.rect.left < Snake.OFF_SCREEN_RIGHT

    def collide_with_player(self):
        self.reset_position()

    def collide_with_bright_blue_fish(self):
        self.reset_position()

    def remove_sprite(self):
        self.kill()

    def set_respawn_timer(self, new_timer):
        """Method to change the respawn timer dynamically."""
        self.respawn_timer = new_timer

    def set_speed(self, new_speed):
        """Method to change the speed dynamically."""
        self.speed = new_speed

    def set_size(self, new_size_multiplier):
        """Method to change the size dynamically by scaling the image."""
        self.size_multiplier = new_size_multiplier
        # Rescale the image based on the size multiplier
        new_width = int(self.image.get_width() * self.size_multiplier)
        new_height = int(self.image.get_height() * self.size_multiplier)

        # Scale the image
        self.image = pygame.transform.scale(self.images["spr_snake_1"], (new_width, new_height))

        # Update the rect to match the new image size
        self.rect = self.image.get_rect(center=self.rect.center)
