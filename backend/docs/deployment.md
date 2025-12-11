# TranslatorAgent Deployment Guide

## Overview

This document provides instructions for deploying the TranslatorAgent service in different environments.

## Prerequisites

- Python 3.11+
- pip package manager
- Access to translation API (e.g., Google Translate API)

## Environment Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Environment (development, staging, production)
ENVIRONMENT=development

# API Configuration
TRANSLATION_API_KEY=your_translation_api_key
TRANSLATION_API_URL=https://translation.googleapis.com/language/translate/v2
DETECTION_API_URL=https://translation.googleapis.com/language/translate/v2/detect

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=true

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600

# Character Limits
CHARACTER_LIMIT=1000

# Logging
LOG_LEVEL=INFO
```

## Running the Service

### Development

```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production

Using uvicorn with production settings:

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Or using a process manager like systemd or supervisord:

```bash
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## Docker Deployment

### Build the Image

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t translator-agent .
```

### Run the Container

```bash
docker run -d -p 8000:8000 --env-file .env translator-agent
```

## API Endpoints

### Translation
- `POST /api/v1/translate` - Translate text to target language
- `POST /api/v1/detect-language` - Detect language of input text

### Health and Monitoring
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /metrics` - Performance metrics

## Monitoring and Logging

The service includes built-in monitoring for:
- Response times (p95, p99 percentiles)
- Error rates
- Rate limit events
- API usage statistics

Logs are output to stdout in JSON format and can be collected by your logging infrastructure.

## Scaling

The service is designed to be stateless and can be scaled horizontally by running multiple instances behind a load balancer.

## Security Considerations

- API keys should be stored securely and not committed to version control
- Rate limiting is implemented to prevent abuse
- Input validation is performed on all requests
- No user data is stored by default (anonymous processing)

## Troubleshooting

### Common Issues

1. **Translation API errors**: Verify your API key and URL are correct
2. **Rate limiting**: Check your API usage against the limits
3. **Performance**: Monitor response times and scale accordingly

### Health Checks

Use the `/health` endpoint to verify service status:
```bash
curl http://localhost:8000/health
```

### Metrics

Use the `/metrics` endpoint to get performance data:
```bash
curl http://localhost:8000/metrics
```

## Updating

To update the service:
1. Pull the latest code
2. Update dependencies: `pip install -r requirements.txt`
3. Restart the service
4. Verify health status

## Rollback

To rollback to a previous version:
1. Revert to the previous code version
2. Restart the service
3. Verify health status