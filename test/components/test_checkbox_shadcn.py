from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from xue import HTML, Head, Body, Div, xue_initialize
from xue.components import checkbox

xue_initialize(tailwind=True)
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    result = HTML(
        Head(
            title="Checkbox Example"
        ),
        Body(
            Div(
                checkbox.checkbox("terms", "Accept terms and conditions"),
                checkbox.checkbox("newsletter", "Subscribe to newsletter", checked=True),
                checkbox.checkbox("disabled", "Disabled option", disabled=True),
                class_="container mx-auto p-4 space-y-4"
            )
        )
    ).render()
    print(result)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)