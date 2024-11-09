import tkinter as tk
import random
from tkinter import messagebox

class MathQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz")
        self.score = 0
        self.total_questions = 0
        self.current_question_number = 0
        self.correct_answers = []
        self.wrong_answers = []
        self.mode = None
        self.create_startup_widgets()

    def create_startup_widgets(self):
        self.startup_frame = tk.Frame(self.root)
        self.startup_frame.pack(pady=20)

        start_label = tk.Label(self.startup_frame, text="Select Mode", font=("Arial", 18))
        start_label.pack(pady=10)

        infinite_button = tk.Button(self.startup_frame, text="Infinite Mode", command=lambda: self.start_quiz("infinite"))
        infinite_button.pack(side=tk.LEFT, padx=10)

        test_button = tk.Button(self.startup_frame, text="Test Mode", command=lambda: self.start_quiz("test"))
        test_button.pack(side=tk.RIGHT, padx=10)

    def create_quiz_widgets(self):
        self.problem_label = tk.Label(self.root, text="", font=("Arial", 18))
        self.problem_label.pack(pady=10)

        self.answer_entry = tk.Entry(self.root, font=("Arial", 18))
        self.answer_entry.pack(pady=10)

        self.check_button = tk.Button(self.root, text="Check", command=self.check_answer)
        self.check_button.pack(pady=5)

        if self.mode == "infinite":
            self.show_answer_button = tk.Button(self.root, text="Show Answer", command=self.show_answer)
            self.show_answer_button.pack(pady=5)

            self.end_button = tk.Button(self.root, text="End", command=self.end_quiz)
            self.end_button.pack(pady=5)

    def start_quiz(self, mode):
        self.mode = mode
        self.startup_frame.pack_forget()
        self.create_quiz_widgets()
        self.next_problem()

    def generate_problem(self):
        self.num1 = random.randint(1, 100)
        self.num2 = random.randint(1, 100)
        self.operator = random.choice(["+", "-", "*", "/"])
        if self.operator == "/":
            while self.num2 == 0:  # avoid division by zero
                self.num2 = random.randint(1, 100)
            self.num1 = self.num1 * self.num2  # ensure result is an integer

        self.problem = f"{self.num1} {self.operator} {self.num2}"
        self.answer = eval(self.problem)
        self.current_question_number += 1

    def next_problem(self):
        if self.mode == "test" and self.total_questions >= 10:
            self.end_quiz()
        else:
            self.generate_problem()
            self.problem_label.config(text=f"Q{self.current_question_number}: {self.problem}")
            self.answer_entry.delete(0, tk.END)

    def check_answer(self):
        try:
            user_answer = float(self.answer_entry.get())
            if user_answer == self.answer:
                messagebox.showinfo("Correct!", "You got it right!")
                self.correct_answers.append((self.problem, self.answer))
                self.score += 1
            else:
                messagebox.showerror("Wrong", f"The correct answer was {self.answer}.")
                self.wrong_answers.append((self.problem, self.answer, user_answer))

            self.total_questions += 1
            self.next_problem()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def show_answer(self):
        messagebox.showinfo("Answer", f"The correct answer is {self.answer}")

    def end_quiz(self):
        if self.total_questions > 0:
            percentage = round((self.score / self.total_questions) * 100)
            result_message = f"Your score: {self.score}/{self.total_questions}\nPercentage: {percentage}%"
            result_message += "\n\nIncorrect Answers:\n"
            for prob, correct, wrong in self.wrong_answers:
                result_message += f"{prob} = {correct} (Your answer: {wrong})\n"
        else:
            result_message = "No questions answered."

        messagebox.showinfo("Quiz Ended", result_message)
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuiz(root)
    root.mainloop()
