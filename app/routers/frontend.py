from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "front" / "templates"
templates = Jinja2Templates(directory=TEMPLATES_DIR)

router = APIRouter(include_in_schema=False)


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/companies/new", response_class=HTMLResponse)
def company_new_page(request: Request):
    return templates.TemplateResponse("company_new.html", {"request": request})


@router.get("/jobs/new", response_class=HTMLResponse)
def job_new_page(request: Request):
    return templates.TemplateResponse("job_new.html", {"request": request})


@router.get("/my-applications", response_class=HTMLResponse)
def my_applications_page(request: Request):
    return templates.TemplateResponse("my_applications.html", {"request": request})


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
