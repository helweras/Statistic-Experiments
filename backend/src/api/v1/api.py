from fastapi import APIRouter
from src.api.v1.metadata import ExperimentList, EXPERIMENTS_RESPONSE
from src.experiments.MontyHall.router import router as router_monty_hall
router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/experiments", response_model=ExperimentList)
async def get_metadata():
    return EXPERIMENTS_RESPONSE

router.include_router(router_monty_hall)
