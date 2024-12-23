import asyncio
import pygame
import os
import random
import sys
import platform

from pygame.constants import RLEACCEL
import datetime
from utils import IMAGES, SOUNDS, FONTS, load_sound, load_image, load_font, SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TOP_UI_LAYER_HEIGHT
from shark import Shark
from red_fish import RedFish
from green_fish import GreenFish
from silver_fish import SilverFish
from snake import Snake
from bright_blue_fish import BrightBlueFish
from bright_blue_fish import FishManager
from bright_blue_fish import FishManager2
from bright_blue_fish import FishManager3
from bright_blue_fish import FishManager4
from bright_blue_fish import FishManager5

from rainbow_fish import RainbowFish
from seahorse import Seahorse
from jellyfish import Jellyfish
from star_powerup import StarPowerup
from player import Player
import math



# Initialize Pygame
pygame.init()
is_mobile = platform.system() == "Linux" and "ANDROID_ARGUMENT" in os.environ

# Set default screen dimensions for landscape mode
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 600

# Detect the actual screen size and adjust for landscape if on mobile
if is_mobile:
    # Use the actual screen dimensions for fullscreen
    real_width = pygame.display.Info().current_w
    real_height = pygame.display.Info().current_h

    # Force landscape: if in portrait, swap width and height
    if real_height > real_width:
        SCREEN_WIDTH, SCREEN_HEIGHT = real_height, real_width
    else:
        SCREEN_WIDTH, SCREEN_HEIGHT = real_width, real_height

    # Set fullscreen on mobile
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

else:
    # Default window mode for PC
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bermuda Frenzy")
gameicon = pygame.image.load("sprites/red_fish.png")
pygame.display.set_icon(gameicon)
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
DEBUG = False
ZOOM_FACTOR = 1.5 # Recommended to be 1.5
print("Current working directory:", os.getcwd())


