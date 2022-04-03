from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from api.api_v1.endpoints import login, users, items
from fastapi.responses import JSONResponse
from api import deps 
import logging

logger = logging.getLogger('caloriemeter')

api_router = APIRouter()

@api_router.get("/healthcheck")
def db_available(db: Session = Depends(deps.get_db)):
    try:
        db.execute('SELECT 1')
        db.commit()
        logger.info('DB connection is OK')
        return JSONResponse(
            content={'message': 'healthy'},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        logger.exception('DB connection is not OK, Exception: {}'.format(e))
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='unhealthy')

api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
