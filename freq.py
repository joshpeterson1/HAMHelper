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
        'opacity': opacity_scale.get(),
        'window_width': root.winfo_width(),
        'window_height': root.winfo_height()
    }
    with open(config_file, 'w') as configfile:
        config.write(configfile)

def load_config():
    # Check if the config file exists, if not, create it with default values
    if not os.path.exists(config_file):
        config['Settings'] = {
            'always_on_top': False,
            'opacity': 1.0,
            'window_width': int(screen_width * 0.105),
            'window_height': int(screen_height * 0.17)
        }
        with open(config_file, 'w') as configfile:
            config.write(configfile)
    else:
        config.read(config_file)
        always_on_top_var.set(config.getboolean('Settings', 'always_on_top', fallback=False))
        opacity_scale.set(config.getfloat('Settings', 'opacity', fallback=1.0))
        window_width = config.getint('Settings', 'window_width', fallback=int(screen_width * 0.105))
        window_height = config.getint('Settings', 'window_height', fallback=int(screen_height * 0.17))
        root.geometry(f"{window_width}x{window_height}")
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

# Function to calculate Ohm's Law
def calculate_ohms_law_and_power(): 
    try:
        E = volts_entry.get()
        I = current_entry.get()
        R = resistance_entry.get()
        P = watts_entry.get()
        power_calculated = False

        # Reset background colors
        volts_entry.config(bg='white')
        current_entry.config(bg='white')
        resistance_entry.config(bg='white')
        watts_entry.config(bg='white')

        # E and I provided
        if E and I:
            R = float(E) / float(I)
            P = float(E) * float(I)
            resistance_entry.delete(0, tk.END)
            resistance_entry.insert(0, str(R))
            watts_entry.delete(0, tk.END)
            watts_entry.insert(0, str(P))
            resistance_entry.config(bg='lightgreen')
            watts_entry.config(bg='lightgreen')

        # E and R provided
        elif E and R:
            I = float(E) / float(R)
            P = (float(E) ** 2) / float(R)
            current_entry.delete(0, tk.END)
            current_entry.insert(0, str(I))
            watts_entry.delete(0, tk.END)
            watts_entry.insert(0, str(P))
            current_entry.config(bg='lightgreen')
            watts_entry.config(bg='lightgreen')

        # I and R provided
        elif I and R:
            E = float(I) * float(R)
            P = (float(I) ** 2) * float(R)
            volts_entry.delete(0, tk.END)
            volts_entry.insert(0, str(E))
            watts_entry.delete(0, tk.END)
            watts_entry.insert(0, str(P))
            volts_entry.config(bg='lightgreen')
            watts_entry.config(bg='lightgreen')

        # E and P provided
        elif E and P:
            I = float(P) / float(E)
            R = (float(E) ** 2) / float(P)
            current_entry.delete(0, tk.END)
            current_entry.insert(0, str(I))
            resistance_entry.delete(0, tk.END)
            resistance_entry.insert(0, str(R))
            current_entry.config(bg='lightgreen')
            resistance_entry.config(bg='lightgreen')

        # I and P provided
        elif I and P:
            E = float(P) / float(I)
            R = float(P) / (float(I) ** 2)
            volts_entry.delete(0, tk.END)
            volts_entry.insert(0, str(E))
            resistance_entry.delete(0, tk.END)
            resistance_entry.insert(0, str(R))
            volts_entry.config(bg='lightgreen')
            resistance_entry.config(bg='lightgreen')

        # R and P provided
        elif R and P:
            E = (float(P) * float(R)) ** 0.5
            I = (float(P) / float(R)) ** 0.5
            volts_entry.delete(0, tk.END)
            volts_entry.insert(0, str(E))
            current_entry.delete(0, tk.END)
            current_entry.insert(0, str(I))
            volts_entry.config(bg='lightgreen')
            current_entry.config(bg='lightgreen')

    except ValueError:
        # Invalid input, do nothing
        pass

