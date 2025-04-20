import tkinter as tk
from tkinter import messagebox


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller  # 主控制器（MainApplication）
        self.configure(bg="white")

        # 标题
        tk.Label(self, text="用户登录", font=("Helvetica", 24, "bold"), bg="white").pack(pady=80)

        # 用户名输入
        tk.Frame(self, bg="white").pack(pady=10)
        tk.Label(self, text="用户名：", font=("Helvetica", 14), bg="white").pack()
        self.username_entry = tk.Entry(self, font=("Helvetica", 14), width=30)
        self.username_entry.pack(pady=5)

        # 密码输入
        tk.Frame(self, bg="white").pack(pady=10)
        tk.Label(self, text="密   码：", font=("Helvetica", 14), bg="white").pack()
        self.password_entry = tk.Entry(self, font=("Helvetica", 14), width=30, show="*")
        self.password_entry.pack(pady=5)

        # 登录按钮
        tk.Button(
            self,
            text="登录系统",
            font=("Helvetica", 14),
            bg="#4CAF50",
            fg="white",
            width=20,
            height=2,
            command=self.handle_login
        ).pack(pady=30)

    def handle_login(self):
        """处理登录逻辑"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # 简单验证（实际需连接数据库）
        if username == "admin" and password == "123456":
            messagebox.showinfo("登录成功", "欢迎进入系统！", icon="info")
            self.controller.show_main_interface()  # 调用主控制器显示主界面
        else:
            messagebox.showerror("登录失败", "用户名或密码错误", icon="error")