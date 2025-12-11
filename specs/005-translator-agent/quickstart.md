# Quickstart: TranslatorAgent

## Overview
The TranslatorAgent provides translation services for the Physical AI & Humanoid Robotics book content. It offers both text translation and language detection capabilities through a REST API.

## Prerequisites
- Python 3.11+
- FastAPI
- Translation API key (Google Translate or similar free service)
- Language detection library (langdetect)

## Setup

### 1. Environment Variables
Create a `.env` file with the following:
```bash
TRANSLATION_API_KEY=your_translation_api_key
TRANSLATION_API_URL=https://translation.googleapis.com/language/translate/v2  # or equivalent
DETECTION_API_URL=https://translation.googleapis.com/language/translate/v2/detect  # or equivalent
```

### 2. Installation
```bash
pip install fastapi uvicorn langdetect requests python-dotenv
```

### 3. Run the Service
```bash
uvicorn backend.api.v1.translator:app --reload --port 8000
```

## API Usage

### Translate Text
```bash
curl -X POST "http://localhost:8000/api/v1/translate" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "text": "The robot uses SLAM algorithms for navigation.",
    "target_language": "es",
    "preserve_formatting": true
  }'
```

### Detect Language
```bash
curl -X POST "http://localhost:8000/api/v1/detect-language" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "text": "Le robot utilise des algorithmes SLAM pour la navigation."
  }'
```

## Key Features
- Translation between 10+ languages
- Automatic source language detection
- Technical terminology preservation
- Rate limiting with user notifications
- Anonymous processing (no user data stored)
- 1000 character limit per request