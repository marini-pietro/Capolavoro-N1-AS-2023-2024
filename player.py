import pygame as pg
from camera import Camera
from collision_manager import CollisionManager
from settings import *

class Player(Camera):
    def __init__(self, engine, position=PLAYER_POS, yaw=-90, pitch=0):
        super().__init__(position, yaw, pitch)
        self.engine = engine
        self.collision_manager = CollisionManager()
        self.width, self.heigth, self.depth = PLAYER_SIZE

    def update(self):
        """Method that updates the player position and camera."""
        
        self.keyboard_control() # Handle keyboard input
        self.mouse_control() # handle mouse input
        self.apply_gravity() # Apply gravity to the player
        super().update() # Update viewing matrices and vectors

    def handle_event(self, event):
        """Handles mouse clicks."""

        # adding and removing voxels with clicks
        if event.type == pg.MOUSEBUTTONDOWN:
            voxel_handler = self.engine.scene.world.voxel_handler
            if event.button == 1:
                voxel_handler.set_voxel()
            if event.button == 3:
                voxel_handler.switch_mode()

    def mouse_control(self):
        """Handle mouse motion input."""

        mouse_dx, mouse_dy = pg.mouse.get_rel() # Get mouse motion relative to last frame (difference from this frame coordinates and last frame's)
        if mouse_dx: # If mouse has moved horizontally
            self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy: # If mouse has moved vertically
            self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)

    def keyboard_control(self):
        """Handle keyboard input for player movement."""

        key_state = pg.key.get_pressed()
        vel = PLAYER_SPEED * self.engine.delta_time
        one_block_above: glm.vec3 = glm.vec3(0, 1, 0)  # Define vector for one block above the player

        if key_state[FORWARD_KEY]:  # Move the player forward
            bound_box = self.get_bound_box(self.position + self.forward * vel)  # Get player bounding box
            collides = False  # Define flag for collision
            blocks_infront_pos: list[glm.ivec3] = [glm.ivec3(self.position + self.forward), glm.ivec3(self.position + self.forward - one_block_above)]  # Define list of blocks in front of the player (assumes that the height of the player is 2)
            for block_pos in blocks_infront_pos:
                voxel_id = self.get_voxel_id(world_pos=block_pos)
                if voxel_id == 0: continue  # If the voxel is air, skip the iteration

                block_infront_bound_box = self.get_voxel_bounds(world_pos=block_pos)
                if self.collision_manager.check_collision(bound_box, block_infront_bound_box):  # Check if player collides with any of the blocks
                    collides = True  # Set collision flag to True
                    break

            if not collides:  # If player does not collide with any of the blocks
                self.move_forward(vel)  # If player does not collide with any of the blocks, move the player forward

        if key_state[BACKWARD_KEY]:  # Move the player backwards
            bound_box = self.get_bound_box(self.position - self.forward * vel)  # Get player bounding box
            collides = False  # Define flag for collision
            blocks_behind_pos: list[glm.ivec3] = [glm.ivec3(self.position - self.forward), glm.ivec3(self.position - self.forward - one_block_above)]  # Define list of blocks behind the player (assumes that the height of the player is 2)
            for block_pos in blocks_behind_pos:
                voxel_id = self.get_voxel_id(world_pos=block_pos)
                if voxel_id == 0:  continue # If the voxel is air, skip the iteration

                block_behind_bound_box = self.get_voxel_bounds(world_pos=block_pos)
                if self.collision_manager.check_collision(bound_box, block_behind_bound_box):  # Check if player collides with any of the blocks
                    collides = True  # Set collision flag to True
                    break  # Break the loop

            if not collides:  # If player does not collide with any of the blocks
                self.move_back(vel)  # If player does not collide with any of the blocks, move the player backwards

        if key_state[RIGHT_KEY]:  # Move the player to the right
            bound_box = self.get_bound_box(self.position + self.right * vel)  # Get player bounding box
            collides = False  # Define flag for collision
            blocks_to_the_right_pos: list[glm.ivec3] = [glm.ivec3(self.position + self.right), glm.ivec3(self.position + self.right - one_block_above)]  # Initialize list of blocks to the right of the player (assumes that the height of the player is 2)
            for block_pos in blocks_to_the_right_pos:
                voxel_id = self.get_voxel_id(world_pos=block_pos)
                if voxel_id == 0: continue # If the voxel is air, skip the iteration

                block_bound_box = self.get_voxel_bounds(world_pos=block_pos)
                if self.collision_manager.check_collision(bound_box, block_bound_box):  # Check if player collides with any of the blocks
                    collides = True  # Set collision flag to True
                    break

            if not collides:  # If player does not collide with any of the blocks
                self.move_right(vel)  # If player does not collide with any of the blocks, move the player to the right

        if key_state[LEFT_KEY]:  # Move the player to the left
            bound_box = self.get_bound_box(self.position - self.right * vel)  # Get player bounding box
            collides = False  # Define flag for collision
            blocks_to_the_left_pos: list[glm.ivec3] = [glm.ivec3(self.position - self.right), glm.ivec3(self.position - self.right - one_block_above)]  # Define list of blocks to the left of the player
            for block_pos in blocks_to_the_left_pos:
                voxel_id = self.get_voxel_id(world_pos=block_pos)
                if voxel_id == 0: continue  # If the voxel is air, skip the iteration

                block_bound_box = self.get_voxel_bounds(world_pos=block_pos)
                if self.collision_manager.check_collision(bound_box, block_bound_box):  # Check if player collides with any of the blocks
                    collides = True  # Set collision flag to True
                    break  # Break the loop

            if not collides:  # If player does not collide with any of the blocks
                self.move_left(vel)  # If player does not collide with any of the blocks, move the player to the left

        if key_state[UP_KEY]:  # Move the player up
            bound_box = self.get_bound_box(self.position + self.up * vel)
            block_above_world_pos: glm.ivec3 = glm.ivec3(self.position + self.up)  # Define block above the player (assumes that the height of the player is 2)
            voxel_id = self.get_voxel_id(world_pos=block_above_world_pos)
            if voxel_id == 0 or not self.collision_manager.check_collision(bound_box, self.get_voxel_bounds(world_pos=block_above_world_pos)):
                self.move_up(vel)

        if key_state[DOWN_KEY]:  # Move the player down
            bound_box = self.get_bound_box(self.position - self.up * vel)
            block_below_pos: glm.ivec3 = glm.ivec3(self.position - self.up + glm.vec3(0, 1, 0))  # Define block below the player (assumes that the height of the player is 2)
            voxel_id = self.get_voxel_id(world_pos=block_below_pos)
            if voxel_id == 0 or not self.collision_manager.check_collision(bound_box, self.get_voxel_bounds(world_pos=block_below_pos)):
                self.move_down(vel)

    def apply_gravity(self):
        """Apply gravity to the player."""

        # Use a fixed downward direction vector (0, -1, 0) for gravity
        downward_direction = glm.vec3(0, -1, 0)
        bound_box = self.get_bound_box(self.position + downward_direction * GRAVITY_STRENGTH)  # Get player bounding box (1 unit below the player to simulate the player standing)
        block_below_world_pos: glm.ivec3 = glm.ivec3(self.position + downward_direction)  # Get block below the player (ivec means integer vector needed to get proper voxel world position)
        voxel_id = self.get_voxel_id(world_pos=block_below_world_pos)
        
        # Check for collision and move down if no collision
        if voxel_id == 0 or not self.collision_manager.check_collision(bound_box, self.get_voxel_bounds(world_pos=block_below_world_pos)):
            self.position += downward_direction * GRAVITY_STRENGTH

    def get_bound_box(self, desired_position):
        """Returns player bounding box."""

        x, y, z = desired_position

        min_x = x - self.width / 2
        max_x = x + self.width / 2
        min_y = y
        max_y = y + self.heigth
        min_z = z - self.depth / 2
        max_z = z + self.depth / 2
        return min_x, max_x, min_y, max_y, min_z, max_z
    
    def get_voxel_bounds(self, world_pos):
        return self.engine.scene.world.get_voxel_bounds(world_pos)
    
    def get_voxel_id(self, world_pos):
        return self.engine.scene.world.get_voxel_id(world_pos)