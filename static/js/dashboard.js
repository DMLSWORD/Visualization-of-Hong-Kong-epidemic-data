// 初始化所有图表实例
const charts = {
    overview: echarts.init(document.getElementById('overviewChart')),
    trend: echarts.init(document.getElementById('trendChart')),
    map: echarts.init(document.getElementById('mapChart')),
    growth: echarts.init(document.getElementById('growthChart')),
    proportion: echarts.init(document.getElementById('proportionChart'))
};

// 加载所有数据
async function loadAllData() {
    try {
        await Promise.all([
            loadOverviewData(),
            loadTrendData(),
            loadDistrictMapData(),
            loadGrowthRateData(),
            loadDistrictProportionData()
        ]);
    } catch (error) {
        console.error('加载数据失败:', error);
    }
}

// 加载总览数据
async function loadOverviewData() {
    try {
        const response = await fetch('/api/overview');
        const data = await response.json();
        
        const option = {
            title: {
                text: '现存确诊率',
                subtext: `现存确诊: ${data.current_confirmed}\n累计确诊: ${data.total_confirmed}`,
                left: 'center'
            },
            series: [{
                type: 'liquidFill',
                data: [data.current_rate],
                label: {
                    formatter: (param) => (param.value * 100).toFixed(2) + '%'
                },
                outline: {
                    show: false
                }
            }],
            dataZoom: [
                { type: 'slider', start: 80, end: 100 },
                { type: 'inside' }
            ]
        };
        
        charts.overview.setOption(option);
    } catch (error) {
        console.error('加载总览数据失败:', error);
    }
}

// 加载趋势数据
async function loadTrendData() {
    try {
        const response = await fetch('/api/trend');
        const data = await response.json();
        
        const option = {
            title: {
                text: '确诊病例趋势',
                left: 'center'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['每日新增确诊', '累计确诊'],
                top: 30
            },
            xAxis: {
                type: 'category',
                data: data.dates,
                axisLabel: {
                    rotate: 45
                }
            },
            yAxis: {
                type: 'value'
            },
            series: [{
                name: '每日新增确诊',
                type: 'line',
                data: data.new_cases,
                smooth: true
            }, {
                name: '累计确诊',
                type: 'line',
                data: data.total_cases,
                smooth: true
            }],
            dataZoom: [
                { type: 'slider', start: 80, end: 100 },
                { type: 'inside' }
            ]
        };
        
        charts.trend.setOption(option);
    } catch (error) {
        console.error('加载趋势数据失败:', error);
    }
}

// 加载地区分布数据
async function loadDistrictMapData() {
    try {
        const response = await fetch('/api/district-map');
        const data = await response.json();
        // 需要将地区名称转换为经纬度坐标（示例数据，实际可根据需要补全）
        const geoCoordMap = {
            '中西区': [114.154374, 22.281981],
            '湾仔区': [114.18299, 22.276345],
            '东区': [114.225965, 22.279779],
            '南区': [114.160023, 22.245811],
            '油尖旺区': [114.173347, 22.311632],
            '深水埗区': [114.163349, 22.32921],
            '九龙城区': [114.188956, 22.312618],
            '黄大仙区': [114.203384, 22.336112],
            '观塘区': [114.221963, 22.320679],
            '荃湾区': [114.121234, 22.368458],
            '屯门区': [113.976308, 22.393896],
            '元朗区': [114.032528, 22.44113],
            '北区': [114.147404, 22.496143],
            '大埔区': [114.171713, 22.44573],
            '沙田区': [114.195365, 22.379531],
            '西贡区': [114.264813, 22.314203],
            '离岛区': [113.94612, 22.286407]
        };
        // 转换为 effectScatter 数据格式
        const scatterData = data.data.map(item => {
            const coord = geoCoordMap[item.name];
            return coord ? {
                name: item.name,
                value: coord.concat(item.value)
            } : null;
        }).filter(Boolean);
        const option = {
            title: {
                text: '香港各区现存确诊分布',
                left: 'center'
            },
            tooltip: {
                trigger: 'item',
                formatter: function(params) {
                    return params.name + ': ' + params.value[2] + '例';
                }
            },
            visualMap: {
                min: 0,
                max: Math.max(...data.data.map(item => item.value)),
                left: '10%',
                text: ['高', '低'],
                calculable: true,
                inRange: {
                    color: ['#4575b4', '#fee090', '#f46d43', '#d73027'] // 蓝-黄-橙-红
                }
            },
            geo: {
                map: '香港',
                roam: true,
                label: {
                    show: true
                },
                itemStyle: {
                    areaColor: '#e0f7fa',
                    borderColor: '#111'
                }
            },
            series: [{
                name: '现存确诊',
                type: 'effectScatter',
                coordinateSystem: 'geo',
                data: scatterData,
                symbolSize: function(val) {
                    return Math.max(10, val[2] / 100); // 根据确诊数调整点大小
                },
                showEffectOn: 'render',
                rippleEffect: {
                    brushType: 'stroke'
                },
                hoverAnimation: true,
                itemStyle: {
                    color: '#c23531',
                    shadowBlur: 10,
                    shadowColor: '#333'
                },
                zlevel: 1
            }]
        };
        charts.map.setOption(option);
    } catch (error) {
        console.error('加载地区分布数据失败:', error);
    }
}

// 加载增长率数据
async function loadGrowthRateData() {
    try {
        const response = await fetch('/api/growth-rate');
        const data = await response.json();
        
        const option = {
            title: {
                text: '确诊病例增长率',
                left: 'center'
            },
            tooltip: {
                trigger: 'axis'
            },
            xAxis: {
                type: 'category',
                data: data.dates,
                axisLabel: {
                    rotate: 45
                }
            },
            yAxis: {
                type: 'value',
                axisLabel: {
                    formatter: '{value}%'
                }
            },
            series: [{
                name: '增长率',
                type: 'bar',
                data: data.growth_rates,
                itemStyle: {
                    color: function(params) {
                        return params.value >= 0 ? '#c23531' : '#2f4554';
                    }
                }
            }],
            dataZoom: [
                { type: 'slider', start: 80, end: 100 },
                { type: 'inside' }
            ]
        };
        
        charts.growth.setOption(option);
    } catch (error) {
        console.error('加载增长率数据失败:', error);
    }
}

// 加载地区占比数据
async function loadDistrictProportionData() {
    try {
        const response = await fetch('/api/district-proportion');
        const data = await response.json();
        
        const option = {
            title: {
                text: '各区确诊占比 (Top 10)',
                left: 'center'
            },
            tooltip: {
                trigger: 'item',
                formatter: '{b}: {c}例 ({d}%)'
            },
            legend: {
                orient: 'horizontal',
                top: 30,
                data: data.districts
            },
            series: [{
                name: '地区分布',
                type: 'pie',
                radius: ['40%', '70%'],
                center: ['50%', '60%'],
                data: data.districts.map((district, index) => ({
                    name: district,
                    value: data.values[index]
                })),
                roseType: 'radius',
                label: {
                    formatter: '{b}: {c}例\n{d}%'
                }
            }],
            dataZoom: [
                { type: 'slider', start: 80, end: 100 },
                { type: 'inside' }
            ]
        };
        
        charts.proportion.setOption(option);
    } catch (error) {
        console.error('加载地区占比数据失败:', error);
    }
}

// 监听窗口大小变化，调整图表大小
window.addEventListener('resize', () => {
    Object.values(charts).forEach(chart => chart.resize());
});

// 页面加载完成后初始化所有图表
document.addEventListener('DOMContentLoaded', loadAllData); 