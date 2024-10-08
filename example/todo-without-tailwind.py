import uuid
from xue import *
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Form as fastapiForm, HTTPException

app = FastAPI()

# 模拟数据库
todos = []

class Todo(BaseModel):
    id: str
    content: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    result = HTML(
        Head(
            Title("HTMX Todo App"),
        ),
        Body(
            H1("HTMX Todo App"),
            Form(
                Input(type="text", name="content", placeholder="Enter a new todo", required="required"),
                Button("Add Todo", type="submit"),
                hx_post="/todos",
                hx_target="#todo-list",
                hx_swap="beforeend"
            ),
            Ul(id="todo-list")
        )
    ).render()

    return result

@app.post("/todos", response_class=HTMLResponse)
async def create_todo(content: str = fastapiForm(...)):
    todo = Todo(id=str(uuid.uuid4()), content=content)
    todos.append(todo)
    return Li(
        todo.content,
        Button("Delete", hx_delete=f"/todos/{todo.id}", hx_target=f"#todo-{todo.id}", hx_swap="outerHTML"),
        id=f"todo-{todo.id}"
    ).render()

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