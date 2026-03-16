from fastapi import APIRouter, Depends

from api.deps import get_devops_log_service, get_kubernetes_troubleshooter
from models.schemas import (
    DevOpsLogAnalysisRequest,
    DevOpsLogAnalysisResponse,
    KubernetesTroubleshootRequest,
    KubernetesTroubleshootResponse,
)
from services.devops_log_service import DevOpsLogService
from services.kubernetes_troubleshooter import KubernetesTroubleshooter

router = APIRouter(prefix="/api/v1", tags=["devops"])


@router.post("/analyze-log", response_model=DevOpsLogAnalysisResponse)
async def analyze_log(
    request: DevOpsLogAnalysisRequest,
    service: DevOpsLogService = Depends(get_devops_log_service),
) -> DevOpsLogAnalysisResponse:
    return await service.analyze(request)


@router.post("/troubleshoot-kubernetes", response_model=KubernetesTroubleshootResponse)
def troubleshoot_kubernetes_module(
    request: KubernetesTroubleshootRequest,
    service: KubernetesTroubleshooter = Depends(get_kubernetes_troubleshooter),
) -> KubernetesTroubleshootResponse:
    return service.troubleshoot(request)
