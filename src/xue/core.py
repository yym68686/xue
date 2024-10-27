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
                for child in self.children if child is not None  # 过滤掉 None 值
            )
            return f"{opening_tag}{content}</{tag_name}>"
        else:
            content = '\n'.join(
                child.render(indent + 2) if isinstance(child, HTMLTag) else f"{' ' * (indent + 2)}{child}"
                for child in self.children if child is not None  # 过滤掉 None 值
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
        cls.default_children += new_default_children

    @classmethod
    def add_default_children(cls, children):
        for child in children:
            if hasattr(child, 'attributes') and 'id' in child.attributes:
                # 如果已经存在相同 id 的元素，则替换它
                cls.default_children = [c for c in cls.default_children if not (hasattr(c, 'attributes') and 'id' in c.attributes and c.attributes['id'] == child.attributes['id'])]
            cls.default_children.append(child)

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
class Strong(HTMLTag): pass
class P(HTMLTag): pass
class Pre(HTMLTag): pass
class Br(HTMLTag):
    def render(self, indent=0):
        return f"{' ' * indent}<br>"
class A(HTMLTag): pass
class Image(HTMLTag):
    def render(self, indent=0):
        attrs = ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in self.attributes.items())
        return f"{' ' * indent}<img {attrs}>"

class Raw(HTMLTag): pass
class Label(HTMLTag): pass
class Table(HTMLTag): pass
class Thead(HTMLTag): pass
class Tbody(HTMLTag): pass
class Tr(HTMLTag): pass
class Th(HTMLTag): pass
class Td(HTMLTag): pass

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
            document.querySelectorAll(".math-display, .math-inline").forEach(function(el) {
                katex.render(el.textContent, el, {
                    displayMode: el.classList.contains("math-display"),
                    throwOnError: false
                });
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
                            light: '#ffffff',
                            dark: '#1a202c',
                        },
                        content: {
                            light: '#f7fafc',
                            dark: '#2d3748',
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
        body {
            transition: background-color 0.3s ease;
        }
        .dark body {
            background-color: #1a202c;
            color: #e2e8f0;
        }
    """),
    # Script("""
    #     tailwind.config = {
    #         darkMode: 'class',
    #         theme: {
    #             extend: {
    #                 colors: {
    #                     primary: {
    #                         light: '#3B82F6',
    #                         dark: '#60A5FA',
    #                     },
    #                     background: {
    #                         light: 'var(--background-light)',
    #                         dark: 'var(--background-dark)',
    #                     },
    #                     content: {
    #                         light: 'var(--content-light)',
    #                         dark: 'var(--content-dark)',
    #                     },
    #                 },
    #             },
    #         },
    #     }

    #     // 监听系统主题变化
    #     function updateTheme() {
    #         if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    #             document.documentElement.classList.add('dark');
    #         } else {
    #             document.documentElement.classList.remove('dark');
    #         }
    #     }

    #     // 初始化主题
    #     updateTheme();

    #     // 监听系统主题变化
    #     window.matchMedia('(prefers-color-scheme: dark)').addListener(updateTheme);
    # """),
    # Style("""
    #     :root {
    #         --background-light: #ffffff;
    #         --background-dark: #1a202c;
    #         --content-light: #f7fafc;
    #         --content-dark: #2d3748;
    #     }
    # """),
]

# LazyIcon 相关脚本
lazy_icon_scripts = [
    Script("""
        function loadSVGContent() {
            console.log('loadSVGContent called');
            document.querySelectorAll('.icon-container').forEach(container => {
                const img = container.querySelector('img.lazy-icon');
                const svg = container.querySelector('svg');
                if (img && svg) {
                    console.log('Processing image:', img.src);
                    fetch(img.src)
                        .then(response => response.text())
                        .then(svgContent => {
                            console.log('SVG content loaded for:', img.src);
                            const parser = new DOMParser();
                            const svgDoc = parser.parseFromString(svgContent, 'image/svg+xml');
                            const newSvg = svgDoc.querySelector('svg');
                            if (newSvg) {
                                newSvg.classList = svg.classList;
                                newSvg.removeAttribute('width');
                                newSvg.removeAttribute('height');
                                svg.parentNode.replaceChild(newSvg, svg);
                                img.style.display = 'none';
                            }
                        })
                        .catch(error => console.error('Error loading SVG:', error));
                }
            });
        }

        document.addEventListener('DOMContentLoaded', loadSVGContent);
        document.body.addEventListener('htmx:afterSettle', loadSVGContent);
    """, id="load-svg-script"),
    Script("""
        htmx.on('htmx:afterSettle', function(event) {
            loadSVGContent();
        });
    """, id="load-svg-script-htmx")
]

import os
import httpx
import inspect
from pathlib import Path

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

class IconManager:
    def __init__(self, icon_dir="icons"):
        self.icon_dir = os.path.join(CURRENT_DIR, icon_dir)
        self.ensure_icon_dir()

    def ensure_icon_dir(self):
        """确保图标目录存在"""
        Path(self.icon_dir).mkdir(parents=True, exist_ok=True)

    def get_icon_path(self, icon_name):
        """获取图标的本地路径"""
        return os.path.join(self.icon_dir, f"{icon_name}.svg")

    def has_local_icon(self, icon_name):
        """检查图标是否在本地存在"""
        return os.path.exists(self.get_icon_path(icon_name))

    async def download_icon(self, icon_name):
        """下载图标到本地"""
        if not self.has_local_icon(icon_name):
            url = f"https://unpkg.com/lucide-static@latest/icons/{icon_name}.svg"
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url)
                    if response.status_code == 200:
                        with open(self.get_icon_path(icon_name), 'wb') as f:
                            f.write(response.content)
                        return True
            except Exception as e:
                print(f"Error downloading icon {icon_name}: {e}")
                return False
        return True

    def get_icon_content(self, icon_name):
        """获取图标内容"""
        if self.has_local_icon(icon_name):
            with open(self.get_icon_path(icon_name), 'r') as f:
                return f.read()
        return None

