import pygame as pg
from camera import Camera
from collision_manager import CollisionManager
from settings import *

class Player(Camera):
    def __init__(self, engine, position=PLAYER_POS, yaw=-90, pitch=0):
        self.engine = engine
        self.collision_manager = CollisionManager(size=PLAYER_SIZE, engine=engine, detection_radius=COLLISION_DETECTION_RADIUS)
        super().__init__(position, yaw, pitch)

    def update(self):
        """Method that updates the player position and camera."""
        
        self.keyboard_control() # Handle keyboard input
        self.mouse_control() # handle mouse input
        super().update() # Update viewing matrices and vectors

    def handle_event(self, event) -> None:
        """Handles mouse clicks."""

        # adding and removing voxels with clicks
        if event.type == pg.MOUSEBUTTONDOWN:
            voxel_handler = self.engine.scene.world.voxel_handler
            if event.button == 1:
                voxel_handler.set_voxel()
            if event.button == 3:
                voxel_handler.switch_mode()

    def mouse_control(self) -> None:
        """Handle mouse motion input."""

        mouse_dx, mouse_dy = pg.mouse.get_rel() # Get mouse motion relative to last frame (difference from this frame coordinates and last frame's)
        if mouse_dx: # If mouse has moved horizontally
            self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy: # If mouse has moved vertically
            self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)

    def keyboard_control(self) -> None:
        """Handle keyboard input."""

        key_state = pg.key.get_pressed() # Get the state of all keyboard keys
        vel = PLAYER_SPEED * self.engine.delta_time # Get the velocity the player should move at (speed * time since last frame) (only taking PLAYER_SPEED would make the player move faster with higher FPS)
        if key_state[pg.K_w]: # Move forward
            desired_position = self.position + self.forward * vel
            if not self.collision_manager.check_collision(desired_position): self.move_forward(vel) # If the player is not colliding with a voxel, move forward
        if key_state[pg.K_s]: # Move back
            desired_position = self.position - self.forward * vel
            if not self.collision_manager.check_collision(desired_position): self.move_back(vel) # If the player is not colliding with a voxel, move back
        if key_state[pg.K_d]: # Move right
            desired_position = self.position + self.right * vel
            if not self.collision_manager.check_collision(desired_position): self.move_right(vel) # If the player is not colliding with a voxel, move right
        if key_state[pg.K_a]: # Move left
            desired_position = self.position - self.right * vel
            if not self.collision_manager.check_collision(desired_position): self.move_left(vel) # If the player is not colliding with a voxel, move left
        if key_state[pg.K_q]: # Move up
            desired_position = self.position - self.up * vel
            if not self.collision_manager.check_collision(desired_position): self.move_up(vel) # If the player is not colliding with a voxel, move up
        if key_state[pg.K_e]: # Move down
            desired_position = self.position + self.up * vel
            if not self.collision_manager.check_collision(desired_position): self.move_down(vel) # If the player is not colliding with a voxel, move down

    def move_left(self, velocity):
        self.position -= self.right * velocity

    def move_right(self, velocity):
        self.position += self.right * velocity

    def move_up(self, velocity):
        self.position += self.up * velocity

    def move_down(self, velocity):
        self.position -= self.up * velocity

    def move_forward(self, velocity):
        self.position += self.forward * velocity

    def move_back(self, velocity):
        self.position -= self.forward * velocity