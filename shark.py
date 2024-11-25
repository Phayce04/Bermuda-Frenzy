import pygame
import random
from utils import SCREEN_WIDTH, SCREEN_HEIGHT  # Assuming you have a config.py with constants

class Shark(pygame.sprite.Sprite):
    TURN_TIME_MS = 50
    SHARKS_SCORES_TO_SPAWN = [25, 75, 125, 200, 200, 200,200, 400,450]
    CHASE_DURATION_MS = 10000  # 10 seconds in milliseconds
    MOVE_SPEED = 2
    PLAYER_SCORE_VALUE = 8
    Y_POSITION_SPAWN = -300
    Y_POSITION_TO_START_PLAYING = 125
    MOVE_CHASE_SPEED = 1
    MOVE_AVOID_SPEED = 2
    OFFSET_FROM_WALL = 10
    DESCEND_SPEED = 1
    def __init__(self, allsprites, images):
        """
        Most frequently-seen predator in the game.
        Starts coming from above and then bounces around the room
        Only time player can avoid:
        When player has a star powerup, shark respawns
        When player has mini shark powerup, they can eat sharks
        """
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = images["spr_shark_left"]
        self.face_image = images["spr_shark_face_left"]
        self.rect = self.image.get_rect()
        allsprites.add(self)
        self.direction = (random.choice([-self.MOVE_SPEED, self.MOVE_SPEED]),
                          random.choice([-self.MOVE_SPEED, self.MOVE_SPEED]))
        self.mini_shark = False
        self.activate = False
        self.rect.topleft = (random.randrange(100, SCREEN_WIDTH - 100), self.Y_POSITION_SPAWN)
        self.stop_timer = 0
        self.initial_descent_complete = False
        self.mask = pygame.mask.from_surface(self.face_image)
        
        self.game_over = False
        self.chase_timer_start = None
        self.is_chasing = False
        self.is_avoiding = False
        self.is_spawned = False  # Track if the shark has been spawned based on score


    def spawn_if_score_met(self, player_score):
        """Spawn the shark if the player's score meets the threshold."""
        if not self.is_spawned and player_score >= self.SPAWN_SCORE_THRESHOLD:
            self.is_spawned = True
            self.activate = True
            self.chase_timer_start = pygame.time.get_ticks()
            self.is_chasing = True

    def start_chase(self):
        """Start chasing the player."""
        self.chase_timer_start = pygame.time.get_ticks()
        self.is_chasing = True
        self.is_avoiding = False

    def update(self, player_pos, player_score):
        if self.game_over:
            return
        self.spawn_if_score_met(player_score)
        current_time = pygame.time.get_ticks()

        # Start chase if within view and not already chasing
        if self.activate and not self.initial_descent_complete:
            if self.rect.top < self.Y_POSITION_TO_START_PLAYING:
                self.rect.y += self.DESCEND_SPEED
            else:
                self.initial_descent_complete = True
                self.start_chase()  # Begin chase when shark is fully visible
            self.update_image_and_mask()

        elif self.is_chasing:
            # Check if chase duration has elapsed
            if current_time - self.chase_timer_start < self.CHASE_DURATION_MS:
                self.chase_player(player_pos)  # Chase the player
            else:
                self.is_chasing = False
                self.is_avoiding = True  # Switch to avoiding mode

        elif self.is_avoiding:
            self.avoid_player(player_pos)  # Avoid the player
            # Despawn after avoiding
            if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT or \
               self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
                self.kill()  # Remove shark from game after avoiding and moving off screen

        else:
            # Regular movement if not chasing or avoiding
            self.update_image_and_mask()
            self.move_shark()

    def update(self):
        if self.game_over:
            return
        if self.activate and not self.initial_descent_complete:
            if self.rect.top < self.Y_POSITION_TO_START_PLAYING:
                self.rect.y += self.DESCEND_SPEED # Move the shark downwards until it is fully visible
            else:
                self.initial_descent_complete = True
            self.update_image_and_mask()
        else:
            current_time = pygame.time.get_ticks()
    
            # Check if the turning period has elapsed
            if self.stop_timer > current_time:
                # During the turning time, keep the turning sprite
                if self.mini_shark == True:
                    self.image = pygame.transform.smoothscale(self.images["spr_shark_turning"], (60, 30))
                else:
                    self.image = self.images["spr_shark_turning"]
                # Do not move while in turning animation
            else:
                # After the turning period, update the sprite based on direction
                self.update_image_and_mask()
    
                # Regular movement code, allows movement after the turning period
                self.move_shark()

    def update_image_and_mask(self):
        # Update image based on direction
        if self.mini_shark == True:
            if self.direction[0] > 0:
                self.image = pygame.transform.smoothscale(self.images["spr_shark_right"], (60, 30))
            else:
                self.image = pygame.transform.smoothscale(self.images["spr_shark_left"], (60, 30))
            self.mask = pygame.mask.from_surface(self.image)
            
        else:
            if self.direction[0] > 0:
                self.image = self.images["spr_shark_right"]
                self.face_image = self.images["spr_shark_face_right"]
            else:
                self.image = self.images["spr_shark_left"]
                self.face_image = self.images["spr_shark_face_left"]
            self.mask = pygame.mask.from_surface(self.face_image)
    def move_shark(self):
        if self.rect.topleft[1] >= 0:
            newpos = self.rect.topleft[0] + self.direction[0], self.rect.topleft[1] + self.direction[1]
            self.rect.topleft = newpos
    def collision_with_wall(self, rect):
        if self.rect.colliderect(rect):
            # Change direction immediately on collision
            self.update_direction()

            # Trigger the turning animation for a set duration
            self.stop_timer = pygame.time.get_ticks() + Shark.TURN_TIME_MS

            # Offset the shark from the wall
            self.offset_from_wall()


    def offset_from_wall(self):
        # Offset the shark away from the wall based on its new direction
        if self.direction[0] > 0:  # Moving right
            self.rect.left += self.OFFSET_FROM_WALL
        elif self.direction[0] < 0:  # Moving left
            self.rect.right -= self.OFFSET_FROM_WALL
        if self.direction[1] > 0:  # Moving down
            self.rect.top += self.OFFSET_FROM_WALL
        elif self.direction[1] < 0:  # Moving up
            self.rect.bottom -= self.OFFSET_FROM_WALL
    def update_direction(self):
        # Determine the new direction based on which wall the shark collided with
        # The actual direction update happens after the turning animation
        if self.rect.left < 32:  # Collided with left wall
            self.direction = (self.MOVE_SPEED, random.choice([-self.MOVE_SPEED, self.MOVE_SPEED]))
        elif self.rect.right > SCREEN_WIDTH - 32:  # Collided with right wall
            self.direction = (-self.MOVE_SPEED, random.choice([-self.MOVE_SPEED, self.MOVE_SPEED]))
        elif self.rect.top < 32:  # Collided with top wall
            self.direction = (random.choice([-self.MOVE_SPEED, self.MOVE_SPEED]), self.MOVE_SPEED)
        elif self.rect.bottom > SCREEN_HEIGHT - 64:  # Collided with bottom wall
            self.direction = (random.choice([-self.MOVE_SPEED, self.MOVE_SPEED]), -self.MOVE_SPEED)

        # Update sprite based on new direction
        if self.direction[0] > 0:
            if self.mini_shark == True:
                pygame.transform.smoothscale(self.images["spr_shark_right"], (60, 30))
            else:
                self.image = self.images["spr_shark_right"]
        else:
            if self.mini_shark == True:
                pygame.transform.smoothscale(self.images["spr_shark_left"], (60, 30))
            else:
                self.image = self.images["spr_shark_left"]
    def handle_timer_event(self):
        # This method should be called when a USEREVENT + 1 is triggered
        if self.rect.left < 32:  # Left walls
            self.direction = (3, random.choice([-self.MOVE_SPEED, self.MOVE_SPEED]))
        elif self.rect.top > SCREEN_HEIGHT - 64:  # Bottom walls
            self.direction = (random.choice([-self.MOVE_SPEED, self.MOVE_SPEED]), -self.MOVE_SPEED)
        elif self.rect.right > SCREEN_WIDTH - 32:  # Right walls
            self.direction = (-self.MOVE_SPEED, random.choice([-self.MOVE_SPEED, self.MOVE_SPEED]))
        elif self.rect.top < 32:  # Top walls
            self.direction = (random.choice([-self.MOVE_SPEED, self.MOVE_SPEED]), self.MOVE_SPEED)

        # Update sprite based on new direction
        if self.direction[0] > 0:
            self.image = self.images["spr_shark_right"]
        else:
            self.image = self.images["spr_shark_left"]
    
    def chase_player(self, player_pos):
        # Move towards the player's position
        if self.rect.x > player_pos[0]:
            self.rect.x -= self.MOVE_CHASE_SPEED
        elif self.rect.x < player_pos[0]:
            self.rect.x += self.MOVE_CHASE_SPEED
        if self.rect.y < player_pos[1]:
            self.rect.y += self.MOVE_CHASE_SPEED
        elif self.rect.y > player_pos[1]:
            self.rect.y -= self.MOVE_CHASE_SPEED

    def avoid_player(self, player_pos):
        # Move away from the player
        if self.rect.x > player_pos[0]:
            self.rect.x += self.MOVE_AVOID_SPEED
        elif self.rect.x < player_pos[0]:
            self.rect.x -= self.MOVE_AVOID_SPEED
        if self.rect.y < player_pos[1]:
            self.rect.y -= self.MOVE_AVOID_SPEED
        elif self.rect.y > player_pos[1]:
            self.rect.y += self.MOVE_AVOID_SPEED

    def reinitialize_for_next_spawn(self):
        self.rect.topleft = (random.randrange(100, SCREEN_WIDTH-100), self.Y_POSITION_SPAWN)
        self.initial_descent_complete = False
    def collide_with_bright_blue_fish(self):
        self.reinitialize_for_next_spawn()
    def collide_with_player(self):
        self.reinitialize_for_next_spawn()
    def get_score_value(self):
        return self.PLAYER_SCORE_VALUE
    def remove_sprite(self):
        self.kill()