import tkinter as tk

def calculate_wavelength(event):
    try:
        frequency = float(entry.get())
        wavelength = 300 / frequency
        output_label.config(text=str(wavelength))
    except ValueError:
        output_label.config(text="Invalid input")
    except ZeroDivisionError:
        output_label.config(text="Infinity")

def toggle_always_on_top():
    root.attributes('-topmost', always_on_top_var.get())

def update_opacity(value):
    root.attributes('-alpha', float(value))

root = tk.Tk()
root.title("Frequency to Wavelength Converter")

# Set the window size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = int(screen_width * 0.1)
window_height = int(screen_height * 0.15)
root.geometry(f"{window_width}x{window_height}")

entry = tk.Entry(root)
entry.pack()
entry.bind("<KeyRelease>", calculate_wavelength)

output_label = tk.Label(root, text="")
output_label.pack()

# Checkbox for always on top
always_on_top_var = tk.BooleanVar()
always_on_top_check = tk.Checkbutton(root, text="Always on top", var=always_on_top_var, command=toggle_always_on_top)
always_on_top_check.pack()

# Opacity slider
opacity_scale = tk.Scale(root, from_=0.1, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, label="Opacity", command=update_opacity)
opacity_scale.set(1.0)  # Set default opacity to 100%
opacity_scale.pack()

root.mainloop()
