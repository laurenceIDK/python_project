from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import *
from datetime import *

from todo_page import *
from timer_page import *
from fquiz_page import *

class home_page:
    def __init__(self, home):
        self.home = home
        self.home.title('Home Page')
        self.home.resizable(False, False)
        self.home.geometry('+200+90')

        self.home_title()
        self.home_widgets()
        

    #Functions
    def home_title(self):
        title_lbl = Label(self.home, text='Home Page', font=('Arial Bold', 21), fg='black')
        title_lbl.pack(padx=(20,0), pady=(20,0), anchor='w')
        subtitle_lbl = Label(self.home, text='Please select an application', font=('Arial', 15), fg='grey')
        subtitle_lbl.pack(padx=20, pady=(5,0), anchor='w')


    def home_widgets(self):
        self.frame_widget = Frame(self.home, background='lightblue')
        self.frame_widget.pack(padx=20, pady=20, anchor='w')

        self.todo_btn = Button(self.frame_widget, text='To-do List Manager', width=20, height=5, relief='raised', borderwidth=3, font=('Arial Bold', 12), command=self.todo_page, activebackground='blue')
        self.todo_btn.grid(column=0,row=0,padx=10, pady=(10,0))

        self.timer_btn = Button(self.frame_widget, text='Timer', width=20, height=5, relief='raised', borderwidth=3, font=('Arial Bold', 12), command=self.timer_page, activebackground='blue')
        self.timer_btn.grid(column=0,row=1,padx=10, pady=(10,0))
        
        self.fquiz_btn = Button(self.frame_widget, text='Flashcard Quiz', width=20, height=5, relief='raised', borderwidth=3, font=('Arial Bold', 12), command=self.fquiz_page, activebackground='blue')
        self.fquiz_btn.grid(column=0,row=2,padx=10, pady=10)
        
    def todo_page(self, event=None):
        todo_start()

    def timer_page(self, event=None):
        timer_start()
    
    def fquiz_page(self, event=None):
        fquiz_start()


def main():
    gui_homepg = home_page(home)
    

home = Tk()
main()
home.mainloop()

