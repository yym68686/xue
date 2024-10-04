from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from xue import *
import os

app = FastAPI()

# 假设所有的Markdown文件都存储在 'markdown' 文件夹中
MARKDOWN_DIR = '.'

# 使用xue框架定义HTML结构

from bs4 import BeautifulSoup
import re

def html_to_xue(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    def parse_node(node):
        if node.name is None:
            return node.string

        tag_class = globals().get(node.name.capitalize(), HTMLTag)
        attrs = dict(node.attrs)

        # 处理 class 属性
        if 'class' in attrs:
            attrs['class_'] = attrs.pop('class')

        children = [parse_node(child) for child in node.children if child.name or not str(child).isspace()]

        return tag_class(*children, **attrs)

    return [parse_node(child) for child in soup.body.children if child.name or not str(child).isspace()]

def create_html_document(content):
    return HTML(
        Head(
            Title("Markdown Renderer"),
            Script(src="https://polyfill.io/v3/polyfill.min.js?features=es6"),
            Script(id="MathJax-script", async_="async", src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"),
            Style("""
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                pre { background-color: #f0f0f0; padding: 10px; border-radius: 5px; }
                code { font-family: monospace; }
            """)
        ),
        Body(
            H1("Markdown Renderer"),
            Div(*content, id="content")
        )
    )

@app.get("/{filename}", response_class=HTMLResponse)
async def read_markdown(filename: str):
    # ... (前面的代码保持不变)
    # 确保文件名以.md结尾
    if not filename.endswith('.md'):
        filename += '.md'

    file_path = os.path.join(MARKDOWN_DIR, filename)

    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    # 读取并渲染Markdown文件
    with open(file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 创建HTML文档
    doc = create_html_document(xue_content)
    print(doc.render())

    return doc.render()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)