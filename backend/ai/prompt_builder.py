def build_log_analysis_prompt(logs: str, context: str | None = None) -> str:
    context_block = f"Context: {context}\n" if context else ""
    return (
        "You are a senior DevOps incident responder. "
        "Analyze the logs, identify the most probable root cause, and provide concise fixes.\n"
        f"{context_block}"
        f"Logs:\n{logs}\n"
        "Respond with summary, root cause, confidence, fixes, and follow-up checks."
    )


def build_kubernetes_prompt(describe_output: str, pod_logs: str | None = None) -> str:
    logs_section = f"Pod logs:\n{pod_logs}\n" if pod_logs else ""
    return (
        "You are a Kubernetes SRE specialist. Diagnose the issue using kubectl describe output "
        "and optional pod logs, then return practical remediation steps.\n"
        f"Describe output:\n{describe_output}\n"
        f"{logs_section}"
        "Respond with summary, root cause, confidence, fixes, and follow-up checks."
    )
