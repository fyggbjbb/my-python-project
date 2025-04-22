import tkinter as tk
from tkinter import messagebox
from utils.data_handler import DataHandler
from data_crud import DataCRUDModule
from tkinter import ttk
import pandas as pd

class DataProcessingModule(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.processed_data = None

        # 标题
        tk.Label(self, text="数据处理模块", font=("Helvetica", 20, "bold"), bg="white").pack(pady=20)

        # 添加数据处理按钮
        tk.Button(
            self,
            text="处理数据",
            bg="#4CAF50",
            fg="white",
            font=("Helvetica", 14),
            command=lambda: self.process_data(self.controller.file_path)
        ).pack(pady=20)

        # 初始化表格
        self.data_tree = None

    def process_data(self, file_path):
        data_handler = DataHandler()
        try:
            data = data_handler.read_csv_file(file_path)
            # 保留指定的 5 个特征
            features = ['年纪', '性别', '购买金额', '历史购买次数', '购买频率']
            data = data[features]
            # 删除有缺失项的行
            data = data.dropna()
            self.processed_data = data
            messagebox.showinfo("提示", "数据处理成功")
            if self.data_crud_module:
                self.data_crud_module.receive_processed_data(self.processed_data)
        except Exception as e:
            messagebox.showerror("错误", f"数据处理失败: {str(e)}")


            self.show_top_five_rows(data)

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
