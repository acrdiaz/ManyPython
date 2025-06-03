# module_b.py
from globals import app_state

def mod_b_toggle_system():
    """Flips the current status"""
    app_state.status = not app_state.status
    print(f"[Module B] System toggled | State: {app_state}")