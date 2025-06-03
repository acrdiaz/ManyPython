# module_a.py
from globals import app_state

def mod_a_enable_system():
    """Sets the global status to True"""
    app_state.status = True
    print(f"[Module A] System enabled | State: {app_state}")