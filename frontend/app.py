from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

STATIC_DIR = Path(__file__).parent / "static"

LOGIN_PAGE = STATIC_DIR / "pages" / "login.html"
HOME_PAGE = STATIC_DIR / "pages" / "home.html"

app = FastAPI()

if not LOGIN_PAGE.exists():
    raise RuntimeError("Login page not found. Check the frontend build output.")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="frontend-static")


@app.get("/", include_in_schema=False)
async def root() -> FileResponse:
    """Serve the login page at the frontend root."""
    return FileResponse(LOGIN_PAGE)


@app.get("/home", include_in_schema=False)
async def homepage() -> FileResponse:
    """Serve the placeholder home page after successful login."""
    if HOME_PAGE.exists():
        return FileResponse(HOME_PAGE)
    return RedirectResponse(url="/")
