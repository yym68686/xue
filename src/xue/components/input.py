from ..core import Div, Input as CoreInput, Style, Head, Script

Head.add_default_children([
    Style("""
        .input-component {
            transition: all 0.2s ease-in-out;
        }
        .input-component:focus-visible {
            outline: none;
            border-color: #000000;
            box-shadow: 0 0 0 1px #000000;
        }
        .dark .input-component:focus-visible {
            border-color: #ffffff;
            box-shadow: 0 0 0 1px #ffffff;
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
    default_class = """
        flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm
        ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium
        placeholder:text-muted-foreground disabled:cursor-not-allowed disabled:opacity-50
        transition-colors duration-200
        dark:bg-gray-800 dark:text-white dark:border-gray-600
        dark:placeholder-gray-400
    """
    combined_class = f"input-component {default_class} {class_}"

    return Div(
        CoreInput(
            type=type,
            placeholder=placeholder,
            id=id,
            class_=combined_class,
            **kwargs
        ),
        class_="relative"
    )