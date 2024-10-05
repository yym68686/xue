from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from xue import HTML, Head, Body, Div, Script, xue_initialize
from xue.components import dropdown

xue_initialize(tailwind=True)
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    result = HTML(
        Head(),
        Body(
            Div(
                dropdown.dropdown("Menu 1", "dropdown1"),
                dropdown.dropdown("Menu 2", "dropdown2"),
                class_="container mx-auto p-4 space-x-4"
            )
        )
    ).render()
    # print(result)
    return result

@app.get("/dropdown/{dropdown_id}", response_class=HTMLResponse)
async def get_dropdown_content(dropdown_id: str):
    items = {
        "dropdown1": ["Option 1", "Option 2", "Option 3"],
        "dropdown2": ["Item A", "Item B", "Item C"]
    }
    result = dropdown.dropdown_content(items[dropdown_id], dropdown_id, visible=True).render()
    # print("result", result)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)