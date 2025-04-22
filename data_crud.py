import tkinter as tk
from tkinter import messagebox
import pandas as pd

class DataCRUDModule(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")
        self.processed_data = None

        # 标题
        tk.Label(self, text="数据分析模块", font=("Helvetica", 20, "bold"), bg="white").pack(pady=20)

        # 数据分析按钮
        tk.Button(
            self,
            text="进行数据分析",
            bg="#4CAF50",
            fg="white",
            font=("Helvetica", 14),
            command=self.perform_analysis
        ).pack(pady=20)

    def receive_processed_data(self, data):
        self.processed_data = data

    def perform_analysis(self):
        if self.processed_data is None:
            messagebox.showerror("错误", "请先进行数据处理", icon="error")
            return

        data = self.processed_data

        # 年纪区间及占比
        age_bins = [i for i in range(0, int(data['年纪'].max()) + 10, 10)]
        age_labels = [f"{i}-{i + 9}" for i in age_bins[:-1]] + [f"{age_bins[-1]}以上"]
        data['年纪区间'] = pd.cut(data['年纪'], bins=age_bins, labels=age_labels)
        age_distribution = data['年纪区间'].value_counts(normalize=True)
        age_distribution_str = "\n".join([f"年纪区间 {interval}: {ratio * 100:.2f}%" for interval, ratio in age_distribution.items()])

        # 男性和女性的人数比值
        gender_counts = data['性别'].value_counts()
        male_count = gender_counts.get('男', 0)
        female_count = gender_counts.get('女', 0)
        if female_count == 0:
            gender_ratio = "女性人数为0，无法计算比值"
        else:
            gender_ratio = f"男性:女性 = {male_count / female_count:.2f}:1"

        # 购买金额区间及占比
        amount_bins = [0, 50, 100, float('inf')]
        amount_labels = ['0-50', '51-100', '100以上']
        data['金额区间'] = pd.cut(data['购买金额'], bins=amount_bins, labels=amount_labels)
        amount_distribution = data['金额区间'].value_counts(normalize=True)
        amount_distribution_str = "\n".join([f"金额区间 {interval}: {ratio * 100:.2f}%" for interval, ratio in amount_distribution.items()])

        # 历史购买次数区间及占比
        purchase_bins = [0, 10, 20, 30, 40, float('inf')]
        purchase_labels = ['0-10', '11-20', '21-30', '31-40', '40以上']
        data['购买次数区间'] = pd.cut(data['历史购买次数'], bins=purchase_bins, labels=purchase_labels)
        purchase_distribution = data['购买次数区间'].value_counts(normalize=True)
        purchase_distribution_str = "\n".join([f"历史购买次数区间 {interval}: {ratio * 100:.2f}%" for interval, ratio in purchase_distribution.items()])

        # 购买频率分布占比
        frequency_distribution = data['购买频率'].value_counts(normalize=True)
        frequency_distribution_str = "\n".join([f"购买频率 {frequency}: {ratio * 100:.2f}%" for frequency, ratio in frequency_distribution.items()])

        analysis_result = f"年纪区间分布占比:\n{age_distribution_str}\n\n" \
                          f"男性和女性的人数比值: {gender_ratio}\n\n" \
                          f"购买金额区间及占比:\n{amount_distribution_str}\n\n" \
                          f"历史购买次数区间及占比:\n{purchase_distribution_str}\n\n" \
                          f"购买频率分布占比:\n{frequency_distribution_str}"

        messagebox.showinfo("数据分析结果", analysis_result)