🔋 Battery Limiter
A lightweight, simple, and modern Windows utility to help you extend your laptop's battery lifespan by reminding you to unplug it when it reaches a custom charge limit.

Why Use Battery Limiter?
Keeping your laptop battery charged between 20% and 80% can significantly increase its overall lifespan. This app runs quietly in your system tray, monitors your battery level, and notifies you to unplug the charger when it hits the limit you've set, preventing unnecessary overcharging.

✨ Key Features
Custom Charge Limit: Set any charge percentage (e.g., 80%, 85%) as your target.

System Tray Icon: Runs silently in the background and is accessible via a clean system tray icon.

Desktop Notifications: Get a clear, audible notification when your battery reaches the set limit.

Start with Windows: Conveniently set the app to launch automatically when you log in.

Modern UI: A simple, clean settings window with a dark theme, built with sv-ttk.

Lightweight: Uses minimal system resources.

⬇️ Installation & Usage
Go to the Releases page of this repository.

Download the BatteryLimiter.exe file from the latest release.

Run the downloaded .exe file. No installation is needed!

The first time you run it, a settings window will appear.

Set your desired charge limit (e.g., 80).

Check the "Start with Windows" box if you want it to run automatically.

Click "Set and Hide".

The app will now run in your system tray. You can right-click the tray icon at any time to open the settings or quit the application.

🛠️ Building From Source
If you want to modify the code or build it yourself, follow these steps.

Prerequisites:

Python 3.8+

Setup:

Clone the repository:

git clone https://github.com/YOUR_USERNAME/battery-limiter.git
cd battery-limiter

Create a virtual environment (recommended):

python -m venv venv
venv\Scripts\activate  # On Windows

Install the required packages:

pip install -r requirements.txt

(You will need to create a requirements.txt file containing the following):

psutil
win10toast-reborn
pystray
Pillow
sv-ttk

Run the application:

python main.py

Build the executable:
Use PyInstaller to package the application into a single .exe file. The icon and assets must be in an assets folder.

pyinstaller --noconsole --onefile --windowed --icon="assets/ikeon.ico" --add-data "assets;assets" main.py -n BatteryLimiter

I shall soon add prebuilt binaries for easy install i am pretty sure this aint a big project but i shall do whats due 
i believe every laptop regardless of the manufactorer needs a method to sustain its battery (and battery limiter a popular 3rd party app has a extremely disgracefull and straight up BAD UI) so i put in some minimum effort to make a small utility that runs in minimum overhead and reminds you to plug out the laptop i will soon add more utility too !
if you are reading this note that most of the readme file was made by LLM/AI because college doesnt gimme much time 
i hope the best for you and a star to this repo would be lovely my aim's to make life easier prolly, idk bye ^_____^

📜 License
As of now none... not that big of a app yo!

🙌 Acknowledgements
This application was made possible by these fantastic open-source libraries:

psutil for battery information.

pystray for the system tray icon.

sv-ttk for the beautiful modern theme.

Pillow for image handling.

win10toast-reborn for Windows notifications.