class Stats:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        self.messages = []

    def update(self, role, content):
        self.messages.append({"role": role, "content": content})

    def clear_messages(self):
        self.messages = []

    def generate_response(self):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages
        )
        return response['choices'][0]['message']['content']

def extract_stats(response):
    # extract stats from model response
    return 0

def update_stats(stats):
    # update stats in interface
    return 0

def increment_turn():
    # increment turn
    return 0