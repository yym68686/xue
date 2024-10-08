from ..core import HTMLTag, Div, Script, Head, Style

class ResizablePanelGroup(HTMLTag):
    def __init__(self, *children, direction="vertical", resizable=True, **attributes):
        super().__init__(*children, **attributes)
        self.direction = direction
        self.resizable = resizable

class ResizablePanel(HTMLTag):
    def __init__(self, *children, default_size=50, **attributes):
        super().__init__(*children, **attributes)
        self.default_size = default_size

class ResizableHandle(HTMLTag):
    pass

Head.add_default_children([
    Style("""
        .resizable-panel-group {
            display: flex;
            flex-direction: column;
            height: 100vh;
            overflow: hidden;
        }
        .resizable-panel {
            overflow: auto;
        }
        .resizable-handle {
            background-color: #e2e8f0;
            height: 4px;
            cursor: row-resize;
        }
        .resizable-handle:hover {
            background-color: #cbd5e0;
        }
        .resizable-handle.disabled {
            cursor: default;
            background-color: #e2e8f0;
        }
        .resizable-handle.disabled:hover {
            background-color: #e2e8f0;
        }
    """, id="resizable-panel-group-style"),
    Script("""
        function initResizable() {
            const handle = document.querySelector('.resizable-handle');
            const header = document.querySelector('.header-panel');
            const content = document.querySelector('.content-panel');
            let isResizing = false;

            if (handle.classList.contains('disabled')) return;

            handle.addEventListener('mousedown', (e) => {
                isResizing = true;
                document.addEventListener('mousemove', resize);
                document.addEventListener('mouseup', stopResize);
            });

            function resize(e) {
                if (!isResizing) return;
                const containerHeight = window.innerHeight;
                const newHeaderHeight = e.clientY;
                const headerPercentage = (newHeaderHeight / containerHeight) * 100;
                header.style.height = `${headerPercentage}%`;
                content.style.height = `${100 - headerPercentage}%`;
            }

            function stopResize() {
                isResizing = false;
                document.removeEventListener('mousemove', resize);
            }
        }

        document.addEventListener('DOMContentLoaded', initResizable);
    """, id="resizable-panel-group-script")
])

def resizable_layout(header_content, content_content, resizable=True):
    handle_class = "resizable-handle" if resizable else "resizable-handle disabled"
    return ResizablePanelGroup(
        ResizablePanel(
            Div(header_content, class_="flex h-full items-center justify-center p-6"),
            class_="header-panel resizable-panel",
            default_size=25
        ),
        ResizableHandle(class_=handle_class),
        ResizablePanel(
            Div(content_content, class_="flex h-full items-center justify-center p-6"),
            class_="content-panel resizable-panel",
            default_size=75
        ),
        class_="resizable-panel-group",
        resizable=resizable
    )