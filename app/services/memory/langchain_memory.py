from typing import List, Dict

# Simple in-memory store: { "user_session_key": [ {role, content}, ... ] }
_memory_store: Dict[str, List[Dict]] = {}

class TherapistMemory:
    def __init__(self, session_id: str, user_id: str):
        self.key = f"{user_id}_{session_id}"
        if self.key not in _memory_store:
            _memory_store[self.key] = []

    def add_user_message(self, message: str):
        _memory_store[self.key].append({"role": "user", "content": message})

    def add_ai_message(self, message: str):
        _memory_store[self.key].append({"role": "assistant", "content": message})

    def get_history_as_list(self) -> List[Dict]:
        return _memory_store[self.key][-20:]

    def get_summary_context(self) -> str:
        messages = _memory_store[self.key]
        if not messages:
            return "This is the start of our conversation."
        return f"We've exchanged {len(messages)} messages so far."

    def clear(self):
        _memory_store[self.key] = []
