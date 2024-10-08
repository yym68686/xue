from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from xue import HTML, Head, Body, Div, xue_initialize, Label
from xue.components.sheet import Sheet, SheetContent, SheetHeader, SheetTitle, SheetDescription, SheetBody, SheetFooter, SheetClose
from xue.components import button
from xue.components.input import input
from xue.components import form
from xue.components.model_config_row import model_config_row
from xue.components import checkbox

xue_initialize(tailwind=True)
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    sheet_content = SheetContent(
        SheetHeader(
            SheetTitle("Edit profile"),
            SheetDescription("Make changes to your profile here. Click save when you're done.")
        ),
        SheetBody(
            Div(
                form.Form(
                    form.FormField("Provider", "provider", placeholder="Enter provider name", required=True),
                    form.FormField("Base URL", "base_url", placeholder="Enter base URL", required=True),
                    form.FormField("API Key", "api_key", type="password", placeholder="Enter API key"),
                    Div(
                        Div("Models", class_="text-lg font-semibold mb-2"),
                        Div(
                            model_config_row("model1", "gpt-4o: deepbricks-gpt-4o-mini", True),
                            model_config_row("model2", "gpt-4o"),
                            model_config_row("model3", "gpt-3.5-turbo"),
                            model_config_row("model4", "claude-3-5-sonnet-20240620: claude-3-5-sonnet"),
                            model_config_row("model5", "o1-mini-all"),
                            model_config_row("model6", "o1-preview-all"),
                            model_config_row("model7", "whisper-1"),
                            id="models-container"
                        ),
                        button.button(
                            "Add Model",
                            class_="mt-2",
                            hx_post="/add-model",
                            hx_target="#models-container",
                            hx_swap="beforeend"
                        ),
                        class_="mb-4"
                    ),
                    Div(
                        checkbox.checkbox("tools", "Enable Tools", checked=True),
                        class_="mb-4"
                    ),
                    form.FormField("Notes", "notes", placeholder="Enter any additional notes"),
                    Div(
                        button.button("Submit", class_="bg-blue-500 text-white"),
                        button.button("Cancel", class_="bg-gray-300 text-gray-700 ml-2"),
                        class_="flex justify-end mt-4"
                    ),
                    hx_post="/submit",
                    hx_swap="outerHTML",
                    class_="space-y-4"
                ),
                class_="container mx-auto p-4 max-w-2xl"
            )
        ),
        # SheetFooter(
        #     SheetClose("Save changes", "edit-profile-sheet", type="submit")
        # )
    )

    result = HTML(
        Head(title="Sheet Example"),
        Body(
            Div(
                Sheet("edit-profile-sheet",
                      button.button("Open", variant="secondary"),
                      sheet_content,
                      width="80%",
                      max_width="800px"
                ),
                class_="container mx-auto p-4"
            )
        )
    ).render()
    print(result)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)