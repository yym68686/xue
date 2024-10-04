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
class Ol(HTMLTag): pass
class Li(HTMLTag): pass
class Div(HTMLTag): pass
class Span(HTMLTag): pass
class P(HTMLTag): pass