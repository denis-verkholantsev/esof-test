from fastapi import Request, APIRouter, WebSocket, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.api.dependencies import (
    OauthClientDependency,
    NumberGeneratorDependency,
    WebSocketManagerDependency,
)


router = APIRouter(prefix="")
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def login(request: Request):
    user = request.session.get("user")
    if user:
        return RedirectResponse(url="/index")
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/login/github")
async def login_via_github(request: Request, oauth: OauthClientDependency):
    redirect_uri = request.url_for("auth_via_github").replace('http', 'https')
    return await oauth.github.authorize_redirect(request, redirect_uri)


@router.get("/index")
async def index(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/")
    return templates.TemplateResponse(
        "index.html", {"request": request, "login": user.get("login", "Гость")}
    )


@router.get("/auth/github")
async def auth_via_github(request: Request, oauth: OauthClientDependency):

    token = await oauth.github.authorize_access_token(request)
    resp = await oauth.github.get("user", token=token)

    user = resp.json()

    if user:
        request.session["user"] = dict(user)
    return RedirectResponse(url="/index")


@router.get("/logout")
async def logout(request: Request, response: Response):
    request.session.clear()
    response = RedirectResponse(url="/")
    return response


@router.websocket("/ws")
async def send_number(
    websocket: WebSocket,
    websocket_manager: WebSocketManagerDependency,
    number_generator: NumberGeneratorDependency,
):
    await websocket_manager.connect(websocket)
    try:
        number = number_generator.get_number()
        await websocket.send_text(str(number))

        while True:
            await websocket.receive_text()

    except Exception as e:
        print(f"Client disconnected: {e}")
    finally:
        websocket_manager.disconnect(websocket)
