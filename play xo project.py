import tkinter as tk
from tkinter import messagebox
import random
import time

# إعدادات اللعبة مع سكنات جديدة
skins = [("❄️", "🕑", 100),  # سكن قلبي
         ("☀️", "🌙", 100),  # سكن شمس وقمر
         ("🔥", "💧", 100),  # سكن نار وماء
         ("🍎", "🍊", 101),  # سكن فواكه
         ("🐶", "🐱", 100)]  # سكن حيوانات

save_file = "save_data.txt"


class TicTacToeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("مشروع XO")  # تغيير العنوان إلى XO Project
        self.root.configure(bg="#2C3E50")  # الخلفية باللون الرمادي الداكن
        self.root.attributes('-fullscreen', True)  # جعل النافذة فل سكرين
        self.root.bind("<F11>", self.toggle_fullscreen)  # تمكين التبديل بين الوضع الكامل والشاشة العادية باستخدام F11
        self.root.bind("<Escape>", self.exit_fullscreen)  # الخروج من وضع فل سكرين عند الضغط على Esc

        self.board_size = 3
        self.board = [""] * (self.board_size ** 2)
        self.buttons = []
        self.current_player = "player1"
        self.current_round = 0
        self.round_limit = 5  # الحد الأقصى للجولات
        self.total_matches = 0
        self.rounds_played = 0
        self.currency = 0
        self.score = {"player1": 0, "player2": 0}
        self.player_names = ["اللاعب 1", "اللاعب 2"]  # الأسماء المبدئية
        self.vs_computer = False  # متغير للتحكم في اللعب ضد الكمبيوتر
        self.current_skin = 0
        self.start_time = None  # لقياس الوقت الذي تم قضاؤه في اللعب
        self.entry_time = time.time()  # إضافة المؤقت عند دخول التطبيق
        self.load_data()

    def load_data(self):
        try:
            with open(save_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                self.currency = int(lines[0].strip().split(":")[1].strip())
                self.total_matches = int(lines[1].strip().split(":")[1].strip())
        except FileNotFoundError:
            self.currency = 0
            self.total_matches = 0

    def save_data(self):
        with open(save_file, "w", encoding="utf-8") as f:
            f.write(f"Currency: {self.currency}\n")
            f.write(f"Total Matches: {self.total_matches}\n")
            f.write(f"Player1: {self.score['player1']}\n")
            f.write(f"Player2: {self.score['player2']}\n")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def draw_board(self):
        self.clear_window()
        self.add_back_button()

        p1, p2 = skins[self.current_skin][:2]  # استخدام السكين الحالي
        tk.Label(self.root, text=f"{p1}: {self.score['player1']}  |  {p2}: {self.score['player2']}",
                 font=("Arial", 18, "bold"), fg="#FF5733", bg="#2C3E50").pack(pady=20)
        tk.Label(self.root, text=f"العملات: {self.currency} 💸", font=("Arial", 14), fg="#FF5733", bg="#2C3E50").pack(
            pady=10)

        if self.round_limit:
            tk.Label(self.root, text=f"الجولة {self.current_round + 1}/{self.round_limit}", font=("Arial", 14),
                     fg="#FF5733", bg="#2C3E50").pack(pady=10)

        frame = tk.Frame(self.root, bg="#2C3E50")
        frame.pack(pady=20)
        self.buttons = []
        for i in range(self.board_size ** 2):
            btn = tk.Button(frame, text="", width=10, height=4, font=("Arial", 24, "bold"), fg="black", bg="#34495E",
                            highlightbackground="#FF5733", command=lambda i=i: self.cell_clicked(i), relief="raised",
                            bd=3)
            btn.grid(row=i // self.board_size, column=i % self.board_size, padx=5, pady=5)
            btn.bind("<Enter>", lambda event, b=btn: b.config(bg="#FF5733", fg="white", relief="sunken"))
            btn.bind("<Leave>", lambda event, b=btn: b.config(bg="#34495E", fg="black", relief="raised"))
            self.buttons.append(btn)

    def add_back_button(self):
        back_button = tk.Button(self.root, text="العودة إلى القائمة الرئيسية", command=self.main_menu,
                                font=("Arial", 16, "bold"),
                                fg="black", bg="#2980B9", highlightbackground="#2980B9", relief="raised", bd=3,
                                width=20, height=3)
        back_button.pack(pady=20)

    def add_exit_button(self):
        exit_button = tk.Button(self.root, text="خروج", command=self.root.quit, font=("Arial", 16, "bold"), fg="black",
                                bg="#D9534F", highlightbackground="#D9534F", relief="raised", bd=3, width=20, height=3)
        exit_button.pack(pady=20)

    def cell_clicked(self, index):
        if self.board[index]:
            return  # إذا كانت الخلية ممتلئة، لا شيء يحدث

        mark = skins[self.current_skin][0 if self.current_player == "player1" else 1]
        self.board[index] = self.current_player
        self.buttons[index].config(text=mark)  # تحديث النص على الزر

        # تحقق إذا فاز اللاعب الحالي
        if self.check_win(self.current_player):
            winner_name = self.player_names[0 if self.current_player == "player1" else 1]
            messagebox.showinfo("فوز", f"🎉 {winner_name} فاز!")
            self.score[self.current_player] += 1
            self.currency += 10  # إضافة عملة عند الفوز
            self.current_round += 1
            self.total_matches += 1
            self.rounds_played += 1
            self.currency += 10  # زيادة المال بمقدار 10 بعد كل جولة
            self.check_round_limit()
            self.reset_game()
        elif "" not in self.board:
            messagebox.showinfo("تعادل", "🤝 تعادل!")
            self.current_round += 1
            self.rounds_played += 1
            self.currency += 10  # زيادة المال بمقدار 10 بعد كل جولة
            self.check_round_limit()
            self.reset_game()
        else:
            # تغيير الدور بين اللاعبين
            self.current_player = "player2" if self.current_player == "player1" else "player1"

            if self.vs_computer and self.current_player == "player2":
                self.computer_move()

    def check_round_limit(self):
        if self.current_round >= self.round_limit:
            self.currency += 50  # إضافة 50 عملة عندما تنتهي الجولات
            messagebox.showinfo("نهاية اللعبة", "لقد انتهت الجولات! العودة إلى القائمة الرئيسية.")
            self.main_menu()  # العودة إلى القائمة الرئيسية

    def reset_game(self):
        # إعادة تعيين اللعبة بعد الفوز أو التعادل
        self.board = [""] * (self.board_size ** 2)
        self.draw_board()

    def computer_move(self):
        empty_cells = [i for i in range(len(self.board)) if self.board[i] == ""]
        index = random.choice(empty_cells)  # اختيار حركة عشوائية من الخلايا المتاحة
        self.cell_clicked(index)  # محاكاة نقرة على الخلية المختارة من الكمبيوتر

    def check_win(self, player):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # صفوف
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # أعمدة
            [0, 4, 8], [2, 4, 6]  # القطرين
        ]
        for condition in win_conditions:
            if all(self.board[i] == player for i in condition):
                return True
        return False

    def store_menu(self):
        self.clear_window()
        self.add_back_button()

        tk.Label(self.root, text="اختر سكينك", font=("Arial", 24, "bold"), fg="#FF5733", bg="#2C3E50").pack(pady=20)

        for idx, (p1, p2, price) in enumerate(skins):
            tk.Button(self.root, text=f"السكين {idx + 1} - السعر: {price} عملات",
                      command=lambda idx=idx: self.select_skin(idx), font=("Arial", 14), fg="black", bg="#34495E",
                      highlightbackground="#FF5733", relief="raised", bd=3, width=20, height=3).pack(pady=10)

    def select_skin(self, idx):
        price = skins[idx][2]
        if self.currency >= price:
            self.currency -= price  # خصم العملة
            self.current_skin = idx
            messagebox.showinfo("تم اختيار السكين", f"لقد اخترت السكين: {skins[idx][0]}")
        else:
            messagebox.showwarning("عدم كفاية العملات", "ليس لديك عملات كافية!")

    def main_menu(self):
        self.clear_window()
        self.add_exit_button()

        tk.Label(self.root, text="مرحبًا في مشروع XO", font=("Arial", 32, "bold"), fg="#FF5733", bg="#2C3E50").pack(pady=20)
        tk.Button(self.root, text="العب ضد الكمبيوتر", command=self.play_computer, font=("Arial", 18), fg="black",
                  bg="#2980B9", relief="raised", bd=3, width=20, height=3).pack(pady=10)
        tk.Button(self.root, text="العب لاعبين", command=self.two_players_mode, font=("Arial", 18),
                  fg="black", bg="#2980B9", relief="raised", bd=3, width=20, height=3).pack(pady=10)
        tk.Button(self.root, text="المتجر", command=self.store_menu, font=("Arial", 18), fg="black", bg="#2980B9",
                  relief="raised", bd=3, width=20, height=3).pack(pady=10)
        tk.Button(self.root, text="معلومات عن اللعبة", command=self.show_info, font=("Arial", 18), fg="black", bg="#2980B9",
                  relief="raised", bd=3, width=20, height=3).pack(pady=10)

        # عرض الوقت عند دخول التطبيق
        elapsed_time = time.time() - self.entry_time
        tk.Label(self.root, text=f"الوقت المستغرق: {elapsed_time:.2f} ثانية", font=("Arial", 14), fg="#FF5733",
                 bg="#2C3E50").pack(pady=10)

    def play_computer(self):
        self.vs_computer = True
        self.player_names = ["اللاعب", "الكمبيوتر"]
        self.round_limit = 5
        self.start_game()

    def two_players_mode(self):
        self.vs_computer = False
        self.round_limit = 5
        self.start_game()

    def start_game(self):
        self.clear_window()
        self.start_time = time.time()  # بدء وقت اللعبة
        self.current_round = 0
        self.score = {"player1": 0, "player2": 0}
        self.board = [""] * (self.board_size ** 2)
        self.draw_board()

    def show_info(self):
        # حساب الوقت الذي تم فيه تسجيل الدخول
        entry_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.entry_time))
        elapsed_time = time.time() - self.entry_time
        info_text = f"تم تسجيل دخولك في: {entry_time_str}\n\n"
        info_text += f"عدد المباريات التي لعبتها: {self.total_matches}\n"
        info_text += f"عدد المباريات الحالية: {self.rounds_played}\n"
        info_text += f"عدد الانتصارات للاعب 1: {self.score['player1']}\n"
        info_text += f"عدد الانتصارات للاعب 2: {self.score['player2']}\n"
        info_text += f"الوقت المستغرق في اللعبة: {elapsed_time:.2f} ثانية\n"
        info_text += f"العملات المتاحة: {self.currency}\n"

        messagebox.showinfo("معلومات اللعبة", info_text)

    def toggle_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))
        return "break"

    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)
        return "break"


# بدء التطبيق
root = tk.Tk()
game = TicTacToeGame(root)
game.main_menu()
root.mainloop()
