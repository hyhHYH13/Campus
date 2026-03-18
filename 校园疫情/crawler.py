import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

class CampusEpidemicCrawler:
    def __init__(self):
        self.base_url = "https://example.com/campus-epidemic"
    
    def crawl_data(self):
        print("开始爬取校园疫情数据...")
        time.sleep(2)  # 模拟网络请求延迟
        
        # 模拟数据
        data = {
            'date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'],
            'total_cases': [120, 135, 142, 150, 158],
            'new_cases': [15, 15, 7, 8, 8],
            'recovered': [5, 8, 12, 15, 18],
            'quarantined': [80, 85, 90, 95, 100]
        }
        
        df = pd.DataFrame(data)
        print("数据爬取完成")
        return df
    
    def save_raw_data(self, df, filename="raw_data.csv"):
        df.to_csv(filename, index=False)
        print(f"原始数据已保存到 {filename}")

if __name__ == "__main__":
    crawler = CampusEpidemicCrawler()
    data = crawler.crawl_data()
    crawler.save_raw_data(data)