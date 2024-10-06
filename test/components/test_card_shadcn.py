from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from xue import HTML, Head, Body, Div, Script, xue_initialize, Style, Button, Form
from xue.components.card import Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter, FormField
from xue.components.dropdown import dropdown_menu, dropdown_menu_content

xue_initialize(tailwind=True)
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    result = HTML(
        Head(),
        Body(
            Div(
                Card(
                    CardHeader(
                        CardTitle("Create project"),
                        CardDescription("Deploy your new project in one-click.")
                    ),
                    CardContent(
                        Form(
                            Div(
                                FormField("Name", id="name", placeholder="Name of your project"),
                                Div(
                                    FormField("Framework", id="framework"),
                                    dropdown_menu("Select Framework"),
                                    class_="relative"
                                ),
                                class_="grid w-full items-center gap-4"
                            )
                        )
                    ),
                    CardFooter(
                        Button("Cancel", class_="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300"),
                        Button("Deploy", class_="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600")
                    ),
                    class_="w-[350px] mx-auto mt-10"
                ),
                class_="container mx-auto p-4"
            )
        )
    ).render()
    print(result)
    return result

@app.get("/dropdown-menu/{menu_id}", response_class=HTMLResponse)
async def get_dropdown_menu_content(menu_id: str):
    items = [
        {"label": "Next.js", "value": "next"},
        {"label": "SvelteKit", "value": "sveltekit"},
        {"label": "Astro", "value": "astro"},
        {"label": "Nuxt.js", "value": "nuxt"},
    ]
    result = dropdown_menu_content(menu_id, items).render()
    print("result", result)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)