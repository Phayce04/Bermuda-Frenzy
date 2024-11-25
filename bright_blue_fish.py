import pygame
import random
from utils import SCREEN_WIDTH, SCREEN_HEIGHT

class BrightBlueFish(pygame.sprite.Sprite):
    OFFSCREEN_LEFT = -1000
    OFFSCREEN_RIGHT = SCREEN_WIDTH + 1000
    MOVEMENT_SPEED = 4
    ARROW_REMOVAL_BOUNDARY = 100
    SPAWN_Y_RANGE = (50, SCREEN_HEIGHT - 200)
    ACTIVATION_SCORE = 50
    DIR_LEFT = 0
    DIR_RIGHT = 1

    def __init__(self, allsprites, images):
        super().__init__()
        self.images = images
        self.direction = random.choice([self.DIR_LEFT, self.DIR_RIGHT])
        self.activate = False
        self.initialize_sprite(allsprites)
        if self.direction == self.DIR_LEFT:
            x_position = self.OFFSCREEN_RIGHT
            y_position = random.randrange(*self.SPAWN_Y_RANGE)
            self.rect.topleft = (x_position, y_position)
        else:
            x_position = self.OFFSCREEN_LEFT
            y_position = random.randrange(*self.SPAWN_Y_RANGE)
            self.rect.topright = (x_position, y_position)
        self.lateral_entry_complete = False
        self.game_over = False
        
    def update(self):
        if self.game_over:
            return
        if self.activate:
            self.update_movement_and_images()
            self.update_mask()
            if self.direction == self.DIR_RIGHT and self.rect.left > self.ARROW_REMOVAL_BOUNDARY:
                self.lateral_entry_complete = True
            elif self.direction == self.DIR_LEFT and self.rect.right < SCREEN_WIDTH - self.ARROW_REMOVAL_BOUNDARY:
                self.lateral_entry_complete = True
        
    def update_movement_and_images(self):
        if self.direction == self.DIR_RIGHT:
            self.image = self.images["spr_bright_blue_fish_right"]
            self.rect.move_ip(self.MOVEMENT_SPEED, 0)
            self.manage_boundaries_for_right_movement()
        elif self.direction == self.DIR_LEFT:
            self.image = self.images["spr_bright_blue_fish_left"]
            self.rect.move_ip(-self.MOVEMENT_SPEED, 0)
            self.manage_boundaries_for_left_movement()
        
    def is_out_of_world(self):
        return self.rect.right < 0 or self.rect.left > SCREEN_WIDTH
    
    def try_activate(self, score, last_activation_score):
        if (last_activation_score // self.ACTIVATION_SCORE < score // self.ACTIVATION_SCORE 
            and score >= self.ACTIVATION_SCORE 
            and self.is_out_of_world()):
            self.reset_position()
            self.activate_fish()
            return True
        return False
    
    def activate_fish(self):
        self.activate = True
        self.lateral_entry_complete = False
        if self.direction == self.DIR_RIGHT:
            self.rect.topright = (self.OFFSCREEN_LEFT, random.randrange(50, SCREEN_HEIGHT - 200))
        else:
            self.rect.topleft = (self.OFFSCREEN_RIGHT, random.randrange(50, SCREEN_HEIGHT - 200))

    def initialize_sprite(self, allsprites):
        self.image = self.images["spr_bright_blue_fish_right"]
        self.rect = self.image.get_rect()
        allsprites.add(self)

    def reset_position(self):
        x_position = random.choice([self.OFFSCREEN_LEFT, self.OFFSCREEN_RIGHT])
        y_position = random.randrange(*self.SPAWN_Y_RANGE)
        if x_position == self.OFFSCREEN_LEFT:
            self.direction = self.DIR_RIGHT
            self.rect.topright = (x_position, y_position)
        else:
            self.direction = self.DIR_LEFT
            self.rect.topleft = (x_position, y_position)

    def update_mask(self):
        if self.direction == self.DIR_RIGHT:
            self.mask = pygame.mask.from_surface(self.images["spr_bright_blue_fish_right_face"])
        elif self.direction == self.DIR_LEFT:
            self.mask = pygame.mask.from_surface(self.images["spr_bright_blue_fish_left_face"])

    def manage_boundaries_for_right_movement(self):
        if self.rect.left > SCREEN_WIDTH:
            self.activate = False

    def manage_boundaries_for_left_movement(self):
        if self.rect.right < 0:
            self.activate = False

    def remove_sprite(self):
        self.kill()

# Manage multiple BrightBlueFish instances# Manage multiple BrightBlueFish instances
class FishManager:
    ACTIVATION_SCORE = 300  # Set the score threshold for all fish to appear

    def __init__(self, allsprites, images):
        # Number of fish instances
        num_fish = 6
        
        # Divide the spawn range into distinct segments
        y_min, y_max = BrightBlueFish.SPAWN_Y_RANGE
        segment_height = (y_max - y_min) // num_fish

        # Create instances of BrightBlueFish with unique y-positions
        self.fish_list = []
        for i in range(num_fish):
            fish = BrightBlueFish(allsprites, images)
            
            # Calculate a unique y-position within each segment
            y_position = y_min + i * segment_height + random.randint(0, segment_height - 50)
            fish.rect.y = y_position
            self.fish_list.append(fish)
        
        self.last_activation_score = 0
        self.activated = False  # Track if all fish have been activated
    def spawn_forced_fish_batch(self):
        """Spawn a batch of fish regardless of score."""
        for fish in self.fish_list:
            fish.activate_fish()
    def update(self, score):
        # Check if the activation score has been reached and not yet activated
        if score >= self.ACTIVATION_SCORE and not self.activated:
            self.activated = True
            self.last_activation_score = score  # Update the last activation score
            
            # Activate all fish simultaneously
            for fish in self.fish_list:
                fish.activate_fish()
        
        # Update each fish in the list
        for fish in self.fish_list:
            fish.update()


