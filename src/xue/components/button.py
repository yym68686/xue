from ..core import Button

def render(text, **kwargs):
    attributes = {
        "class_": "px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
    }

    # 添加所有额外的属性，包括 hx-get 和 hx-target
    attributes.update(kwargs)

    return Button(text, **attributes)