def reset_ohms_law():
    volts_entry.delete(0, tk.END)
    current_entry.delete(0, tk.END)
    resistance_entry.delete(0, tk.END)
    watts_entry.delete(0, tk.END)
    volts_entry.config(bg='white')
    current_entry.config(bg='white')
    resistance_entry.config(bg='white')
    watts_entry.config(bg='white')

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
root.title("Ham Companion")
root.iconbitmap('freq.ico')  # Set the window icon

# Set the window size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = int(screen_width * 0.105)
window_height = int(screen_height * 0.17)
root.geometry(f"{window_width}x{window_height}")
style = ttk.Style(root)
style.configure('bottomtab.TNotebook', tabposition='sw')

# Create the tab control
tab_control = ttk.Notebook(root, style='bottomtab.TNotebook')

# Frequency Tab
freq_tab = ttk.Frame(tab_control)
tab_control.add(freq_tab, text='Freq')
freq_entry = tk.Entry(freq_tab)
freq_entry.pack(pady=5)  # Add vertical padding
freq_entry.bind("<KeyRelease>", calculate_wavelength)

freq_output_label = tk.Label(freq_tab, text="Input")
freq_output_label.pack()

# Instructional text with rich formatting using Text widget
instruction_text = tk.Text(freq_tab, height=3, wrap='word', borderwidth=0)
instruction_text.tag_configure("italic_underline", font=("Arial", 10, "italic underline"))
instruction_text.insert(tk.END, "Enter Freq ")
instruction_text.insert(tk.END, "in MHz", "italic_underline")
instruction_text.insert(tk.END, " to see approx bandwidth ")
instruction_text.insert(tk.END, "in meters", "italic_underline")
instruction_text.insert(tk.END, " or vice versa.")
instruction_text.config(state=tk.DISABLED)  # Make the text widget read-only
instruction_text.pack(pady=(10, 0))


# Ohm's Law Tab
ohms_tab = ttk.Frame(tab_control)
tab_control.add(ohms_tab, text='Ohms Law')
# Add Ohm's Law widgets here

# Voltage (E)
volts_label = tk.Label(ohms_tab, text="E (Volts):")
volts_label.pack(side=tk.TOP, anchor='w')
volts_entry = tk.Entry(ohms_tab)
volts_entry.pack(side=tk.TOP, anchor='w')
volts_entry.bind("<KeyRelease>", lambda event: calculate_ohms_law_and_power())

# Current (I)
current_label = tk.Label(ohms_tab, text="I (Current):")
current_label.pack(side=tk.TOP, anchor='w')
current_entry = tk.Entry(ohms_tab)
current_entry.pack(side=tk.TOP, anchor='w')
current_entry.bind("<KeyRelease>", lambda event: calculate_ohms_law_and_power())

# Resistance (R)
resistance_label = tk.Label(ohms_tab, text="R (Resistance):")
resistance_label.pack(side=tk.TOP, anchor='w')
resistance_entry = tk.Entry(ohms_tab)
resistance_entry.pack(side=tk.TOP, anchor='w')
resistance_entry.bind("<KeyRelease>", lambda event: calculate_ohms_law_and_power())

volts_entry.bind("<KeyRelease>", lambda event: calculate_ohms_law_and_power())
current_entry.bind("<KeyRelease>", lambda event: calculate_ohms_law_and_power())
resistance_entry.bind("<KeyRelease>", lambda event: calculate_ohms_law_and_power())

# Watts (P)
watts_label = tk.Label(ohms_tab, text="P (Watts):")
watts_label.pack(side=tk.TOP, anchor='w')
watts_entry = tk.Entry(ohms_tab)
watts_entry.pack(side=tk.TOP, anchor='w')
watts_entry.bind("<KeyRelease>", lambda event: calculate_ohms_law_and_power())

# Reset button (centered)
reset_button = tk.Button(ohms_tab, text="Reset", command=reset_ohms_law)
reset_button.pack(side=tk.LEFT, padx=10)



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
