# module_c.py
from globals import app_state
from module_a import mod_a_enable_system
from module_b import mod_b_toggle_system

def mod_c_check_status():
    """Returns current status with verification"""
    status = "ACTIVE" if app_state.status else "INACTIVE"
    print(f"[Module C] Current system status: {status}")
    return app_state.status

def main():
    print("=== System Control Demo ===")
    print(f"Initial state: {app_state}\n")
    
    mod_c_check_status()          # Should show INACTIVE
    mod_a_enable_system()         # Module A sets to True
    mod_c_check_status()          # Should show ACTIVE
    mod_b_toggle_system()         # Module B flips to False
    mod_b_toggle_system()         # Module B flips back to True
    mod_c_check_status()          # Should show ACTIVE
    
    print("\nFinal state:", app_state)

if __name__ == "__main__":
    main()