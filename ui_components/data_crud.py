import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd


class DataCRUDModule(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller  # 主控制器（MainApplication）
        self.configure(bg="white")

        # 标题
        tk.Label(self, text="数据增删查改模块", font=("Helvetica", 20, "bold"), bg="white").pack(pady=20)

        # 输入区域
        input_frame = tk.Frame(self, bg="white")
        input_frame.pack(pady=15, fill=tk.X, padx=20)

        tk.Label(input_frame, text="年龄 (age)：", bg="white", font=("Helvetica", 14)).pack(side=tk.LEFT, padx=5)
        self.age_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=15)
        self.age_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(input_frame, text="购买历史 (purchase_history)：", bg="white", font=("Helvetica", 14)).pack(
            side=tk.LEFT, padx=5)
        self.purchase_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=15)
        self.purchase_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(input_frame, text="目标标签 (target_label)：", bg="white", font=("Helvetica", 14)).pack(side=tk.LEFT,
                                                                                                        padx=5)
        self.target_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=15)
        self.target_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(
            input_frame,
            text="新增数据",
            bg="#4CAF50",
            fg="white",
            font=("Helvetica", 14),
            command=self.add_data
        ).pack(side=tk.LEFT, padx=10)

        # 数据表格
        self.data_tree = ttk.Treeview(self, columns=("age", "purchase_history", "target_label"), show="headings")
        self.data_tree.heading("age", text="年龄", anchor=tk.CENTER)
        self.data_tree.heading("purchase_history", text="购买历史", anchor=tk.CENTER)
        self.data_tree.heading("target_label", text="目标标签", anchor=tk.CENTER)
        self.data_tree.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

    def update_data_table(self):
        """更新数据表格"""
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        if self.controller.uploaded_data is not None:
            for _, row in self.controller.uploaded_data.iterrows():
                self.data_tree.insert("", tk.END, values=(row["age"], row["purchase_history"], row["target_label"]))

    def add_data(self):
        """新增数据"""
        if self.controller.uploaded_data is None:
            messagebox.showerror("错误", "请先上传数据", icon="error")
            return
        try:
            age = float(self.age_entry.get())
            purchase = float(self.purchase_entry.get())
            target = int(self.target_entry.get())
            new_row = pd.DataFrame([[age, purchase, target]], columns=["age", "purchase_history", "target_label"])
            self.controller.uploaded_data = pd.concat(
                [self.controller.uploaded_data, new_row],
                ignore_index=True
            )
            self.update_data_table()
            messagebox.showinfo("成功", "数据新增成功", icon="info")
        except ValueError:
            messagebox.showerror("错误", "请输入正确格式的数据", icon="error")