from abc import ABC, abstractmethod

from models.schemas import AIAnalysisResult


class AIEngine(ABC):
    """Abstraction for any LLM/AI provider used by DevOpsBrain."""

    @abstractmethod
    async def analyze_logs(self, logs: str, context: str | None = None) -> AIAnalysisResult:
        """Analyze logs and return root-cause insights."""

    @abstractmethod
    async def troubleshoot_kubernetes(self, describe_output: str, pod_logs: str | None = None) -> AIAnalysisResult:
        """Analyze kubernetes diagnostics and return troubleshooting guidance."""