class FishManager2:
    ACTIVATION_SCORE = 330  # Set the score threshold for all fish to appear

    def __init__(self, allsprites, images):
        # Number of fish instances
        num_fish = 5
        
        # Divide the spawn range into distinct segments
        y_min, y_max = BrightBlueFish.SPAWN_Y_RANGE
        segment_height = (y_max - y_min) // num_fish

        # Create instances of BrightBlueFish with unique y-positions
        self.fish_list3 = []
        for i in range(num_fish):
            fish = BrightBlueFish(allsprites, images)
            
            # Calculate a unique y-position within each segment
            y_position = y_min + i * segment_height + random.randint(0, segment_height - 50)
            fish.rect.y = y_position
            self.fish_list3.append(fish)
        
        self.last_activation_score = 0
        self.activated = False  # Track if all fish have been activated
    def spawn_forced_fish_batch(self):
        """Spawn a batch of fish regardless of score."""
        for fish in self.fish_list3:
            fish.activate_fish()
    def update(self, score):
        # Check if the activation score has been reached and not yet activated
        if score >= self.ACTIVATION_SCORE and not self.activated:
            self.activated = True
            self.last_activation_score = score  # Update the last activation score
            
            # Activate all fish simultaneously
            for fish in self.fish_list3:
                fish.activate_fish()
        
        # Update each fish in the list
        for fish in self.fish_list3:
            fish.update()


class FishManager3:
    ACTIVATION_SCORE = 370  # Set the score threshold for all fish to appear

    def __init__(self, allsprites, images):
        # Number of fish instances
        num_fish = 5
        
        # Divide the spawn range into distinct segments
        y_min, y_max = BrightBlueFish.SPAWN_Y_RANGE
        segment_height = (y_max - y_min) // num_fish

        # Create instances of BrightBlueFish with unique y-positions
        self.fish_list2 = []
        for i in range(num_fish):
            fish = BrightBlueFish(allsprites, images)
            
            # Calculate a unique y-position within each segment
            y_position = y_min + i * segment_height + random.randint(0, segment_height - 50)
            fish.rect.y = y_position
            self.fish_list2.append(fish)
        
        self.last_activation_score = 0
        self.activated = False  # Track if all fish have been activated
    def spawn_forced_fish_batch(self):
        """Spawn a batch of fish regardless of score."""
        for fish in self.fish_list2:
            fish.activate_fish()
    def update(self, score):
        # Check if the activation score has been reached and not yet activated
        if score >= self.ACTIVATION_SCORE and not self.activated:
            self.activated = True
            self.last_activation_score = score  # Update the last activation score
            
            # Activate all fish simultaneously
            for fish in self.fish_list2:
                fish.activate_fish()
        
        # Update each fish in the list
        for fish in self.fish_list2:
            fish.update()


class FishManager4:
    ACTIVATION_SCORE = 400  # Set the score threshold for all fish to appear

    def __init__(self, allsprites, images):
        # Number of fish instances
        num_fish = 7
        
        # Divide the spawn range into distinct segments
        y_min, y_max = BrightBlueFish.SPAWN_Y_RANGE
        segment_height = (y_max - y_min) // num_fish

        # Create instances of BrightBlueFish with unique y-positions
        self.fish_list2 = []
        for i in range(num_fish):
            fish = BrightBlueFish(allsprites, images)
            
            # Calculate a unique y-position within each segment
            y_position = y_min + i * segment_height + random.randint(0, segment_height - 50)
            fish.rect.y = y_position
            self.fish_list2.append(fish)
        
        self.last_activation_score = 0
        self.activated = False  # Track if all fish have been activated
    def spawn_forced_fish_batch(self):
        """Spawn a batch of fish regardless of score."""
        for fish in self.fish_list2:
            fish.activate_fish()
    def update(self, score):
        # Check if the activation score has been reached and not yet activated
        if score >= self.ACTIVATION_SCORE and not self.activated:
            self.activated = True
            self.last_activation_score = score  # Update the last activation score
            
            # Activate all fish simultaneously
            for fish in self.fish_list2:
                fish.activate_fish()
        
        # Update each fish in the list
        for fish in self.fish_list2:
            fish.update()


class FishManager5:
    ACTIVATION_SCORE = 450  # Set the score threshold for all fish to appear

    def __init__(self, allsprites, images):
        # Number of fish instances
        num_fish = 7
        
        # Divide the spawn range into distinct segments
        y_min, y_max = BrightBlueFish.SPAWN_Y_RANGE
        segment_height = (y_max - y_min) // num_fish

        # Create instances of BrightBlueFish with unique y-positions
        self.fish_list2 = []
        for i in range(num_fish):
            fish = BrightBlueFish(allsprites, images)
            
            # Calculate a unique y-position within each segment
            y_position = y_min + i * segment_height + random.randint(0, segment_height - 50)
            fish.rect.y = y_position
            self.fish_list2.append(fish)
        
        self.last_activation_score = 0
        self.activated = False  # Track if all fish have been activated
    def spawn_forced_fish_batch(self):
        """Spawn a batch of fish regardless of score."""
        for fish in self.fish_list2:
            fish.activate_fish()
    def update(self, score):
        # Check if the activation score has been reached and not yet activated
        if score >= self.ACTIVATION_SCORE and not self.activated:
            self.activated = True
            self.last_activation_score = score  # Update the last activation score
            
            # Activate all fish simultaneously
            for fish in self.fish_list2:
                fish.activate_fish()
        
        # Update each fish in the list
        for fish in self.fish_list2:
            fish.update()
