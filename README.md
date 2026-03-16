# DevOpsBrain

DevOpsBrain is an AI-powered DevOps assistant designed to help engineers diagnose failures quickly and apply actionable fixes.

## MVP Capabilities

- Log Analyzer: upload/paste logs and receive root-cause insights.
- CI/CD Failure Analyzer: explain pipeline failures from raw job logs.
- Kubernetes Troubleshooter: analyze `kubectl describe` output and pod logs.
- Infrastructure Health Dashboard: show cluster status, pod failures, and resource usage.
- AI DevOps Chat Assistant: answer troubleshooting questions in natural language.

## Architecture

DevOpsBrain follows a modular architecture so each capability evolves independently:

- API layer: FastAPI routes and request/response contracts.
- Service layer: orchestration and use-case logic.
- AI layer: provider-agnostic engine interface and implementation factory.
- Integration layer: external systems (GitHub, Kubernetes, Prometheus).
- Worker layer: async task execution entry points.
- Frontend: React + Tailwind dashboard for incident workflows.

## Project Structure

```text
backend/
	api/
		routes/
			analysis.py
			health.py
		app.py
		deps.py
	services/
		analysis_service.py
		dashboard_service.py
	ai/
		base.py
		llm_client.py
		prompt_builder.py
	integrations/
		github.py
		kubernetes.py
		prometheus.py
	models/
		schemas.py
	workers/
		tasks.py
	config.py
	main.py
	requirements.txt

frontend/
	components/
		AnalysisResultCard.tsx
		MetricCard.tsx
	pages/
		AnalyzerPage.tsx
		AssistantPage.tsx
		DashboardPage.tsx
	services/
		api.ts
	src/
		App.tsx
		main.tsx
		index.css
```

## Backend Quick Start

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Backend URL: `http://localhost:8000`
Swagger docs: `http://localhost:8000/docs`

## Frontend Quick Start

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:5173`

To point frontend to a different API URL:

```bash
echo "VITE_API_URL=http://localhost:8000" > frontend/.env
```

## Example API Requests

Analyze log snippet:

```bash
curl -X POST http://localhost:8000/api/v1/analyze/log \
	-H "Content-Type: application/json" \
	-d '{
		"source": "log_file",
		"content": "Error: ImagePullBackOff pulling app:v2"
	}'
```

Troubleshoot Kubernetes issue:

```bash
curl -X POST http://localhost:8000/api/v1/troubleshoot/kubernetes \
	-H "Content-Type: application/json" \
	-d '{
		"resource_type": "pod",
		"resource_name": "payments-api-77fdb",
		"describe_output": "State: Waiting, Reason: CrashLoopBackOff",
		"pod_logs": "panic: unable to load config"
	}'
```

## Design Notes

- AI provider abstraction is implemented through `AIEngine` so you can plug in OpenAI, Azure OpenAI, or local models later.
- API endpoints stay thin; business logic lives in services.
- Integration modules are isolated from route logic for easier testing.
- Worker layer is prepared for Redis-backed async processing (Celery/RQ style).

This scaffold is intentionally production-oriented in structure while keeping MVP behavior simple and easy to extend.