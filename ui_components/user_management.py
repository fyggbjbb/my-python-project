import tkinter as tk
from tkinter import messagebox, ttk
import json  # 用于数据持久化


class UserManagementModule(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.users = []  # 存储用户信息

        # 从文件加载已存用户数据
        try:
            with open('users.json', 'r') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            self.users = []

        # 标题
        tk.Label(self, text="用户管理", font=("Helvetica", 18, "bold"), bg="#f9f9f9").pack(pady=20)

        # 输入框框架
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        # 用户名输入
        tk.Label(input_frame, text="用户名:").grid(row=0, column=0, padx=5)
        self.username_entry = tk.Entry(input_frame)
        self.username_entry.grid(row=0, column=1, padx=5)

        # 密码输入
        tk.Label(input_frame, text="密码:").grid(row=1, column=0, padx=5)
        self.password_entry = tk.Entry(input_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5)

        # 其他信息输入
        tk.Label(input_frame, text="其他信息:").grid(row=2, column=0, padx=5)
        self.other_info_entry = tk.Entry(input_frame)
        self.other_info_entry.grid(row=2, column=1, padx=5)

        # 添加用户按钮
        tk.Button(
            input_frame,
            text="添加用户",
            bg="#4CAF50",
            fg="white",
            command=self.add_user
        ).grid(row=3, column=0, columnspan=2, pady=10)

        # 操作框架（修改/删除）
        operate_frame = tk.Frame(self, bg="white")
        operate_frame.pack(pady=10, fill=tk.X)

        # 修改用户名标签与输入
        tk.Label(operate_frame, text="修改用户名:").pack(side=tk.LEFT, padx=5)
        self.modify_username_entry = tk.Entry(operate_frame, font=("Helvetica", 14), width=20)
        self.modify_username_entry.pack(side=tk.LEFT, padx=5)

        # 新密码标签与输入
        tk.Label(operate_frame, text="新密码:").pack(side=tk.LEFT, padx=5)
        self.new_password_entry = tk.Entry(operate_frame, font=("Helvetica", 14), width=20, show="*")
        self.new_password_entry.pack(side=tk.LEFT, padx=5)

        # 修改密码按钮
        tk.Button(
            operate_frame,
            text="修改密码",
            bg="#2196F3",
            fg="white",
            command=self.modify_password
        ).pack(side=tk.LEFT, padx=10)

        # 删除用户名标签与输入
        tk.Label(operate_frame, text="删除用户名:").pack(side=tk.LEFT, padx=5)
        self.delete_username_entry = tk.Entry(operate_frame, font=("Helvetica", 14), width=20)
        self.delete_username_entry.pack(side=tk.LEFT, padx=5)

        # 删除用户按钮
        tk.Button(
            operate_frame,
            text="删除用户",
            bg="#FF4433",
            fg="white",
            command=self.delete_user
        ).pack(side=tk.LEFT, padx=10)

        # 用户列表展示（Treeview）
        self.user_tree = ttk.Treeview(self, columns=("Username", "Password", "OtherInfo"), show="headings")
        self.user_tree.heading("Username", text="用户名", anchor=tk.CENTER)
        self.user_tree.heading("Password", text="密码", anchor=tk.CENTER)
        self.user_tree.heading("OtherInfo", text="其他信息", anchor=tk.CENTER)
        self.user_tree.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        # 初始化加载用户数据
        self.update_user_list()
    def add_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        other_info = self.other_info_entry.get().strip()

        if not username or not password:
            messagebox.showerror("错误", "用户名和密码不能为空")
            return

        self.users.append({
            "username": username,
            "password": password,
            "other_info": other_info
        })
        self.update_user_list()
        # 保存用户数据到文件
        with open('users.json', 'w') as f:
            json.dump(self.users, f)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.other_info_entry.delete(0, tk.END)
        messagebox.showinfo("成功", "用户添加成功")

    def modify_password(self):
        username = self.modify_username_entry.get().strip()
        new_password = self.new_password_entry.get().strip()

        if not username or not new_password:
            messagebox.showerror("错误", "用户名和新密码不能为空")
            return

        for user in self.users:
            if user["username"] == username:
                user["password"] = new_password
                self.update_user_list()
                # 保存更新后的数据到文件
                with open('users.json', 'w') as f:
                    json.dump(self.users, f)
                messagebox.showinfo("成功", "密码修改成功")
                return
        messagebox.showerror("错误", "用户不存在")

    def delete_user(self):
        username = self.delete_username_entry.get().strip()

        if not username:
            messagebox.showerror("错误", "用户名不能为空")
            return

        self.users = [user for user in self.users if user["username"] != username]
        self.update_user_list()
        # 保存删除后的数据到文件
        with open('users.json', 'w') as f:
            json.dump(self.users, f)
        messagebox.showinfo("成功", "用户删除成功")

    def update_user_list(self):
        # 清空Treeview
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        # 重新插入数据
        for user in self.users:
            self.user_tree.insert("", tk.END, values=(
                user["username"],
                user["password"],
                user["other_info"]
            ))