from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def about(request: Request):
    template = request.state.templates.get_template("about.html")
    return template.render(request=request)
