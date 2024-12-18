from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from xue import HTML, Head, Body, Div, xue_initialize
from xue.components import sidebar

app = FastAPI()
xue_initialize(tailwind=True)

sidebar_items = [
    {
        "icon": "layout-dashboard",
        "label": "Dashboard",
        "value": "dashboard",
        "hx": {"get": "/dashboard", "target": "#main-content"}
    },
    {
        "icon": "settings",
        "label": "Settings",
        "value": "settings",
        "hx": {"get": "/settings", "target": "#main-content"}
    },
    {
        "icon": "database",
        "label": "Data",
        "value": "data",
        "hx": {"get": "/data", "target": "#main-content"}
    },
    {
        "icon": "scroll-text",
        "label": "Logs",
        "value": "logs",
        "hx": {"get": "/logs", "target": "#main-content"}
    }
]
# sidebar_items = [
#     {
#         "label": "Overview",
#         "items": [
#             {
#                 "icon": "layout-dashboard",
#                 "label": "Dashboard",
#                 "value": "dashboard",
#                 "hx": {"get": "/dashboard", "target": "#main-content"}
#             },
#             {
#                 "icon": "settings",
#                 "label": "Settings",
#                 "value": "settings",
#                 "hx": {"get": "/settings", "target": "#main-content"}
#             }
#         ]
#     },
#     {
#         "label": "Management",
#         "items": [
#             {
#                 "icon": "database",
#                 "label": "Data",
#                 "value": "data",
#                 "hx": {"get": "/data", "target": "#main-content"}
#             },
#             {
#                 "icon": "scroll-text",
#                 "label": "Logs",
#                 "value": "logs",
#                 "hx": {"get": "/logs", "target": "#main-content"}
#             }
#         ]
#     }
# ]

@app.get("/sidebar/toggle", response_class=HTMLResponse)
async def toggle_sidebar(is_collapsed: bool = False):
    # 返回相反的折叠状态
    return sidebar.Sidebar(
        "zap",
        "Xue Admin",
        sidebar_items,
        is_collapsed=not is_collapsed,  # 切换状态
        active_item="dashboard"
    ).render()

# 同时修改主内容区域的样式，使其随着侧边栏的状态变化而调整
@app.get("/", response_class=HTMLResponse)
async def root():
    result = HTML(
        Head(title="Sidebar Example"),
        Body(
            Div(
                sidebar.Sidebar("zap", "Xue Admin", sidebar_items, is_collapsed=False, active_item="dashboard"),
                Div(
                    "Welcome to Dashboard",
                    id="main-content",
                    # 使用 ml-[240px] 和 ml-16 来精确控制边距
                    class_="ml-[240px] p-6 transition-[margin] duration-200 ease-in-out"
                ),
                class_="flex"
            )
        )
    ).render()
    print(result)
    return result

@app.get("/data", response_class=HTMLResponse)
async def data_page():
    return Div(
        "数据库已禁用",
        id="main-content",
        class_="ml-[240px] p-6 transition-[margin] duration-200 ease-in-out"
    ).render()

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page():
    return Div(
        "Welcome to Dashboard",
        id="main-content",
        class_="ml-[240px] p-6 transition-[margin] duration-200 ease-in-out"
    ).render()

@app.get("/sidebar/update/{active_item}", response_class=HTMLResponse)
async def update_sidebar(active_item: str):
    return sidebar.Sidebar(
        "zap",
        "Xue Admin",
        sidebar_items,
        is_collapsed=False,
        active_item=active_item
    ).render()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)