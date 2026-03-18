from crawler import CampusEpidemicCrawler
from data_cleaner import DataCleaner
from data_analyzer import DataAnalyzer
from visualizer import DataVisualizer

def main():
    print("=== 校园疫情数据分析系统 ===")
    
    # 1. 数据爬取
    crawler = CampusEpidemicCrawler()
    raw_data = crawler.crawl_data()
    crawler.save_raw_data(raw_data)
    
    # 2. 数据清洗
    cleaner = DataCleaner()
    cleaned_data = cleaner.clean_data(raw_data)
    cleaner.save_cleaned_data(cleaned_data)
    
    # 3. 数据分析
    analyzer = DataAnalyzer()
    analyzed_data = analyzer.analyze_trends(cleaned_data)
    analyzer.generate_statistics(analyzed_data)
    analyzer.save_analyzed_data(analyzed_data)
    
    # 4. 数据可视化
    visualizer = DataVisualizer()
    visualizer.plot_trends(analyzed_data)
    visualizer.plot_pie_chart(analyzed_data)
    visualizer.plot_correlation_heatmap(analyzed_data)
    
    print("\n=== 数据分析完成 ===")
    print("生成的文件:")
    print("- raw_data.csv: 原始爬取数据")
    print("- cleaned_data.csv: 清洗后的数据")
    print("- analyzed_data.csv: 分析后的数据")
    print("- trend_plots.png: 趋势图表")
    print("- pie_chart.png: 病例分布饼图")
    print("- correlation_heatmap.png: 数据相关性热力图")

if __name__ == "__main__":
    main()