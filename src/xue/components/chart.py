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

    # 处理数据格式
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
            "foreColor": "#6b7280",  # 默认文字颜色
            "background": "transparent",
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
                }
            },
            "axisBorder": {
                "show": False
            },
            "axisTicks": {
                "show": False
            }
        },
        "yaxis": {
            "labels": {
                "style": {
                    "cssClass": "text-sm"
                }
            }
        },
        "grid": {
            "show": default_config["grid"],
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
            "show": default_config["legend"],
            "position": "bottom",
            "markers": {
                "radius": 4
            },
            "fontFamily": "inherit"
        },
        "tooltip": {
            "enabled": default_config["tooltip"],
            "shared": True,
            "intersect": False,
            "custom": None
        },
        "series": series_data
    }

    # 添加深色模式检测和主题切换的JavaScript代码
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