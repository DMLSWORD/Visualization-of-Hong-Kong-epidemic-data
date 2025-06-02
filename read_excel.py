import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.dates as mdates
from datetime import datetime

# 设置中文字体
try:
    # 尝试使用微软雅黑字体
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
except:
    # 如果没有微软雅黑，尝试使用系统默认字体
    print("警告：未找到微软雅黑字体，将尝试使用系统默认字体")
    plt.rcParams['font.sans-serif'] = ['SimSun']
finally:
    plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

# 读取Excel文件
# 注意：设置 encoding='utf-8' 以正确处理中文
df = pd.read_excel('香港各区疫情数据_20250322.xlsx')

# 显示前20行数据
print("\n=== 显示前20行数据 ===")
print(df.head(20))

# 显示数据基本信息
print("\n=== 数据基本信息 ===")
print(df.info())

# 计算确诊病例统计数据
print("\n=== 确诊病例统计数据 ===")

# 按日期分组计算每日数据
daily_stats = df.groupby('报告日期').agg({
    '新增确诊': 'sum',    # 每日新增确诊总数
    '累计确诊': 'max',    # 每日累计确诊数（取最大值，因为是累计数）
    '现存确诊': 'sum'     # 每日现存确诊总数
}).reset_index()

# 将报告日期转换为datetime类型
daily_stats['报告日期'] = pd.to_datetime(daily_stats['报告日期'])

# 创建图形和子图
plt.figure(figsize=(15, 10))

# 绘制三条折线
plt.plot(daily_stats['报告日期'], daily_stats['新增确诊'], label='每日新增确诊', marker='o', markersize=2)
plt.plot(daily_stats['报告日期'], daily_stats['累计确诊'], label='累计确诊', marker='s', markersize=2)
plt.plot(daily_stats['报告日期'], daily_stats['现存确诊'], label='现存确诊', marker='^', markersize=2)

# 设置图表标题和标签
plt.title('香港疫情数据统计', fontsize=16)
plt.xlabel('报告日期', fontsize=12)
plt.ylabel('确诊人数', fontsize=12)

# 设置x轴日期格式
ax = plt.gca()
# 设置主刻度为每15天
ax.xaxis.set_major_locator(mdates.DayLocator(interval=15))
# 设置日期格式
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# 设置图例
plt.legend(fontsize=10)

# 旋转x轴日期标签，避免重叠
plt.xticks(rotation=45)

# 添加网格线
plt.grid(True, linestyle='--', alpha=0.7)

# 自动调整布局，确保日期标签完整显示
plt.tight_layout()

# 保存图表
plt.savefig('香港疫情数据统计.png', dpi=300, bbox_inches='tight')

# 显示统计数据
print("\n每日确诊数据统计（最近10天）：")
print(daily_stats.tail(10))

# 计算总体统计数据
print("\n总体统计数据：")
print(f"最新累计确诊总数：{daily_stats['累计确诊'].max():,} 例")
print(f"最新现存确诊总数：{daily_stats['现存确诊'].iloc[-1]:,} 例")
print(f"单日新增确诊最高：{daily_stats['新增确诊'].max():,} 例")
print(f"平均每日新增确诊：{daily_stats['新增确诊'].mean():.2f} 例") 