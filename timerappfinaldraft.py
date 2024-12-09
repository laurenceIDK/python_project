from tkinter import *
import time
from tkinter import simpledialog
from tkinter import messagebox
import os

# Initialize the main application window
root = Tk()
root.title("Timer App")
root.geometry("500x700")
root.config(bg="#FAF3E0")
root.resizable(False, False)

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

Label(root, font=("arial", 20, "bold"), text="Timer", bg="#FAF3E0", fg="#333333").pack(pady=10)
current_time = Label(root, font=("arial", 15, "bold"), text="", fg="#333333", bg="#FAF3E0", width=12)
current_time.pack(pady=5)
clock()

# Timer input fields
timer_frame = Frame(root, bg="#FAF3E0")
timer_frame.pack(pady=20)
Entry(timer_frame, textvariable=hrs, width=2, font="arial 50", bg="#FAF3E0", fg="#333333", bd=0).grid(row=0, column=0, padx=10)
Entry(timer_frame, textvariable=mins, width=2, font="arial 50", bg="#FAF3E0", fg="#333333", bd=0).grid(row=0, column=1, padx=10)
Entry(timer_frame, textvariable=secs, width=2, font="arial 50", bg="#FAF3E0", fg="#333333", bd=0).grid(row=0, column=2, padx=10)
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
        root.after(1000, lambda: countdown(time_left - 1))

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
    remark = simpledialog.askstring("Save Timer", "Enter timer remark:")
    if remark:
        with open(timers_file, "a") as file:
            file.write(f"{remark}:{hrs.get()}:{mins.get()}:{secs.get()}\n")
        load_saved_timers()

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
            Button(
                saved_timers_frame,
                text=remark,
                bg="#ea3548",
                fg="#fff",
                command=lambda h=h, m=m, s=s: load_timer(h, m, s)
            ).pack(pady=2)
        except ValueError:
            continue

def load_timer(h, m, s):
    hrs.set(h)
    mins.set(m)
    secs.set(s)

# Presets area
saved_timers_frame = Frame(root, bg="#FAF3E0")
saved_timers_frame.pack(pady=10)
load_saved_timers()

# Buttons
button_frame = Frame(root, bg="#FAF3E0")
button_frame.pack(pady=20)
Button(button_frame, text="Start", bg="#A1CDA8", fg="#333333", width=10, height=2, command=start_timer).grid(row=0, column=0, padx=5)
Button(button_frame, text="Pause", bg="#FFABAB", fg="#333333", width=10, height=2, command=pause_timer).grid(row=0, column=1, padx=5)
Button(button_frame, text="Reset", bg="#FFD6A5", fg="#333333", width=10, height=2, command=reset_timer).grid(row=0, column=2, padx=5)
Button(button_frame, text="Save Timer", bg="#FFE6A7", fg="#333333", width=10, height=2, command=save_timer).grid(row=0, column=3, padx=5)

root.mainloop()
