class Stats:
    def __init__(self, items):
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.day_number = 0
        self.day = "Monday"
        self.new_day = True
        self.time = 60
        self.items = items
        self.relationships = {
            "Acquaintances": {
                "count": 0,
                "info": "",
            },
            "Friends": {
                "count": 0,
                "info": "",
            },
            "Best Friend": {
                "count": 0,
                "info": "",
            },
            "Enemies": {
                "count": 0,
                "info": "",
            },
            "Arch Nemesis": {
                "count": 0,
                "info": "",
            }
        }

    def set_day(self, day):
        self.day = day
    
    def set_time(self, time):
        self.time = time
    
    def subtract_time(self, time):
        self.time -= time

    def format_day_time(self):
        return f"{self.day} --- {self.time} minutes remaining"
    
    def format_items(self):
        return "\n".join(self.items)

    def format_relationships(self):
        return "\n".join([f"{data['count']} {rank}{' --- ' + data['info'] if data['info'] else ''}" for rank, data in self.relationships.items()])

    def format_stats(self):
        return [self.format_day_time(), self.format_items(), self.format_relationships()]
    
    def to_string(self):
        formatted_stats = self.format_stats()
        return f"Start of a new day: {str(self.new_day)}\nDay: {formatted_stats[0]}\nItems:\n{formatted_stats[1]}\nFriends:\n{formatted_stats[2]}"

    def update(self, arguments_json):
        self.subtract_time(int(arguments_json.get('Time', 0)))
        self.items = arguments_json.get('Items', self.items)

        updated_relationships = arguments_json.get('Relationships')
        if updated_relationships:
            self.relationships.update(updated_relationships)

        if self.time <= 0:
            self.day_number += 1
            self.time = 60
            self.new_day = True
            if self.day_number < len(self.days):
                self.day = self.days[self.day_number]
            else:
                self.day = "Unknown"
        else:
            self.new_day = False

stats = Stats([])
