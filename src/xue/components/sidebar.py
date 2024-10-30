from ..core import Div, Button, Span, Raw, Style, Head, Image, LazyIcon, Script

Head.add_default_children([
    Style("""
        .sidebar {
            height: 100vh;
            transition: width 0.2s ease-in-out;
            position: fixed;
            left: 0;
            top: 0;
            z-index: 40;
            background-color: white;
            border-right: 1px solid #e5e7eb;
            display: flex;
            flex-direction: column;
        }

        .sidebar-expanded {
            width: 240px;
        }

        .sidebar-collapsed {
            width: 64px;
        }

        .sidebar-content {
            flex: 1;
            overflow-y: auto;
            padding: 0.5rem;
        }

        .sidebar-header {
            padding: 1rem;
            border-bottom: 1px solid #e5e7eb;
            display: flex;
            align-items: center;
        }

        .sidebar-logo-container {
            display: flex;
            align-items: center;
            flex: 1;
            min-width: 0;
        }

        .sidebar-logo {
            font-weight: 500;
            margin-left: 0.75rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            opacity: 1;
            transition: opacity 0.2s ease-in-out;
        }

        .sidebar-collapsed .sidebar-logo {
            opacity: 0;
        }

        .sidebar-item {
            display: flex;
            align-items: center;
            padding: 0.75rem 1rem;
            color: #4b5563;
            transition: all 0.2s ease;
            border-radius: 0.375rem;
            margin: 0.25rem 0;
            cursor: pointer;
        }

        .sidebar-item:hover {
            background-color: rgba(0, 0, 0, 0.05);
        }

        .sidebar-item.active {
            background-color: rgba(0, 0, 0, 0.1);
            color: #000000;
            font-weight: 500;
        }

        .sidebar-item-label {
            margin-left: 0.75rem;
            font-size: 0.875rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            opacity: 1;
            transition: opacity 0.2s ease-in-out;
        }

        .sidebar-collapsed .sidebar-item-label {
            opacity: 0;
        }

        .sidebar-footer {
            padding: 1rem;
            background: inherit;
            border-top: 1px solid #e5e7eb;
        }

        .toggle-button-expanded,
        .toggle-button-collapsed {
            padding: 0.5rem;
            border-radius: 0.375rem;
            transition: background-color 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            min-width: 28px;
        }

        .toggle-button-expanded:hover,
        .toggle-button-collapsed:hover {
            background-color: rgba(0, 0, 0, 0.05);
        }

        .tooltip {
            position: relative;
        }

        .tooltip .tooltip-text {
            visibility: hidden;
            position: absolute;
            z-index: 100;
            background-color: #1f2937;
            color: white;
            text-align: center;
            padding: 0.5rem;
            border-radius: 0.375rem;
            left: 100%;
            margin-left: 0.75rem;
            font-size: 0.875rem;
            white-space: nowrap;
            opacity: 0;
            transition: opacity 0.2s ease;
        }

        .tooltip:hover .tooltip-text {
            visibility: visible;
            opacity: 1;
        }

        /* Dark mode styles */
        @media (prefers-color-scheme: dark) {
            .sidebar {
                background-color: #1f2937;
                border-right-color: #374151;
            }

            .sidebar-item {
                color: #e5e7eb;
            }

            .sidebar-item:hover {
                background-color: rgba(255, 255, 255, 0.05);
            }

            .sidebar-item.active {
                background-color: rgba(255, 255, 255, 0.1);
                color: #ffffff;
            }

            .sidebar-footer {
                border-top-color: #374151;
            }

            .sidebar-header {
                border-bottom-color: #374151;
            }

            .toggle-button-expanded:hover,
            .toggle-button-collapsed:hover {
                background-color: rgba(255, 255, 255, 0.05);
            }

            .tooltip .tooltip-text {
                background-color: #374151;
                color: #e5e7eb;
            }
        }

        /* Icon container styles */
        .icon-container {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 1em;  /* 添加这行 */
            height: 1em; /* 添加这行 */
        }

        .icon-container svg {
            width: 100%;
            height: 100%;
            max-width: 100%; /* 添加这行 */
            max-height: 100%; /* 添加这行 */
        }

        /* 为不同大小的图标添加特定的尺寸类 */
        .icon-container.icon-sm {
            width: 1rem;
            height: 1rem;
        }

        .icon-container.icon-md {
            width: 1.5rem;
            height: 1.5rem;
        }

        .icon-container.icon-lg {
            width: 2rem;
            height: 2rem;
        }
    """, id="sidebar-style"),
    Script("""
        function initializeSidebarEvents() {
            // 移除现有的事件监听器
            document.removeEventListener('click', handleSidebarClick);
            // 添加新的事件监听器
            document.addEventListener('click', handleSidebarClick);
        }

        function handleSidebarClick(event) {
            const sidebarItem = event.target.closest('.sidebar-item');
            if (sidebarItem) {
                const value = sidebarItem.getAttribute('data-value');
                if (value) {
                    // 更新侧边栏
                    fetch(`/sidebar/update/${value}`)
                        .then(response => response.text())
                        .then(html => {
                            document.getElementById('sidebar').outerHTML = html;
                            // 重新初始化事件监听器
                            initializeSidebarEvents();
                        });

                    // 更新内容区域
                    const url = sidebarItem.getAttribute('data-url');
                    if (url) {
                        fetch(url)
                            .then(response => response.text())
                            .then(html => {
                                document.getElementById('main-content').outerHTML = html;
                            });
                    }
                }
            }
        }

        // 初始化事件监听器
        document.addEventListener('DOMContentLoaded', initializeSidebarEvents);
    """, id="sidebar-script"),
])

