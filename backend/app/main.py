from fastapi import FastAPI, Request
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from .auth.router import router as auth_router
from .friends.router import router as friends_router
from .examples.auth import router as test_auth_router
from config import DB_URL, IS_DEVELOPPING

app = FastAPI()

@app.get('/')
def root():
    return {'message': 'Hello world'}

@app.middleware("http")
async def catching_exceptions(request: Request, call_next):
    if IS_DEVELOPPING:
        return await call_next(request)
    
    try:
        return await call_next(request)
    except HTTPException as ex:
        return JSONResponse(status_code=ex.status_code, 
                            content={'detail': ex.detail})
    except Exception:
        return JSONResponse(status_code=500, content={'detail': 'мы упали'})

        

app.include_router(
    auth_router
)
app.include_router(
    friends_router
)
app.include_router(
    test_auth_router
)


