import tkinter as tk
from tkinter import ttk
import sv_ttk # pip install sv-ttk

def set_charge_limit():
    """
    This function is called when the 'Set' button is clicked.
    It retrieves the value from the entry box and prints it.
    In a real application, you would add the logic to control
    the battery charge limit here.
    """
    try:
        limit = limit_entry.get()
        if limit and limit.isdigit():
            # In a real app, you would implement the charging logic here.
            # For now, we'll just print it to the console and show a message.
            print(f"Charge limit set to: {limit}%")
            status_label.config(text=f"Limit set to {limit}%.", foreground="green")
        elif not limit:
             status_label.config(text="Please enter a value.", foreground="red")
        else:
            status_label.config(text="Please enter a valid number.", foreground="red")
    except Exception as e:
        print(f"An error occurred: {e}")
        status_label.config(text="An error occurred.", foreground="red")


# --- Main Window Setup ---
# Create the main application window
root = tk.Tk()
root.title("Battery Monitor")

# Set a modern window size
root.geometry("400x200")
root.resizable(True, True) # Make the window not resizable

# --- Theming ---
# This is the magic line that applies the modern theme.
# It automatically picks the light or dark theme based on your system settings.
sv_ttk.set_theme("dark") # or "dark"

# --- Widgets ---
# Create a main frame to hold all the content and add padding
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill="both", expand=True)

# Label: "Set max charge limit"
# Using ttk.Label for themed text
prompt_label = ttk.Label(
    main_frame,
    text="Set max charge limit",
    font=("Segoe UI", 12) # Segoe UI is the standard font for Windows 11
)
prompt_label.pack(pady=(0, 10)) # Add some vertical padding below the label

# Entry box for user input
# Using ttk.Entry for a themed input box
limit_entry = ttk.Entry(
    main_frame,
    width=10, # Set a width for the entry box
    font=("Segoe UI", 11),
    justify='center' # Center the text inside the entry
)
limit_entry.pack(pady=5)

# "Set" button
# Using ttk.Button for a themed button
# The "accent" style gives it the prominent blue color in Windows 11
set_button = ttk.Button(
    main_frame,
    text="Set",
    command=set_charge_limit,
    style="Accent.TButton" # Apply the accent style for emphasis
)
set_button.pack(pady=10)

# Status label to provide feedback to the user
status_label = ttk.Label(
    main_frame,
    text="",
    font=("Segoe UI", 10)
)
status_label.pack(pady=(5, 0))


# --- Run the Application ---
# Start the Tkinter event loop to display the window and handle events
root.mainloop()
