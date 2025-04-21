# visualization.py
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
        tk.Label(self, text="数据可视化", font=("Helvetica", 18, "bold"), bg="white").pack(pady=20)

        # 绘图区域
        self.figure = plt.figure(figsize=(14, 12))
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(pady=20, fill=tk.BOTH, expand=True)

        # 绘制按钮
        tk.Button(
            self,
            text="绘制分析图表",
            command=self.plot_analysis_charts,
            bg="#FF5722", fg="white",
            font=("Helvetica", 14)
        ).pack(pady=10)

        # 返回按钮
        tk.Button(
            self,
            text="返回数据分析",
            command=lambda: self.controller.show_page("DataCRUDModule"),
            bg="#607D8B", fg="white",
            font=("Helvetica", 14)
        ).pack(pady=15)

    def plot_analysis_charts(self):
        self.data = self.controller.processed_data  # 获取处理后的数据
        if self.data is None:
            messagebox.showerror("错误", "未获取到数据，请先进行数据处理")
            return

        X, _ = self.data
        required_cols = ["性别", "年纪区间", "金额区间", "RepeatPurchase", "购买次数区间", "购买频率"]
        if not all(col in X.columns for col in required_cols):
            messagebox.showerror("错误", f"数据缺少必要列：{required_cols}")
            return

        self.figure.clear()

        # 子图1-4：四个饼状图
        ax1 = self.figure.add_subplot(2, 2, 1)
        self.plot_pie_chart(ax1, X["性别"], "男女比例", ["男性", "女性"])

        ax2 = self.figure.add_subplot(2, 2, 2)
        self.plot_pie_chart(ax2, X["年纪区间"], "年纪分布")

        ax3 = self.figure.add_subplot(2, 2, 3)
        self.plot_pie_chart(ax3, X["金额区间"], "购买金额区间分布")

        ax4 = self.figure.add_subplot(2, 2, 4)
        self.plot_pie_chart(ax4, X["RepeatPurchase"], "复购占比", ["不复购", "复购"])

        # 补充图表：历史购买次数区间柱状图（子图5）
        ax5 = self.figure.add_subplot(3, 2, 5)
        purchase_counts = X["购买次数区间"].value_counts().sort_index()
        ax5.bar(purchase_counts.index, purchase_counts.values, color="#3498db")
        ax5.set_title("历史购买次数分布")
        ax5.set_xlabel("购买次数区间")
        ax5.set_ylabel("人数")

        # 补充图表：购买频率条形图（子图6）
        ax6 = self.figure.add_subplot(3, 2, 6)
        frequency_counts = X["购买频率"].value_counts().sort_index()
        ax6.barh(frequency_counts.index, frequency_counts.values, color="#2ecc71")
        ax6.set_title("购买频率分布")
        ax6.set_xlabel("人数")
        ax6.set_ylabel("购买频率（编码后）")

        plt.tight_layout(pad=3)
        self.canvas.draw()

    def plot_pie_chart(self, ax, data, title, labels=None):
        """通用饼图绘制函数"""
        counts = data.value_counts()
        if labels is None:
            labels = counts.index
        ax.pie(counts, labels=labels, autopct="%1.1f%%", startangle=90, colors=["#3498db", "#e74c3c", "#2ecc71", "#9b59b6"])
        ax.set_title(title)