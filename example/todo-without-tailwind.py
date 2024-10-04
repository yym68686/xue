from fastapi import FastAPI, Request, Form as fastapiForm, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uuid

app = FastAPI()

# 模拟数据库
todos = []

class Todo(BaseModel):
    id: str
    content: str

# HTML构建系统
class HTMLTag:
    def __init__(self, *children, **attributes):
        self.attributes = attributes
        self.children = list(children)
        if 'class_' in self.attributes:
            self.attributes['class'] = self.attributes.pop('class_')

    def render(self, indent=0):
        attrs = ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in self.attributes.items())
        if attrs != "":
            attrs = " " + attrs

        tag_name = self.__class__.__name__.lower()
        opening_tag = f"{' ' * indent}<{tag_name}{attrs}>"

        if not self.children:
            return f"{opening_tag}</{tag_name}>"

        content = '\n'.join(
            child.render(indent + 2) if isinstance(child, HTMLTag) else f"{' ' * (indent + 2)}{child}"
            for child in self.children
        )

        return f"{opening_tag}\n{content}\n{' ' * indent}</{tag_name}>"

class HTML(HTMLTag):
    def render(self, indent=0):
        return f"<!DOCTYPE html>\n{super().render(indent)}"

class Head(HTMLTag):
    def __init__(self, *children, **attributes):
        default_children = [
            Meta(charset="UTF-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            Script(src="https://unpkg.com/htmx.org@1.9.0"),
        ]
        super().__init__(*(default_children + list(children)), **attributes)

class Body(HTMLTag): pass
class Title(HTMLTag): pass
class Meta(HTMLTag):
    def render(self, indent=0):
        attrs = ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in self.attributes.items())
        return f"{' ' * indent}<meta {attrs}>"

class Script(HTMLTag): pass
class Link(HTMLTag):
    def render(self, indent=0):
        attrs = ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in self.attributes.items())
        return f"{' ' * indent}<link {attrs}>"
class Style(HTMLTag): pass
class H1(HTMLTag): pass
class Form(HTMLTag): pass
class Input(HTMLTag):
    def render(self, indent=0):
        attrs = ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in self.attributes.items())
        return f"{' ' * indent}<input {attrs}>"

class Button(HTMLTag): pass
class Ul(HTMLTag): pass
class Li(HTMLTag): pass
class Div(HTMLTag): pass
class Span(HTMLTag): pass

# 创建HTML文档结构
def create_html_document():
    return HTML(
        Head(
            Title("HTMX Todo App"),
            Style("""
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                ul { list-style-type: none; padding: 0; }
                li { margin-bottom: 10px; }
            """)
        ),
        Body(
            H1("HTMX Todo App"),
            Form(
                Input(type="text", name="content", placeholder="Enter a new todo", required="required"),
                Button("Add Todo", type="submit"),
                hx_post="/todos", hx_target="#todo-list", hx_swap="beforeend"
            ),
            Ul(id="todo-list")
        )
    )

# 渲染单个待办事项的函数
def render_todo(todo):
    return Li(
        todo.content,
        Button("Delete", hx_delete=f"/todos/{todo.id}", hx_target=f"#todo-{todo.id}", hx_swap="outerHTML"),
        id=f"todo-{todo.id}"
    ).render()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    doc = create_html_document()
    # print(doc.render())
    return doc.render()

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