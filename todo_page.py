from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import *
from datetime import *
import re

class gui_todolist:
    
    #Function Flow of To-do List Manager Program
    def __init__(self, master):

        self._count_pending = 0
        self._count_completed = 0

        self.master = master
        self.master.title('To-do List')
        self.master.geometry('+500+90')
        self.master.resizable(False, False)

        #Try opening the file to check if it exists
        try:
            open('activetask.txt', 'r')
            open('completedtask.txt', 'r')
        except FileNotFoundError:
            with open ('activetask.txt', 'w') as file:
                file.write('')
            print('File activetask.txt created.')

            with open ('completedtask.txt','w') as file:
                file.write('')
            print('File completedtask.txt created.')

        self.title()
        self.widgets()
        self.dashboard()
        self.table_task()

#Output Design
    #Title Design
    def title(self):
        self.title_frame = Frame(self.master, bg='lightblue')
        self.title_frame.pack(pady=(10,0), fill=X)

        title_label = Label(self.title_frame,text='To-Do List', font=('Arial Bold', 22), bg='lightblue')
        title_label.pack(padx=20, side=LEFT)


    #Widgets Design
    def widgets(self):
        self.widgets_frame = Frame(self.master)
        self.widgets_frame.pack(padx=20, pady=(10,10), fill=X)
        self.widgets_frame.columnconfigure(4, weight=1)

        add_task_btn = Button(self.widgets_frame, text='Add Task', command=self.add_task)
        add_task_btn.grid(column=0, row=0, padx=10)

        history_btn = Button(self.widgets_frame, text='History', command=self.check_history)
        history_btn.grid(column=2, row=0, padx=10)

        delete_task_btn = Button(self.widgets_frame, text='Delete Task', bg='red', activebackground='pink', command=self.delete_task)
        delete_task_btn.grid(column=1, row=0, padx=10)

        exit_btn = Button(self.widgets_frame, text=' X ', bg='pink', command= lambda: self.master.destroy())
        exit_btn.grid(column=5, row=0, padx=10, sticky='E')

        checked_btn = Button(self.master, text='\u2713', bg='green', activebackground='lightgreen', command=self.mark_task)
        checked_btn.pack(pady=(0,20), side='bottom')
    
    #Dashboard Design
    def dashboard(self):
        self.dashboard_frame = Frame(self.master,relief=RIDGE, borderwidth=2)
        self.dashboard_frame.pack(padx=20, pady=(10,20), fill=X)

        self.pending_task = Label(self.dashboard_frame, text=f'Pending Tasks: 0')
        self.pending_task.pack(side=LEFT, padx=10)

        self.completed_task_lbl = Label(self.dashboard_frame, text=f'Completed Tasks: 0')
        self.completed_task_lbl.pack(side=LEFT, padx=10)

        self.total_task_lbl = Label(self.dashboard_frame, text=f'Total Tasks: 0')
        self.total_task_lbl.pack(side=LEFT, padx=10)

    #Table Design
    def table_task(self):
        self.style = ttk.Style(self.master)
        self.style.configure("Treeview", rowheight=25)
        self.table_view = ttk.Treeview(self.master, selectmode='browse', height=10, columns=('Title', 'Priority', 'Description', 'Reminder'), show='headings')

        self.table_view.heading('Title', text='Title')
        self.table_view.heading('Priority', text='Priority')
        self.table_view.heading('Description', text='Description')
        self.table_view.heading('Reminder', text='Reminder')

        self.table_view.column('Title', width=100, anchor='center')
        self.table_view.column('Priority', width=100, anchor='center')
        self.table_view.column('Description', width=250, anchor='w')
        self.table_view.column('Reminder', width=150, anchor='center') 

        self.table_view.pack(padx=20, pady=(0,20), fill=BOTH)
        self.load_task()
        self.load_history()


