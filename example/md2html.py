from parse_markdown import *
from xue import *

def convert_entities_to_html(entities):
    html_body = Body()

    for entity in entities:
        if isinstance(entity, Title):
            header_tag = globals()[f'H{entity.level}']
            html_body.children.append(header_tag(entity.content))

        elif isinstance(entity, CodeBlock):
            pre = HTMLTag('pre')
            code = Code(entity.content, class_=f"language-{entity.language}")
            pre.children.append(code)
            html_body.children.append(pre)

        elif isinstance(entity, ListItem):
            html_body.children.append(Li(entity.content))

        elif isinstance(entity, Link):
            html_body.children.append(HTMLTag('a', entity.content, href=entity.url))

        elif isinstance(entity, EmptyLine):
            html_body.children.append(HTMLTag('br'))

        elif isinstance(entity, OrderList):
            ol = Ol(start=entity.index)
            ol.children.append(Li(entity.content))
            html_body.children.append(ol)

        elif isinstance(entity, Paragraph):
            html_body.children.append(P(entity.content))

        elif isinstance(entity, Br):
            html_body.children.append(Br())

        elif isinstance(entity, DisplayMath):
            math_div = Div(class_="math-display")
            math_div.children.append(entity.content)
            html_body.children.append(math_div)

    html_doc = HTML(
        Head(
            Title("Markdown to HTML"),
            Meta(charset="UTF-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/katex@0.16.4/dist/katex.min.css"),
            Script(src="https://cdn.jsdelivr.net/npm/katex@0.16.4/dist/katex.min.js"),
            Script("""
                document.addEventListener("DOMContentLoaded", function() {
                    document.querySelectorAll(".math-display").forEach(function(el) {
                        katex.render(el.textContent, el, {displayMode: true});
                    });
                });
            """)
        ),
        html_body
    )

    return html_doc

entities = get_entities_from_markdown_file("README.md")
html_doc = convert_entities_to_html(entities)
print(html_doc.render())