import tkinter as tk


def get_multiline_input(title, prompt):
    """Display a multi-line input dialog and return the user input."""
    def submit():
        nonlocal user_input
        user_input = text_box.get("1.0", tk.END).strip()  # Get all text from the Text widget
        root.destroy()  # Close the window

    user_input = None
    root = tk.Tk()
    root.title(title)
    root.geometry("400x300")  # Retaining the current size

    tk.Label(root, text=prompt).pack(pady=5)

    text_box = tk.Text(root, height=13, width=50)  # Multi-line text box
    text_box.pack(pady=5)

    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.pack(pady=5)

    root.mainloop()
    return user_input