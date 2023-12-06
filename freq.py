import tkinter as tk
from tkinter import ttk
import configparser
import sys
import os

if getattr(sys, 'frozen', False):
    # We are running in a bundle (executable)
    bundle_dir = sys._MEIPASS
else:
    # We are running in a normal Python environment
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

icon_path = os.path.join(bundle_dir, 'freq.ico')

calculation_id = None  # Global initialization
moar_live_calc_delay = None

# Configuration file path
config_file = 'config.txt'

# Load configuration
config = configparser.ConfigParser()
config.read(config_file)

def save_config():
    config['Settings'] = {
        'always_on_top': str(always_on_top_var.get()),
        'opacity': str(opacity_scale.get()),
        'window_width': str(root.winfo_width()),
        'window_height': str(root.winfo_height()),
        'ohms_live_calc': str(ohms_live_calc_enabled.get()),
        'moar_live_calc': str(moar_live_calc.get()),
        'moar_live_calc_delay': str(moar_live_calc_delay)
    }
    with open(config_file, 'w') as configfile:
        config.write(configfile)

def load_config():
    global moar_live_calc_delay
    # Check if the config file exists, if not, create it with default values
    if not os.path.exists(config_file):
        config['Settings'] = {
            'always_on_top': False,
            'opacity': 1.0,
            'window_width': int(screen_width * 0.105),
            'window_height': int(screen_height * 0.17),
            'ohms_live_calc': True,
            'moar_live_calc': True,
            'moar_live_calc_delay': 0.5
        }
        with open(config_file, 'w') as configfile:
            config.write(configfile)
    else:
        config.read(config_file)
        always_on_top_var.set(config.getboolean('Settings', 'always_on_top', fallback=False))
        opacity_scale.set(config.getfloat('Settings', 'opacity', fallback=1.0))
        window_width = config.getint('Settings', 'window_width', fallback=int(screen_width * 0.105))
        window_height = config.getint('Settings', 'window_height', fallback=int(screen_height * 0.17))
        ohms_live_calc_enabled.set(config.getboolean('Settings', 'ohms_live_calc', fallback=True))
        moar_live_calc.set(config.getboolean('Settings', 'moar_live_calc', fallback=True))
        moar_live_calc_delay = config.getfloat('Settings', 'moar_live_calc_delay', fallback=0.5)
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
    if not ohms_live_calc_enabled.get():
        return
    try:
        ohms_E = ohms_volts_entry.get()
        ohms_I = ohms_current_entry.get()
        ohms_R = ohms_resistance_entry.get()
        ohms_P = ohms_watts_entry.get()
        power_calculated = False

        # Reset background colors
        ohms_volts_entry.config(bg='white')
        ohms_current_entry.config(bg='white')
        ohms_resistance_entry.config(bg='white')
        ohms_watts_entry.config(bg='white')

        # E and I provided
        if ohms_E and ohms_I:
            ohms_R = float(ohms_E) / float(ohms_I)
            ohms_P = float(ohms_E) * float(ohms_I)
            ohms_resistance_entry.delete(0, tk.END)
            ohms_resistance_entry.insert(0, str(ohms_R))
            ohms_watts_entry.delete(0, tk.END)
            ohms_watts_entry.insert(0, str(ohms_P))
            ohms_resistance_entry.config(bg='lightgreen')
            ohms_watts_entry.config(bg='lightgreen')

        # E and R provided
        elif ohms_E and ohms_R:
            ohms_I = float(ohms_E) / float(ohms_R)
            ohms_P = (float(ohms_E) ** 2) / float(ohms_R)
            ohms_current_entry.delete(0, tk.END)
            ohms_current_entry.insert(0, str(ohms_I))
            ohms_watts_entry.delete(0, tk.END)
            ohms_watts_entry.insert(0, str(ohms_P))
            ohms_current_entry.config(bg='lightgreen')
            ohms_watts_entry.config(bg='lightgreen')

        # I and R provided
        elif ohms_I and ohms_R:
            ohms_E = float(ohms_I) * float(ohms_R)
            ohms_P = (float(ohms_I) ** 2) * float(ohms_R)
            ohms_volts_entry.delete(0, tk.END)
            ohms_volts_entry.insert(0, str(ohms_E))
            ohms_watts_entry.delete(0, tk.END)
            ohms_watts_entry.insert(0, str(ohms_P))
            ohms_volts_entry.config(bg='lightgreen')
            ohms_watts_entry.config(bg='lightgreen')

        # E and P provided
        elif ohms_E and ohms_P:
            ohms_I = float(ohms_P) / float(ohms_E)
            ohms_R = (float(ohms_E) ** 2) / float(ohms_P)
            ohms_current_entry.delete(0, tk.END)
            ohms_current_entry.insert(0, str(ohms_I))
            ohms_resistance_entry.delete(0, tk.END)
            ohms_resistance_entry.insert(0, str(ohms_R))
            ohms_current_entry.config(bg='lightgreen')
            ohms_resistance_entry.config(bg='lightgreen')

        # I and P provided
        elif ohms_I and ohms_P:
            ohms_E = float(ohms_P) / float(ohms_I)
            ohms_R = float(ohms_P) / (float(ohms_I) ** 2)
            ohms_volts_entry.delete(0, tk.END)
            ohms_volts_entry.insert(0, str(ohms_E))
            ohms_resistance_entry.delete(0, tk.END)
            ohms_resistance_entry.insert(0, str(ohms_R))
            ohms_volts_entry.config(bg='lightgreen')
            ohms_resistance_entry.config(bg='lightgreen')

        # R and P provided
        elif ohms_R and ohms_P:
            ohms_E = (float(ohms_P) * float(ohms_R)) ** 0.5
            ohms_I = (float(ohms_P) / float(ohms_R)) ** 0.5
            ohms_volts_entry.delete(0, tk.END)
            ohms_volts_entry.insert(0, str(ohms_E))
            ohms_current_entry.delete(0, tk.END)
            ohms_current_entry.insert(0, str(ohms_I))
            ohms_volts_entry.config(bg='lightgreen')
            ohms_current_entry.config(bg='lightgreen')

    except ValueError:
        # Invalid input, do nothing
        pass

