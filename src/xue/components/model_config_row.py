from ..core import Div, Button, Script, Head, Style, Input
from .checkbox import checkbox
from .input import input
from .button import button

Head.add_default_children([
    Style("""
        .model-config-row {
            display: flex;
            align-items: center;
            padding: 0.5rem;
            border-radius: 0.375rem;
            transition: all 0.3s ease;
        }
        .model-config-row:hover {
            background-color: rgba(0, 0, 0, 0.05);
        }
        .model-config-row .checkbox {
            margin-right: 1rem;
        }
        .model-config-row .text-area {
            flex-grow: 1;
            margin-right: 1rem;
            display: flex;
            align-items: center;
        }
        .model-config-row .buttons {
            display: flex;
            gap: 0.5rem;
        }
        .model-config-row input {
            transition: all 0.2s ease-in-out;
        }
        .model-config-row .rename-input {
            max-width: 0;
            padding: 0;
            margin: 0;
            border: none;
            opacity: 0;
            transition: all 0.3s ease-in-out;
        }
        .model-config-row .rename-input.active {
            max-width: 200px;
            padding: 0.5rem;
            margin-left: 0.5rem;
            border: 1px solid #e2e8f0;
            opacity: 1;
        }
    """, id="model_config_row-style"),
    Script("""
        function toggleRenameInput(id) {
            event.preventDefault();
            const textArea = document.querySelector(`#${id} .text-area`);
            const renameInput = textArea.querySelector('.rename-input');
            renameInput.classList.toggle('active');
            if (renameInput.classList.contains('active')) {
                renameInput.focus();
            }
        }

        function deleteRow(id) {
            event.preventDefault();
            const row = document.getElementById(id);
            row.style.opacity = '0';
            row.style.height = '0';
            row.style.overflow = 'hidden';
            setTimeout(() => row.remove(), 300);
        }
    """, id="model_config_row-script")
])

def model_config_row(id, model_name="", enabled=False, **kwargs):
    attributes = {
        "class_": "model-config-row" + " " + kwargs.get("class_", "")
    }
    if kwargs.get("class_", None):
        kwargs.pop("class_", None)

    # 添加所有额外的属性，包括 hx-get 和 hx-target
    attributes.update(kwargs)

    return Div(
        checkbox(f"{id}-checkbox", "", checked=enabled),
        Div(
            input(type="text", placeholder="Model name", value=model_name),
            input(type="text", placeholder="New name", class_="rename-input"),
            class_="text-area"
        ),
        Div(
            button("Rename", class_="bg-blue-500 text-white", onclick=f"toggleRenameInput('{id}')"),
            button("Delete", class_="bg-red-500 text-white", onclick=f"deleteRow('{id}')"),
            class_="buttons"
        ),
        id=id,
        **attributes
    )