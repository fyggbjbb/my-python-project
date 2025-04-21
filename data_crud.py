import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd


class DataCRUDModule(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

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

        # 数据表格
        self.data_tree = ttk.Treeview(self, columns=("年纪", "性别", "购买金额", "历史购买次数", "购买频率"), show="headings")
        self.data_tree.heading("年纪", text="年纪", anchor=tk.CENTER)
        self.data_tree.heading("性别", text="性别", anchor=tk.CENTER)
        self.data_tree.heading("购买金额", text="购买金额", anchor=tk.CENTER)
        self.data_tree.heading("历史购买次数", text="历史购买次数", anchor=tk.CENTER)
        self.data_tree.heading("购买频率", text="购买频率", anchor=tk.CENTER)
        self.data_tree.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

    def update_data_table(self):
        """更新数据表格"""
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        if self.controller.uploaded_data is not None:
            features = ['年纪', '性别', '购买金额', '历史购买次数', '购买频率']
            if all(col in self.controller.uploaded_data.columns for col in features):
                for _, row in self.controller.uploaded_data[features].iterrows():
                    self.data_tree.insert("", tk.END, values=list(row))

    def perform_analysis(self):
        if self.controller.uploaded_data is None:
            messagebox.showerror("错误", "请先上传数据", icon="error")
            return
        features = ['年纪', '性别', '购买金额', '历史购买次数', '购买频率']
        if not all(col in self.controller.uploaded_data.columns for col in features):
            messagebox.showerror("错误", "数据缺少必要列，请检查文件", icon="error")
            return

        data = self.controller.uploaded_data[features]
        # 删除包含缺失值的行
        data = data.dropna(subset=['年纪'])

        age_distribution_str = self.calculate_age_distribution(data)
        gender_ratio = self.calculate_gender_ratio(data)
        amount_distribution_str = self.calculate_amount_distribution(data)
        purchase_distribution_str = self.calculate_purchase_distribution(data)
        frequency_distribution_str = self.calculate_frequency_distribution(data)

        analysis_result = f"年纪区间分布占比:\n{age_distribution_str}\n\n" \
                          f"男性和女性的人数比值: {gender_ratio}\n\n" \
                          f"购买金额区间及占比:\n{amount_distribution_str}\n\n" \
                          f"历史购买次数区间及占比:\n{purchase_distribution_str}\n\n" \
                          f"购买频率分布占比:\n{frequency_distribution_str}"

        messagebox.showinfo("数据分析结果", analysis_result)

    def calculate_age_distribution(self, data):
        age_bins = [i for i in range(0, int(data['年纪'].max()) + 10, 10)]
        age_labels = [f"{i}-{i + 9}" for i in age_bins[:-1]] + [f"{age_bins[-1]}以上"]
        data['年纪区间'] = pd.cut(data['年纪'], bins=age_bins, labels=age_labels)
        age_distribution = data['年纪区间'].value_counts(normalize=True)
        return "\n".join([f"年纪区间 {interval}: {ratio * 100:.2f}%" for interval, ratio in age_distribution.items()])

    def calculate_gender_ratio(self, data):
        gender_counts = data['性别'].value_counts()
        male_count = gender_counts.get('男', 0)
        female_count = gender_counts.get('女', 0)
        if female_count == 0:
            return "女性人数为0，无法计算比值"
        else:
            return f"男性:女性 = {male_count / female_count:.2f}:1"

    def calculate_amount_distribution(self, data):
        amount_bins = [0, 50, 100, float('inf')]
        amount_labels = ['0-50', '51-100', '100以上']
        data['金额区间'] = pd.cut(data['购买金额'], bins=amount_bins, labels=amount_labels)
        amount_distribution = data['金额区间'].value_counts(normalize=True)
        return "\n".join([f"金额区间 {interval}: {ratio * 100:.2f}%" for interval, ratio in amount_distribution.items()])

    def calculate_purchase_distribution(self, data):
        purchase_bins = [0, 10, 20, 30, 40, float('inf')]
        purchase_labels = ['0-10', '11-20', '21-30', '31-40', '40以上']
        data['购买次数区间'] = pd.cut(data['历史购买次数'], bins=purchase_bins, labels=purchase_labels)
        purchase_distribution = data['购买次数区间'].value_counts(normalize=True)
        return "\n".join([f"历史购买次数区间 {interval}: {ratio * 100:.2f}%" for interval, ratio in purchase_distribution.items()])

    def calculate_frequency_distribution(self, data):
        frequency_distribution = data['购买频率'].value_counts(normalize=True)
        return "\n".join([f"购买频率 {frequency}: {ratio * 100:.2f}%" for frequency, ratio in frequency_distribution.items()])

    def receive_processed_data(self, processed_data):
        # 检查 processed_data 的类型和结构
        if isinstance(processed_data, tuple) and len(processed_data) == 2:
            X, y = processed_data
            self.controller.uploaded_data = pd.concat([X, y], axis=1)
            self.update_data_table()
        else:
            # 处理不符合预期的数据
            messagebox.showerror("错误", "处理后的数据格式不符合预期")