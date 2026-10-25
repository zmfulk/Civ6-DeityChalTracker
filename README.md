# Civ 6 Challenge Tracker Overlay

A customizable, animated OBS stream overlay for tracking Civilization VI victory condition challenges. It features a Python/Tkinter control panel that updates a local browser source in real-time.

## Features
* **Dynamic Overlay:** Tracks Domination, Science, Culture, Religious, and Diplomacy victories.
* **Match Settings Bar:** A sleek gold header to display current game settings (Speed, Difficulty, Map).
* **Master Timer:** Automatically calculates total challenge time based on individual running timers.
* **Turn Counter:** Displays the exact turn a victory condition was achieved.
* **Automated Audio & Animation:** Triggers a 3D flip animation and plays a `.wav` file when a victory is conquered.
* **Data Persistence:** Automatically saves your timers, selections, and layouts locally so you never lose progress between streams.

## Prerequisites
* Python 3.x installed (if running from source).
* OBS Studio (or any streaming software that supports local browser sources).

## Setup Instructions

**1. Prepare the Control Panel**
* Clone or download this repository.
* Run the Python controller: `python gui_controller.py`
* (Optional) Select a custom `victory.wav` file via the Browse button in the app.

**2. Add to OBS**
* In OBS, add a new **Browser Source**.
* Check the box for **Local file** and select the `overlay.html` file from this folder.
* Set the **Width** to `1920` and **Height** to `1080` (or match your base canvas size).
* Check the box for **Refresh browser when scene becomes active**.
* Click OK. The overlay will appear at the bottom center of your screen.

## File Structure
Ensure your image and audio assets are placed correctly:
* `gui_controller.py` - The main control panel.
* `overlay.html` - The OBS browser source.
* `leadericons/` - Folder containing 256x256 `.png` leader portraits (e.g., `abraham_lincoln.png`).
* `domination.png`, `science.png`, etc. - Victory condition icons placed in the root directory.
* `victory.wav` - The default audio cue played upon victory.

## Usage
Use the Python app to select leaders, reorder conditions via the up/down arrows, and control your timers. All changes update the OBS overlay instantly and save automatically to a local `data.json` file.