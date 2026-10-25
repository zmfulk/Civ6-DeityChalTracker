import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import filedialog
import json
import time
import os
import winsound

DATA_FILE = "data.json"
CONDITIONS = ["Domination", "Science", "Culture", "Religious", "Diplomacy"]
STATUSES = ["Pending", "Active", "Conquered!"]

# Replaced "Civ / Leader" with a blank string for a cleaner default option
LEADERS = [""] + sorted([
    "Teddy Roosevelt (Rough Rider)", "Teddy Roosevelt (Bull Moose)", "Abraham Lincoln",
    "Saladin (Vizier)", "Cleopatra (Egyptian)", "Cleopatra (Ptolemaic)", "Saladin (Sultan)", "John Curtin", "Montezuma", "Hammurabi",
    "Pedro II", "Basil II", "Theodora", "Wilfrid Laurier", "Qin Shi Huang (Unifier)",
    "Qin Shi Huang", "Wu Zetian", "Yongle", "Kublai Khan (China)" ,"Kublai Khan (Mongolia)",
    "Poundmaker", "Victoria (Age of Empire)", "Victoria (Age of Steam)",
    "Eleanor of Aquitaine", "Elizabeth I", "Menelik II", "Catherine de Medici (Magnificent)",
    "Catherine de Medici (Black Queen)", "Ambiorix", "Tamar", "Frederick Barbarossa",
    "Ludwig II", "Simon Bolivar", "Pericles", "Gorgo", "Matthias Corvinus",
    "Pachacuti", "Gandhi", "Chandragupta", "Gitarja", "Hojo Tokimune", "Tokugawa",
    "Jayavarman VII", "Mvemba a Nzinga", "Nzinga Mbande", "Seondeok", "Sejong",
    "Alexander", "Mansa Musa", "Sundiata Keita", "Kupe", "Lady Six Sky",
    "Genghis Khan", "Wilhelmina", "Harald Hardrada (Varangian)",
    "Harald Hardrada (Konge)", "Amanitore", "Suleiman (Kanuni)",
    "Suleiman (Muhtesem)", "Cyrus", "Nader Shah", "Dido", "Jadwiga", "Joao III",
    "Trajan", "Julius Caesar", "Peter", "Robert the Bruce", "Tomyris",
    "Philip II", "Gilgamesh", "Kristina", "Ba Trieu", "Shaka",
])

current_order = CONDITIONS.copy()
timer_state = {cond: {"running": False, "elapsed": 0.0, "last_start": 0.0} for cond in CONDITIONS}
previous_statuses = {cond: "Pending" for cond in CONDITIONS}

def get_raw_seconds(cond):
    data = timer_state[cond]
    total_sec = data["elapsed"]
    if data["running"]:
        total_sec += time.time() - data["last_start"]
    return total_sec

def get_formatted_time(cond, show_seconds=False):
    total_sec = int(get_raw_seconds(cond))
    h = total_sec // 3600
    m = (total_sec % 3600) // 60
    s = total_sec % 60
    if show_seconds:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{h:02d}:{m:02d}"

def get_master_time(show_seconds=False):
    total_sec = int(sum(get_raw_seconds(cond) for cond in CONDITIONS))
    h = total_sec // 3600
    m = (total_sec % 3600) // 60
    s = total_sec % 60
    if show_seconds:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{h:02d}:{m:02d}"

