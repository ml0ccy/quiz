import customtkinter as ctk
import tkinter as tk
import random

class QuizApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Викторина")
        self.geometry("600x400")

        self.quiz_data = {
            "Столицы стран": {
                "Столица Польши?": "Варшава",
                "Столица Франции?": "Париж",
                "Столица Германии?": "Берлин",
                "Столица Италии?": "Рим",
                "Столица Испании?": "Мадрид",
            },
            "Животные": {
                "Самое быстрое наземное животное?": "Гепард",
                "Самое крупное млекопитающее?": "Синий кит",
                "Животное с самым длинным языком?": "Муравьед",
                "Какое животное является символом Австралии?": "Кенгуру",
                "Самая большая кошка в мире?": "Тигр",
            },
            "История": {
                "В каком году началась Вторая мировая война?": "1939",
                "Кто был первым президентом США?": "Джордж Вашингтон",
                "В каком году был основан город Москва?": "1147",
                "Кто открыл Америку?": "Христофор Колумб",
                "Какая страна была родиной Олимпийских игр?": "Греция",
            }
        }

        self.main_menu()

    def main_menu(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.title_label = ctk.CTkLabel(self, text="Главное меню", font=ctk.CTkFont(size=30))
        self.title_label.pack(pady=20)

        self.quiz_buttons = {}
        for quiz_name in self.quiz_data:
            self.quiz_buttons[quiz_name] = ctk.CTkButton(self, text=quiz_name, command=lambda name=quiz_name: self.start_quiz(name))
            self.quiz_buttons[quiz_name].pack(pady=5)

        self.exit_button = ctk.CTkButton(self, text="Выход", command=self.destroy)
        self.exit_button.pack(pady=10)

    def start_quiz(self, quiz_name):
        for widget in self.winfo_children():
            widget.destroy()

        self.questions = self.quiz_data[quiz_name]
        self.question_keys = list(self.questions.keys())
        self.score = 0
        self.current_question = None
        self.time_left = 10  # Время на вопрос в секундах

        self.question_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=20))
        self.question_label.pack(pady=20)

        self.answer_entry = ctk.CTkEntry(self, font=ctk.CTkFont(size=16))
        self.answer_entry.pack(pady=10)

        self.submit_button = ctk.CTkButton(self, text="Ответить", command=self.check_answer)
        self.submit_button.pack()

        self.score_label = ctk.CTkLabel(self, text="Счет: 0", font=ctk.CTkFont(size=16))
        self.score_label.pack(pady=10)

        self.timer_label = ctk.CTkLabel(self, text=f"Время: {self.time_left}", font=ctk.CTkFont(size=16))
        self.timer_label.pack(pady=10)

        self.back_to_menu_button = ctk.CTkButton(self, text="В главное меню", command=self.main_menu)
        self.back_to_menu_button.pack(pady=10)

        self.next_question()

    def next_question(self):
        if self.question_keys:
            self.current_question = random.choice(self.question_keys)
            self.question_label.configure(text=self.current_question)
            self.answer_entry.delete(0, tk.END)
            self.time_left = 10 # Сброс таймера для нового вопроса
            self.start_timer()
        else:
            self.question_label.configure(text="Викторина окончена!")
            self.answer_entry.configure(state="disabled")
            self.submit_button.configure(state="disabled")
            self.timer_label.configure(text="") # Скрытие таймера

    def start_timer(self):
        if self.time_left > 0:
            self.timer_label.configure(text=f"Время: {self.time_left}")
            self.time_left -= 1
            self.after(1000, self.start_timer)
        else:
            self.check_answer() # Автоматический переход к следующему вопросу

    def check_answer(self):
        user_answer = self.answer_entry.get().strip()
        if self.current_question: # Проверка, есть ли текущий вопрос
            correct_answer = self.questions[self.current_question]

            if user_answer.lower() == correct_answer.lower():
                self.score += 1
                self.score_label.configure(text=f"Счет: {self.score}")
                try:
                    self.question_keys.remove(self.current_question)
                except ValueError:
                    pass
                self.next_question()
            else:
                print("Неправильный ответ")
                self.next_question() # Переход к следующему вопросу даже при неправильном ответе
        else:
            self.next_question() # Случай, когда время вышло, а вопроса нет

if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()
