# globals.py
class _AppState:
    def __init__(self):
        self.status = False  # Default false state
    
    def __str__(self):
        return f"AppState(status={self.status})"

# The single shared instance
print("@@@@@@@@@@@@@@@@@@@@@@@")
app_state = _AppState()