def reset_ohms_law():
    ohms_volts_entry.delete(0, tk.END)
    ohms_current_entry.delete(0, tk.END)
    ohms_resistance_entry.delete(0, tk.END)
    ohms_watts_entry.delete(0, tk.END)
    ohms_volts_entry.config(bg='white')
    ohms_current_entry.config(bg='white')
    ohms_resistance_entry.config(bg='white')
    ohms_watts_entry.config(bg='white')

def calculate_power_parameters():
    global calculation_id  # Declare calculation_id as global
    if not moar_live_calc.get():
        return
    # Check if at least one of the other fields has a value
    if not (pwr_peak_entry.get() or pwr_pep_entry.get() or pwr_rms_entry.get() or pwr_p_to_p_entry.get()):
        return  # Do not schedule calculation if all other fields are empty
    # Cancel previous scheduled calculation if any
    if calculation_id is not None:
        root.after_cancel(calculation_id)
    # Schedule a new calculation
    calculation_id = root.after(int(moar_live_calc_delay * 1000), perform_power_calculation)

def perform_power_calculation():
    if not moar_live_calc.get():
        return

    try:
        pwr_Vp = float(pwr_peak_entry.get()) if pwr_peak_entry.get() else None
        pwr_PEP = float(pwr_pep_entry.get()) if pwr_pep_entry.get() else None
        pwr_Vrms = float(pwr_rms_entry.get()) if pwr_rms_entry.get() else None
        pwr_Vpp = float(pwr_p_to_p_entry.get()) if pwr_p_to_p_entry.get() else None
        pwr_R = float(pwr_resistance_entry.get()) if pwr_resistance_entry.get() else 50

        # Reset background colors
        pwr_peak_entry.config(bg='white')
        pwr_pep_entry.config(bg='white')
        pwr_rms_entry.config(bg='white')
        pwr_p_to_p_entry.config(bg='white')

        # Calculate based on the provided values
        if pwr_Vp is not None:
            pwr_Vrms = pwr_Vp * 0.707
            pwr_Vpp = pwr_Vp * 2
            pwr_PEP = (pwr_Vrms ** 2) / pwr_R
        elif pwr_Vrms is not None:
            pwr_Vp = pwr_Vrms / 0.707
            pwr_Vpp = pwr_Vp * 2
            pwr_PEP = (pwr_Vrms ** 2) / pwr_R
        elif pwr_PEP is not None:
            pwr_Vrms = (pwr_PEP * pwr_R) ** 0.5
            pwr_Vp = pwr_Vrms / 0.707
            pwr_Vpp = pwr_Vp * 2
        elif pwr_Vpp is not None:
            pwr_Vp = pwr_Vpp / 2
            pwr_Vrms = pwr_Vp * 0.707
            pwr_PEP = (pwr_Vrms ** 2) / pwr_R

        # Update the fields
        pwr_peak_entry.delete(0, tk.END)
        pwr_peak_entry.insert(0, str(pwr_Vp))
        pwr_pep_entry.delete(0, tk.END)
        pwr_pep_entry.insert(0, str(pwr_PEP))
        pwr_rms_entry.delete(0, tk.END)
        pwr_rms_entry.insert(0, str(pwr_Vrms))
        pwr_p_to_p_entry.delete(0, tk.END)
        pwr_p_to_p_entry.insert(0, str(pwr_Vpp))

    except ValueError:
        # Handle invalid input
        pass


