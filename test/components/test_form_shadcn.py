from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from xue import HTML, Head, Body, Div, xue_initialize
from xue.components import form

xue_initialize(tailwind=True)
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    result = HTML(
        Head(
            title="Form Example"
        ),
        Body(
            Div(
                form.Form(
                    form.FormField(
                        "Username",
                        "username",
                        placeholder="Enter your username",
                        description="This is your public display name.",
                        required=True
                    ),
                    form.FormField(
                        "Email",
                        "email",
                        type="email",
                        placeholder="Enter your email",
                        required=True
                    ),
                    form.FormField(
                        "Password",
                        "password",
                        type="password",
                        placeholder="Enter your password",
                        required=True
                    ),
                    form.FormButton("Submit"),
                    class_="space-y-4"
                ),
                class_="container mx-auto p-4 max-w-md"
            )
        )
    ).render()
    print(result)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)