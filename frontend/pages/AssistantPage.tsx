import { useState } from "react";

import AnalysisResultCard from "../components/AnalysisResultCard";
import { askAssistant, type AnalysisResult } from "../services/api";

export default function AssistantPage() {
  const [question, setQuestion] = useState("Why is my pod crashing?");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const ask = async () => {
    try {
      setLoading(true);
      setError(null);
      setResult(await askAssistant(question));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Assistant request failed");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="grid gap-5 lg:grid-cols-2">
      <div className="panel space-y-4">
        <h2 className="text-2xl font-extrabold text-steel">AI DevOps Chat Assistant</h2>
        <p className="text-sm text-steel/80">
          Ask troubleshooting questions about Kubernetes, CI/CD failures, Linux logs, and cloud operations.
        </p>
        <textarea
          className="h-40 w-full rounded-xl border border-steel/20 p-3"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button
          type="button"
          disabled={loading || question.trim().length < 10}
          onClick={ask}
          className="rounded-xl bg-steel px-5 py-3 text-sm font-bold text-white disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? "Thinking..." : "Ask Assistant"}
        </button>
      </div>
      <AnalysisResultCard title="Assistant Response" result={result} loading={loading} error={error} />
    </section>
  );
}
