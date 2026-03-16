from ai.base import AIEngine
from models.schemas import AIAnalysisResult, LogAnalysisRequest, TroubleshootingRequest


class AnalysisService:
    """Application service coordinating AI analysis use-cases."""

    def __init__(self, ai_engine: AIEngine) -> None:
        self.ai_engine = ai_engine

    async def analyze_logs(self, request: LogAnalysisRequest) -> AIAnalysisResult:
        return await self.ai_engine.analyze_logs(logs=request.content, context=request.context)

    async def analyze_pipeline_failure(self, request: LogAnalysisRequest) -> AIAnalysisResult:
        pipeline_context = request.context or "GitHub Actions / CI-CD pipeline"
        return await self.ai_engine.analyze_logs(logs=request.content, context=pipeline_context)

    async def troubleshoot_kubernetes(self, request: TroubleshootingRequest) -> AIAnalysisResult:
        describe_output = request.describe_output or ""
        return await self.ai_engine.troubleshoot_kubernetes(
            describe_output=describe_output,
            pod_logs=request.pod_logs,
        )

    async def answer_devops_question(self, question: str) -> AIAnalysisResult:
        return await self.ai_engine.analyze_logs(
            logs=question,
            context="DevOps assistant Q&A",
        )
