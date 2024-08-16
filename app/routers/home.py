from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    try:
        todos = await request.app.mongodb.todos.find().to_list(length=100)
        print(f'todos: {todos}')
    except Exception as e:
        print(f"Error fetching todos: {e}")
        todos = []

    template = request.state.templates.get_template("home.html")
    return template.render(request=request, todos=todos)