#Running Functionalities
    #Load Task
    def load_task(self):
        self._count_pending = 0
        for row in self.table_view.get_children():
            self.table_view.delete(row)

        with open('activetask.txt','r') as file:
            text = file.read()
            if text:
                with open('activetask.txt', 'r') as file:
                    for row in file:
                        row = row.strip()
                        if row:
                            data = row.split('|')
                            self.table_view.insert('', 'end', values=data)
                            self._count_pending += 1
                            self.pending_task.config(text=f'Pending Tasks: {self._count_pending}')
            else:
                self.pending_task.config(text='Pending Tasks: 0')
        self.load_total()
                
    #Add Task
    def add_task(self):
        self.add_task_form = Toplevel()
        self.add_task_form.title('Add Task')
        
        def confirmation(event=None):
            task_title = task_title_entry.get()
            task_priority = task_priority_list.get()
            task_description = task_description_entry.get('1.0','end').strip()
            task_reminder = date_entry.get() + ' ' + time_choice.get() + ' ' + ampm_choice.get()

            confirm = messagebox.askyesno('Confirmation Task', f'Task Title: {task_title}\nPriority: {task_priority}\nReminder: {task_reminder}\nDescription: {task_description}')

            if confirm == True and (task_title == 'Insert task title here...' or task_priority == 'Select an option' or re.search('Select an option', task_reminder)):
                messagebox.showwarning('Incomplete Task', 'Task title, priority, and reminder are required fields.\nPlease refill again!')
                self.add_task_form.focus()
            elif confirm == False: 
                self.add_task_form.destroy()
            else:
                self.add_task_form.destroy()
                messagebox.showinfo('Add Task Successfully', 'Task added Successfully!')
                self.p_add_task(task_title, task_priority, task_description, task_reminder)
                

        def not_focus(event):
            if not task_title_entry.get():
                task_title_entry.insert(0, 'Insert task title here...')
                task_title_entry.configure(fg='gray')

        def on_focus(event):
            if task_title_entry.get() == 'Insert task title here...':
                task_title_entry.delete(0, END)
                task_title_entry.configure(fg='black')

        task_title_lbl = Label(self.add_task_form, text='Task Title: ')
        task_title_lbl.grid(row=0, column=0, sticky='w', padx=(20,0), pady=(10,0)) 
        task_title_entry = Entry(self.add_task_form, width=30)
        task_title_entry.grid(row=0, column=1, sticky='w', columnspan=2)
        task_title_entry.insert(0, 'Insert task title here...')
        task_title_entry.configure(fg='gray')

        task_title_entry.bind("<FocusIn>", on_focus)
        task_title_entry.bind("<FocusOut>", not_focus)

        task_priority_lbl = Label(self.add_task_form, text='Priority: ')
        task_priority_lbl.grid(row=1, column=0, sticky='w', padx=(20,0), pady=(10,0))
        task_priority_list = ttk.Combobox(self.add_task_form, width=25, state='readonly', values=['Important', 'Medium', 'Ignore'])
        task_priority_list.set('Select an option')
        task_priority_list.grid(row=1, column=1, sticky='w', columnspan=2)

        task_reminder_lbl = Label(self.add_task_form, text='Time Reminder: ')
        task_reminder_lbl.grid(row=2, column=0, sticky='w', padx=(20,0), pady=(10,0))
        time_choice = ttk.Combobox(self.add_task_form, width=20, state='readonly', values=['01:00','02:00','03:00','04:00','05:00','06:00','07:00','08:00','09:00','10:00','11:00','12:00'])
        time_choice.set('Select an option')
        time_choice.grid(row=2, column=1, sticky='w')
        ampm_choice = ttk.Combobox(self.add_task_form, width=5, state='readonly', values=['AM', 'PM'])
        ampm_choice.set('PM')
        ampm_choice.grid(row=2, column=1, sticky='e', padx=(0,20))

        date_entry = DateEntry(self.add_task_form, mindate=datetime.today(), maxdate=datetime.today()+timedelta(days=7), date_pattern='MM/dd/yyyy')
        date_entry.grid(row=3, column=1, sticky='w', columnspan=2, pady=(10,0))

        task_description_lbl = Label(self.add_task_form, text='Description (Optional): ')
        task_description_lbl.grid(row=4, column=0, sticky='w', padx=(20,0), pady=(10,0))
        task_description_entry = Text(self.add_task_form, width=50, height=5)
        task_description_entry.grid(row=5, column=0, columnspan=2, padx=20, pady=(10,20))

        self.add_task_form.bind('<Return>', confirmation)

        add_task_submit = Button(self.add_task_form, text='Submit', command=confirmation)
        add_task_submit.grid(row=6, column=0, columnspan=2, pady=(0,10))

    #Mark Task
    def mark_task(self):
        selected_item = self.table_view.focus()
        if not selected_item:
            messagebox.showwarning('No Task Selected', 'Please select a task to mark completed.')
        else:
            mark_title = self.table_view.item(selected_item)['values'][0]
            mark_priority = self.table_view.item(selected_item)['values'][1]
            mark_description = self.table_view.item(selected_item)['values'][2]
            mark_reminder = self.table_view.item(selected_item)['values'][3]
            index = self.table_view.index(selected_item)

            with open('activetask.txt', 'r') as file:
                reader = file.readlines()

            if index >= 0 and index < len(reader):
                del reader[index]
                with open('activetask.txt', 'w') as file:
                    file.writelines(reader)
            self.load_task()

            with open('completedtask.txt', 'a') as file:
                file.writelines(f'{mark_title}|{mark_priority}|{mark_description}|{mark_reminder}\n')

            self.load_history()

    #Check History
    def check_history(self):
        self.history_frame = Toplevel()
        self.history_frame.title('Completed Tasks History')

        self.history_tree = ttk.Treeview(self.history_frame, selectmode='browse', height=10, columns=('Title', 'Priority', 'Description'), show='headings')

        self.history_tree.heading('Title', text='Title')
        self.history_tree.heading('Priority', text='Priority')
        self.history_tree.heading('Description', text='Description')

        self.history_tree.column('Title', width=100, anchor='center')
        self.history_tree.column('Priority', width=100, anchor='center')
        self.history_tree.column('Description', width=300, anchor='w') 

        self.history_tree.pack(padx=20, pady=(20,10), fill=BOTH)

        self.clear_history = Button(self.history_frame, text='Clear History', command=self.p_clear_history)
        self.clear_history.pack(pady=(10,20), anchor='center')

        self.p_history_pg()

    #Load History
    def load_history(self):
        self._count_completed = 0
        with open ('completedtask.txt', 'r') as file:
            text = file.read()
        
        if text:
            with open ('completedtask.txt', 'r') as file:  
                for row in file:
                    row = row.strip()
                    if row:
                        data = row.split('|')
                        self._count_completed += 1
                        self.completed_task_lbl.config(text=f'Completed Tasks: {self._count_completed}')
        else:
            self.completed_task_lbl.config(text='Completed Tasks: 0')
        self.load_total()

    #Load History Page
    def p_history_pg(self):
        self._count_completed = 0
        with open ('completedtask.txt', 'r') as file:
            text = file.read()
        
        if text:
            with open ('completedtask.txt', 'r') as file:  
                for row in file:
                    row = row.strip()
                    if row:
                        data = row.split('|')
                        self.history_tree.insert('', 'end', values=data)
                        self._count_completed += 1
                        self.completed_task_lbl.config(text=f'Completed Tasks: {self._count_completed}')
        else:
            self.completed_task_lbl.config(text='Completed Tasks: 0')

    #Add Task Page
    def p_add_task(self, task_title, task_priority, task_description, task_reminder):
        save_task = [f'{task_title}|{task_priority}|{task_description}|{task_reminder}\n']
        with open ('activetask.txt', 'a') as file:
            file.writelines(save_task)
        self.load_task()

    #Delete Task
    def delete_task(self):
        selected_item = self.table_view.focus()
        if not selected_item:
            messagebox.showwarning('No Task Selected', 'Please select a task to delete.')
        else:
            del_title = self.table_view.item(selected_item)['values'][0]
            del_priority = self.table_view.item(selected_item)['values'][1]
            del_description = self.table_view.item(selected_item)['values'][2]
            del_reminder = self.table_view.item(selected_item)['values'][3]
            index = self.table_view.index(selected_item)
            confirm = messagebox.askyesno('Confirmation Task', f'Are you sure you want to delete the task:\nTitle: {del_title}\nPriority: {del_priority}\nDescription: {del_description}\nReminder: {del_reminder}')                
            
            if confirm == True:
                with open('activetask.txt', 'r') as file:
                    reader = file.readlines()

                if index >= 0 and index < len(reader):
                    del reader[index]
                    with open('activetask.txt', 'w') as file:
                        file.writelines(reader)
                self.load_task()

    #Load Total Page
    def load_total(self):
        total = self._count_pending + self._count_completed
        self.total_task_lbl.config(text=f'Total Tasks: {total}')

    
    def p_clear_history(self):
        confirm = messagebox.askyesno('Confirmation', 'Are you sure you want to clear the history?')
        if confirm == True:
            with open('completedtask.txt', 'w') as file:
                file.write('')
            self.load_history()
            self.p_history_pg()
            self.history_tree.delete(*self.history_tree.get_children())

def todo_start():
    main_todo = Toplevel()
    gui = gui_todolist(main_todo)
