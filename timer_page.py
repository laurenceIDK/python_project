from tkinter import *
from tkinter import simpledialog, messagebox
import time
import os

class timerrun:
    def __init__(self, root):
        # Initialize the main application window
        self.root = root
        self.root.title('Timer App')
        self.root.geometry('500x500+500+90')
        self.root.config(bg='#FAF3E0')
        self.root.resizable(False, False)

        # Variables
        self.hrs = StringVar(value="00")
        self.mins = StringVar(value="00")
        self.secs = StringVar(value="00")
        self.timer_running = False
        self.paused_time = 0
        self.timers_file = "timers.txt"

        try:
            open('timers.txt', 'r')
        except FileNotFoundError:
            messagebox.showerror("Error", "Timers file not found. A new file created.")
            with open('timers.txt', 'w') as file:
                file.write("")


        Label(root, font=("arial", 20, "bold"), text="Timer", bg="#FAF3E0", fg="#333333").pack(pady=10)
        self.current_time = Label(root, font=("arial", 15, "bold"), text="", fg="#333333", bg="#FAF3E0", width=12)
        self.current_time.pack(pady=5)
        self.clock()

        # Timer input fields
        timer_frame = Frame(root, bg="#FAF3E0")
        timer_frame.pack(pady=20)
        Entry(timer_frame, textvariable=self.hrs, width=2, font="arial 50", bg="#FAF3E0", fg="#333333", bd=0).grid(row=0, column=0, padx=10)
        Entry(timer_frame, textvariable=self.mins, width=2, font="arial 50", bg="#FAF3E0", fg="#333333", bd=0).grid(row=0, column=1, padx=10)
        Entry(timer_frame, textvariable=self.secs, width=2, font="arial 50", bg="#FAF3E0", fg="#333333", bd=0).grid(row=0, column=2, padx=10)
        Label(timer_frame, text="hours", font="arial 12", bg="#FAF3E0", fg="#333333").grid(row=1, column=0)
        Label(timer_frame, text="mins", font="arial 12", bg="#FAF3E0", fg="#333333").grid(row=1, column=1)
        Label(timer_frame, text="secs", font="arial 12", bg="#FAF3E0", fg="#333333").grid(row=1, column=2)

        # Presets area
        self.saved_timers_frame = Frame(root, bg="#FAF3E0")
        self.saved_timers_frame.pack(pady=10)
        self.load_saved_timers()

        # Buttons
        button_frame = Frame(root, bg="#FAF3E0")
        button_frame.pack(pady=20)
        Button(button_frame, text="Start", bg="#A1CDA8", fg="#333333", width=10, height=2, command=self.start_timer).grid(row=0, column=0, padx=5)
        Button(button_frame, text="Pause", bg="#FFABAB", fg="#333333", width=10, height=2, command=self.pause_timer).grid(row=0, column=1, padx=5)
        Button(button_frame, text="Reset", bg="#FFD6A5", fg="#333333", width=10, height=2, command=self.reset_timer).grid(row=0, column=2, padx=5)
        Button(button_frame, text="Save Timer", bg="#FFE6A7", fg="#333333", width=10, height=2, command=self.save_timer).grid(row=0, column=3, padx=5)

    # Clock display
    def clock(self):
        clock_time = time.strftime('%H:%M:%S %p')
        self.current_time.config(text=clock_time)
        self.current_time.after(1000, self.clock)

    # Timer functionality
    def timer_alert(self):
        messagebox.showinfo("Time's Up", "The timer has finished!")

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True

            try:
                countdown = int(self.hrs.get()) * 3600 + int(self.mins.get()) * 60 + int(self.secs.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter a valid time.")
                self.timer_running = False
                return
            
            self.countdown(countdown)

    def countdown(self, time_left):
        if time_left < 0 or not self.timer_running:
            timer_running = False
            return

        self.hrs.set(f"{time_left // 3600:02}")
        self.mins.set(f"{(time_left % 3600) // 60:02}")
        self.secs.set(f"{time_left % 60:02}")

        if time_left == 0:
            self.timer_alert()  # Trigger alert
        else:
            self.root.after(1000, lambda: self.countdown(time_left - 1))

    def pause_timer(self):
        if self.timer_running:
            self.paused_time = int(self.hrs.get()) * 3600 + int(self.mins.get()) * 60 + int(self.secs.get())
            self.timer_running = False

    def reset_timer(self):
        self.timer_running = False
        self.hrs.set("00"), self.mins.set("00"), self.secs.set("00")

    # Save and load timers
    def save_timer(self):
        remark = simpledialog.askstring("Save Timer", "Enter timer remark:")
        if remark:
            with open(self.timers_file, "a") as file:
                file.write(f"{remark}:{self.hrs.get()}:{self.mins.get()}:{self.secs.get()}\n")
            self.load_saved_timers()

    def load_saved_timers(self):
        if not os.path.exists(self.timers_file):
            return

        with open(self.timers_file, "r") as file:
            lines = file.readlines()

        for widget in self.saved_timers_frame.winfo_children():
            widget.destroy()

        for line in lines:
            try:
                remark, h, m, s = line.strip().split(":")
                Button(
                    self.saved_timers_frame,
                    text=remark,
                    bg="#ea3548",
                    fg="#fff",
                    command=lambda h=h, m=m, s=s: self.load_timer(h, m, s)
                ).pack(pady=2)
            except ValueError:
                continue

    def load_timer(self, h, m, s):
        self.hrs.set(h)
        self.mins.set(m)
        self.secs.set(s)

def timer_start():
    main_timer = Toplevel()
    gui = timerrun(main_timer)
