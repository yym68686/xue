from ..core import Div, Style, Script, Head, Raw

Head.add_default_children([
    Style("""
        .chart-container {
            position: relative;
            padding: 3rem 2rem 3rem 4rem;
            background: white;
            border-radius: 0.5rem;
            border: 1px solid #e5e7eb;
            margin-top: 1rem;
        }

        .chart-grid {
            position: absolute;
            width: calc(100% - 6rem);
            height: calc(100% - 6rem);
            right: 2rem;
            top: 3rem;
            border-left: 1px solid #e5e7eb;
            border-bottom: 1px solid #e5e7eb;
            pointer-events: none;
        }

        .chart-grid-line {
            position: absolute;
            width: 100%;
            border-top: 1px dashed #e5e7eb;
        }

        .chart-bars {
            position: relative;
            height: 100%;
            display: flex;
            align-items: flex-end;
        }

        .bar-group {
            position: relative;
            flex: 1;
            height: 100%;
            padding: 0 0.5rem;
        }

        .bar {
            position: absolute;
            width: 40%;
            transition: all 0.2s;
            border-radius: 0.25rem 0.25rem 0 0;
        }

        .bar:nth-child(2) {
            right: 0;
            left: auto;
        }

        .bar:hover {
            opacity: 0.8;
            cursor: pointer;
        }

        .x-axis {
            position: absolute;
            bottom: 1rem;
            left: 4rem;
            right: 2rem;
            display: flex;
            justify-content: space-between;
        }

        .x-axis-label {
            flex: 1;
            text-align: center;
            font-size: 0.875rem;
            color: #6b7280;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            padding: 0 0.5rem;
        }

        .y-axis {
            position: absolute;
            left: 0;
            top: 3rem;
            bottom: 3rem;
            width: 4rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .y-axis-label {
            transform: translateY(50%);
            padding-right: 1rem;
            text-align: right;
            font-size: 0.875rem;
            color: #6b7280;
            white-space: nowrap;
        }

        .chart-tooltip {
            position: fixed;
            background: #1f2937;
            color: white;
            padding: 0.5rem 0.75rem;
            border-radius: 0.375rem;
            font-size: 0.875rem;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.2s;
            z-index: 50;
            white-space: nowrap;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }

        .chart-legend {
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
            justify-content: center;
            flex-wrap: wrap;
        }

        .legend-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.875rem;
            color: #6b7280;
        }

        .legend-color {
            width: 0.75rem;
            height: 0.75rem;
            border-radius: 0.25rem;
            flex-shrink: 0;
        }

        @media (prefers-color-scheme: dark) {
            .chart-container {
                background: #1f2937;
                border-color: #374151;
            }

            .chart-grid,
            .chart-grid-line {
                border-color: #374151;
            }

            .x-axis-label,
            .y-axis-label,
            .legend-item {
                color: #9ca3af;
            }

            .chart-tooltip {
                background: #374151;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -1px rgba(0, 0, 0, 0.1);
            }
        }
    """),
    Script("""
        function showTooltip(event, values) {
            const tooltip = document.getElementById('chart-tooltip');
            if (!tooltip) return;

            const tooltipContent = Object.entries(values)
                .filter(([key]) => key !== 'label')
                .map(([key, value]) => `${key}: ${value}`)
                .join('<br>');

            tooltip.innerHTML = tooltipContent;
            tooltip.style.opacity = '1';

            const tooltipRect = tooltip.getBoundingClientRect();
            let left = event.clientX + 10;
            let top = event.clientY - tooltipRect.height - 10;

            if (left + tooltipRect.width > window.innerWidth) {
                left = window.innerWidth - tooltipRect.width - 10;
            }

            if (top < 0) {
                top = event.clientY + 10;
            }

            tooltip.style.left = left + 'px';
            tooltip.style.top = top + 'px';

            event.target.style.opacity = '0.8';
        }

        function hideTooltip(event) {
            const tooltip = document.getElementById('chart-tooltip');
            if (tooltip) {
                tooltip.style.opacity = '0';
            }
            event.target.style.opacity = '1';
        }
    """)
])

def chart(data, config, stacked=False, height="400px", show_grid=True):
    # 计算最大值
    max_value = 0
    if stacked:
        for item in data:
            total = sum(item[k] for k in config.keys() if k in item)
            max_value = max(max_value, total)
    else:
        for item in data:
            max_value = max(max_value, max(item[k] for k in config.keys() if k in item))

    # 确保最大值不为0，并调整为适当的刻度范围
    if max_value == 0:
        max_value = 100
    else:
        # 将最大值向上取整到最接近的10的倍数
        max_value = ((max_value + 9) // 10) * 10 + 10  # 加10给顶部留些空间

    # 生成5个均匀分布的刻度点（包括0和最大值）
    step = max_value / 4
    y_ticks = [int(i * step) for i in range(5)][::-1]

    # 生成网格线 - 确保从底部开始，每个网格线对应一个刻度值
    grid_lines = []
    if show_grid:
        for i in range(4):  # 不包括最底部的线，因为已经有边框了
            grid_lines.append(
                Div(
                    class_="chart-grid-line",
                    style=f"bottom: {(i + 1) * 25}%"
                )
            )

    def generate_bars(item):
        bars = []
        cumulative_height = 0

        for i, (key, cfg) in enumerate(config.items()):
            if key in item:
                value = item[key]
                # 计算高度百分比时使用 max_value
                height_percent = (value / max_value * 100)

                if stacked:
                    bars.append(
                        Div(
                            class_="bar",
                            style=f"""
                                height: {height_percent}%;
                                background-color: {cfg['color']};
                                bottom: {cumulative_height}%;
                                right: 0;
                                left: 30%;
                            """,
                            onmouseover=f"showTooltip(event, {item})",
                            onmouseout="hideTooltip(event)"
                        )
                    )
                    cumulative_height += height_percent
                else:
                    bars.append(
                        Div(
                            class_="bar",
                            style=f"""
                                height: {height_percent}%;
                                background-color: {cfg['color']};
                                bottom: 0;
                                left: {9 if i == 0 else 51}%;
                            """,
                            onmouseover=f"showTooltip(event, {item})",
                            onmouseout="hideTooltip(event)"
                        )
                    )
        return bars

    # 生成图例
    legend_items = [
        Div(
            Div(class_="legend-color", style=f"background-color: {cfg['color']}"),
            cfg['label'],
            class_="legend-item"
        )
        for key, cfg in config.items()
    ]

    return Div(
        # 图表容器
        Div(
            # 网格
            Div(*grid_lines, class_="chart-grid") if show_grid else None,

            # Y轴
            Div(
                *[Div(str(tick), class_="y-axis-label") for tick in y_ticks],
                class_="y-axis"
            ),

            # 柱状图
            Div(
                *[Div(*generate_bars(item), class_="bar-group") for item in data],
                class_="chart-bars"
            ),

            # X轴
            Div(
                *[Div(item.get('label', ''), class_="x-axis-label") for item in data],
                class_="x-axis"
            ),

            class_="chart-container",
            style=f"height: {height};"
        ),

        # 图例
        Div(*legend_items, class_="chart-legend"),

        # 工具提示
        Div(id="chart-tooltip", class_="chart-tooltip"),

        class_="w-full"
    )