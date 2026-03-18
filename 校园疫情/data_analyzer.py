import pandas as pd
import numpy as np

class DataAnalyzer:
    def __init__(self):
        pass
    
    def load_cleaned_data(self, filename="cleaned_data.csv"):
        print(f"加载清洗后的数据: {filename}")
        return pd.read_csv(filename)
    
    def analyze_trends(self, df):
        print("开始数据分析...")
        
        # 计算每日新增病例的移动平均
        df['new_cases_ma'] = df['new_cases'].rolling(window=3).mean()
        
        # 计算累计康复率
        df['recovery_rate'] = df['recovered'].cumsum() / df['total_cases'] * 100
        
        # 计算活跃病例数
        df['active_cases'] = df['total_cases'] - df['recovered'].cumsum()
        
        print("趋势分析完成")
        return df
    
    def generate_statistics(self, df):
        print("生成统计数据...")
        
        stats = {
            '总确诊病例': df['total_cases'].max(),
            '平均每日新增': df['new_cases'].mean(),
            '最大单日新增': df['new_cases'].max(),
            '累计康复人数': df['recovered'].sum(),
            '平均康复率': df['recovery_rate'].mean(),
            '最高隔离人数': df['quarantined'].max()
        }
        
        for key, value in stats.items():
            print(f"{key}: {value}")
        
        return stats
    
    def save_analyzed_data(self, df, filename="analyzed_data.csv"):
        df.to_csv(filename, index=False)
        print(f"分析后的数据已保存到 {filename}")

if __name__ == "__main__":
    analyzer = DataAnalyzer()
    cleaned_df = analyzer.load_cleaned_data()
    analyzed_df = analyzer.analyze_trends(cleaned_df)
    analyzer.generate_statistics(analyzed_df)
    analyzer.save_analyzed_data(analyzed_df)