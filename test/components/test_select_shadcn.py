from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from xue import HTML, Head, Body, Div, xue_initialize
from xue.components import select

xue_initialize(tailwind=True)
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    result = HTML(
        Head(),
        Body(
            Div(
                select.select("Select a fruit", [], "fruit-select"),
                class_="container mx-auto p-4"
            )
        )
    ).render()
    
    return result

@app.get("/select/{select_id}", response_class=HTMLResponse)
async def get_select_content(select_id: str):
    options = [
        {"value": "apple", "label": "Apple"},
        {"value": "banana", "label": "Banana"},
        {"value": "blueberry", "label": "Blueberry"},
        {"value": "grapes", "label": "Grapes"},
        {"value": "pineapple", "label": "Pineapple"},
    ]
    result = select.select_content(select_id, options, "Fruits").render()
    return result

@app.post("/select/{select_id}/{value}", response_class=HTMLResponse)
async def update_select(select_id: str, value: str):
    options = {
        "apple": "Apple",
        "banana": "Banana",
        "blueberry": "Blueberry",
        "grapes": "Grapes",
        "pineapple": "Pineapple",
    }
    label = options.get(value, "Select a fruit")
    result = select.select(label, [], select_id).render()
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)