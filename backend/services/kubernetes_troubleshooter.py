from models.schemas import (
    KubernetesIssueSuggestion,
    KubernetesTroubleshootRequest,
    KubernetesTroubleshootResponse,
)


class KubernetesTroubleshooter:
    """Rule-based Kubernetes diagnostics that produce actionable kubectl commands."""

    def troubleshoot(self, request: KubernetesTroubleshootRequest) -> KubernetesTroubleshootResponse:
        combined = f"{request.kubectl_describe_output}\n{request.kubectl_logs_output or ''}".lower()
        suggestions: list[KubernetesIssueSuggestion] = []

        if "crashloopbackoff" in combined:
            suggestions.append(
                KubernetesIssueSuggestion(
                    issue="CrashLoopBackOff",
                    root_cause="Container process exits repeatedly shortly after startup.",
                    recommended_fix="Verify startup command, environment variables, and mounted secrets/config.",
                    kubectl_commands=[
                        "kubectl describe pod <pod-name> -n <namespace>",
                        "kubectl logs <pod-name> -n <namespace> --previous",
                        "kubectl rollout restart deployment/<deployment-name> -n <namespace>",
                    ],
                    confidence="high",
                )
            )

        if "imagepullbackoff" in combined or "errimagepull" in combined:
            suggestions.append(
                KubernetesIssueSuggestion(
                    issue="ImagePullBackOff",
                    root_cause="Kubernetes cannot pull the container image (tag, auth, or registry reachability).",
                    recommended_fix="Validate image tag, registry credentials, and imagePullSecrets.",
                    kubectl_commands=[
                        "kubectl get pod <pod-name> -n <namespace> -o wide",
                        "kubectl describe pod <pod-name> -n <namespace>",
                        "kubectl get secret -n <namespace>",
                    ],
                    confidence="high",
                )
            )

        if "oomkilled" in combined or "out of memory" in combined:
            suggestions.append(
                KubernetesIssueSuggestion(
                    issue="OOMKilled",
                    root_cause="Container exceeded configured memory limit and was terminated by the kernel.",
                    recommended_fix="Increase memory limits/requests and optimize memory consumption.",
                    kubectl_commands=[
                        "kubectl top pod <pod-name> -n <namespace>",
                        "kubectl describe pod <pod-name> -n <namespace>",
                        "kubectl set resources deployment/<deployment-name> -n <namespace> --limits=memory=1Gi --requests=memory=512Mi",
                    ],
                    confidence="high",
                )
            )

        if "failedscheduling" in combined or "0/" in combined and "nodes are available" in combined:
            suggestions.append(
                KubernetesIssueSuggestion(
                    issue="FailedScheduling",
                    root_cause="Scheduler could not place pod due to resource pressure or scheduling constraints.",
                    recommended_fix="Relax scheduling constraints or add cluster capacity.",
                    kubectl_commands=[
                        "kubectl describe pod <pod-name> -n <namespace>",
                        "kubectl get nodes",
                        "kubectl top nodes",
                    ],
                    confidence="medium",
                )
            )

        if "liveness probe failed" in combined:
            suggestions.append(
                KubernetesIssueSuggestion(
                    issue="LivenessProbeFailed",
                    root_cause="Health probe endpoint/command is failing and kubelet is restarting the container.",
                    recommended_fix="Adjust probe settings and verify probe endpoint availability inside container.",
                    kubectl_commands=[
                        "kubectl describe pod <pod-name> -n <namespace>",
                        "kubectl logs <pod-name> -n <namespace>",
                        "kubectl edit deployment <deployment-name> -n <namespace>",
                    ],
                    confidence="high",
                )
            )

        if not suggestions:
            suggestions.append(
                KubernetesIssueSuggestion(
                    issue="Unknown",
                    root_cause="No known pattern detected from provided describe/log output.",
                    recommended_fix="Inspect Events and previous container logs for first-error indicators.",
                    kubectl_commands=[
                        "kubectl describe pod <pod-name> -n <namespace>",
                        "kubectl logs <pod-name> -n <namespace> --previous",
                        "kubectl get events -n <namespace> --sort-by=.lastTimestamp",
                    ],
                    confidence="low",
                )
            )

        return KubernetesTroubleshootResponse(
            summary="Kubernetes troubleshooting analysis completed.",
            detected_issues=[item.issue for item in suggestions],
            suggestions=suggestions,
        )
