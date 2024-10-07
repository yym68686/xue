from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from xue import HTML, Head, Body, Div, xue_initialize
from xue.components.model_config_row import model_config_row

xue_initialize(tailwind=True)
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    result = HTML(
        Head(
            title="Model Config Row Example"
        ),
        Body(
            Div(
                model_config_row("model1", "GPT-3.5", True, class_="w-1/2"),
                model_config_row("model2", "GPT-4"),
                model_config_row("model3", "DALL-E"),
                class_="container mx-auto p-4 space-y-4"
            )
        )
    ).render()
    print(result)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)