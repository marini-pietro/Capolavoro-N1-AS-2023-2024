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

        #Define standardized vectors
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

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
        self.pitch -= delta_y # Update pitch
        self.pitch = glm.clamp(self.pitch, -PITCH_MAX, PITCH_MAX) # Clamp pitch to avoid flipping the camera

    def rotate_yaw(self, delta_x):
        self.yaw += delta_x

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