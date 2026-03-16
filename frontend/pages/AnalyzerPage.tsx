import { useState } from "react";

import AnalysisResultCard from "../components/AnalysisResultCard";
import { analyzeCiCd, analyzeLogs, troubleshootKubernetes, type AnalysisResult } from "../services/api";

type AnalyzerMode = "logs" | "cicd" | "k8s";

export default function AnalyzerPage() {
  const [mode, setMode] = useState<AnalyzerMode>("logs");
  const [primaryInput, setPrimaryInput] = useState("");
  const [secondaryInput, setSecondaryInput] = useState("");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const runAnalysis = async () => {
    try {
      setLoading(true);
      setError(null);
      if (mode === "logs") {
        setResult(await analyzeLogs(primaryInput));
      } else if (mode === "cicd") {
        setResult(await analyzeCiCd(primaryInput));
      } else {
        setResult(await troubleshootKubernetes(primaryInput, secondaryInput));
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="grid gap-5 lg:grid-cols-2">
      <div className="panel space-y-4">
        <h2 className="text-2xl font-extrabold text-steel">Diagnostic Analyzer</h2>
        <div className="flex flex-wrap gap-2">
          {[
            { key: "logs", label: "Log Analyzer" },
            { key: "cicd", label: "CI/CD Analyzer" },
            { key: "k8s", label: "Kubernetes Troubleshooter" },
          ].map((item) => (
            <button
              key={item.key}
              type="button"
              onClick={() => setMode(item.key as AnalyzerMode)}
              className={`rounded-full px-4 py-2 text-sm font-bold transition ${
                mode === item.key ? "bg-steel text-white" : "bg-steel/10 text-steel"
              }`}
            >
              {item.label}
            </button>
          ))}
        </div>

        <label className="block text-sm font-semibold text-steel">
          {mode === "k8s" ? "kubectl describe output or logs" : "Paste logs"}
          <textarea
            className="mt-2 h-52 w-full rounded-xl border border-steel/20 p-3"
            value={primaryInput}
            onChange={(e) => setPrimaryInput(e.target.value)}
            placeholder="Paste diagnostic output here..."
          />
        </label>

        {mode === "k8s" && (
          <label className="block text-sm font-semibold text-steel">
            Optional pod logs
            <textarea
              className="mt-2 h-36 w-full rounded-xl border border-steel/20 p-3"
              value={secondaryInput}
              onChange={(e) => setSecondaryInput(e.target.value)}
              placeholder="Additional pod logs..."
            />
          </label>
        )}

        <button
          type="button"
          disabled={loading || primaryInput.trim().length < 10}
          onClick={runAnalysis}
          className="rounded-xl bg-ember px-5 py-3 text-sm font-bold text-white disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? "Running analysis..." : "Run AI Analysis"}
        </button>
      </div>

      <AnalysisResultCard
        title="AI Diagnosis"
        result={result}
        loading={loading}
        error={error}
      />
    </section>
  );
}
