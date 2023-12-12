# Dependencies

# api
from fastapi import APIRouter

# Router
router = APIRouter()

# Endpoints

@router.get("/healthcheck", tags=["api|admin|get"])
async def root():
    '''
    health check for container
    '''
    # TODO: return HTTP error if necessary table doesnt exist
    return