def reset_power_fields():
    pwr_peak_entry.delete(0, tk.END)
    pwr_pep_entry.delete(0, tk.END)
    pwr_rms_entry.delete(0, tk.END)
    pwr_p_to_p_entry.delete(0, tk.END)
    pwr_resistance_entry.delete(0, tk.END)
    pwr_resistance_entry.insert(0, "50")  # Reset to default value
    pwr_peak_entry.config(bg='white')
    pwr_pep_entry.config(bg='white')
    pwr_rms_entry.config(bg='white')
    pwr_p_to_p_entry.config(bg='white')
    pwr_resistance_entry.config(bg='white')

def calculate_rcl():
    # Process the entries for R, C, and L
    r_values = [float(val.strip()) for val in rcl_r_entry.get().replace(',', '').split(';') if val]
    c_values = [float(val.strip()) for val in rcl_c_entry.get().replace(',', '').split(';') if val]
    l_values = [float(val.strip()) for val in rcl_l_entry.get().replace(',', '').split(';') if val]

    # Perform calculations based on series/parallel selection
    if rcl_series_parallel_var.get() == "series":
        # Series calculations
        r_total = sum(r_values)
        c_total = 1 / sum([1 / c for c in c_values if c != 0]) if c_values else 0
        l_total = sum(l_values)
    else:
        # Parallel calculations
        r_total = 1 / sum([1 / r for r in r_values if r != 0]) if r_values else 0
        c_total = sum(c_values)
        l_total = 1 / sum([1 / l for l in l_values if l != 0]) if l_values else 0

    # Update the display with calculated values
    conversion_output.config(text=f"R: {r_total}, C: {c_total}, L: {l_total}")

# Function to handle unit conversion
def convert_units():
    # Conversion logic
    unit_factors = {
        "giga": 1e9, "mega": 1e6, "kilo": 1e3, "base": 1,
        "milli": 1e-3, "micro": 1e-6, "nano": 1e-9, "pico": 1e-12
    }
    base_value = float(unit_conversion_entry.get()) * unit_factors[unit_prefix_var.get()]
    converted_values = {k: base_value / v for k, v in unit_factors.items()}
    conversion_text = ", ".join([f"{k}: {v:.3g}" for k, v in converted_values.items()])
    rcl_results_label.config(text=f"Converted values: {conversion_text}")



# Function to toggle always on top
def toggle_always_on_top():
    root.attributes('-topmost', always_on_top_var.get())

# Function to update opacity
def update_opacity(value):
    root.attributes('-alpha', float(value))

def reset_window_size():
    root.geometry(f"{int(screen_width * 0.105)}x{int(screen_height * 0.30)}")

def on_close():
    save_config()
    root.destroy()

root = tk.Tk()
root.title("Ham Companion")
root.iconbitmap(icon_path)

# Set the window size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = int(screen_width * 0.105)
window_height = int(screen_height * 0.30)
root.geometry(f"{window_width}x{window_height}")
style = ttk.Style(root)
style.configure('bottomtab.TNotebook', tabposition='sw')

# Create the tab control
tab_control = ttk.Notebook(root, style='bottomtab.TNotebook')



# =========================================================================================
# =========================================================================================
# Frequency Tab     =======================================================================
# =========================================================================================
# =========================================================================================
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



# =========================================================================================
# =========================================================================================
# Ohm's Law Tab     =======================================================================
# =========================================================================================
# =========================================================================================
ohms_tab = ttk.Frame(tab_control)
tab_control.add(ohms_tab, text='Ohms')
# Add Ohm's Law widgets here

