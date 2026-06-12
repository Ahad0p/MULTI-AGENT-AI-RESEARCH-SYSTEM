# Multi-Agent AI Research System

A Python application that automates research using a four-stage LangChain pipeline: **Search → Read → Write → Critic**. Users submit a topic through a Streamlit web UI (or CLI), and the system gathers web results, scrapes relevant content, drafts a structured report, and produces critic feedback.

## Features

- **Search Agent** — finds recent, reliable information via [Tavily](https://tavily.com/)
- **Reader Agent** — selects a relevant URL and scrapes page content
- **Writer Chain** — generates a structured research report (introduction, findings, conclusion, sources)
- **Critic Chain** — scores and reviews the report with actionable feedback
- **Streamlit UI** — interactive web interface with downloadable reports
- **Production deployment** — Docker, Docker Compose, Kubernetes, and Jenkins CI/CD included

## Architecture

```
User Topic
    │
    ▼
┌─────────────┐     Tavily API
│ Search Agent│ ─────────────────► web_search tool
└──────┬──────┘
       ▼
┌─────────────┐     HTTP + BeautifulSoup
│ Reader Agent│ ─────────────────► scrape_url tool
└──────┬──────┘
       ▼
┌─────────────┐     Groq LLM
│Writer Chain │ ─────────────────► structured report
└──────┬──────┘
       ▼
┌─────────────┐     Groq LLM
│Critic Chain │ ─────────────────► score + feedback
└──────┬──────┘
       ▼
  Streamlit UI
```

| Component | Technology |
|---|---|
| UI | Streamlit |
| LLM | Groq (`openai/gpt-oss-120b` via `langchain-groq`) |
| Agents | LangChain |
| Web search | Tavily |
| Scraping | `requests` + BeautifulSoup |
| Python | 3.12 |

## Project Structure

```
├── agents.py          # LangChain agents and writer/critic chains
├── pipeline.py        # Multi-agent orchestration (CLI entry point)
├── streamlit.py       # Streamlit web UI
├── tools.py           # web_search and scrape_url tools
├── main.py            # Placeholder stub
├── requirements.txt   # Python dependencies
├── Dockerfile         # Multi-stage production image
├── docker-compose.yml # Local container orchestration
├── Jenkinsfile        # CI/CD pipeline
└── k8s/               # Kubernetes manifests
    ├── namespace.yaml
    ├── configmap.yaml
    ├── secret.yaml
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    └── hpa.yaml
```

## Prerequisites

- Python 3.12
- [Groq API key](https://console.groq.com/)
- [Tavily API key](https://tavily.com/)

For containerized deployment:

- Docker and Docker Compose
- Kubernetes cluster (for K8s deployment)
- Jenkins (for CI/CD pipeline)

## Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | Yes | API key for Groq LLM (used by `ChatGroq`) |
| `TAVILY_API_KEY` | Yes | API key for Tavily web search |

## Local Development

### 1. Clone and install

```bash
git clone https://github.com/Ahad0p/MULTI-AGENT-AI-RESEARCH-SYSTEM.git
cd MULTI-AGENT-AI-RESEARCH-SYSTEM

python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 2. Run the Streamlit UI

```bash
streamlit run streamlit.py
```

Open [http://localhost:8501](http://localhost:8501), enter a research topic, and click **Generate Research**.

### 3. Run from CLI

```bash
python pipeline.py
```

## Docker

### Build

```bash
docker build -t ahadkhan021/multi-agent-ai-research-system:latest .
```

### Run

```bash
docker run --rm -p 8501:8501 \
  -e GROQ_API_KEY=your_groq_api_key \
  -e TAVILY_API_KEY=your_tavily_api_key \
  ahadkhan021/multi-agent-ai-research-system:latest
```

### Docker Compose

```bash
# Ensure .env contains GROQ_API_KEY and TAVILY_API_KEY
docker compose up --build -d
```

Access the app at [http://localhost:8501](http://localhost:8501).

Health check endpoint: `GET /_stcore/health` on port `8501`.

## Kubernetes

### Deploy

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml

kubectl create secret generic multi-agent-research-secrets \
  --namespace=multi-agent-research \
  --from-literal=GROQ_API_KEY=your_groq_api_key \
  --from-literal=TAVILY_API_KEY=your_tavily_api_key

kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/hpa.yaml
```

### Verify

```bash
kubectl get pods -n multi-agent-research
kubectl rollout status deployment/multi-agent-research -n multi-agent-research
```

Update the host in `k8s/ingress.yaml` (`research.example.com`) to your domain before production use.

### Rollback

```bash
kubectl rollout undo deployment/multi-agent-research -n multi-agent-research
```

## Jenkins CI/CD

The `Jenkinsfile` defines a declarative pipeline:

1. Checkout source code
2. Install dependencies
3. Run syntax validation (`py_compile`)
4. Build Docker image
5. Push to Docker Hub (`ahadkhan021/multi-agent-ai-research-system`)
6. Deploy to Kubernetes
7. Verify deployment
8. Auto-rollback on failure

### Required Jenkins credentials

| Credential ID | Type | Description |
|---|---|---|
| `dockerhub-credentials` | Username/Password | Docker Hub login for `ahadkhan021` |
| `kubeconfig-credentials` | Secret file | Kubernetes cluster kubeconfig |
| `groq-api-key` | Secret text | Groq API key |
| `tavily-api-key` | Secret text | Tavily API key |

### Required Jenkins plugins

Pipeline, Git, Credentials Binding, Docker Pipeline, Kubernetes CLI, Timestamper, Workspace Cleanup

## Deployment Flow

```
Developer Push → GitHub → Jenkins Pipeline → Build & Test
    → Docker Build → Docker Hub (ahadkhan021) → Kubernetes Deploy → Verification
```

## License

This project is provided as-is for research and educational purposes.
