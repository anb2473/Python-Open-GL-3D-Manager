from app import App
from model import Cube


def foo(obj):
    obj.rot.y = app.time


if __name__ == '__main__':
    global app

    app = App()

    app.add_texture('box', 'img.png')
    app.add_texture('water', 'water-1018808_1280.jpg')
    app.add_object(Cube(app, texture='box', pos=(0, 0, 0)))
    app.add_object(Cube(app, texture='water', pos=(0, -2, 0), scale=(100, 0, 100)))

    id = app.add_obj_mesh('cat', 'cat/20430_cat_diff_v1.jpg', 'textures/cat/20430_Cat_v1_NEW.obj', rot=(-90, 0, 0), pos=(0, -2, -10))

    app.add_obj_mesh('cone', 'cone/pavement_06_diff_2k.jpg', 'textures/cone/untitled.obj', rot=(0, 0, 0),
                     pos=(0, 2, 10))

    app.add_obj_mesh('cube', 'cone/pavement_06_diff_2k.jpg', 'textures/texturedCube/untitled.obj', rot=(0, 0, 0),
                     pos=(0, 5, 10))

    while True:
        app.call_on_object(id, foo)

        app.run()