# Voltage (E)
volts_label = tk.Label(ohms_tab, text="E (Volts):")
volts_label.pack(side=tk.TOP, anchor='w', padx=10)
ohms_volts_entry = tk.Entry(ohms_tab)
ohms_volts_entry.pack(side=tk.TOP, anchor='w', padx=10)
ohms_volts_entry.bind("<KeyRelease>", lambda event: calculate_ohms_law_and_power())

# Current (I)
current_label = tk.Label(ohms_tab, text="I (Current):")
current_label.pack(side=tk.TOP, anchor='w', padx=10)
ohms_current_entry = tk.Entry(ohms_tab)
ohms_current_entry.pack(side=tk.TOP, anchor='w', padx=10)
ohms_current_entry.bind("<KeyRelease>", lambda event: calculate_ohms_law_and_power())

# Resistance (R)
resistance_label = tk.Label(ohms_tab, text="R (Resistance):")
resistance_label.pack(side=tk.TOP, anchor='w', padx=10)
ohms_resistance_entry = tk.Entry(ohms_tab)
ohms_resistance_entry.pack(side=tk.TOP, anchor='w', padx=10)
ohms_resistance_entry.bind("<KeyRelease>", lambda event: calculate_ohms_law_and_power())

ohms_volts_entry.bind("<KeyRelease>", lambda event: calculate_ohms_law_and_power())
ohms_current_entry.bind("<KeyRelease>", lambda event: calculate_ohms_law_and_power())
ohms_resistance_entry.bind("<KeyRelease>", lambda event: calculate_ohms_law_and_power())

# Watts (P)
watts_label = tk.Label(ohms_tab, text="P (Watts):")
watts_label.pack(side=tk.TOP, anchor='w', padx=10)
ohms_watts_entry = tk.Entry(ohms_tab)
ohms_watts_entry.pack(side=tk.TOP, anchor='w', padx=10)
ohms_watts_entry.bind("<KeyRelease>", lambda event: calculate_ohms_law_and_power())

# Reset button (centered)
reset_button = tk.Button(ohms_tab, text="Reset", command=reset_ohms_law)
reset_button.pack(side=tk.LEFT, padx=10, pady=5, anchor='s')

# Global variable to track the state of live calculation
ohms_live_calc_enabled = tk.BooleanVar(value=True)

# Checkbox for live calculation
ohms_live_calc_checkbox = tk.Checkbutton(ohms_tab, text="Live Calc", var=ohms_live_calc_enabled)
ohms_live_calc_checkbox.pack(side=tk.RIGHT, padx=10, pady=5, anchor='s')



# =========================================================================================
# =========================================================================================
# MOAR Power Tab        ===================================================================
# =========================================================================================
# =========================================================================================
power_tab = ttk.Frame(tab_control)
tab_control.add(power_tab, text='Moar Pwr')

# Create input fields for Peak, PEP, RMS, P to P, and Resistance
tk.Label(power_tab, text="Peak Voltage:").pack(side=tk.TOP, anchor='w', padx=10)
pwr_peak_entry = tk.Entry(power_tab)
pwr_peak_entry.pack(side=tk.TOP, anchor='w', padx=10)
pwr_peak_entry.bind("<KeyRelease>", lambda event: calculate_power_parameters())

tk.Label(power_tab, text="PEP:").pack(side=tk.TOP, anchor='w', padx=10)
pwr_pep_entry = tk.Entry(power_tab)
pwr_pep_entry.pack(side=tk.TOP, anchor='w', padx=10)
pwr_pep_entry.bind("<KeyRelease>", lambda event: calculate_power_parameters())

tk.Label(power_tab, text="RMS:").pack(side=tk.TOP, anchor='w', padx=10)
pwr_rms_entry = tk.Entry(power_tab)
pwr_rms_entry.pack(side=tk.TOP, anchor='w', padx=10)
pwr_rms_entry.bind("<KeyRelease>", lambda event: calculate_power_parameters())

tk.Label(power_tab, text="Peak-to-Peak Voltage:").pack(side=tk.TOP, anchor='w', padx=10)
pwr_p_to_p_entry = tk.Entry(power_tab)
pwr_p_to_p_entry.pack(side=tk.TOP, anchor='w', padx=10)
pwr_p_to_p_entry.bind("<KeyRelease>", lambda event: calculate_power_parameters())

