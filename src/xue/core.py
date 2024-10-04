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