# 创建全局图标管理器实例
icon_manager = IconManager(icon_dir="icons")

class LazyIcon(HTMLTag):

    def __init__(self, icon_name, label, class_="mr-2 h-4 w-4 inline"):
        super().__init__()
        self.icon_name = icon_name
        self.label = label
        self.class_ = class_

    def render(self, indent=0):
        # 检查本地是否有图标
        icon_content = icon_manager.get_icon_content(self.icon_name)

        if icon_content:
            # 如果本地有图标，直接使用本地内容
            svg_content = icon_content.replace('class="', f'class="{self.class_} ')
            return Div(
                Raw(svg_content),
                class_="inline-block icon-container",
            ).render(indent)
        else:
            # 如果本地没有图标，使用远程加载
            url = f"https://unpkg.com/lucide-static@latest/icons/{self.icon_name}.svg"
            return Div(
                Image(src=url, alt=f"{self.label} icon", class_=f"{self.class_} lazy-icon", style="display: none;"),
                Raw(f'<svg class="{self.class_}" data-icon="{self.icon_name}"></svg>'),
                class_="inline-block icon-container",
            ).render(indent)

def detect_component_usage():
    """检测主程序是否导入了特定组件"""
    # 获取调用栈
    stack = inspect.stack()
    # 查找主程序文件
    main_module = None
    for frame in stack:
        if frame.filename != __file__ and not frame.filename.endswith('importlib/__init__.py'):
            main_module = frame.filename
            break

    if not main_module:
        return set()

    # 读取主程序文件内容
    try:
        with open(main_module, 'r') as f:
            content = f.read()
    except:
        return set()

    # 检测使用的组件
    used_components = set()
    component_patterns = {
        'sidebar': ['from xue.components.sidebar import', 'from xue.components import sidebar'],
        'dropdown': ['from xue.components.dropdown import', 'from xue.components import dropdown'],
        # 添加其他需要检测的组件
    }

    for component, patterns in component_patterns.items():
        if any(pattern in content for pattern in patterns):
            used_components.add(component)

    return used_components

def xue_initialize(katex=False, prism_code_highlight=False, prism_copy_to_clipboard=False, tailwind=False):
    init_setting = [
        Meta(charset="UTF-8"),
        Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
        Script(src="https://unpkg.com/htmx.org@1.9.0"),
    ]

    # 检测组件使用情况
    used_components = detect_component_usage()

    # 如果使用了 sidebar 或 dropdown，添加 LazyIcon 脚本
    if {'sidebar', 'dropdown'} & used_components:
        init_setting.extend(lazy_icon_scripts)

    if tailwind:
        init_setting.extend(tailwind_setting)
    if katex:
        init_setting.extend(katex_setting)
    if prism_code_highlight:
        init_setting.extend(prism_code_highlight_setting)
    if prism_copy_to_clipboard:
        init_setting.extend(prism_copy_to_clipboard_setting)

    Head.set_default_children(init_setting)