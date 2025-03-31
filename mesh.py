from vao import VAO
from texture import Texture


class Mesh:
    def __init__(self, app, skybox_dtype):
        self.app = app
        self.vao = VAO(app.ctx)
        self.texture = Texture(app, skybox_dtype)

    def destroy(self):
        self.vao.destroy()
        self.texture.destroy()