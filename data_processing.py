import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import pandas as pd
import chardet  # 导入 chardet 库


class DataCRUDModule:
    def __init__(self, main_interface, controller):
        self.main_interface = main_interface
        self.controller = controller

    def receive_processed_data(self, data):
        pass


class DataHandler:
    def read_csv_file(self, file_path):
        try:
            # 自动检测文件编码
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                encoding = result['encoding']

            # 使用检测到的编码读取文件
            return pd.read_csv(file_path, encoding=encoding)
        except Exception as e:
            messagebox.showerror("错误", f"读取文件失败: {str(e)}")
            return None


class DataProcessingModule(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.processed_data = None
        self.data_crud_module = controller.data_crud_module

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
        data = data_handler.read_csv_file(file_path)
        if data is None:
            return
        try:
            # 保留指定的 5 个特征
            features = ['年纪', '性别', '购买金额', '历史购买次数', '购买频率']
            data = data[features]
            # 删除有缺失项的行
            data = data.dropna()
            self.processed_data = data
            messagebox.showinfo("提示", "数据处理成功")
            if self.data_crud_module:
                self.data_crud_module.receive_processed_data(self.processed_data)
            self.show_top_five_rows(data)
        except Exception as e:
            messagebox.showerror("错误", f"数据处理失败: {str(e)}")

    def show_top_five_rows(self, data):
        # 获取数据的列名
        columns = data.columns.tolist()

        if self.data_tree is None:
            # 创建表格
            self.data_tree = ttk.Treeview(self, columns=columns, show="headings")

            # 设置列标题
            for col in columns:
                self.data_tree.heading(col, text=col, anchor=tk.CENTER)
                self.data_tree.column(col, width=100)

            # 显示表格
            self.data_tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # 清空表格
        for i in self.data_tree.get_children():
            self.data_tree.delete(i)

        # 插入前 5 行数据
        for index, row in data.head(5).iterrows():
            self.data_tree.insert("", tk.END, values=list(row))


class Controller:
    def __init__(self, main_interface):
        self.main_interface = main_interface
        self.file_path = None
        self.uploaded_data = None
        self.data_crud_module = DataCRUDModule(main_interface, self)
        self.processed_data = None
        self.data_processing_module = DataProcessingModule(main_interface, self)

    def handle_data_processing(self):
        if not self.file_path:
            tk.messagebox.showerror("错误", "未上传文件，请先上传文件")
            return
        self.data_processing_module.process_data(self.file_path)
        self.processed_data = self.data_processing_module.processed_data


