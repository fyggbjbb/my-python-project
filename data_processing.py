import tkinter as tk
from tkinter import messagebox
from utils.data_handler import DataHandler
from data_crud import DataCRUDModule

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

    def process_data(self, file_path):
        data_handler = DataHandler()
        try:
            self.processed_data = data_handler.handle_data(file_path)
            messagebox.showinfo("提示", "数据处理成功")
            return self.processed_data
        except Exception as e:
            messagebox.showerror("错误", f"数据处理失败: {str(e)}")

