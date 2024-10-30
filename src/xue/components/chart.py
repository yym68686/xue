from ..core import Div, Script, Head, Style, Raw
import json

Head.add_default_children([
    Script(src="https://cdn.jsdelivr.net/npm/apexcharts", id="apexcharts-script"),
    Style("""
        .chart-container {
            border-radius: 0.5rem;
            padding: 1rem;
            min-height: 350px;
            border: 1px solid #e5e7eb;
            transition: background-color 0.2s ease;
        }

        .chart-tooltip {
            border-radius: 0.375rem;
            padding: 0.5rem;
            background: #ffffff;
            border: 1px solid #e5e7eb;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        @media (prefers-color-scheme: dark) {
            .chart-container {
                border-color: #374151;
            }

            .chart-tooltip {
                background: #1f2937;
                border-color: #374151;
                color: #e5e7eb;
            }

            .apexcharts-text {
                fill: #e5e7eb !important;
            }

            .apexcharts-legend-text {
                color: #e5e7eb !important;
            }

            .apexcharts-gridline {
                stroke: #374151 !important;
            }

            .apexcharts-xaxis-label,
            .apexcharts-yaxis-label {
                fill: #9ca3af !important;
            }

            .apexcharts-toolbar {
                filter: invert(1) hue-rotate(180deg);
            }
        }
    """, id="chart-style"),
])

def bar_chart(id, data, x_axis, series, config=None):
    default_config = {
        "stacked": False,
        "horizontal": False,
        "grid": True,
        "tooltip": True,
        "legend": True,
        "colors": ["#2563eb", "#60a5fa", "#93c5fd"],
    }

    if config:
        default_config.update(config)

    # 检查数据是否为空
    is_empty = len(data) == 0

    # 如果数据为空，创建一个空的数据集
    if is_empty:
        data = [{"empty": ""}]  # 创建一个空数据点
        categories = [""]
        # series_data = [{"name": s["name"], "data": [0]} for s in series]
        series_data = []
    else:
        # 处理正常数据
        categories = [item[x_axis] for item in data]
        series_data = []
        for s in series:
            series_data.append({
                "name": s["name"],
                "data": [item[s["data_key"]] for item in data]
            })

    # 创建 ApexCharts 配置
    chart_options = {
        "chart": {
            "type": "bar",
            "height": 350,
            "stacked": default_config["stacked"],
            "toolbar": {
                "show": True
            },
            "zoom": {
                "enabled": True
            },
            "foreColor": "#6b7280",
            "background": "transparent",
            "events": {
                "mounted": """function(chartContext, config) {
                    const chart = chartContext.el;
                    if (%s) {
                        const noDataEl = document.createElement('div');
                        noDataEl.style.position = 'absolute';
                        noDataEl.style.left = '50%%';
                        noDataEl.style.top = '50%%';
                        noDataEl.style.transform = 'translate(-50%%, -50%%)';
                        noDataEl.style.fontSize = '1rem';
                        noDataEl.style.color = '#6b7280';
                        noDataEl.textContent = '暂无数据';
                        chart.appendChild(noDataEl);
                    }
                }""" % str(is_empty).lower()
            }
        },
        "theme": {
            "mode": "light",
        },
        "plotOptions": {
            "bar": {
                "horizontal": default_config["horizontal"],
                "borderRadius": 4,
                "columnWidth": "70%",
                "dataLabels": {
                    "position": "top" if not default_config["horizontal"] else "center"
                },
            }
        },
        "colors": default_config["colors"],
        "xaxis": {
            "categories": categories,
            "labels": {
                "style": {
                    "cssClass": "text-sm"
                },
                "show": not is_empty  # 数据为空时隐藏标签
            },
            "axisBorder": {
                "show": not is_empty
            },
            "axisTicks": {
                "show": not is_empty
            }
        },
        "yaxis": {
            "labels": {
                "style": {
                    "cssClass": "text-sm"
                },
                "show": not is_empty  # 数据为空时隐藏标签
            },
            "min": 0  # 确保Y轴从0开始
        },
        "grid": {
            "show": default_config["grid"] and not is_empty,  # 数据为空时隐藏网格
            "borderColor": "#e5e7eb",
            "strokeDashArray": 4,
            "padding": {
                "top": 0,
                "right": 0,
                "bottom": 0,
                "left": 0
            }
        },
        "legend": {
            "show": default_config["legend"] and not is_empty,  # 数据为空时隐藏图例
            "position": "bottom",
            "markers": {
                "radius": 4
            },
            "fontFamily": "inherit"
        },
        "tooltip": {
            "enabled": default_config["tooltip"] and not is_empty,  # 数据为空时禁用工具提示
            "shared": True,
            "intersect": False,
            "custom": None
        },
        "series": series_data,
        "noData": {
            "text": "暂无数据",
            "align": "center",
            "verticalAlign": "middle",
            "style": {
                "fontSize": "1rem",
                "color": "#6b7280"
            }
        }
    }

    # 主题切换脚本保持不变
    theme_script = """
        function updateChartTheme(chart) {
            const isDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
            chart.updateOptions({
                chart: {
                    foreColor: isDark ? '#e5e7eb' : '#6b7280',
                },
                grid: {
                    borderColor: isDark ? '#4b5563' : '#e5e7eb',
                },
                theme: {
                    mode: isDark ? 'dark' : 'light',
                }
            });
        }
    """

    chart_options_json = json.dumps(chart_options).replace('"True"', 'true').replace('"False"', 'false')

    return Div(
        Script(f"""
            {theme_script}
            document.addEventListener('DOMContentLoaded', function() {{
                var options = {chart_options_json};
                options.tooltip.custom = function({{series, seriesIndex, dataPointIndex, w}}) {{
                    let value = series[seriesIndex][dataPointIndex];
                    let name = w.globals.seriesNames[seriesIndex];
                    return '<div class="chart-tooltip">' +
                        '<div class="font-medium">' + name + '</div>' +
                        '<div>' + value + '</div>' +
                        '</div>';
                }};
                var chart = new ApexCharts(document.getElementById('{id}'), options);
                chart.render();

                // 初始化主题
                updateChartTheme(chart);

                // 监听系统主题变化
                window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function() {{
                    updateChartTheme(chart);
                }});
            }});
        """),
        id=id,
        class_="chart-container"
    )