tk.Label(power_tab, text="Resistance:").pack(side=tk.TOP, anchor='w', padx=10)
pwr_resistance_entry = tk.Entry(power_tab)
pwr_resistance_entry.insert(0, "50")  # Default value
pwr_resistance_entry.pack(side=tk.TOP, anchor='w', padx=10)
pwr_resistance_entry.bind("<KeyRelease>", lambda event: calculate_power_parameters() if (pwr_peak_entry.get() or pwr_pep_entry.get() or pwr_rms_entry.get() or pwr_p_to_p_entry.get()) else None)

# Live calculation checkbox
moar_live_calc = tk.BooleanVar(value=True)
moar_live_calc_checkbox = tk.Checkbutton(power_tab, text="Live Calc", var=moar_live_calc)
moar_live_calc_checkbox.pack(side=tk.RIGHT, padx=10, pady=5, anchor='s')

# Reset button
reset_button = tk.Button(power_tab, text="Reset", command=reset_power_fields)
reset_button.pack(side=tk.LEFT, padx=10, pady=5, anchor='s')



# =========================================================================================
# =========================================================================================
# # R-C-L Tab       =======================================================================
# =========================================================================================
# =========================================================================================
rcl_tab = ttk.Frame(tab_control)
tab_control.add(rcl_tab, text='R-C-L')

# Input Fields with Labels
tk.Label(rcl_tab, text="Resistor (R):").pack(side=tk.TOP, anchor='w', padx=10)
rcl_r_entry = tk.Entry(rcl_tab)
rcl_r_entry.pack(side=tk.TOP, anchor='w', padx=10)

tk.Label(rcl_tab, text="Capacitor (C):").pack(side=tk.TOP, anchor='w', padx=10)
rcl_c_entry = tk.Entry(rcl_tab)
rcl_c_entry.pack(side=tk.TOP, anchor='w', padx=10)

tk.Label(rcl_tab, text="Inductor (L):").pack(side=tk.TOP, anchor='w', padx=10)
rcl_l_entry = tk.Entry(rcl_tab)
rcl_l_entry.pack(side=tk.TOP, anchor='w', padx=10)

# Radio Buttons for Series/Parallel
rcl_series_parallel_var = tk.StringVar(value="series")
series_radio = tk.Radiobutton(rcl_tab, text="Series", variable=rcl_series_parallel_var, value="series")
series_radio.pack(side=tk.TOP, anchor='w', padx=10)
parallel_radio = tk.Radiobutton(rcl_tab, text="Parallel", variable=rcl_series_parallel_var, value="parallel")
parallel_radio.pack(side=tk.TOP, anchor='w', padx=10)

# Calculate Button
calc_button = tk.Button(rcl_tab, text="Calculate", command=calculate_rcl)
calc_button.pack(side=tk.TOP, pady=10)

# Results Label
rcl_results_label = tk.Label(rcl_tab, text="")
rcl_results_label.pack(side=tk.TOP, pady=10)

# Conversion Section
tk.Label(rcl_tab, text="Convert Value:").pack(side=tk.TOP, anchor='w', padx=10)
unit_conversion_entry = tk.Entry(rcl_tab)
unit_conversion_entry.pack(side=tk.TOP, anchor='w', padx=10)

# Dropdown and Convert Button Side by Side
unit_factors = {
    "giga": 1e9, "mega": 1e6, "kilo": 1e3, "base": 1,
    "milli": 1e-3, "micro": 1e-6, "nano": 1e-9, "pico": 1e-12
}
unit_prefix_var = tk.StringVar(value="base")
unit_dropdown = ttk.Combobox(rcl_tab, textvariable=unit_prefix_var, values=unit_factors)
unit_dropdown.pack(side=tk.LEFT, padx=5)

convert_button = tk.Button(rcl_tab, text="Convert", command=convert_units)
convert_button.pack(side=tk.LEFT, padx=5)

# Conversion Output with Text Wrapping
conversion_output = tk.Text(rcl_tab, height=4, wrap='word')
conversion_output.pack(side=tk.TOP, padx=10, pady=10)
conversion_output.config(state=tk.DISABLED)



# =========================================================================================
# =========================================================================================
# Settings Tab      =======================================================================
# =========================================================================================
# =========================================================================================
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
reset_size_button = tk.Button(settings_tab, text="Reset Window Size", command=reset_window_size)
reset_size_button.pack()

tab_control.pack(expand=1, fill="both")

# Load config and apply settings
load_config()

# Save config on close
root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
