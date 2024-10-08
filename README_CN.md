# Xue

[英文](README.md) | [中文](README_CN.md)

Xue（show，[ˈʃəʊ]）是一个极简主义前端 web 框架，用于快速构建简单的 web 应用程序。本项目灵感来源于 [FastHTML](https://github.com/AnswerDotAI/fasthtml). FastHTML 非常好用，但是在我构建我的 blog 程序的时候，我发现我无法解决 markdown 渲染问题的一些 bug。因此，我决定自己写一个极简主义的 web 框架。我不喜欢使用别人的框架，因为如果我遇到了问题，我将不知道如何解决。如果你跟我一样使用 python 作为开发语言，我想 xue 比较适合你快速开发 web 应用。

## 安装

```bash
pip install xue
```

## 使用

你可以使用 xue 仅使用 50 行代码构建一个简单的 todo list web 应用程序，如下所示:

```python
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
```

## 组件

Xue 提供了一些简单的组件，你可以使用这些组件构建你的 web 应用程序。

目前已经写好的组件有：button，checkbox，dropdown，form，input，select。采用 tailwindcss 进行样式设计。模仿 shadcn/ui 组件库，包括丝滑的动态效果，优雅简洁美观的界面，平滑的动画效果和响应式交互。

## LLM 友好

由于这是一个新的框架，如果问目前的 LLM 不会提供有效的建议，所以我写了一个自动生成 LLM 友好的文档的脚本。你可以使用以下命令生成 LLM 友好的文档:

```bash
python llm_context.py
```

改脚本会自动把文档保存在 `llm_context.txt` 文件中。直接复制给 LLM 提问即可得到有效的建议。

## Tailwind CSS

Tailwind CSS 的 JIT (Just-In-Time) 模式，以下是实现步骤:

1. 安装必要的依赖:

```bash
npm init -y
npm install tailwindcss@latest postcss@latest autoprefixer@latest
```

2. 创建 Tailwind CSS 配置文件:

```bash
npx tailwindcss init -p
```

这将创建 `tailwind.config.js` 和 `postcss.config.js` 文件。

3. 修改 `tailwind.config.js`:

```javascript
module.exports = {
  mode: 'jit',
  purge: [
    './templates/**/*.html',
    './static/**/*.js',
    './your_python_file.py',  // 包含你的 Python 代码的文件
  ],
  darkMode: false,
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
```

4. 创建一个 `input.css` 文件:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

5. 添加一个 npm 脚本到 `package.json`:

```json
"scripts": {
  "build-css": "tailwindcss -i ./input.css -o ./static/styles.css --watch"
}
```

6. 运行构建脚本:

```bash
npm run build-css
```

这将启动一个监视进程，每当你的 Python 文件发生变化时，它都会重新生成 CSS。