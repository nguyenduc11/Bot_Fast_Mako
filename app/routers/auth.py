from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    template = request.state.templates.get_template("login.html")
    return template.render(request=request)


@router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    # This is a simple example. In a real application, you would validate the credentials
    if username == "admin" and password == "password":
        return RedirectResponse(url="/home", status_code=303)
    else:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
