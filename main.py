from fastapi import FastAPI, Security, Request
from starlette.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse
# from fastapi.staticfiles import StaticFiles
from api.api_v1.api import api_router
from core.config import settings
from core.security import get_api_key
import logging

logger = logging.getLogger('CalorieMeter')

app = FastAPI(
    title=settings.PROJECT_NAME, 
    openapi_url=f"{settings.API_V1_STR}/openapi.json", 
    # dependencies=[Security(get_api_key)]
)

# app.mount("/static", StaticFiles(directory="static"), name="static")

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get('/')
def root():
    return {'message': 'Hello World'}

@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    #log your exception here
    # you can also request details by using request object  
    logger.exception('Request: {} & Exception: {}'.format(request, exc))
    return JSONResponse(
        content = { "error": f"Oops! {exc} did something wrong."},
        status_code=500
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000, host='0.0.0.0')
