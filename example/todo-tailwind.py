from fastapi import FastAPI, Request, Form as fastapiForm, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uuid
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

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