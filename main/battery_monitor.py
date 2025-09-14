import tkinter as tk
from tkinter import ttk
import sv_ttk
import psutil
from win10toast import ToastNotifier
import winsound
import time
import threading
from pystray import MenuItem as item, Icon
from PIL import Image
import sys
import os
import winreg # --- NEW --- Import for registry access
import winsdk.windows.ui.notifications as notifications
import winsdk.windows.data.xml.dom as dom
import time
import os, sys, winshell
from win32com.client import Dispatch

xml_doc = dom.XmlDocument()


# APP_ID = "Chargee"

# shortcut_path = os.path.join(winshell.start_menu(), "Chargee.lnk")
# target = sys.executable   # path to python.exe
# arguments = os.path.abspath(__file__)  # your script
# icon = target

# shell = Dispatch("WScript.Shell")
# shortcut = shell.CreateShortCut(shortcut_path)
# shortcut.Targetpath = target
# shortcut.Arguments = arguments
# shortcut.IconLocation = icon
# shortcut.save()

# --- Helper Function for PyInstaller ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller. """
    try:
        base_path = sys._MEIPASS  # type: ignore # folder created by PyInstaller
    except AttributeError:
        base_path = os.path.dirname(__file__)  # script directory in dev

    return os.path.join(base_path, relative_path)

# --- NEW --- Registry Management Functions ---
APP_NAME = "BatteryChargeMonitor" # Name for the registry key

def get_startup_key():
    # This will point to HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
    return winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                           r'Software\Microsoft\Windows\CurrentVersion\Run',
                           0, winreg.KEY_ALL_ACCESS)

def add_to_startup():
    """Adds the application to Windows startup."""
    try:
        key = get_startup_key()
        # sys.executable is the path to python.exe when running script,
        # but becomes the path to the .exe when bundled by PyInstaller.
        exe_path = f'"{sys.executable}"' # Ensure path is quoted
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
        print(f"'{APP_NAME}' added to startup.")
    except Exception as e:
        print(f"Error adding to startup: {e}")

def remove_from_startup():
    """Removes the application from Windows startup."""
    try:
        key = get_startup_key()
        winreg.DeleteValue(key, APP_NAME)
        winreg.CloseKey(key)
        print(f"'{APP_NAME}' removed from startup.")
    except FileNotFoundError:
        print(f"'{APP_NAME}' was not in startup, nothing to remove.")
    except Exception as e:
        print(f"Error removing from startup: {e}")

def check_if_in_startup():
    """Checks if the application is already in the startup registry."""
    try:
        key = get_startup_key()
        winreg.QueryValueEx(key, APP_NAME)
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"Error checking startup status: {e}")
        return False

def toggle_startup(variable):
    """Toggles the app's presence in startup based on the checkbox."""
    if variable.get():
        add_to_startup()
    else:
        remove_from_startup()
# --- END NEW ---


# --- Global Settings & Shared Data ---
app_settings = {
    "charge_limit": 80,
    "min_charge_limit": 20  # <-- NEW: Default minimum charge limit
}

# --- Backend Battery Logic ---
class BatMonitor():
    def __init__(self, battery_status, limit):
        self.percentage = battery_status.percent
        self.is_charging = battery_status.power_plugged
        self.limit = limit

    def limit_reached(self):
        return self.percentage >= self.limit

    def is_plugged_in(self):
        return self.is_charging

def monitor_charge(icon):
    notified = False
    min_notified = False  # <-- NEW: Track min notification
    toaster = ToastNotifier()
    toast_icon_path = None
    try:
        toast_icon_path = resource_path("toast.ico")
        if not os.path.exists(toast_icon_path):
            toast_icon_path = None  # Use None if icon is missing
    except Exception as e:
        print(f"Could not find toast icon. Error: {e}")
        toast_icon_path = None

    while not icon.visible:
        time.sleep(1)

    while True:
        try:
            battery = psutil.sensors_battery()
            device = BatMonitor(battery, app_settings["charge_limit"])
            min_limit = app_settings["min_charge_limit"]  # <-- NEW

            # --- Max limit logic (existing) ---
            if device.is_plugged_in():
                if device.limit_reached() and not notified:
                    print(f"Limit of {device.limit}% reached. Notifying user.")
                    toast_xml_str = """
                        <toast>
                        <visual>
                            <binding template="ToastGeneric">
                            <text>⚡ Charging Alert! </text>
                            <text>Please unplug your charger🔋</text>
                            </binding>
                        </visual>
                        </toast>
                    """
                    xml_doc.load_xml(toast_xml_str)
                    notifier = notifications.ToastNotificationManager.create_toast_notifier("Python")
                    notification = notifications.ToastNotification(xml_doc)
                    notifier.show(notification) # type: ignore
                    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                    notified = True

                    # toaster.show_toast(
                    #     "⚡ Charging Alert!",
                    #     f"Battery is at {device.percentage}%. Please unplug your charger.",
                    #     duration=10,
                    #     threaded=True,
                    #     icon_path=toast_icon_path
                    # )
                elif not device.limit_reached() and notified:
                    notified = False
            else:
                if notified:
                    notified = False

            # --- Min limit logic ---
            if not device.is_plugged_in():
                if device.percentage <= min_limit and not min_notified:
                    print(f"Minimum limit of {min_limit}% reached. Notifying user to charge.")
                    toast_xml_str = """
                        <toast>
                        <visual>
                            <binding template="ToastGeneric">
                            <text>⚡ Charging Alert! </text>
                            <text>Please plug in your charger🪫</text>
                            </binding>
                        </visual>
                        </toast>
                    """
                    xml_doc.load_xml(toast_xml_str)
                    notifier = notifications.ToastNotificationManager.create_toast_notifier("Python")
                    notification = notifications.ToastNotification(xml_doc)
                    notifier.show(notification) # type: ignore
                    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                    min_notified = True
                elif device.percentage > min_limit and min_notified:
                    min_notified = False
            else:
                if min_notified:
                    min_notified = False
            # --- END NEW ---

            time.sleep(10)
        except Exception as e:
            print(f"An error occurred in monitor thread: {e}")
            time.sleep(60)

