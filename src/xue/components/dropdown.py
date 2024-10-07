from ..core import Div, Button, A, Ul, Li, Span, Head, Image, Raw, LazyIcon, Script, Style
def render(text, **kwargs):
    button_attributes = {
       "class_": "px-4 py-2 bg-gray-200 rounded",
    }

    # 添加所有额外的属性，包括 hx-get 和 hx-target
    button_attributes.update(kwargs)
    return Div(
        Button(
            text,
            hx_target="#dropdown-menu",
            hx_swap="innerHTML",
            **button_attributes,
        ),
        Div(
            id="dropdown-menu",
            class_="absolute mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 hidden"
        ),
        class_="relative"
    )

Head.add_default_children([
    # 点击其他地方关闭下拉菜单
    Script("""
        document.addEventListener('click', function(event) {
            var dropdowns = document.querySelectorAll('[id$="-content"]');
            var triggers = document.querySelectorAll('[id$="-trigger"]');

            dropdowns.forEach(function(dropdown) {
                if (!dropdown.contains(event.target) && !event.target.closest('[id$="-trigger"]')) {
                    dropdown.classList.remove('opacity-100', 'scale-100', 'pointer-events-auto');
                    dropdown.classList.add('opacity-0', 'scale-95', 'pointer-events-none');
                }
            });

            if (event.target.closest('[id$="-trigger"]')) {
                var triggerId = event.target.closest('[id$="-trigger"]').id;
                var dropdownId = triggerId.replace('-trigger', '-content');
                var dropdown = document.getElementById(dropdownId);

                if (dropdown.classList.contains('opacity-0')) {
                    dropdown.classList.remove('opacity-0', 'scale-95', 'pointer-events-none');
                    dropdown.classList.add('opacity-100', 'scale-100', 'pointer-events-auto');
                } else {
                    dropdown.classList.remove('opacity-100', 'scale-100', 'pointer-events-auto');
                    dropdown.classList.add('opacity-0', 'scale-95', 'pointer-events-none');
                }
            }
        });

        htmx.on('htmx:afterSwap', function(event) {
            if (event.detail.target.id.endsWith('-content')) {
                setTimeout(function() {
                    event.detail.target.classList.remove('opacity-0', 'scale-95', 'pointer-events-none');
                    event.detail.target.classList.add('opacity-100', 'scale-100', 'pointer-events-auto');
                }, 0);
            }
        });
    """, id="dropdown-menu-script"),
    # 加载懒加载的图标
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
    # 在 htmx:afterSettle 事件后调用 loadSVGContent
    Script("""
        htmx.on('htmx:afterSettle', function(event) {
            loadSVGContent();
        });
    """, id="load-svg-script-htmx"),
    # 添加样式
    Style("""
        .icon-container svg {
            display: inline-block;
            vertical-align: middle;
        }
    """, id="icon-container-style"),
])

def dropdown_menu(label):
    menu_id = f"dropdown-menu-{label.lower().replace(' ', '-')}"
    return Div(
        Button(
            label,
            id=f"{menu_id}-trigger",
            class_="px-4 py-2 bg-white border rounded-md shadow-sm hover:bg-gray-50 focus:outline-none",
            hx_get=f"/dropdown-menu/{menu_id}",
            hx_target=f"#{menu_id}-content",
            hx_swap="innerHTML",
            hx_trigger="click",
        ),
        Div(
            id=f"{menu_id}-content",
            class_="absolute mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none transition-all duration-300 ease-in-out opacity-0 scale-95 pointer-events-none",
        ),
        class_="relative inline-block text-left"
    )

def get_lucide_icon_url(icon_name):
    return f"https://unpkg.com/lucide-static@latest/icons/{icon_name}.svg"

def dropdown_menu_content(menu_id, items):
    menu_items = []
    for item in items:
        if item == "separator":
            menu_items.append(Li(Div(class_="my-1 h-px bg-gray-200")))
        elif isinstance(item, dict):
            icon = LazyIcon(item['icon'], item['label']) if 'icon' in item else ""
            if item.get('disabled'):
                menu_items.append(Li(
                    Div(
                        icon,
                        Span(item['label'], class_="opacity-50"),
                        Span(item.get('shortcut', ''), class_="ml-auto text-xs text-gray-400 opacity-50"),
                        class_="flex items-center px-4 py-2 text-sm text-gray-500 cursor-not-allowed"
                    )
                ))
            else:
                menu_items.append(Li(
                    A(
                        icon,
                        Span(item['label']),
                        Span(item.get('shortcut', ''), class_="ml-auto text-xs text-gray-400"),
                        href=item.get('href', '#'),
                        class_="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900 transition-colors duration-150 ease-in-out"
                    )
                ))

    return Ul(*menu_items, class_="py-1")


Head.add_default_children([Script("""
    document.body.addEventListener('click', function(event) {
        var dropdowns = document.querySelectorAll('[id$="-content"]');
        dropdowns.forEach(function(dropdown) {
            if (!dropdown.contains(event.target) && !event.target.closest('[id$="-trigger"]')) {
                dropdown.classList.remove('opacity-100', 'scale-100');
                dropdown.classList.add('opacity-0', 'scale-95');
            }
        });
    });
""", id="dropdown-script")])

def dropdown(label, id):
    return Div(
        Button(
            Span(label),
            Span("▼", class_="ml-2"),
            id=f"{id}-trigger",
            class_="group flex items-center px-4 py-2 bg-white border rounded-md shadow-sm hover:bg-gray-50",
            hx_get=f"/dropdown/{id}",
            hx_target=f"#{id}-content",
            hx_swap="outerHTML",
        ),
        Div(
            id=f"{id}-content",
            class_="absolute mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none hidden",
        ),
        class_="relative inline-block text-left"
    )

def dropdown_content(items, id, visible=False):
    visibility_class = "opacity-0 scale-95" if not visible else "opacity-100 scale-100"
    return Div(
        Ul(
            *[Li(
                Button(
                    item,
                    class_="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
                )
            ) for item in items],
            class_="py-1",
            role="menu",
            aria_orientation="vertical",
            aria_labelledby="options-menu"
        ),
        id=f"{id}-content",
        class_=f"absolute mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none transform transition-all duration-200 ease-in-out {visibility_class}"
    )

def custom_dropdown(label, items, id, button_class="", menu_class=""):
    default_button_class = "flex items-center px-4 py-2 bg-white border rounded-md shadow-sm hover:bg-gray-50"
    default_menu_class = "absolute mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none hidden"

    return dropdown(label, items, id,
                    button_class=f"{default_button_class} {button_class}",
                    menu_class=f"{default_menu_class} {menu_class}")