from fastapi import APIRouter

from models.schemas import APIResponse

router = APIRouter(tags=["system"])


@router.get("/health", response_model=APIResponse)
async def health_check() -> APIResponse:
    return APIResponse(ok=True, message="DevOpsBrain API is healthy")
