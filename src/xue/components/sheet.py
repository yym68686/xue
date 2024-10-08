from ..core import Div, Button, Script, Head, Style, Raw

Head.add_default_children([
    Style("""
        .sheet-overlay {
            position: fixed;
            inset: 0;
            background-color: rgba(0, 0, 0, 0.4);
            opacity: 0;
            transition: opacity 0.3s ease;
            z-index: 50;
            display: none;
        }
        .sheet-overlay.open {
            opacity: 1;
        }
        .sheet-content {
            position: fixed;
            top: 0;
            bottom: 0;
            right: -100%;
            width: var(--sheet-width, 100%);
            max-width: var(--sheet-max-width, 400px);
            background-color: white;
            box-shadow: -4px 0 8px rgba(0, 0, 0, 0.1);
            transition: right 0.3s ease;
            z-index: 51;
            display: flex;
            flex-direction: column;
        }
        .sheet-content.open {
            right: 0;
        }
        .sheet-header {
            padding: 1.5rem;
        }
        .sheet-title {
            font-size: 1.125rem;
            font-weight: 600;
            line-height: 1;
            margin-bottom: 0.25rem;
        }
        .sheet-description {
            color: #6b7280;
            font-size: 0.875rem;
            line-height: 1.25rem;
        }
        .sheet-body {
            padding: 0 1.5rem;
            flex-grow: 1;
            overflow-y: auto;
        }
        .sheet-footer {
            padding: 1.5rem;
            display: flex;
            justify-content: flex-end;
        }
        @media (prefers-color-scheme: dark) {
            .sheet-content {
                background-color: #1f2937;
                border-left-color: rgba(255, 255, 255, 0.1);
            }
            .sheet-title {
                color: #f3f4f6;
            }
            .sheet-description {
                color: #9ca3af;
            }
        }
    """, id="sheet-style"),
    Script("""
        function toggleSheet(sheetId) {
            const overlay = document.getElementById(sheetId + '-overlay');
            const content = document.getElementById(sheetId + '-content');
            const isOpen = overlay.classList.contains('open');

            if (isOpen) {
                closeSheet(overlay, content);
            } else {
                openSheet(overlay, content);
            }
        }

        function openSheet(overlay, content) {
            overlay.style.display = 'block';
            setTimeout(() => {
                overlay.classList.add('open');
                content.classList.add('open');
            }, 10);
        }

        function closeSheet(overlay, content) {
            overlay.classList.remove('open');
            content.classList.remove('open');
            setTimeout(() => {
                overlay.style.display = 'none';
            }, 300);
        }

        function setupSheetListeners(sheetId) {
            const overlay = document.getElementById(sheetId + '-overlay');
            const content = document.getElementById(sheetId + '-content');
            const closeButtons = content.querySelectorAll('[data-close-sheet]');

            overlay.addEventListener('click', (event) => {
                if (event.target === overlay) {
                    closeSheet(overlay, content);
                }
            });

            closeButtons.forEach(button => {
                button.addEventListener('click', () => closeSheet(overlay, content));
            });
        }

        htmx.on('htmx:afterSettle', function(event) {
            if (event.detail.target.id === 'sheet-container') {
                const sheetContent = event.detail.target.querySelector('[id$="-content"]');
                if (sheetContent) {
                    const sheetId = sheetContent.id.replace('-content', '');
                    setupSheetListeners(sheetId);
                    toggleSheet(sheetId);
                }
            }
        });
    """, id="sheet-script")
])

def Sheet(id, trigger, content, width=None, max_width=None):
    style = ""
    if width:
        style += f"--sheet-width: {width};"
    if max_width:
        style += f"--sheet-max-width: {max_width};"

    return Raw(f"""
        <div>
            <div onclick="toggleSheet('{id}')">{trigger.render()}</div>
            <div id="{id}-overlay" class="sheet-overlay"></div>
            <div id="{id}-content" class="sheet-content" style="{style}">
                {content.render()}
            </div>
        </div>
    """)

def SheetContent(*children, **kwargs):
    return Div(*children, **kwargs)

def SheetHeader(*children, **kwargs):
    return Div(*children, class_="sheet-header", **kwargs)

def SheetTitle(text, **kwargs):
    return Div(text, class_="sheet-title", **kwargs)

def SheetDescription(text, **kwargs):
    return Div(text, class_="sheet-description", **kwargs)

def SheetBody(*children, **kwargs):
    return Div(*children, class_="sheet-body", **kwargs)

def SheetFooter(*children, **kwargs):
    return Div(*children, class_="sheet-footer", **kwargs)

def SheetClose(text, sheet_id, **kwargs):
    kwargs['data-close-sheet'] = 'true'
    return Button(text, **kwargs)