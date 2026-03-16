export type AnalysisResult = {
  summary: string;
  probable_root_cause: string;
  confidence: number;
  suggested_fixes: string[];
  follow_up_checks: string[];
};

export type DashboardHealth = {
  cluster_status: { name: string; status: string; value: string; updated_at: string };
  pod_failures: { name: string; status: string; value: string; updated_at: string };
  resource_usage: { name: string; status: string; value: string; updated_at: string };

export type DevOpsLogAnalysisResponse = {
  summary: string;
  root_cause: string;
  recommended_fix: string;
  confidence: "low" | "medium" | "high";
};

export type KubernetesIssueSuggestion = {
  issue: string;
  root_cause: string;
  recommended_fix: string;
  kubectl_commands: string[];
  confidence: "low" | "medium" | "high";
};

export type KubernetesTroubleshootResponse = {
  summary: string;
  detected_issues: string[];
  suggestions: KubernetesIssueSuggestion[];
};
};

const BASE_URL = import.meta.env.VITE_API_URL ?? "";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...(options?.headers ?? {}) },
    ...options,
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed with status ${response.status}`);
  }

  return (await response.json()) as T;
}

export function fetchDashboardHealth(): Promise<DashboardHealth> {
  return request<DashboardHealth>("/api/v1/dashboard/health");
}

export function analyzeLogs(content: string): Promise<AnalysisResult> {
  return request<AnalysisResult>("/api/v1/analyze/log", {
    method: "POST",
    body: JSON.stringify({ source: "log_file", content }),
  });
}

export function analyzeCiCd(content: string): Promise<AnalysisResult> {
  return request<AnalysisResult>("/api/v1/analyze/cicd", {
    method: "POST",
    body: JSON.stringify({ source: "pipeline", content }),
  });
}

export function troubleshootKubernetes(describeOutput: string, podLogs: string): Promise<AnalysisResult> {
  return request<AnalysisResult>("/api/v1/troubleshoot/kubernetes", {
    method: "POST",
    body: JSON.stringify({ describe_output: describeOutput, pod_logs: podLogs }),
  });
}

export function askAssistant(question: string): Promise<AnalysisResult> {
  return request<AnalysisResult>("/api/v1/chat", {
    method: "POST",
    body: JSON.stringify({ question }),

  export function analyzeDevOpsLog(rawLogText: string): Promise<DevOpsLogAnalysisResponse> {
    return request<DevOpsLogAnalysisResponse>("/api/v1/analyze-log", {
      method: "POST",
      body: JSON.stringify({ raw_log_text: rawLogText }),
    });
  }

  export function troubleshootKubernetesModule(
    kubectlDescribeOutput: string,
    kubectlLogsOutput?: string,
  ): Promise<KubernetesTroubleshootResponse> {
    return request<KubernetesTroubleshootResponse>("/api/v1/troubleshoot-kubernetes", {
      method: "POST",
      body: JSON.stringify({
        kubectl_describe_output: kubectlDescribeOutput,
        kubectl_logs_output: kubectlLogsOutput ?? null,
      }),
    });
  }
  });
}
