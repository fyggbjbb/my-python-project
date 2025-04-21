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
            command=lambda: self.process_data(self.controller.uploaded_file_path)
        ).pack(pady=20)

    def process_data(self, file_path):
        data_handler = DataHandler()
        try:
            # 读取数据
            data = data_handler.read_csv_file(file_path)
            # 选择需要的特征
            features = ['年纪', '性别', '购买金额', '历史购买次数', '购买频率']
            data = data[features]
            # 删除包含缺失值的行
            data = data.dropna(subset=features)
            self.processed_data = data
            messagebox.showinfo("提示", "数据处理成功")
            # 将处理后的数据传递给 DataCRUDModule
            data_crud_module = DataCRUDModule(self, self.controller)
            data_crud_module.receive_processed_data(self.processed_data)
        except Exception as e:
            messagebox.showerror("错误", f"数据处理失败: {str(e)}")
