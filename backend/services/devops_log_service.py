from typing import Literal

from ai.base import AIEngine
from models.schemas import DevOpsLogAnalysisRequest, DevOpsLogAnalysisResponse


class DevOpsLogService:
    """LLM-backed service that converts raw logs into structured incident guidance."""

    def __init__(self, ai_engine: AIEngine) -> None:
        self.ai_engine = ai_engine

    async def analyze(self, request: DevOpsLogAnalysisRequest) -> DevOpsLogAnalysisResponse:
        source = self._detect_source(request.raw_log_text)
        ai_result = await self.ai_engine.analyze_logs(
            logs=request.raw_log_text,
            context=f"Detected source: {source}",
        )

        fix_text = " ".join(ai_result.suggested_fixes[:3])
        return DevOpsLogAnalysisResponse(
            summary=ai_result.summary,
            root_cause=ai_result.probable_root_cause,
            recommended_fix=fix_text,
            confidence=self._map_confidence(ai_result.confidence),
        )

    def _detect_source(self, logs: str) -> Literal["kubernetes", "docker", "cicd", "linux"]:
        lowered = logs.lower()
        if any(token in lowered for token in ["kubectl", "pod", "crashloopbackoff", "kubelet"]):
            return "kubernetes"
        if any(token in lowered for token in ["docker", "container", "image", "docker-compose"]):
            return "docker"
        if any(token in lowered for token in ["github actions", "gitlab-ci", "jenkins", "pipeline"]):
            return "cicd"
        return "linux"

    def _map_confidence(self, score: float) -> Literal["low", "medium", "high"]:
        if score < 0.45:
            return "low"
        if score < 0.75:
            return "medium"
        return "high"
