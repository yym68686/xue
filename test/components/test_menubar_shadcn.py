from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from xue import HTML, Head, Body, Div, xue_initialize
from xue.components.menubar import (
    Menubar, MenubarMenu, MenubarTrigger, MenubarContent,
    MenubarItem, MenubarSeparator
)

xue_initialize(tailwind=True)
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    result = HTML(
        Head(
            title="Menubar Example"
        ),
        Body(
            Div(
                Menubar(
                    MenubarMenu(
                        MenubarTrigger("File", "file-menu"),
                        MenubarContent(
                            MenubarItem("New Tab", shortcut="⌘T"),
                            MenubarItem("New Window", shortcut="⌘N"),
                            MenubarItem("New Incognito Window", disabled=True),
                            MenubarSeparator(),
                            MenubarItem("Print...", shortcut="⌘P"),
                        ),
                        id="file-menu"
                    ),
                    MenubarMenu(
                        MenubarTrigger("Edit", "edit-menu"),
                        MenubarContent(
                            MenubarItem("Undo", shortcut="⌘Z"),
                            MenubarItem("Redo", shortcut="⇧⌘Z"),
                            MenubarSeparator(),
                            MenubarItem("Cut"),
                            MenubarItem("Copy"),
                            MenubarItem("Paste"),
                        ),
                        id="edit-menu"
                    ),
                    MenubarMenu(
                        MenubarTrigger("View", "view-menu"),
                        MenubarContent(
                            MenubarItem("Always Show Bookmarks Bar"),
                            MenubarItem("Always Show Full URLs"),
                            MenubarSeparator(),
                            MenubarItem("Reload", shortcut="⌘R"),
                            MenubarItem("Force Reload", shortcut="⇧⌘R", disabled=True),
                            MenubarSeparator(),
                            MenubarItem("Toggle Fullscreen"),
                            MenubarItem("Hide Sidebar"),
                        ),
                        id="view-menu"
                    ),
                ),
                class_="p-4"
            ),
            Div("Content goes here", class_="p-4"),
            class_="container mx-auto"
        )
    ).render()
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)