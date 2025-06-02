from flask import Flask, render_template, jsonify
from data_processor import EpidemicDataProcessor
import os
import numpy as np

app = Flask(__name__)

# 初始化数据处理器
data_processor = EpidemicDataProcessor('香港各区疫情数据_20250322.xlsx')

@app.route('/')
def index():
    """渲染主页"""
    return render_template('index.html')

@app.route('/api/overview')
def get_overview_data():
    """获取总览数据"""
    return jsonify(data_processor.get_overview_data())

@app.route('/api/trend')
def get_trend_data():
    """获取趋势数据"""
    return jsonify(data_processor.get_trend_data())

@app.route('/api/district-map')
def get_district_map_data():
    """获取地区分布数据"""
    return jsonify(data_processor.get_district_map_data())

@app.route('/api/growth-rate')
def get_growth_rate_data():
    """获取增长率数据"""
    growth_rates = data_processor.get_growth_rate_data()['growth_rates']
    return jsonify({
        'dates': data_processor.get_growth_rate_data()['dates'],
        'growth_rates': growth_rates
    })

@app.route('/api/district-proportion')
def get_district_proportion_data():
    """获取地区占比数据"""
    return jsonify(data_processor.get_district_proportion_data())

if __name__ == '__main__':
    app.run(debug=True, port=5000) 