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
                dropdown.dropdown_menu("Open"),
                class_="container mx-auto p-4"
            )
        )
    ).render()
    print(result)
    return result

@app.get("/dropdown-menu/{menu_id}", response_class=HTMLResponse)
async def get_dropdown_menu_content(menu_id: str):
    items = [
        {"icon": "👤", "label": "Profile", "shortcut": "⇧⌘P"},
        {"icon": "💳", "label": "Billing", "shortcut": "⌘B"},
        {"icon": "⚙️", "label": "Settings", "shortcut": "⌘S"},
        {"icon": "⌨️", "label": "Keyboard shortcuts", "shortcut": "⌘K"},
        "separator",
        {"icon": "👥", "label": "Team"},
        {"icon": "➕", "label": "New Team", "shortcut": "⌘+T"},
        "separator",
        {"icon": "🐙", "label": "GitHub"},
        {"icon": "🛟", "label": "Support"},
        {"icon": "☁️", "label": "API", "disabled": True},
        "separator",
        {"icon": "🚪", "label": "Log out", "shortcut": "⇧⌘Q"},
    ]
    result = dropdown.dropdown_menu_content(menu_id, items).render()
    # print("result", result)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)