import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class DataVisualizer:
    def __init__(self):
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    
    def load_analyzed_data(self, filename="analyzed_data.csv"):
        print(f"加载分析后的数据: {filename}")
        return pd.read_csv(filename)
    
    def plot_trends(self, df):
        print("生成趋势图...")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # 总确诊病例趋势
        axes[0, 0].plot(df['date'], df['total_cases'], marker='o', color='blue')
        axes[0, 0].set_title('总确诊病例趋势')
        axes[0, 0].set_xlabel('日期')
        axes[0, 0].set_ylabel('病例数')
        axes[0, 0].grid(True)
        
        # 每日新增病例
        axes[0, 1].bar(df['date'], df['new_cases'], color='red')
        axes[0, 1].plot(df['date'], df['new_cases_ma'], color='green', linestyle='--', linewidth=2)
        axes[0, 1].set_title('每日新增病例')
        axes[0, 1].set_xlabel('日期')
        axes[0, 1].set_ylabel('新增病例数')
        axes[0, 1].grid(True)
        
        # 康复率趋势
        axes[1, 0].plot(df['date'], df['recovery_rate'], marker='s', color='green')
        axes[1, 0].set_title('康复率趋势')
        axes[1, 0].set_xlabel('日期')
        axes[1, 0].set_ylabel('康复率 (%)')
        axes[1, 0].grid(True)
        
        # 隔离人数
        axes[1, 1].plot(df['date'], df['quarantined'], marker='^', color='orange')
        axes[1, 1].set_title('隔离人数趋势')
        axes[1, 1].set_xlabel('日期')
        axes[1, 1].set_ylabel('隔离人数')
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        plt.savefig('trend_plots.png')
        print("趋势图已保存为 trend_plots.png")
    
    def plot_pie_chart(self, df):
        print("生成饼图...")
        
        # 最新数据
        latest_data = df.iloc[-1]
        active_cases = latest_data['active_cases']
        recovered = latest_data['recovered']
        
        labels = ['活跃病例', '已康复']
        sizes = [active_cases, recovered]
        colors = ['#ff9999', '#99ff99']
        explode = (0.1, 0)
        
        plt.figure(figsize=(8, 6))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')
        plt.title('病例状态分布')
        plt.savefig('pie_chart.png')
        print("饼图已保存为 pie_chart.png")
    
    def plot_correlation_heatmap(self, df):
        print("生成相关性热力图...")
        
        numeric_cols = ['total_cases', 'new_cases', 'recovered', 'quarantined', 'active_cases']
        corr = df[numeric_cols].corr()
        
        plt.figure(figsize=(10, 8))
        plt.imshow(corr, cmap='coolwarm', interpolation='nearest')
        plt.colorbar()
        plt.xticks(np.arange(len(numeric_cols)), numeric_cols, rotation=45)
        plt.yticks(np.arange(len(numeric_cols)), numeric_cols)
        plt.title('数据相关性热力图')
        
        # 添加相关系数
        for i in range(len(numeric_cols)):
            for j in range(len(numeric_cols)):
                plt.text(j, i, f"{corr.iloc[i, j]:.2f}", ha='center', va='center', color='white' if abs(corr.iloc[i, j]) > 0.5 else 'black')
        
        plt.tight_layout()
        plt.savefig('correlation_heatmap.png')
        print("相关性热力图已保存为 correlation_heatmap.png")

if __name__ == "__main__":
    visualizer = DataVisualizer()
    analyzed_df = visualizer.load_analyzed_data()
    visualizer.plot_trends(analyzed_df)
    visualizer.plot_pie_chart(analyzed_df)
    visualizer.plot_correlation_heatmap(analyzed_df)