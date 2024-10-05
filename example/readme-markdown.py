import os
# from xue import *
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from parse_markdown import get_entities_from_markdown_file, Title as TitleEntity, CodeBlock, ListItem, Link as LinkEntity, EmptyLine, OrderList, UnOrderList, Paragraph, DisplayMath, OrderedListItem, UnorderedListItem, InlineLink, InlineMath, CompositeEntity

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

        if isinstance(self, (Code, Pre)):
            # 对于 Code 和 Pre 标签，不添加额外的缩进和换行
            content = ''.join(
                child.render() if isinstance(child, HTMLTag) else str(child)
                for child in self.children
            )
            return f"{opening_tag}{content}</{tag_name}>"
        else:
            content = '\n'.join(
                child.render(indent + 2) if isinstance(child, HTMLTag) else f"{' ' * (indent + 2)}{child}"
                for child in self.children
            )
            return f"{opening_tag}\n{content}\n{' ' * indent}</{tag_name}>"

class HTML(HTMLTag):
    def render(self, indent=0):
        return f"<!DOCTYPE html>\n{super().render(indent)}"

class Meta(HTMLTag):
    def render(self, indent=0):
        attrs = ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in self.attributes.items())
        return f"{' ' * indent}<meta {attrs}>"

class Script(HTMLTag): pass
class Head(HTMLTag):
    default_children = [
        Meta(charset="UTF-8"),
        Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
        Script(src="https://unpkg.com/htmx.org@1.9.0"),
    ]

    @classmethod
    def set_default_children(cls, new_default_children):
        cls.default_children = new_default_children

    def __init__(self, *children, **attributes):
        all_children = self.default_children + list(children)
        super().__init__(*all_children, **attributes)

class Body(HTMLTag): pass
class Title(HTMLTag): pass
class Link(HTMLTag):
    def render(self, indent=0):
        attrs = ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in self.attributes.items())
        return f"{' ' * indent}<link {attrs}>"
class Style(HTMLTag): pass
class H1(HTMLTag): pass
class H2(HTMLTag): pass
class H3(HTMLTag): pass
class H4(HTMLTag): pass
class H5(HTMLTag): pass
class H6(HTMLTag): pass
class Code(HTMLTag): pass
class Form(HTMLTag): pass
class Input(HTMLTag):
    def render(self, indent=0):
        attrs = ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in self.attributes.items())
        return f"{' ' * indent}<input {attrs}>"

class Button(HTMLTag): pass
class Ul(HTMLTag): pass
class Ol(HTMLTag):
    def __init__(self, *children, start=None, **attributes):
        super().__init__(*children, **attributes)
        if start is not None:
            self.attributes['start'] = start
class Li(HTMLTag): pass
class Div(HTMLTag): pass
class Span(HTMLTag): pass
class P(HTMLTag): pass
class Pre(HTMLTag): pass
class Br(HTMLTag):
    def render(self, indent=0):
        return f"{' ' * indent}<br>"
class A(HTMLTag): pass

