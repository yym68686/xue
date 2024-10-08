from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from xue import HTML, Head, Body, Div, xue_initialize
from xue.components.menubar import (
    Menubar, MenubarMenu, MenubarTrigger, MenubarContent,
    MenubarItem, MenubarSeparator
)

from xue.components import data_table, dropdown, sheet, form, button, checkbox
from xue.components.model_config_row import model_config_row
import time

from fastapi import Form as FastapiForm
from typing import Optional, List


xue_initialize(tailwind=True)
app = FastAPI()

data = [
    {"status": "1", "provider": "gpt", "base_url": "https://api.openai.com/v1/chat/completions", "engine": "Admin", "tools": "true"},
    {"status": "2", "provider": "claude", "base_url": "https://api.openai.com/v1/chat/completions", "engine": "Manager", "tools": "true"},
    {"status": "3", "provider": "gemini", "base_url": "https://api.openai.com/v1/chat/completions", "engine": "User", "tools": "true"},
    {"status": "4", "provider": "llama", "base_url": "https://api.openai.com/v1/chat/completions", "engine": "User", "tools": "true"},
]

data_table_columns = [
    {"label": "Status", "value": "status", "sortable": True},
    {"label": "Provider", "value": "provider", "sortable": True},
    {"label": "Base url", "value": "base_url", "sortable": True},
    {"label": "Engine", "value": "engine", "sortable": True},
    {"label": "Tools", "value": "tools"},
]

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
            Div(
                data_table.data_table(data_table_columns, data, "users-table"),
                class_="p-4"
            ),
            # Div("Content goes here", class_="p-4"),
            # data_table.data_table(columns, data, "users-table"),
            Div(id="sheet-container"),  # 这里是 sheet 将被加载的地方
            class_="container mx-auto",
            id="body"
        )
    ).render()
    print(result)
    return result

@app.get("/dropdown-menu/{menu_id}/{row_id}", response_class=HTMLResponse)
async def get_columns_menu(menu_id: str, row_id: str):
    if menu_id == "dropdown-menu-⋮":
        columns = [
            {
                "label": "Edit",
                "value": "edit",
                "hx-get": f"/edit-sheet/{row_id}",  # 添加行ID
                "hx-target": "#sheet-container",
                "hx-swap": "innerHTML"
            },
            {"label": "Duplicate", "value": "duplicate"},
            {"label": "Delete", "value": "delete"},
            # "separator",
            # {"header": "More...", "accessor": "more"},
        ]
    else:
        columns = [
            {"label": "ID", "value": "id"},
            {"label": "Name", "value": "name"},
            {"label": "Email", "value": "email"},
            {"label": "Role", "value": "role"},
        ]
    result = dropdown.dropdown_menu_content(menu_id, columns).render()
    print(result)
    return result

    # print(data_table.get_column_visibility_menu("columns", columns).render())
    # return data_table.get_column_visibility_menu("columns", columns).render()

@app.post("/add-model", response_class=HTMLResponse)
async def add_model():
    new_model_id = f"model{hash(str(time.time()))}"  # 生成一个唯一的ID
    new_model = model_config_row(new_model_id).render()
    return new_model

@app.get("/edit-sheet/{row_id}", response_class=HTMLResponse)
async def get_edit_sheet(row_id: str):
    row_data = get_row_data(row_id)
    print("row_data", row_data)
    edit_sheet_content = sheet.SheetContent(
        sheet.SheetHeader(
            sheet.SheetTitle("Edit Item"),
            sheet.SheetDescription("Make changes to your item here.")
        ),
        sheet.SheetBody(
            Div(
                form.Form(
                    form.FormField("Provider", "provider", placeholder="Enter provider name", required=True),
                    form.FormField("Base URL", "base_url", placeholder="Enter base URL", required=True),
                    form.FormField("API Key", "api_key", type="password", placeholder="Enter API key"),
                    Div(
                        Div("Models", class_="text-lg font-semibold mb-2"),
                        Div(
                            model_config_row("model1", "gpt-4o", True),
                            model_config_row("model4", "claude-3-5-sonnet-20240620"),
                            id="models-container"
                        ),
                        button.button(
                            "Add Model",
                            class_="mt-2",
                            hx_post="/add-model",
                            hx_target="#models-container",
                            hx_swap="beforeend"
                        ),
                        class_="mb-4"
                    ),
                    Div(
                        checkbox.checkbox("tools", "Enable Tools", checked=True),
                        class_="mb-4"
                    ),
                    form.FormField("Notes", "notes", placeholder="Enter any additional notes"),
                    Div(
                        button.button("Submit", variant="primary", type="submit"),
                        button.button("Cancel", variant="outline", class_="ml-2"),
                        class_="flex justify-end mt-4"
                    ),
                    hx_post=f"/submit/{row_id}",
                    hx_swap="outerHTML",
                    # hx_target=f"#row-{row_id}",
                    hx_target="body",
                    class_="space-y-4"
                ),
                class_="container mx-auto p-4 max-w-2xl"
            )
        )
    )

    result = sheet.Sheet(
        "edit-sheet",
        Div(),
        edit_sheet_content,
        width="80%",
        max_width="800px"
    ).render()
    return result

def get_row_data(row_id):
    index = int(row_id)
    return data[index]

def update_row_data(row_id, updated_data):
    print(row_id, updated_data)
    index = int(row_id)
    data[index] = updated_data

@app.post("/submit/{row_id}", response_class=HTMLResponse)
async def submit_form(
    row_id: str,
    provider: str = FastapiForm(...),
    base_url: str = FastapiForm(...),
    api_key: Optional[str] = FastapiForm(None),
    models: List[str] = FastapiForm([]),
    tools: Optional[str] = FastapiForm(None),
    notes: Optional[str] = FastapiForm(None)
):
    # 更新数据
    updated_data = {
        "status": "1",  # 假设状态不变
        "provider": provider,
        "base_url": base_url,
        "engine": ", ".join(models),  # 假设 engine 是模型列表
        "tools": "true" if tools else "false",
    }

    # 更新数据存储（这里你需要实现实际的数据更新逻辑）
    update_row_data(row_id, updated_data)

    # 返回更新后的行 HTML
    return await root()
    # return data_table.render_row(updated_data, row_id, data_table_columns)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)