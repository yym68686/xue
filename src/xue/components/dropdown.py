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
    Style("""
        .dropdown-menu,
        .dropdown-trigger {
            border: 1px solid #e5e7eb;
        }
        .dropdown-menu {
            background-color: white;
            color: #374151;
            position: absolute;
            z-index: 1000;
            padding: 0.25rem;
        }
        .dropdown-item {
            display: flex;
            align-items: center;
            gap: 0.5rem; /* 统一图标和文本之间的间距 */
            color: #374151;
            border-radius: 0.25rem;
            transition: background-color 0.2s ease;
            padding: 0.5rem 0.75rem;
            font-size: 0.875rem;
            width: 100%;
        }
        .dropdown-item .icon-container {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 1rem;  /* 固定图标大小 */
            height: 1rem; /* 固定图标大小 */
            flex-shrink: 0; /* 防止图标被压缩 */
        }
        .dropdown-item .icon-container svg {
            width: 100%;
            height: 100%;
            max-width: 100%;
            max-height: 100%;
        }
        .dropdown-item:hover {
            background-color: #f3f4f6;
        }
        .dropdown-separator {
            background-color: #e5e7eb;
        }
        @media (prefers-color-scheme: dark) {
            .dropdown-menu,
            .dropdown-trigger {
                border-color: #4b5563;
            }
            .dropdown-menu {
                background-color: #1f2937;
                color: #e5e7eb;
            }
            .dropdown-item {
                color: #e5e7eb;
            }
            .dropdown-item:hover {
                background-color: #374151;
            }
            .dropdown-separator {
                background-color: #4b5563;
            }
        }
    """, id="dropdown-style"),
    # 点击其他地方关闭下拉菜单
    Script("""
        let activeDropdown = null;

        function toggleDropdown(dropdownId, event) {
            const dropdown = document.getElementById(dropdownId + '-content');
            const isCurrentlyActive = dropdown.classList.contains('opacity-100');

            // 关闭之前打开的下拉菜单
            if (activeDropdown && activeDropdown !== dropdown) {
                closeDropdown(activeDropdown);
            }

            if (isCurrentlyActive) {
                closeDropdown(dropdown);
            } else {
                openDropdown(dropdown);
            }

            activeDropdown = isCurrentlyActive ? null : dropdown;
            event.stopPropagation();
        }

        function openDropdown(dropdown) {
            dropdown.classList.remove('opacity-0', 'scale-95', 'pointer-events-none');
            dropdown.classList.add('opacity-100', 'scale-100', 'pointer-events-auto');
        }

        function closeDropdown(dropdown) {
            dropdown.classList.remove('opacity-100', 'scale-100', 'pointer-events-auto');
            dropdown.classList.add('opacity-0', 'scale-95', 'pointer-events-none');
        }

        document.addEventListener('click', function(event) {
            if (activeDropdown && !activeDropdown.contains(event.target) && !event.target.closest('[id$="-trigger"]')) {
                closeDropdown(activeDropdown);
                activeDropdown = null;
            }
        });

        htmx.on('htmx:afterSwap', function(event) {
            if (event.detail.target.id.endsWith('-content')) {
                openDropdown(event.detail.target);
                activeDropdown = event.detail.target;
            }
        });

        htmx.on('htmx:beforeRequest', function(event) {
            if (event.detail.elt.closest('.dropdown-item')) {
                if (activeDropdown) {
                    closeDropdown(activeDropdown);
                    activeDropdown = null;
                }
            }
        });
    """, id="dropdown-script"),
    # # 添加样式
    Style("""
        .icon-container svg {
            width: 100%;
            height: 100%;
            max-width: 100%; /* 添加这行 */
            max-height: 100%; /* 添加这行 */
        }
    """, id="icon-container-style"),
    # Style("""
    #     .icon-container svg {
    #         display: inline-block;
    #         vertical-align: middle;
    #     }
    # """, id="icon-container-style"),
])

def dropdown_menu(label, **kwargs):
    if kwargs.get("id"):
        value = kwargs.get("id")
    else:
        value = label
    menu_id = f"dropdown-menu-{value.lower().replace(' ', '-')}"
    get_mode = f"/dropdown-menu/{menu_id}"
    if kwargs.get('hx_get'):
        get_mode = kwargs['hx_get']
    return Div(
        Button(
            label,
            id=f"{menu_id}-trigger",
            class_="px-4 py-2 bg-white dark:bg-gray-800 rounded-md shadow-sm hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none dropdown-trigger",
            onclick=f"toggleDropdown('{menu_id}', event)",  # 修改这里
            hx_get=get_mode,
            hx_target=f"#{menu_id}-content",
            hx_swap="innerHTML",
            hx_trigger="click once",
        ),
        Div(
            id=f"{menu_id}-content",
            class_="absolute mt-2 rounded-md shadow-lg bg-white dark:bg-gray-800 ring-1 ring-black ring-opacity-5 focus:outline-none dropdown-menu transition-all duration-300 ease-in-out opacity-0 scale-95 pointer-events-none",
        ),
        class_="relative inline-block text-left"
    )

def get_lucide_icon_url(icon_name):
    return f"https://unpkg.com/lucide-static@latest/icons/{icon_name}.svg"

def dropdown_menu_content(menu_id, items):
    menu_items = []
    max_label_length = max(len(item['label']) for item in items if isinstance(item, dict) and 'label' in item)
    max_shortcut_length = max(len(item.get('shortcut', '')) for item in items if isinstance(item, dict))
    for item in items:
        if item == "separator":
            menu_items.append(Li(Div(class_="my-1 h-px bg-gray-200 dark:bg-gray-600 dropdown-separator")))
        elif isinstance(item, dict):
            icon = LazyIcon(item['icon'], item['label']) if 'icon' in item else ""
            if item.get('disabled'):
                menu_items.append(Li(
                    Div(
                        icon,
                        Span(item['label'], class_="flex-grow"),
                        Span(item.get('shortcut', ''), class_="ml-auto text-xs text-gray-400 dark:text-gray-500 opacity-50"),
                        class_="dropdown-item opacity-50 cursor-not-allowed"
                    )
                ))
            else:
                # 创建一个属性字典，包含所有的 HTMX 属性
                attrs = {
                    'class_': "dropdown-item",
                    'href': item.get('href', '#')
                }

                for key, value in item.items():
                    if key.startswith('hx-'):
                        attrs[key.replace('-', '_')] = value

                menu_items.append(Li(
                    A(
                        icon,
                        Span(item['label'], class_="flex-grow"),
                        Span(
                            item.get('shortcut', ''),
                            class_="ml-auto text-xs text-gray-400 dark:text-gray-500"
                        ) if item.get('shortcut') else None,
                        **attrs
                    )
                ))

    return Ul(*menu_items, class_="py-1 min-w-[220px]")

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