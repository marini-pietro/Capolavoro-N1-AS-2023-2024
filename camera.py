from settings import *
from frustum import Frustum

class Camera:
    def __init__(self, position, yaw, pitch):
        """Iitializes camera object.

        Args:
            position (int): Position of the camera in 3D space
            yaw (int): Initial yaw of the camera
            pitch (int): Initial pitch of the camera
        """
        
        self.position = glm.vec3(position) # Player position vector

        # Define camera orentation variables
        self.yaw = glm.radians(yaw) # Define yaw
        self.pitch = glm.radians(pitch) # Define pitch

        #Define standardized vectors (down, left and backwards are the negative of up, right and forward)
        self.up = glm.vec3(0, 1, 0) # Up vector
        self.right = glm.vec3(1, 0, 0) # Right vector
        self.forward = glm.vec3(0, 0, -1) # Forward vector

        # Define standard matrices
        self.m_proj = glm.perspective(V_FOV, ASPECT_RATIO, NEAR, FAR) # Projection matrix
        self.m_view = glm.mat4() # View matrix (initially an indendity matrix will be updated every frame)

        self.frustum = Frustum(self) # Define Frustum object

    def update(self):
        self.update_vectors()
        self.update_view_matrix()

    def update_view_matrix(self):
        """Updates view matrix."""

        self.m_view = glm.lookAt(self.position, self.position + self.forward, self.up)

    def update_vectors(self):
        """
        Updates camera vectors based on yaw and pitch.
        """

        self.forward.x = glm.cos(self.yaw) * glm.cos(self.pitch)
        self.forward.y = glm.sin(self.pitch)
        self.forward.z = glm.sin(self.yaw) * glm.cos(self.pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def rotate_pitch(self, delta_y):
        """Rotate the camera/player around the pitch axis."""
        self.pitch -= delta_y # Update pitch
        self.pitch = glm.clamp(self.pitch, -PITCH_MAX, PITCH_MAX) # Clamp pitch to avoid flipping the camera

    def rotate_yaw(self, delta_x):
        """Rotate the camera/player around the yaw axis."""
        self.yaw += delta_x

    def move_left(self, velocity):
        """Move the camera/player to the left."""
        self.position -= self.right * velocity

    def move_right(self, velocity):
        """Move the camera/player to the right."""
        self.position += self.right * velocity

    def move_up(self, velocity):
        """Move the camera/player up."""
        self.position += self.up * velocity

    def move_down(self, velocity):
        """Move the camera/player down."""
        self.position -= self.up * velocity

    def move_forward(self, velocity):
        """Move the camera/player forward."""
        self.position += self.forward * velocity

    def move_back(self, velocity):
        """Move the camera/player backward."""
        self.position -= self.forward * velocity