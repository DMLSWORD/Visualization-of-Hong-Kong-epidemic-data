import pandas as pd
import json
import numpy as np

class EpidemicDataProcessor:
    def __init__(self, excel_file):
        """初始化数据处理器"""
        print("开始读取数据文件...")
        self.df = pd.read_excel(excel_file)
        self.df['报告日期'] = pd.to_datetime(self.df['报告日期'])
        self.process_data()
        print("数据处理完成")
        
    def process_data(self):
        """处理数据，计算统计值"""
        # 按日期统计全港数据
        self.daily_stats = self.df.groupby('报告日期').agg({
            '新增确诊': 'sum',
            '累计确诊': 'max',
            '现存确诊': 'sum',
            '新增康复': 'sum',
            '累计康复': 'max',
            '新增死亡': 'sum',
            '累计死亡': 'max'
        }).reset_index()
        
        # 计算增长率
        self.daily_stats['增长率'] = self.daily_stats['新增确诊'].pct_change() * 100
        
        # 获取最新数据
        self.latest_data = self.df[self.df['报告日期'] == self.df['报告日期'].max()]

    def get_overview_data(self):
        """获取总览数据，现存确诊率保留两位小数"""
        latest = self.daily_stats.iloc[-1]
        current_rate = float(latest['现存确诊'] / latest['累计确诊']) if latest['累计确诊'] else 0
        return {
            'total_confirmed': int(latest['累计确诊']),
            'current_confirmed': int(latest['现存确诊']),
            'total_recovered': int(latest['累计康复']),
            'total_death': int(latest['累计死亡']),
            'current_rate': round(current_rate, 4)
        }

    def get_trend_data(self):
        """获取趋势数据"""
        return {
            'dates': self.daily_stats['报告日期'].dt.strftime('%Y-%m-%d').tolist(),
            'new_cases': self.daily_stats['新增确诊'].tolist(),
            'total_cases': self.daily_stats['累计确诊'].tolist()
        }

    def get_district_map_data(self):
        """获取地区分布数据"""
        district_data = [
            {'name': district, 'value': int(confirmed)}
            for district, confirmed 
            in zip(self.latest_data['地区名称'], self.latest_data['现存确诊'])
        ]
        return {'data': district_data}

    def get_growth_rate_data(self):
        """获取增长率数据，NaN替换为0"""
        growth_rates = self.daily_stats['增长率'].replace({np.nan: 0}).round(2).tolist()
        return {
            'dates': self.daily_stats['报告日期'].dt.strftime('%Y-%m-%d').tolist(),
            'growth_rates': growth_rates
        }

    def get_district_proportion_data(self):
        """获取地区占比数据"""
        top_districts = self.latest_data.nlargest(10, '现存确诊')
        return {
            'districts': top_districts['地区名称'].tolist(),
            'values': top_districts['现存确诊'].tolist()
        } 