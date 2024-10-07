from ..core import Div, Input, Label, Script, Head, Style

Head.add_default_children([
    Style("""
        .checkbox-component {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .checkbox-input {
            appearance: none;
            width: 1rem;
            height: 1rem;
            border: 1px solid #d1d5db;
            border-radius: 0.25rem;
            background-color: #fff;
            cursor: pointer;
            transition: all 0.2s ease-in-out;
        }
        .checkbox-input:checked {
            background-color: #3b82f6;
            border-color: #3b82f6;
        }
        .checkbox-input:checked::after {
            content: '✓';
            display: flex;
            justify-content: center;
            align-items: center;
            color: #fff;
            font-size: 0.75rem;
            font-weight: bold;
        }
        .checkbox-input:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .checkbox-label {
            font-size: 0.875rem;
            line-height: 1;
            cursor: pointer;
        }
        .checkbox-label:disabled {
            opacity: 0.7;
            cursor: not-allowed;
        }
    """, id="checkbox-style"),
    Script("""
        document.addEventListener('DOMContentLoaded', function() {
            const checkboxes = document.querySelectorAll('.checkbox-input');
            checkboxes.forEach(checkbox => {
                checkbox.addEventListener('change', function() {
                    this.classList.toggle('checked', this.checked);
                });
            });
        });
    """, id="checkbox-script")
])

def checkbox(id, label, checked=False, disabled=False, **kwargs):

    input_attrs = {
        "type": "checkbox",
        "id": id,
        "class_": "checkbox-input",
    }

    if checked:
        input_attrs["checked"] = "checked"

    if disabled:
        input_attrs["disabled"] = "disabled"

    input_attrs.update(kwargs)

    label_attrs = {
        "for": id,
        "class_": "checkbox-label peer-disabled:cursor-not-allowed peer-disabled:opacity-70",
    }

    return Div(
        Input(**input_attrs),
        Label(label, **label_attrs),
        class_="checkbox-component"
    )