import tkinter as tk
from tkinter import simpledialog

def get_multiline_input():
    def submit():
        nonlocal user_input
        user_input = text_box.get("1.0", tk.END).strip()  # Get all text from the Text widget
        root.destroy()  # Close the window

    user_input = None
    root = tk.Tk()
    root.title("Multi-Line Input")
    
    tk.Label(root, text="Enter your text below:").pack(pady=5)
    
    text_box = tk.Text(root, height=10, width=50)  # Multi-line text box
    text_box.pack(pady=5)
    
    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.pack(pady=5)
    
    root.mainloop()
    return user_input

# Example usage
user_text = get_multiline_input()
print("\nYou entered:")
print(user_text)

user_text = get_multiline_input()
print("\nYou entered:")
print(user_text)