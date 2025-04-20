import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文显示问题


class VisualizationModule(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        # 标题
        tk.Label(self, text="特征可视化", font=("Helvetica", 18, "bold"), bg="white").pack(pady=20)

        # 绘图区域
        self.figure = plt.figure(figsize=(12, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(pady=20, fill=tk.BOTH, expand=True)

        # 绘制按钮
        tk.Button(
            self,
            text="绘制特征分布图",
            command=self.plot_features,
            bg="#FF5722", fg="white"
        ).pack(pady=10)

        # 返回按钮
        tk.Button(
            self,
            text="返回数据预处理",
            command=lambda: self.controller.show_page("DataProcessingPage"),
            bg="#607D8B", fg="white"
        ).pack(pady=15)

    def plot_features(self):
        self.data = self.controller.preprocess_result
        if self.data is None:
            messagebox.showerror("错误", "未获取到数据，请先上传数据并预处理")
            return
        required_cols = ["age", "purchase_history", "target_label"]
        if not all(col in self.data.columns for col in required_cols):
            messagebox.showerror("错误", f"数据缺少必要列：{required_cols}，请检查文件")
            return
        self.figure.clear()

        # 子图1：年龄分布直方图
        ax1 = self.figure.add_subplot(1, 2, 1)
        age_data = self.data["age"]
        ax1.hist(age_data, bins=20, color="#3498db", edgecolor="white", alpha=0.7)
        ax1.set_title("年龄分布", fontsize=14)
        ax1.set_xlabel("年龄", fontsize=12)
        ax1.set_ylabel("频数", fontsize=12)

        # 子图2：购买历史箱线图（按目标标签分组）
        ax2 = self.figure.add_subplot(1, 2, 2)
        target_labels = self.data["target_label"].unique()
        if len(target_labels) < 2:
            messagebox.showerror("错误", "目标标签分类不足，无法绘制箱线图")
            return
        self.data.boxplot(
            column="purchase_history",
            by="target_label",
            ax=ax2,
            patch_artist=True,
            medianprops={'color': 'black'},
            whiskerprops={'color': 'black'},
            capprops={'color': 'black'}
        )
        colors = ['#e74c3c', '#2ecc71']  # 可根据实际目标标签数量扩展
        for i, patch in enumerate(ax2.artists):
            patch.set_facecolor(colors[i % len(colors)])

        ax2.set_title("不同目标标签的购买历史对比", fontsize=14)
        ax2.set_xlabel("目标标签", fontsize=12)
        ax2.set_ylabel("购买金额", fontsize=12)
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)

        self.canvas.draw()
