from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from xue import HTML, Head, Body, Div, xue_initialize
from xue.components.chart import bar_chart

app = FastAPI()
xue_initialize(tailwind=True)

@app.get("/", response_class=HTMLResponse)
async def root():
    # 示例数据
    chart_data = [
        {"month": "Jan", "desktop": 186, "mobile": 80},
        {"month": "Feb", "desktop": 305, "mobile": 200},
        {"month": "Mar", "desktop": 237, "mobile": 120},
        {"month": "Apr", "desktop": 73, "mobile": 190},
        {"month": "May", "desktop": 209, "mobile": 130},
        {"month": "Jun", "desktop": 214, "mobile": 140}
    ]
    chart_data = []

    # 定义系列
    series = [
        {"name": "Desktop", "data_key": "desktop"},
        {"name": "Mobile", "data_key": "mobile"}
    ]
    # series = []

    chart_config = {
        "stacked": False,
        "horizontal": False,
        "colors": ["#2563eb", "#60a5fa"],
        "grid": True,  # 隐藏网格
        "legend": True,  # 显示图例
        "tooltip": True  # 启用工具提示
    }
    result = HTML(
        Head(title="Chart Examples"),
        Body(
            Div(
                # 基础柱状图
                Div(
                    bar_chart("basic-chart", chart_data, "month", series, chart_config),
                    class_="mb-8"
                ),
                # 堆叠柱状图
                Div(
                    bar_chart("stacked-chart", chart_data, "month", series,
                             {**chart_config, "stacked": True}),
                    class_="mb-8"
                ),
                # 水平柱状图
                Div(
                    bar_chart("horizontal-chart", chart_data, "month", series,
                             {**chart_config, "horizontal": True}),
                    class_="mb-8"
                ),
                class_="container mx-auto p-4 max-w-4xl"
            )
        )
    ).render()
    print(result)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)