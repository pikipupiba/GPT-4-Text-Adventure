class Game:
    def __init__(self):
        ...
        self.history = []  # list to store history
        
    def add_to_history(self, event):
        self.history.append(event)