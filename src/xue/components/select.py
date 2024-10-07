from ..core import Div, Button, Ul, Li, Span, Head, Script, Style

Head.add_default_children([
    Script("""
        document.addEventListener('click', function(event) {
            var selects = document.querySelectorAll('[id$="-content"]');
            selects.forEach(function(select) {
                if (!select.contains(event.target) && !event.target.closest('[id$="-trigger"]')) {
                    select.classList.remove('opacity-100', 'scale-100', 'pointer-events-auto');
                    select.classList.add('opacity-0', 'scale-95', 'pointer-events-none');
                }
            });
        });

        htmx.on('htmx:afterSwap', function(event) {
            if (event.detail.target.id.endsWith('-content')) {
                setTimeout(function() {
                    event.detail.target.classList.remove('opacity-0', 'scale-95', 'pointer-events-none');
                    event.detail.target.classList.add('opacity-100', 'scale-100', 'pointer-events-auto');
                }, 0);
            }
        });

        function updateSelectValue(selectId, value, label) {
            var trigger = document.getElementById(selectId + '-trigger');
            trigger.querySelector('.select-value').textContent = label;
            trigger.setAttribute('data-value', value);
        }
    """, id="select-script"),
    Style("""
        .select-content {
            transition: all 0.2s ease-in-out;
        }
    """, id="select-style")
])

def select(placeholder, options, id):
    return Div(
        Button(
            Span(placeholder, class_="select-value"),
            Span("▼", class_="ml-2"),
            id=f"{id}-trigger",
            class_="flex items-center justify-between w-[180px] px-3 py-2 text-sm bg-white border rounded-md shadow-sm hover:bg-gray-50 focus:outline-none",
            hx_get=f"/select/{id}",
            hx_target=f"#{id}-content",
            hx_swap="innerHTML",
            hx_trigger="click",
        ),
        Div(
            id=f"{id}-content",
            class_="absolute mt-1 w-[180px] rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none select-content transition-all duration-200 ease-in-out opacity-0 scale-95 pointer-events-none",
        ),
        class_="relative inline-block text-left"
    )

def select_content(id, options, group_label=None):
    items = []
    if group_label:
        items.append(Li(Span(group_label, class_="px-3 py-1 text-sm font-semibold text-gray-900")))
    for option in options:
        items.append(
            Li(
                Button(
                    option['label'],
                    class_="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900",
                    hx_post=f"/select/{id}/{option['value']}",
                    hx_target=f"#{id}-trigger",
                    hx_swap="outerHTML",
                )
            )
        )
    return Ul(*items, class_="py-1 max-h-60 overflow-auto")