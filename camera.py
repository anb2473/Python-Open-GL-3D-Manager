from pyglm import glm
import pygame as pg
from settings import *


class Camera:
    def __init__(self, app, position, yaw, pitch, yaw_move, pitch_move, pitch_turn, yaw_turn):
        self.yaw_move = yaw_move
        self.pitch_move = pitch_move
        self.pitch_turn = pitch_turn
        self.yaw_turn = yaw_turn

        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.position = glm.vec3(position)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)
        self.move_forward = glm.vec3(0, 0, -1)
        self.yaw = yaw
        self.pitch = pitch
        # view matrix
        self.m_view = self.get_view_matrix()
        # projection matrix
        self.m_proj = self.get_projection_matrix()

    def rotate(self):
        rel_x, rel_y = pg.mouse.get_rel()
        self.yaw += rel_x * MOUSE_SENSITIVITY
        self.pitch -= rel_y * MOUSE_SENSITIVITY
        self.pitch = max(-89, min(89, self.pitch))

    def update_camera_vectors(self):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        # self.move_forward.x = glm.cos(yaw) * glm.cos(pitch)
        # self.move_forward.y = glm.sin(pitch)
        # self.move_forward.z = glm.sin(yaw) * glm.cos(pitch)
        if self.yaw_turn:
            self.forward.x = glm.cos(yaw)
            self.forward.z = glm.sin(yaw)
        if self.pitch_turn:
            self.forward.x *= glm.cos(pitch)
            self.forward.y = glm.sin(pitch)
            self.forward.z *= glm.cos(pitch)

        if self.yaw_move:
            self.move_forward.x = glm.cos(yaw)
            self.move_forward.z = glm.sin(yaw)
        if self.pitch_move:
            self.move_forward.x *= glm.cos(pitch)
            self.move_forward.y = glm.sin(pitch)
            self.move_forward.z *= glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.move_forward = glm.normalize(self.move_forward)
        self.right = glm.normalize(glm.cross(self.move_forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.move_forward))

    def update(self):
        self.move()
        self.rotate()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()

    def move(self):
        velocity = SPEED * self.app.delta_time
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.position += self.move_forward * velocity
        if keys[pg.K_s]:
            self.position -= self.move_forward * velocity
        if keys[pg.K_a]:
            self.position -= self.right * velocity
        if keys[pg.K_d]:
            self.position += self.right * velocity
        if keys[pg.K_q]:
            self.position += self.up * velocity
        if keys[pg.K_e]:
            self.position -= self.up * velocity

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)




















