from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from xue import HTML, Head, Body, Div, H2, Script, xue_initialize
from xue.components import button, dropdown

xue_initialize(tailwind=True)
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    result = HTML(
        Head(),
        Body(
            Div(
                button.render("Click me", hx_get="/button-clicked", hx_target="#button-result"),
                Div(id="button-result"),
            )
        )
    ).render()
    print(result)
    return result

@app.get("/button-clicked")
async def button_clicked():
    return "Button was clicked!"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "__main__:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )