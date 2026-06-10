from fastapi import FastAPI, Request, status
# asyn error handler
from fastapi.exception_handlers import request_validation_exception_handler, http_exception_handler

# from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# manager
from contextlib import asynccontextmanager

# magic behind handling api and html response
from starlette.exceptions import HTTPException as starletteHttpException
# from fastapi.responses import JSONResponse #
from fastapi.exceptions import RequestValidationError

from database import engine
from Router import users, posts, html_router
  

@asynccontextmanager
async def lifespan(app: FastAPI):
  
  yield

  await engine.dispose()

app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")


app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(posts.router, prefix="/api/posts", tags=["posts"])
app.include_router(html_router.router)



# ERRORS ROUTE ❌❌❌
# Request validation handler: Input raise Error by fastapi

@app.exception_handler(RequestValidationError)
async def custom_RequestValidationError(request: Request, exc: RequestValidationError):

  if request.url.path.startswith("/api"):
    return await request_validation_exception_handler(request, exc)
  
  return templates.TemplateResponse(
    request, "error_page.html", 
    {
      "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
      "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
      "message": "Invalid request, Please check your input and try again."
    },
    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )


# GENERAL FOR BOTH HTTPEXCEPTION AND STARLETTE DEFAULT HANDLER (FOR PAGE NOT NOT)
@app.exception_handler(starletteHttpException)
async def custom_general_httpexception(request: Request, exc: starletteHttpException):

  if request.url.path.startswith("/api"):
    return await http_exception_handler(request, exc)
  
  message = exc.detail if exc.detail else "An error occured. please check your rquest and try again"

  return templates.TemplateResponse(
    request, "error_page.html", 
    {
      "status_code": exc.status_code,
      "title": exc.status_code,
      "message": message
    }, status_code=exc.status_code)