def Sidebar(logo_icon, site_name, items, is_collapsed=False, active_item=None):
    def render_menu_items(items):
        menu_items = []
        for item in items:
            if "items" in item:
                menu_items.append(
                    Div(
                        Span(item['label'], class_=f"text-xs font-medium text-gray-500 dark:text-gray-400 px-3 {'hidden' if is_collapsed else ''}"),
                        *[render_single_item(sub_item) for sub_item in item['items']],
                        class_="py-2"
                    )
                )
            else:
                menu_items.append(render_single_item(item))
        return menu_items

    def render_single_item(item):
        return Div(
            LazyIcon(item['icon'], item['label'], class_="w-5 h-5"),
            Span(
                item['label'],
                class_=f"sidebar-item-label {'hidden' if is_collapsed else ''}"
            ),
            Span(
                item['label'],
                class_="tooltip-text" if is_collapsed else "tooltip-text hidden"
            ),
            class_=f"sidebar-item tooltip {' active' if item.get('value') == active_item else ''}",
            data_value=item['value'],
            data_url=item['hx'].get('get', '')  # 将 URL 存储在 data-url 属性中
        )

    def render_toggle_button():
        icon_name = "chevron-left" if not is_collapsed else "chevron-right"
        button_class = (
            "toggle-button-expanded hover:bg-gray-100 dark:hover:bg-gray-700" if not is_collapsed
            else "toggle-button-collapsed hover:bg-gray-100 dark:hover:bg-gray-700"
        )
        return Button(
            LazyIcon(icon_name, "Toggle sidebar", class_="w-4 h-4"),  # 稍微减小图标尺寸
            class_=button_class,
            hx_get=f"/sidebar/toggle?is_collapsed={is_collapsed}",
            hx_target="#sidebar",
            hx_swap="outerHTML"
        )

    if is_collapsed:
        # 折叠状态：展开按钮在底部
        header_content = Div(
            LazyIcon(logo_icon, site_name, class_="w-6 h-6"),
            class_="sidebar-header justify-center"
        )
        footer_content = render_toggle_button()
    else:
        # 展开状态：折叠按钮在标题栏右侧
        header_content = Div(
            Div(
                LazyIcon(logo_icon, site_name, class_="w-6 h-6"),
                Span(site_name, class_="sidebar-logo"),
                class_="sidebar-logo-container"
            ),
            render_toggle_button(),
            class_="sidebar-header"
        )
        footer_content = None

    return Div(
        header_content,
        Div(
            *render_menu_items(items),
            class_="sidebar-content"
        ),
        Div(
            footer_content,
            class_="sidebar-footer" if footer_content else "hidden"
        ),
        id="sidebar",
        class_=f"sidebar {'sidebar-collapsed' if is_collapsed else 'sidebar-expanded'}"
    )