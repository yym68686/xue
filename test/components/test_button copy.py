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
                dropdown.render("Open Dropdown", ["Option 1", "Option 2", "Option 3"]),
                class_="container mx-auto p-4"
            )
        )
    ).render()
    print(result)
    return result

@app.get("/button-clicked")
async def button_clicked():
    return "Button was clicked!"

@app.get("/dropdown-content")
async def get_dropdown_content():
    items = ["Option 1", "Option 2", "Option 3"]
    result = dropdown.dropdown_content(items).render()
    print("result", result)
    return result

@app.get("/dropdown-content/{id}")
async def get_dropdown_content(id: str):
    items = ["Profile", "Settings", "Sign out"]
    content = Div(
        dropdown.dropdown_content(items),
        Script(f"""
            const content = document.getElementById('{id}-content');
            content.classList.toggle('hidden');
        """, hx_swap_oob=True, hx_target=f"#{id}-content")
    ).render()

    return HTMLResponse(content)

def dropdown_example():
    result = HTML(
        Head(),
        Body(
            Div(
                H2("Dropdown Example"),
                dropdown.dropdown("Options", ["Option 1", "Option 2", "Option 3"], "example-dropdown"),
                class_="p-4"
            )
        )
    ).render()
    print(result)
    return result

@app.get("/examples/dropdown")
async def dropdown_example_page():
    return HTMLResponse(dropdown_example())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "__main__:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )