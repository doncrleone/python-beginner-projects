import tkinter as tk
from tkinter import ttk, messagebox
from math import sin, cos, pi


def update_clock():
    try:
        # Get the current time in seconds
        current_time = time_var.get()
        seconds = current_time % 60
        minutes = (current_time // 60) % 60
        hours = (current_time // 3600) % 12

        # Calculate angles for clock hands
        seconds_angle = 90 - seconds * 6
        minutes_angle = 90 - minutes * 6 - seconds * 0.1
        hours_angle = 90 - (hours * 30 + minutes * 0.5)

        # Clear the canvas for redrawing
        canvas.delete("all")

        # Center and radius for the clock face
        center_x, center_y = canvas.winfo_width() // 2, canvas.winfo_height() // 2
        radius = 100

        # Draw clock face
        canvas.create_oval(center_x - radius, center_y - radius,
                           center_x + radius, center_y + radius)

        # Draw clock numbers
        for i in range(1, 13):
            angle = 90 - i * 30
            x = center_x + radius * 0.85 * cos(angle * (pi / 180))
            y = center_y - radius * 0.85 * sin(angle * (pi / 180))
            canvas.create_text(x, y, text=str(i), font=("Arial", 12, "bold"))

        # Draw clock hands
        draw_hand(center_x, center_y, seconds_angle, radius * 0.8, 1)  # Second hand
        draw_hand(center_x, center_y, minutes_angle, radius * 0.7, 2)  # Minute hand
        draw_hand(center_x, center_y, hours_angle, radius * 0.5, 4)    # Hour hand

        # Update the time
        time_var.set(current_time + 1)

        # Schedule the next update
        root.after(1000, update_clock)
    except Exception as e:
        print(f"Error in update_clock: {e}")  # Print any errors to help debugging


def draw_hand(center_x, center_y, angle, length, width):
    try:
        radian_angle = angle * (pi / 180)
        end_x = center_x + length * cos(radian_angle)
        end_y = center_y - length * sin(radian_angle)
        canvas.create_line(center_x, center_y, end_x, end_y, width=width)
    except Exception as e:
        print(f"Error in draw_hand: {e}")  # Print any errors to help debugging")


def set_alarm():
    global alarm_time
    # Get selected hour and minute
    alarm_hour = hour_combobox.get()
    alarm_minute = minute_combobox.get()

    if not alarm_hour or not alarm_minute:
        messagebox.showerror("Invalid Input", "Please select both hour and minute.")
        return

    alarm_time = f"{int(alarm_hour):02}:{int(alarm_minute):02}"
    messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_time}.")


def check_alarm(current_hour, current_minute):
    global alarm_time
    if alarm_time:
        alarm_hour, alarm_minute = map(int, alarm_time.split(":"))
        if alarm_hour == current_hour and alarm_minute == current_minute:
            messagebox.showwarning("Alarm!", "Time's up!")
            alarm_time = None  # Reset the alarm after it triggers


# Initialize the main Tkinter window
root = tk.Tk()
root.title("Analog Clock with Alarm")

# Create a canvas for drawing the clock
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Alarm input fields with dropdowns
alarm_label = tk.Label(root, text="Set Alarm:")
alarm_label.pack()

frame = tk.Frame(root)
frame.pack()

# Dropdown for selecting hours
hour_combobox = ttk.Combobox(frame, values=[f"{i:02}" for i in range(12)], width=5)
hour_combobox.set("10")  # Default to 10 AM
hour_combobox.pack(side="left")

# Separator (colon)
separator = tk.Label(frame, text=":")
separator.pack(side="left")

# Dropdown for selecting minutes
minute_combobox = ttk.Combobox(frame, values=[f"{i:02}" for i in range(60)], width=5)
minute_combobox.set("00")  # Default to :00
minute_combobox.pack(side="left")

# Set alarm button
set_alarm_button = tk.Button(root, text="Set Alarm", command=set_alarm)
set_alarm_button.pack()

# Initialize alarm time and time variable
alarm_time = None
time_var = tk.IntVar()
time_var.set(10 * 3600)  # Start the clock at 10:00:00 AM

# Start the clock update
update_clock()

# Start the Tkinter main loop
root.mainloop()
