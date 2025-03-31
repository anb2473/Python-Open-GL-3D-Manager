import pygame as pg
import sys
import moderngl as mgl
from model import *
from camera import Camera
from light import Light
from mesh import Mesh
from scene import Scene
from scene_renderer import SceneRenderer
from vbo import AdvancedObjVBO


class App:
    def __init__(self, win_size=(1200, 700), skybox_dtype='jpg', camera_position=(0, 0, 4), camera_yaw=-90, camera_pitch=0, yaw_move=True, pitch_move=False, pitch_turn=True, yaw_turn=True):
        pg.init()
        self.WIN_SIZE = win_size

        # set opengl attr
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        # create display
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)

        # mouse settings
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)

        # time variables
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0

        # camera objects
        self.light = Light()
        self.camera = Camera(self, camera_position, camera_yaw, camera_pitch, yaw_move, pitch_move, pitch_turn, yaw_turn)

        self.mesh = Mesh(self, skybox_dtype)

        # scene objects
        self.scene = Scene(self)
        self.scene_renderer = SceneRenderer(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                self.scene_renderer.destroy()
                pg.quit()
                sys.exit()

    def render(self):
        self.ctx.clear(color=(0.08, 0.16, 0.18, 1.0))

        # render scene
        self.scene_renderer.render()

        # swap buffers
        pg.display.flip()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def run(self):
        self.get_time()
        self.check_events()
        self.camera.update()
        self.render()
        self.delta_time = self.clock.tick(60)

    def add_object(self, object):
        return self.scene.add_object(object)

    def call_on_object(self, id, func):
        func(self.scene.objects[id])

    def add_texture(self, id, path):
        self.mesh.texture.add_texture(id, path)

    def add_vao(self, id, program='default', vbo=None, shadow_vbo=None):
        if vbo is None:
            vbo = id
        if shadow_vbo is None:
            shadow_vbo = vbo
        self.mesh.vao.add_vao(id, program, vbo)
        self.mesh.vao.add_vao('shadow_' + id, 'shadow_map', shadow_vbo)

    def add_vbo(self, id, objectClass):
        self.mesh.vao.vbo.add_vbo(id, objectClass)

    def add_mesh(self, id, texture, object_class, vbo, program='default'):
        self.add_texture(id, texture)
        self.add_vbo(id, vbo)
        self.add_vao(id, program)
        return self.add_object(object_class(self, pos=(0, -1, -10)))

    def add_obj_mesh(self, id, texture, object_file, program='default', pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        self.add_texture(id, texture)
        vbo = AdvancedObjVBO(self, path=object_file)
        self.mesh.vao.vbo.add_class_vbo(id, vbo)
        self.add_vao(id, program)
        object_class = ExtendedBaseModel(self, id, id, pos, rot, scale)
        return self.add_object(object_class)