def save_data(notify=True):
    out_data = {
        "_order": current_order,
        "match_settings": settings_var.get(),
        "master_timer": get_master_time(show_seconds=False),
        "audio_file": audio_file_var.get()
    }
    
    for cond in current_order:
        status_val = status_vars[cond].get()
        civ_val = civ_vars[cond].get()
        turn_val = turn_vars[cond].get()
        
        if status_val == "Conquered!" and previous_statuses.get(cond) != "Conquered!":
            audio_path = audio_file_var.get()
            if audio_path and os.path.exists(audio_path):
                try:
                    winsound.PlaySound(audio_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                except Exception:
                    pass
                
        previous_statuses[cond] = status_val
        
        out_data[cond] = {
            "status": status_val,
            "civ": civ_val,
            "timer": get_formatted_time(cond, show_seconds=False),
            "turns": turn_val,
            "elapsed_seconds": get_raw_seconds(cond)
        }
    
    with open(DATA_FILE, "w") as f:
        json.dump(out_data, f)
        
    if notify:
        status_label.config(text="Live Overlay Updated!", fg="#2e7d32")
        root.after(2000, lambda: status_label.config(text=""))

def on_var_change(*args):
    save_data(notify=True)

def toggle_timer(cond):
    if timer_state[cond]["running"]:
        timer_state[cond]["elapsed"] += time.time() - timer_state[cond]["last_start"]
        timer_state[cond]["running"] = False
        if cond in toggle_btns and toggle_btns[cond].winfo_exists():
            toggle_btns[cond].config(text="Start")
    else:
        timer_state[cond]["last_start"] = time.time()
        timer_state[cond]["running"] = True
        if cond in toggle_btns and toggle_btns[cond].winfo_exists():
            toggle_btns[cond].config(text="Pause")
    
    update_gui_timers()
    save_data(notify=True)

def reset_timer(cond):
    timer_state[cond]["elapsed"] = 0.0
    timer_state[cond]["running"] = False
    timer_state[cond]["last_start"] = 0.0
    if cond in toggle_btns and toggle_btns[cond].winfo_exists():
        toggle_btns[cond].config(text="Start")
    update_gui_timers()
    save_data(notify=True)

def set_timer(cond):
    val = simpledialog.askstring("Set Time", f"Enter new time for {cond} (HH:MM):", parent=root)
    if val:
        try:
            parts = val.split(":")
            if len(parts) == 2:
                h, m = int(parts[0]), int(parts[1])
            elif len(parts) == 1:
                h, m = 0, int(parts[0]) 
            else:
                return
            timer_state[cond]["elapsed"] = (h * 3600) + (m * 60)
            if timer_state[cond]["running"]:
                timer_state[cond]["last_start"] = time.time()
            update_gui_timers()
            save_data(notify=True)
        except ValueError:
            pass

def update_gui_timers():
    for cond in CONDITIONS:
        if cond in timer_labels and timer_labels[cond].winfo_exists():
            timer_labels[cond].config(text=get_formatted_time(cond, show_seconds=True))
    if 'lbl_master_timer' in globals() and lbl_master_timer.winfo_exists():
        lbl_master_timer.config(text=f"Total: {get_master_time(show_seconds=True)}")

def tick_timers():
    any_running = any(timer_state[cond]["running"] for cond in CONDITIONS)
    update_gui_timers()
    if any_running:
        save_data(notify=False)
    root.after(1000, tick_timers)

def move_up(cond):
    idx = current_order.index(cond)
    if idx > 0:
        current_order[idx], current_order[idx-1] = current_order[idx-1], current_order[idx]
        draw_rows()
        save_data()

def move_down(cond):
    idx = current_order.index(cond)
    if idx < len(current_order) - 1:
        current_order[idx], current_order[idx+1] = current_order[idx+1], current_order[idx]
        draw_rows()
        save_data()

def select_audio():
    filepath = filedialog.askopenfilename(title="Select Victory Audio", filetypes=[("WAV files", "*.wav")])
    if filepath:
        audio_file_var.set(filepath)
        save_data(notify=True)

def clear_audio():
    audio_file_var.set("")
    save_data(notify=True)

root = tk.Tk()
root.title("Civ 6 Challenge Tracker")
root.geometry("980x500") 
root.configure(padx=20, pady=20)

tk.Label(root, text="Civilization VI Challenge Tracker", font=("Helvetica", 14, "bold")).pack(pady=(0, 10))

status_vars = {}
civ_vars = {}
turn_vars = {}
timer_labels = {}
toggle_btns = {}

settings_var = tk.StringVar(value="Deity | Pangea | Standard Speed | Monopolies Mode")
audio_file_var = tk.StringVar(value="victory.wav")

for cond in CONDITIONS:
    status_vars[cond] = tk.StringVar(value="Pending")
    civ_vars[cond] = tk.StringVar(value="") # Initialize as purely blank
    turn_vars[cond] = tk.StringVar(value="")

if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r") as f:
            saved_data = json.load(f)
            if "_order" in saved_data: current_order = saved_data["_order"]
            if "match_settings" in saved_data: settings_var.set(saved_data["match_settings"])
            if "audio_file" in saved_data: audio_file_var.set(saved_data["audio_file"])
            for cond in CONDITIONS:
                if cond in saved_data:
                    d = saved_data[cond]
                    loaded_status = d.get("status", "Pending")
                    status_vars[cond].set(loaded_status)
                    previous_statuses[cond] = loaded_status 
                    
                    civ_val = d.get("civ", "")
                    civ_vars[cond].set(civ_val) # Loads raw value directly
                    
                    turn_vars[cond].set(d.get("turns", ""))
                    timer_state[cond]["elapsed"] = d.get("elapsed_seconds", 0.0)
                    timer_state[cond]["running"] = False
                    timer_state[cond]["last_start"] = 0.0
    except Exception as e:
        print(f"Warning: Could not load data.json - starting fresh. ({e})")

settings_var.trace_add("write", on_var_change)
for cond in CONDITIONS:
    status_vars[cond].trace_add("write", on_var_change)
    civ_vars[cond].trace_add("write", on_var_change)
    turn_vars[cond].trace_add("write", on_var_change)

settings_frame = tk.Frame(root)
settings_frame.pack(pady=(0, 5), fill=tk.X, padx=10)
tk.Label(settings_frame, text="Match Settings Bar:", font=("Helvetica", 10), width=18, anchor="w").pack(side=tk.LEFT)
ent_settings = tk.Entry(settings_frame, textvariable=settings_var, width=65)
ent_settings.pack(side=tk.LEFT)
lbl_master_timer = tk.Label(settings_frame, text="Total: 00:00:00", font=("Consolas", 11, "bold"), fg="#b08d44")
lbl_master_timer.pack(side=tk.RIGHT)

audio_frame = tk.Frame(root)
audio_frame.pack(pady=(0, 15), fill=tk.X, padx=10)
tk.Label(audio_frame, text="Victory Sound (.wav):", font=("Helvetica", 10), width=18, anchor="w").pack(side=tk.LEFT)
ent_audio = tk.Entry(audio_frame, textvariable=audio_file_var, width=50, state='readonly')
ent_audio.pack(side=tk.LEFT, padx=(0, 5))
btn_browse = tk.Button(audio_frame, text="Browse...", command=select_audio)
btn_browse.pack(side=tk.LEFT, padx=2)
btn_clear = tk.Button(audio_frame, text="Clear", command=clear_audio)
btn_clear.pack(side=tk.LEFT, padx=2)

rows_frame = tk.Frame(root)
rows_frame.pack()

status_label = tk.Label(root, text="", font=("Helvetica", 9))
status_label.pack(pady=10)

def draw_rows():
    for widget in rows_frame.winfo_children():
        widget.destroy()
        
    for i, cond in enumerate(current_order):
        btn_up = tk.Button(rows_frame, text="▲", command=lambda c=cond: move_up(c), width=2)
        btn_up.grid(row=i, column=0, padx=2, pady=5)
        if i == 0: btn_up.config(state=tk.DISABLED)
        
        btn_down = tk.Button(rows_frame, text="▼", command=lambda c=cond: move_down(c), width=2)
        btn_down.grid(row=i, column=1, padx=2, pady=5)
        if i == len(current_order) - 1: btn_down.config(state=tk.DISABLED)
        
        tk.Label(rows_frame, text=cond + ":", font=("Helvetica", 10, "bold"), width=12, anchor="e").grid(row=i, column=2, padx=5, pady=5)
        
        status_dropdown = ttk.Combobox(rows_frame, textvariable=status_vars[cond], values=STATUSES, state="readonly", width=12)
        status_dropdown.grid(row=i, column=3, padx=5, pady=5)
        
        civ_dropdown = ttk.Combobox(rows_frame, textvariable=civ_vars[cond], values=LEADERS, width=28)
        civ_dropdown.grid(row=i, column=4, padx=5, pady=5)
        
        lbl_timer = tk.Label(rows_frame, text=get_formatted_time(cond, show_seconds=True), font=("Consolas", 11, "bold"), width=8)
        lbl_timer.grid(row=i, column=5, padx=10)
        timer_labels[cond] = lbl_timer
        
        btn_state = "Pause" if timer_state[cond]["running"] else "Start"
        btn_toggle = tk.Button(rows_frame, text=btn_state, command=lambda c=cond: toggle_timer(c), width=6)
        btn_toggle.grid(row=i, column=6, padx=2)
        toggle_btns[cond] = btn_toggle
        
        btn_reset = tk.Button(rows_frame, text="Reset", command=lambda c=cond: reset_timer(c), width=5)
        btn_reset.grid(row=i, column=7, padx=2)
        
        btn_set = tk.Button(rows_frame, text="Set Time", command=lambda c=cond: set_timer(c), width=8)
        btn_set.grid(row=i, column=8, padx=2)
        
        tk.Label(rows_frame, text="Turns:", font=("Helvetica", 9)).grid(row=i, column=9, padx=(10, 2))
        ent_turns = tk.Entry(rows_frame, textvariable=turn_vars[cond], width=6)
        ent_turns.grid(row=i, column=10, padx=2)

draw_rows()
save_data(notify=False)
tick_timers() 
root.mainloop()