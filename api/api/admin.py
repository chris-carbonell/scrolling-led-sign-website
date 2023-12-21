# Dependencies

# api
from fastapi import APIRouter

# Router
router = APIRouter()

# Endpoints

@router.get("/healthcheck")
async def root():
    '''
    health check for container
    '''
    # TODO: return HTTP error if necessary table doesnt exist
    return