# GitHub Actions Workflows

This directory contains CI/CD workflows for the FastAPI Kubernetes Demo project.

## Workflows Overview

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ci.yml` | Push, PR | Lint, test, build Docker image |
| `deploy-dev.yml` | Push to develop, Manual | Deploy to development |
| `deploy-prod.yml` | Manual only | Deploy to production |

## CI Workflow (`ci.yml`)

Runs on every push and pull request:
1. **Lint & Test**: Python linting and pytest
2. **Build**: Docker image build and push to GitHub Container Registry
3. **Helm Lint**: Validates Helm chart

## Setup Requirements

### 1. Enable GitHub Container Registry

The CI workflow uses GitHub Container Registry (ghcr.io). It works automatically with `GITHUB_TOKEN`.

### 2. Configure Secrets (for deployment workflows)

Go to **Settings → Secrets and variables → Actions** and add:

| Secret | Description | Required For |
|--------|-------------|--------------|
| `KUBE_CONFIG` | Base64 encoded kubeconfig | Dev deployment |
| `KUBE_CONFIG_PROD` | Base64 encoded prod kubeconfig | Prod deployment |

**To encode kubeconfig:**
```bash
cat ~/.kube/config | base64 -w 0
```

### 3. Create Environments (optional but recommended)

Go to **Settings → Environments** and create:
- `development` - No protection rules needed
- `production` - Add required reviewers for safety

## Usage

### Run Tests Locally
```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

### Trigger Dev Deployment
Push to `develop` branch or manually trigger from Actions tab.

### Trigger Prod Deployment
1. Go to Actions → "Deploy to Production"
2. Click "Run workflow"
3. Enter image tag (e.g., `abc123` or `latest`)
4. Type `DEPLOY` to confirm
5. Click "Run workflow"

## Image Tags

The CI workflow creates these image tags:
- `latest` - Main/master branch
- `<branch-name>` - Feature branches
- `<commit-sha>` - Every commit
- `pr-<number>` - Pull requests
