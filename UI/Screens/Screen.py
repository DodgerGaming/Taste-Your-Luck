class Screen:

    def __init__(self):
        self.next_screen = None

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass

    def get_next_screen(self):
        return self.next_screen