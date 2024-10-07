from ..core import Button, Script, Head, Style

Head.add_default_children([
    Style("""
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 0.375rem;
            font-weight: 500;
            font-size: 0.875rem;
            line-height: 1.25rem;
            padding: 0.5rem 1rem;
            transition-property: color, background-color, border-color, text-decoration-color, fill, stroke;
            transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
            transition-duration: 150ms;
        }
        .btn-primary {
            color: #ffffff;
            background-color: #000000;
        }
        .btn-primary:hover {
            background-color: #262626;
        }
        .btn-secondary {
            color: #000000;
            background-color: #ffffff;
            border: 1px solid #e5e7eb;
        }
        .btn-secondary:hover {
            background-color: #f3f4f6;
        }
        .btn:focus-visible {
            outline: 2px solid #000000;
            outline-offset: 2px;
        }
        .btn:disabled {
            opacity: 0.5;
            pointer-events: none;
        }
        @media (prefers-color-scheme: dark) {
            .btn-primary {
                color: #000000;
                background-color: #ffffff;
            }
            .btn-primary:hover {
                background-color: #e5e7eb;
            }
            .btn-secondary {
                color: #ffffff;
                background-color: #1f2937;
                border-color: #4b5563;
            }
            .btn-secondary:hover {
                background-color: #374151;
            }
            .btn:focus-visible {
                outline-color: #ffffff;
            }
        }
    """, id="button-style"),
])

def button(text, variant="primary", **kwargs):
    class_ = f"btn btn-{variant}"
    if "class_" in kwargs:
        class_ += f" {kwargs.pop('class_')}"

    attributes = {
        "class_": class_,
    }
    attributes.update(kwargs)

    return Button(text, **attributes)