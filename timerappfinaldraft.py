import time
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
import os

# Initialize the main application window
win = Tk()
win.title("Timer App")
win.geometry("500x700")
win.config(bg="#FAF3E0")
win.resizable(False, False)

# Variables
hrs = StringVar(value="00")
mins = StringVar(value="00")
secs = StringVar(value="00")
timer_running = False
paused_time = 0
timers_file = "timers.txt"

# Clock display
def clock():
    clock_time = time.strftime('%H:%M:%S %p')
    current_time.config(text=clock_time)
    current_time.after(1000, clock)

Label(win, font=("arial", 20, "bold"), text="Timer", bg="#FAF3E0", fg="#333333").pack(pady=10)
current_time = Label(win, font=("arial", 15, "bold"), text="", fg="#333333", bg="#FAF3E0", width=12)
current_time.pack(pady=5)
clock()

#function for validating input (only integers and max 99 for hours, 59 for minutes and seconds)
def validate_input(newInput, field):
    if newInput.isdigit() and len(newInput) <= 2:
        if field == 'hrs':
            return int(newInput) <= 99
        elif field in ['mins', 'secs']:
            return int(newInput) <= 59
    return newInput == ""

# Timer input fields
vcmd_hrs = (win.register(lambda newInput: validate_input(newInput, 'hrs')), "%P")
vcmd_mins_secs = (win.register(lambda newInput: validate_input(newInput, 'mins')), "%P")

timer_frame = Frame(win, bg="#FAF3E0")
timer_frame.pack(pady=20)
Entry(timer_frame, textvariable=hrs, width=2, font="arial 50", bg="#FAF3E0", fg="#333333", bd=0, validate = "key", validatecommand = vcmd_hrs).grid(row=0, column=0, padx=10)
Entry(timer_frame, textvariable=mins, width=2, font="arial 50", bg="#FAF3E0", fg="#333333", bd=0, validate = "key", validatecommand = vcmd_mins_secs).grid(row=0, column=1, padx=10)
Entry(timer_frame, textvariable=secs, width=2, font="arial 50", bg="#FAF3E0", fg="#333333", bd=0, validate = "key", validatecommand = vcmd_mins_secs).grid(row=0, column=2, padx=10)
Label(timer_frame, text="hours", font="arial 12", bg="#FAF3E0", fg="#333333").grid(row=1, column=0)
Label(timer_frame, text="mins", font="arial 12", bg="#FAF3E0", fg="#333333").grid(row=1, column=1)
Label(timer_frame, text="secs", font="arial 12", bg="#FAF3E0", fg="#333333").grid(row=1, column=2)

# Timer functionality
def timer_alert():
    messagebox.showinfo("Time's Up", "The timer has finished!")

def start_timer():
    global timer_running, paused_time
    if not timer_running:
        timer_running = True
        countdown(int(hrs.get()) * 3600 + int(mins.get()) * 60 + int(secs.get()))

def countdown(time_left):
    global timer_running, paused_time
    if time_left < 0 or not timer_running:
        timer_running = False
        return

    hrs.set(f"{time_left // 3600:02}")
    mins.set(f"{(time_left % 3600) // 60:02}")
    secs.set(f"{time_left % 60:02}")

    if time_left == 0:
        timer_alert()  # Trigger alert
    else:
        win.after(1000, lambda: countdown(time_left - 1))

def pause_timer():
    global timer_running, paused_time
    if timer_running:
        paused_time = int(hrs.get()) * 3600 + int(mins.get()) * 60 + int(secs.get())
        timer_running = False

def reset_timer():
    global timer_running
    timer_running = False
    hrs.set("00"), mins.set("00"), secs.set("00")

# Save and load timers
def save_timer():
    # Check the number of saved timers
    if os.path.exists(timers_file):
        with open(timers_file, "r") as file:
            lines = file.readlines()

        if len(lines) >= 6:  # Limit to 6 timers
            messagebox.showwarning("Limit Reached", "You can only save up to 6 timers. Please delete one of the timers before you can save another.")
            return

    # Ask for remark and save the timer
    remark = simpledialog.askstring("Save Timer", "Enter timer remark:")
    if remark:
        with open(timers_file, "a") as file:
            file.write(f"{remark}:{hrs.get()}:{mins.get()}:{secs.get()}\n")
        load_saved_timers()

def delete_timer(timer_line):
    if os.path.exists(timers_file):
        with open(timers_file, "r") as file:
            lines = file.readlines()

        with open(timers_file, "w") as file:
            for line in lines:
                if line.strip() != timer_line.strip():
                    file.write(line)

    load_saved_timers()  # Reloads the Saved timers

def load_saved_timers():
    if not os.path.exists(timers_file):
        return

    with open(timers_file, "r") as file:
        lines = file.readlines()

    for widget in saved_timers_frame.winfo_children():
        widget.destroy()

    for line in lines:
        try:
            remark, h, m, s = line.strip().split(":")
            timer_frame = Frame(saved_timers_frame, bg="#000")
            timer_frame.pack(pady=2, fill=X)

            # Timer Button (uniform size)
            Button(timer_frame, text=remark, bg="#ea3548", fg="#fff",
                   width=15, height=2,  # Set button size
                   command=lambda h=h, m=m, s=s: load_timer(h, m, s)).pack(side=LEFT, padx=5)

            # Delete Button
            Button(timer_frame, text="Delete", bg="#ff0000", fg="#fff",
                   width=8, height=2,  # Set button size
                   command=lambda line=line: delete_timer(line)).pack(side=LEFT, padx=5)
        except ValueError:
            continue


def load_timer(h, m, s):
    hrs.set(h)
    mins.set(m)
    secs.set(s)

# Presets area
saved_timers_frame = Frame(win, bg="#FAF3E0")
saved_timers_frame.pack(pady=10)
load_saved_timers()

# Buttons
button_frame = Frame(win, bg="#FAF3E0")
button_frame.pack(pady=20)
Button(button_frame, text="Start", font=("arial", 9, "bold"), bg="#A1CDA8", fg="#333333", width=10, height=2, command=start_timer).grid(row=0, column=0, padx=5)
Button(button_frame, text="Pause", font=("arial", 9, "bold"), bg="#FFABAB", fg="#333333", width=10, height=2, command=pause_timer).grid(row=0, column=1, padx=5)
Button(button_frame, text="Reset", font=("arial", 9, "bold"), bg="#FFD6A5", fg="#333333", width=10, height=2, command=reset_timer).grid(row=0, column=2, padx=5)
Button(button_frame, text="Save Timer", font=("arial", 9, "bold"), bg="#FFE6A7", fg="#333333", width=10, height=2, command=save_timer).grid(row=0, column=3, padx=5)

win.mainloop()
