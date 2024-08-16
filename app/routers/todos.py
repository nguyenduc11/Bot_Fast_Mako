from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from bson import ObjectId
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def get_todos(request: Request):
    try:
        todos = await request.app.mongodb.todos.find().to_list(length=100)
        print(f'todos: {todos}')
    except Exception as e:
        print(f"Error fetching todos: {e}")
        todos = []

    template = request.state.templates.get_template("todos.html")
    return template.render(request=request, todos=todos)


@router.post("/add", response_class=HTMLResponse)
async def add_todo(request: Request, newTodo: str = Form(...)):
    try:
        await request.app.mongodb.todos.insert_one({"title": newTodo})
        return RedirectResponse(url=request.url_for("get_todos"), status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Error adding todo: {e}")
        raise HTTPException(status_code=500, detail="Error adding todo item")


@router.post("/delete/{todo_id}", response_class=HTMLResponse)
async def delete_todo(request: Request, todo_id: str):
    try:
        print(f"todo_id: {todo_id}")
        # Convert the todo_id to an ObjectId
        result = await request.app.mongodb.todos.delete_one({"_id": ObjectId(todo_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Todo not found")
        return RedirectResponse(url=request.url_for("get_todos"), status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Error deleting todo: {e}")
        raise HTTPException(status_code=500, detail="Error deleting todo item")
