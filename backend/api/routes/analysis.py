from fastapi import APIRouter, Depends, File, UploadFile

from api.deps import get_analysis_service, get_dashboard_service
from models.schemas import AIAnalysisResult, DashboardHealthResponse, LogAnalysisRequest, TroubleshootingRequest
from services.analysis_service import AnalysisService
from services.dashboard_service import DashboardService

router = APIRouter(prefix="/api/v1", tags=["analysis"])


@router.post("/analyze/log", response_model=AIAnalysisResult)
async def analyze_log_file(
    request: LogAnalysisRequest,
    service: AnalysisService = Depends(get_analysis_service),
) -> AIAnalysisResult:
    return await service.analyze_logs(request)


@router.post("/analyze/log/upload", response_model=AIAnalysisResult)
async def analyze_uploaded_log(
    file: UploadFile = File(...),
    service: AnalysisService = Depends(get_analysis_service),
) -> AIAnalysisResult:
    content = (await file.read()).decode("utf-8", errors="ignore")
    request = LogAnalysisRequest(source="log_file", content=content)
    return await service.analyze_logs(request)


@router.post("/analyze/cicd", response_model=AIAnalysisResult)
async def analyze_cicd_failure(
    request: LogAnalysisRequest,
    service: AnalysisService = Depends(get_analysis_service),
) -> AIAnalysisResult:
    return await service.analyze_pipeline_failure(request)


@router.post("/troubleshoot/kubernetes", response_model=AIAnalysisResult)
async def troubleshoot_kubernetes(
    request: TroubleshootingRequest,
    service: AnalysisService = Depends(get_analysis_service),
) -> AIAnalysisResult:
    return await service.troubleshoot_kubernetes(request)


@router.post("/chat", response_model=AIAnalysisResult)
async def devops_chat_assistant(
    payload: dict[str, str],
    service: AnalysisService = Depends(get_analysis_service),
) -> AIAnalysisResult:
    question = payload.get("question", "")
    return await service.answer_devops_question(question=question)


@router.get("/dashboard/health", response_model=DashboardHealthResponse)
async def infrastructure_health(
    service: DashboardService = Depends(get_dashboard_service),
) -> DashboardHealthResponse:
    return await service.get_health_snapshot()
