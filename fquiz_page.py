import tkinter as tk
from tkinter import messagebox as mb

#Fonts
subway_london=("SubwayLondon", 15)
arial_bold = ("Arial", 12, "bold")
arial_round = ("Arial Round MT Bold",16)
cooper = ("Cooper Black", 24)
times_new_roman = ("Times New Roman", 12)

class flashcardQuizzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard Quizzer")
        self.root.geometry("800x600+500+45")

        self.quiz = []          #list to store all the created quiz data
        self.current_quiz = None
        self.quiz_file = "quiz.txt"
        self.progress_file = "progress.txt"
        self.progress = {"attempted" : 0, "correct" : 0} #progress tracking dict

        self.load_quiz()
        self.load_progress()
        self.main_menu()

    def main_menu(self):

        self.clear_window()
        tk.Label(self.root, text="Welcome to Flashcard Quizzer!", font=cooper, bg='#37e6e3', relief="ridge", bd=7, padx=10, pady=5).pack(pady=30)
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Create Quiz", font=arial_round, bg='#d19711', activebackground='#0ee832', relief="sunken", bd=5, padx=7, pady=3, command= lambda: self.form_quiz()).pack(pady=10, fill='x')
        tk.Button(btn_frame, text="Study Quiz", font=arial_round, bg='#d19711', activebackground='#0ee832', relief="sunken", bd=5, padx=7, pady=3, command=self.study_quiz).pack(pady=10, fill='x')
        tk.Button(btn_frame, text="Edit/Delete Quiz", font=arial_round, bg='#d19711', activebackground='#0ee832', relief="sunken", bd=5, padx=7, pady=3, command=self.edit_del_quiz).pack(pady=10, fill='x')
        tk.Button(btn_frame, text="Track Progress", font=arial_round, bg='#d19711', activebackground='#0ee832', relief="sunken", bd=5, padx=7, pady=3, command=self.track_progress).pack(pady=10, fill='x')
        tk.Button(btn_frame, text="Back to Main Menu", font=arial_round, bg='#fc0000', activebackground='#0ee832', relief='raised', bd=5, padx=7, pady=3, command=lambda: self.root.destroy()).pack(pady=10, fill='x')

    def form_quiz(self, quiz_idx = None, quiz_data = None):
        #function to form a quiz form (for create quiz and edit quiz)
        self.clear_window()
        
        title = "Create a New Quiz!" if quiz_idx is None else "Edit Quiz!"
        tk.Label(self.root, text=title, font=cooper, bg='#37e6e3', relief="ridge", bd=7, padx=10, pady=5).pack(pady=10)
        
        ques_frame = tk.Frame(self.root)
        ques_frame.pack(fill='x', padx=20, pady=5)
        tk.Label(ques_frame, text="Question:", font=arial_bold).pack(side="left", padx=5, pady=5)
        ques_entry = tk.Entry(ques_frame)
        ques_entry.pack(side="left",fill='x', expand=True)
        
        if quiz_data:
            ques_entry.insert(0,quiz_data[0])   #insert question of the create quiz when editing quiz

        options = [] #list to store all the 'raw option' written
        for i in range(4):
            option_frame = tk.Frame(self.root)
            option_frame.pack(fill='x', padx=20, pady=5)
            tk.Label(option_frame, text=f"Option {i+1}:", font=arial_bold).pack(side='left', padx=5, pady=5)
            opt_entry = tk.Entry(option_frame)
            opt_entry.pack(side="left", fill='x', expand=True)
            if quiz_data:
                opt_entry.insert(0, quiz_data[i + 1])   #insert options of the created quiz when editing quiz
            options.append(opt_entry)

        tk.Label(self.root, text="Check the following box for the correct answers:", font=arial_bold).pack(pady=10)
        ans_frame = tk.Frame(self.root)
        ans_frame.pack(anchor='center', pady=5)
        
        opt_var_list = [] #list to store the variable[selected(1) or not(0)] of checkbutton
        for i in range(4):
            chkbtn_var = tk.IntVar(value=int(quiz_data[i + 5]) if quiz_data else 0)
            #i + 5 is to get the idx for variable of chkbtn, first 5 item is question and 4 options
            ans_chkbtn = tk.Checkbutton(ans_frame, text=f"Option {i+1}", font=times_new_roman, variable=chkbtn_var)
            ans_chkbtn.pack(side='left', padx=15)
            opt_var_list.append(chkbtn_var)

        def save_quiz():
            question = ques_entry.get().strip()
            opt_text = [opt.get().strip() for opt in options]
            correct_options = [str(var.get()) for var in opt_var_list]
            #convert var to string so can be save to txt file

            if question and all(opt_text) and ('1' in correct_options):
            #check if question, all options field is filled and at least one option is selected as correct ans
                new_quiz = [question, *opt_text, *correct_options]
                if quiz_idx is None:
                    self.quiz.append(new_quiz) #append new quiz if creating quiz
                else:
                    self.quiz[quiz_idx] = new_quiz #overwrite the selected quiz when editing quiz
                self.save_quiz_file()
                mb.showinfo("Success", "Quiz saved successfully!")
                self.main_menu() if quiz_idx is None else self.edit_del_quiz()
                
            #if conditions to make a quiz doesnt fullfilled    
            elif not question or not all(opt_text):
                mb.showwarning("Input Error", "Question field and all options field must be filled!")
            else:
                mb.showwarning("No Correct Answer Selected", "Please select at least one correct answer for the question!")
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        if quiz_idx is None:
            tk.Button(btn_frame, text="Save Quiz", font=arial_round, bg='#d19711', activebackground='#0ee832', relief="sunken", bd=5, padx=7, pady=3, command=save_quiz).pack(pady=10, fill='x')
            tk.Button(btn_frame, text="Back to Flashcard Quizzer Menu", font=arial_round, bg='#fc0000', activebackground='#0ee832', relief='raised', bd=5, padx=7, pady=3, command=self.main_menu).pack(pady=10, fill='x')       
        else:
            tk.Button(btn_frame, text="Save Changes", font=arial_round, bg='#d19711', activebackground='#0ee832', relief="sunken", bd=5, padx=7, pady=3, command=save_quiz).pack(side="left", pady=10)
            tk.Button(btn_frame, text="Cancel Edit", font=arial_round, bg='#fc0000', activebackground='#0ee832', relief='raised', bd=5, padx=7, pady=3, command=self.edit_del_quiz).pack(side="left", pady=10)       

    def edit_del_quiz(self):
        self.clear_window()

        if not self.quiz:
            mb.showerror("No Quiz Created", "No quiz available. Please create some first.")
            self.main_menu()
            return

        tk.Label(self.root, text="Edit/Delete Quizzes", font=cooper, bg='#37e6e3', relief="ridge", bd=7, padx=10, pady=5).pack(pady=20)
        
        quiz_list_frame = tk.Frame(self.root, bd=5, bg='#a0ad74', relief='sunken')
        quiz_list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        #a listbox to show all the quiz available to edit
        quiz_listbox = tk.Listbox(quiz_list_frame, font=arial_bold, bd=0, highlightbackground='#a0ad74', bg='#a0ad74', selectmode="single")
        quiz_listbox.pack(side="left", fill="both", expand=True, padx=8, pady=5)
        
        #a scroll bar for the listbox
        scrollbar = tk.Scrollbar(quiz_list_frame, orient="vertical")
        scrollbar.pack(side="right", fill='y')
        quiz_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=quiz_listbox.yview)

        #display the question of the quiz
        for idx, quiz in enumerate(self.quiz, 1):
            question = quiz[0]
            quiz_listbox.insert("end", f"{idx}. {question}")

        def edit_quiz():
            try:
                #curselection return tuple of selected list index. Since the selectmode is single, use idx = 0 to get selected list index
                selected_idx = quiz_listbox.curselection()[0]
                selected_quiz = self.quiz[selected_idx]
                self.form_quiz(selected_idx, selected_quiz) #edit quiz
            except IndexError:
                mb.showwarning("No Selection!", "Please select a quiz to edit.")

        def del_quiz():
            try:
                selected_idx = quiz_listbox.curselection()[0]
                #double confirmation to prevent accidental deletion
                res = mb.askyesno("Delete Quiz Confirmation", f"Do you sure you want to delete quiz number {selected_idx + 1}?")
                if res:
                    del self.quiz[selected_idx]
                    self.save_quiz_file()
                    mb.showinfo("Success", "Quiz deleted successfully!")
                    self.edit_del_quiz()
            except IndexError:
                mb.showwarning("No Selection!", "Please select a quiz to edit.")
            
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Edit Selected Quiz", font=arial_round, bg='#d19711', activebackground='#0ee832', relief="sunken", bd=5, padx=7, pady=3, command=edit_quiz).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Delete Selected Quiz", font=arial_round, bg='#fc0000', activebackground='#0ee832', relief="raised", bd=5, padx=7, pady=3, command=del_quiz).pack(side="left", padx=10)
        tk.Button(self.root, text="Back to Flashcard Quizzer Menu", font=arial_round, bg='#fc0000', activebackground='#0ee832', relief='raised', bd=5, padx=7, pady=3, command=self.main_menu).pack(pady=20)

    def study_quiz(self):
        self.clear_window()

        if not self.quiz:
            mb.showerror("No Quiz Created", "No quiz available. Please create some first.")
            self.main_menu()
            return
        #iterator of the quiz data list
        self.current_quiz = iter(self.quiz)

        ques_label = tk.Label(self.root, text="", font=subway_london, relief='raised', bd=5, bg="#7771ad", wraplength=self.root.winfo_width() - 50, justify="left", padx=15, pady=8)
        ques_label.pack(pady=20)
        chkbtn_frame = tk.Frame(self.root)
        chkbtn_frame.pack(pady=10)

        options_chkbtn = []
        option_vars = []
        for i in range(4):
            option_var = tk.IntVar()
            opt_chkbtn = tk.Checkbutton(chkbtn_frame, text="", font=times_new_roman, bd=3, relief="solid", bg="#8a8a8a", padx=12, pady=7, variable=option_var)
            opt_chkbtn.pack(fill='x', pady=5)
            options_chkbtn.append(opt_chkbtn)
            option_vars.append(option_var)

        def show_next_quiz():
            try:
                quiz = next(self.current_quiz)  #show next question
                quiz_no = self.quiz.index(quiz) + 1
                ques = quiz[0]
                opt_txt = quiz[1:5]
                correct_opts = quiz[5:]

                ques_label.config(text=f"Question {quiz_no}:\n {ques}") #display question

                #display all 4 options user can choose from
                for idx, chkbtn in enumerate(options_chkbtn):
                    chkbtn.config(text=f"{opt_txt[idx]}")
                    option_vars[idx].set(0)

                def check_answer(correct_opts):
                    self.progress["attempted"] += 1
                    selected_ans = [str(var.get()) for var in option_vars]

                    if selected_ans == correct_opts:
                        #compare selected ans to correct ans
                        self.progress["correct"] += 1
                        mb.showinfo("Correct!", "You selected the correct answers!")
                        self.save_progress_file()
                        show_next_quiz()
                    else:
                        mb.showerror("Incorrect", "The selected answers is wrong. \nTry again!")
                        self.save_progress_file()

                def show_answer():
                    #show user correct answers
                    for idx, result in enumerate(correct_opts):
                        option_vars[idx].set(int(result))
                    mb.showinfo("Correct Answers Shown", "The correct answers is selected.")

                submit_btn.config(command=lambda: check_answer(correct_opts))
                show_btn.config(command=show_answer)
            except StopIteration:
                mb.showinfo("End of Quiz", "You have completed every single quiz!")
                self.main_menu()

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)
        submit_btn = tk.Button(btn_frame, text="Submit Answer", font=arial_round, bg='#d19711', activebackground='#0ee832', relief="sunken", bd=5, padx=7, pady=3)
        submit_btn.pack(side="left")
        show_btn = tk.Button(btn_frame, text="Show Answer", font=arial_round, bg='#d19711', activebackground='#0ee832', relief="sunken", bd=5, padx=7, pady=3)
        show_btn.pack(side="left")
        tk.Button(self.root, text="Back to Flashcard Quizzer Menu", font=arial_round, bg='#fc0000', activebackground='#0ee832', relief='raised', bd=5, padx=7, pady=3, command=self.main_menu).pack(pady=10)
        show_next_quiz()

    def track_progress(self):
        self.clear_window()
        tk.Label(self.root, text="Track Your Progress", font=cooper, bg='#37e6e3', relief="ridge", bd=7, padx=10, pady=5).pack(pady=20)

        total_quiz = len(self.quiz)             #total quiz created
        attempted = self.progress["attempted"]  #number of attempted answer of quizzes (note: not "no of quiz attempted" but "no of attempted")
        correct = self.progress["correct"]      #number of correct attempt

        tk.Label(self.root, text=f"Total Quiz Created: {total_quiz}", font=arial_round, bg="#4ccfdd", relief="groove", bd=3, padx=7, pady=5).pack(pady=20)
        big_frame = tk.Frame(self.root)
        big_frame.pack(pady=30)
        frame1 = tk.Frame(big_frame)
        frame1.pack(fill='x', padx=10, pady=5)
        frame2 = tk.Frame(big_frame)
        frame2.pack(fill='x', padx=15, pady=5)
        tk.Label(frame1, text=f"No of Attempted: {attempted}", font=arial_round, bg="#f7d058", relief="groove", bd=3, padx=7, pady=5).pack(side="left", padx=5)
        tk.Label(frame1, text=f"Answered Correct: {correct}", font=arial_round, bg="#49a64e", relief="groove", bd=3, padx=7, pady=5).pack(side="right", padx=5)
        tk.Label(frame2, text=f"Accuracy: {correct / attempted * 100:.2f}%" if attempted > 0 else "Accuracy: N/A", font=arial_round, bg="#f76767", relief="groove", bd=3, padx=7, pady=5).pack(fill='x')
        tk.Button(self.root, text="Reset Progress", font=arial_round, bg='#fc0000', activebackground='#0ee832', relief="solid", bd=3, padx=7, pady=3, command=self.reset_progress).pack(pady=20)
        tk.Button(self.root, text="Back to Flashcard Quizzer Menu", font=arial_round, bg='#fc0000', activebackground='#0ee832', relief='raised', bd=5, padx=7, pady=3, command=self.main_menu).pack(pady=30)

    def save_quiz_file(self):
        with open(self.quiz_file, 'w') as file:
            for q in self.quiz:
                file.write('|'.join(q) + '\n')

    def load_quiz(self):
        try:
            with open(self.quiz_file, 'r') as file:
                for line in file:
                    data = line.strip().split('|')
                    #ensure only quizzes that contain correct no of field is loaded, prevent error
                    if len(data) == 9:  
                        self.quiz.append(data)
        except FileNotFoundError:
            self.quiz = []

    def save_progress_file(self):
        with open(self.progress_file, 'w') as file:
            attempted = str(self.progress["attempted"])
            correct = str(self.progress["correct"])
            file.write(f"{attempted}\n{correct}")

    def load_progress(self):
        try:
            with open(self.progress_file, 'r') as file:
                lines = file.readlines()
                #ensure only progress file that has two lines of data is loaded
                if len(lines) == 2:
                    self.progress["attempted"] = int(lines[0].strip())
                    self.progress["correct"] = int(lines[1].strip())
        except FileNotFoundError:
            self.progress = {"attempted": 0, "correct": 0}

    def reset_progress(self):
        #double confirmation to prevent accidental reset of progress
        res = mb.askyesno("Reset progress confirmation", "Do you sure you want to reset your progress?")
        if res:
            self.progress["attempted"] = 0
            self.progress["correct"] = 0
            self.save_progress_file()
            mb.showinfo("Success", "Progress reset succesfully!")
            self.track_progress()
        else:
            return

    def clear_window(self):
        #function to clear the window
        for widget in self.root.winfo_children():
            widget.destroy() 

#to run flashcardquizzer
def fquiz_start():
    root = tk.Toplevel()
    app = flashcardQuizzer(root)
