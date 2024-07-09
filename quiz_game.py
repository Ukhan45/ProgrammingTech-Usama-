import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")
        self.master.geometry("600x400")
        self.bg_image = Image.open("quiz.jpeg")
        self.bg_image = self.bg_image.resize((600, 400), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.master, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)  
        self.frame = tk.Frame(self.master, bg='#ffffff', bd=5)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")
        self.label_username = tk.Label(self.frame, text="Username:", font=("Arial", 12))
        self.label_username.grid(row=0, column=0, pady=10, padx=10)
        self.entry_username = tk.Entry(self.frame, font=("Arial", 12))
        self.entry_username.grid(row=0, column=1, pady=10, padx=10)
        self.label_password = tk.Label(self.frame, text="Password:", font=("Arial", 12))
        self.label_password.grid(row=1, column=0, pady=10, padx=10)
        self.entry_password = tk.Entry(self.frame, font=("Arial", 12), show="*")
        self.entry_password.grid(row=1, column=1, pady=10, padx=10)  
        self.btn_login = tk.Button(self.frame, text="Login", command=self.check_login, font=("Arial", 12), bg="#4CAF50", fg="white")
        self.btn_login.grid(row=2, columnspan=2, pady=10, padx=10)
    def check_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if username == "usama" and password == "pass":
            self.master.withdraw()  
            self.open_welcome_window()
        else:
            messagebox.showerror("Login Error", "Invalid username or password")

    def open_welcome_window(self):
        welcome_root = tk.Toplevel(self.master)
        app = WelcomeWindow(welcome_root)

class WelcomeWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Welcome")
        self.master.geometry("600x400")
        self.bg_image = Image.open("welcome.jpeg")
        self.bg_image = self.bg_image.resize((600, 400), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.master, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)
        self.frame = tk.Frame(self.master, bg='#ffffff', bd=5)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")
        self.label_welcome = tk.Label(self.frame, text="Welcome to the Quiz Game!", font=("Arial", 16, "bold"), bg="#ffffff")
        self.label_welcome.pack(pady=10)  
        self.label_rules = tk.Label(self.frame, text="Rules:\n- You will have 10 seconds to answer each question.\n- Click 'Submit Answer' to submit your choice.\n- Each correct answer scores one point.\n- Have fun!", font=("Arial", 12), justify="center", bg="#ffffff")
        self.label_rules.pack(pady=10)
        self.btn_start = tk.Button(self.frame, text="Start Quiz", command=self.start_quiz, font=("Arial", 12), bg="#4CAF50", fg="white")
        self.btn_start.pack(pady=10)
        self.btn_exit = tk.Button(self.frame, text="Exit", command=self.master.quit, font=("Arial", 12), bg="#f44336", fg="white")
        self.btn_exit.pack(pady=10)
    def start_quiz(self):
        self.master.withdraw()  
        quiz_root = tk.Toplevel(self.master)
        app = QuizGame(quiz_root)
class QuizGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz Game")
        self.master.geometry("600x400")
        self.master.configure(bg="#f0f0f0")
        self.questions = [
            {
                "question": "What is the capital of France?",
                "choices": ["Paris", "London", "Berlin", "Madrid"],
                "correct_answer": "Paris"
            },
            {
                "question": "Who wrote 'Hamlet'?",
                "choices": ["William Shakespeare", "Charles Dickens", "Leo Tolstoy", "Jane Austen"],
                "correct_answer": "William Shakespeare"
            },
            {
                "question": "What is the largest planet in our solar system?",
                "choices": ["Earth", "Jupiter", "Saturn", "Mars"],
                "correct_answer": "Jupiter"
            },
            {
                "question": "Who painted the Mona Lisa?",
                "choices": ["Leonardo da Vinci", "Vincent van Gogh", "Pablo Picasso", "Michelangelo"],
                "correct_answer": "Leonardo da Vinci"
            },
            {
                "question": "Which country is the largest by land area?",
                "choices": ["Russia", "Canada", "China", "United States"],
                "correct_answer": "Russia"
            }
        ]
        
        self.current_question = 0
        self.score = 0
        self.quiz_finished = False
        
        self.show_question()
    
    def show_question(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            
            self.label_question = tk.Label(self.master, text=question_data["question"], wraplength=400, justify="center", font=("Arial", 14), bg="#f0f0f0")
            self.label_question.pack(pady=20)
            
            self.radio_var = tk.StringVar()
            self.radio_var.set(question_data["choices"][0])
            self.radio_buttons = [] 
            for choice in question_data["choices"]:
                radio = tk.Radiobutton(self.master, text=choice, variable=self.radio_var, value=choice, font=("Arial", 12), bg="#f0f0f0", selectcolor="#d9d9d9")
                radio.pack(pady=5)
                self.radio_buttons.append(radio)
            
            self.btn_submit = tk.Button(self.master, text="Submit Answer", command=self.submit_answer, font=("Arial", 12), bg="#4CAF50", fg="white")
            self.btn_submit.pack(pady=10)
            
            self.label_feedback = tk.Label(self.master, text="", font=("Arial", 12), fg="blue", bg="#f0f0f0")
            self.label_feedback.pack(pady=10)
            
            self.label_score = tk.Label(self.master, text=f"Score: {self.score}", font=("Arial", 12), bg="#f0f0f0")
            self.label_score.pack(pady=10)
            
            self.label_timer = tk.Label(self.master, text="", font=("Arial", 12), fg="red", bg="#f0f0f0")
            self.label_timer.pack(pady=10)
            
            self.start_timer()
        else:
            self.show_results()
    
    def start_timer(self):
        self.time_left = 10
        self.update_timer()
    
    def update_timer(self):
        if self.label_timer.winfo_exists():
            if self.time_left >= 0:
                self.label_timer.config(text=f"Time left: {self.time_left} seconds")
                self.time_left -= 1
                self.master.after(1000, self.update_timer)
            else:
                self.submit_answer(timeout=True)
        else:
            self.time_left = -1  
    
    def submit_answer(self, timeout=False):
        if self.current_question < len(self.questions):
            if timeout:
                selected_answer = ""
            else:
                selected_answer = self.radio_var.get()
            
            correct_answer = self.questions[self.current_question]["correct_answer"]
            
            if selected_answer == "":
                if not timeout:
                    self.label_feedback.config(text=f"Time's up! The correct answer is: {correct_answer}", fg="red")
                else:
                    messagebox.showwarning("Warning", "Please select an answer.")
            else:
                if selected_answer == correct_answer:
                    self.score += 1
                    self.label_feedback.config(text="Correct!", fg="green")
                else:
                    self.label_feedback.config(text=f"Incorrect. The correct answer is: {correct_answer}", fg="red")
                
                self.label_score.config(text=f"Score: {self.score}")
            
            
            self.current_question += 1
            self.master.after(2000, self.show_question)
    
    def show_results(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        
        result_text = f"Quiz Finished!\nYour score: {self.score}/{len(self.questions)}"
        if self.score >= len(self.questions) / 2:
            result_text += "\nGood job! You scored above average."
        else:
            result_text += "\nYou can do better. Try again!"
        
        self.label_result = tk.Label(self.master, text=result_text, font=("Arial", 14), bg="#f0f0f0")
        self.label_result.pack(pady=20)
        
        self.btn_play_again = tk.Button(self.master, text="Play Again", command=self.restart_quiz, font=("Arial", 12), bg="#4CAF50", fg="white")
        self.btn_play_again.pack(pady=10)
        
        self.btn_exit = tk.Button(self.master, text="Exit", command=self.exit_quiz, font=("Arial", 12), bg="#f44336", fg="white")
        self.btn_exit.pack(pady=10)
    
    def restart_quiz(self):
        self.current_question = 0
        self.score = 0
        self.quiz_finished = False
        self.show_question()
    
    def exit_quiz(self):
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
