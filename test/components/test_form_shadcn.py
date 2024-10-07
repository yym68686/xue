from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from xue import HTML, Head, Body, Div, xue_initialize, Div, Strong, Span, Ul, Li
from xue.components import form, button

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
                    button.button(
                        "Submit",
                    ),
                    hx_post="/submit",
                    hx_swap="outerHTML",
                    class_="space-y-4"
                ),
                class_="container mx-auto p-4 max-w-md"
            )
        )
    ).render()
    print(result)
    return result

def form_success_message(username, email, password):
    return Div(
        Strong("Success!", class_="font-bold"),
        Span("Form submitted successfully.", class_="block sm:inline"),
        Ul(
            Li(f"Username: {username}"),
            Li(f"Email: {email}"),
            Li(f"Password length: {len(password)}"),
            class_="mt-3"
        ),
        class_="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative",
        role="alert"
    )

@app.post("/submit", response_class=HTMLResponse)
async def submit_form(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    # 这里处理提交的数据
    # 例如，可以打印数据，保存到数据库，或进行验证
    print(f"Received: username={username}, email={email}, password={password}")

    # 返回处理结果
    return form_success_message(username, email, password).render()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)