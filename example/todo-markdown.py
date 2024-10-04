from fastapi import FastAPI, Request, Form as fastapiForm, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uuid
from fastapi.staticfiles import StaticFiles
from xue import *

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")



# 创建HTML文档结构
def create_html_document():
    return HTML(
        Head(
            Title("HTMX Todo App"),
            Link(rel="stylesheet", href="/static/styles.css"),
        ),
        Body(
            Div(
                H1("HTMX Todo App", class_="text-3xl font-bold mb-6"),
                Form(
                    Input(type="text", name="content", placeholder="Enter a new todo", required="required",
                          class_="w-full px-4 py-2 text-gray-700 bg-white border rounded-md focus:border-blue-400 focus:outline-none focus:ring focus:ring-blue-300 focus:ring-opacity-40 mb-4"),
                    Button("Add Todo", type="submit",
                           class_="px-4 py-2 font-bold text-white bg-blue-500 rounded-md hover:bg-blue-600 focus:outline-none focus:shadow-outline"),
                    hx_post="/todos", hx_target="#todo-list", hx_swap="beforeend",
                    class_="space-y-4"
                ),
                Ul(id="todo-list", class_="mt-6 space-y-4"),
                class_="container mx-auto px-4 py-8"
            ),
            class_="bg-gray-100 min-h-screen"
        )
    )

# 渲染单个待办事项的函数
def render_todo(todo):
    return Li(
        Div(
            Span(todo.content, class_="text-lg"),
            Button("Delete",
                   class_="ml-4 px-3 py-1 text-sm font-medium text-white bg-red-500 rounded-md hover:bg-red-600 focus:outline-none focus:shadow-outline",
                   hx_delete=f"/todos/{todo.id}", hx_target=f"#todo-{todo.id}", hx_swap="outerHTML"),
            class_="flex items-center justify-between p-4 bg-white rounded-lg shadow"
        ),
        id=f"todo-{todo.id}"
    ).render()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    doc = create_html_document()
    # print(doc.render())
    return doc.render()

# 模拟数据库
todos = []

class Todo(BaseModel):
    id: str
    content: str

@app.post("/todos", response_class=HTMLResponse)
async def create_todo(content: str = fastapiForm(...)):
    todo = Todo(id=str(uuid.uuid4()), content=content)
    todos.append(todo)
    return render_todo(todo)

@app.delete("/todos/{todo_id}", response_class=HTMLResponse)
async def delete_todo(todo_id: str):
    for todo in todos:
        if todo.id == todo_id:
            todos.remove(todo)
            return ""
    raise HTTPException(status_code=404, detail="Todo not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)