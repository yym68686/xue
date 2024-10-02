from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import uuid

app = FastAPI()

# 模拟数据库
todos = []

class Todo(BaseModel):
    id: str
    content: str

# 用于HTML转义的辅助函数
def escape_html(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# HTML模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTMX Todo App</title>
    <script src="https://unpkg.com/htmx.org@1.9.0"></script>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin-bottom: 10px; }}
    </style>
</head>
<body>
    <h1>HTMX Todo App</h1>
    <form hx-post="/todos" hx-target="#todo-list" hx-swap="beforeend">
        <input type="text" name="content" placeholder="Enter a new todo" required>
        <button type="submit">Add Todo</button>
    </form>
    <ul id="todo-list">
        {todo_list}
    </ul>
</body>
</html>
"""

# 渲染单个待办事项的函数
def render_todo(todo):
    return f"""
    <li id="todo-{todo.id}">
        {escape_html(todo.content)}
        <button hx-delete="/todos/{todo.id}" hx-target="#todo-{todo.id}" hx-swap="outerHTML">Delete</button>
    </li>
    """

@app.get("/", response_class=HTMLResponse)
async def read_root():
    todo_list_html = "".join(render_todo(todo) for todo in todos)
    return HTML_TEMPLATE.format(todo_list=todo_list_html)

@app.post("/todos", response_class=HTMLResponse)
async def create_todo(content: str = Form(...)):
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