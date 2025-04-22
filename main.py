import tkinter as tk
from login import LoginPage
from main_interface import MainInterface

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.uploaded_data = None
        self.title("消费者行为预测系统")
        self.geometry("1200x800")

        self.login_window = LoginPage(self, self)
        self.login_window.pack(fill=tk.BOTH, expand=True)

    def show_main_interface(self):
        self.login_window.pack_forget()
        self.main_interface = MainInterface(self)
        self.main_interface.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()