class SceneManager:
    def __init__(self):
        self.scene = None

    def set_scene(self, scene):
        self.scene = scene

    def handle_events(self, events):
        if self.scene:
            self.scene.handle_events(events)

    def update(self):
        if self.scene:
            self.scene.update()

    def draw(self, screen):
        if self.scene:
            self.scene.draw(screen)