def load_all_assets():
    load_image("sprites/coral_reef.png", "spr_wall", True)
    load_image("sprites/player_left.png", "player_left", True)
    load_image("sprites/player_down_left.png", "player_down_left", True)
    load_image("sprites/player_down.png", "player_down", True)
    load_image("sprites/player_down_right.png", "player_down_right", True)
    load_image("sprites/player_right.png", "player_right", True)
    load_image("sprites/player_up_right.png", "player_up_right", True)
    load_image("sprites/player_up.png", "player_up", True)
    load_image("sprites/player_up_left.png", "player_up_left", True)
    # Load heart image
    load_image("sprites/heart.png", "heart", True)

    load_image("sprites/player_left_munch.png", "player_left_munch", True)
    load_image("sprites/player_down_left_munch.png", "player_down_left_munch", True)
    load_image("sprites/player_down_munch.png", "player_down_munch", True)
    load_image("sprites/player_down_right_munch.png", "player_down_right_munch", True)
    load_image("sprites/player_right_munch.png", "player_right_munch", True)
    load_image("sprites/player_up_right_munch.png", "player_up_right_munch", True)
    load_image("sprites/player_up_munch.png", "player_up_munch", True)
    load_image("sprites/player_up_left_munch.png", "player_up_left_munch", True)
    
    load_image("sprites/player_left_face.png", "player_left_face", True)
    load_image("sprites/player_down_left_face.png", "player_down_left_face", True)
    load_image("sprites/player_down_face.png", "player_down_face", True)
    load_image("sprites/player_down_right_face.png", "player_down_right_face", True)
    load_image("sprites/player_right_face.png", "player_right_face", True)
    load_image("sprites/player_up_right_face.png", "player_up_right_face", True)
    load_image("sprites/player_up_face.png", "player_up_face", True)
    load_image("sprites/player_up_left_face.png", "player_up_left_face", True)
    
    load_image("sprites/player_left_gold.png", "player_left_gold", True)
    load_image("sprites/player_down_left_gold.png", "player_down_left_gold", True)
    load_image("sprites/player_down_gold.png", "player_down_gold", True)
    load_image("sprites/player_down_right_gold.png", "player_down_right_gold", True)
    load_image("sprites/player_right_gold.png", "player_right_gold", True)
    load_image("sprites/player_up_right_gold.png", "player_up_right_gold", True)
    load_image("sprites/player_up_gold.png", "player_up_gold", True)
    load_image("sprites/player_up_left_gold.png", "player_up_left_gold", True)
    
    load_image("sprites/red_fish.png", "spr_red_fish", True)
    load_image("sprites/green_fish.png", "spr_green_fish_right", True)
    IMAGES["spr_green_fish_left"] = pygame.transform.flip(IMAGES["spr_green_fish_right"], 1, 0)
    
    load_image("sprites/big_green_fish_left.png", "spr_big_green_fish_left", True)
    load_image("sprites/big_green_fish_left_face.png", "spr_big_green_fish_left_face", True)
    load_image("sprites/big_green_fish_right.png", "spr_big_green_fish_right", True)
    load_image("sprites/big_green_fish_right_face.png", "spr_big_green_fish_right_face", True)
    load_image("sprites/big_green_fish_turning.png", "spr_big_green_fish_turning", True)

    
    load_image("sprites/silver_fish.png", "spr_silver_fish", True)
    load_image("sprites/snake_1.png", "spr_snake_1", True)
    load_image("sprites/snake_2.png", "spr_snake_2", True)
    load_image("sprites/snake_3.png", "spr_snake_3", True)
    load_image("sprites/snake_4.png", "spr_snake_4", True)
    load_image("sprites/seahorse.png", "spr_seahorse", True)
    load_image("sprites/jellyfish_1.png", "spr_jellyfish_1", True)
    load_image("sprites/jellyfish_2.png", "spr_jellyfish_2", True)
    load_image("sprites/jellyfish_3.png", "spr_jellyfish_3", True)
    load_image("sprites/jellyfish_4.png", "spr_jellyfish_4", True)
    load_image("sprites/jellyfish_5.png", "spr_jellyfish_5", True)
    load_image("sprites/jellyfish_6.png", "spr_jellyfish_6", True)
    load_image("sprites/jellyfish_7.png", "spr_jellyfish_7", True)
    load_image("sprites/shark_left.png", "spr_shark_left", True)
    load_image("sprites/shark_face_left.png", "spr_shark_face_left", True)
    load_image("sprites/shark_face_right.png", "spr_shark_face_right", True)
    load_image("sprites/shark_right.png", "spr_shark_right", True)
    load_image("sprites/shark_turning.png", "spr_shark_turning", True)
    
    # Load and scale the images directly
    load_image("sprites/bright_blue_fish_right.png", "spr_bright_blue_fish_right", True)
    IMAGES["spr_bright_blue_fish_right"] = pygame.transform.smoothscale(IMAGES["spr_bright_blue_fish_right"], (300, 200))

    load_image("sprites/bright_blue_fish_right_face.png", "spr_bright_blue_fish_right_face", True)
    IMAGES["spr_bright_blue_fish_right_face"] = pygame.transform.smoothscale(IMAGES["spr_bright_blue_fish_right_face"], (300, 200))

    load_image("sprites/bright_blue_fish_left.png", "spr_bright_blue_fish_left", True)
    IMAGES["spr_bright_blue_fish_left"] = pygame.transform.smoothscale(IMAGES["spr_bright_blue_fish_left"], (300, 200))

    load_image("sprites/bright_blue_fish_left_face.png", "spr_bright_blue_fish_left_face", True)
    IMAGES["spr_bright_blue_fish_left_face"] = pygame.transform.smoothscale(IMAGES["spr_bright_blue_fish_left_face"], (300, 200))

    load_image("sprites/starfish_1.png", "spr_star_1", True)
    load_image("sprites/starfish_2.png", "spr_star_2", True)
    load_image("sprites/starfish_3.png", "spr_star_3", True)
    load_image("sprites/arrow_warning_red.png", "arrow_warning_red_top", True)
    load_image("sprites/arrow_warning_silver.png", "arrow_warning_silver_top", True)
    load_image("sprites/arrow_warning_blue_left.png", "arrow_warning_blue_left", True)
    load_image("sprites/arrow_warning_blue_right.png", "arrow_warning_blue_right", True)

    load_image("sprites/seaweed_middle.png", "spr_seaweed", True)
    load_image("sprites/seaweed_left.png", "spr_seaweed_left", True)
    load_image("sprites/seaweed_right.png", "spr_seaweed_right", True)
    
    load_image("sprites/rainbow_fish_left.png", "spr_rainbow_fish_left", True)
    load_image("sprites/rainbow_fish_left_face.png", "spr_rainbow_fish_left_face", True)
    load_image("sprites/rainbow_fish_turning.png", "spr_rainbow_fish_turning", True)
    load_image("sprites/rainbow_fish_right.png", "spr_rainbow_fish_right", True)
    load_image("sprites/rainbow_fish_right_face.png", "spr_rainbow_fish_right_face", True)

    # arrow keys
    load_image("sprites/unpressed_arrow_up.png", "spr_unpressed_arrow_up", True, 128)
    load_image("sprites/pressed_arrow_up.png", "spr_pressed_arrow_up", True, 128)
    load_image("sprites/pressed_arrow_up_right.png", "spr_pressed_arrow_up_right", True, 128)
    load_image("sprites/pressed_arrow_right.png", "spr_pressed_arrow_right", True, 128)
    load_image("sprites/pressed_arrow_down_right.png", "spr_pressed_arrow_down_right", True, 128)
    load_image("sprites/pressed_arrow_down.png", "spr_pressed_arrow_down", True, 128)
    load_image("sprites/pressed_arrow_down_left.png", "spr_pressed_arrow_down_left", True, 128)
    load_image("sprites/pressed_arrow_left.png", "spr_pressed_arrow_left", True, 128)
    load_image("sprites/pressed_arrow_up_left.png", "spr_pressed_arrow_up_left", True, 128)
    load_image("sprites/unpressed_arrow_up_right.png", "spr_unpressed_arrow_up_right", True, 128)
    load_image("sprites/unpressed_arrow_right.png", "spr_unpressed_arrow_right", True, 128)
    load_image("sprites/unpressed_arrow_down_right.png", "spr_unpressed_arrow_down_right", True, 128)
    load_image("sprites/unpressed_arrow_down.png", "spr_unpressed_arrow_down", True, 128)
    load_image("sprites/unpressed_arrow_down_left.png", "spr_unpressed_arrow_down_left", True, 128)
    load_image("sprites/unpressed_arrow_left.png", "spr_unpressed_arrow_left", True, 128)
    load_image("sprites/unpressed_arrow_up_left.png", "spr_unpressed_arrow_up_left", True, 128)
    load_image("sprites/neutral_zone.png", "spr_neutral_zone", True, 128)
    
    #font and texts
    load_font("fonts/ocean_font.ttf", 16, False)
    load_font("fonts/ocean_font.ttf", 22)
    load_font("fonts/ocean_font.ttf", 48)
    load_font("fonts/ocean_font.ttf", 76)
    load_font("Arial", 32, is_system_font=True)
    load_font("fonts/ARCADE_N.ttf", 16, False)
    load_font("fonts/ARCADE_N.ttf", 14)

    load_font("fonts/ARCADE_N.ttf", 12)
    load_font("fonts/ARCADE_N.ttf", 22)
    load_font("fonts/ARCADE_N.ttf", 36)

    load_font("fonts/ARCADE_N.ttf", 48)
    load_font("fonts/ARCADE_N.ttf", 76)
    #backgrounds
    game_over_bg=load_image("sprites/game_over.png", "game_over", True)
    success_bg=load_image("sprites/success_screen.png", "game_over", True)
    fail_bg=load_image("sprites/fail_screen.png", "game_over", True)

    load_image("sprites/ground.png", "ground", False)
    load_image("sprites/ground_red.png", "ground_red", False)
    load_image("sprites/ground_blue.png", "ground_blue", False)
    load_image("sprites/ground_black.png", "ground_black", False)


    load_image("sprites/play_background.jpg", "play_background", False)
    #bgwater = pygame.transform.scale(bgwater, (SCREEN_WIDTH, SCREEN_HEIGHT))
    top_ui_layer = load_image("sprites/top_ui_layer.jpg", "top_ui_layer", False)
    IMAGES['top_ui_layer'] = pygame.transform.scale(top_ui_layer, (SCREEN_WIDTH, TOP_UI_LAYER_HEIGHT))
    start_menu_bg = load_image("sprites/start_menu.png", "start_menu_bg", False)
    load_image("sprites/info_screen.png", "info_screen_bg", False)
    load_image("sprites/success_screen.png", "success_screen_bg", False)
    load_image("sprites/fail_screen.png", "fail_screen_bg", False)

    pygame.mouse.set_visible(True)
    load_sound("sounds/snd_eat.wav", "snd_eat")
    SOUNDS["snd_eat"].set_volume(1)
    load_sound("sounds/eat_shark.wav", "snd_eat_shark")
    SOUNDS["snd_eat_shark"].set_volume(.7)
    load_sound("sounds/size_down.wav", "snd_size_down")
    load_sound("sounds/player_die.wav", "snd_player_die")
    SOUNDS["snd_player_die"].set_volume(1)
    load_sound("sounds/powerup_timer.wav", "snd_powerup_timer")
    SOUNDS["snd_powerup_timer"].set_volume(1)
    load_sound("sounds/power_up.wav", "snd_powerup_timer")
    SOUNDS["snd_powerup_timer"].set_volume(1)
    load_sound("sounds/siren.wav", "snd_siren")
    SOUNDS["snd_siren"].set_volume(0.3)
    load_sound("sounds/shark_attack.wav", "snd_shark_attack")
    SOUNDS["snd_shark_attack"].set_volume(1)
    load_sound("sounds/whale_chase.wav", "snd_whale_chase")
    SOUNDS["snd_whale_chase"].set_volume(1)
    load_sound("sounds/shark_incoming.wav", "snd_shark_incoming")
    SOUNDS["snd_shark_incoming"].set_volume(1)
    # Music loop
    pygame.mixer.music.load("sounds/game_music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)




def collide_rect_to_mask(sprite1, sprite2, mask_name='mask'):
    """
    Check for collision between sprite1's rect and a specified mask of sprite2.

    :param sprite1: The first sprite (uses its rect for collision).
    :param sprite2: The second sprite (whose specified mask is used for collision).
    :param mask_name: The name of the mask attribute in sprite2 to use for collision.
    :return: True if there is a collision, False otherwise.
    """
    # First, check if the rectangles collide. If not, there can't be a mask collision.
    if not pygame.sprite.collide_rect(sprite1, sprite2):
        return False

    # Create a temporary mask for sprite1's rect
    mask1 = pygame.mask.Mask((sprite1.rect.width, sprite1.rect.height))
    mask1.fill()  # Fill the mask (all pixels set to 1)

    # Get the specified mask from sprite2
    mask2 = getattr(sprite2, mask_name, None)
    if mask2 is None:
        raise ValueError(f"Mask '{mask_name}' not found in sprite2")

    # Get the offset between the two sprites
    offset_x = sprite2.rect.left - sprite1.rect.left
    offset_y = sprite2.rect.top - sprite1.rect.top

    # Use the offset to check if the masks overlap
    return mask1.overlap(mask2, (offset_x, offset_y)) is not None


def collide_mask_to_mask(sprite1, mask1_name, sprite2, mask2_name, use_rect_check=True):
    """
    Check for collision between two masks of two different sprites, with an optional
    rectangle collision check for optimization.

    :param sprite1: The first sprite.
    :param mask1_name: The name of the mask attribute in the first sprite.
    :param sprite2: The second sprite.
    :param mask2_name: The name of the mask attribute in the second sprite.
    :param use_rect_check: Whether to perform an initial rectangle collision check.
    :return: True if there is a collision, False otherwise.
    """
    # Retrieve the actual mask objects from the sprites
    mask1 = getattr(sprite1, mask1_name, None)
    mask2 = getattr(sprite2, mask2_name, None)

    # Ensure both masks are present
    if not mask1 or not mask2:
        return False

    # First, check if the rectangles collide if use_rect_check is True.
    if use_rect_check and not sprite1.rect.colliderect(sprite2.rect):
        return False

    # Calculate the offset between the two sprites
    offset_x = sprite2.rect.left - sprite1.rect.left
    offset_y = sprite2.rect.top - sprite1.rect.top

    # Check if the masks overlap
    return mask1.overlap(mask2, (offset_x, offset_y)) is not None


class Wall(pygame.sprite.Sprite):
    def __init__(self, allsprites):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32))
        self.image.fill((0, 0, 0, 0))  # Black color, can be changed to (0, 0, 0, 0) for invisible
        self.image.set_colorkey((0, 0, 0))  # Make black color transparent
        self.rect = self.image.get_rect()
    def remove_sprite(self):
        self.kill()

