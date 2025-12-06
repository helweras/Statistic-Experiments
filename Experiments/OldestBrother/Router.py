from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/experiment_2",
    tags=["OldestBrother"]
)


@router.get("/")
def info():
    return {"experiment": "OldestBrother"}
