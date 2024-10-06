from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from xue import HTML, Head, Body, Div, xue_initialize
from xue.components import input

xue_initialize(tailwind=True)
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    result = HTML(
        Head(),
        Body(
            Div(
                input.input(type="email", placeholder="Email", id="email-input"),
                input.input(type="password", placeholder="Password", id="password-input", class_="mt-4"),
                input.input(type="text", placeholder="Disabled input", id="disabled-input", class_="mt-4", disabled=True),
                class_="container mx-auto p-4 max-w-sm"
            )
        )
    ).render()
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)