from ..core import Div, Input as CoreInput, Style, Head, Script

# 添加样式和脚本
Head.add_default_children([
    Style("""
        .input-component {
            border: 1px solid #e2e8f0;
        }
        .input-component:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
        }
    """),
    Script("""
        document.addEventListener('DOMContentLoaded', function() {
            const inputs = document.querySelectorAll('.input-component');
            inputs.forEach(input => {
                input.addEventListener('focus', function() {
                    this.classList.add('input-focus');
                });
                input.addEventListener('blur', function() {
                    this.classList.remove('input-focus');
                });
            });
        });
    """, id="input-script")
])

def input(type="text", placeholder="", id="", class_="", **kwargs):
    default_class = "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50 transition-all duration-200 ease-in-out"
    combined_class = f"{default_class} {class_}"

    return Div(
        CoreInput(
            type=type,
            placeholder=placeholder,
            id=id,
            class_=f"input-component {combined_class}",
            **kwargs
        ),
        class_="relative"
    )