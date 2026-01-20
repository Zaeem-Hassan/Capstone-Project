# Capstone-Project
# 🎯 Sentiment Analysis MLOps Pipeline

[![CI Pipeline](https://github.com/Zaeem-Hassan/Capstone-Project/actions/workflows/ci.yaml/badge.svg)](https://github.com/Zaeem-Hassan/Capstone-Project/actions/workflows/ci.yaml)

An end-to-end MLOps project for sentiment analysis with automated CI/CD pipeline, model versioning, containerization, and Kubernetes deployment.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [DVC Pipeline](#dvc-pipeline)
- [CI/CD Pipeline](#cicd-pipeline)
- [Deployment](#deployment)
- [Monitoring](#monitoring)
- [API Endpoints](#api-endpoints)

## 🎯 Overview

This project implements a complete MLOps pipeline for a **Sentiment Analysis** model that classifies text as positive or negative. The pipeline includes:

- **Data Version Control (DVC)** for reproducible ML pipelines
- **MLflow** for experiment tracking and model registry
- **DagsHub** as the remote MLflow server
- **Docker** containerization
- **AWS ECR** for container registry
- **AWS EKS** for Kubernetes deployment
- **Prometheus** for metrics collection
- **Grafana** for visualization

## 🏗️ Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   GitHub    │────▶│  CI/CD      │────▶│   AWS ECR   │────▶│   AWS EKS   │
│   (Code)    │     │  (Actions)  │     │  (Docker)   │     │  (K8s)      │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
       │                   │                                       │
       │                   ▼                                       ▼
       │            ┌─────────────┐                         ┌─────────────┐
       │            │   DagsHub   │                         │ Prometheus  │
       │            │   (MLflow)  │                         │  + Grafana  │
       │            └─────────────┘                         └─────────────┘
       │
       ▼
┌─────────────┐
│     DVC     │
│  (Pipeline) │
└─────────────┘
```

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **ML Framework** | Scikit-learn |
| **Pipeline Orchestration** | DVC |
| **Experiment Tracking** | MLflow + DagsHub |
| **Web Framework** | Flask + Gunicorn |
| **Containerization** | Docker |
| **Container Registry** | AWS ECR |
| **Orchestration** | AWS EKS (Kubernetes) |
| **CI/CD** | GitHub Actions |
| **Monitoring** | Prometheus + Grafana |
| **Language** | Python 3.10 |

## 📁 Project Structure

```
Capstone-Project/
├── .github/
│   └── workflows/
│       └── ci.yaml              # CI/CD pipeline
├── data/
│   ├── raw/                     # Raw data
│   ├── interim/                 # Preprocessed data
│   └── processed/               # Feature-engineered data
├── flask_app/
│   ├── app.py                   # Flask application
│   ├── templates/
│   │   └── index.html           # Web UI
│   └── requirements.txt         # App dependencies
├── models/
│   ├── model.pkl                # Trained model
│   └── vectorizer.pkl           # Text vectorizer
├── src/
│   ├── data/
│   │   ├── data_ingestion.py    # Data loading
│   │   └── data_preprocessing.py # Text preprocessing
│   ├── features/
│   │   └── feature_engineering.py # BOW vectorization
│   └── model/
│       ├── model_building.py    # Model training
│       ├── model_evaluation.py  # Model evaluation + MLflow
│       └── register_model.py    # MLflow model registry
├── scripts/
│   └── promote_model.py         # Model promotion script
├── tests/
│   ├── test_flask_app.py        # Flask API tests
│   └── test_model.py            # Model validation tests
├── Dockerfile                   # Container definition
├── deployment.yaml              # Kubernetes manifests
├── dvc.yaml                     # DVC pipeline definition
├── params.yaml                  # Pipeline parameters
└── requirements.txt             # Project dependencies
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Git
- DVC
- Docker
- AWS CLI (for deployment)
- kubectl (for Kubernetes)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Zaeem-Hassan/Capstone-Project.git
   cd Capstone-Project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .\.venv\Scripts\Activate.ps1  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file with:
   CAPSTONE_TEST=<your-dagshub-token>
   ```

5. **Run the DVC pipeline**
   ```bash
   dvc repro
   ```

6. **Run the Flask app locally**
   ```bash
   python flask_app/app.py
   ```

## 🔄 DVC Pipeline

The ML pipeline consists of 6 stages:

```
data_ingestion → data_preprocessing → feature_engineering → model_building → model_evaluation → model_registration
```

| Stage | Description | Output |
|-------|-------------|--------|
| `data_ingestion` | Load and split data | `data/raw/` |
| `data_preprocessing` | Clean and preprocess text | `data/interim/` |
| `feature_engineering` | Apply Bag of Words | `data/processed/`, `models/vectorizer.pkl` |
| `model_building` | Train classifier | `models/model.pkl` |
| `model_evaluation` | Evaluate & log to MLflow | `reports/metrics.json` |
| `model_registration` | Register model in MLflow | Model in registry |

### Run Pipeline
```bash
dvc repro           # Run entire pipeline
dvc repro -s <stage> # Run specific stage
```

## 🔁 CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yaml`) automates:

1. **Run DVC Pipeline** - Reproduces ML pipeline
2. **Model Tests** - Validates model performance
3. **Promote Model** - Promotes staging model to production
4. **Flask Tests** - Tests API endpoints
5. **Build & Push Docker** - Pushes to AWS ECR
6. **Deploy to EKS** - Updates Kubernetes deployment

### Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `CAPSTONE_TEST` | DagsHub access token |
| `AWS_ACCESS_KEY_ID` | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key |
| `AWS_REGION` | AWS region (e.g., `us-east-1`) |
| `AWS_ACCOUNT_ID` | AWS account ID |
| `ECR_REPOSITORY` | ECR repository name |

## 🐳 Deployment

### Docker

```bash
# Build image
docker build -t sentiment-app .

# Run locally
docker run -p 5000:5000 -e CAPSTONE_TEST=<token> sentiment-app
```

### Kubernetes (EKS)

```bash
# Create EKS cluster
eksctl create cluster --name flask-app-cluster --region us-east-1 --node-type t3.small --nodes 1

# Deploy application
kubectl apply -f deployment.yaml

# Check status
kubectl get pods
kubectl get svc
```

## 📊 Monitoring

### Prometheus Metrics

The Flask app exposes custom metrics at `/metrics`:

- `app_request_count_total` - Total requests by endpoint
- `app_request_latency_seconds` - Request latency histogram
- `model_prediction_count` - Predictions by class

### Prometheus Configuration

```yaml
scrape_configs:
  - job_name: "flask-app"
    scrape_interval: 60s
    scrape_timeout: 30s
    static_configs:
      - targets: ["<load-balancer-url>:5000"]
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page with input form |
| `/predict` | POST | Predict sentiment for text |
| `/metrics` | GET | Prometheus metrics |

### Example Request

```bash
curl -X POST http://localhost:5000/predict \
  -d "text=I love this product!"
```

## 📈 Model Performance

| Metric | Value |
|--------|-------|
| Accuracy | ~85% |
| Precision | ~85% |
| Recall | ~85% |
| AUC | ~92% |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

**Zaeem Hassan**

- GitHub: [@Zaeem-Hassan](https://github.com/Zaeem-Hassan)