# --- GUI Functions ---
def set_charge_limit():
    try:
        limit_str = limit_entry.get()
        min_limit_str = min_limit_entry.get()  # <-- NEW
        if limit_str and limit_str.isdigit() and min_limit_str and min_limit_str.isdigit():
            limit_val = int(limit_str)
            min_limit_val = int(min_limit_str)
            if 0 < min_limit_val < limit_val <= 100:
                app_settings["charge_limit"] = limit_val
                app_settings["min_charge_limit"] = min_limit_val  # <-- NEW
                print(f"Charge limits set to: Max {limit_val}%, Min {min_limit_val}%")
                status_label.config(
                    text=f"Limits set: Max {limit_val}%, Min {min_limit_val}%.",
                    foreground="green"
                )
                root.withdraw() # Hide window after setting
            else:
                status_label.config(
                    text="Min must be < Max, both 1-100.",
                    foreground="orange"
                )
        else:
            status_label.config(text="Please enter valid numbers.", foreground="red")
    except Exception as e:
        print(f"An error occurred in set_charge_limit: {e}")
        status_label.config(text="An error occurred.", foreground="red")

def show_window(icon=None, item=None):
    root.deiconify()
    root.lift()
    root.focus_force()

def quit_app(icon, item):
    print("Quit command received. Shutting down.")
    icon.stop()
    root.quit()
    root.destroy()
    sys.exit()

# --- System Tray Icon Setup ---
def setup_tray_icon():
    try:
        image = Image.open(resource_path("ikeon.png"))
    except Exception as e:
        print(f"⚠️ Could not load image icon. Using default. Error: {e}")
        image = Image.new("RGB", (64, 64), color="grey")

    menu = (
        item('Open Settings', show_window, default=True),
        item('Quit', quit_app)
    )
    icon = Icon("BatteryMonitor", image, "Battery Charge Monitor", menu)
    root.tray_icon = icon # type: ignore

    monitor_thread = threading.Thread(target=monitor_charge, args=(icon,), daemon=True)
    monitor_thread.start()

    print("Starting tray icon...")
    icon.run()
    print("Tray icon stopped.")

# --- Main Window (GUI) Setup ---
root = tk.Tk()
root.title("Battery Monitor Settings")
root.geometry("400x250") # Increased height for new checkbox
root.resizable(True, True)
sv_ttk.set_theme("dark")

main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill="both", expand=True)

prompt_label = ttk.Label(main_frame, text="Set Max Charge Limit (%)", font=("Segoe UI", 12))
prompt_label.pack(pady=(0, 10))

limit_entry = ttk.Entry(main_frame, width=10, font=("Segoe UI", 11), justify='center')
limit_entry.pack(pady=5)
limit_entry.insert(0, str(app_settings["charge_limit"]))

# --- NEW: Minimum Charge Limit Field ---
min_prompt_label = ttk.Label(main_frame, text="Set Min Charge Limit (%)", font=("Segoe UI", 12))
min_prompt_label.pack(pady=(10, 0))

min_limit_entry = ttk.Entry(main_frame, width=10, font=("Segoe UI", 11), justify='center')
min_limit_entry.pack(pady=5)
min_limit_entry.insert(0, str(app_settings["min_charge_limit"]))
# --- END NEW ---

set_button = ttk.Button(main_frame, text="Set and Hide", command=set_charge_limit, style="Accent.TButton")
set_button.pack(pady=10)

status_label = ttk.Label(main_frame, text="", font=("Segoe UI", 10))
status_label.pack(pady=(5, 0))

# --- NEW --- Startup Checkbox ---
startup_var = tk.BooleanVar()
startup_checkbox = ttk.Checkbutton(
    main_frame,
    text="Start with Windows",
    variable=startup_var,
    command=lambda: toggle_startup(startup_var)
)
startup_checkbox.pack(pady=10)
# --- END NEW ---

# --- Application Start ---
if __name__ == "__main__":
    # Hide the main window initially
    root.withdraw()
    root.tray_icon = None # type: ignore

    # --- NEW --- Check startup status and set checkbox ---
    if check_if_in_startup():
        startup_var.set(True)
    # --- END NEW ---

    tray_thread = threading.Thread(target=setup_tray_icon, daemon=True)
    tray_thread.start()
    
    # If settings window is opened for the first time, show it
    # This provides a good first-run experience.
    # On subsequent starts (from Windows startup), this won't show.
    if not check_if_in_startup():
        show_window()

    root.mainloop()