prism_copy_to_clipboard_setting = [
    Script(src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/plugins/copy-to-clipboard/prism-copy-to-clipboard.min.js"),
    Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/plugins/copy-to-clipboard/prism-copy-to-clipboard.min.css"),
    Style("""
        .code-block-wrapper {
            position: relative;
            margin-bottom: 1rem;
        }
        .copy-button {
            position: absolute;
            top: 0.5rem;
            right: 0.5rem;
            padding: 0.25rem 0.5rem;
            font-size: 0.75rem;
            background-color: rgba(209, 213, 219, 0.8);
            color: rgba(55, 65, 81, 1);
            border-radius: 0.25rem;
            border: 1px solid rgba(209, 213, 219, 1);
            cursor: pointer;
            transition: background-color 0.2s;
            z-index: 10;
        }
        .copy-button:hover {
            background-color: rgba(229, 231, 235, 0.8);
        }
        pre {
            margin-top: 0 !important;
        }
        .dark .copy-button {
            background-color: rgba(55, 65, 81, 0.8);
            color: rgba(209, 213, 219, 1);
            border-color: rgba(75, 85, 99, 1);
        }
        .dark .copy-button:hover {
            background-color: rgba(75, 85, 99, 0.8);
        }
    """),
    Script("""
        document.addEventListener("DOMContentLoaded", function() {
            Prism.highlightAll();

            document.querySelectorAll('pre').forEach(function(preElement) {
                var wrapper = document.createElement('div');
                wrapper.className = 'code-block-wrapper';
                preElement.parentNode.insertBefore(wrapper, preElement);
                wrapper.appendChild(preElement);

                var copyButton = document.createElement('button');
                copyButton.textContent = 'Copy';
                copyButton.className = 'copy-button';
                wrapper.appendChild(copyButton);

                copyButton.addEventListener('click', function() {
                    var codeElement = preElement.querySelector('code');
                    var textArea = document.createElement('textarea');
                    textArea.value = codeElement.textContent;
                    document.body.appendChild(textArea);
                    textArea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textArea);

                    copyButton.textContent = 'Copied!';
                    copyButton.style.backgroundColor = 'rgba(34, 197, 94, 0.8)';
                    copyButton.style.color = 'white';
                    setTimeout(function() {
                        copyButton.textContent = 'Copy';
                        copyButton.style.backgroundColor = '';
                        copyButton.style.color = '';
                    }, 2000);
                });
            });
        });
    """),
]

prism_code_highlight_setting = [
    Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/themes/prism.min.css", id="prism-light"),
    Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/themes/prism-okaidia.min.css", id="prism-dark"),
    # Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/themes/prism-tomorrow.min.css", id="prism-dark"),
    Script(src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/components/prism-core.min.js"),
    Script(src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/plugins/autoloader/prism-autoloader.min.js"),
    Style("""
        @media (prefers-color-scheme: dark) {
            #prism-light { display: none; }
        }
        @media (prefers-color-scheme: light) {
            #prism-dark { display: none; }
        }
    """)
]

prism_theme_switch_script = Script("""
    document.addEventListener("DOMContentLoaded", function() {
        Prism.highlightAll();
    });
""")

prism_code_highlight_setting.append(prism_theme_switch_script)

katex_setting = [
    Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/katex@0.16.4/dist/katex.min.css"),
    Script(src="https://cdn.jsdelivr.net/npm/katex@0.16.4/dist/katex.min.js"),
    Script("""
        document.addEventListener("DOMContentLoaded", function() {
            document.querySelectorAll(".math-display").forEach(function(el) {
                katex.render(el.textContent, el, {displayMode: true});
            });
        });
    """),
]

tailwind_setting = [
    Script(src="https://cdn.tailwindcss.com"),
    Script("""
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        primary: {
                            light: '#3B82F6',
                            dark: '#60A5FA',
                        },
                        background: {
                            light: 'var(--background-light)',
                            dark: 'var(--background-dark)',
                        },
                        content: {
                            light: 'var(--content-light)',
                            dark: 'var(--content-dark)',
                        },
                    },
                },
            },
        }

        // 监听系统主题变化
        function updateTheme() {
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                document.documentElement.classList.add('dark');
            } else {
                document.documentElement.classList.remove('dark');
            }
        }

        // 初始化主题
        updateTheme();

        // 监听系统主题变化
        window.matchMedia('(prefers-color-scheme: dark)').addListener(updateTheme);
    """),
    Style("""
        :root {
            --background-light: #ffffff;
            --background-dark: #1a202c;
            --content-light: #f7fafc;
            --content-dark: #2d3748;
        }
    """),
]

def xue_initialize(katex=False, prism_code_highlight=False, prism_copy_to_clipboard=False, tailwind=False):
    init_setting = [
        Meta(charset="UTF-8"),
        Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
        Script(src="https://unpkg.com/htmx.org@1.9.0"),
    ]
    if tailwind:
        init_setting += tailwind_setting
    if katex:
        init_setting += katex_setting
    if prism_code_highlight:
        init_setting += prism_code_highlight_setting
    if prism_copy_to_clipboard:
        init_setting += prism_copy_to_clipboard_setting

    Head.set_default_children(init_setting)




xue_initialize(katex=True, prism_code_highlight=True, prism_copy_to_clipboard=True, tailwind=True)
# 使用xue框架定义HTML结构
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
            # Script(src="https://polyfill.io/v3/polyfill.min.js?features=es6"),
        ),
        Body(
            Div(
                Div(content, class_="content-wrapper p-6 max-w-3xl mx-auto"),
                class_="page-wrapper"
            ),
            class_="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100"
        )
    )

def convert_entities_to_xue(entities):
    def process_entity(entity):
        if isinstance(entity, TitleEntity):
            header_tag = globals()[f'H{entity.level}']
            size_class = {
                1: "text-4xl",
                2: "text-3xl",
                3: "text-2xl",
                4: "text-xl",
                5: "text-lg",
                6: "text-base"
            }.get(entity.level, "text-base")
            return header_tag(entity.content, class_=f"font-bold mb-4 text-gray-800 dark:text-gray-200 {size_class}")

        elif isinstance(entity, CodeBlock):
            code_block = Pre(
                Code(entity.content, class_=f"language-{entity.language}"),
                class_="bg-gray-100 dark:bg-gray-800 rounded-lg p-4 overflow-x-auto"
            )
            return Div(code_block, class_="code-block-wrapper")

        # elif isinstance(entity, ListItem):
        #     print("entity", entity)
        #     print("entity.content", entity.content)
        #     print("entity.children", entity.children)
        #     return Li(process_children(entity.children) if hasattr(entity, 'children') else entity.content, class_="mb-2")

        elif isinstance(entity, LinkEntity) or isinstance(entity, InlineLink):
            return A(entity.content, href=entity.url, class_="mr-2 text-primary-light dark:text-primary-dark hover:underline")

        elif isinstance(entity, EmptyLine):
            return None

        elif isinstance(entity, OrderedListItem):
            content = process_children(entity.children) if hasattr(entity, 'children') else [entity.content]
            return Ol(Li(*content, class_="mb-2"), start=entity.index, class_="list-decimal list-inside mb-4")

        elif isinstance(entity, UnorderedListItem):
            content = process_children(entity.children) if hasattr(entity, 'children') else [entity.content]
            return Ul(Li(Div(*content, class_ = "flex items-center"), class_="mb-0"), class_="list-disc list-inside mb-0")

        elif isinstance(entity, Paragraph):
            return P(process_inline_elements(entity.content), class_="mr-2 whitespace-nowrap")

        elif isinstance(entity, DisplayMath):
            return Div(entity.content, class_="math-display bg-gray-50 dark:bg-gray-800 p-4 rounded-lg mb-4")

        elif isinstance(entity, InlineMath):
            return Span(entity.content, class_="math-inline")

        elif isinstance(entity, CompositeEntity):
            return Div(*[process_entity(child) for child in entity.children], class_="composite-entity flex items-center mb-0")

        else:
            return str(entity)

    def process_children(children):
        return [Span(process_entity(child), class_="mr-2 flex-shrink-0") for child in children if child is not None if process_entity(child) is not None]

    def process_inline_elements(content):
        # 这里可以添加处理行内元素的逻辑，比如链接、行内数学公式等
        # 现在我们简单地返回内容
        return content

    html_body = Body(class_="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 p-6 max-w-3xl mx-auto")
    html_body.children.extend(process_children(entities))

    return html_body

MARKDOWN_DIR = '/Users/yanyuming/Downloads/GitHub/PurePage/'
app = FastAPI()
@app.get("/{filename}", response_class=HTMLResponse)
async def read_markdown(filename: str):
    # 确保文件名以.md结尾
    if not filename.endswith('.md'):
        filename += '.md'

    file_path = os.path.join(MARKDOWN_DIR, filename)

    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    entities = get_entities_from_markdown_file(file_path)
    html_doc = convert_entities_to_xue(entities)
    # print(html_doc)

    # 创建HTML文档
    doc = create_html_document(html_doc)
    print(doc.render())

    return doc.render()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "__main__:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        ws="none",
        # log_level="warning"
    )