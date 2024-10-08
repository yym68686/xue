from ..core import Div, Button, Ul, Li, Span, Head, Script, Style

Head.add_default_children([
    Style("""
        .menubar {
            display: inline-flex;
            background-color: white;
            border-radius: 0.5rem;
            border: 1px solid #e2e8f0;
            padding: 0.25rem;
        }
        .menubar-menu {
            position: relative;
        }
        .menubar-trigger {
            padding: 0.5rem 0.75rem;
            font-size: 0.875rem;
            font-weight: 500;
            color: #374151;
            background-color: transparent;
            border: none;
            border-radius: 0.25rem;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        .menubar-trigger:focus {
            outline: none;
        }
        .menubar-menu.active .menubar-trigger {
            background-color: #f3f4f6;
        }
        .menubar-content {
            position: absolute;
            top: 100%;
            left: 0;
            min-width: 12rem;
            padding: 0.5rem;
            margin-top: 0.5rem;
            background-color: white;
            border: 1px solid #e2e8f0;
            border-radius: 0.375rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            z-index: 50;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.2s, visibility 0.2s;
        }
        .menubar-menu.active .menubar-content {
            opacity: 1;
            visibility: visible;
        }
        .menubar-item {
            display: flex;
            align-items: center;
            padding: 0.5rem 0.75rem;
            font-size: 0.875rem;
            color: #374151;
            border-radius: 0.25rem;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        .menubar-item:hover {
            background-color: #f3f4f6;
        }
        .menubar-item.disabled {
            color: #9ca3af;
            cursor: not-allowed;
        }
        .menubar-separator {
            height: 1px;
            margin: 0.5rem 0;
            background-color: #e2e8f0;
        }
        .menubar-shortcut {
            margin-left: auto;
            font-size: 0.75rem;
            color: #6b7280;
        }
        @media (prefers-color-scheme: dark) {
            .menubar {
                background-color: #1f2937;
                border-color: #374151;
            }
            .menubar-trigger {
                color: #e5e7eb;
            }
            .menubar-menu.active .menubar-trigger {
                background-color: #374151;
            }
            .menubar-content {
                background-color: #1f2937;
                border-color: #374151;
            }
            .menubar-item {
                color: #e5e7eb;
            }
            .menubar-item:hover {
                background-color: #374151;
            }
            .menubar-item.disabled {
                color: #6b7280;
            }
            .menubar-separator {
                background-color: #374151;
            }
            .menubar-shortcut {
                color: #9ca3af;
            }
        }
    """, id="menubar-style"),
    Script("""
        let activeMenu = null;

        function closeAllMenus() {
            document.querySelectorAll('.menubar-menu').forEach(menu => {
                menu.classList.remove('active');
            });
        }

        function toggleMenu(menuId, event) {
            event.stopPropagation();
            const menu = document.getElementById(menuId);
            if (activeMenu && activeMenu !== menu) {
                activeMenu.classList.remove('active');
            }
            menu.classList.toggle('active');
            activeMenu = menu.classList.contains('active') ? menu : null;
        }

        document.addEventListener('click', function(event) {
            if (!event.target.closest('.menubar')) {
                closeAllMenus();
            }
        });

        document.addEventListener('DOMContentLoaded', function() {
            const menubar = document.querySelector('.menubar');
            menubar.addEventListener('mouseover', function(event) {
                const menuTrigger = event.target.closest('.menubar-trigger');
                if (menuTrigger && activeMenu) {
                    const menuId = menuTrigger.getAttribute('data-menu-id');
                    closeAllMenus();
                    toggleMenu(menuId, event);
                }
            });
        });
    """, id="menubar-script")
])

def Menubar(*children, **kwargs):
    return Div(*children, class_="menubar", **kwargs)

def MenubarMenu(*children, id, **kwargs):
    return Div(*children, id=id, class_="menubar-menu", **kwargs)

def MenubarTrigger(text, menu_id, **kwargs):
    return Button(text, class_="menubar-trigger", onclick=f"toggleMenu('{menu_id}', event)", data_menu_id=menu_id, **kwargs)

def MenubarContent(*children, **kwargs):
    return Ul(*children, class_="menubar-content", **kwargs)

def MenubarItem(text, shortcut=None, disabled=False, **kwargs):
    class_ = "menubar-item"
    if disabled:
        class_ += " disabled"

    content = [text]
    if shortcut:
        content.append(Span(shortcut, class_="menubar-shortcut"))

    return Li(*content, class_=class_, **kwargs)

def MenubarSeparator(**kwargs):
    return Li(class_="menubar-separator", **kwargs)