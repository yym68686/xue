from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from xue import HTML, Head, Body, Div, Script, xue_initialize, Style
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
        {"icon": "user", "label": "Profile", "shortcut": "⇧⌘P"},
        {"icon": "credit-card", "label": "Billing", "shortcut": "⌘B"},
        {"icon": "settings", "label": "Settings", "shortcut": "⌘S"},
        {"icon": "keyboard", "label": "Keyboard shortcuts", "shortcut": "⌘K"},
        "separator",
        {"icon": "users", "label": "Team"},
        {"icon": "plus", "label": "New Team", "shortcut": "⌘+T"},
        "separator",
        {"icon": "github", "label": "GitHub"},
        {"icon": "life-buoy", "label": "Support"},
        {"icon": "cloud", "label": "API", "disabled": True},
        "separator",
        {"icon": "log-out", "label": "Log out", "shortcut": "⇧⌘Q"},
    ]
    result = dropdown.dropdown_menu_content(menu_id, items).render()
    print("result", result)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)