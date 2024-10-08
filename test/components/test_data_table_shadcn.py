from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from xue import HTML, Head, Body, Div, xue_initialize
from xue.components import data_table

xue_initialize(tailwind=True)
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    columns = [
        {"header": "ID", "accessor": "id", "sortable": True},
        {"header": "Name", "accessor": "name", "sortable": True},
        {"header": "Email", "accessor": "email", "sortable": True},
        {"header": "Role", "accessor": "role"},
    ]

    data = [
        {"id": "1", "name": "John Doe", "email": "john@example.com", "role": "Admin"},
        {"id": "2", "name": "Alice Brown", "email": "alice@example.com", "role": "Manager"},
        {"id": "3", "name": "Jane Smith", "email": "jane@example.com", "role": "User"},
        {"id": "4", "name": "Bob Johnson", "email": "bob@example.com", "role": "User"},
    ]

    result = HTML(
        Head(title="Data Table Example"),
        Body(
            Div(
                data_table.data_table(columns, data, "users-table"),
                class_="container mx-auto p-4"
            )
        )
    ).render()
    print(result)
    return result

@app.get("/dropdown-menu/{menu_id}", response_class=HTMLResponse)
async def get_columns_menu():
    columns = [
        {"header": "ID", "accessor": "id"},
        {"header": "Name", "accessor": "name"},
        {"header": "Email", "accessor": "email"},
        {"header": "Role", "accessor": "role"},
    ]
    print(data_table.get_column_visibility_menu("columns", columns).render())
    return data_table.get_column_visibility_menu("columns", columns).render()

@app.get("/dropdown-menu/row-actions-{row_id}", response_class=HTMLResponse)
async def get_row_actions_menu(row_id: str):
    return data_table.get_row_actions_menu(row_id).render()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)