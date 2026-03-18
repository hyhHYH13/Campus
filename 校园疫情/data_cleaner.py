import pandas as pd

class DataCleaner:
    def __init__(self):
        pass
    
    def load_data(self, filename="raw_data.csv"):
        print(f"加载数据文件: {filename}")
        return pd.read_csv(filename)
    
    def clean_data(self, df):
        print("开始数据清洗...")
        
        # 转换日期格式
        df['date'] = pd.to_datetime(df['date'])
        
        # 检查并处理缺失值
        if df.isnull().values.any():
            print("发现缺失值，正在处理...")
            df = df.fillna(0)
        
        # 确保数值列类型正确
        numeric_columns = ['total_cases', 'new_cases', 'recovered', 'quarantined']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 去除异常值（如果有）
        for col in numeric_columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        
        print("数据清洗完成")
        return df
    
    def save_cleaned_data(self, df, filename="cleaned_data.csv"):
        df.to_csv(filename, index=False)
        print(f"清洗后的数据已保存到 {filename}")

if __name__ == "__main__":
    cleaner = DataCleaner()
    raw_df = cleaner.load_data()
    cleaned_df = cleaner.clean_data(raw_df)
    cleaner.save_cleaned_data(cleaned_df)