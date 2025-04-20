import tkinter as tk
from tkinter import messagebox, filedialog


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

    def upload_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV文件", "*.csv")])
        if not file_path:
            messagebox.showwarning(title="提示", message="未选择文件")
            return
        try:
            self.controller.set_file_path(file_path)
            self.status_label.config(text="文件上传成功")
        except Exception as e:
            messagebox.showerror(title="错误", message=f"上传失败: {str(e)}")
