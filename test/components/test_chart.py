from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from xue import HTML, Head, Body, Div, xue_initialize
from xue.components import chart

app = FastAPI()
xue_initialize(tailwind=True)

@app.get("/", response_class=HTMLResponse)
async def root():
    # 示例数据
    data = [
        {"label": "Jan", "desktop": 186, "mobile": 80},
        {"label": "Feb", "desktop": 305, "mobile": 200},
        {"label": "Mar", "desktop": 237, "mobile": 120},
        {"label": "Apr", "desktop": 73, "mobile": 190},
        {"label": "May", "desktop": 209, "mobile": 130},
        {"label": "Jun", "desktop": 214, "mobile": 140},
    ]

    # 配置
    config = {
        "desktop": {
            "label": "Desktop",
            "color": "#2563eb"
        },
        "mobile": {
            "label": "Mobile",
            "color": "#60a5fa"
        }
    }

    result = HTML(
        Head(title="Chart Example"),
        Body(
            Div(
                # 普通柱状图
                Div(
                    "Side by Side Bars",
                    chart.chart(data, config, stacked=False),
                    class_="mb-8"
                ),

                # 堆叠柱状图
                Div(
                    "Stacked Bars",
                    chart.chart(data, config, stacked=True),
                    class_="mb-8"
                ),

                class_="container mx-auto p-4"
            )
        )
    ).render()
    print(result)

    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)