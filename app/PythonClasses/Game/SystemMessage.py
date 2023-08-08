class SystemMessage:
    def __init__(self):
        self.current_message = ""
    
    def set_message(self, message):
        self.current_message = message
    
    def get_message(self):
        return self.current_message