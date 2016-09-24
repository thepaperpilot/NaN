import esper

class SceneBase:

    def __init__(self):
        self.world = esper.World()
        self.next = self

    def init(self):
        print("uh-oh, you didn't override this in the child class")

    def switch_to_scene(self, next_scene):
        if next_scene is not None:
            next_scene.init()
        self.next = next_scene

    def terminate(self):
        self.switch_to_scene(None)
