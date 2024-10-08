from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from xue import HTML, Head, Body, Div, xue_initialize
from xue.components import resizable

xue_initialize(tailwind=True)
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    result = HTML(
        Head(
            title="Resizable Layout Example"
        ),
        Body(
            resizable.resizable_layout(
                Div("Header Content", class_="text-2xl font-bold"),
                Div("Content Area", class_="text-xl"),
                resizable=False  # 设置为 False 将禁用调整大小功能
            )
        )
    ).render()
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)