import tkinter as tk
from tkinter import ttk
import configparser
import os

# Configuration file path
config_file = 'config.txt'

# Load configuration
config = configparser.ConfigParser()
config.read(config_file)

def save_config():
    config['Settings'] = {
        'always_on_top': always_on_top_var.get(),
        'opacity': opacity_scale.get()
    }
    with open(config_file, 'w') as configfile:
        config.write(configfile)

def load_config():
    # Check if the config file exists, if not, create it with default values
    if not os.path.exists(config_file):
        config['Settings'] = {
            'always_on_top': False,
            'opacity': 1.0
        }
        with open(config_file, 'w') as configfile:
            config.write(configfile)
    else:
        config.read(config_file)
        always_on_top_var.set(config.getboolean('Settings', 'always_on_top', fallback=False))
        opacity_scale.set(config.getfloat('Settings', 'opacity', fallback=1.0))
        update_opacity(opacity_scale.get())
        toggle_always_on_top()

# Function to calculate wavelength
def calculate_wavelength(event):
    try:
        frequency = float(freq_entry.get())
        wavelength = 300 / frequency
        freq_output_label.config(text=str(wavelength))
    except ValueError:
        freq_output_label.config(text="Invalid input")
    except ZeroDivisionError:
        freq_output_label.config(text="Infinity")

# Function to toggle always on top
def toggle_always_on_top():
    root.attributes('-topmost', always_on_top_var.get())

# Function to update opacity
def update_opacity(value):
    root.attributes('-alpha', float(value))


def on_close():
    save_config()
    root.destroy()

root = tk.Tk()
root.title("Radio Helper")
root.iconbitmap('freq.ico')  # Set the window icon

# Set the window size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = int(screen_width * 0.1)
window_height = int(screen_height * 0.15)
root.geometry(f"{window_width}x{window_height}")
style = ttk.Style(root)
style.configure('bottomtab.TNotebook', tabposition='sw')

# Create the tab control
tab_control = ttk.Notebook(root, style='bottomtab.TNotebook')

# Frequency Tab
freq_tab = ttk.Frame(tab_control)
tab_control.add(freq_tab, text='Freq')
freq_entry = tk.Entry(freq_tab)
freq_entry.pack()
freq_entry.bind("<KeyRelease>", calculate_wavelength)
freq_output_label = tk.Label(freq_tab, text="")
freq_output_label.pack()

# Ohm's Law Tab
ohms_tab = ttk.Frame(tab_control)
tab_control.add(ohms_tab, text='Ohms Law')
# Add Ohm's Law widgets here

# Power Tab
power_tab = ttk.Frame(tab_control)
tab_control.add(power_tab, text='Power')
# Add Power calculation widgets here

# Settings Tab
settings_tab = ttk.Frame(tab_control)
tab_control.add(settings_tab, text='Settings')
# Checkbox for always on top
always_on_top_var = tk.BooleanVar()
always_on_top_check = tk.Checkbutton(settings_tab, text="Always on top", var=always_on_top_var, command=toggle_always_on_top)
always_on_top_check.pack()
# Opacity slider
opacity_scale = tk.Scale(settings_tab, from_=0.1, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, label="Opacity", command=update_opacity)
opacity_scale.set(1.0)  # Set default opacity to 100%
opacity_scale.pack()

tab_control.pack(expand=1, fill="both")

# Load config and apply settings
load_config()

# Save config on close
root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
