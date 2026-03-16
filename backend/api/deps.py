from ai.llm_client import create_ai_engine
from config import get_settings
from services.analysis_service import AnalysisService
from services.dashboard_service import DashboardService
from services.devops_log_service import DevOpsLogService
from services.kubernetes_troubleshooter import KubernetesTroubleshooter


def get_analysis_service() -> AnalysisService:
    settings = get_settings()
    ai_engine = create_ai_engine(
        provider=settings.llm_provider,
        api_key=settings.effective_openai_key,
        model=settings.llm_model,
    )
    return AnalysisService(ai_engine=ai_engine)


def get_dashboard_service() -> DashboardService:
    return DashboardService()


def get_devops_log_service() -> DevOpsLogService:
    settings = get_settings()
    ai_engine = create_ai_engine(
        provider=settings.llm_provider,
        api_key=settings.effective_openai_key,
        model=settings.llm_model,
    )
    return DevOpsLogService(ai_engine=ai_engine)


def get_kubernetes_troubleshooter() -> KubernetesTroubleshooter:
    return KubernetesTroubleshooter()
