from pyecharts import options as opts
from pyecharts.charts import Page, Line, Bar, Map, Grid, Pie, Liquid, Tab
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
import pandas as pd
import os

class EpidemicDashboard:
    def __init__(self, excel_file):
        """初始化数据"""
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

    def create_base_opts(self):
        """创建基础配置项"""
        return opts.InitOpts(
            theme=ThemeType.MACARONS,
            width="1000px",
            height="600px",
            animation_opts=opts.AnimationOpts(animation=True)
        )

    def create_dashboard(self):
        """创建整体大屏"""
        try:
            print("开始创建大屏...")
            
            # 创建页面
            page = Page(layout=Page.SimplePageLayout)
            
            # 使用页面配置
            page.page_title = "香港疫情数据大屏"
            
            # 使用自定义布局模板
            page_template = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{{ page.page_title }}</title>
                {{ page.css }}
                {{ page.js_dependencies }}
                <style>
                    .main-header {
                        text-align: center;
                        padding: 40px 20px;
                        background: linear-gradient(135deg, #1a365d 0%, #2c5282 100%);
                        margin-bottom: 40px;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    }
                    .main-title {
                        font-size: 48px;
                        font-weight: bold;
                        color: #ffffff;
                        margin: 0;
                        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
                    }
                    .main-subtitle {
                        font-size: 24px;
                        color: #e2e8f0;
                        margin-top: 15px;
                    }
                    .chart-container {
                        padding: 40px;
                        margin: 0 auto;
                        max-width: 1600px;
                    }
                    .chart-grid {
                        display: grid;
                        gap: 40px;
                        grid-template-columns: repeat(2, 1fr);
                        grid-template-rows: auto;
                    }
                    .chart-item {
                        background: #fff;
                        padding: 30px;
                        border-radius: 12px;
                        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
                        min-height: 500px;
                    }
                    .chart-item.full-width {
                        grid-column: 1 / -1;
                        height: 600px;
                    }
                    body {
                        margin: 0;
                        padding: 0;
                        background: #f8fafc;
                        font-family: "Microsoft YaHei", Arial, sans-serif;
                    }
                    @media (max-width: 1200px) {
                        .chart-grid {
                            grid-template-columns: 1fr;
                        }
                        .chart-item {
                            min-height: 400px;
                        }
                        .chart-item.full-width {
                            height: 500px;
                        }
                        .main-title {
                            font-size: 36px;
                        }
                        .main-subtitle {
                            font-size: 20px;
                        }
                    }
                </style>
            </head>
            <body>
                <div class="main-header">
                    <h1 class="main-title">香港疫情数据可视化大屏</h1>
                    <div class="main-subtitle">实时疫情数据分析与监控</div>
                </div>
                <div class="chart-container">
                    <div class="chart-grid">
                        <div class="chart-item full-width">{{ chart0 }}</div>
                        <div class="chart-item">{{ chart1 }}</div>
                        <div class="chart-item">{{ chart2 }}</div>
                        <div class="chart-item">{{ chart3 }}</div>
                        <div class="chart-item">{{ chart4 }}</div>
                    </div>
                </div>
                {{ page.js_code }}
            </body>
            </html>
            """
            
            # 创建各个图表并调整大小
            overview = self.create_overview_cards()
            trend = self.create_trend_line()
            map_chart = self.create_district_map()
            growth = self.create_growth_rate_bar()
            pie = self.create_district_pie()
            
            # 添加图表到页面
            page.add(overview)
            page.add(trend)
            page.add(map_chart)
            page.add(growth)
            page.add(pie)
            
            print("开始渲染页面...")
            # 保存为HTML文件
            page.render(
                path="香港疫情数据大屏.html",
                template_content=page_template
            )
            print("页面渲染完成！")
            
        except Exception as e:
            print(f"创建大屏时发生错误: {str(e)}")
            import traceback
            print(traceback.format_exc())

    def create_trend_line(self):
        """创建趋势折线图"""
        line = (
            Line(init_opts=self.create_base_opts())
            .add_xaxis(self.daily_stats['报告日期'].dt.strftime('%Y-%m-%d').tolist())
            .add_yaxis(
                "每日新增确诊", 
                self.daily_stats['新增确诊'].tolist(),
                is_smooth=True,
                linestyle_opts=opts.LineStyleOpts(width=2)
            )
            .add_yaxis(
                "累计确诊", 
                self.daily_stats['累计确诊'].tolist(),
                is_smooth=True,
                linestyle_opts=opts.LineStyleOpts(width=2)
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="确诊病例趋势",
                    pos_left="center"
                ),
                xaxis_opts=opts.AxisOpts(
                    type_="category",
                    boundary_gap=False,
                    axislabel_opts=opts.LabelOpts(rotate=45, interval=5)
                ),
                yaxis_opts=opts.AxisOpts(
                    type_="value",
                    axislabel_opts=opts.LabelOpts(formatter="{value}")
                ),
                datazoom_opts=[
                    opts.DataZoomOpts(range_start=80, range_end=100),
                    opts.DataZoomOpts(type_="inside")
                ],
                tooltip_opts=opts.TooltipOpts(trigger="axis"),
                legend_opts=opts.LegendOpts(pos_top="5%")
            )
        )
        return line

    def create_district_map(self):
        """创建地区分布地图"""
        district_data = [
            [district, confirmed] 
            for district, confirmed 
            in zip(self.latest_data['地区名称'], self.latest_data['现存确诊'])
        ]
        
        map_chart = (
            Map(init_opts=self.create_base_opts())
            .add(
                "现存确诊", 
                district_data, 
                "香港",
                is_map_symbol_show=True,
                layout_center=["50%", "50%"],
                layout_size="95%"
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="香港各区现存确诊分布",
                    pos_left="center"
                ),
                visualmap_opts=opts.VisualMapOpts(
                    min_=0,
                    max_=self.latest_data['现存确诊'].max(),
                    is_piecewise=True,
                    pos_left="10%",
                    pieces=[
                        {"min": 1000, "label": "≥1000例"},
                        {"min": 500, "max": 999, "label": "500-999例"},
                        {"min": 100, "max": 499, "label": "100-499例"},
                        {"min": 10, "max": 99, "label": "10-99例"},
                        {"min": 0, "max": 9, "label": "0-9例"}
                    ]
                )
            )
        )
        return map_chart
    
    def create_growth_rate_bar(self):
        """创建增长率柱状图"""
        bar = (
            Bar(init_opts=self.create_base_opts())
            .add_xaxis(self.daily_stats['报告日期'].dt.strftime('%Y-%m-%d').tolist())
            .add_yaxis(
                "增长率(%)", 
                self.daily_stats['增长率'].round(2).tolist(),
                label_opts=opts.LabelOpts(is_show=False),
                itemstyle_opts=opts.ItemStyleOpts(
                    color=JsCode(
                        """function(params) {
                            return params.value >= 0 ? '#c23531' : '#2f4554';
                        }"""
                    )
                )
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="确诊病例增长率",
                    pos_left="center"
                ),
                xaxis_opts=opts.AxisOpts(
                    type_="category",
                    axislabel_opts=opts.LabelOpts(rotate=45, interval=5)
                ),
                yaxis_opts=opts.AxisOpts(
                    type_="value",
                    axislabel_opts=opts.LabelOpts(formatter="{value}%")
                ),
                datazoom_opts=[
                    opts.DataZoomOpts(range_start=80, range_end=100),
                    opts.DataZoomOpts(type_="inside")
                ]
            )
        )
        return bar
    
    def create_district_pie(self):
        """创建地区分布饼图"""
        # 按现存确诊数排序，取top 10
        top_districts = self.latest_data.nlargest(10, '现存确诊')
        
        pie = (
            Pie(init_opts=self.create_base_opts())
            .add(
                "地区分布",
                [list(z) for z in zip(
                    top_districts['地区名称'], 
                    top_districts['现存确诊']
                )],
                radius=["40%", "70%"],
                center=["50%", "60%"],
                rosetype="radius"
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="各区确诊占比 (Top 10)",
                    pos_left="center"
                ),
                legend_opts=opts.LegendOpts(
                    orient="horizontal",
                    pos_top="5%",
                    pos_left="center",
                    type_="scroll"
                )
            )
            .set_series_opts(
                label_opts=opts.LabelOpts(
                    position="outside",
                    formatter="{b}: {c}例\n({d}%)"
                )
            )
        )
        return pie
    
    def create_overview_cards(self):
        """创建总览数据卡片"""
        latest = self.daily_stats.iloc[-1]
        total_confirmed = latest['累计确诊']
        current_confirmed = latest['现存确诊']
        
        # 使用Liquid图表展示现存确诊率
        liquid = (
            Liquid(init_opts=self.create_base_opts())
            .add(
                "现存确诊率",
                [round(current_confirmed/total_confirmed, 4)],
                label_opts=opts.LabelOpts(
                    font_size=30,
                    formatter=JsCode(
                        "function(param){return param.value * 100 + '%';}"
                    ),
                    position="inside"
                ),
                is_outline_show=False
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="现存确诊率",
                    subtitle=f"现存确诊: {current_confirmed}\n累计确诊: {total_confirmed}",
                    pos_left="center"
                )
            )
        )
        return liquid

if __name__ == "__main__":
    import sys
    print(f"Python version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")
    
    try:
        print("开始创建疫情数据大屏...")
        # 创建仪表盘实例
        dashboard = EpidemicDashboard('香港各区疫情数据_20250322.xlsx')
        print("成功读取数据文件")
        
        # 生成大屏
        dashboard.create_dashboard()
        print("数据大屏已生成，请打开 香港疫情数据大屏.html 查看结果！")
    except Exception as e:
        print(f"发生错误: {str(e)}")
        import traceback
        print(traceback.format_exc()) 