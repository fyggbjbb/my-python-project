import tkinter as tk
from tkinter import messagebox
from sklearn.linear_model import LogisticRegression
from utils.model_handler import train_model  # 假设此工具函数接收 X, y 训练模型


class PredictionPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.model = None  # 存储训练好的模型

        self.configure(bg="#f5f5f5")
        self.model_var=tk.StringVar(value="LogisticRegression")
        tk.OptionMenu(self,self.model_var,"LogisticRegression","RandomForest").pack(pady=5)

        # 标题
        tk.Label(self, text="预测模块", font=("Helvetica", 18, "bold"), bg="#f5f5f5").pack(pady=20)

        # 模型选择（示例：简单固定逻辑回归，可根据需求扩展）
        tk.Label(self, text="当前模型：逻辑回归", bg="#f5f5f5").pack(pady=5)
        tk.OptionMenu(self,self.model_var,"LogisticRegession","RandomForest").pack(pady=5)

        # 训练模型按钮
        tk.Button(
            self,
            text="训练模型",
            bg="#4CAF50",
            fg="white",
            command=self.train_model
        ).pack(pady=10)

        # 特征输入区域
        tk.Label(self, text="输入特征（用逗号分隔，按预处理后的特征顺序）:", bg="#f5f5f5").pack(pady=10)
        self.feature_input = tk.Entry(self, width=50)
        self.feature_input.pack(pady=5)
        tk.Button(
            self,
            text="进行预测",
            bg="#2196F3",
            fg="white",
            command=self.make_prediction
        ).pack(pady=10)


    def make_prediction(self):
        if self.model is None:
            messagebox.showerror("错误", "请先训练模型！")
            return
        try:
            # 处理输入特征
            feature_str = self.feature_input.get().strip()
            if not feature_str:
                raise ValueError("特征输入不能为空")
            features = [float(x.strip()) for x in feature_str.split(",")]
            # 进行预测（假设模型接口为 predict）
            prediction = self.model.predict([features])
            messagebox.showinfo("预测结果", f"预测结果为：{prediction[0]}")
        except ValueError as ve:
            messagebox.showerror("输入错误", f"特征输入格式不正确：{str(ve)}")
        except Exception as e:
            messagebox.showerror("预测错误", f"预测过程中出现异常：{str(e)}")