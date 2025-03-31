from model import *
from pyglm import glm


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []

        # skybox
        self.skybox = AdvancedSkyBox(app)

    def add_object(self, obj):
        self.objects.append(obj)
        return len(self.objects) - 1
