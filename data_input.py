import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
from tkinter import ttk

class DataInputModule(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='white')

        tk.Label(self, text="数据输入模块", font=("Helvetica", 20, "bold"), bg="white").pack(pady=20)

        tk.Button(
            self,
            text="点击上传CSV数据文件",
            font=("Helvetica", 14),
            command=self.upload_data
        ).pack(pady=50)

        self.status_label = tk.Label(self, text="", bg="white", font=("Helvetica", 14))
        self.status_label.pack(pady=20)

        # 初始化表格
        self.data_tree = None

    def upload_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV文件", "*.csv")])
        if not file_path:
            messagebox.showwarning(title="提示", message="未选择文件")
            return
        try:
            # 调用 set_file_path 方法设置 file_path 属性
            self.controller.set_file_path(file_path)
            self.status_label.config(text="文件上传成功")

            # 读取数据
            data = pd.read_csv(file_path, encoding='gbk')

            # 显示前 5 行数据
            self.show_top_five_rows(data)

        except Exception as e:
            messagebox.showerror(title="错误", message=f"上传失败: {str(e)}")

    def show_top_five_rows(self, data):
        # 如果表格已经存在，先销毁
        if self.data_tree:
            self.data_tree.destroy()

        # 获取数据的列名
        columns = data.columns.tolist()

        # 创建表格
        self.data_tree = ttk.Treeview(self, columns=columns, show="headings")

        # 设置列标题
        for col in columns:
            self.data_tree.heading(col, text=col, anchor=tk.CENTER)
            self.data_tree.column(col, width=100)

        # 插入前 5 行数据
        for index, row in data.head(5).iterrows():
            self.data_tree.insert("", tk.END, values=list(row))

        # 显示表格
        self.data_tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)