class Memory:
    def __init__(self, max_history=20):
        self.max_history = max_history
        self.histories = {}
    
    def add(self, user_id: int, role: str, content: str):
        if user_id not in self.histories:
            self.histories[user_id] = []
        self.histories[user_id].append({"role": role, "content": content})
        # Batasi history
        if len(self.histories[user_id]) > self.max_history:
            self.histories[user_id] = self.histories[user_id][-self.max_history:]
    
    def get(self, user_id: int) -> list:
        return self.histories.get(user_id, [])
    
    def clear(self, user_id: int):
        self.histories[user_id] = []

memory = Memory()