class Seaweed(pygame.sprite.Sprite):
    def __init__(self, allsprites, x_pos, y_pos):
        """
        Animated seaweed
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = IMAGES["spr_seaweed"]
        self.rect = self.image.get_rect()
        self.rect.topleft = x_pos, y_pos
        allsprites.add(self)
        self.seaweed_animate_timer = random.randint(0, 30)
    def update(self):
        self.seaweed_animate_timer += 1
        seaweed_images = [IMAGES["spr_seaweed"], IMAGES["spr_seaweed_left"], IMAGES["spr_seaweed_right"]]
        if self.seaweed_animate_timer > 15 and self.seaweed_animate_timer < 30:
            self.image = seaweed_images[1]
        if self.seaweed_animate_timer >= 30:
            self.image = seaweed_images[2]
        if self.seaweed_animate_timer > 45:
            self.seaweed_animate_timer = 0
            self.image = seaweed_images[0]
    def remove_sprite(self):
        self.kill()

class ArrowWarning(pygame.sprite.Sprite):
    def __init__(self, arrow_warning_sprites, arrow_type, target_sprite, side='top'):
        pygame.sprite.Sprite.__init__(self)
        self.arrow_type = arrow_type
        self.image = IMAGES[f"arrow_warning_{arrow_type}_{side}"]  # e.g., "arrow_warning_red"
        self.rect = self.image.get_rect()
        self.target_sprite = target_sprite
        self.side = side

        # Adjust the position based on the side
        if side == 'top':
            self.rect.y = 40  # Fixed Y position for top
            self.rect.x = self.target_sprite.rect.left
        elif side == 'left':
            self.rect.x = SCREEN_WIDTH-100
            self.rect.y = self.target_sprite.rect.centery
        elif side == 'right':
            self.rect.x = 50
            self.rect.y = self.target_sprite.rect.centery

        arrow_warning_sprites.add(self)
        self.visible = False

    def update(self):
        if self.side == 'top':
            self.rect.x = self.target_sprite.rect.left
        elif self.side == 'left':
            self.rect.y = self.target_sprite.rect.centery
        elif self.side == 'right':
            self.rect.y = self.target_sprite.rect.centery
        
class GameState:
    START_SCREEN = 0
    PLAY_SCREEN = 1
    GAME_OVER_SCREEN = 2
    INFO_SCREEN = 3
    FAIL_SCREEN = 4  
    SUCCESS_SCREEN = 5 
    SCORE_BLIT_TICKS_TO_DISAPPEAR = 30
    TIMER_UNTIL_GAME_OVER_SCREEN = 100
    
    def __init__(self, images, start_screen_bg=None, info_screen_bg=None, joystick=None):
        self.allsprites = pygame.sprite.Group()
        self.arrow_warning_sprites = pygame.sprite.Group()
        self.score = 0
        self.score_blit = 0
        self.key_states = {
            pygame.K_UP: False,
            pygame.K_LEFT: False,
            pygame.K_DOWN: False,
            pygame.K_RIGHT: False
        }
        self.current_state = GameState.START_SCREEN
        self.one_powerup_sound = 0
        self.score_disappear_timer = 0
        self.initialize_entities()
        self.start_screen_bg = start_screen_bg
        self.info_screen_bg = info_screen_bg
        self.is_paused = False
        self.joystick = joystick
        self.dead_fish_position = ()
        self.last_bbf_activation_score = 0  # Initialize last activation score for Bright Blue Fish
        self.game_over_timer = 0
        self.game_over_type = "normal"  # Default to "normal" game over type

        # Define button rectangles
        self.start_button_rect = pygame.Rect(400, 305, 200, 125)
        self.touch_position = None  # Position where the user touches the screen
        self.joystick_visible = False  # Whether the joystick is currently visible
        self.info_button_play_rect = pygame.Rect(SCREEN_WIDTH - 80, 3, 75, TOP_UI_LAYER_HEIGHT-5)  # Adjust position and size as needed
        self.shark_attack_played = False
     
    def initialize_entities(self):
        # Initialize all your entities here
        self.player = Player(self.allsprites, IMAGES)
        self.walls = []
        self.seaweeds = []
        for x_top in range(31):
            self.wall = Wall(self.allsprites)
            self.wall.rect.topleft = (x_top*32, 0) #top walls
            self.walls.append(self.wall)
        for x_bottom in range(32, SCREEN_WIDTH-32, 32):
            self.wall = Wall(self.allsprites)
            self.wall.rect.topleft = (x_bottom, SCREEN_HEIGHT-32) #bottom walls
            self.walls.append(self.wall)
        for y_left in range(0, SCREEN_HEIGHT-32, 32):
            self.wall = Wall(self.allsprites)
            self.wall.rect.topleft = (0, y_left) #left walls
            self.walls.append(self.wall)
        for y_right in range(0, SCREEN_HEIGHT-32, 32):
            self.wall = Wall(self.allsprites)
            self.wall.rect.topleft = (SCREEN_WIDTH-32, y_right) #right walls
            self.walls.append(self.wall)
        for x_pos in range(200, SCREEN_WIDTH-165, 60):
            self.seaweed = Seaweed(self.allsprites, x_pos, SCREEN_HEIGHT-60)
            self.seaweeds.append(self.seaweed)
        self.red_fishes = [RedFish(self.allsprites, IMAGES) for i in range(6)]
        self.green_fishes = [GreenFish(self.allsprites, IMAGES) for i in range(3)]
        self.silver_fish = SilverFish(self.allsprites, IMAGES)
        self.snake = Snake(self.allsprites, IMAGES)
        self.seahorse = Seahorse(self.allsprites, IMAGES)
        self.jellyfishes = [Jellyfish(self.allsprites, IMAGES) for i in range(len(Jellyfish.JELLYFISHES_SCORE_TO_SPAWN))]
        self.sharks = []
        self.silver_arrow_warnings = []
        for s in range(len(Shark.SHARKS_SCORES_TO_SPAWN)):
            self.sharks.append(Shark(self.allsprites, IMAGES))
            self.silver_arrow_warnings.append(ArrowWarning(self.arrow_warning_sprites, "silver", self.sharks[s]))
        self.star = StarPowerup(self.allsprites, IMAGES)
        self.rainbow_fish = RainbowFish(self.allsprites, IMAGES)
        self.red_arrow_warning = ArrowWarning(self.arrow_warning_sprites, "red", self.rainbow_fish)
        self.bright_blue_fish = BrightBlueFish(self.allsprites, IMAGES)
        self.blue_arrow_warning_left = ArrowWarning(self.arrow_warning_sprites, "blue", self.bright_blue_fish, "left")
        self.blue_arrow_warning_right = ArrowWarning(self.arrow_warning_sprites, "blue", self.bright_blue_fish, "right")
        self.whales = []
        self.whales2 = []
        self.whales3 = []

        self.fish_manager = FishManager(self.allsprites, IMAGES)
        self.fish_manager2 = FishManager2(self.allsprites, IMAGES)
        self.fish_manager3 = FishManager3(self.allsprites, IMAGES)
        self.fish_manager4 = FishManager4(self.allsprites, IMAGES)
        self.fish_manager5 = FishManager5(self.allsprites, IMAGES)


        for s in range(3):
            self.whales.append(BrightBlueFish(self.allsprites, IMAGES))
    def activate_whale_barrage(self): 
        for whale in self.whales:
            whale.activate_fish()
            print("Whale activated:", whale)  # Debug statement
            whale.update()


    def reset_game(self, images):
        self.allsprites.empty()
        self.arrow_warning_sprites.empty()
        self.current_state = GameState.PLAY_SCREEN
        self.score = 0
        self.initialize_entities()
        self.player.last_pressed = 0
        self.key_states = {
            pygame.K_UP: False,
            pygame.K_LEFT: False,
            pygame.K_DOWN: False,
            pygame.K_RIGHT: False
        }
        self.last_bbf_activation_score = 0
        self.game_over_timer = 0
        self.score_over_200 = False
        self.red_ground_start_time = None
        self.shark_attack_played = False
        self.shark_attack_timer_done = False

        self.score_over_300 = False
        self.blue_ground_start_time = None
        self.whale_chase_played = False
        self.whale_chase_timer_done = False

        self.score_over_400 = False
        self.black_ground_start_time = None
        self.final_music_played = False
        self.final_challenge_timer_done = False
    
    def change_state(self, new_state):
        self.current_state = new_state


    def activate_game_objects(self, zoomed_surface):
        # Rainbow Fish activation logic
        if self.rainbow_fish.rainbow_timer >= RainbowFish.NUM_OF_TICKS_FOR_ENTRANCE:
            self.rainbow_fish.is_active = True
        if self.rainbow_fish.is_active and not self.rainbow_fish.initial_descent_complete:
            if self.red_arrow_warning.visible == False:
                # Only play the sound right before the arrow shows up
                SOUNDS["snd_shark_incoming"].play()
            self.red_arrow_warning.visible = True
        else:
            self.red_arrow_warning.visible = False
        # Sharks
        for s in range(len(Shark.SHARKS_SCORES_TO_SPAWN)):
            if self.score >= Shark.SHARKS_SCORES_TO_SPAWN[s]:
                self.sharks[s].activate = True
                if self.sharks[s].activate and not self.sharks[s].initial_descent_complete:
                    if self.silver_arrow_warnings[s].visible == False and self.sharks[s].mini_shark == False:
                        SOUNDS["snd_shark_incoming"].play()
                    self.silver_arrow_warnings[s].visible = True
                else:
                    self.silver_arrow_warnings[s].visible = False
        # Bright Blue Fish
        if self.bright_blue_fish.activate and not self.bright_blue_fish.lateral_entry_complete:
            SOUNDS["snd_siren"].play()
            if self.bright_blue_fish.direction == BrightBlueFish.DIR_RIGHT:
                # Position the blue arrow on the left side of the screen
                self.blue_arrow_warning_right.visible = True
            elif self.bright_blue_fish.direction == BrightBlueFish.DIR_LEFT:
                # Position the blue arrow on the right side of the screen
                self.blue_arrow_warning_left.visible = True
        else:
            self.blue_arrow_warning_right.visible = False
            self.blue_arrow_warning_left.visible = False
        # Jellyfish
        for j in range(len(Jellyfish.JELLYFISHES_SCORE_TO_SPAWN)):
            if self.score >= Jellyfish.JELLYFISHES_SCORE_TO_SPAWN[j]:
                self.jellyfishes[j].activate = True
                
    def player_eat_prey_collision(self, prey, snd="snd_eat"):
        self.player.collide_with_prey()
        SOUNDS[snd].play()
        self.dead_fish_position = prey.rect.topleft
        fish_score = prey.get_score_value()
        self.score += fish_score
        self.score_blit = fish_score
        if self.player.size_score >= self.player.MAX_SIZE_SCORE:
            self.player.size_score = self.player.MAX_SIZE_SCORE
        else:
            self.player.size_score += fish_score
        prey.collide_with_player()
        
    def predator_eat_player_collision(self, enemy_object):
    # Check if the player collides with the enemy (predator)
        if pygame.sprite.collide_rect(self.player, enemy_object):
            if self.player.lives > 0:
                self.player.lives -= 1  # Reduce lives on collision
                self.player.reset_position()  # Reset the player's position after losing a life
                print(f"Player hit by {enemy_object.__class__.__name__}. Lives left: {self.player.lives}")
            else:
                self.player.game_over = True  # End the game if no lives are left
                print("Game Over!")

    # Drawing the lives based on player lives
    def draw_lives(self, screen):
        heart_image = IMAGES['heart']  # Assuming IMAGES is your image dictionary
        num_hearts = self.player.lives
        heart_spacing = 5  # Space between hearts

        # Resize the heart image to 75% of its original size
        heart_size = (int(heart_image.get_width() * 0.75), int(heart_image.get_height() * 0.75))
        heart_image = pygame.transform.scale(heart_image, heart_size)

        # Position the hearts at the left side of the screen
        start_x = 15  # Starting X position from the left edge
        start_y = 40  # Y position just above the bottom edge, aligned with the pause button

        for i in range(num_hearts):
            x_position = start_x + i * (heart_image.get_width() + heart_spacing)
            screen.blit(heart_image, (x_position, start_y))




        

    def handle_collisions(self):
        ##################
        # COLLISIONS
        ##################
        for red_fish in self.red_fishes:
            if self.player.star_power == self.player.INVINCIBLE_POWERUP:
                if collide_rect_to_mask(red_fish, self.player, "body_mask"):
                    self.player_eat_prey_collision(red_fish)
            else:
                if collide_rect_to_mask(red_fish, self.player, "face_mask"):
                    self.player_eat_prey_collision(red_fish)
            for green_fish in self.green_fishes:
                if red_fish.rect.colliderect(green_fish):
                    green_fish.collision_with_red_fish()
                    if green_fish.is_big == False:
                        red_fish.collide_with_green_fish()
            if pygame.sprite.collide_mask(red_fish, self.bright_blue_fish):
                red_fish.collide_with_bright_blue_fish()
            for wall in self.walls:
                if red_fish.rect.colliderect(wall.rect):
                    red_fish.collision_with_wall(wall.rect)
        for green_fish in self.green_fishes:
            if(green_fish.is_big == False or 
               self.player.size_score >= Player.PLAYER_SCORE_BIGGER_THAN_BIG_GREEN_FISH or 
               self.player.star_power == Player.INVINCIBLE_POWERUP):
                if self.player.star_power == self.player.INVINCIBLE_POWERUP:
                    if collide_mask_to_mask(green_fish, "body_mask", self.player, "body_mask", False):
                        self.player_eat_prey_collision(green_fish)
                else:
                    if collide_mask_to_mask(green_fish, "body_mask", self.player, "face_mask", False):
                        # Green fish is small or player is bigger than green fish or player has star power
                        self.player_eat_prey_collision(green_fish)
            else: 
                if collide_mask_to_mask(green_fish, "face_mask", self.player, "body_mask", False):
                    if green_fish.is_big:
                        # Green fish is bigger than player
                        self.predator_eat_player_collision(green_fish)
            if pygame.sprite.collide_mask(green_fish, self.bright_blue_fish):
                green_fish.reset_position()
            for wall in self.walls:
                if green_fish.rect.colliderect(wall.rect):
                    green_fish.collision_with_wall(wall.rect)
        if self.player.star_power == self.player.INVINCIBLE_POWERUP:
            if collide_rect_to_mask(self.silver_fish, self.player, "body_mask"):
                self.player_eat_prey_collision(self.silver_fish)
        else:
            if collide_rect_to_mask(self.silver_fish, self.player, "face_mask"):
                self.player_eat_prey_collision(self.silver_fish)
        if collide_mask_to_mask(self.bright_blue_fish, "mask", self.player, "body_mask"):
            if self.player.star_power != Player.INVINCIBLE_POWERUP:
                self.predator_eat_player_collision(self.bright_blue_fish)
        if pygame.sprite.collide_mask(self.rainbow_fish, self.player):
            # Player eats rainbow_fish only when appears bigger (arbitrary)
            if (self.rainbow_fish.size_score <= self.player.size_score or 
                self.player.star_power == self.player.INVINCIBLE_POWERUP):
                self.player_eat_prey_collision(self.rainbow_fish)
            else:
                if self.player.star_power != Player.INVINCIBLE_POWERUP:
                    self.predator_eat_player_collision(self.rainbow_fish)
        for shark in self.sharks:
            if self.player.star_power == Player.SHARK_SHRINKER_POWERUP:
                shark.mini_shark = True
                if collide_mask_to_mask(self.player, "face_mask", shark, "mask", False):
                    self.player_eat_prey_collision(shark, "snd_eat_shark")
            elif self.player.star_power == Player.INVINCIBLE_POWERUP:
                pass
            else:
                shark.mini_shark = False
                if collide_mask_to_mask(self.player, "body_mask", shark, "mask", False):
                    self.predator_eat_player_collision(shark)
            if pygame.sprite.collide_mask(shark, self.bright_blue_fish):
                shark.collide_with_bright_blue_fish()
                SOUNDS["snd_eat"].play()
            for wall in self.walls:
                if shark.rect.colliderect(wall.rect):
                    shark.collision_with_wall(wall.rect)
        if pygame.sprite.collide_mask(self.rainbow_fish, self.bright_blue_fish):
            SOUNDS["snd_eat"].play()
            self.rainbow_fish.collide_with_bright_blue_fish()
        if pygame.sprite.collide_mask(self.snake, self.player):
            self.snake.collide_with_player()
            if self.player.star_power != Player.INVINCIBLE_POWERUP:
                self.player.collide_with_snake()
                SOUNDS["snd_size_down"].play()
            else:
                SOUNDS["snd_eat"].play()
        if pygame.sprite.collide_mask(self.silver_fish, self.bright_blue_fish):
            SOUNDS["snd_eat"].play()
            self.silver_fish.collide_with_bright_blue_fish()
        if pygame.sprite.collide_mask(self.snake, self.bright_blue_fish):
            self.snake.collide_with_bright_blue_fish()
        if pygame.sprite.collide_mask(self.seahorse, self.player):
            self.player.collide_with_seahorse()
            self.seahorse.collide_with_player()
            SOUNDS["snd_eat"].play()
            self.one_powerup_sound += 1
            if self.one_powerup_sound > 1:
                SOUNDS["snd_powerup_timer"].stop()
            for i in range(0, len(SOUNDS)):
                sounds_list = list(SOUNDS.keys()) #returns list of keys in sounds
                SOUNDS[sounds_list[i]].stop() #stops all sounds
            SOUNDS["snd_powerup_timer"].play()
        for jellyfish in self.jellyfishes:
            if pygame.sprite.collide_mask(jellyfish, self.player):
                jellyfish.collide_with_player()
                if self.player.star_power == Player.INVINCIBLE_POWERUP:
                    SOUNDS["snd_eat"].play()
                else:
                    self.player.collide_with_jellyfish()
                    SOUNDS["snd_size_down"].play()
                    self.one_powerup_sound += 1
                    SOUNDS["snd_powerup_timer"].play()

                    if self.one_powerup_sound > 1:
                        SOUNDS["snd_powerup_timer"].stop()
                    
                    SOUNDS["snd_powerup_timer"].play()
            if pygame.sprite.collide_mask(jellyfish, self.bright_blue_fish):
                jellyfish.collide_with_bright_blue_fish()
                SOUNDS["snd_eat"].play()
        if self.player.rect.colliderect(self.star):
            self.player.collide_with_star()
            self.star.collide_with_player()
            SOUNDS["snd_eat"].play()
            SOUNDS["snd_powerup_timer"].play()
            self.one_powerup_sound += 1
            if self.one_powerup_sound > 1:
                SOUNDS["snd_powerup_timer"].stop()
            
            

                
    def handle_input(self, pause_button_rect):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
            if event.type == pygame.KEYDOWN:
                if event.key in self.key_states:
                    self.key_states[event.key] = True
    
            if event.type == pygame.KEYUP:
                if event.key in self.key_states:
                    self.key_states[event.key] = False
                    
            if self.current_state == GameState.GAME_OVER_SCREEN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.reset_game(IMAGES)
            elif self.current_state == GameState.START_SCREEN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                     self.change_state(GameState.INFO_SCREEN)
            elif self.current_state == GameState.INFO_SCREEN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Clicking anywhere on the Info screen returns to the Start screen
                    self.change_state(GameState.PLAY_SCREEN)
            elif self.current_state == GameState.PLAY_SCREEN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pause_button_rect.collidepoint(event.pos):
                        self.is_paused = not self.is_paused
                    elif self.info_button_play_rect.collidepoint(event.pos):
                        self.is_paused = True
                        self.change_state(GameState.INFO_SCREEN)
                    else:
                        # Call the joystick's handle_click method
                        self.joystick.handle_click(event.pos)
        
                if event.type == pygame.MOUSEMOTION:
                    if self.joystick.mouse_is_pressed:
                        new_direction = self.joystick.handle_mouse_move(event.pos)
                        if new_direction:
                            if new_direction == "neutral":
                                for key in self.key_states:
                                    self.key_states[key] = False
                            else:
                                for key in self.key_states:
                                    self.key_states[key] = False
                                for key in self.map_direction_to_key(new_direction):
                                    self.key_states[key] = True

                if event.type == pygame.MOUSEBUTTONUP:
                    # Call the joystick's handle_mouse_up method
                    self.joystick.handle_mouse_up()
                        
    def map_direction_to_key(self, direction):
        mapping = {
            "up": [pygame.K_UP],
            "up_right": [pygame.K_UP, pygame.K_RIGHT],
            "right": [pygame.K_RIGHT],
            "down_right": [pygame.K_DOWN, pygame.K_RIGHT],
            "down": [pygame.K_DOWN],
            "down_left": [pygame.K_DOWN, pygame.K_LEFT],
            "left": [pygame.K_LEFT],
            "up_left": [pygame.K_UP, pygame.K_LEFT]
        }
        return mapping.get(direction, [])


                    
    def show_start_screen(self, screen):
        # Check if a background image is provided, if not, fill with black
        if self.start_screen_bg:
            screen.blit(self.start_screen_bg, (0, 0))
        else:
            screen.fill((0, 0, 0))

        # Draw the "Click to Start" button with custom font and color
        

    



    def show_info_screen(self, screen):
        if self.info_screen_bg:
            screen.blit(self.info_screen_bg, (0, 0))
        else:
                screen.fill((0, 0, 0))
    def show_game_over_screen(self, screen):
        # Choose background based on game_over_type
        if self.game_over_type == "success":
            game_over_bg = load_image("sprites/success_screen.png", "success_screen", False)
        elif self.game_over_type == "fail":
            game_over_bg = load_image("sprites/fail_screen.png", "fail_screen", False)
        else:
            game_over_bg = load_image("sprites/game_over.png", "game_over", False)
        
        # Scale and display background
        game_over_bg = pygame.transform.scale(game_over_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(game_over_bg, (0, 0))

        # Set up the font and display the score
        font = FONTS['arcade_n_36']
        points_text = str(self.score)
        position = (SCREEN_WIDTH // 2 + 98, SCREEN_HEIGHT - 140)
        self.render_text_with_outline(screen, font, points_text, color=(255, 255, 255), outline_color=(0, 0, 0), position=position)


    def show_success_screen(self, screen):
    # Load and scale the success background image
        success_bg = load_image("sprites/success_screen.png", "success", False)
        success_bg = pygame.transform.scale(success_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(success_bg, (0, 0))
    def show_fail_screen(self, screen):
    # Load and scale the fail background image
        fail_bg = load_image("sprites/fail_screen.jpg", "fail", False)
        fail_bg = pygame.transform.scale(fail_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(fail_bg, (0, 0))
        font = FONTS['arcade_n_36']
        points_text = str(self.score)
        
        position = (SCREEN_WIDTH // 2 + 75, SCREEN_HEIGHT - 150)

        self.render_text_with_outline(screen, font, points_text, color=(255, 255, 255), outline_color=(0, 0, 0), position=position)


    def render_text_with_outline(self, screen, font, text, color, outline_color, position):
        """Helper function to render text with a black outline."""
        outline_text = font.render(text, True, outline_color)
        outline_rect = outline_text.get_rect(center=position)

        screen.blit(outline_text, outline_rect.move(-2, -2))  
        screen.blit(outline_text, outline_rect.move(2, -2))   
        screen.blit(outline_text, outline_rect.move(-2, 2))   
        screen.blit(outline_text, outline_rect.move(2, 2))    

        main_text = font.render(text, True, color)
        main_rect = main_text.get_rect(center=position)
        screen.blit(main_text, main_rect)




    def update(self, zoomed_surface):
        if self.player.game_over == True:
            # Fades player when predator eats it
            self.game_over_timer += 1
            if self.game_over_timer >= self.TIMER_UNTIL_GAME_OVER_SCREEN:
                self.current_state = self.GAME_OVER_SCREEN
        elif self.current_state == GameState.PLAY_SCREEN and not self.is_paused:
            self.handle_collisions()
            self.activate_game_objects(zoomed_surface)
            # Diagonal Movements
            if self.key_states[pygame.K_UP] and self.key_states[pygame.K_RIGHT]:
                self.player.move_up_right()
            elif self.key_states[pygame.K_UP] and self.key_states[pygame.K_LEFT]:
                self.player.move_up_left()
            elif self.key_states[pygame.K_DOWN] and self.key_states[pygame.K_RIGHT]:
                self.player.move_down_right()
            elif self.key_states[pygame.K_DOWN] and self.key_states[pygame.K_LEFT]:
                self.player.move_down_left()
        
            # Single direction movements
            elif self.key_states[pygame.K_UP]:
                self.player.move_up()
            elif self.key_states[pygame.K_DOWN]:
                self.player.move_down()
            elif self.key_states[pygame.K_LEFT]:
                self.player.move_left()
            elif self.key_states[pygame.K_RIGHT]:
                self.player.move_right()
        
            # Stop movement if no arrow keys are pressed
            if not any(self.key_states.values()):
                self.player.stop_movement()
                
            # Activate Bright Blue Fish every time the score increases by increments
            if self.bright_blue_fish.try_activate(self.score, self.last_bbf_activation_score):
                self.last_bbf_activation_score = self.score


class Joystick:
    def __init__(self, images, screen):
        self.images = images
        self.screen = screen
        self.pressed_direction = None  # To track the currently pressed direction        
        self.neutral_zone_rect = images['spr_neutral_zone'].get_rect(center=(158, SCREEN_HEIGHT - 143))
        # Define the positions and sizes of the arrows
        self.arrows = {
            "up_left": self.images["spr_unpressed_arrow_up_left"].get_rect(topleft=(20, SCREEN_HEIGHT - 280)),
            "up_right": self.images["spr_unpressed_arrow_up_right"].get_rect(topleft=(200, SCREEN_HEIGHT - 280)),
            "down_left": self.images["spr_unpressed_arrow_down_left"].get_rect(topleft=(20, SCREEN_HEIGHT - 100)),
            "down_right": self.images["spr_unpressed_arrow_down_right"].get_rect(topleft=(200, SCREEN_HEIGHT - 100)),
            "up": self.images["spr_unpressed_arrow_up"].get_rect(topleft=(110, SCREEN_HEIGHT - 280)),
            "down": self.images["spr_unpressed_arrow_down"].get_rect(topleft=(110, SCREEN_HEIGHT - 100)),
            "left": self.images["spr_unpressed_arrow_left"].get_rect(topleft=(20, SCREEN_HEIGHT - 190)),
            "right": self.images["spr_unpressed_arrow_right"].get_rect(topleft=(200, SCREEN_HEIGHT - 190))
        }
        
        # Mapping of keyboard keys to joystick directions
        self.key_to_direction = {
             (pygame.K_UP,): "up",
             (pygame.K_DOWN,): "down",
             (pygame.K_LEFT,): "left",
             (pygame.K_RIGHT,): "right",
             (pygame.K_UP, pygame.K_RIGHT): "up_right",
             (pygame.K_UP, pygame.K_LEFT): "up_left",
             (pygame.K_DOWN, pygame.K_RIGHT): "down_right",
             (pygame.K_DOWN, pygame.K_LEFT): "down_left",
         }
        self.mouse_is_pressed = False
        self.activation_distance = 30  # The distance in pixels to activate direction change
        self.center_position = None  # Initialize the center position

        button_width, button_height = 200, 50
        screen_center = self.screen.get_rect().center
        
        # Create start button rectangle centered on the screen
        self.start_button_rect = pygame.Rect(
            screen_center[0] - button_width // 2,  # Center button horizontally
            screen_center[1],                      # Position vertically in the middle
            button_width,
            button_height
        )
    
    def draw(self, key_states, center_position):
        if center_position is None:
            return  # Don't draw if there's no center position

        # Calculate the top-left position for the neutral zone
        neutral_zone_size = self.images['spr_neutral_zone'].get_size()
        neutral_zone_top_left = (center_position[0] - neutral_zone_size[0] // 2,
                                 center_position[1] - neutral_zone_size[1] // 2)

        # Draw neutral zone centered at the mouse click position
        self.screen.blit(self.images['spr_neutral_zone'], neutral_zone_top_left)

        # Calculate and draw arrows around the neutral zone
        arrow_offsets = {
            "up": (0, -neutral_zone_size[1]),
            "down": (0, neutral_zone_size[1]),
            "left": (-neutral_zone_size[0], 0),
            "right": (neutral_zone_size[0], 0),
            # Add other directions (diagonals) here with appropriate offsets
        }
        for direction, offset in arrow_offsets.items():
            arrow_image_key = f"spr_{'pressed' if key_states.get(self.map_direction_to_key(direction), False) else 'unpressed'}_arrow_{direction}"
            arrow_image = self.images[arrow_image_key]
            arrow_rect = arrow_image.get_rect(center=(center_position[0] + offset[0], center_position[1] + offset[1]))
            self.screen.blit(arrow_image, arrow_rect.topleft)
            
    @staticmethod
    def map_direction_to_key(direction):
        direction_to_key = {
            "up": pygame.K_UP,
            "down": pygame.K_DOWN,
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            # Add mappings for other directions (diagonals) here
        }
        return direction_to_key.get(direction, None)


    def blit_arrow(self, direction, is_pressed):
        image_key = "spr_pressed_arrow_" if is_pressed else "spr_unpressed_arrow_"
        image_key += direction
        rect = self.arrows[direction]
        self.screen.blit(self.images[image_key], rect.topleft)

    def handle_click(self, mouse_pos):
        # Check if the click is within any of the joystick areas
        self.center_position = mouse_pos  # Set the center position when mouse is pressed

        if self.neutral_zone_rect.collidepoint(mouse_pos):
            self.pressed_direction = "neutral"
        else:
            for direction, rect in self.arrows.items():
                if rect.collidepoint(mouse_pos):
                    self.pressed_direction = direction
                    break

        self.mouse_is_pressed = True  # Set the flag when the mouse is pressed
        return self.pressed_direction
    
    def handle_mouse_up(self):
        self.center_position = None  # Reset the center position when mouse is released
        # Return the last pressed direction when the mouse button is released
        last_direction = self.pressed_direction
        self.mouse_is_pressed = False  # Reset the flag when the mouse is released
        self.pressed_direction = None  # Reset the pressed direction
        return last_direction
        
    def handle_mouse_move(self, mouse_pos):
        if not self.mouse_is_pressed or self.center_position is None:
            return None

        # Calculate distance and angle from the joystick center
        dx = mouse_pos[0] - self.center_position[0]
        dy = mouse_pos[1] - self.center_position[1]
        distance = math.sqrt(dx**2 + dy**2)
        angle = math.degrees(math.atan2(-dy, dx)) % 360  # Negative dy because screen coordinates are inverted on y-axis

        # Determine the direction based on the angle
        if distance > self.activation_distance:  # Only change direction if the mouse is dragged far enough
            if 45 <= angle < 135:
                return "up"
            elif 135 <= angle < 225:
                return "left"
            elif 225 <= angle < 315:
                return "down"
            else:
                return "right"
        else:
            return "neutral"

def zoom_in_on_player(screen, player, ZOOM_FACTOR):
    # Define the area around the player to zoom in on
    zoom_width, zoom_height = 100, 100  # Adjust size as needed
    zoom_rect = pygame.Rect(
        player.rect.centerx - zoom_width // 2,
        player.rect.centery - zoom_height // 2,
        zoom_width,
        zoom_height
    )

    # Ensure the zoom rectangle doesn't go outside the screen
    zoom_rect.clamp_ip(screen.get_rect())

    # Capture the area around the player
    subsurface = screen.subsurface(zoom_rect)

    # Scale up the captured area
    zoomed_surface = pygame.transform.scale(
        subsurface,
        (zoom_rect.width * ZOOM_FACTOR, zoom_rect.height * ZOOM_FACTOR)
    )

    return zoomed_surface

def draw_mask(surface, mask, x, y, color=(255, 0, 0)):
    # Create a surface from the mask
    if mask:
        mask_surface = mask.to_surface(setcolor=color, unsetcolor=(0, 0, 0, 0))
        surface.blit(mask_surface, (x, y))

# Main game loop
def main():
    # Define Pause and Info Button Properties
    pause_button_size = (75, TOP_UI_LAYER_HEIGHT-5)
    button_color = (173, 216, 230)  # Light Cyan color
    pause_button_position = (SCREEN_WIDTH - 160, 3)

    pause_button_rect = pygame.Rect(pause_button_position, pause_button_size)

    (x_first, y_first) = (0, 0)
    (x_second, y_second) = (0, -SCREEN_HEIGHT)
    load_all_assets()
    
    running = True
    joystick = Joystick(IMAGES, screen)
    game_state_manager = GameState(IMAGES, IMAGES['start_menu_bg'], IMAGES['info_screen_bg'], joystick)
    
    # Ensure the zoomed surface is large enough to handle the maximum offset
    
    zoomed_surface = pygame.Surface((SCREEN_WIDTH // ZOOM_FACTOR, SCREEN_HEIGHT // ZOOM_FACTOR), pygame.SRCALPHA)

    world_width = SCREEN_WIDTH
    world_height = SCREEN_HEIGHT

    while running:
        clock.tick(FPS)
        game_state_manager.handle_input(pause_button_rect)
        # Clear the screen (fill with a background color or image)
        screen.fill((0, 0, 0))
        if game_state_manager.current_state == GameState.INFO_SCREEN:
            game_state_manager.show_info_screen(screen)
        elif game_state_manager.current_state == GameState.START_SCREEN:
            game_state_manager.show_start_screen(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
        elif game_state_manager.current_state == GameState.GAME_OVER_SCREEN:
            game_state_manager.show_game_over_screen(screen)
        
        elif game_state_manager.current_state == GameState.PLAY_SCREEN:


            y_first += 10
            y_second += 10

            if y_first >= SCREEN_HEIGHT:
                y_first = -SCREEN_HEIGHT
            if y_second >= SCREEN_HEIGHT:
                y_second = -SCREEN_HEIGHT
            
            # Calculate camera position with boundary limits
            camera_x = max(0, min(game_state_manager.player.rect.centerx - SCREEN_WIDTH // (2 * ZOOM_FACTOR),
                              world_width - SCREEN_WIDTH // ZOOM_FACTOR))
            camera_y = max(0, min(game_state_manager.player.rect.centery - SCREEN_HEIGHT // (2 * ZOOM_FACTOR),
                                  world_height - SCREEN_HEIGHT // ZOOM_FACTOR))

            # Clear the zoomed surface
            zoomed_surface.fill((0, 0, 0))
    
            # Draw the background on zoomed_surface
            zoomed_surface.blit(IMAGES['play_background'], (-camera_x, y_first - camera_y))
            zoomed_surface.blit(IMAGES['play_background'], (-camera_x, y_second - camera_y))
        

            if game_state_manager.score >= 100:
                game_state_manager.activate_whale_barrage()
                game_state_manager.snake.set_respawn_timer(Snake.FAST_RESPAWN_TIMER)
                game_state_manager.snake.set_speed(Snake.FAST_SPEED)
                game_state_manager.snake.set_size(Snake.BIGGER_SIZE)
                game_state_manager.snake.rect.y =  SCREEN_HEIGHT - 90

        # Initialization of flags for 200-point effect
           # Initialization for 200-point and 400-point effects
            if not hasattr(game_state_manager, 'score_over_200'):
                game_state_manager.score_over_200 = False
            if not hasattr(game_state_manager, 'red_ground_start_time'):
                game_state_manager.red_ground_start_time = None
            if not hasattr(game_state_manager, 'shark_attack_played'):
                game_state_manager.shark_attack_played = False
            if not hasattr(game_state_manager, 'shark_attack_timer_done'):
                game_state_manager.shark_attack_timer_done = False

            if not hasattr(game_state_manager, 'score_over_300'):
                game_state_manager.score_over_300 = False
            if not hasattr(game_state_manager, 'blue_ground_start_time'):
                game_state_manager.blue_ground_start_time = None
            if not hasattr(game_state_manager, 'whale_chase_played'):
                game_state_manager.whale_chase_played = False
            if not hasattr(game_state_manager, 'whale_chase_timer_done'):
                game_state_manager.whale_chase_timer_done = False
            if not hasattr(game_state_manager, 'score_over_400'):
                game_state_manager.score_over_400 = False
            if not hasattr(game_state_manager, 'black_ground_start_time'):
                game_state_manager.black_ground_start_time = None
            if not hasattr(game_state_manager, 'final_music_played'):
                game_state_manager.final_music_played = False
            if not hasattr(game_state_manager, 'final_challenge_timer_done'):
                game_state_manager.final_challenge_timer_done = False
            # Handle the ground and music effects based on score
            if game_state_manager.score < 200:
                # Before 200: Normal game music and ground
                zoomed_surface.blit(IMAGES['ground'], (-camera_x, world_height - 600 - camera_y))
                if game_state_manager.shark_attack_played or game_state_manager.whale_chase_played:
                    print("Resuming normal background music...")
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("sounds/game_music.mp3")
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(-1)

            elif game_state_manager.score >= 200 and not game_state_manager.shark_attack_timer_done:
                # 200 points: Shark music and red ground
                if not game_state_manager.score_over_200:
                    game_state_manager.score_over_200 = True
                    game_state_manager.red_ground_start_time = pygame.time.get_ticks()

                # Draw red ground effect
                zoomed_surface.blit(IMAGES['ground_red'], (-camera_x, world_height - 600 - camera_y))

                # Play shark attack sound once
                if not game_state_manager.shark_attack_played:
                    print("Playing shark attack sound as background music...")
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("sounds/shark_attack.wav")
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(-1)
                    game_state_manager.shark_attack_played = True
                    
                elapsed_time = pygame.time.get_ticks() - game_state_manager.red_ground_start_time
                if elapsed_time >= 20000:
                    game_state_manager.shark_attack_timer_done = True
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("sounds/game_music.mp3")
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(-1)
                    sharks_to_kill = 0
                    for shark in game_state_manager.sharks:  # Assuming `all_sharks` is the group of sharks
                        if sharks_to_kill < 3:
                            shark.remove_sprite()  # Remove the shark from the game
                            sharks_to_kill += 1

            elif game_state_manager.score >= 300 and not game_state_manager.whale_chase_timer_done:
                # 300 points: Whale music and blue ground
                if not game_state_manager.score_over_300:
                    game_state_manager.score_over_300 = True
                    game_state_manager.blue_ground_start_time = pygame.time.get_ticks()

                # Draw blue ground effect
                zoomed_surface.blit(IMAGES['ground_blue'], (-camera_x, world_height - 600 - camera_y))

                # Play whale chase sound once
                if not game_state_manager.whale_chase_played:
                    print("Playing whale chase sound as background music...")
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("sounds/whale_chase.wav")
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(-1)
                    game_state_manager.whale_chase_played = True
                    game_state_manager.fish_manager.update(game_state_manager.score)
                    game_state_manager.fish_manager2.update(game_state_manager.score)
                    game_state_manager.fish_manager3.update(game_state_manager.score)


                # Timer for whale chase effect
                elapsed_time = pygame.time.get_ticks() - game_state_manager.blue_ground_start_time
                if elapsed_time >= 25000:
                    game_state_manager.whale_chase_timer_done = True
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("sounds/game_music.mp3")
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(-1)
            elif game_state_manager.score >= 400 and not game_state_manager.final_challenge_timer_done:
    # 400 points: Black ground and final challenge music
                if not game_state_manager.score_over_400:
                    game_state_manager.score_over_400 = True
                    game_state_manager.black_ground_start_time = pygame.time.get_ticks()

                # Draw black ground effect
                zoomed_surface.blit(IMAGES['ground_black'], (-camera_x, world_height - 600 - camera_y))

                # Play final challenge music once
                if not game_state_manager.final_music_played:
                    print("Playing final challenge music as background music...")
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("sounds/final.wav")
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(-1)
                    game_state_manager.final_music_played = True
                    game_state_manager.fish_manager4.update(game_state_manager.score)
                    game_state_manager.fish_manager5.update(game_state_manager.score)
                    

                # Timer for final challenge effect
                elapsed_time = pygame.time.get_ticks() - game_state_manager.black_ground_start_time
                if elapsed_time >= 60000:
                    game_state_manager.final_challenge_timer_done = True
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("sounds/game_music.mp3")
                    pygame.mixer.music.play(-1)

                    # If score is below 500, set to fail game over screen
                    if game_state_manager.score < 500:
                        game_state_manager.game_over_type = "fail"
                        game_state_manager.current_state = GameState.GAME_OVER_SCREEN
                    if game_state_manager.score >= 500:
                        game_state_manager.game_over_type = "success"
                        game_state_manager.current_state = GameState.GAME_OVER_SCREEN



            else:
                # If no effect is active, draw normal ground
                zoomed_surface.blit(IMAGES['ground'], (-camera_x, world_height - 600 - camera_y))
           
                    


















                
            # Update game state only if the game is not paused
            if not game_state_manager.is_paused:
                # Update RainbowFish with player's current state
                game_state_manager.rainbow_fish.player_size_score = game_state_manager.player.size_score
                game_state_manager.rainbow_fish.player_star_power = game_state_manager.player.star_power == game_state_manager.player.INVINCIBLE_POWERUP
                game_state_manager.rainbow_fish.player_position = game_state_manager.player.rect.center
    
                # Update all sprites
                game_state_manager.allsprites.update()
                game_state_manager.arrow_warning_sprites.update()
                game_state_manager.update(zoomed_surface)
    
                # Decide chase or avoid behavior for the RainbowFish
                if game_state_manager.rainbow_fish.is_active:
                    game_state_manager.rainbow_fish.decide_chase_or_avoid(
                        game_state_manager.player.size_score,
                        game_state_manager.player.star_power == game_state_manager.player.INVINCIBLE_POWERUP,
                        game_state_manager.player.rect.center
                    )
        
            # Adjust sprite positions and draw on zoomed_surface
            for sprite in game_state_manager.allsprites:
                original_position = (sprite.rect.x, sprite.rect.y)
                sprite.rect.x -= camera_x
                sprite.rect.y -= camera_y
                zoomed_surface.blit(sprite.image, sprite.rect)
                sprite.rect.x, sprite.rect.y = original_position
            # Update and draw arrow warning sprites on zoomed_surface
            for arrow_sprite in game_state_manager.arrow_warning_sprites:
                arrow_sprite.update()
                if arrow_sprite.visible:
                    zoomed_surface.blit(arrow_sprite.image, (arrow_sprite.rect.x - camera_x, arrow_sprite.rect.y - camera_y))
            
            
            #%% Debug
            if DEBUG:
                draw_mask(zoomed_surface, game_state_manager.player.body_mask, game_state_manager.player.rect.x - camera_x, game_state_manager.player.rect.y - camera_y, (63, 26, 186))
                draw_mask(zoomed_surface, game_state_manager.player.face_mask, game_state_manager.player.rect.x - camera_x, game_state_manager.player.rect.y - camera_y)
                draw_mask(zoomed_surface, game_state_manager.rainbow_fish.body_mask, game_state_manager.rainbow_fish.rect.x - camera_x, game_state_manager.rainbow_fish.rect.y - camera_y, (0, 128, 0))
                draw_mask(zoomed_surface, game_state_manager.rainbow_fish.face_mask, game_state_manager.rainbow_fish.rect.x - camera_x, game_state_manager.rainbow_fish.rect.y - camera_y)

                # for shark in game_state_manager.sharks:
                #     draw_mask(zoomed_surface, shark.mask, shark.rect.x - camera_x, shark.rect.y - camera_y)
                # draw_mask(zoomed_surface, 
                #           game_state_manager.bright_blue_fish.mask, 
                #           game_state_manager.bright_blue_fish.rect.x - camera_x, 
                #           game_state_manager.bright_blue_fish.rect.y - camera_y)
                # for green_fish in game_state_manager.green_fishes:
                #     draw_mask(zoomed_surface, green_fish.body_mask, green_fish.rect.x - camera_x, green_fish.rect.y - camera_y, (0, 128, 0))
                #     draw_mask(zoomed_surface, green_fish.face_mask, green_fish.rect.x - camera_x, green_fish.rect.y - camera_y)


            # Check if there is a score to blit
            if game_state_manager.score_blit > 0:
                # Calculate the relative position of the score text on the zoomed surface
                relative_x = game_state_manager.dead_fish_position[0] - camera_x
                relative_y = game_state_manager.dead_fish_position[1] - camera_y
            
                # Render the score text
                SCORE_BLIT_TEXT = FONTS['ocean_font_16'].render("+" + str(game_state_manager.score_blit), True, (255, 255, 255))
            
                # Blit the score text at the adjusted position on the zoomed surface
                zoomed_surface.blit(SCORE_BLIT_TEXT, (relative_x, relative_y))
            
                # Increment the disappear timer
                game_state_manager.score_disappear_timer += 1
            
                # Reset the score blit and timer after a certain duration
                if game_state_manager.score_disappear_timer > GameState.SCORE_BLIT_TICKS_TO_DISAPPEAR:
                    game_state_manager.score_blit = 0
                    game_state_manager.score_disappear_timer = 0
    
            # Scale the zoomed surface to fill the entire screen
            scaled_zoomed_area = pygame.transform.scale(zoomed_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))

    
            # Draw the scaled zoomed view to the main screen
            screen.blit(scaled_zoomed_area, (0, 0))
            # Draw joystick and other UI elements on top
            if game_state_manager.joystick_visible:
                joystick.draw(game_state_manager.key_states, game_state_manager.touch_position)
                pygame.draw.circle(screen, (255, 0, 0), game_state_manager.touch_position, 5)  # Draw a small red circle at the center position

            # Menu Design
            screen.blit(IMAGES['top_ui_layer'], (0, 0))
            available_prey_text = FONTS['arcade_n_14'].render("Available Prey:", True, (255, 255, 255))
            text_rect = available_prey_text.get_rect(topleft=(10, TOP_UI_LAYER_HEIGHT/2-10))
            screen.blit(available_prey_text, text_rect)
            
                        
            # Draw Pause Button
            pause_or_resume_text = "Resume" if game_state_manager.is_paused else "Pause"
            pause_text_surface = FONTS['arcade_n_12'].render(pause_or_resume_text, True, (0, 0, 0))
            pause_text_x = pause_button_rect.x + (pause_button_rect.width - pause_text_surface.get_width()) // 2
            pause_text_y = pause_button_rect.y + (pause_button_rect.height - pause_text_surface.get_height()) // 2
            pygame.draw.rect(screen, button_color, pause_button_rect)
            screen.blit(pause_text_surface, (pause_text_x, pause_text_y))
            
            # Draw Info Button (only in play screen)
            info_text_surface = FONTS['arcade_n_12'].render("Info", True, (0, 0, 0))
            info_text_x = game_state_manager.info_button_play_rect.x + (game_state_manager.info_button_play_rect.width - info_text_surface.get_width()) // 2
            info_text_y = game_state_manager.info_button_play_rect.y + (game_state_manager.info_button_play_rect.height - info_text_surface.get_height()) // 2
            pygame.draw.rect(screen, button_color, game_state_manager.info_button_play_rect)
            screen.blit(info_text_surface, (info_text_x, info_text_y))

            
            # Starting position for the first icon
            icon_x = text_rect.right + 10  # 10 is a buffer; adjust as needed
            base_icon_y = TOP_UI_LAYER_HEIGHT/2-15  # Base Y position for icons
        
            # Blit each icon with a buffer space in between
            icon_buffer = 5  # Space between icons
        
            # Standard icons
            standard_icons = ['spr_red_fish', 'spr_green_fish_left', 'spr_silver_fish']
            max_height_standard = max(IMAGES[key].get_height() for key in standard_icons)
            game_state_manager.draw_lives(screen)  # Draw lives here

            for icon_key in standard_icons:
                icon = IMAGES[icon_key]
                # Center align standard icons based on their original size
                icon_y = base_icon_y + (max_height_standard - icon.get_height()) // 2
                screen.blit(icon, (icon_x, icon_y))
                icon_x += icon.get_width() + icon_buffer
        
            # Scaled icons
            scaled_icon_size = (24, 15)  # Adjust the size as needed
            scaled_icons = []
        
            if game_state_manager.rainbow_fish.size_score <= game_state_manager.player.size_score:
                scaled_icons.append(pygame.transform.smoothscale(IMAGES["spr_rainbow_fish_left"], scaled_icon_size))
        
            if game_state_manager.player.size_score >= Player.PLAYER_SCORE_BIGGER_THAN_BIG_GREEN_FISH:
                scaled_icons.append(pygame.transform.smoothscale(IMAGES["spr_big_green_fish_left"], scaled_icon_size))
        
            if game_state_manager.player.star_power == Player.SHARK_SHRINKER_POWERUP:
                scaled_icons.append(pygame.transform.smoothscale(IMAGES["spr_shark_left"], scaled_icon_size))
        
            for icon in scaled_icons:
                # Calculate the vertical offset for the scaled icon
                vertical_offset = (max_height_standard - icon.get_height()) // 2
                icon_y = base_icon_y + vertical_offset
                screen.blit(icon, (icon_x, icon_y))
                icon_x += icon.get_width() + icon_buffer


            # Font On Top of Playing Screen
            score_text = FONTS['arcade_n_16'].render("Score: " + str(game_state_manager.score), 1, (255, 255, 255))
            screen.blit(score_text, ((SCREEN_WIDTH/2)-100, TOP_UI_LAYER_HEIGHT/2-10))
            game_state_manager.player.get_powerup_timer_text(FONTS['arcade_n_12'])
            game_state_manager.player.get_speed_timer_text(FONTS['arcade_n_12'])
            screen_width_percentage = 0.70  # 75% of screen width
            x_position_powerup_timer = SCREEN_WIDTH * screen_width_percentage
            screen.blit(game_state_manager.player.get_powerup_timer_text(FONTS['ocean_font_16']), (x_position_powerup_timer, TOP_UI_LAYER_HEIGHT/2-7))
            screen_width_percentage = 0.56  # 60% of screen width
            x_position_speed_timer = SCREEN_WIDTH * screen_width_percentage
            screen.blit(game_state_manager.player.get_speed_timer_text(FONTS['ocean_font_16']), (x_position_speed_timer, TOP_UI_LAYER_HEIGHT/2-7))
            
            ##################
            # Sound Checks
            ##################
            if game_state_manager.player.star_power == Player.NO_STAR_POWER: # Powerup is over on the player
                game_state_manager.one_powerup_sound -= 1
                SOUNDS["snd_powerup_timer"].stop()
            if game_state_manager.player.speed_time_left < 0:
                game_state_manager.one_powerup_sound -= 1
                SOUNDS["snd_powerup_timer"].stop()

        # Update the display
        pygame.display.update()

    pygame.quit()

# Run the game
main()