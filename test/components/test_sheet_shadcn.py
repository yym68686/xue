from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from xue import HTML, Head, Body, Div, xue_initialize, Label
from xue.components.sheet import Sheet, SheetContent, SheetHeader, SheetTitle, SheetDescription, SheetBody, SheetFooter, SheetClose
from xue.components.button import button
from xue.components.input import input

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
                Div(
                    Label("Name", for_="name", class_="text-sm font-medium"),
                    input(id="name", value="Pedro Duarte", class_="mt-1"),
                    class_="mb-4"
                ),
                Div(
                    Label("Username", for_="username", class_="text-sm font-medium"),
                    input(id="username", value="@peduarte", class_="mt-1"),
                    class_="mb-4"
                ),
            )
        ),
        SheetFooter(
            SheetClose("Save changes", "edit-profile-sheet", class_="px-4 py-2 bg-black text-white rounded hover:bg-gray-800")
        )
    )

    result = HTML(
        Head(title="Sheet Example"),
        Body(
            Div(
                Sheet("edit-profile-sheet",
                      button("Open Default Sheet", variant="secondary"),
                      sheet_content
                ),
                Sheet("wide-sheet",
                      button("Open Wide Sheet", variant="secondary"),
                      sheet_content,
                      width="80%",
                      max_width="800px"
                ),
                Sheet("narrow-sheet",
                      button("Open Narrow Sheet", variant="secondary"),
                      sheet_content,
                      width="300px"
                ),
                class_="container mx-auto p-4 space-y-4"
            )
        )
    ).render()
    print(result)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)