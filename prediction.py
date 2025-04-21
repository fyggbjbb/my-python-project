import tkinter as tk
from tkinter import messagebox
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from utils.model_handler import train_model  # 假设此工具函数接收 X, y 训练模型

class PredictionPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.model = None  # 存储训练好的模型

        self.configure(bg="#f5f5f5")
        self.model_var = tk.StringVar(value="LogisticRegression")
        tk.OptionMenu(self, self.model_var, "LogisticRegression", "RandomForest").pack(pady=5)

        # 标题
        tk.Label(self, text="预测模块", font=("Helvetica", 18, "bold"), bg="#f5f5f5").pack(pady=20)

        # 模型选择（示例：简单固定逻辑回归，可根据需求扩展）
        tk.Label(self, text="当前模型：逻辑回归", bg="#f5f5f5").pack(pady=5)
        tk.OptionMenu(self, self.model_var, "LogisticRegression", "RandomForest").pack(pady=5)

        # 训练模型按钮
        tk.Button(
            self,
            text="训练模型",
            bg="#4CAF50",
            fg="white",
            command=self.train_model
        ).pack(pady=10)

        # 特征输入区域
        features = ['年纪', '性别', '购买金额', '历史购买次数', '购买频率']
        for feature in features:
            tk.Label(self, text=f"{feature}:", bg="#f5f5f5").pack(pady=5)
            setattr(self, f"{feature}_entry", tk.Entry(self, width=50))
            getattr(self, f"{feature}_entry").pack(pady=5)

        tk.Button(
            self,
            text="进行预测",
            bg="#2196F3",
            fg="white",
            command=self.make_prediction
        ).pack(pady=10)

    def train_model(self):
        if self.controller.processed_data is None:
            messagebox.showerror("错误", "请先进行数据处理！")
            return
        X, y = self.controller.processed_data
        model_name = self.model_var.get()
        if model_name == "LogisticRegression":
            self.model = LogisticRegression()
        elif model_name == "RandomForest":
            self.model = RandomForestClassifier()
        self.model.fit(X, y)
        messagebox.showinfo("成功", "模型训练成功！")

    def make_prediction(self):
        if self.model is None:
            messagebox.showerror("错误", "请先训练模型！")
            return
        try:
            features = ['年纪', '性别', '购买金额', '历史购买次数', '购买频率']
            input_features = []
            for feature in features:
                value = float(getattr(self, f"{feature}_entry").get().strip())
                input_features.append(value)
            prediction = self.model.predict([input_features])
            messagebox.showinfo("预测结果", f"预测结果为：{prediction[0]}")
        except ValueError as ve:
            messagebox.showerror("输入错误", f"特征输入格式不正确：{str(ve)}")
        except Exception as e:
            messagebox.showerror("预测错误", f"预测过程中出现异常：{str(e)}")